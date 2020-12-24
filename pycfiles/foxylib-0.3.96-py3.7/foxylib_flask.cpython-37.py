# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/flask/foxylib_flask.py
# Compiled at: 2020-01-31 12:32:02
# Size of source mod 2**32: 3200 bytes
import logging, os
from functools import lru_cache, reduce
import connexion
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 3, FILE_DIR)

class FoxylibFlask:

    @classmethod
    def _load_urls2app(cls, app):
        logger = FoxylibLogger.func_level2logger(cls._load_urls2app, logging.DEBUG)

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def app(cls):
        logger = FoxylibLogger.func_level2logger(cls.app, logging.DEBUG)
        logger.debug({'START': 'START'})
        application = connexion.FlaskApp(__name__)
        application.add_api('swagger.yaml')
        app = application.app
        j_config = {'STATIC_FOLDER': FoxylibFront.dirpath_static()}
        app.config.update(j_config)
        logger.debug({'app.static_folder': app.static_folder})
        cls._load_urls2app(app)
        logger.debug({'END': 'END'})
        return app

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def test_client(cls):
        logger = FoxylibLogger.func_level2logger(cls.test_client, logging.DEBUG)
        logger.debug({'START': 'START'})
        app = cls.app()
        c = app.test_client()
        logger.debug({'END': 'END'})
        return c


class FoxylibFront:

    @classmethod
    def dirpath_static(cls):
        return os.path.join(FILE_DIR, 'static')

    @classmethod
    def health_liveness(cls):
        return ('Foxylib service is healthy based on liveness health check', 200)

    @classmethod
    def health_readiness(cls):
        return ('Foxylib service is healthy based on liveness health check', 200)

    @classmethod
    def test_post(cls, k1, k2):
        return ('Foxylib service is healthy based on liveness health check', 200)


class FoxylibFlaskConfig:

    class Field:
        SESSION_TYPE = 'SESSION_TYPE'
        SECRET_KEY = 'SECRET_KEY'
        SECURITY_PASSWORD_SALT = 'SECURITY_PASSWORD_SALT'

    F = Field

    @classmethod
    def j_config(cls):
        j = {cls.F.SESSION_TYPE: 'filesystem', 
         cls.F.SECRET_KEY: 'sullivan_secret', 
         cls.F.SECURITY_PASSWORD_SALT: 'sullivan_secret second'}
        return j


def main():
    FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
    app = FoxylibFlask.app()
    app.run()


if __name__ == '__main__':
    main()