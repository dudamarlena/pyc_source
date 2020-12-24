# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/service.py
# Compiled at: 2015-06-29 23:06:14
import logging, logging.config, logging.handlers, os, sys
from oslo_config import cfg
import six
from six import moves
from seedbox import version
logging.getLogger().addHandler(logging.NullHandler())
PROJECT = __package__
DEFAULT_LIBRARY_LOG_LEVEL = {'xworkflows': logging.ERROR, 'stevedore': logging.ERROR, 
   'sqlalchemy': logging.ERROR, 
   'migrate': logging.ERROR}
CONSOLE_MESSAGE_FORMAT = '%(message)s'
LOG_FILE_MESSAGE_FORMAT = '[%(asctime)s] %(levelname)-8s %(name)s %(message)s'
cfg.CONF.import_opt('cron', 'seedbox.options')
cfg.CONF.import_opt('logfile', 'seedbox.options')
cfg.CONF.import_opt('loglevel', 'seedbox.options')
cfg.CONF.import_opt('logconfig', 'seedbox.options')

def _setup_logging():
    if cfg.CONF.logconfig and os.path.exists(cfg.CONF.logconfig):
        logging.config.fileConfig(cfg.CONF.logconfig, disable_existing_loggers=False)
    else:
        root_logger = logging.getLogger()
        root_logger.setLevel(cfg.CONF.loglevel.upper())
        if cfg.CONF.logfile:
            file_handler = logging.handlers.RotatingFileHandler(filename=cfg.CONF.logfile, maxBytes=1024000, backupCount=9)
            formatter = logging.Formatter(LOG_FILE_MESSAGE_FORMAT)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        if not cfg.CONF.cron:
            console = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter(CONSOLE_MESSAGE_FORMAT)
            console.setFormatter(formatter)
            root_logger.addHandler(console)
        for xlib, xlevel in six.iteritems(DEFAULT_LIBRARY_LOG_LEVEL):
            xlogger = logging.getLogger(xlib)
            xlogger.setLevel(xlevel)


def _configure(args):
    config_files = []
    virtual_path = os.getenv('VIRTUAL_ENV')
    cfg_file = ('{0}.conf').format(PROJECT)
    if virtual_path:
        config_files.append(os.path.join(virtual_path, 'etc', cfg_file))
        config_files.append(os.path.join(virtual_path, 'etc', PROJECT, cfg_file))
    config_files.extend(cfg.find_config_files(project=PROJECT))
    cfg.CONF(args, project=PROJECT, version=version.version_string(), default_config_files=list(moves.filter(os.path.isfile, config_files)))
    if not cfg.CONF.config_dir:
        cfg.CONF.set_default('config_dir', os.path.dirname(cfg.CONF.config_file[(-1)]))


def prepare_service(args=None):
    """Configures application and setups logging."""
    _configure(args)
    _setup_logging()
    cfg.CONF.log_opt_values(logging.getLogger(), logging.DEBUG)