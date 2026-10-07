# 📩 Telegram File Mail Bot

A modular Telegram bot that allows registered users to send multiple files to a predefined email address directly through Telegram.

The project includes a FastAPI-based web administration panel, SQLite database, SMTP email delivery, user management, file history, database backup and restore, configurable settings, timezone support, pagination, and bilingual English/Persian support.

**Current Release: `v1.0.3`**

---

## ✨ Features

- 📤 Send multiple files through Telegram
- 📎 Multiple attachments in a single email
- 📏 Configurable total file-size limit
- 📝 Custom email subject
- 📧 SMTP email delivery
- 👤 Telegram user registration
- 📱 Phone number registration
- 🚫 Enable/disable users from the admin panel
- 📂 File delivery history
- 🔄 Retry failed email delivery
- 🗑 Pending file management
- 📤 Support for forwarded Telegram files
- 🖥️ FastAPI web administration panel
- 🔐 Admin authentication
- ⚙️ Configure application settings from the web panel
- 🌐 English and Persian language support
- 🇬🇧 English is the default language
- 🇮🇷 Persian with RTL interface
- 🕐 Configurable timezone
- 📄 Files pagination and search
- 💾 SQLite database
- 💾 Database Backup & Restore
- 📧 HTML sender information table in outgoing emails
- 🚀 systemd service support
- 🌐 Nginx reverse-proxy support
- 🐧 Ubuntu VPS deployment
- 🧩 Modular Python architecture

> **Note:** PDF compression is not included in `v1.0.3`.

---

# 🆕 What's New in v1.0.3

### 💾 Database Backup & Restore

The administration panel now provides database backup and restore functionality.

Administrators can create a backup of the SQLite database and restore a previously created backup when required.

This is useful before upgrades, configuration changes, migrations, or maintenance.

### 📄 Files Pagination & Search

The Files section now supports pagination and search.

This makes it easier to manage installations with a large number of uploaded files and delivery records.

### 🕐 Timezone Support

A configurable timezone is available from the administration panel.

The selected timezone is used when displaying date and time information throughout the panel, including backup-related timestamps.

### 📤 Forwarded Files

Files forwarded to the Telegram bot from other chats are handled through the normal file-processing flow.

Users can forward supported files without needing to download and upload them again manually.

### 📧 HTML Email Information Table

Outgoing emails now include sender and upload information in a structured HTML table.

The table can include information such as:

- User name
- Telegram username
- Telegram ID
- Phone number
- Email subject
- Number of files
- Total file size
- File names

The fields included in the email can be configured from the administration panel.

### 🎨 Administration Panel Improvements

- Improved Backup interface
- Improved pagination card layout
- Improved Settings interface
- Improved bilingual UI
- Improved RTL/LTR handling

---

# 🏗️ Architecture

The project is organized into independent modules:

```text
telegram-file-mail-bot/
│
├── app.py
├── i18n.py
├── requirements.txt
├── install.sh
├── .env.example
├── nginx.conf.example
├── telegram-file-mail-bot.service
├── LICENSE
├── README.md
│
├── bot/
│   ├── app.py
│   ├── cleanup.py
│   ├── handlers.py
│   └── helpers.py
│
├── config/
│   └── settings.py
│
├── database/
│   ├── core.py
│   ├── files.py
│   ├── pending.py
│   ├── settings.py
│   └── users.py
│
├── mail/
│   └── smtp.py
│
├── web/
│   ├── auth.py
│   ├── dashboard.py
│   ├── files.py
│   ├── settings.py
│   └── users.py
│
├── templates/
├── static/
└── storage/
```

## Main components

| Component | Purpose |
|---|---|
| `bot/` | Telegram bot logic and handlers |
| `database/` | SQLite database operations |
| `mail/` | SMTP email delivery |
| `web/` | FastAPI administration panel |
| `templates/` | Web UI templates |
| `static/` | CSS and JavaScript |
| `config/` | Application configuration |
| `i18n.py` | English/Persian translations |

