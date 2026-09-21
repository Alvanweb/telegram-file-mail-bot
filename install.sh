#!/usr/bin/env bash
set -euo pipefail

# Telegram File Mail Bot Installer

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${APP_DIR:-/opt/telegram-file-mail-bot}"

SERVICE_USER="${SERVICE_USER:-telegrambot}"
SERVICE_NAME="telegram-file-mail-bot"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo
echo "=========================================="
echo " Telegram File Mail Bot - Installer"
echo "=========================================="
echo

if [[ "${EUID}" -ne 0 ]]; then
    error "Please run this installer as root or with sudo."
    exit 1
fi

if [[ ! -f "${SCRIPT_DIR}/app.py" ]]; then
    error "app.py was not found in:"
    echo "  ${SCRIPT_DIR}"
    exit 1
fi

if [[ ! -f "${SCRIPT_DIR}/requirements.txt" ]]; then
    error "requirements.txt was not found."
    exit 1
fi

if [[ ! -f "${SCRIPT_DIR}/telegram-file-mail-bot.service" ]]; then
    error "telegram-file-mail-bot.service was not found."
    exit 1
fi

info "Source directory:"
echo "  ${SCRIPT_DIR}"
info "Application directory:"
echo "  ${APP_DIR}"
echo

if [[ "${SCRIPT_DIR}" != "${APP_DIR}" ]]; then
    if [[ -e "${APP_DIR}" ]]; then
        if [[ -n "$(find "${APP_DIR}" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then
            error "Target directory is not empty:"
            echo "  ${APP_DIR}"
            echo
            echo "Please remove it or set APP_DIR to another location."
            exit 1
        fi
    else
        mkdir -p "${APP_DIR}"
    fi
    info "Copying application files..."
    cp -a "${SCRIPT_DIR}/." "${APP_DIR}/"
else
    info "Application is already in the target directory."
fi

if [[ ! -f /etc/os-release ]]; then
    error "Cannot detect operating system."
    exit 1
fi
source /etc/os-release

if [[ "${ID:-}" != "ubuntu" ]]; then
    warn "This installer is primarily tested on Ubuntu."
    warn "Detected OS: ${PRETTY_NAME:-unknown}"
fi

export DEBIAN_FRONTEND=noninteractive
info "Updating package lists..."
apt-get update

info "Installing required packages..."
apt-get install -y python3 python3-venv python3-pip ca-certificates

PYTHON_MAJOR="$(python3 -c 'import sys; print(sys.version_info.major)')"
PYTHON_MINOR="$(python3 -c 'import sys; print(sys.version_info.minor)')"
PYTHON_VERSION="${PYTHON_MAJOR}.${PYTHON_MINOR}"

info "Detected Python ${PYTHON_VERSION}"

if (( PYTHON_MAJOR < 3 || (PYTHON_MAJOR == 3 && PYTHON_MINOR < 11) )); then
    error "Python 3.11 or newer is required."
    exit 1
fi

if id -u "${SERVICE_USER}" >/dev/null 2>&1; then
    info "Service user '${SERVICE_USER}' already exists."
else
    info "Creating service user '${SERVICE_USER}'..."
    useradd --system --home-dir "${APP_DIR}" --shell /usr/sbin/nologin "${SERVICE_USER}"
fi

if [[ -d "${APP_DIR}/venv" ]]; then
    info "Existing virtual environment found."
else
    info "Creating Python virtual environment..."
    python3 -m venv "${APP_DIR}/venv"
fi

info "Installing Python dependencies..."
"${APP_DIR}/venv/bin/python" -m pip install --upgrade pip
"${APP_DIR}/venv/bin/python" -m pip install -r "${APP_DIR}/requirements.txt"

info "Creating runtime directories..."
mkdir -p "${APP_DIR}/storage" "${APP_DIR}/storage/pending_uploads"

if [[ -f "${APP_DIR}/.env" ]]; then
    info ".env already exists. Keeping existing configuration."
else
    if [[ ! -f "${APP_DIR}/.env.example" ]]; then
        error ".env.example was not found."
        exit 1
    fi
    info "Creating .env from .env.example..."
    cp "${APP_DIR}/.env.example" "${APP_DIR}/.env"
    warn "You must configure .env before starting the application."
fi

info "Setting application permissions..."
chown -R "${SERVICE_USER}:${SERVICE_USER}" "${APP_DIR}"
chmod 600 "${APP_DIR}/.env"

info "Installing systemd service..."
sed \
    -e "s|/opt/telegram-file-mail-bot|${APP_DIR}|g" \
    -e "s|User=telegrambot|User=${SERVICE_USER}|g" \
    -e "s|Group=telegrambot|Group=${SERVICE_USER}|g" \
    "${APP_DIR}/telegram-file-mail-bot.service" \
    > "${SERVICE_FILE}"

chmod 0644 "${SERVICE_FILE}"
systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"

echo
echo "=========================================="
echo " Installation completed"
echo "=========================================="
echo
info "Application directory:"
echo "  ${APP_DIR}"
info "Service:"
echo "  ${SERVICE_NAME}"
echo
warn "Configure .env before starting the application:"
echo "  ${APP_DIR}/.env"
echo
echo "Start:"
echo "  systemctl start ${SERVICE_NAME}"
echo
echo "Status:"
echo "  systemctl status ${SERVICE_NAME}"
echo
echo "Logs:"
echo "  journalctl -u ${SERVICE_NAME} -f"
echo
