from i18n import tr, language, SUPPORTED

def context():
    lang = language()
    return {'lang': lang, 'dir': 'rtl' if lang == 'fa' else 'ltr', 't': tr}
