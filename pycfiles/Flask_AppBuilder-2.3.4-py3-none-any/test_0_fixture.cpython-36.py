# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/daniel/workarea/preset/Flask-AppBuilder/flask_appbuilder/tests/test_0_fixture.py
# Compiled at: 2020-03-31 08:10:13
# Size of source mod 2**32: 1060 bytes
from flask_appbuilder import SQLA
from .base import FABTestCase
from .const import MODEL1_DATA_SIZE, PASSWORD_ADMIN, PASSWORD_READONLY, USERNAME_ADMIN, USERNAME_READONLY
from .sqla.models import insert_data

class TestData(FABTestCase):

    def setUp(self):
        from flask import Flask
        from flask_appbuilder import AppBuilder
        self.app = Flask(__name__)
        self.app.config.from_object('flask_appbuilder.tests.config_api')
        self.db = SQLA(self.app)
        self.appbuilder = AppBuilder(self.app, self.db.session)

    def test_data(self):
        insert_data(self.db.session, MODEL1_DATA_SIZE)

    def test_create_admin(self):
        self.create_admin_user(self.appbuilder, USERNAME_ADMIN, PASSWORD_ADMIN)

    def test_create_ro_user(self):
        self.create_user((self.appbuilder),
          USERNAME_READONLY,
          PASSWORD_READONLY,
          'ReadOnly',
          first_name='readonly',
          last_name='readonly',
          email='readonly@fab.org')