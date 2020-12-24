# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/filebeat_delegate/publisher.py
# Compiled at: 2019-06-16 05:47:41
__author__ = 'Alexander.Li'
import json, boto3, logging, requests
from utilities import SingletonMixin
from errorbuster import formatError

class MailgunPublisher(SingletonMixin):

    def __init__(self):
        self.url = None
        self.key = None
        self.configure = None
        return

    def init_publisher(self, configure):
        self.url = ('https://api.mailgun.net/v3/{0.mg_domain}/messages').format(configure)
        self.key = configure.mg_key
        self.configure = configure

    def sendMessage(self, message):
        r = requests.post(self.url, auth=('api', self.key), data={'from': (' <mailgun@{0.mg_domain}>').format(self.configure), 'to': [
                self.configure.mg_target, 'YOU@YOUR_DOMAIN_NAME'], 
           'subject': 'error report', 
           'text': message})
        logging.info(r.text)


class SNSPublisher(SingletonMixin):

    def __init__(self):
        self.sns = None
        self.topic = None
        return

    def init_publisher(self, configure):
        self.sns = boto3.resource('sns', region_name=configure.aws_region, aws_access_key_id=configure.aws_key, aws_secret_access_key=configure.aws_secret)
        self.topic = self.sns.Topic(configure.aws_topic)

    def sendMessage(self, message):
        payloads = json.dumps({'default': message})
        try:
            response = self.topic.publish(Message=payloads, MessageStructure='json')
            logging.info('%s published with response %s', message, response)
        except Exception as e:
            logging.error(formatError(e))