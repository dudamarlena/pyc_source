# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/utils.py
# Compiled at: 2017-08-31 11:17:14
# Size of source mod 2**32: 3391 bytes
import unittest
from odcs.server import db
from sqlalchemy import event
from odcs.server.events import cache_composes_if_state_changed
from odcs.server.events import start_to_publish_messages
from flask.ext.sqlalchemy import SignallingSession

class ModelsBaseTest(unittest.TestCase):
    __doc__ = 'Base test case for models\n\n    Database and schemas are initialized on behalf of developers.\n    '
    disable_event_handlers = True

    def setUp(self):
        event.remove(SignallingSession, 'before_commit', cache_composes_if_state_changed)
        event.remove(SignallingSession, 'after_commit', start_to_publish_messages)
        db.session.remove()
        db.drop_all()
        db.create_all()
        db.session.commit()
        setup_composes = getattr(self, 'setup_composes', None)
        if setup_composes is not None:
            assert callable(setup_composes)
            setup_composes()
        if hasattr(self, 'setup_composes'):
            getattr(self, 'setup_composes')()
        if not self.disable_event_handlers:
            event.listen(SignallingSession, 'before_commit', cache_composes_if_state_changed)
            event.listen(SignallingSession, 'after_commit', start_to_publish_messages)

    def tearDown(self):
        if not self.disable_event_handlers:
            event.remove(SignallingSession, 'before_commit', cache_composes_if_state_changed)
            event.remove(SignallingSession, 'after_commit', start_to_publish_messages)
        db.session.remove()
        db.drop_all()
        db.session.commit()
        event.listen(SignallingSession, 'before_commit', cache_composes_if_state_changed)
        event.listen(SignallingSession, 'after_commit', start_to_publish_messages)