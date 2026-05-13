<div dir="rtl" align="right">

# مستندات کامل — 3x-ui Monitor

[← برگشت به README](README.md)

---

## قابلیت‌ها

- **نمودار ترافیک** — گراف مصرف ساعتی به تفکیک هر کاربر و مجموع کل
- **کاربران آنلاین** — شناسایی لحظه‌ای با نمایش مدت اتصال
- **سلامت سرور** — CPU، RAM، دیسک و پهنای باند
- **راه‌اندازی مجدد خودکار Xray** — هنگام عبور کاربر از کوتا (با مقدار مجاز قابل تنظیم)
- **پاک‌سازی پنل** — مشاهده و حذف انبوه کاربران منقضی، لیمیت‌شده یا قدیمی مستقیم از پنل
- **بکاپ قبل از حذف** — فایل CSV از اطلاعات کاربران قبل از هر حذف ذخیره می‌شود
- **زمان‌بند پاک‌سازی** — حذف خودکار شبانه در ساعت دلخواه
- **HTTPS** — فعال‌سازی اختیاری با گواهینامه دلخواه
- **منطقه زمانی** — تمام زمان‌ها در timezone تنظیم‌شده نمایش داده می‌شوند
- **چند مدیر** — حساب‌های مدیریتی با رمزنگاری PBKDF2

---

## راهنمای تنظیمات

| تنظیم | توضیح |
|---|---|
| آدرس پنل | آدرس کامل پنل 3x-ui — مثلاً `http://1.2.3.4:2096` یا `https://panel.example.com` |
| نام کاربری / رمز پنل | اطلاعات ورود به پنل 3x-ui |
| فاصله بررسی | هر چند ثانیه پنل بررسی شود (پیش‌فرض: ۳۰) |
| مجاز اضافی (MB) | ترافیک اضافه مجاز بعد از کوتا قبل از ری‌استارت Xray |
| راه‌اندازی مجدد Xray | فعال/غیرفعال کردن ری‌استارت خودکار |
| منطقه زمانی | مثلاً `Asia/Tehran` |
| HTTPS | فعال‌سازی با مسیر cert و key |
| پاک‌سازی خودکار | حذف شبانه رکوردهای قدیمی از DB محلی |
| پاک‌سازی پنل | حذف کاربران منقضی/لیمیت‌شده مستقیم از پنل |

---

## سرویس‌ها

| سرویس | نقش |
|---|---|
| `xui-dashboard` | رابط تحت‌وب — روی پورت ۵۰۰۰ اجرا می‌شود |
| `xui-monitor` | پردازش پس‌زمینه — پنل را بررسی می‌کند و در صورت تجاوز از کوتا، Xray را ری‌استارت می‌کند |

هر دو سرویس با راه‌اندازی سیستم شروع می‌شوند و در صورت خطا خودکار ری‌استارت می‌شوند.

---

## بکاپ کاربران حذف‌شده

قبل از هر حذف (چه دستی چه خودکار)، یک فایل CSV در مسیر زیر ذخیره می‌شود:

```
/opt/xui-monitor/deleted_backup/YYYY-MM-DD_HH-MM-SS.csv
```

فیلدها: `email`, `client_id`, `subscription`, `tg_id`, `comment`, `quota_gb`, `up_gb`, `down_gb`, `total_gb`, `pct`, `expiry_date`

---

## کتابخانه‌ها

**نصب خودکار توسط installer:**

| بسته | کاربرد |
|---|---|
| `flask` | وب‌فریمورک — رابط کاربری و API |
| `requests` | ارتباط با API پنل 3x-ui |
| `tzdata` | پایگاه داده منطقه‌های زمانی |

**استاندارد پایتون (نیاز به نصب ندارند):**

`sqlite3`, `hashlib`, `threading`, `zoneinfo`, `logging`, `json`, `pathlib`, `datetime`, `csv`

</div>

---

# Advanced Docs — 3x-ui Monitor

[← Back to README](README.md)

---

## Features

- **Traffic charts** — Hourly usage per user and totals
- **Online users** — Live detection with connection duration
- **Server health** — CPU, RAM, disk, live bandwidth
- **Auto-restart Xray** — Triggers on quota breach (configurable grace)
- **Panel cleanup** — Preview and bulk-delete expired / over-limit / aged users
- **Deletion backup** — CSV saved before every delete (auto or manual)
- **Scheduled cleanup** — Nightly auto-delete at a time you choose
- **HTTPS** — Optional TLS with your own certificate
- **Timezone-aware** — All times in your configured timezone
- **Multi-admin** — PBKDF2-hashed admin accounts

---

## Settings reference

| Setting | Description |
|---|---|
| Panel URL | Full URL to your 3x-ui panel — e.g. `http://1.2.3.4:2096` or `https://panel.example.com` |
| Panel User / Pass | Your 3x-ui login credentials |
| Check Interval | How often the monitor polls the panel in seconds (default: 30) |
| Grace MB | Extra traffic allowed after quota before Xray restarts |
| Auto-restart Xray | Enable/disable automatic Xray restart on quota breach |
| Timezone | e.g. `Asia/Tehran` |
| HTTPS | Enable with cert and key paths |
| Auto Cleanup | Nightly deletion of old records from local DB |
| Panel Cleanup | Delete expired / over-limit users directly from the panel |

---

## Services

| Service | Role |
|---|---|
| `xui-dashboard` | Flask web UI — listens on port 5000 |
| `xui-monitor` | Background poller — checks panel every N seconds, restarts Xray on quota breach |

Both start on boot and restart automatically on failure.

---

## Deletion backup

Before any delete (manual or scheduled), a CSV is written to:

```
/opt/xui-monitor/deleted_backup/YYYY-MM-DD_HH-MM-SS.csv
```

Fields: `email`, `client_id`, `subscription`, `tg_id`, `comment`, `quota_gb`, `up_gb`, `down_gb`, `total_gb`, `pct`, `expiry_date`

---

## Libraries

**Installed automatically:**

| Package | Purpose |
|---|---|
| `flask` | Web framework — dashboard UI and API routes |
| `requests` | HTTP client — communicates with the 3x-ui panel API |
| `tzdata` | Timezone database |

**Python standard library (no install needed):**

`sqlite3`, `hashlib`, `threading`, `zoneinfo`, `logging`, `json`, `pathlib`, `datetime`, `csv`

---

MIT License
