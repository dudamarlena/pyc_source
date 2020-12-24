# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/server/tests/test_database_actor.py
# Compiled at: 2016-11-12 07:38:04
import unittest, uuid
from datetime import datetime
import json, tempfile, os, zmq.green, gevent, beeswarm.shared
from beeswarm.server.db import database_setup
from beeswarm.server.db.entities import Honeypot, Client
from beeswarm.server.db.entities import Session
from beeswarm.drones.honeypot.models.session import Session as HoneypotSession
from beeswarm.shared.socket_enum import SocketNames
from beeswarm.shared.message_enum import Messages
from beeswarm.server.db.database_actor import DatabaseActor
from beeswarm.drones.client.models.session import BaitSession
from beeswarm.server.misc.config_actor import ConfigActor
from beeswarm.shared.helpers import send_zmq_request_socket

class ClassifierTests(unittest.TestCase):

    def setUp(self):
        beeswarm.shared.zmq_context = zmq.Context()
        fd, self.db_file = tempfile.mkstemp()
        os.close(fd)
        connection_string = ('sqlite:///{0}').format(self.db_file)
        os.remove(self.db_file)
        database_setup.setup_db(connection_string)

    def tearDown(self):
        if os.path.isfile(self.db_file):
            os.remove(self.db_file)

    def test_matching_quick_succession(self):
        """
        Tests that attack sessions coming in quick succession are classified correctly.
        This test relates to issue #218
        """
        honeypot_id = 1
        honeypot = Honeypot(id=honeypot_id)
        db_session = database_setup.get_session()
        db_session.add(honeypot)
        db_session.commit()
        drone_data_socket = beeswarm.shared.zmq_context.socket(zmq.PUB)
        drone_data_socket.bind(SocketNames.DRONE_DATA.value)
        database_actor = DatabaseActor(999, delay_seconds=2)
        database_actor.start()
        gevent.sleep(1)
        for x in xrange(0, 100):
            honeypot_session = HoneypotSession(source_ip='192.168.100.22', source_port=52311, protocol='pop3', users={}, destination_port=110)
            honeypot_session.add_auth_attempt('plaintext', True, username='james', password='bond')
            honeypot_session.honeypot_id = honeypot_id
            drone_data_socket.send(('{0} {1} {2}').format(Messages.SESSION_HONEYPOT.value, honeypot_id, json.dumps(honeypot_session.to_dict(), default=json_default, ensure_ascii=False)))

        gevent.sleep(1)
        database_actor_request_socket = beeswarm.shared.zmq_context.socket(zmq.REQ)
        database_actor_request_socket.connect(SocketNames.DATABASE_REQUESTS.value)
        sessions = send_zmq_request_socket(database_actor_request_socket, ('{0}').format(Messages.GET_SESSIONS_ALL.value))
        for session in sessions:
            self.assertEqual(session['classification'], 'Bruteforce')

        self.assertEqual(len(sessions), 100)

    def test_bait_classification_honeypot_first(self):
        """
        Tests that bait sessions are paired correctly with their honeypot counter parts when honeypot message arrives
        first.
        """
        self.populate_bait(True)
        db_session = database_setup.get_session()
        sessions = db_session.query(Session).all()
        for session in sessions:
            self.assertEqual(session.classification_id, 'bait_session')

        self.assertEqual(len(sessions), 1)

    def test_bait_classification_client_first(self):
        """
        Tests that bait sessions are paired correctly with their honeypot counter parts when client message arrives
        first.
        """
        self.populate_bait(False)
        db_session = database_setup.get_session()
        sessions = db_session.query(Session).all()
        for session in sessions:
            self.assertEqual(session.classification_id, 'bait_session')

        self.assertEqual(len(sessions), 1)

    def populate_bait(self, honeypot_first):
        honeypot_id = 1
        client_id = 2
        honeypot = Honeypot(id=honeypot_id)
        client = Client(id=client_id)
        db_session = database_setup.get_session()
        db_session.add(honeypot)
        db_session.add(client)
        db_session.commit()
        drone_data_socket = beeswarm.shared.zmq_context.socket(zmq.PUB)
        drone_data_socket.bind(SocketNames.DRONE_DATA.value)
        fd, config_file = tempfile.mkstemp()
        os.close(fd)
        os.remove(config_file)
        config_actor = ConfigActor(config_file, '')
        config_actor.start()
        database_actor = DatabaseActor(999, delay_seconds=2)
        database_actor.start()
        gevent.sleep(1)
        BaitSession.client_id = client_id
        honeypot_session = HoneypotSession(source_ip='192.168.100.22', source_port=52311, protocol='pop3', users={}, destination_port=110)
        honeypot_session.add_auth_attempt('plaintext', True, username='james', password='bond')
        honeypot_session.honeypot_id = honeypot_id
        bait_session = BaitSession('pop3', '1234', 110, honeypot_id)
        bait_session.add_auth_attempt('plaintext', True, username='james', password='bond')
        bait_session.honeypot_id = honeypot_id
        bait_session.did_connect = bait_session.did_login = bait_session.alldone = bait_session.did_complete = True
        if honeypot_first:
            drone_data_socket.send(('{0} {1} {2}').format(Messages.SESSION_HONEYPOT.value, honeypot_id, json.dumps(honeypot_session.to_dict(), default=json_default, ensure_ascii=False)))
            drone_data_socket.send(('{0} {1} {2}').format(Messages.SESSION_CLIENT.value, client_id, json.dumps(bait_session.to_dict(), default=json_default, ensure_ascii=False)))
        else:
            drone_data_socket.send(('{0} {1} {2}').format(Messages.SESSION_CLIENT.value, client_id, json.dumps(bait_session.to_dict(), default=json_default, ensure_ascii=False)))
            drone_data_socket.send(('{0} {1} {2}').format(Messages.SESSION_HONEYPOT.value, honeypot_id, json.dumps(honeypot_session.to_dict(), default=json_default, ensure_ascii=False)))
        gevent.sleep(2)
        config_actor.stop()
        database_actor.stop()
        if os.path.isfile(config_file):
            os.remove(config_file)


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        if isinstance(obj, uuid.UUID):
            return str(obj)
        else:
            return

        return