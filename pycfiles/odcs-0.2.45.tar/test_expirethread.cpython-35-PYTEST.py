# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_expirethread.py
# Compiled at: 2017-08-31 11:17:14
# Size of source mod 2**32: 3591 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from odcs.server import db
from odcs.server.models import Compose
from odcs.common.types import COMPOSE_STATES, COMPOSE_RESULTS
from odcs.server.backend import ExpireThread
from odcs.server.pungi import PungiSourceType
from datetime import datetime, timedelta
from utils import ModelsBaseTest

class TestExpireThread(ModelsBaseTest):
    maxDiff = None

    def setUp(self):
        super(TestExpireThread, self).setUp()
        compose = Compose.create(db.session, 'unknown', PungiSourceType.MODULE, 'testmodule-master', COMPOSE_RESULTS['repository'], 60)
        db.session.add(compose)
        db.session.commit()
        self.expire = ExpireThread()

    def test_no_expire(self):
        """
        Test that we do not expire composes on non-done state.
        """
        c = db.session.query(Compose).filter(Compose.id == 1).one()
        c.time_to_expire = datetime.utcnow() - timedelta(seconds=-120)
        for name, state in COMPOSE_STATES.items():
            if name == 'done':
                pass
            else:
                c.state = state
                db.session.add(c)
                db.session.commit()
                self.expire.do_work()
                db.session.expunge_all()
                c = db.session.query(Compose).filter(Compose.id == 1).one()
                self.assertEqual(c.state, state)

    def test_expire_done(self):
        """
        Test that we do expire compose in done state.
        """
        c = db.session.query(Compose).filter(Compose.id == 1).one()
        c.time_to_expire = datetime.utcnow() - timedelta(seconds=120)
        c.state = COMPOSE_STATES['done']
        db.session.add(c)
        db.session.commit()
        self.expire.do_work()
        db.session.expunge_all()
        c = db.session.query(Compose).filter(Compose.id == 1).one()
        self.assertEqual(c.state, COMPOSE_STATES['removed'])

    def test_no_expire_done_time_to_expire_in_future(self):
        """
        Test that we do not expire compose if time_to_expire has not been
        reached yet.
        """
        c = db.session.query(Compose).filter(Compose.id == 1).one()
        c.state = COMPOSE_STATES['done']
        db.session.add(c)
        db.session.commit()
        self.expire.do_work()
        db.session.expunge_all()
        c = db.session.query(Compose).filter(Compose.id == 1).one()
        self.assertEqual(c.state, COMPOSE_STATES['done'])