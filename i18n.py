from database.settings import get_setting

SUPPORTED = {"en": "English", "fa": "فارسی"}

TEXT = {
    "en": {
        "login_title": "Login | File Mail", "admin_panel": "Admin Panel", "welcome": "Welcome",
        "login_hint": "Enter your administrator credentials to continue.", "username": "Username", "password": "Password", "login": "Sign in",
        "invalid_login": "Invalid username or password.", "bot_management": "Telegram Bot Management", "dashboard": "Dashboard",
        "users": "Users", "files": "Files", "settings": "Settings", "logout": "Logout", "overview": "Overview",
        "service_active": "Service active", "total_users": "Total users", "active_users": "Active users", "blocked_users": "Blocked users",
        "total_files": "Total files", "successful_files": "Successful sends", "failed_files": "Failed sends", "system_status": "System status",
        "system_status_hint": "Quick service health overview", "telegram_bot": "Telegram bot", "polling_active": "Polling is active",
        "database": "Database", "sqlite_available": "SQLite is available", "web_panel": "Web panel", "fastapi_nginx": "FastAPI / Nginx",
        "management": "Management", "registered_users": "Registered bot users", "search_users": "Search users...", "name": "Name",
        "phone": "Phone", "status": "Status", "actions": "Actions", "active": "Active", "blocked": "Blocked", "block": "Block",
        "activate": "Activate", "delete": "Delete", "no_users": "No users registered yet.", "confirm_delete": "Are you sure you want to delete this user and their file history?",
        "send_report": "Send report", "file_history": "Received files and email status", "search_files": "Search files...", "subject": "Subject",
        "filename": "Filename", "size": "Size", "success": "Success", "error": "Error", "processing": "Processing", "time": "Time", "no_files": "No files recorded yet.",
        "configuration": "Configuration", "smtp_settings": "SMTP settings", "smtp_hint": "Connection and email recipient settings", "smtp_host": "SMTP Host",
        "smtp_port": "SMTP Port", "smtp_username": "SMTP Username", "smtp_password": "SMTP Password", "smtp_password_hint": "Leave blank to keep the current password",
        "smtp_from": "SMTP From", "recipients": "Email recipients", "one_per_line": "One email per line", "use_tls": "Use TLS",
        "file_management": "File management", "file_management_hint": "Successfully sent files are deleted; failed or abandoned files remain for the configured period.",
        "max_total": "Maximum total upload size per send (MB)", "retention": "Retention for failed/abandoned files (hours)", "email_content": "Email content",
        "email_content_hint": "Select the information to include with the attachments.", "save_settings": "Save settings", "test_smtp": "Test SMTP",
        "settings_saved": "Settings saved successfully.", "test_success": "Test email sent successfully.", "test_failed": "SMTP test failed: {error}",
        "size_range": "Allowed size must be between 1 and 100 MB.", "retention_range": "Retention must be between 1 and 720 hours.", "recipient_required": "At least one recipient email is required.",
        "full_name": "Full name", "telegram_username": "Telegram username", "telegram_id": "Telegram ID", "mobile": "Mobile number",
        "file_count": "File count", "total_size": "Total size", "filenames": "Filenames", "email_subject": "Email subject",
        "mail_service": "File Mail Service", "bot_name": "File Mail", "bot_about": "Telegram bot management",
        "lang": "Language", "english": "English", "persian": "Persian", "language_hint": "Choose the language used by the web panel and Telegram bot.",
        "language_saved": "Language updated successfully.",
        "unknown_error": "An unexpected error occurred.",
        "telegram_blocked": "⛔ Your access to the bot is blocked.", "register_prompt": "Hello 👋\n\nPlease register your mobile number before using the bot.",
        "register_button": "📱 Register mobile number", "subject_prompt": "📧 Please enter the *email subject*:",
        "wrong_contact": "❌ Please send your own mobile number using the registration button.", "registered": "✅ Registration completed successfully.\n\n📧 Now enter the *email subject*.",
        "start_register": "❌ Please register first with /start and provide your mobile number.", "subject_too_long": "❌ The *email subject* must be 200 characters or fewer.",
        "subject_saved": "✅ Email subject saved.\n\n📎 Now send your files.\nMaximum total file size: {mb} MB\n\nAfter sending all files, press «📤 Send email».",
        "blocked": "⛔ Your access is blocked.", "subject_first": "❗ Please enter the *email subject* first.", "unsupported": "❌ This file type is not supported.",
        "size_limit": "❌ The total file size would exceed the allowed limit.\n\nCurrent total: {current:.2f} MB\nNew file: {new:.2f} MB\nMaximum total: {maximum} MB",
        "receiving": "⏳ Receiving file...", "file_added": "✅ File added.\n\n{summary}\n\nYou can send another file or press the button below to send the email.",
        "download_failed": "❌ File download failed. Please try again.", "sending": "⏳ Sending {count} files by email...\nTotal size: {total:.2f} MB",
        "subject_missing": "❌ *Email subject* not found. Please start again with /start.", "no_files": "❌ There are no files to send yet.",
        "total_limit": "❌ The total file size exceeds the allowed limit.", "mail_success": "✅ Email sent successfully.\n\n📎 Files: {count}\n📦 Total size: {total:.2f} MB\n\nTo send a new email, press the button below.",
        "send_failed": "❌ Email sending failed.\n\nYour files were not deleted. You can press Send email again.", "cancelled": "🗑 Selected files were deleted.\n\nTo start again, enter a new *email subject*.",
        "cancel_command": "🗑 Operation cancelled.\n\n📧 Enter a new *email subject*.", "restart": "🔄 Start again\n\n📧 Please enter the new *email subject*.",
        "send_email": "📤 Send email", "cancel_restart": "🗑 Cancel and restart", "new_file": "🔄 Send new files",
        "summary": "📎 {count} files\n📦 Total size: {total:.2f} / {maximum} MB",
    },
    "fa": {
        "login_title": "ورود | File Mail", "admin_panel": "پنل مدیریت", "welcome": "خوش آمدید",
        "login_hint": "برای ورود، اطلاعات مدیر را وارد کنید.", "username": "نام کاربری", "password": "رمز عبور", "login": "ورود به پنل",
        "invalid_login": "نام کاربری یا رمز عبور اشتباه است.", "bot_management": "مدیریت ربات تلگرام", "dashboard": "داشبورد",
        "users": "کاربران", "files": "فایل‌ها", "settings": "تنظیمات", "logout": "خروج", "overview": "نمای کلی",
        "service_active": "سرویس فعال", "total_users": "کل کاربران", "active_users": "کاربران فعال", "blocked_users": "کاربران مسدود",
        "total_files": "کل فایل‌ها", "successful_files": "ارسال موفق", "failed_files": "ارسال ناموفق", "system_status": "وضعیت سیستم",
        "system_status_hint": "نمایش سریع وضعیت سرویس‌ها", "telegram_bot": "ربات تلگرام", "polling_active": "Polling فعال است",
        "database": "پایگاه داده", "sqlite_available": "SQLite در دسترس است", "web_panel": "پنل وب", "fastapi_nginx": "FastAPI / Nginx",
        "management": "مدیریت", "registered_users": "کاربران ثبت‌نام‌شده ربات", "search_users": "جستجو در کاربران...", "name": "نام",
        "phone": "شماره", "status": "وضعیت", "actions": "عملیات", "active": "فعال", "blocked": "مسدود", "block": "مسدود کردن",
        "activate": "فعال کردن", "delete": "حذف", "no_users": "هنوز کاربری ثبت نشده است.", "confirm_delete": "آیا از حذف این کاربر و سوابق فایل او مطمئن هستید؟",
        "send_report": "گزارش ارسال", "file_history": "سوابق فایل‌های دریافت‌شده و وضعیت ایمیل", "search_files": "جستجو در فایل‌ها...", "subject": "موضوع",
        "filename": "نام فایل", "size": "حجم", "success": "موفق", "error": "خطا", "processing": "در حال پردازش", "time": "زمان", "no_files": "هنوز فایلی ثبت نشده است.",
        "configuration": "پیکربندی", "smtp_settings": "تنظیمات SMTP", "smtp_hint": "اطلاعات اتصال و گیرندگان ایمیل", "smtp_host": "SMTP Host",
        "smtp_port": "SMTP Port", "smtp_username": "SMTP Username", "smtp_password": "SMTP Password", "smtp_password_hint": "برای حفظ رمز فعلی خالی بگذارید",
        "smtp_from": "SMTP From", "recipients": "گیرندگان ایمیل", "one_per_line": "هر ایمیل در یک خط", "use_tls": "استفاده از TLS",
        "file_management": "مدیریت فایل", "file_management_hint": "فایل‌ها پس از ارسال موفق حذف می‌شوند؛ فایل‌های ناموفق یا رهاشده تا مدت تعیین‌شده باقی می‌مانند.",
        "max_total": "حداکثر حجم مجموع هر ارسال (MB)", "retention": "مدت نگهداری فایل‌های ناموفق/رهاشده (ساعت)", "email_content": "اطلاعات داخل ایمیل",
        "email_content_hint": "مواردی را که می‌خواهید همراه فایل‌ها برای گیرنده ارسال شود انتخاب کنید.", "save_settings": "ذخیره تنظیمات", "test_smtp": "تست SMTP",
        "settings_saved": "تنظیمات با موفقیت ذخیره شد.", "test_success": "ایمیل تست با موفقیت ارسال شد.", "test_failed": "تست SMTP ناموفق بود: {error}",
        "size_range": "حجم مجاز باید بین ۱ تا ۱۰۰ مگابایت باشد.", "retention_range": "مدت نگهداری باید بین ۱ تا ۷۲۰ ساعت باشد.", "recipient_required": "حداقل یک ایمیل گیرنده وارد کنید.",
        "full_name": "نام و نام خانوادگی", "telegram_username": "نام کاربری تلگرام", "telegram_id": "Telegram ID", "mobile": "شماره موبایل",
        "file_count": "تعداد فایل‌ها", "total_size": "حجم مجموع", "filenames": "نام فایل‌ها", "email_subject": "موضوع",
        "mail_service": "سرویس File Mail", "bot_name": "File Mail", "bot_about": "مدیریت ربات تلگرام",
        "lang": "زبان", "english": "انگلیسی", "persian": "فارسی", "language_hint": "زبان پنل وب و پیام‌های ربات تلگرام را انتخاب کنید.",
        "language_saved": "زبان با موفقیت تغییر کرد.", "unknown_error": "خطای غیرمنتظره رخ داد.",
        "telegram_blocked": "⛔ دسترسی شما به ربات مسدود شده است.", "register_prompt": "سلام 👋\n\nبرای استفاده از ربات ابتدا شماره موبایل خود را ثبت کنید.",
        "register_button": "📱 ثبت شماره موبایل", "subject_prompt": "📧 لطفاً *موضوع ایمیل* را وارد کنید:",
        "wrong_contact": "❌ لطفاً شماره موبایل خودتان را با دکمه ثبت شماره ارسال کنید.", "registered": "✅ ثبت‌نام با موفقیت انجام شد.\n\n📧 حالا *موضوع ایمیل* را وارد کنید.",
        "start_register": "❌ ابتدا با /start شماره موبایل خود را ثبت کنید.", "subject_too_long": "❌ *موضوع ایمیل* حداکثر ۲۰۰ کاراکتر باشد.",
        "subject_saved": "✅ موضوع ایمیل ثبت شد.\n\n📎 حالا فایل‌ها را ارسال کنید.\nحداکثر حجم مجموع فایل‌ها: {mb} MB\n\nبعد از ارسال همه فایل‌ها، روی «📤 ارسال ایمیل» بزنید.",
        "blocked": "⛔ دسترسی شما مسدود شده است.", "subject_first": "❗ ابتدا *موضوع ایمیل* را وارد کنید.", "unsupported": "❌ این نوع فایل پشتیبانی نمی‌شود.",
        "size_limit": "❌ حجم مجموع فایل‌ها از حد مجاز بیشتر می‌شود.\n\nحجم فعلی: {current:.2f} MB\nحجم فایل جدید: {new:.2f} MB\nحداکثر مجموع: {maximum} MB",
        "receiving": "⏳ فایل در حال دریافت است...", "file_added": "✅ فایل اضافه شد.\n\n{summary}\n\nمی‌توانید فایل دیگری بفرستید یا برای ارسال ایمیل روی دکمه زیر بزنید.",
        "download_failed": "❌ دریافت فایل ناموفق بود. لطفاً دوباره تلاش کنید.", "sending": "⏳ در حال ارسال {count} فایل به ایمیل...\nحجم مجموع: {total:.2f} MB",
        "subject_missing": "❌ *موضوع ایمیل* پیدا نشد. دوباره /start را بزنید.", "no_files": "❌ هنوز فایلی برای ارسال وجود ندارد.",
        "total_limit": "❌ حجم مجموع فایل‌ها از حد مجاز بیشتر است.", "mail_success": "✅ ایمیل با موفقیت ارسال شد.\n\n📎 تعداد فایل‌ها: {count}\n📦 حجم مجموع: {total:.2f} MB\n\nبرای ارسال ایمیل جدید، روی دکمه زیر بزنید.",
        "send_failed": "❌ ارسال ایمیل ناموفق بود.\n\nفایل‌ها حذف نشده‌اند و می‌توانید دوباره دکمه ارسال ایمیل را بزنید.", "cancelled": "🗑 فایل‌های انتخاب‌شده حذف شدند.\n\nبرای شروع دوباره، *موضوع ایمیل* را ارسال کنید.",
        "cancel_command": "🗑 عملیات لغو شد.\n\n📧 *موضوع ایمیل* جدید را وارد کنید.", "restart": "🔄شروع مجدد\n\n📧 لطفاً *موضوع ایمیل* جدید را وارد کنید.",
        "send_email": "📤 ارسال ایمیل", "cancel_restart": "🗑 لغو و شروع مجدد", "new_file": "🔄 ارسال فایل جدید",
        "summary": "📎 {count} فایل\n📦 حجم مجموع: {total:.2f} / {maximum} MB",
    },
}


def language():
    try:
        lang = str(get_setting("language", "en")).lower()
    except Exception:
        lang = "en"
    return lang if lang in SUPPORTED else "en"


def tr(key, **kwargs):
    value = TEXT.get(language(), TEXT["en"]).get(key, TEXT["en"].get(key, key))
    return value.format(**kwargs) if kwargs else value


def is_rtl():
    return language() == "fa"