---

# 🌐 Languages

The application supports:

- 🇬🇧 English
- 🇮🇷 Persian

English is the default language.

The language can be changed from:

```text
Admin Panel → Settings → Language
```

The selected language is stored in the database.

When Persian is selected:

- The web interface uses RTL layout.
- Telegram bot messages use Persian translations.

When English is selected:

- The web interface uses LTR layout.
- Telegram bot messages use English translations.

---

# 🚀 Installation

## Requirements

Recommended environment:

- Ubuntu 22.04 or newer
- Python 3.11+
- SQLite
- Nginx for production
- A Telegram Bot
- An SMTP account

---

## 1. Clone the repository

```bash
cd /opt

git clone https://github.com/Alvanweb/telegram-file-mail-bot.git

cd telegram-file-mail-bot
```

### Install a specific release

To install `v1.0.3`:

```bash
git clone --branch v1.0.3 --depth 1 \
https://github.com/Alvanweb/telegram-file-mail-bot.git \
telegram-file-mail-bot

cd telegram-file-mail-bot
```

---

## 2. Run the installer

Make the installer executable:

```bash
chmod +x install.sh
```

Run:

```bash
sudo ./install.sh
```

The installer will:

- Check that it is running as root
- Check the application files
- Install required Ubuntu packages
- Verify Python 3.11+
- Create the `telegrambot` service user
- Create the Python virtual environment
- Install Python dependencies
- Create runtime directories
- Create `.env` from `.env.example`
- Set secure file permissions
- Install the systemd service
- Enable the systemd service

---

## Application Directory

The default application directory is:

```text
/opt/telegram-file-mail-bot
```

The installer is designed to install the application into this directory even when the repository was cloned from another location.

For example:

```bash
cd /root

git clone https://github.com/Alvanweb/telegram-file-mail-bot.git

cd telegram-file-mail-bot

chmod +x install.sh

sudo ./install.sh
```

The application will still be installed under:

```text
/opt/telegram-file-mail-bot
```

---

# ⚙️ Configuration

After installation, edit:

```bash
nano /opt/telegram-file-mail-bot/.env
```

Example:

```env
# Telegram
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=CHANGE_THIS_PASSWORD
SESSION_SECRET=CHANGE_THIS_TO_A_RANDOM_SECRET

# Database
DB_PATH=/opt/telegram-file-mail-bot/bot.db

# Web panel
PANEL_HOST=127.0.0.1
PANEL_PORT=8000
```

## Important

Never commit `.env` to GitHub.

The repository excludes sensitive runtime files such as:

```text
.env
*.db
*.sqlite
*.sqlite3
venv/
.venv/
__pycache__/
*.log
```

---

# 🤖 Telegram Bot

Create a Telegram bot using BotFather and obtain its token.

Set the token in:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

The bot uses Telegram polling and does not require a public webhook.

## User flow

The normal user flow is:

```text
/start
   │
   ▼
User Registration
   │
   ▼
Enter Email Subject
   │
   ▼
Upload / Forward Files
   │
   ▼
Check Total Size
   │
   ▼
Review Files
   │
   ▼
Send Email
   │
   ▼
Email Delivered
```

Multiple files are attached to the same email.

The maximum total file size is configurable from the administration panel.

---

# 📧 SMTP Configuration

SMTP configuration can be managed from:

```text
Admin Panel → Settings → SMTP
```

## Gmail

Recommended Gmail configuration:

```text
SMTP Host: smtp.gmail.com
SMTP Port: 587
TLS: Enabled
SMTP Username: your@gmail.com
SMTP Password: Gmail App Password
SMTP From: your@gmail.com
```

For Gmail, use a **Google App Password** instead of your normal Google account password.

The application can also be configured with other compatible SMTP providers and relay services such as Brevo.

---

# 🖥️ Administration Panel

The application provides a FastAPI administration panel.

## Default production configuration

```env
PANEL_HOST=127.0.0.1
PANEL_PORT=8000
```

