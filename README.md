# 📩 Telegram File Mail Bot

A modular Telegram bot that allows registered users to send multiple files to a predefined email address directly through Telegram.

The project includes a FastAPI-based web administration panel, SQLite database, SMTP email delivery, user management, file history, configurable settings, and bilingual English/Persian support.

## ✨ Features

* 📤 Send multiple files through Telegram
* 📎 Multiple attachments in a single email
* 📏 Configurable total file-size limit
* 📝 Custom email subject
* 📧 SMTP email delivery
* 👤 Telegram user registration
* 📱 Phone number registration
* 🚫 Enable/disable users from the admin panel
* 📂 File delivery history
* 🔄 Retry failed email delivery
* 🗑 Pending file management
* 🖥️ FastAPI web administration panel
* 🔐 Admin authentication
* ⚙️ Configure application settings from the web panel
* 🌐 English and Persian language support
* 🇬🇧 English is the default language
* 🇮🇷 Persian with RTL interface
* 💾 SQLite database
* 🚀 systemd service support
* 🌐 Nginx reverse-proxy support
* 🐧 Ubuntu VPS deployment
* 🧩 Modular Python architecture

---

## 🏗️ Architecture

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

### Main components

| Component    | Purpose                         |
| ------------ | ------------------------------- |
| `bot/`       | Telegram bot logic and handlers |
| `database/`  | SQLite database operations      |
| `mail/`      | SMTP email delivery             |
| `web/`       | FastAPI administration panel    |
| `templates/` | Web UI templates                |
| `static/`    | CSS and JavaScript              |
| `config/`    | Application configuration       |
| `i18n.py`    | English/Persian translations    |

---

# 🌐 Languages

The application supports:

* 🇬🇧 English
* 🇮🇷 Persian

English is the default language.

The language can be changed from:

```text
Admin Panel → Settings → Language
```

The selected language is stored in the database.

When Persian is selected, the web interface uses RTL layout.

When English is selected, the web interface uses LTR layout.

---

# 🚀 Installation

## Requirements

Recommended environment:

* Ubuntu 22.04 or newer
* Python 3.11+
* SQLite
* Nginx for production
* A Telegram Bot
* An SMTP account

---

## 1. Clone the repository

```bash
cd /opt

git clone https://github.com/Alvanweb/telegram-file-mail-bot.git

cd telegram-file-mail-bot
```

You can also install a specific release:

```bash
git clone --branch v1.0.2 --depth 1 \
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

* Check that it is running as root
* Check the application files
* Install required Ubuntu packages
* Verify Python 3.11+
* Create the `telegrambot` service user
* Create the Python virtual environment
* Install Python dependencies
* Create runtime directories
* Create `.env` from `.env.example`
* Set secure file permissions
* Install the systemd service
* Enable the systemd service

### Application directory

The default application directory is:

```text
/opt/telegram-file-mail-bot
```

The installer is designed to install the application into this directory even when the repository was cloned from another location.

For example, cloning from `/root` is supported:

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

### Important

Never commit `.env` to GitHub.

The repository includes a `.gitignore` that excludes:

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

---

# 📧 SMTP Configuration

SMTP configuration can be managed from the administration panel.

Open:

```text
Admin Panel → Settings → SMTP
```

For Gmail:

```text
SMTP Host: smtp.gmail.com
SMTP Port: 587
TLS: Enabled
SMTP Username: your@gmail.com
SMTP Password: Gmail App Password
SMTP From: your@gmail.com
```

For Gmail, use an App Password instead of your normal Google account password.

The application can also be configured with other SMTP providers such as Brevo or compatible SMTP relay services.

---

# 🖥️ Administration Panel

The application provides a FastAPI administration panel.

## Default configuration

The production-safe default is:

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

## Temporary direct-access testing

For testing without Nginx, you can temporarily change `.env`:

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

### Security note

Do not use `0.0.0.0` as the normal production configuration unless you intentionally want the FastAPI application directly exposed.

For production, use:

```env
PANEL_HOST=127.0.0.1
PANEL_PORT=8000
```

with Nginx in front of the application.

---

# 📊 Dashboard

The dashboard provides:

* Total users
* Active users
* File statistics
* Delivery statistics
* Application status

---

# 👤 Users

The Users section provides:

* Registered users
* Telegram username
* Telegram ID
* Phone number
* Registration information
* Enable/disable users
* Delete users

---

# 📂 Files

The Files section provides:

* Uploaded file history
* File names
* File sizes
* Email subjects
* Delivery status
* Error information
* Pending file management

---

# ⚙️ Settings

The Settings section provides:

* 🌐 Language selection
* 📧 SMTP configuration
* 📬 Email recipients
* 📦 Total file-size limit
* 🧹 Pending file retention
* 🧾 Email content fields
* ✉️ SMTP connection testing

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

Use a strong:

```env
ADMIN_PASSWORD=
SESSION_SECRET=
```

and do not reuse sensitive credentials from other services.

---

# ⚙️ systemd

A systemd service file is included:

```text
telegram-file-mail-bot.service
```

The installer automatically installs and enables the service.

Start:

```bash
sudo systemctl start telegram-file-mail-bot
```

Enable at boot:

```bash
sudo systemctl enable telegram-file-mail-bot
```

Check status:

```bash
sudo systemctl status telegram-file-mail-bot
```

View logs:

```bash
sudo journalctl -u telegram-file-mail-bot -f
```

Restart:

```bash
sudo systemctl restart telegram-file-mail-bot
```

The service is configured to restart automatically if the application stops unexpectedly.

---

# 💾 Database

The project uses SQLite.

The database stores application data such as:

* Telegram users
* User registration information
* File history
* Pending uploads
* Application settings
* Language preference

The production database should never be committed to GitHub.

A new installation creates its own database.

---

# 📦 File Upload Flow

The normal user flow is:

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
Upload Files
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

Users can retry sending the email from Telegram when supported by the application flow.

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

Developed by MOЯ

GitHub:

https://github.com/Alvanweb

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

Contributions, bug reports, and feature requests are welcome.
