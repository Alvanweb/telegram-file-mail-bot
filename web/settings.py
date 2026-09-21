import json

from fastapi import Request, Form
from fastapi.responses import RedirectResponse

from web.auth import logged
from web.i18n import context

from config.settings import (
    smtp_config,
    max_total_mb,
    pending_retention_hours,
)

from database.settings import get_setting, set_setting
from mail.smtp import test_smtp

from i18n import tr, SUPPORTED


FIELDS = [
    ("first_name", "full_name"),
    ("username", "telegram_username"),
    ("phone", "mobile"),
    ("telegram_id", "telegram_id"),
    ("subject", "email_subject"),
    ("file_count", "file_count"),
    ("total_size", "total_size"),
    ("filenames", "filenames"),
]


def setup_routes(app, templates):

    # =========================================================
    # Settings page
    # =========================================================

    @app.get("/settings")
    async def settings_page(request: Request):

        if not logged(request):
            return RedirectResponse("/login", status_code=303)

        cfg = smtp_config()

        try:
            selected = json.loads(
                get_setting("email_fields", "[]")
            )
        except Exception:
            selected = []

        return templates.TemplateResponse(
            request=request,
            name="settings.html",
            context={
                **context(),

                "smtp": cfg,

                "max_total_mb": max_total_mb(),

                "retention": pending_retention_hours(),

                "selected_fields": selected,

                "fields": FIELDS,

                "languages": SUPPORTED,

                "selected_language": get_setting(
                    "language",
                    "en"
                ),

                "message": request.session.pop(
                    "settings_message",
                    None
                ),

                "error": request.session.pop(
                    "settings_error",
                    None
                ),
            },
        )

    # =========================================================
    # Save language
    # =========================================================

    @app.post("/settings/language")
    async def save_language(
        request: Request,
        language: str = Form("en"),
    ):

        if not logged(request):
            return RedirectResponse(
                "/login",
                status_code=303
            )

        # Validate language
        if language not in SUPPORTED:
            language = "en"

        # Save language first
        set_setting(
            "language",
            language
        )

        # Use i18n translation instead of hard-coded
        # Persian/English text.
        #
        # This prevents encoding problems such as:
        # ???? ?? ?????? ????? ???.
        request.session["settings_message"] = tr(
            "language_saved"
        )

        return RedirectResponse(
            "/settings",
            status_code=303
        )

    # =========================================================
    # Save SMTP / general settings
    # =========================================================

    @app.post("/settings")
    async def save_settings(
        request: Request,

        smtp_host: str = Form(...),

        smtp_port: int = Form(...),

        smtp_user: str = Form(...),

        smtp_password: str = Form(""),

        smtp_from: str = Form(...),

        smtp_recipients: str = Form(...),

        smtp_use_tls: str = Form("false"),

        max_total_mb_value: int = Form(...),

        retention_hours: int = Form(...),

        email_fields: list[str] = Form([]),
    ):

        if not logged(request):
            return RedirectResponse(
                "/login",
                status_code=303
            )

        # -----------------------------------------------------
        # Validate max total file size
        # -----------------------------------------------------

        if (
            max_total_mb_value < 1
            or max_total_mb_value > 100
        ):
            request.session["settings_error"] = tr(
                "size_range"
            )

            return RedirectResponse(
                "/settings",
                status_code=303
            )

        # -----------------------------------------------------
        # Validate retention
        # -----------------------------------------------------

        if (
            retention_hours < 1
            or retention_hours > 720
        ):
            request.session["settings_error"] = tr(
                "retention_range"
            )

            return RedirectResponse(
                "/settings",
                status_code=303
            )

        # -----------------------------------------------------
        # Process recipients
        # -----------------------------------------------------

        recipients = [
            x.strip()
            for x in (
                smtp_recipients
                .replace(";", "\n")
                .replace(",", "\n")
                .splitlines()
            )
            if x.strip()
        ]

        if not recipients:

            request.session["settings_error"] = tr(
                "recipient_required"
            )

            return RedirectResponse(
                "/settings",
                status_code=303
            )

        # -----------------------------------------------------
        # Save settings
        # -----------------------------------------------------

        settings = {
            "smtp_host": smtp_host.strip(),

            "smtp_port": smtp_port,

            "smtp_user": smtp_user.strip(),

            "smtp_from": smtp_from.strip(),

            "smtp_recipients": "\n".join(
                recipients
            ),

            "smtp_use_tls": (
                "true"
                if smtp_use_tls == "true"
                else "false"
            ),

            "max_total_mb": max_total_mb_value,

            "pending_retention_hours": retention_hours,

            "email_fields": json.dumps(
                email_fields,
                ensure_ascii=False
            ),
        }

        for key, value in settings.items():
            set_setting(
                key,
                value
            )

        # -----------------------------------------------------
        # Only update SMTP password if a new password
        # was entered.
        # -----------------------------------------------------

        if smtp_password:
            set_setting(
                "smtp_password",
                smtp_password
            )

        # -----------------------------------------------------
        # Success message
        # -----------------------------------------------------

        request.session["settings_message"] = tr(
            "settings_saved"
        )

        return RedirectResponse(
            "/settings",
            status_code=303
        )

    # =========================================================
    # SMTP test
    # =========================================================

    @app.post("/settings/test-smtp")
    async def smtp_test(request: Request):

        if not logged(request):
            return RedirectResponse(
                "/login",
                status_code=303
            )

        try:

            test_smtp()

            request.session["settings_message"] = tr(
                "test_success"
            )

        except Exception as exc:

            request.session["settings_error"] = tr(
                "test_failed",
                error=exc
            )

        return RedirectResponse(
            "/settings",
            status_code=303
        )
