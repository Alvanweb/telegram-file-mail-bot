#!/usr/bin/env bash
set -euo pipefail

# Telegram File Mail Bot Installer

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${APP_DIR:-${SCRIPT_DIR}}"

SERVICE_USER="${SERVICE_USER:-telegrambot}"
SERVICE_NAME="telegram-file-mail-bot"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo
echo "=========================================="
echo " Telegram File Mail Bot - Installer"
echo "=========================================="
echo

# --------------------------------------------------
# Root check
# --------------------------------------------------

if [[ "${EUID}" -ne 0 ]]; then
    error "Please run this installer as root or with sudo."
    exit 1
fi

# --------------------------------------------------
# Application directory
# --------------------------------------------------

info "Application directory:"
echo "  ${APP_DIR}"
echo

if [[ ! -f "${APP_DIR}/app.py" ]]; then
    error "Application files were not found:"
    echo "  ${APP_DIR}"
    echo
    echo "Clone the repository first:"
    echo "  git clone https://github.com/Alvanweb/telegram-file-mail-bot.git"
    echo "  cd telegram-file-mail-bot"
    echo "  sudo ./install.sh"
    exit 1
fi

if [[ ! -f "${APP_DIR}/requirements.txt" ]]; then
    error "requirements.txt was not found."
    exit 1
fi

if [[ ! -f "${APP_DIR}/telegram-file-mail-bot.service" ]]; then
    error "telegram-file-mail-bot.service was not found."
    exit 1
fi

# --------------------------------------------------
# Operating system
# --------------------------------------------------

if [[ ! -f /etc/os-release ]]; then
    error "Cannot detect operating system."
    exit 1
fi

source /etc/os-release

if [[ "${ID:-}" != "ubuntu" ]]; then
    warn "This installer is primarily tested on Ubuntu."
    warn "Detected OS: ${PRETTY_NAME:-unknown}"
    echo
fi

# --------------------------------------------------
# Install system packages
# --------------------------------------------------

info "Updating package lists..."

export DEBIAN_FRONTEND=noninteractive

apt-get update

info "Installing required packages..."

apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    ca-certificates

# --------------------------------------------------
# Python version
# --------------------------------------------------

PYTHON_VERSION=$(python3 -c \
'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

info "Detected Python ${PYTHON_VERSION}"

PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if (( PYTHON_MAJOR < 3 || (PYTHON_MAJOR == 3 && PYTHON_MINOR < 11) )); then
    error "Python 3.11 or newer is required."
    exit 1
fi

# --------------------------------------------------
# Service user
# --------------------------------------------------

if id -u "${SERVICE_USER}" >/dev/null 2>&1; then
    info "Service user '${SERVICE_USER}' already exists."
else
    info "Creating service user '${SERVICE_USER}'..."

    useradd \
        --system \
        --home-dir "${APP_DIR}" \
        --shell /usr/sbin/nologin \
        "${SERVICE_USER}"
fi

# --------------------------------------------------
# Virtual environment
# --------------------------------------------------

if [[ -d "${APP_DIR}/venv" ]]; then
    info "Existing virtual environment found."
else
    info "Creating Python virtual environment..."

    python3 -m venv "${APP_DIR}/venv"
fi

# --------------------------------------------------
# Python dependencies
# --------------------------------------------------

info "Installing Python dependencies..."

"${APP_DIR}/venv/bin/python" -m pip install --upgrade pip

"${APP_DIR}/venv/bin/pip" install \
    -r "${APP_DIR}/requirements.txt"

# --------------------------------------------------
# Runtime directories
# --------------------------------------------------

info "Creating runtime directories..."

mkdir -p \
    "${APP_DIR}/storage" \
    "${APP_DIR}/storage/pending_uploads"

# --------------------------------------------------
# Environment file
# --------------------------------------------------

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

# --------------------------------------------------
# Permissions
# --------------------------------------------------

info "Setting application permissions..."

chown -R "${SERVICE_USER}:${SERVICE_USER}" "${APP_DIR}"

chmod 600 "${APP_DIR}/.env"

# --------------------------------------------------
# Generate systemd service
# --------------------------------------------------

info "Installing systemd service..."

sed \
    -e "s|/opt/telegram-file-mail-bot|${APP_DIR}|g" \
    -e "s|User=telegrambot|User=${SERVICE_USER}|g" \
    -e "s|Group=telegrambot|Group=${SERVICE_USER}|g" \
    "${APP_DIR}/telegram-file-mail-bot.service" \
    > "${SERVICE_FILE}"

chmod 0644 "${SERVICE_FILE}"

systemctl daemon-reload

# --------------------------------------------------
# Enable service
# --------------------------------------------------

info "Enabling service..."

systemctl enable "${SERVICE_NAME}"

# --------------------------------------------------
# Finish
# --------------------------------------------------

echo
echo "=========================================="
echo " Installation completed successfully"
echo "=========================================="
echo
echo "Application directory:"
echo "  ${APP_DIR}"
echo
echo "Service:"
echo "  ${SERVICE_NAME}"
echo
echo "Next steps:"
echo
echo "1. Configure the environment:"
echo "   nano ${APP_DIR}/.env"
echo
echo "2. Start the application:"
echo "   systemctl start ${SERVICE_NAME}"
echo
echo "3. Check status:"
echo "   systemctl status ${SERVICE_NAME} --no-pager"
echo
echo "4. View logs:"
echo "   journalctl -u ${SERVICE_NAME} -f"
echo
