# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/server/tests/test_webapp.py
# Compiled at: 2016-11-12 07:38:04
import json, os, uuid, unittest, tempfile, shutil
from datetime import datetime
import zmq.green, beeswarm
from beeswarm.server.misc.config_actor import ConfigActor
import beeswarm.server.db.database_setup as database
from beeswarm.server.db.entities import Client, Honeypot, Session, BaitSession, Authentication, Transcript, BaitUser
from beeswarm.server.webapp import app
from beeswarm.server.db.database_actor import DatabaseActor

class WebAppTests(unittest.TestCase):

    def setUp(self):
        self.password = 'testpassword'
        app.ensure_admin_password(True, password=self.password)
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.work_dir = tempfile.mkdtemp()
        beeswarm.shared.zmq_context = zmq.Context()
        fd, self.db_file = tempfile.mkstemp()
        os.close(fd)
        connection_string = ('sqlite:///{0}').format(self.db_file)
        os.remove(self.db_file)
        database.setup_db(connection_string)
        self.config_actor = ConfigActor(os.path.join(os.path.dirname(__file__), 'beeswarmcfg.json.test'), self.work_dir)
        self.config_actor.start()
        session = database.get_session()
        session.add_all([Client(), Honeypot()])
        session.commit()
        self.database_actor = DatabaseActor(999, delay_seconds=2)
        self.database_actor.start()
        self.app = app.app.test_client()
        app.connect_sockets()

    def tearDown(self):
        self.database_actor.stop()
        self.database_actor = None
        self.config_actor.stop()
        self.config_actor = None
        shutil.rmtree(self.work_dir)
        if os.path.isfile(self.db_file):
            os.remove(self.db_file)
        return

    def test_data_sessions_all(self):
        """ Tests if all sessions are returned properly"""
        self.login('test', self.password)
        self.populate_sessions()
        resp = self.app.get('/data/sessions/all')
        table_data = json.loads(resp.data)
        self.assertEquals(len(table_data), 4)
        self.logout()

    def test_data_sessions_honeybees(self):
        """ Tests if bait_sessions are returned properly """
        self.login('test', self.password)
        self.populate_honeybees()
        resp = self.app.get('/data/sessions/bait_sessions')
        table_data = json.loads(resp.data)
        self.assertEquals(len(table_data), 3)
        self.logout()

    def test_data_sessions_attacks(self):
        """ Tests if attacks are returned properly """
        self.login('test', self.password)
        self.populate_sessions()
        resp = self.app.get('/data/sessions/attacks')
        table_data = json.loads(resp.data)
        self.assertEquals(len(table_data), 4)
        self.logout()

    def test_data_transcripts(self):
        """ Tests that if given a session ID we can extract the relevant transcripts"""
        db_session = database.get_session()
        self.login('test', self.password)
        session_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        db_session.add(Transcript(timestamp=timestamp, direction='outgoing', data='whoami', session_id=session_id))
        db_session.add(Transcript(timestamp=timestamp, direction='outgoing', data='root\r\n', session_id=session_id))
        db_session.commit()
        resp = self.app.get(('/data/session/{0}/transcript').format(session_id))
        data = json.loads(resp.data)
        string_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        expected_result = [{'direction': 'outgoing', 'data': 'whoami', 'time': ('{0}').format(string_timestamp)}, {'direction': 'outgoing', 'data': 'root\r\n', 'time': ('{0}').format(string_timestamp)}]
        self.assertDictEqual(sorted(data)[0], sorted(expected_result)[0])

    def test_login_logout(self):
        """ Tests basic login/logout """
        self.login('admin', self.password)
        self.logout()

    def test_get_baitusers(self):
        """ Tests GET on the '/ws/bait_users' route."""
        self.login('admin', self.password)
        self.populate_bait_users()
        resp = self.app.get('/ws/bait_users')
        table_data = json.loads(resp.data)
        self.assertEquals(len(table_data), 2)
        self.logout()

    def test_add_baituser(self):
        """ Tests POST on the '/ws/bait_users/add' route."""
        self.login('admin', self.password)
        data = [{'username': 'userA', 'password': 'passA'}, {'username': 'userB', 'password': 'passB'}, {'username': 'userC', 'password': 'passC'}]
        self.app.post('/ws/bait_users/add', data=json.dumps(data), follow_redirects=True)
        resp = self.app.get('/ws/bait_users')
        bait_users = json.loads(resp.data)
        self.assertEquals(len(bait_users), 25)
        self.logout()

    def populate_clients(self):
        """ Populates the database with 4 clients """
        db_session = database.get_session()
        self.clients = []
        for i in xrange(4):
            f = Client()
            self.clients.append(f.id)
            db_session.add(f)

        db_session.commit()

    def populate_honeypots(self):
        """ Populates the database with 4 honeypots """
        db_session = database.get_session()
        self.honeypots = []
        for i in xrange(4):
            h = Honeypot()
            self.honeypots.append(h.id)
            db_session.add(h)

        db_session.commit()

    def populate_bait_users(self):
        """ Populates the database with 2 bait users """
        db_session = database.get_session()
        db_session.query(BaitUser).delete()
        self.clients = []
        for c in [('userA', 'passA'), ('userB', 'passB')]:
            bait_user = BaitUser(username=c[0], password=c[1])
            db_session.add(bait_user)

        db_session.commit()

    def login(self, username, password):
        """ Logs into the web-app """
        data = {'username': username, 
           'password': password}
        return self.app.post('/login', data=data, follow_redirects=True)

    def populate_honeybees(self):
        """ Populates the database with 3 Honeybees """
        db_session = database.get_session()
        for i in xrange(3):
            h = BaitSession(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), received=datetime.utcnow(), protocol='ssh', destination_ip='1.2.3.4', destination_port=1234, source_ip='4.3.2.1', source_port=4321, did_connect=True, did_login=False, did_complete=True)
            a = Authentication(id=str(uuid.uuid4()), username='uuu', password='vvvv', successful=False, timestamp=datetime.utcnow())
            h.authentication.append(a)
            db_session.add(h)

        db_session.commit()

    def populate_sessions(self):
        """ Populates the database with 3 Sessions """
        db_session = database.get_session()
        for i in xrange(4):
            s = Session(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), received=datetime.utcnow(), protocol='telnet', destination_ip='123.123.123.123', destination_port=1234, source_ip='12.12.12.12', source_port=12345, classification_id='asd')
            a = Authentication(id=str(uuid.uuid4()), username='aaa', password='bbb', successful=False, timestamp=datetime.utcnow())
            s.authentication.append(a)
            db_session.add(s)

        db_session.commit()

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


if __name__ == '__main__':
    unittest.main()