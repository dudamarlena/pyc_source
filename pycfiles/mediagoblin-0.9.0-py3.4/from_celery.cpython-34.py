# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/init/celery/from_celery.py
# Compiled at: 2013-09-23 12:05:51
# Size of source mod 2**32: 3274 bytes
import os, logging, logging.config
from celery.signals import setup_logging
from mediagoblin import app, mg_globals
from mediagoblin.init.celery import setup_celery_from_config
from mediagoblin.tools.pluginapi import hook_runall
OUR_MODULENAME = __name__
_log = logging.getLogger(__name__)

def setup_logging_from_paste_ini(loglevel, **kw):
    if os.path.exists(os.path.abspath('paste_local.ini')):
        logging_conf_file = 'paste_local.ini'
    else:
        logging_conf_file = 'paste.ini'
    logging_conf_file = os.environ.get('PASTE_CONFIG', logging_conf_file)
    if not os.path.exists(logging_conf_file):
        raise IOError('{0} does not exist. Logging can not be set up.'.format(logging_conf_file))
    logging.config.fileConfig(logging_conf_file)
    hook_runall('celery_logging_setup')


setup_logging.connect(setup_logging_from_paste_ini)

def setup_self(check_environ_for_conf=True, module_name=OUR_MODULENAME, default_conf_file=None):
    """
    Transform this module into a celery config module by reading the
    mediagoblin config file.  Set the environment variable
    MEDIAGOBLIN_CONFIG to specify where this config file is.

    By default it defaults to 'mediagoblin.ini'.

    Note that if celery_setup_elsewhere is set in your config file,
    this simply won't work.
    """
    if not default_conf_file:
        if os.path.exists(os.path.abspath('mediagoblin_local.ini')):
            default_conf_file = 'mediagoblin_local.ini'
        else:
            default_conf_file = 'mediagoblin.ini'
    if check_environ_for_conf:
        mgoblin_conf_file = os.path.abspath(os.environ.get('MEDIAGOBLIN_CONFIG', default_conf_file))
    else:
        mgoblin_conf_file = default_conf_file
    if not os.path.exists(mgoblin_conf_file):
        raise IOError('MEDIAGOBLIN_CONFIG not set or file does not exist')
    os.environ['CELERY_CONFIG_MODULE'] = module_name
    app.MediaGoblinApp(mgoblin_conf_file, setup_celery=False)
    setup_celery_from_config(mg_globals.app_config, mg_globals.global_config, settings_module=module_name, set_environ=False)


if os.environ['CELERY_CONFIG_MODULE'] == OUR_MODULENAME:
    setup_self()