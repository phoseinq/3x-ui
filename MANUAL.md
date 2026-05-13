<div dir="rtl" align="right">

# نصب دستی

[← نصب](README.md)

اگه install.sh کار نکرد یا می‌خوای خودت قدم به قدم نصب کنی:

```bash
# ۱. پیش‌نیازها
apt install python3 python3-pip -y
pip3 install flask requests --break-system-packages

# ۲. پوشه
mkdir -p /opt/xui-monitor/static

# ۳. دانلود فایل‌ها
#    اگه پروکسی نیاز داری، اضافه کن: --proxy socks5://HOST:PORT
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

**[← بعدی: راه‌اندازی اولیه و تنظیمات](SETUP.md)**

</div>

---

# Manual Install

[← Installation](README.md)

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

**[Next: First run & settings →](SETUP.md)**
