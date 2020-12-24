# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/django_heroku/core.py
# Compiled at: 2019-10-23 15:02:04
# Size of source mod 2**32: 5886 bytes
import logging, os, dj_database_url
from django.test.runner import DiscoverRunner
MAX_CONN_AGE = 600
logger = logging.getLogger(__name__)

class HerokuDiscoverRunner(DiscoverRunner):
    __doc__ = 'Test Runner for Heroku CI, which provides a database for you.\n    This requires you to set the TEST database (done for you by settings().)'

    def setup_databases(self, **kwargs):
        if not os.environ.get('CI'):
            raise ValueError("The CI env variable must be set to enable this functionality.  WARNING:  This test runner will wipe all tables in the 'public' schema of the database it targets!")
        self.keepdb = True
        return (super(HerokuDiscoverRunner, self).setup_databases)(**kwargs)

    def _wipe_tables(self, connection):
        with connection.cursor() as (cursor):
            cursor.execute("\n                    DROP TABLE (\n                        SELECT\n                            table_name\n                        FROM\n                            information_schema.tables\n                        WHERE\n                            table_schema = 'public'\n                    ) CASCADE;\n                ")

    def teardown_databases(self, old_config, **kwargs):
        self.keepdb = True
        for connection, old_name, destroy in old_config:
            if destroy:
                self._wipe_tables(connection)

        (super(HerokuDiscoverRunner, self).teardown_databases)(old_config, **kwargs)


def settings(config, *, db_colors=False, databases=True, test_runner=True, staticfiles=True, allowed_hosts=True, logging=True, secret_key=True):
    if databases:
        if 'DATABASES' not in config:
            config['DATABASES'] = {'default': None}
        else:
            conn_max_age = config.get('CONN_MAX_AGE', MAX_CONN_AGE)
            if db_colors:
                for env, url in os.environ.items():
                    if env.startswith('HEROKU_POSTGRESQL'):
                        db_color = env[len('HEROKU_POSTGRESQL_'):].split('_')[0]
                        logger.info('Adding ${} to DATABASES Django setting ({}).'.format(env, db_color))
                        config['DATABASES'][db_color] = dj_database_url.parse(url, conn_max_age=conn_max_age, ssl_require=True)

            elif 'DATABASE_URL' in os.environ:
                logger.info('Adding $DATABASE_URL to default DATABASE Django setting.')
                config['DATABASES']['default'] = dj_database_url.config(conn_max_age=conn_max_age, ssl_require=True)
                logger.info('Adding $DATABASE_URL to TEST default DATABASE Django setting.')
                if 'CI' in os.environ:
                    config['DATABASES']['default']['TEST'] = config['DATABASES']['default']
            else:
                logger.info('$DATABASE_URL not found, falling back to previous settings!')
    else:
        if test_runner:
            if 'CI' in os.environ:
                config['TEST_RUNNER'] = 'django_heroku.HerokuDiscoverRunner'
        if staticfiles:
            logger.info('Applying Heroku Staticfiles configuration to Django settings.')
            config['STATIC_ROOT'] = os.path.join(config['BASE_DIR'], 'staticfiles')
            config['STATIC_URL'] = '/static/'
            os.makedirs((config['STATIC_ROOT']), exist_ok=True)
            try:
                config['MIDDLEWARE_CLASSES'] = tuple(['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE_CLASSES']))
            except KeyError:
                config['MIDDLEWARE'] = tuple(['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE']))

            config['STATICFILES_STORAGE'] = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        if allowed_hosts:
            logger.info('Applying Heroku ALLOWED_HOSTS configuration to Django settings.')
            config['ALLOWED_HOSTS'] = ['*']
        if logging:
            logger.info('Applying Heroku logging configuration to Django settings.')
            config['LOGGING'] = {'version':1, 
             'disable_existing_loggers':False, 
             'formatters':{'verbose':{'format':'%(asctime)s [%(process)d] [%(levelname)s] pathname=%(pathname)s lineno=%(lineno)s funcname=%(funcName)s %(message)s', 
               'datefmt':'%Y-%m-%d %H:%M:%S'}, 
              'simple':{'format': '%(levelname)s %(message)s'}}, 
             'handlers':{'null':{'level':'DEBUG', 
               'class':'logging.NullHandler'}, 
              'console':{'level':'DEBUG', 
               'class':'logging.StreamHandler', 
               'formatter':'verbose'}}, 
             'loggers':{'testlogger': {'handlers':[
                              'console'], 
                             'level':'INFO'}}}
        if secret_key and 'SECRET_KEY' in os.environ:
            logger.info('Adding $SECRET_KEY to SECRET_KEY Django setting.')
            config['SECRET_KEY'] = os.environ['SECRET_KEY']