# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_consumer.py
# Compiled at: 2019-01-03 01:37:10
import mock
from .utils import ModelsBaseTest, ConfigPatcher
import odcs.server.consumer
from odcs.server import db
from odcs.server.consumer import ODCSConsumer
from odcs.server.models import Compose

class ConsumerBaseTest(ModelsBaseTest):

    def _create_consumer(self):
        hub = mock.MagicMock()
        hub.config = {}
        hub.config['odcsconsumer'] = True
        hub.config['validate_signatures'] = False
        return ODCSConsumer(hub)

    def _compose_state_change_msg(self, id=1, state=None):
        msg = {'body': {'compose': {'id': id, 
                                'state_name': state or 'wait'}}, 
           'msg_id': '2017-7afcb214-cf82-4130-92d2-22f45cf59cf7', 
           'topic': 'VirtualTopic.eng.odcs.state.change'}
        return msg

    def _internal_clean_composes_msg(self):
        msg = {'body': {'msg_id': '2017-7afcb214-cf82-4130-92d2-22f45cf59cf7', 
                    'topic': 'VirtualTopic.eng.odcs.internal.cleanup', 
                    'signature': 'qRZ6oXBpKD/q8BTjBNa4MREkAPxT+KzI8Oret+TSKazGq/6gk0uuprdFpkfBXLR5dd4XDoh3NQWp\nyC74VYTDVqJR7IsEaqHtrv01x1qoguU/IRWnzrkGwqXm+Es4W0QZjHisBIRRZ4ywYBG+DtWuskvy\n6/5Mc3dXaUBcm5TnT0c=\n'}}
        msg = {'body': {}, 'msg_id': '2017-7afcb214-cf82-4130-92d2-22f45cf59cf7', 
           'topic': 'VirtualTopic.eng.odcs.internal.cleanup'}
        return msg


class ConsumerTest(ConsumerBaseTest):

    def setUp(self):
        super(ConsumerTest, self).setUp()
        self.config_patcher = ConfigPatcher(odcs.server.consumer.conf)
        self.config_patcher.patch('messaging_topic', 'VirtualTopic.eng.odcs.state.change')
        self.config_patcher.patch('internal_messaging_topic', 'VirtualTopic.eng.odcs.internal.cleanup')
        self.config_patcher.start()
        self.consumer = self._create_consumer()
        self.compose = Compose.create(db.session, 'me', 1, 'foo-1', 1, 3600)
        db.session.add(self.compose)
        db.session.commit()

    def tearDown(self):
        super(ConsumerTest, self).tearDown()
        self.config_patcher.stop()

    @mock.patch('odcs.server.backend.ComposerThread.generate_new_compose')
    def test_consumer_processing_state_change(self, generate_new_compose):
        msg = self._compose_state_change_msg()
        self.consumer.consume(msg)
        generate_new_compose.assert_called_once_with(self.compose)

    @mock.patch('odcs.server.backend.ComposerThread.generate_new_compose')
    def test_consumer_processing_state_change_unknown_id(self, generate_new_compose):
        msg = self._compose_state_change_msg(-1)
        self.consumer.consume(msg)
        generate_new_compose.assert_not_called()

    @mock.patch('odcs.server.backend.ComposerThread.generate_new_compose')
    def test_consumer_processing_state_change_non_wait_state(self, generate_new_compose):
        for state in ['generating', 'expired', 'removed', 'done']:
            msg = self._compose_state_change_msg(1, state)
            self.consumer.consume(msg)
            generate_new_compose.assert_not_called()

    @mock.patch('odcs.server.backend.RemoveExpiredComposesThread.do_work')
    @mock.patch('odcs.server.backend.ComposerThread.pickup_waiting_composes')
    @mock.patch('odcs.server.backend.ComposerThread.fail_lost_generating_composes')
    def test_consumer_processing_internal_cleaup(self, fail_generating_lost_composes, pickup_waiting_composes, remove_expired):
        msg = self._internal_clean_composes_msg()
        self.consumer.consume(msg)
        remove_expired.assert_called_once()
        pickup_waiting_composes.assert_called_once()
        fail_generating_lost_composes.assert_called_once()