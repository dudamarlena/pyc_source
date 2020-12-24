# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/messaging.py
# Compiled at: 2017-10-30 03:09:30
import json
from logging import getLogger
from odcs.server import conf
log = getLogger(__name__)
__all__ = ('publish', )

def publish(msgs):
    """Start to send messages to message broker"""
    backend = _get_messaging_backend()
    if backend is not None:
        backend(msgs)
    return


def _umb_send_msg(msgs):
    """Send message to Unified Message Bus"""
    import proton
    from rhmsg.activemq.producer import AMQProducer
    config = {'urls': conf.messaging_broker_urls, 
       'certificate': conf.messaging_cert_file, 
       'private_key': conf.messaging_key_file, 
       'trusted_certificates': conf.messaging_ca_cert}
    with AMQProducer(**config) as (producer):
        producer.through_topic(conf.messaging_topic)
        for msg in msgs:
            outgoing_msg = proton.Message()
            outgoing_msg.body = json.dumps(msg)
            producer.send(outgoing_msg)


def _fedmsg_send_msg(msgs):
    """Send message to fedmsg!  Yay!"""
    import fedmsg
    for msg in msgs:
        event = msg.get('event', 'event')
        topic = 'compose.%s' % event
        fedmsg.publish(topic=topic, msg=msg)


def _get_messaging_backend():
    if conf.messaging_backend == 'rhmsg':
        return _umb_send_msg
    else:
        if conf.messaging_backend == 'fedmsg':
            return _fedmsg_send_msg
        if conf.messaging_backend:
            raise ValueError(('Unknown messaging backend {0}').format(conf.messaging_backend))
        else:
            return
        return