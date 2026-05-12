#!/usr/bin/env python3
"""
xui-mon — management CLI for xui-dashboard & xui-monitor services.

Usage:
  xui-mon status
  xui-mon start | stop | restart
  xui-mon remove
  xui-mon user <new-username>
  xui-mon pass <new-password>
  xui-mon port <number>
  xui-mon https on  [--cert /path/fullchain.pem --key /path/privkey.pem]
  xui-mon https off
"""

import hashlib
import os
import sqlite3
import subprocess
import sys

APP_DB   = "/opt/xui-monitor/app.db"
SVC_DASH = "xui-dashboard"
SVC_MON  = "xui-monitor"

# ── ANSI colours ──────────────────────────────────────────────────────────────
R  = "\033[0;31m";  G  = "\033[0;32m";  Y  = "\033[0;33m"
B  = "\033[0;34m";  C  = "\033[0;36m";  W  = "\033[0;37m"
BLD= "\033[1m";     DIM= "\033[2m";     RST= "\033[0m"

def ok(msg):   print(f"  {G}✔{RST}  {msg}")
def err(msg):  print(f"  {R}✘{RST}  {msg}"); sys.exit(1)
def info(msg): print(f"  {C}→{RST}  {msg}")
def warn(msg): print(f"  {Y}!{RST}  {msg}")
def head(msg): print(f"\n{BLD}{msg}{RST}")

def ask(prompt) -> str:
    try:
        return input(f"  {Y}?{RST}  {prompt}: ").strip()
    except (KeyboardInterrupt, EOFError):
        print(); sys.exit(0)

# ── DB helpers ────────────────────────────────────────────────────────────────

def db_get(key: str, default: str = "") -> str:
    try:
        with sqlite3.connect(APP_DB) as c:
            row = c.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row[0] if row else default
    except Exception:
        return default

def db_set(key: str, value: str):
    try:
        with sqlite3.connect(APP_DB) as c:
            c.execute("INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)", (key, value))
    except Exception as e:
        err(f"DB write failed: {e}")

def db_get_user() -> tuple[str, str]:
    try:
        with sqlite3.connect(APP_DB) as c:
            c.row_factory = sqlite3.Row
            row = c.execute("SELECT username, password FROM admin_users LIMIT 1").fetchone()
        return (row["username"], row["password"]) if row else ("", "")
    except Exception:
        return ("", "")

def db_set_username(new_name: str):
    try:
        with sqlite3.connect(APP_DB) as c:
            old, _ = db_get_user()
            if old:
                c.execute("UPDATE admin_users SET username=? WHERE username=?", (new_name, old))
            else:
                err("No admin user found in database.")
    except Exception as e:
        err(f"DB write failed: {e}")

def db_set_password(new_pass: str):
    salt = os.urandom(16).hex()
    h    = hashlib.pbkdf2_hmac("sha256", new_pass.encode(), salt.encode(), 260_000)
    hashed = f"pbkdf2${salt}${h.hex()}"
    try:
        with sqlite3.connect(APP_DB) as c:
            c.execute("UPDATE admin_users SET password=?", (hashed,))
    except Exception as e:
        err(f"DB write failed: {e}")

# ── systemctl helpers ─────────────────────────────────────────────────────────

