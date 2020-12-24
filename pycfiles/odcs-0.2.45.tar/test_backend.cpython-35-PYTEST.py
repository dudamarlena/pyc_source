# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_backend.py
# Compiled at: 2017-08-31 11:17:14
# Size of source mod 2**32: 5698 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from mock import patch, MagicMock
from odcs.server import db
from odcs.server.models import Compose
from odcs.common.types import COMPOSE_FLAGS, COMPOSE_RESULTS, COMPOSE_STATES
from odcs.server.pdc import ModuleLookupError
from odcs.server.pungi import PungiSourceType
from odcs.server.backend import resolve_compose, get_reusable_compose
from utils import ModelsBaseTest
from pdc import mock_pdc
thisdir = os.path.abspath(os.path.dirname(__file__))

class TestBackend(ModelsBaseTest):

    def test_resolve_compose_repo(self):
        c = Compose.create(db.session, 'me', PungiSourceType.REPO, os.path.join(thisdir, 'repo'), COMPOSE_RESULTS['repository'], 3600, packages='ed')
        db.session.commit()
        resolve_compose(c)
        db.session.commit()
        db.session.expire_all()
        c = db.session.query(Compose).filter(Compose.id == 1).one()
        self.assertEqual(c.koji_event, 1496834159)

    @mock_pdc
    def test_resolve_compose_module(self):
        c = Compose.create(db.session, 'me', PungiSourceType.MODULE, 'moduleA-f26', COMPOSE_RESULTS['repository'], 3600)
        db.session.commit()
        resolve_compose(c)
        db.session.commit()
        c = db.session.query(Compose).filter(Compose.id == 1).one()
        self.assertEqual(c.source, ' '.join(['moduleA-f26-20170809000000',
         'moduleB-f26-20170808000000',
         'moduleC-f26-20170807000000',
         'moduleD-f26-20170806000000']))

    @mock_pdc
    def test_resolve_compose_module_no_deps(self):
        c = Compose.create(db.session, 'me', PungiSourceType.MODULE, 'moduleA-f26 moduleA-f26', COMPOSE_RESULTS['repository'], 3600, flags=COMPOSE_FLAGS['no_deps'])
        db.session.commit()
        resolve_compose(c)
        db.session.commit()
        c = db.session.query(Compose).filter(Compose.id == 1).one()
        self.assertEqual(c.source, 'moduleA-f26-20170809000000')

    @mock_pdc
    def expect_module_lookup_error(self, source, match):
        c = Compose.create(db.session, 'me', PungiSourceType.MODULE, source, COMPOSE_RESULTS['repository'], 3600)
        db.session.commit()
        with self.assertRaisesRegexp(ModuleLookupError, match):
            resolve_compose(c)

    def test_resolve_compose_module_not_found(self):
        self.expect_module_lookup_error('moduleA-f30', 'Failed to find')

    def test_resolve_compose_module_not_found2(self):
        self.expect_module_lookup_error('moduleA-f26-00000000000000', 'Failed to find')

    def test_resolve_compose_module_conflict(self):
        self.expect_module_lookup_error('moduleA-f26 moduleB-f27', 'which conflicts with')

    def test_resolve_compose_module_conflict2(self):
        self.expect_module_lookup_error('moduleB-f26 moduleB-f27', 'conflicts with')

    @patch('odcs.server.backend.create_koji_session')
    def test_resolve_compose_repo_no_override_koji_event(self, create_koji_session):
        koji_session = MagicMock()
        create_koji_session.return_value = koji_session
        koji_session.getLastEvent.return_value = {'id': 123}
        c = Compose.create(db.session, 'me', PungiSourceType.KOJI_TAG, 'f26', COMPOSE_RESULTS['repository'], 3600, packages='ed')
        c.koji_event = 1
        db.session.commit()
        resolve_compose(c)
        db.session.commit()
        db.session.expire_all()
        c = db.session.query(Compose).filter(Compose.id == 1).one()
        self.assertEqual(c.koji_event, 1)

    def test_get_reusable_compose(self):
        old_c = Compose.create(db.session, 'me', PungiSourceType.REPO, os.path.join(thisdir, 'repo'), COMPOSE_RESULTS['repository'], 3600, packages='ed')
        resolve_compose(old_c)
        old_c.state = COMPOSE_STATES['done']
        c = Compose.create(db.session, 'me', PungiSourceType.REPO, os.path.join(thisdir, 'repo'), COMPOSE_RESULTS['repository'], 3600, packages='ed')
        resolve_compose(c)
        db.session.add(old_c)
        db.session.add(c)
        db.session.commit()
        reused_c = get_reusable_compose(c)
        self.assertEqual(reused_c, old_c)