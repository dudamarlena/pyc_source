# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/__init__.py
# Compiled at: 2013-04-11 17:47:52
import logging, warnings
from camelot.core.conf import settings
logging.basicConfig(level=logging.INFO, format='[%(levelname)-7s] [%(name)-35s] - %(message)s')

class TestSettings(object):

    def __init__(self):
        from sqlalchemy.pool import StaticPool
        from sqlalchemy import create_engine
        self.engine = create_engine('sqlite:///', poolclass=StaticPool)

    def setup_model(self):
        from camelot.core.sql import metadata
        metadata.bind = self.ENGINE()
        from camelot.model import authentication
        from camelot.model import party
        from camelot.model import i18n
        from camelot.model import memento
        from camelot.model import fixture
        from camelot.model import batch_job
        import camelot_example.model
        from camelot_example.view import setup_views
        from camelot_example.fixtures import load_movie_fixtures
        from camelot.model.authentication import update_last_login
        from camelot.core.orm import setup_all
        setup_all(create_tables=True)
        setup_views()
        load_movie_fixtures()
        update_last_login()

    CAMELOT_MEDIA_ROOT = 'media'

    def ENGINE(self):
        return self.engine


settings.append(TestSettings())