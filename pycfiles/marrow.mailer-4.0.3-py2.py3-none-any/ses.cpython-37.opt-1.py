# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/ses.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 1800 bytes
try:
    import boto.ses
    from boto.ses import SESConnection
except ImportError:
    raise ImportError('You must install the boto package to deliver mail via Amazon SES.')

__all__ = [
 'AmazonTransport']
log = __import__('logging').getLogger(__name__)

class AmazonTransport(object):
    __slots__ = ('ephemeral', 'config', 'region', 'connection')

    def __init__(self, config):
        config['aws_access_key_id'] = config.pop('id')
        config['aws_secret_access_key'] = config.pop('key')
        self.region = config.pop('region', 'us-east-1')
        config.pop('use')
        self.config = config
        self.connection = None

    def startup(self):
        self.connection = (boto.ses.connect_to_region)((self.region), **self.config)

    def deliver(self, message):
        try:
            destinations = [r.encode(encoding='utf-8') for r in message.recipients]
            response = self.connection.send_raw_email(str(message), message.author.encode(), destinations)
            return (
             response['SendRawEmailResponse']['SendRawEmailResult']['MessageId'],
             response['SendRawEmailResponse']['ResponseMetadata']['RequestId'])
        except SESConnection.ResponseError:
            raise

    def shutdown(self):
        if self.connection:
            self.connection.close()
        self.connection = None