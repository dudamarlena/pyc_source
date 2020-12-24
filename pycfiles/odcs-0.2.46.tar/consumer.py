# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/consumer.py
# Compiled at: 2019-01-03 01:37:10
import fedmsg.consumers
from odcs.server import log, conf, db
from odcs.server.backend import ComposerThread, RemoveExpiredComposesThread
from odcs.server.models import Compose
from odcs.server.utils import retry

class ODCSConsumer(fedmsg.consumers.FedmsgConsumer):
    """
    This is triggered by running fedmsg-hub. This class is responsible for
    ingesting and processing messages from the message bus.
    """
    config_key = 'odcsconsumer'

    def __init__(self, hub):
        messaging_topic = conf.messaging_topic_prefix + conf.messaging_topic
        internal_messaging_topic = conf.messaging_topic_prefix + conf.internal_messaging_topic
        self.topic = [messaging_topic, internal_messaging_topic]
        log.debug(('Setting topics: {}').format((', ').join(self.topic)))
        super(ODCSConsumer, self).__init__(hub)
        self.composer = ComposerThread()
        self.remove_expired_compose_thread = RemoveExpiredComposesThread()
        self.stop_condition = hub.config.get('odcs.stop_condition')
        initial_messages = hub.config.get('odcs.initial_messages', [])
        for msg in initial_messages:
            self.incoming.put(msg)

    def shutdown(self):
        log.info('Scheduling shutdown.')
        from moksha.hub.reactor import reactor
        reactor.callFromThread(self.hub.stop)
        reactor.callFromThread(reactor.stop)

    def validate(self, message):
        if conf.messaging_backend == 'fedmsg':
            super(ODCSConsumer, self).validate(message)

    def consume(self, message):
        topic, inner_msg = self.parse_message(message)
        try:
            self.process_message(topic, inner_msg)
        except Exception:
            log.exception(('Failed while handling {0!r}').format(message))

        db.session.commit()
        if self.stop_condition and self.stop_condition(message):
            self.shutdown()

    def parse_message(self, message):
        """
        Returns the topic of message and inner message which we actually care
        about.
        """
        if 'topic' not in message:
            raise ValueError(('The messaging format "{}" is not supported').format(conf.messaging_backend))
        inner_msg = message.get('body')
        inner_msg = inner_msg.get('msg', inner_msg)
        return (message['topic'], inner_msg)

    @retry(wait_on=RuntimeError)
    def get_odcs_compose(self, compose_id):
        """
        Gets the compose from ODCS DB.
        """
        compose = Compose.query.filter(Compose.id == compose_id).first()
        if not compose:
            raise RuntimeError('No compose with id %d in ODCS DB.' % compose_id)
        return compose

    def process_message(self, topic, msg):
        """
        Handles the parsed message `msg` of topic `topic`.
        """
        log.debug('Received: %r', msg)
        if topic.endswith(conf.messaging_topic):
            compose_state = msg['compose']['state_name']
            if compose_state != 'wait':
                return
            compose_id = msg['compose']['id']
            compose = self.get_odcs_compose(compose_id)
            self.composer.generate_new_compose(compose)
        elif topic.endswith(conf.internal_messaging_topic):
            self.remove_expired_compose_thread.do_work()
            self.composer.pickup_waiting_composes()
            self.composer.fail_lost_generating_composes()