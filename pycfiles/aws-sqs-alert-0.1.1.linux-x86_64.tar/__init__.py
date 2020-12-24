# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/AWSSQSAlert/__init__.py
# Compiled at: 2014-02-11 00:57:28
__version__ = '0.1.1'
import time, os, sys, json, logging, boto, boto.sqs
from boto.sqs.message import RawMessage

class AWSSQSAlert:
    """
    Amazon Web Services AutoScale and Cloudwatch Alerting via SQS
    """

    def __init__(self, config=None, logger=None):
        """
        Init
        """
        self.config = config
        self.logger = logger
        self.sqs = None
        self.region = None
        self.queue = None
        self.handlers = []
        if 'AWS_ACCESS' not in self.config:
            self.config['AWS_ACCESS'] = None
        if 'AWS_SECRET' not in self.config:
            self.config['AWS_SECRET'] = None
        sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/handlers')
        sys.path.append('/etc/aws-sqs-alert/handlers')
        autoscale_alert_handlers = self.config['active_handlers']
        handlers = []
        for r in boto.sqs.regions():
            if r.name == self.config['region']:
                self.region = r
                break

        self._connect()
        for h in autoscale_alert_handlers:
            handle = __import__(h, globals(), locals(), ['*'])
            cls = getattr(handle, h)
            self.handlers.append(cls)
            self.logger.debug('Loaded Handler: %s' % h, extra=dict(program='autoscale-alert', handler=h))

        return

    def _connect(self):
        if self.sqs is None:
            self.sqs = boto.connect_sqs(aws_access_key_id=self.config['AWS_ACCESS'], aws_secret_access_key=self.config['AWS_SECRET'], region=self.region)
            self.queue = self.sqs.get_queue(self.config['queue'])
            if self.queue is not None:
                self.queue.set_message_class(RawMessage)
            else:
                self.logger.critical('Could not open Queue: %s' % self.config['queue'], extra=dict(program='autoscale-alert', queue=self.config['queue']))
                raise Exception('Could not open Queue: %s' % self.config['queue'])
        return

    def get_messages(self):
        self._connect()
        found_handler = False
        self.logger.debug('Attempting to get Queue Messages', extra=dict(program='autoscale-alert'))
        messages = self.queue.get_messages(num_messages=self.config['num_messages'])
        for msg in messages:
            m = json.loads(msg.get_body())
            e = json.loads(m['Message'])
            if 'Event' in e:
                msgtype = 'Event'
                msgid = e['Event']
            else:
                if 'AlarmName' in e:
                    msgtype = 'Alarm'
                    msgid = e['AlarmName']
                else:
                    msgtype = 'Unknown'
                    msgid = 'Unknown'
                self.logger.debug('Receiving Message.', extra=dict(program='autoscale-alert', msgtype=msgtype, msgid=msgid, queuemsg=e))
                for handler in self.handlers:
                    h = handler()
                    if h.watches(msgtype, msgid):
                        found_handler = True
                        self.logger.debug('Routing Message: %s to %s' % (msgid, h.__class__.__name__), extra=dict(program='autoscale-alert', msgtype=msgtype, msgid=msgid, queuemsg=e))
                        h.alert(self.config, msgtype, e)

            if found_handler == False:
                self.logger.error('Cound not find handler for message: %s of type %s' % (msgid, msgtype), extra=dict(program='autoscale-alert', msgtype=msgtype, msgid=msgid, queuemsg=e))
            if self.config['delete']:
                msg.delete()