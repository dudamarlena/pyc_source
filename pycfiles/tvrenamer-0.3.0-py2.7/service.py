# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/service.py
# Compiled at: 2015-11-08 18:31:47
import logging, logging.config, logging.handlers, os, sys
from oslo_config import cfg
import six
from six import moves
import tvrenamer
from tvrenamer import options
from tvrenamer import services
logging.getLogger().addHandler(logging.NullHandler())
DEFAULT_LIBRARY_LOG_LEVEL = {'stevedore': logging.WARNING, 'requests': logging.WARNING, 
   'tvdbapi_client': logging.WARNING, 
   'trakt': logging.WARNING}
CONSOLE_MESSAGE_FORMAT = '%(message)s'
LOG_FILE_MESSAGE_FORMAT = '[%(asctime)s] %(levelname)-8s %(name)s %(message)s'

def _setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(cfg.CONF.loglevel.upper())
    if cfg.CONF.logfile:
        file_handler = logging.handlers.RotatingFileHandler(filename=cfg.CONF.logfile, maxBytes=1024000, backupCount=9)
        formatter = logging.Formatter(LOG_FILE_MESSAGE_FORMAT)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    if cfg.CONF.console_output_enabled:
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
    cfg_file = ('{0}.conf').format(tvrenamer.PROJECT_NAME)
    if virtual_path:
        config_files.append(os.path.join(virtual_path, 'etc', cfg_file))
        config_files.append(os.path.join(virtual_path, 'etc', tvrenamer.PROJECT_NAME, cfg_file))
    config_files.extend(cfg.find_config_files(project=tvrenamer.PROJECT_NAME))
    cfg.CONF(args, project=tvrenamer.PROJECT_NAME, version=tvrenamer.__version__, default_config_files=list(moves.filter(os.path.isfile, config_files)))
    if not cfg.CONF.config_dir and cfg.CONF.config_file:
        cfg.CONF.set_default('config_dir', os.path.dirname(cfg.CONF.config_file[(-1)]))


def prepare_service(args=None):
    """Configures application and setups logging."""
    options.register_opts(cfg.CONF)
    services.load_service_opts(cfg.CONF)
    _configure(args)
    _setup_logging()
    cfg.CONF.log_opt_values(logging.getLogger(), logging.DEBUG)