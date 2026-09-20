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

## 🌐 Languages

The application supports:

* 🇬🇧 English
* 🇮🇷 Persian

English is used by default.

The language can be changed from:

```text
Admin Panel → Settings → Language
```

The selected language is stored in the database.

When Persian is selected, the web interface uses RTL layout.

---

# 🚀 Installation

## Requirements

Recommended environment:

* Ubuntu 22.04 or newer
* Python 3.11+
* SQLite
* Nginx (optional)
* A Telegram Bot
* An SMTP account

---

## 1. Clone the repository

```bash
git clone https://github.com/Alvanweb/telegram-file-mail-bot.git
cd telegram-file-mail-bot
```

---

## 2. Run the installer

```bash
chmod +x install.sh
sudo ./install.sh
```

The installer prepares the Python environment and application dependencies.

---

## 3. Configure environment variables

Copy the example configuration:

```bash
cp .env.example .env
```

Edit it:

```bash
nano .env
```

Example:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

ADMIN_USERNAME=admin
ADMIN_PASSWORD=CHANGE_THIS_PASSWORD
SESSION_SECRET=CHANGE_THIS_TO_A_RANDOM_SECRET

DB_PATH=/opt/telegram-file-mail-bot/bot.db
PANEL_HOST=127.0.0.1
PANEL_PORT=8000
```

### Important

Never commit `.env` to GitHub.

The `.gitignore` file already excludes it.

---

# 🤖 Telegram Bot

Create a Telegram bot using **BotFather** and obtain its token.

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
Settings → SMTP
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

For Gmail, use an **App Password** instead of your normal Google account password.

---

# 🖥️ Administration Panel

The application provides a FastAPI administration panel.

The default local address is:

```text
http://127.0.0.1:8000
```

The panel provides:

### Dashboard

* Total users
* Active users
* File statistics
* Delivery statistics

### Users

* View registered users
* View Telegram information
* Enable/disable users
* Remove users

### Files

* View uploaded files
* View delivery status
* View errors
* View file history

### Settings

* Language
* SMTP configuration
* Email recipients
* File-size limits
* Retention settings
* Other application settings

---

# 🔐 Security

Do not publish or commit:

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

If a Telegram bot token or SMTP credential is accidentally exposed, revoke/rotate it immediately.

---

# 🌐 Nginx

An example Nginx configuration is included:

```text
nginx.conf.example
```

The recommended architecture is:

```text
Internet
   │
   ▼
 Nginx
   │
   ▼
FastAPI :8000
```

Telegram polling runs independently:

```text
Telegram
   │
   ▼
Telegram Bot
   │
   ▼
Application
```

---

# ⚙️ systemd

A systemd service file is included:

```text
telegram-file-mail-bot.service
```

After installation:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-file-mail-bot
sudo systemctl start telegram-file-mail-bot
```

Check status:

```bash
sudo systemctl status telegram-file-mail-bot
```

View logs:

```bash
sudo journalctl -u telegram-file-mail-bot -f
```

The service is configured to restart automatically if the application stops unexpectedly.

---

# 💾 Database

The project uses SQLite.

The database contains application data such as:

* Telegram users
* User registration information
* File history
* Pending uploads
* Application settings
* Language preference

The production database should not be committed to GitHub.

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

---

# 🔄 Failed Delivery

If email delivery fails, the uploaded files remain available for retry according to the application's retention and cleanup settings.

Users can retry sending the email from Telegram.

---

# 🛠️ Development

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

# 📁 Project Data

Runtime data should remain outside the public source history.

Typical production files include:

```text
.env
bot.db
storage/pending_uploads/
```

These files are intentionally excluded from Git.

---

# 🐛 Troubleshooting

### Check service status

```bash
systemctl status telegram-file-mail-bot
```

### View application logs

```bash
journalctl -u telegram-file-mail-bot -n 100 --no-pager
```

### Restart the service

```bash
systemctl restart telegram-file-mail-bot
```

### Check Python dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Check whether port 8000 is listening

```bash
ss -lntp | grep 8000
```

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
