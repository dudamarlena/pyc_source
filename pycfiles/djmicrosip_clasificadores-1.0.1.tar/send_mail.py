# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_clasificadores\djmicrosip_clasificadores\send_mail.py
# Compiled at: 2020-04-11 02:25:26
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

def send_mail_contrasena(host, port, mail, password, destinatarios, asunto, mensaje, archivo, nombre):
    if mail and port and host and password:
        try:
            msg = MIMEMultipart()
            message = mensaje
            if archivo:
                fo = open(archivo, 'rb')
                pdfAttachment = MIMEApplication(fo.read(), _subtype='pdf')
                fo.close()
                pdfAttachment.add_header('Content-Disposition', 'attachment', filename=nombre)
                msg.attach(pdfAttachment)
            msg.attach(MIMEText(mensaje, 'html', _charset='UTF-8'))
            password = password
            msg['Subject'] = asunto
            server = smtplib.SMTP(host, int(port))
            server.ehlo()
            server.starttls()
            server.login(mail, password)
            server.sendmail(mail, destinatarios, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print e
            return False