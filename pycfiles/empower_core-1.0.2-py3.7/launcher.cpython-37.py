# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/launcher.py
# Compiled at: 2020-05-10 08:37:07
# Size of source mod 2**32: 5055 bytes
"""Launcher module."""
import configparser, ssl, uuid, os, logging, logging.config, sys
from importlib import import_module
from argparse import ArgumentParser
import tornado.ioloop
from pymodm.connection import connect
SERVICES = dict()

def srv(name):
    """Get a service instance or return None"""
    if name in SERVICES:
        return SERVICES[name]


def srv_or_die(name):
    """Get a service instance or return None"""
    if name in SERVICES:
        return SERVICES[name]
    logging.error('Unable to find service %s', name)
    sys.exit(1)


def _do_launch(managers, managers_order):
    """Parse arguments and launch controller."""
    for manager in managers_order:
        module = managers[manager]['module']
        params = managers[manager]['params']
        if manager in SERVICES:
            logging.error('%s manager already registered', manager)
            return False
        init_method = getattr(import_module(module), 'launch')
        logging.info('Loading manager: %s', manager)
        if params:
            logging.info('  - params: %s', params)
        service = init_method(context=None, service_id=uuid.uuid4(), **params)
        SERVICES[manager] = service

    for manager in managers_order:
        service = SERVICES[manager]
        logging.info('Starting manager: %s', manager)
        api_manager = srv_or_die('apimanager')
        for handler in service.HANDLERS:
            api_manager.register_handler(handler)
            handler.service = service

        service.start()

    return True


def _setup_db(args):
    """ Setup db connection. """
    runtime_config = args.config + '/runtime.cfg'
    config = configparser.ConfigParser()
    config.read(runtime_config)
    mongodb_uri = config.get('general', 'mongodb', fallback=None)
    if mongodb_uri:
        connect(mongodb_uri, ssl_cert_reqs=(ssl.CERT_NONE))


def _setup_logging(args):
    """ Setup logging. """
    runtime_config = args.config + '/runtime.cfg'
    config = configparser.ConfigParser()
    config.read(runtime_config)
    log_config = config.get('general', 'logging', fallback='/etc/empower/logging.cfg')
    if not os.path.exists(log_config):
        print('Could not find logging config file: %s' % log_config)
        sys.exit(1)
    logging.config.fileConfig(log_config, disable_existing_loggers=False)


def _pre_startup(args):
    """Perform pre-startup operations."""
    _setup_logging(args)
    _setup_db(args)


def _post_startup():
    """Perform post-startup operation."""
    pass


def _read_config(args):
    """Read config file."""
    runtime_config = args.config + '/runtime.cfg'
    config = configparser.ConfigParser()
    config.read(runtime_config)
    managers = {}
    managers_order = []
    mngrs = config.get('general', 'managers', fallback=None)
    if not mngrs:
        return (
         managers, managers_order)
    for mngr in mngrs.split(','):
        module = config.get(mngr, 'module', fallback=None)
        if not module:
            continue
        managers_order.append(mngr)
        managers[mngr] = {'module':module, 
         'params':{}}
        for param in config[mngr]:
            if param == 'module':
                continue
            managers[mngr]['params'][param] = config[mngr][param]

    return (
     managers, managers_order)


def _parse_global_args(config):
    """ Parse global arguments list. """
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', dest='config',
      default=config,
      help=('Configuration directory, default: %s' % config))
    return parser.parse_known_args(sys.argv[1:])


def main(config=''):
    """Parses the command line and loads the plugins."""
    args, _ = _parse_global_args(config)
    _pre_startup(args)
    managers, managers_order = _read_config(args)
    if _do_launch(managers, managers_order):
        _post_startup()
    else:
        raise RuntimeError()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()