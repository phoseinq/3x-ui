<div align="center">

# ðŸ“Š 3x-ui Monitor

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/3x--ui-Compatible-orange?style=for-the-badge" alt="3x-ui">
<img src="https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge" alt="License">

**Traffic monitor & web dashboard for 3x-ui VPN panels**  
**Ù…Ø§Ù†ÛŒØªÙˆØ± ØªØ±Ø§ÙÛŒÚ© Ùˆ Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯ ÙˆØ¨ Ø¨Ø±Ø§ÛŒ Ù¾Ù†Ù„â€ŒÙ‡Ø§ÛŒ 3x-ui**

[English](#english) | [ÙØ§Ø±Ø³ÛŒ](#ÙØ§Ø±Ø³ÛŒ)

---

</div>

## English

### ðŸ“– Description

**3x-ui Monitor** is a self-hosted web dashboard that connects to your [3x-ui](https://github.com/MHSanaei/3x-ui) panel and gives you a real-time view of user traffic, online activity, server health, and automatic quota enforcement â€” all from a clean dark UI.

**Key Features:**
- ðŸ“ˆ **Traffic charts** â€” Hourly usage graphs per user and total
- ðŸŸ¢ **Online users** â€” Live detection + duration tracking, sorted by longest online
- ðŸ–¥ï¸ **Server health** â€” CPU, RAM, disk, and live bandwidth gauges
- ðŸ”„ **Auto-restart Xray** â€” Kicks in when users exceed their quota (with grace allowance)
- ðŸ§¹ **Panel cleanup** â€” Preview and delete expired / over-limit users directly from the panel
- â° **Auto-cleanup scheduler** â€” Nightly auto-delete of aged accounts
- ðŸ”’ **HTTPS support** â€” Optional TLS with your own certificate
- ðŸŒ **Timezone-aware** â€” All times shown in your configured timezone
- ðŸ‘¤ **Multi-admin** â€” PBKDF2-hashed admin accounts

---

### ðŸš€ Installation

Run this single command on your Ubuntu/Debian server:

```bash
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui/main/install.sh | sudo bash
```

The script will:
1. Install `flask` and `requests` (via pip, falls back to apt if needed)
2. Download files to `/opt/xui-monitor/`
3. Generate a random secret key
4. Create and start two systemd services: `xui-dashboard` and `xui-monitor`
5. Print your dashboard URL

**After install:**
1. Open `http://YOUR_SERVER_IP:5000` in your browser
2. Register your admin account (first visit only)
3. Go to **Settings** â†’ enter your 3x-ui panel URL, username, and password

---

### âš™ï¸ Settings

| Setting | Description |
|---|---|
| **Panel URL** | Full URL to your 3x-ui panel (e.g. `http://1.2.3.4:2096/path`) |
| **Panel User / Pass** | Your 3x-ui login credentials |
| **Check Interval** | How often the monitor polls the panel (seconds) |
| **Grace MB** | Extra traffic allowed after quota before Xray restarts |
| **Auto-restart Xray** | Restart Xray core when a user exceeds their quota |
| **Timezone** | Timezone for all displayed times (e.g. `Asia/Tehran`) |
| **TLS / HTTPS** | Enable HTTPS with a custom cert/key path |
| **Auto Cleanup** | Nightly deletion of expired users from local DB |
| **Panel Cleanup** | Preview + delete expired / over-limit users from the panel |

---

### ðŸ–¥ï¸ Services

| Service | Description |
|---|---|
| `xui-dashboard` | Flask web UI â€” runs on port 5000 |
| `xui-monitor` | Background poller â€” checks panel every N seconds, restarts Xray on quota breach |

Both services start on boot and restart automatically on failure.

---

### ðŸ”§ CLI Commands

```bash
# View live dashboard logs
journalctl -u xui-dashboard -f

# View live monitor logs
journalctl -u xui-monitor -f

# Restart both services
systemctl restart xui-dashboard xui-monitor

# Stop both services
systemctl stop xui-dashboard xui-monitor

# Uninstall completely
systemctl disable --now xui-dashboard xui-monitor && rm -rf /opt/xui-monitor
```

---

### ðŸ“„ License

This project is licensed under the MIT License â€” see the [LICENSE](LICENSE) file for details.

---

### ðŸ¤ Contributing

Contributions are welcome! Feel free to:
- ðŸ› Report bugs
- ðŸ’¡ Suggest features
- ðŸ”§ Submit pull requests

---

### â­ Support

If this project helped you, please consider:
- â­ Starring the repository
- ðŸ› Reporting issues
- ðŸ“¢ Sharing with others

---

<div dir="rtl" align="right">

## ÙØ§Ø±Ø³ÛŒ

### ðŸ“– Ù…Ø¹Ø±ÙÛŒ

**3x-ui Monitor** ÛŒÙ‡ Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯ ÙˆØ¨ self-hosted Ù‡Ø³Øª Ú©Ù‡ Ø¨Ù‡ Ù¾Ù†Ù„ [3x-ui](https://github.com/MHSanaei/3x-ui) Ø´Ù…Ø§ ÙˆØµÙ„ Ù…ÛŒâ€ŒØ´Ù‡ Ùˆ ÛŒÙ‡ Ø¯ÛŒØ¯ Ù„Ø­Ø¸Ù‡â€ŒØ§ÛŒ Ø§Ø² ØªØ±Ø§ÙÛŒÚ© Ú©Ø§Ø±Ø¨Ø±Ø§ØŒ ÙØ¹Ø§Ù„ÛŒØª Ø¢Ù†Ù„Ø§ÛŒÙ†ØŒ Ø³Ù„Ø§Ù…Øª Ø³Ø±ÙˆØ±ØŒ Ùˆ Ú©Ù†ØªØ±Ù„ Ø®ÙˆØ¯Ú©Ø§Ø± Ú©ÙˆØªØ§ Ø±Ùˆ Ø¨Ø§ ÛŒÙ‡ UI ØªØ§Ø±ÛŒÚ© Ùˆ ØªÙ…ÛŒØ² Ø¨Ù‡ØªÙˆÙ† Ù…ÛŒâ€ŒØ¯Ù‡.

**Ø§Ù…Ú©Ø§Ù†Ø§Øª Ú©Ù„ÛŒØ¯ÛŒ:**
- ðŸ“ˆ **Ù†Ù…ÙˆØ¯Ø§Ø± ØªØ±Ø§ÙÛŒÚ©** â€” Ú¯Ø±Ø§Ù Ø³Ø§Ø¹ØªÛŒ Ù…ØµØ±Ù Ù‡Ø± Ú©Ø§Ø±Ø¨Ø± Ùˆ Ú©Ù„
- ðŸŸ¢ **Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø¢Ù†Ù„Ø§ÛŒÙ†** â€” ØªØ´Ø®ÛŒØµ Ù„Ø­Ø¸Ù‡â€ŒØ§ÛŒ + Ø±Ø¯ÛŒØ§Ø¨ÛŒ Ù…Ø¯Øª Ø²Ù…Ø§Ù†ØŒ Ù…Ø±ØªØ¨â€ŒØ´Ø¯Ù‡ Ø¨Ø± Ø§Ø³Ø§Ø³ Ø·ÙˆÙ„Ø§Ù†ÛŒâ€ŒØªØ±ÛŒÙ† Ø¢Ù†Ù„Ø§ÛŒÙ†
- ðŸ–¥ï¸ **Ø³Ù„Ø§Ù…Øª Ø³Ø±ÙˆØ±** â€” Ú¯ÛŒØ¬â€ŒÙ‡Ø§ÛŒ CPUØŒ RAMØŒ Ø¯ÛŒØ³Ú© Ùˆ Ù¾Ù‡Ù†Ø§ÛŒ Ø¨Ø§Ù†Ø¯ Ø²Ù†Ø¯Ù‡
- ðŸ”„ **Ø±ÛŒâ€ŒØ§Ø³ØªØ§Ø±Øª Ø®ÙˆØ¯Ú©Ø§Ø± Xray** â€” ÙˆÙ‚ØªÛŒ Ú©Ø§Ø±Ø¨Ø± Ø§Ø² Ú©ÙˆØªØ§Ø´ Ø±Ø¯ Ø´Ø¯ ÙØ¹Ø§Ù„ Ù…ÛŒâ€ŒØ´Ù‡ (Ø¨Ø§ Ù…Ø§Ø±Ø¬ÛŒÙ† Ù‚Ø§Ø¨Ù„ ØªÙ†Ø¸ÛŒÙ…)
- ðŸ§¹ **Ù¾Ø§Ú©Ø³Ø§Ø²ÛŒ Ù¾Ù†Ù„** â€” Ù¾ÛŒØ´â€ŒÙ†Ù…Ø§ÛŒØ´ Ùˆ Ø­Ø°Ù Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø§Ú©Ø³Ù¾Ø§ÛŒØ± ÛŒØ§ Ù„ÛŒÙ…ÛŒØªâ€ŒØ´Ø¯Ù‡ Ù…Ø³ØªÙ‚ÛŒÙ… Ø§Ø² Ù¾Ù†Ù„
- â° **Ø²Ù…Ø§Ù†â€ŒØ¨Ù†Ø¯ Ù¾Ø§Ú©Ø³Ø§Ø²ÛŒ** â€” Ø­Ø°Ù Ø®ÙˆØ¯Ú©Ø§Ø± Ø´Ø¨Ø§Ù†Ù‡ Ø­Ø³Ø§Ø¨â€ŒÙ‡Ø§ÛŒ Ù‚Ø¯ÛŒÙ…ÛŒ
- ðŸ”’ **Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ HTTPS** â€” TLS Ø§Ø®ØªÛŒØ§Ø±ÛŒ Ø¨Ø§ Ú¯ÙˆØ§Ù‡ÛŒÙ†Ø§Ù…Ù‡ Ø®ÙˆØ¯ØªÙˆÙ†
- ðŸŒ **Ø¢Ú¯Ø§Ù‡ Ø§Ø² ØªØ§ÛŒÙ…â€ŒØ²ÙˆÙ†** â€” Ù‡Ù…Ù‡ Ø²Ù…Ø§Ù†â€ŒÙ‡Ø§ Ø¯Ø± ØªØ§ÛŒÙ…â€ŒØ²ÙˆÙ† ØªÙ†Ø¸ÛŒÙ…â€ŒØ´Ø¯Ù‡ Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø¯Ù‡ Ù…ÛŒâ€ŒØ´Ù†
- ðŸ‘¤ **Ú†Ù†Ø¯ Ø§Ø¯Ù…ÛŒÙ†** â€” Ø­Ø³Ø§Ø¨â€ŒÙ‡Ø§ÛŒ Ø§Ø¯Ù…ÛŒÙ† Ø¨Ø§ Ù‡Ø´ PBKDF2

---

### ðŸš€ Ù†ØµØ¨

Ø§ÛŒÙ† ÛŒÙ‡ Ø¯Ø³ØªÙˆØ± Ø±Ùˆ Ø±ÙˆÛŒ Ø³Ø±ÙˆØ± Ubuntu/Debian Ø§Ø¬Ø±Ø§ Ú©Ù†:

```bash
curl -fsSL https://raw.githubusercontent.com/phoseinq/3x-ui/main/install.sh | sudo bash
```

Ø§Ø³Ú©Ø±ÛŒÙ¾Øª Ø§ÛŒÙ† Ú©Ø§Ø±Ø§ Ø±Ùˆ Ù…ÛŒâ€ŒÚ©Ù†Ù‡:
1. Ù†ØµØ¨ `flask` Ùˆ `requests` (Ø§Ø² pipØŒ Ø¯Ø± ØµÙˆØ±Øª Ù†ÛŒØ§Ø² Ø§Ø² apt)
2. Ø¯Ø§Ù†Ù„ÙˆØ¯ ÙØ§ÛŒÙ„â€ŒÙ‡Ø§ Ø¨Ù‡ `/opt/xui-monitor/`
3. ØªÙˆÙ„ÛŒØ¯ ÛŒÙ‡ secret key Ø±Ù†Ø¯ÙˆÙ…
4. Ø³Ø§Ø®Øª Ùˆ Ø±Ø§Ù‡â€ŒØ§Ù†Ø¯Ø§Ø²ÛŒ Ø¯Ùˆ Ø³Ø±ÙˆÛŒØ³ systemd: `xui-dashboard` Ùˆ `xui-monitor`
5. Ù†Ù…Ø§ÛŒØ´ Ù„ÛŒÙ†Ú© Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯

**Ø¨Ø¹Ø¯ Ø§Ø² Ù†ØµØ¨:**
1. Ù…Ø±ÙˆØ±Ú¯Ø± Ø±Ùˆ Ø¨Ø§Ø² Ú©Ù†ØŒ Ø¨Ø±Ùˆ Ø¨Ù‡ `http://IP_Ø³Ø±ÙˆØ±:5000`
2. Ø­Ø³Ø§Ø¨ Ø§Ø¯Ù…ÛŒÙ† Ø¨Ø³Ø§Ø² (ÙÙ‚Ø· Ø§ÙˆÙ„ÛŒÙ† Ø¨Ø§Ø±)
3. Ø¨Ø±Ùˆ Ø¨Ù‡ **Settings** â† Ø¢Ø¯Ø±Ø³ Ù¾Ù†Ù„ 3x-uiØŒ Ù†Ø§Ù… Ú©Ø§Ø±Ø¨Ø±ÛŒ Ùˆ Ø±Ù…Ø² Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†

---

### âš™ï¸ ØªÙ†Ø¸ÛŒÙ…Ø§Øª

| ØªÙ†Ø¸ÛŒÙ… | ØªÙˆØ¶ÛŒØ­ |
|---|---|
| **Panel URL** | Ø¢Ø¯Ø±Ø³ Ú©Ø§Ù…Ù„ Ù¾Ù†Ù„ 3x-ui (Ù…Ø«Ù„Ø§Ù‹ `http://1.2.3.4:2096/path`) |
| **Panel User / Pass** | Ø§Ø·Ù„Ø§Ø¹Ø§Øª ÙˆØ±ÙˆØ¯ Ø¨Ù‡ Ù¾Ù†Ù„ 3x-ui |
| **Check Interval** | Ù‡Ø± Ú†Ù†Ø¯ Ø«Ø§Ù†ÛŒÙ‡ ÛŒÙ‡â€ŒØ¨Ø§Ø± Ù¾Ù†Ù„ Ú†Ú© Ø¨Ø´Ù‡ |
| **Grace MB** | ØªØ±Ø§ÙÛŒÚ© Ø§Ø¶Ø§ÙÙ‡â€ŒØ§ÛŒ Ú©Ù‡ Ø¨Ø¹Ø¯ Ø§Ø² Ú©ÙˆØªØ§ Ù…Ø¬Ø§Ø²Ù‡ Ù‚Ø¨Ù„ Ø§Ø² Ø±ÛŒâ€ŒØ§Ø³ØªØ§Ø±Øª |
| **Auto-restart Xray** | Ø±ÛŒâ€ŒØ§Ø³ØªØ§Ø±Øª Xray ÙˆÙ‚ØªÛŒ Ú©Ø§Ø±Ø¨Ø± Ø§Ø² Ú©ÙˆØªØ§ Ø±Ø¯ Ø´Ø¯ |
| **Timezone** | ØªØ§ÛŒÙ…â€ŒØ²ÙˆÙ† Ø¨Ø±Ø§ÛŒ Ù†Ù…Ø§ÛŒØ´ Ø²Ù…Ø§Ù†â€ŒÙ‡Ø§ (Ù…Ø«Ù„Ø§Ù‹ `Asia/Tehran`) |
| **TLS / HTTPS** | ÙØ¹Ø§Ù„â€ŒØ³Ø§Ø²ÛŒ HTTPS Ø¨Ø§ Ù…Ø³ÛŒØ± cert/key Ø¯Ù„Ø®ÙˆØ§Ù‡ |
| **Auto Cleanup** | Ø­Ø°Ù Ø´Ø¨Ø§Ù†Ù‡ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø§Ú©Ø³Ù¾Ø§ÛŒØ± Ø§Ø² Ø¯ÛŒØªØ§Ø¨ÛŒØ³ Ù…Ø­Ù„ÛŒ |
| **Panel Cleanup** | Ù¾ÛŒØ´â€ŒÙ†Ù…Ø§ÛŒØ´ + Ø­Ø°Ù Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø§Ú©Ø³Ù¾Ø§ÛŒØ± / Ù„ÛŒÙ…ÛŒØªâ€ŒØ´Ø¯Ù‡ Ø§Ø² Ù¾Ù†Ù„ |

---

### ðŸ–¥ï¸ Ø³Ø±ÙˆÛŒØ³â€ŒÙ‡Ø§

| Ø³Ø±ÙˆÛŒØ³ | ØªÙˆØ¶ÛŒØ­ |
|---|---|
| `xui-dashboard` | Ø±Ø§Ø¨Ø· ÙˆØ¨ Flask â€” Ø±ÙˆÛŒ Ù¾ÙˆØ±Øª 5000 Ø§Ø¬Ø±Ø§ Ù…ÛŒâ€ŒØ´Ù‡ |
| `xui-monitor` | Ù¾ÙˆÙ„Ø± Ù¾Ø³â€ŒØ²Ù…ÛŒÙ†Ù‡ â€” Ù‡Ø± N Ø«Ø§Ù†ÛŒÙ‡ Ù¾Ù†Ù„ Ø±Ùˆ Ú†Ú© Ù…ÛŒâ€ŒÚ©Ù†Ù‡ØŒ Ø¯Ø± ØµÙˆØ±Øª Ù†Ù‚Ø¶ Ú©ÙˆØªØ§ Xray Ø±Ùˆ Ø±ÛŒâ€ŒØ§Ø³ØªØ§Ø±Øª Ù…ÛŒâ€ŒÚ©Ù†Ù‡ |

Ù‡Ø± Ø¯Ùˆ Ø³Ø±ÙˆÛŒØ³ Ø¨Ø§ Ø¨ÙˆØª Ø³ÛŒØ³ØªÙ… Ø´Ø±ÙˆØ¹ Ù…ÛŒâ€ŒØ´Ù† Ùˆ Ø¯Ø± ØµÙˆØ±Øª Ø®Ø·Ø§ Ø®ÙˆØ¯Ú©Ø§Ø± Ø±ÛŒâ€ŒØ§Ø³ØªØ§Ø±Øª Ù…ÛŒâ€ŒÚ©Ù†Ù†.

---

### ðŸ”§ Ø¯Ø³ØªÙˆØ±Ø§Øª CLI

```bash
# Ù„Ø§Ú¯ Ø²Ù†Ø¯Ù‡ Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯
journalctl -u xui-dashboard -f

# Ù„Ø§Ú¯ Ø²Ù†Ø¯Ù‡ Ù…Ø§Ù†ÛŒØªÙˆØ±
journalctl -u xui-monitor -f

# Ø±ÛŒâ€ŒØ§Ø³ØªØ§Ø±Øª Ù‡Ø± Ø¯Ùˆ Ø³Ø±ÙˆÛŒØ³
systemctl restart xui-dashboard xui-monitor

# ØªÙˆÙ‚Ù Ù‡Ø± Ø¯Ùˆ Ø³Ø±ÙˆÛŒØ³
systemctl stop xui-dashboard xui-monitor

# Ø­Ø°Ù Ú©Ø§Ù…Ù„
systemctl disable --now xui-dashboard xui-monitor && rm -rf /opt/xui-monitor
```

---

### ðŸ“„ Ù…Ø¬ÙˆØ²

Ø§ÛŒÙ† Ù¾Ø±ÙˆÚ˜Ù‡ ØªØ­Øª Ù…Ø¬ÙˆØ² MIT Ù…Ù†ØªØ´Ø± Ø´Ø¯Ù‡ â€” ÙØ§ÛŒÙ„ [LICENSE](LICENSE) Ø±Ùˆ Ø¨Ø¨ÛŒÙ†.

---

### ðŸ¤ Ù…Ø´Ø§Ø±Ú©Øª

Ù…Ø´Ø§Ø±Ú©Øªâ€ŒÙ‡Ø§ Ø®ÙˆØ´â€ŒØ¢Ù…Ø¯Ù†! Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒ:
- ðŸ› Ø¨Ø§Ú¯ Ú¯Ø²Ø§Ø±Ø´ Ú©Ù†ÛŒ
- ðŸ’¡ Ø§ÛŒØ¯Ù‡ Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯ Ø¨Ø¯ÛŒ
- ðŸ”§ Ù¾ÙˆÙ„ Ø±ÛŒÚ©ÙˆØ¦Ø³Øª Ø¨ÙØ±Ø³ØªÛŒ

---

### â­ Ø­Ù…Ø§ÛŒØª

Ø§Ú¯Ù‡ Ø§ÛŒÙ† Ù¾Ø±ÙˆÚ˜Ù‡ Ø¨Ù‡Øª Ú©Ù…Ú© Ú©Ø±Ø¯ØŒ Ù„Ø·ÙØ§Ù‹:
- â­ Ø¨Ù‡ Ø±ÛŒÙ¾Ø§Ø²ÛŒØªÙˆØ±ÛŒ Ø³ØªØ§Ø±Ù‡ Ø¨Ø¯Ù‡
- ðŸ› Ù…Ø´Ú©Ù„Ø§Øª Ø±Ùˆ Ú¯Ø²Ø§Ø±Ø´ Ú©Ù†
- ðŸ“¢ Ø¨Ø§ Ø¯ÛŒÚ¯Ø±Ø§Ù† Ø¨Ù‡ Ø§Ø´ØªØ±Ø§Ú© Ø¨Ø°Ø§Ø±

---

</div>

<div align="center">

**Made with â¤ï¸ for 3x-ui users**

[Report a Bug](https://github.com/phoseinq/3x-ui/issues) Â· [Ú¯Ø²Ø§Ø±Ø´ Ø¨Ø§Ú¯](https://github.com/phoseinq/3x-ui/issues)

</div>

