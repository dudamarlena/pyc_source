# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/web2py_utils/email_sms/send.py
# Compiled at: 2010-04-28 20:50:50
TEMPLATES = dict(email='From: %(frm)s\r\nTo: %(to)s\r\nSubject: %(subject)s\r\n%(body)s', sms='From: %(frm)s\r\nTo: %(to)s\r\n%(body)s')

def open_smtp(settings):
    """
    Connects to the SMTP server using mail.settings.
    
    Returns SMTP server object, connected and logged in.
    """
    import smtplib
    (host, port) = settings.server.split(':')
    (username, password) = settings.login.split(':')
    try:
        serv = smtplib.SMTP(host, port)
        serv.ehlo()
        serv.starttls()
        serv.ehlo()
        serv.login(username, password)
    except:
        serv = None

    return serv


def send(message, record, typ='email', serv=None, close_smtp=False, logger=None):
    """
    Sends a ``message`` to ``record`` by ``typ`` using ``serv``. Optionally
    closes the smtp connection if ``close_smtp=True``.
    
    If ``serv=None`` it will create a new SMTP server object using ``open_smtp()``.
        Also, it will close the smtp connection autmatically if serv=None
    """
    if not serv:
        serv = open_smtp()
        close_smtp = True
    context = dict(frm=mail.settings.sender, to=panel[typ], subject=message.subject, body=message.content, footer=footer)
    the_msg = TEMPLATES[typ] % context
    serv.sendmail(context['frm'], context['to'], the_msg)
    if callable(logger):
        logger(msg=message, panel=panel, sent_on=datetime.now())
    if close_smtp:
        serv.close()
    return True