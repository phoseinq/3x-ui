#!/bin/bash
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  3x-ui Monitor Dashboard â€” one-line installer
#  Usage:
#    curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui/main/install.sh | sudo bash
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
set -e

REPO_RAW="https://raw.githubusercontent.com/phoseinq/3x-ui/main"
DIR="/opt/xui-monitor"

R='\033[0;31m'; G='\033[0;32m'; B='\033[0;34m'; Y='\033[1;33m'; C='\033[0;36m'; N='\033[0m'
ok()   { echo -e "  ${G}âœ“${N} $1"; }
info() { echo -e "  ${C}â†’${N} $1"; }
err()  { echo -e "  ${R}âœ— $1${N}"; exit 1; }

echo -e "\n${B}â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”${N}"
echo -e "${B}   3x-ui Monitor Dashboard Installer   ${N}"
echo -e "${B}â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”${N}\n"

[ "$EUID" -ne 0 ] && err "Run as root: sudo bash install.sh"
command -v python3 &>/dev/null || err "python3 not found â€” install it first"

# â”€â”€ 1. Python packages â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo -e "${Y}[1/4] Installing Python packages...${N}"
install_pip() {
  pip3 install "$@" -q 2>/dev/null && return 0
  info "pip3 failed, trying apt..."
  apt-get update -qq && apt-get install -y python3-pip -q
  pip3 install "$@" -q
}
install_pip flask requests
pip3 install tzdata -q 2>/dev/null || true   # for ZoneInfo on older systems
ok "Python packages ready"

# â”€â”€ 2. Directory & files â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo -e "\n${Y}[2/4] Setting up ${DIR}...${N}"
mkdir -p "$DIR"

download() {
  info "Downloading $1..."
  curl -fsSL "${REPO_RAW}/$1" -o "${DIR}/$1" || err "Failed to download $1"
}
download dashboard.py
download monitor.py
download xui-mon.py
chmod +x "${DIR}/xui-mon.py"
ln -sf "${DIR}/xui-mon.py" /usr/local/bin/xui-mon
ok "Files downloaded"

# â”€â”€ 3. Generate secret key â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
sed -i "s/xui-monitor-2026-change-me/${SECRET}/" "${DIR}/dashboard.py"
ok "Secret key generated"

# â”€â”€ 4. Systemd services â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo -e "\n${Y}[3/4] Creating systemd services...${N}"

PYTHON=$(command -v python3)

cat > /etc/systemd/system/xui-dashboard.service << EOF
[Unit]
Description=3x-ui Traffic Dashboard
After=network.target

[Service]
ExecStart=${PYTHON} ${DIR}/dashboard.py
WorkingDirectory=${DIR}
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/system/xui-monitor.service << EOF
[Unit]
Description=3x-ui Traffic Monitor
After=network.target xui-dashboard.service

[Service]
ExecStart=${PYTHON} ${DIR}/monitor.py
WorkingDirectory=${DIR}
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable xui-dashboard xui-monitor -q
systemctl restart xui-dashboard xui-monitor
ok "Services started"

# â”€â”€ 5. Done â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
sleep 2
IP=$(hostname -I 2>/dev/null | awk '{print $1}')
[ -z "$IP" ] && IP="YOUR_SERVER_IP"

echo -e "\n${Y}[4/4] Verifying...${N}"
if systemctl is-active --quiet xui-dashboard; then
  ok "xui-dashboard running"
else
  echo -e "  ${R}âœ— xui-dashboard failed to start â€” check logs below${N}"
  journalctl -u xui-dashboard -n 20 --no-pager
  exit 1
fi

echo -e "\n${G}â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”${N}"
echo -e "${G}  Done! Dashboard is up and running.${N}"
echo -e "${G}â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”${N}\n"

echo -e "  ${C}URL:${N}      http://${IP}:5000"
echo -e "  ${C}First run:${N} Open the URL â†’ register your admin account"
echo -e "  ${C}Settings:${N}  Enter your 3x-ui panel URL, username & password\n"

echo -e "  ${Y}Management CLI (xui-mon):${N}"
echo -e "   â€¢ Status:      xui-mon status"
echo -e "   â€¢ Restart:     xui-mon restart"
echo -e "   â€¢ Change user: xui-mon user <new-username>"
echo -e "   â€¢ Change pass: xui-mon pass <new-password>"
echo -e "   â€¢ Change port: xui-mon port <number>"
echo -e "   â€¢ HTTPS on:    xui-mon https on --cert /path/fullchain.pem --key /path/privkey.pem"
echo -e "   â€¢ Remove:      xui-mon remove
"
echo -e "  ${Y}Service logs:${N}"
echo -e "   â€¢ Dashboard:   journalctl -u xui-dashboard -f"
echo -e "   â€¢ Monitor:     journalctl -u xui-monitor -f
"

