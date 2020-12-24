# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/olympo/enviaremail.py
# Compiled at: 2012-03-22 06:34:55
from email import Encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, smtplib

def enviar_email(remitente, destinatarios, asunto, mensaje, servidor, login, password, ficheros=[], html='', charset='iso-8859-1'):
    u"""
    IN
      remitente      (<email>, <nombre>)
      destinatarios  [(<email>, <nombre>), ...]
      asunto         <str>
      mensaje        <str>
      servidor       <str>
      login          <str>
      password       <str>
      ficheros       [<str>, ...] (opcional)
                     [(<StringIO>, <str>), ...] (opcional)
      html           <str>        (opcional)
      
      Por ejemplo,
        enviar_email(('pperez@gmail.com', 'Pepe Pérez'),
                     [('malopez@gmail.com', 'María López'), (mlopez@yahoo.com, 'María')],
                     'Hola, mundo!', '¿Qué tal por ahí?

Pepe',
                     'smtp.gmail.com', 
                     'pperez@gmail.com', 'ilovemarialopez')
                     
    """
    msg = MIMEText(mensaje)
    msg.set_type('text/plain')
    msg.set_charset(charset)
    msg_root = None
    if html:
        msg_root = MIMEMultipart('related')
        msg_root.preamble = 'This is a multi-part message in MIME format.'
        if html:
            msg_alt = MIMEMultipart('alternative')
            msg_alt.attach(msg)
            msg_html = MIMEText(html)
            msg_html.set_type('text/html')
            msg_html.set_charset(charset)
            msg_alt.attach(msg_html)
            msg_root.attach(msg_alt)
        msg = msg_root
    if ficheros:
        if not msg_root:
            msg_root = MIMEMultipart()
            msg_root.attach(msg)
            msg = msg_root
        for f in ficheros:
            part = MIMEBase('application', 'octet-stream')
            if isinstance(f, str):
                f = open(f, 'rb')
                f_name = os.path.basename(f)
            else:
                f, f_name = f
            part.set_payload(f.read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % f_name)
            msg.attach(part)

    msg['Subject'] = Header(asunto, charset)
    msg['From'] = '%s <%s>' % (remitente[1], remitente[0])
    nombres = [ '%s <%s>' % (dst[1], dst[0]) for dst in destinatarios ]
    msg['To'] = (';').join(nombres)
    s = smtplib.SMTP(servidor)
    try:
        s.set_debuglevel(False)
        s.ehlo()
        if s.has_extn('STARTTLS'):
            s.starttls()
            s.ehlo()
        s.login(login, password)
        emails_destino = [ dst[0] for dst in destinatarios ]
        resultado = s.sendmail(remitente[0], emails_destino, msg.as_string())
        return resultado
    finally:
        s.quit()

    return


def normalizar_a_html(texto):
    return texto.replace("'", '&#39;').replace('&', '&amp;').replace('#', '&#35;').replace('á', '&aacute;').replace('Á', '&Aacute;').replace('é', '&eacute;').replace('É', '&Eacute;').replace('í', '&iacute;').replace('Í', '&Iacute;').replace('ó', '&oacute;').replace('Ó', '&Oacute;').replace('ú', '&uacute;').replace('Ú', '&Uacute;').replace('ü', '&uuml;').replace('Ü', '&Uuml;').replace('ñ', '&ntilde;').replace('Ñ', '&Ntilde;').replace('<', '&lt;').replace('>', '&gt;').replace('¡', '&iexcl;').replace('?', '&iquest;').replace('"', '&quot;').replace('%', '&#37;')