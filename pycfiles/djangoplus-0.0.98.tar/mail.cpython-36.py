# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/utils/mail.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 1678 bytes
import json
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend
DEBUG_EMAIL_FILE_PATH = '/tmp/{}.json'.format(settings.PROJECT_NAME)

class EmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        messagens = []
        for message in email_messages:
            messagens.append(dict(from_email=(message.from_email), to=(', '.join(message.to)), message=(message.body)))

        open(DEBUG_EMAIL_FILE_PATH, 'w').write(json.dumps(messagens))
        return len(messagens)


def send_mail(subject, message, to, reply_to=None, actions=()):
    from djangoplus.admin.models import Settings
    url = 'http://{}'.format(settings.HOST_NAME or 'localhost:8000')
    app_settings = Settings.default()
    context = dict()
    context['subject'] = subject
    context['project_url'] = url
    context['project_name'] = app_settings.initials
    context['project_description'] = app_settings.name
    context['project_logo'] = app_settings.logo and '{}/media/{}'.format(url, app_settings.logo) or '{}/static/images/mail.png'.format(url)
    context['actions'] = actions
    context['message'] = message.replace('\n', '<br>').replace('\t', '&nbsp;' * 4)
    reply_to = reply_to and [reply_to] or None
    from_email = 'Não-Responder <{}>'.format(settings.SERVER_EMAIL)
    html = loader.render_to_string('mail.html', context)
    email = EmailMultiAlternatives(subject, 'Mensagem em anexo.', from_email, [to], reply_to=reply_to)
    email.attach_alternative(html, 'text/html')
    return email.send()