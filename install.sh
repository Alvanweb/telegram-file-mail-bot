#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/telegram-file-mail-bot}"
SERVICE_USER="${SERVICE_USER:-telegrambot}"
SERVICE_NAME="telegram-file-mail-bot"

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this installer as root or with sudo."
  exit 1
fi

if [[ ! -f "${APP_DIR}/app.py" ]]; then
  echo "Application files were not found at ${APP_DIR}."
  echo "Clone/copy the project there first, or set APP_DIR=/path/to/project."
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python3 python3-venv python3-pip

if ! id -u "${SERVICE_USER}" >/dev/null 2>&1; then
  useradd --system --home "${APP_DIR}" --shell /usr/sbin/nologin "${SERVICE_USER}"
fi

python3 -m venv "${APP_DIR}/venv"
"${APP_DIR}/venv/bin/pip" install --upgrade pip
"${APP_DIR}/venv/bin/pip" install -r "${APP_DIR}/requirements.txt"

mkdir -p "${APP_DIR}/storage/pending_uploads"

if [[ ! -f "${APP_DIR}/.env" ]]; then
  cp "${APP_DIR}/.env.example" "${APP_DIR}/.env"
  echo "Created ${APP_DIR}/.env from .env.example."
  echo "Edit it and set BOT_TOKEN, ADMIN_PASSWORD and SESSION_SECRET before starting the service."
fi

chown -R "${SERVICE_USER}:${SERVICE_USER}" "${APP_DIR}"
chmod 600 "${APP_DIR}/.env"

install -m 0644 "${APP_DIR}/telegram-file-mail-bot.service"   "/etc/systemd/system/${SERVICE_NAME}.service"

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"

echo
echo "Installation completed."
echo "Edit ${APP_DIR}/.env if needed, then run:"
echo "  systemctl restart ${SERVICE_NAME}"
echo "  systemctl status ${SERVICE_NAME} --no-pager"
