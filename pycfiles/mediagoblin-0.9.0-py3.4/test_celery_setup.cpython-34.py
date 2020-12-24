# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_celery_setup.py
# Compiled at: 2014-10-15 12:42:52
# Size of source mod 2**32: 2652 bytes
import pkg_resources
from mediagoblin.init import celery as celery_setup
from mediagoblin.init.config import read_mediagoblin_config
TEST_CELERY_CONF_NOSPECIALDB = pkg_resources.resource_filename('mediagoblin.tests', 'fake_celery_conf.ini')

def test_setup_celery_from_config():

    def _wipe_testmodule_clean(module):
        vars_to_wipe = [var for var in dir(module) if not var.startswith('__') and not var.endswith('__')]
        for var in vars_to_wipe:
            delattr(module, var)

    global_config, validation_result = read_mediagoblin_config(TEST_CELERY_CONF_NOSPECIALDB)
    app_config = global_config['mediagoblin']
    celery_setup.setup_celery_from_config(app_config, global_config, 'mediagoblin.tests.fake_celery_module', set_environ=False)
    from mediagoblin.tests import fake_celery_module
    assert fake_celery_module.SOME_VARIABLE == 'floop'
    assert fake_celery_module.MAIL_PORT == 2000
    assert isinstance(fake_celery_module.MAIL_PORT, int)
    assert fake_celery_module.CELERYD_ETA_SCHEDULER_PRECISION == 1.3
    assert isinstance(fake_celery_module.CELERYD_ETA_SCHEDULER_PRECISION, float)
    assert fake_celery_module.CELERY_RESULT_PERSISTENT is True
    assert fake_celery_module.CELERY_IMPORTS == [
     'foo.bar.baz', 'this.is.an.import', 'mediagoblin.processing.task',
     'mediagoblin.notifications.task', 'mediagoblin.submit.task']
    assert fake_celery_module.CELERY_RESULT_BACKEND == 'database'
    assert fake_celery_module.CELERY_RESULT_DBURI == 'sqlite:///' + pkg_resources.resource_filename('mediagoblin.tests', 'celery.db')
    assert fake_celery_module.BROKER_TRANSPORT == 'sqlalchemy'
    assert fake_celery_module.BROKER_URL == 'sqlite:///' + pkg_resources.resource_filename('mediagoblin.tests', 'kombu.db')