This means the FastAPI panel is accessible only from the local server.

Default local address:

```text
http://127.0.0.1:8000
```

For production, use Nginx as a reverse proxy and expose the panel through HTTPS.

---

# 🔓 Temporary Direct Access Testing

For temporary testing without Nginx:

```env
PANEL_HOST=0.0.0.0
PANEL_PORT=8880
```

Then restart:

```bash
systemctl restart telegram-file-mail-bot
```

The panel can then be accessed through:

```text
http://SERVER_IP:8880
```

## Security Warning

Do not use `0.0.0.0` as the normal production configuration unless you intentionally want the FastAPI application directly exposed.

For production use:

```env
PANEL_HOST=127.0.0.1
PANEL_PORT=8000
```

with Nginx in front of the application.

---

# 📊 Dashboard

The dashboard provides:

- Total users
- Active users
- File statistics
- Delivery statistics
- Application status

---

# 👤 Users

The Users section provides:

- Registered users
- Telegram username
- Telegram ID
- Phone number
- Registration information
- Enable/disable users
- Delete users

---

# 📂 Files

The Files section provides:

- Uploaded file history
- File names
- File sizes
- Email subjects
- Delivery status
- Error information
- Pending file management
- Search
- Pagination

Pagination helps manage large file histories without displaying every record on a single page.

---

# 💾 Database Backup & Restore

The administration panel provides database backup and restore functionality.

The SQLite database contains important application information including:

- Telegram users
- User registration information
- File history
- Pending uploads
- Application settings
- Language preferences

Before major upgrades or migrations, it is recommended to create a database backup.

> Always keep an independent backup of important production data.

The production database should never be committed to GitHub.

---

# 🕐 Timezone

The administration panel supports configurable timezone settings.

The selected timezone is used for date and time information displayed by the application.

This is particularly useful when the server is hosted in a different country or timezone from the administrator.

Timezone settings can be managed from:

```text
Admin Panel → Settings
```

---

# ⚙️ Settings

The Settings section provides:

- 🌐 Language selection
- 📧 SMTP configuration
- 📬 Email recipients
- 📦 Total file-size limit
- 🧹 Pending file retention
- 🧾 Email content fields
- 🕐 Timezone
- ✉️ SMTP connection testing

---

# 📧 Email Content

Outgoing emails contain information about the uploaded files and sender.

The sender information is displayed in an HTML table for easier reading.

Depending on the selected email fields, the message can contain:

| Field | Description |
|---|---|
| User Name | Telegram user's first name |
| Username | Telegram username |
| Telegram ID | Telegram account ID |
| Phone | Registered phone number |
| Subject | Email subject |
| File Count | Number of attached files |
| Total Size | Combined file size |
| Filenames | Names of uploaded files |

The fields included in the email can be selected from:

```text
Admin Panel → Settings → Email Content
```

---

# 📤 Forwarded Files

The bot supports files forwarded from other Telegram chats.

Users can forward supported files directly to the bot and continue through the normal file-upload process.

This avoids the need to download a file and upload it again manually.

---

# 🌐 Nginx / Production

For production deployments, the recommended architecture is:

```text
                    Internet
                       │
                       ▼
                 ┌───────────┐
                 │   Nginx   │
                 │   :443    │
                 └─────┬─────┘
                       │
                       ▼
                 127.0.0.1:8000
                       │
                       ▼
                 ┌───────────┐
                 │ FastAPI   │
                 │ Web Panel │
                 └───────────┘
```

The Telegram bot runs independently:

```text
Telegram
   │
   ▼
Telegram Bot
   │
   ▼
Application
   │
   ▼
SMTP
   │
   ▼
Email Recipient
```

An example Nginx configuration is included:

```text
nginx.conf.example
```

For production, configure HTTPS using a valid TLS certificate.

---

# 🔐 Security

Never publish or commit:

```text
.env
bot.db
*.backup
SMTP passwords
Telegram bot tokens
Session secrets
Admin passwords
```

