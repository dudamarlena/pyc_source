# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/sendgrid.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 3087 bytes
import urllib, urllib2
from marrow.mailer.exc import MailConfigurationException, DeliveryFailedException, MessageFailedException
__all__ = [
 'SendgridTransport']
log = __import__('logging').getLogger(__name__)

class SendgridTransport(object):
    __slots__ = ('ephemeral', 'user', 'key', 'bearer')

    def __init__(self, config):
        self.bearer = False
        if 'user' not in config:
            self.bearer = True
        else:
            self.user = config.get('user')
        self.key = config.get('key')

    def startup(self):
        pass

    def deliver(self, message):
        to = message.to
        if message.cc:
            to.extend(message.cc)
        args = dict({'from':[fromaddr.address.encode(message.encoding) for fromaddr in message.author], 
         'fromname':[fromaddr.name.encode(message.encoding) for fromaddr in message.author], 
         'to':[toaddr.address.encode(message.encoding) for toaddr in to], 
         'toname':[toaddr.name.encode(message.encoding) for toaddr in to], 
         'subject':message.subject.encode(message.encoding), 
         'text':message.plain.encode(message.encoding)})
        if message.bcc:
            args['bcc'] = [bcc.address.encode(message.encoding) for bcc in message.bcc]
        if message.reply:
            args['replyto'] = message.reply.encode(message.encoding)
        if message.rich:
            args['html'] = message.rich.encode(message.encoding)
        if message.attachments:
            raise MailConfigurationException()
        if not self.bearer:
            args['api_user'] = self.user
            args['api_key'] = self.key
        request = urllib2.Request('https://sendgrid.com/api/mail.send.json', urllib.urlencode(args, True))
        if self.bearer:
            request.add_header('Authorization', 'Bearer %s' % self.key)
        try:
            response = urllib2.urlopen(request)
        except (urllib2.HTTPError, urllib2.URLError):
            raise DeliveryFailedException(message, 'Could not connect to Sendgrid.')
        else:
            respcode = response.getcode()
            if respcode >= 400 and respcode <= 499:
                raise MessageFailedException(response.read())
            else:
                if respcode >= 500:
                    if respcode <= 599:
                        raise DeliveryFailedException(message, 'Sendgrid service unavailable.')
                response.close()

    def shutdown(self):
        pass