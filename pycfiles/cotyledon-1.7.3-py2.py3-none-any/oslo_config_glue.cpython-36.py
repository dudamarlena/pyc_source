# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /workspace/sileht/common/cotyledon/build/lib.linux-x86_64-2.7/cotyledon/oslo_config_glue.py
# Compiled at: 2018-08-28 05:24:33
# Size of source mod 2**32: 3908 bytes
import copy, functools, logging, os
from oslo_config import cfg
LOG = logging.getLogger(__name__)
service_opts = [
 cfg.BoolOpt('log_options', default=True,
   mutable=True,
   help='Enables or disables logging values of all registered options when starting a service (at DEBUG level).'),
 cfg.IntOpt('graceful_shutdown_timeout', mutable=True,
   default=60,
   help='Specify a timeout after which a gracefully shutdown server will exit. Zero value means endless wait.')]

def _load_service_manager_options(service_manager, conf):
    service_manager.graceful_shutdown_timeout = conf.graceful_shutdown_timeout
    if conf.log_options:
        LOG.debug('Full set of CONF:')
        conf.log_opt_values(LOG, logging.DEBUG)


def _load_service_options(service, conf):
    service.graceful_shutdown_timeout = conf.graceful_shutdown_timeout
    if conf.log_options:
        LOG.debug('Full set of CONF:')
        conf.log_opt_values(LOG, logging.DEBUG)


def _configfile_reload(conf, reload_method):
    if reload_method == 'reload':
        conf.reload_config_files()
    elif reload_method == 'mutate':
        conf.mutate_config_files()


def _new_worker_hook(conf, reload_method, service_id, worker_id, service):

    def _service_reload(service):
        _configfile_reload(conf, reload_method)
        _load_service_options(service, conf)

    service._on_reload_internal_hook = _service_reload
    _load_service_options(service, conf)


def setup(service_manager, conf, reload_method='reload'):
    """Load services configuration from oslo config object.

    It reads ServiceManager and Service configuration options from an
    oslo_config.ConfigOpts() object. Also It registers a ServiceManager hook to
    reload the configuration file on reload in the master process and in all
    children. And then when each child start or reload, the configuration
    options are logged if the oslo config option 'log_options' is True.

    On children, the configuration file is reloaded before the running the
    application reload method.

    Options currently supported on ServiceManager and Service:
    * graceful_shutdown_timeout

    :param service_manager: ServiceManager instance
    :type service_manager: cotyledon.ServiceManager
    :param conf: Oslo Config object
    :type conf: oslo_config.ConfigOpts()
    :param reload_method: reload or mutate the config files
    :type reload_method: str "reload/mutate"
    """
    conf.register_opts(service_opts)
    _load_service_manager_options(service_manager, conf)

    def _service_manager_reload():
        _configfile_reload(conf, reload_method)
        _load_service_manager_options(service_manager, conf)

    if os.name != 'posix':
        return
    service_manager.register_hooks(on_new_worker=(functools.partial(_new_worker_hook, conf, reload_method)),
      on_reload=_service_manager_reload)


def list_opts():
    """Entry point for oslo-config-generator."""
    return [
     (
      None, copy.deepcopy(service_opts))]