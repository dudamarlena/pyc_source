# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neptuno/enviaremail.py
# Compiled at: 2012-10-29 11:33:17
from sendmail import send_mail

def enviar_email(remitente, destinatarios, asunto, mensaje, servidor, login, password, ficheros=[], html='', cc=[], bcc=[], charset='iso-8859-1'):
    send_mail(remitente, destinatarios, asunto, mensaje, servidor, login, password, files=ficheros, html=html, cc=cc, bcc=bcc, charset=charset)


def normalizar_a_html(texto):
    return texto.replace("'", '&#39;').replace('&', '&amp;').replace('#', '&#35;').replace('á', '&aacute;').replace('Á', '&Aacute;').replace('é', '&eacute;').replace('É', '&Eacute;').replace('í', '&iacute;').replace('Í', '&Iacute;').replace('ó', '&oacute;').replace('Ó', '&Oacute;').replace('ú', '&uacute;').replace('Ú', '&Uacute;').replace('ü', '&uuml;').replace('Ü', '&Uuml;').replace('ñ', '&ntilde;').replace('Ñ', '&Ntilde;').replace('<', '&lt;').replace('>', '&gt;').replace('¡', '&iexcl;').replace('?', '&iquest;').replace('"', '&quot;').replace('%', '&#37;')