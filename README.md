# Telegram File Mail Bot

A modular Telegram bot that collects a user's phone number, accepts an email subject and multiple files, and sends the files as email attachments through SMTP.

The project also includes a lightweight Persian RTL web administration panel for users, file history, and runtime settings.

## Features

- Telegram phone-number registration
- Email subject collection before upload
- Multiple attachments in one email
- Configurable total upload-size limit
- Retry failed email delivery
- Start a new upload batch after successful delivery
- SQLite database
- Persian RTL admin panel
- User activation/deactivation
- File delivery history
- SMTP configuration from the admin panel
- Configurable email metadata fields
- Automatic cleanup of pending uploads
- systemd deployment
- Nginx reverse-proxy example
- Telegram polling (no webhook required)

## Project structure

```text
telegram-file-mail-bot/
├── app.py
├── bot/
├── config/
├── database/
├── mail/
├── web/
├── templates/
├── static/
├── storage/
├── .env.example
├── .gitignore
├── install.sh
├── nginx.conf.example
├── requirements.txt
├── telegram-file-mail-bot.service
└── LICENSE
```

## Requirements

- Ubuntu 22.04+ recommended
- Python 3.10+
- A Telegram bot token
- An SMTP account/provider
- Optional: Nginx for public web access

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/telegram-file-mail-bot.git
cd telegram-file-mail-bot
```

Create the private environment file:

```bash
cp .env.example .env
nano .env
```

Set at least:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
ADMIN_USERNAME=admin
ADMIN_PASSWORD=YOUR_STRONG_PASSWORD
SESSION_SECRET=YOUR_LONG_RANDOM_SECRET
```

Then run:

```bash
chmod +x install.sh
sudo ./install.sh
```

The installer creates the `telegrambot` service account, Python virtual environment, installs dependencies, prepares storage, installs systemd, and starts the service.

Check the service:

```bash
sudo systemctl status telegram-file-mail-bot --no-pager
```

## Admin panel

By default the FastAPI application listens on:

```text
127.0.0.1:8000
```

Use Nginx if the panel needs to be reachable through a domain.

An example configuration is provided in:

```text
nginx.conf.example
```

## SMTP configuration

SMTP credentials, recipients, upload limits, retention, and email metadata settings are stored in SQLite and can be changed from:

```text
/settings
```

The default SMTP configuration is intended as a starting point only. Configure the provider you actually use.

For Gmail SMTP, use an App Password rather than your normal Google account password.

## Database

The application creates `bot.db` automatically on first start.

The database contains:

- registered Telegram users
- file history
- pending uploads
- application settings

Do not commit `bot.db` to a public repository.

## Security

Never commit:

- `.env`
- `bot.db`
- SMTP passwords
- Telegram bot tokens
- admin passwords
- session secrets
- uploaded files
- server-specific backups

If a Telegram bot token or SMTP credential is ever exposed, revoke/rotate it immediately.

## Backup

For a private deployment, back up both the database and environment configuration.

Example:

```bash
sudo cp /opt/telegram-file-mail-bot/.env /root/telegram-file-mail-bot.env.backup
sudo cp /opt/telegram-file-mail-bot/bot.db /root/telegram-file-mail-bot.db.backup
```

Keep these backups private.

## systemd

The included service file is:

```text
telegram-file-mail-bot.service
```

Useful commands:

```bash
sudo systemctl enable telegram-file-mail-bot
sudo systemctl start telegram-file-mail-bot
sudo systemctl restart telegram-file-mail-bot
sudo systemctl status telegram-file-mail-bot --no-pager
sudo journalctl -u telegram-file-mail-bot -n 100 --no-pager
```

## License

MIT License. See `LICENSE`.

## 🌐 Localization

The project supports two languages:

- **English** — default
- **فارسی (Persian)** — RTL

The language can be changed from **Settings → Language** in the admin panel. The selected language is stored in SQLite and is used by both the web panel and Telegram bot messages.

No environment variable is required for the language setting.
