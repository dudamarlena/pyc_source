# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot_example/main.py
# Compiled at: 2013-04-11 17:47:53
import logging
FORMAT = '[%(levelname)-7s] [%(name)-35s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger('videostore.main')
try:
    import matplotlib
except:
    logger.error('Charts will not work because of missing matplotlib')

from camelot.core.conf import settings, SimpleSettings

class ExampleSettings(SimpleSettings):
    """Special settings class for the example application, this is done to
    'survive' various packaging regimes, such as windows, debian, ...
    """

    @staticmethod
    def setup_model():
        from sqlalchemy.orm import configure_mappers
        from camelot.core.sql import metadata
        metadata.bind = settings.ENGINE()
        import camelot.model.party, camelot.model.authentication, camelot.model.i18n, camelot.model.fixture, camelot.model.memento, camelot.model.batch_job, camelot_example.model
        configure_mappers()
        metadata.create_all()
        from camelot.model.authentication import update_last_login
        from camelot_example.fixtures import load_movie_fixtures
        load_movie_fixtures()
        from camelot_example.view import setup_views
        setup_views()


settings.append(ExampleSettings('camelot', 'videostore', data='videostore_3.sqlite'))

def main():
    from camelot.view.main import main
    from camelot_example.application_admin import MyApplicationAdmin
    main(MyApplicationAdmin())


if __name__ == '__main__':
    main()