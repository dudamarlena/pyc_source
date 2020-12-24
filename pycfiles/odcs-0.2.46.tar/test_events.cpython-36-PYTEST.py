# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_events.py
# Compiled at: 2017-11-24 05:51:09
# Size of source mod 2**32: 5511 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, json, six, unittest
from mock import patch
from odcs.server import conf
from odcs.server import db
from odcs.server.models import Compose
from odcs.server.pungi import PungiSourceType
from odcs.common.types import COMPOSE_RESULTS
from odcs.common.types import COMPOSE_STATES
from .utils import ModelsBaseTest
try:
    import rhmsg
except ImportError:
    rhmsg = None

try:
    import fedmsg
except ImportError:
    fedmsg = None

@unittest.skipUnless(rhmsg, 'rhmsg is required to run this test case.')
@unittest.skipIf(six.PY3, 'rhmsg has no Python 3 package so far.')
class TestRHMsgSendMessageWhenComposeIsCreated(ModelsBaseTest):
    __doc__ = 'Test send message when compose is created'
    disable_event_handlers = False

    def setUp(self):
        super(TestRHMsgSendMessageWhenComposeIsCreated, self).setUp()
        self.mock_lock = patch('threading.Lock')
        self.mock_lock.start()

    def tearDown(self):
        self.mock_lock.stop()

    def setup_composes(self):
        self.compose = Compose.create(db.session, 'mine', PungiSourceType.KOJI_TAG, 'f25', COMPOSE_RESULTS['repository'], 3600)
        db.session.commit()

    @patch.object(conf, 'messaging_backend', new='rhmsg')
    @patch('rhmsg.activemq.producer.AMQProducer')
    @patch('proton.Message')
    def assert_messaging(self, compose, Message, AMQProducer):
        db.session.commit()
        self.assertEqual(json.dumps({'event':'state-changed',  'compose':compose.json()}), Message.return_value.body)
        producer_send = AMQProducer.return_value.__enter__.return_value.send
        producer_send.assert_called_once_with(Message.return_value)

    def test_send_message(self):
        compose = Compose.create(db.session, 'me', PungiSourceType.MODULE, 'testmodule-master', COMPOSE_RESULTS['repository'], 3600)
        self.assert_messaging(compose)

    def test_message_on_state_change(self):
        compose = db.session.query(Compose).filter(Compose.id == self.compose.id).all()[0]
        compose.state = COMPOSE_STATES['generating']
        self.assert_messaging(compose)


@unittest.skipUnless(fedmsg, 'fedmsg is required to run this test case.')
class TestFedMsgSendMessageWhenComposeIsCreated(ModelsBaseTest):
    __doc__ = 'Test send message when compose is created'
    disable_event_handlers = False

    def setUp(self):
        super(TestFedMsgSendMessageWhenComposeIsCreated, self).setUp()
        self.mock_lock = patch('threading.Lock')
        self.mock_lock.start()

    def tearDown(self):
        self.mock_lock.stop()

    def setup_composes(self):
        self.compose = Compose.create(db.session, 'mine', PungiSourceType.KOJI_TAG, 'f25', COMPOSE_RESULTS['repository'], 3600)
        db.session.commit()

    @patch.object(conf, 'messaging_backend', new='fedmsg')
    @patch('fedmsg.publish')
    def assert_messaging(self, compose, publish):
        db.session.commit()
        publish.assert_called_once_with(topic='compose.state-changed',
          msg={'event':'state-changed', 
         'compose':compose.json()})

    def test_send_message(self):
        compose = Compose.create(db.session, 'me', PungiSourceType.MODULE, 'testmodule-master', COMPOSE_RESULTS['repository'], 3600)
        self.assert_messaging(compose)

    def test_message_on_state_change(self):
        compose = db.session.query(Compose).filter(Compose.id == self.compose.id).all()[0]
        compose.state = COMPOSE_STATES['generating']
        self.assert_messaging(compose)