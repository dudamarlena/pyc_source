# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/gae.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 1376 bytes
from google.appengine.api import mail
__all__ = [
 'AppEngineTransport']
log = __import__('logging').getLogger(__name__)

class AppEngineTransport(object):
    __slots__ = ('ephemeral', )

    def __init__(self, config):
        pass

    def startup(self):
        pass

    def deliver(self, message):
        msg = mail.EmailMessage(sender=(message.author.encode()),
          to=[to.encode() for to in message.to],
          subject=(message.subject),
          body=(message.plain))
        if message.cc:
            msg.cc = [cc.encode() for cc in message.cc]
        if message.bcc:
            msg.bcc = [bcc.encode() for bcc in message.bcc]
        if message.reply:
            msg.reply_to = message.reply.encode()
        if message.rich:
            msg.html = message.rich
        if message.attachments:
            attachments = []
            for attachment in message.attachments:
                attachments.append((
                 attachment['Content-Disposition'].partition(';')[2],
                 attachment.get_payload(True)))

            msg.attachments = attachments
        msg.send()

    def shutdown(self):
        pass