def svc_run(*args) -> tuple[int, str]:
    r = subprocess.run(["systemctl", *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()

def svc_active(name: str) -> bool:
    code, _ = svc_run("is-active", "--quiet", name)
    return code == 0

def svc_enabled(name: str) -> bool:
    code, _ = svc_run("is-enabled", "--quiet", name)
    return code == 0

def svc_action(name: str, action: str):
    code, out = svc_run(action, name)
    if code == 0:
        ok(f"{name}  {action}ed")
    else:
        warn(f"{name}: {out or 'no output'}")

# ── commands ──────────────────────────────────────────────────────────────────

def cmd_status():
    head("Service status")
    for svc in (SVC_DASH, SVC_MON):
        active  = f"{G}active{RST}"  if svc_active(svc)  else f"{R}inactive{RST}"
        enabled = f"{G}enabled{RST}" if svc_enabled(svc) else f"{Y}disabled{RST}"
        print(f"    {BLD}{svc:<22}{RST}  {active}  /  {enabled}")

    head("Dashboard settings")
    username, _ = db_get_user()
    port        = db_get("port", "5000")
    tls         = db_get("tls_enabled", "0")
    tls_cert    = db_get("tls_cert", "")
    tls_key     = db_get("tls_key",  "")
    domain      = db_get("tls_domain","")
    scheme      = "https" if tls == "1" else "http"
    print(f"    {'Username':<16}  {username or DIM+'(not set)'+RST}")
    print(f"    {'Port':<16}  {port}")
    print(f"    {'HTTPS':<16}  {'ON  '+G+scheme+RST if tls=='1' else Y+'OFF'+RST}")
    if tls == "1":
        print(f"    {'  cert':<16}  {tls_cert or R+'(not set)'+RST}")
        print(f"    {'  key':<16}  {tls_key  or R+'(not set)'+RST}")
        if domain:
            print(f"    {'  domain':<16}  {domain}")
    print()


def cmd_start():
    head("Start services")
    svc_action(SVC_DASH, "start")
    svc_action(SVC_MON,  "start")

def cmd_stop():
    head("Stop services")
    svc_action(SVC_DASH, "stop")
    svc_action(SVC_MON,  "stop")

def cmd_restart():
    head("Restart services")
    svc_action(SVC_DASH, "restart")
    svc_action(SVC_MON,  "restart")


def cmd_remove():
    head("Remove services")
    warn("This will STOP and DELETE both xui-dashboard and xui-monitor services.")
    warn("Files in /opt/xui-monitor/ will NOT be deleted.")
    ans = ask("Type  yes  to confirm")
    if ans != "yes":
        info("Aborted.")
        return
    for svc in (SVC_DASH, SVC_MON):
        svc_run("stop",    svc)
        svc_run("disable", svc)
        svc_file = f"/etc/systemd/system/{svc}.service"
        if os.path.exists(svc_file):
            try:
                os.remove(svc_file)
                ok(f"Removed {svc_file}")
            except PermissionError:
                err(f"Permission denied removing {svc_file} — run as root.")
    svc_run("daemon-reload")
    ok("Services removed. Data at /opt/xui-monitor/ is intact.")


def cmd_user(new_name: str):
    head("Change username")
    old, _ = db_get_user()
    if not old:
        err("No admin user found.")
    db_set_username(new_name)
    ok(f"Username changed:  {DIM}{old}{RST}  →  {BLD}{new_name}{RST}")
    info("No restart needed — takes effect on next login.")


def cmd_pass(new_pass: str):
    head("Change password")
    if len(new_pass) < 6:
        err("Password must be at least 6 characters.")
    db_set_password(new_pass)
    ok("Password updated (PBKDF2-SHA256).")
    info("No restart needed — takes effect on next login.")


def cmd_port(new_port: str):
    head("Change port")
    try:
        p = int(new_port)
        if not (1 <= p <= 65535):
            raise ValueError
    except ValueError:
        err(f"Invalid port: {new_port!r}  (must be 1–65535)")
    old = db_get("port", "5000")
    db_set("port", str(p))
    ok(f"Port changed:  {DIM}{old}{RST}  →  {BLD}{p}{RST}")
    info("Restarting dashboard to apply…")
    svc_action(SVC_DASH, "restart")


def cmd_https(args: list[str]):
    head("HTTPS / TLS")
    if not args:
        print(__doc__); sys.exit(1)

    sub = args[0].lower()

    if sub == "off":
        db_set("tls_enabled", "0")
        ok("HTTPS disabled (HTTP mode).")
        info("Restarting dashboard…")
        svc_action(SVC_DASH, "restart")
        return

    if sub == "on":
        # optional --cert / --key flags
        cert = key = ""
        i = 1
        while i < len(args):
            if args[i] in ("--cert", "-c") and i + 1 < len(args):
                cert = args[i + 1]; i += 2
            elif args[i] in ("--key", "-k") and i + 1 < len(args):
                key = args[i + 1]; i += 2
            else:
                i += 1

        # if not provided on command line, ask (or use existing)
        existing_cert = db_get("tls_cert", "")
        existing_key  = db_get("tls_key",  "")

        if not cert:
            cert = existing_cert or ask("Certificate path (fullchain.pem)")
        if not key:
            key  = existing_key  or ask("Key path (privkey.pem)")

        if not cert or not key:
            err("Certificate and key paths are required to enable HTTPS.")

        if not os.path.isfile(cert):
            err(f"Certificate file not found: {cert}")
        if not os.path.isfile(key):
            err(f"Key file not found: {key}")

        db_set("tls_enabled", "1")
        db_set("tls_cert", cert)
        db_set("tls_key",  key)
        ok(f"HTTPS enabled")
        print(f"    cert  {cert}")
        print(f"    key   {key}")
        info("Restarting dashboard…")
        svc_action(SVC_DASH, "restart")
        return

    err(f"Unknown https sub-command: {sub!r}  (use  on  or  off)")


# ── main ──────────────────────────────────────────────────────────────────────

HELP = f"""{BLD}xui-mon{RST} — xui-dashboard management CLI

{BLD}Usage:{RST}
  xui-mon status
  xui-mon start | stop | restart | remove
  xui-mon user  <new-username>
  xui-mon pass  <new-password>
  xui-mon port  <number>
  xui-mon https on  [--cert /path/fullchain.pem --key /path/privkey.pem]
  xui-mon https off
"""

def main():
    args = sys.argv[1:]
    if not args:
        print(HELP); sys.exit(0)

    cmd = args[0].lower()

    if   cmd == "status":              cmd_status()
    elif cmd == "start":               cmd_start()
    elif cmd == "stop":                cmd_stop()
    elif cmd == "restart":             cmd_restart()
    elif cmd == "remove":              cmd_remove()
    elif cmd == "user"  and len(args) >= 2: cmd_user(args[1])
    elif cmd == "pass"  and len(args) >= 2: cmd_pass(args[1])
    elif cmd == "port"  and len(args) >= 2: cmd_port(args[1])
    elif cmd == "https" and len(args) >= 2: cmd_https(args[1:])
    elif cmd in ("user", "pass", "port", "https"):
        print(HELP); sys.exit(1)
    else:
        err(f"Unknown command: {cmd!r}\n{HELP}")

if __name__ == "__main__":
    main()
