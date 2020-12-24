# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/postmark.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 2905 bytes
import urllib2, json, base64
from marrow.mailer.exc import DeliveryFailedException, MessageFailedException
__all__ = [
 'PostmarkTransport']
log = __import__('logging').getLogger(__name__)

class PostmarkTransport(object):
    __slots__ = ('ephemeral', 'key', 'messages')

    def __init__(self, config):
        self.key = config.get('key')
        self.messages = []

    def _mapmessage(self, message):
        args = dict({'From':message.author.encode(message.encoding), 
         'To':message.to.encode(message.encoding), 
         'Subject':message.subject.encode(message.encoding), 
         'TextBody':message.plain.encode(message.encoding)})
        if message.cc:
            args['Cc'] = message.cc.encode()
        if message.bcc:
            args['Bcc'] = message.bcc.encode(message.encoding)
        if message.reply:
            args['ReplyTo'] = message.reply.encode(message.encoding)
        if message.rich:
            args['HtmlBody'] = message.rich.encode(message.encoding)
        if message.attachments:
            args['Attachments'] = []
            for attachment in message.attachments:
                args['Attachments'].append({'Name':attachment.get_filename(), 
                 'Content':base64.b64encode(attachment.get_payload(decode=True)), 
                 'ContentType':attachment.get_content_type()})

        return args

    def _batchsend(self):
        request = urllib2.Request('https://api.postmarkapp.com/email/batch', json.dumps(self.messages), {'Accept':'application/json', 
         'Content-Type':'application/json', 
         'X-Postmark-Server-Token':self.key})
        try:
            response = urllib2.urlopen(request)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            try:
                raise DeliveryFailedException(e, 'Could not connect to Postmark.')
            finally:
                e = None
                del e

        else:
            respcode = response.getcode()
            if respcode >= 400 and respcode <= 499:
                raise MessageFailedException(response.read())
            else:
                if respcode >= 500:
                    if respcode <= 599:
                        raise DeliveryFailedException(self.messages[0], 'Postmark service unavailable. Just diplaying first message of batch')
        del self.messages[:]

    def startup(self):
        self.messages = []

    def deliver(self, message):
        if len(self.messages) >= 500:
            self._batchsend()
        args = self._mapmessage(message)
        self.messages.append(args)

    def shutdown(self):
        self._batchsend()