# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/monobot/sync/tickettest/simpletickets/simpleemail/email_helper.py
# Compiled at: 2016-09-18 17:33:29
import os
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class EmailManager(EmailMultiAlternatives):

    def __init__(self, context, subject='', body='', from_email=settings.EMAIL_HOST_USER, to=None, bcc=None, connection=None, attachments=None, headers=None, alternatives=None, cc=None, reply_to=None):
        txt_content = render_to_string(body, context)
        self.reply_to = reply_to or settings.EMAIL_HOST_USER
        super(EmailMultiAlternatives, self).__init__(subject, txt_content, from_email, to, bcc, connection, attachments, headers, cc, reply_to)
        self.alternatives = alternatives or []
        self.context = context

    def attachImages(self, imagenames):
        for image in imagenames:
            fp = open(os.path.join(settings.MEDIA_ROOT, image), 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header('Content-ID', ('<{}>').format(image))
            self.attach(msg_img)

    def attachHtml(self, template, context):
        html_content = render_to_string(template, context)
        self.attach_alternative(html_content, 'text/html')
        self.mixed_subtype = 'related'