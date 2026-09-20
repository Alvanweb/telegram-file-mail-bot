import mimetypes, smtplib
from email.message import EmailMessage
from config.settings import smtp_config


def parse_recipients(value):
    if not value: return []
    normalized = value.replace(',', '\n').replace(';', '\n')
    return [x.strip() for x in normalized.splitlines() if x.strip()]


def send_email_sync(subject, body, attachments):
    cfg = smtp_config()
    recipients = parse_recipients(cfg['recipients'])
    if not recipients: raise RuntimeError('No email recipients configured')
    if not cfg['user'] or not cfg['password']: raise RuntimeError('SMTP credentials are not configured')
    msg = EmailMessage(); msg['From']=cfg['from']; msg['To']=', '.join(recipients); msg['Subject']=subject; msg.set_content(body)
    for path, filename in attachments:
        mime_type,_=mimetypes.guess_type(filename); maintype,subtype=(mime_type.split('/',1) if mime_type else ('application','octet-stream'))
        with open(path,'rb') as f: data=f.read()
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)
    with smtplib.SMTP(cfg['host'], cfg['port'], timeout=60) as smtp:
        smtp.ehlo()
        if cfg['use_tls']: smtp.starttls(); smtp.ehlo()
        smtp.login(cfg['user'], cfg['password']); smtp.send_message(msg)


def test_smtp():
    cfg=smtp_config(); recipients=parse_recipients(cfg['recipients'])
    if not recipients: raise RuntimeError('No email recipients configured')
    msg=EmailMessage(); msg['From']=cfg['from']; msg['To']=', '.join(recipients); msg['Subject']='File Mail SMTP Test'; msg.set_content('This email was sent to test the File Mail Bot SMTP configuration.')
    with smtplib.SMTP(cfg['host'], cfg['port'], timeout=20) as smtp:
        smtp.ehlo()
        if cfg['use_tls']: smtp.starttls(); smtp.ehlo()
        smtp.login(cfg['user'], cfg['password']); smtp.send_message(msg)
