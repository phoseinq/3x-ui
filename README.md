<div align="center">

# 3x-ui Monitor

**داشبورد مانیتورینگ ترافیک برای پنل‌های 3x-ui**

[مستندات کامل](ADVANCED.md) · [Advanced Docs](ADVANCED.md)

---

<img width="2559" height="1363" alt="image" src="https://github.com/user-attachments/assets/d5eb19c3-1fe0-4d0a-98f8-18e47b9bf77b" />

</div>

---

<div dir="rtl" align="right">

## نصب

### نصب معمولی

```bash
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/install.sh | sudo bash
```

---

### نصب با پروکسی (سرور ایران)

سرور ایران بدون پروکسی به GitHub دسترسی ندارد — هم دانلود اسکریپت و هم تمام مراحل نصب باید از طریق پروکسی برود:

```bash
curl -fsSL --proxy socks5://HOST:PORT \
  https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/install.sh \
  | sudo bash -s -- --proxy socks5://HOST:PORT
```

اگه پروکسی یوزر و پسورد داره:

```bash
curl -fsSL --proxy socks5://user:pass@HOST:PORT \
  https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/install.sh \
  | sudo bash -s -- --proxy socks5://user:pass@HOST:PORT
```

> پروکسی باید هم جلوی `curl` و هم جلوی `bash` بیاد — اسکریپت نصب با همون پروکسی فایل‌ها رو دانلود می‌کنه.

---

### نصب دستی (بدون اسکریپت)

اگه install.sh کار نکرد یا می‌خوای قدم به قدم نصب کنی:

```bash
# ۱. نصب پیش‌نیازها
apt install python3 python3-pip -y
pip3 install flask requests --break-system-packages

# ۲. ساخت پوشه
mkdir -p /opt/xui-monitor/static

# ۳. دانلود فایل‌ها
#    اگه پروکسی نیاز داری، قبل از هر curl این رو اضافه کن: --proxy socks5://HOST:PORT
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/dashboard.py -o /opt/xui-monitor/dashboard.py
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/monitor.py   -o /opt/xui-monitor/monitor.py
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/boy.py        -o /opt/xui-monitor/boy.py
curl -fsSL https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js           -o /opt/xui-monitor/static/chart.min.js

# ۴. کلید امنیتی
SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
sed -i "s/xui-monitor-2026-change-me/$SECRET/" /opt/xui-monitor/dashboard.py

# ۵. boy CLI
chmod +x /opt/xui-monitor/boy.py
ln -sf /opt/xui-monitor/boy.py /usr/local/bin/boy

# ۶. سرویس‌های systemd
cat > /etc/systemd/system/xui-dashboard.service << 'EOF'
[Unit]
Description=3x-ui Traffic Dashboard
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/xui-monitor/dashboard.py
WorkingDirectory=/opt/xui-monitor
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/system/xui-monitor.service << 'EOF'
[Unit]
Description=3x-ui Traffic Monitor
After=network.target xui-dashboard.service

[Service]
ExecStart=/usr/bin/python3 /opt/xui-monitor/monitor.py
WorkingDirectory=/opt/xui-monitor
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
EOF

# ۷. راه‌اندازی
systemctl daemon-reload
systemctl enable xui-dashboard xui-monitor
systemctl start xui-dashboard xui-monitor
```

---

## راه‌اندازی اولیه

۱. مرورگر را باز کنید: `http://IP_سرور:5000`
۲. حساب مدیر بسازید (فقط بار اول)
۳. به **Settings** بروید و آدرس پنل 3x-ui، نام کاربری و رمز را وارد کنید

---

## دستورات boy

```bash
boy              # منوی تعاملی
boy status       # وضعیت سرویس‌ها
boy restart      # ری‌استارت
boy update       # آپدیت به آخرین نسخه
boy user <نام>   # تغییر یوزرنیم مدیر
boy pass         # تغییر پسورد (بدون نمایش روی صفحه)
boy port <عدد>   # تغییر پورت داشبورد
boy https on --cert /path/cert.pem --key /path/key.pem
boy https off    # غیرفعال کردن HTTPS
boy remove       # حذف سرویس‌ها (داده‌ها حفظ می‌شوند)
```

> همه دستورات باید به عنوان root اجرا شوند: `sudo boy ...`

---

## لاگ‌ها

```bash
journalctl -u xui-dashboard -f
journalctl -u xui-monitor -f
```

</div>

---

## Installation

### Standard

```bash
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/install.sh | sudo bash
```

### With SOCKS5 proxy

On restricted servers (e.g. Iran), even the initial `curl` needs a proxy — both the script download and all install steps must go through it:

```bash
curl -fsSL --proxy socks5://HOST:PORT \
  https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/install.sh \
  | sudo bash -s -- --proxy socks5://HOST:PORT
```

With username and password:

```bash
curl -fsSL --proxy socks5://user:pass@HOST:PORT \
  https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/install.sh \
  | sudo bash -s -- --proxy socks5://user:pass@HOST:PORT
```

### Manual install

```bash
# 1. Dependencies
apt install python3 python3-pip -y
pip3 install flask requests --break-system-packages

# 2. Directory
mkdir -p /opt/xui-monitor/static

# 3. Download files
#    Add --proxy socks5://HOST:PORT to each curl if needed
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/dashboard.py -o /opt/xui-monitor/dashboard.py
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/monitor.py   -o /opt/xui-monitor/monitor.py
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui-monitor/main/boy.py        -o /opt/xui-monitor/boy.py
curl -fsSL https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js           -o /opt/xui-monitor/static/chart.min.js

# 4. Secret key
SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
sed -i "s/xui-monitor-2026-change-me/$SECRET/" /opt/xui-monitor/dashboard.py

# 5. boy CLI
chmod +x /opt/xui-monitor/boy.py
ln -sf /opt/xui-monitor/boy.py /usr/local/bin/boy

# 6. Systemd services
cat > /etc/systemd/system/xui-dashboard.service << 'EOF'
[Unit]
Description=3x-ui Traffic Dashboard
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/xui-monitor/dashboard.py
WorkingDirectory=/opt/xui-monitor
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/system/xui-monitor.service << 'EOF'
[Unit]
Description=3x-ui Traffic Monitor
After=network.target xui-dashboard.service

[Service]
ExecStart=/usr/bin/python3 /opt/xui-monitor/monitor.py
WorkingDirectory=/opt/xui-monitor
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
EOF

# 7. Start
systemctl daemon-reload
systemctl enable xui-dashboard xui-monitor
systemctl start xui-dashboard xui-monitor
```

---

## First run

1. Open `http://SERVER_IP:5000` in your browser
2. Register your admin account (first visit only)
3. Go to **Settings** → enter your 3x-ui panel URL, username, and password

## boy CLI

```bash
boy              # interactive menu
boy status       # service status
boy restart      # restart services
boy update       # update to latest version
boy user <name>  # change admin username
boy pass         # change admin password
boy port <num>   # change dashboard port
boy https on --cert /path/cert.pem --key /path/key.pem
boy https off    # disable HTTPS
boy remove       # remove services (data is kept)
```

> Always run as root: `sudo boy ...`

## Logs

```bash
journalctl -u xui-dashboard -f
journalctl -u xui-monitor -f
```

---

[Advanced docs (features, settings, libraries) →](ADVANCED.md)

MIT License