The repository includes a `.gitignore` configured to exclude sensitive runtime files.

If a Telegram bot token or SMTP credential is accidentally exposed, revoke or rotate it immediately.

Use strong values for:

```env
ADMIN_PASSWORD=
SESSION_SECRET=
```

Do not reuse sensitive credentials from other services.

---

# ⚙️ systemd

A systemd service file is included:

```text
telegram-file-mail-bot.service
```

The installer automatically installs and enables the service.

## Start

```bash
sudo systemctl start telegram-file-mail-bot
```

## Enable at boot

```bash
sudo systemctl enable telegram-file-mail-bot
```

## Check status

```bash
sudo systemctl status telegram-file-mail-bot
```

## View logs

```bash
sudo journalctl -u telegram-file-mail-bot -f
```

## Restart

```bash
sudo systemctl restart telegram-file-mail-bot
```

The service is configured to restart automatically if the application stops unexpectedly.

---

# 💾 Database

The project uses SQLite.

The database stores:

- Telegram users
- User registration information
- File history
- Pending uploads
- Application settings
- Language preferences

The production database should never be committed to GitHub.

A new installation creates its own database.

---

# 📦 File Upload Flow

The standard workflow is:

```text
Start
  │
  ▼
User Registration
  │
  ▼
Enter Email Subject
  │
  ▼
Upload / Forward Files
  │
  ▼
Check Total Size
  │
  ▼
Review Files
  │
  ▼
Send Email
  │
  ▼
Email Delivered
```

Multiple files are attached to the same email.

The maximum total file size is configurable from the administration panel.

---

# 🔄 Failed Delivery

If email delivery fails, uploaded files remain available according to the application's retention and cleanup settings.

Users can retry sending the email when supported by the application flow.

Delivery status and errors are available in the Files section of the administration panel.

---

# 🧹 Pending Files

Pending uploads are stored in:

```text
storage/pending_uploads/
```

The application includes cleanup and retention handling for pending files.

The retention period can be configured from:

```text
Admin Panel → Settings → File Management
```

---

# 🛠️ Development

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

# 🐛 Troubleshooting

## Check service status

```bash
systemctl status telegram-file-mail-bot --no-pager
```

## View application logs

```bash
journalctl -u telegram-file-mail-bot -n 100 --no-pager
```

## Restart the service

```bash
systemctl restart telegram-file-mail-bot
```

## Check Python version

```bash
python3 --version
```

Python 3.11 or newer is required.

## Check dependencies

```bash
/opt/telegram-file-mail-bot/venv/bin/python -m pip install \
    -r /opt/telegram-file-mail-bot/requirements.txt
```

## Check whether port 8000 is listening

```bash
ss -lntp | grep 8000
```

Expected production binding:

```text
127.0.0.1:8000
```

For temporary direct testing:

```text
0.0.0.0:8880
```

## Check systemd service configuration

```bash
systemctl cat telegram-file-mail-bot
```

## Check environment file permissions

```bash
ls -l /opt/telegram-file-mail-bot/.env
```

Expected:

```text
-rw------- ... .env
```

---

# 📁 Project Data

Runtime data should remain outside the public source history.

Typical production files include:

```text
.env
bot.db
storage/pending_uploads/
venv/
```

These files are intentionally excluded from Git.

---

# 📜 License

This project is licensed under the MIT License.

See [`LICENSE`](LICENSE) for details.

---

# 👨‍💻 Author

Developed by **MOЯ**

GitHub:

https://github.com/Alvanweb

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

Contributions, bug reports, and feature requests are welcome.

---

## 📌 Release

Current stable release:

**v1.0.3**

Release history:

- `v1.0.1` — Initial public release
- `v1.0.2` — Installation, configuration, and bilingual UI improvements
- `v1.0.3` — Backup & Restore, Timezone, Pagination, Forwarded Files, HTML email information table, UI improvements, and removal of PDF compression
