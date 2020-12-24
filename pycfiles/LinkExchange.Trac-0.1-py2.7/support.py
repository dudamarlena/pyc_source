# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/trac/support.py
# Compiled at: 2011-05-12 17:23:25
import os.path, logging
from linkexchange.utils import normalize_uri
from linkexchange.config import file_config, ConfigError
from linkexchange.clients import PageRequest
log = logging.getLogger('linkexchange.trac')

def configure(component):
    config = component.config
    env = component.env
    lx_log = logging.getLogger('linkexchange')
    try:
        lx_log._trac_handler
    except AttributeError:
        try:
            log_hdl = env.log._trac_handler
        except AttributeError:
            pass
        else:
            lx_log.addHandler(log_hdl)
            lx_log._trac_handler = log_hdl
            lx_log.setLevel(env.log.getEffectiveLevel())

    cfg_fn = config.getpath('linkexchange', 'config', None)
    if not cfg_fn:
        cfg_fn = os.path.join(env.path, 'conf', 'linkexchange.cfg')
        if not os.path.exists(cfg_fn):
            cfg_fn = None
    component.lx_platform = None
    component.lx_formatters = None
    component.lx_options = {}
    if cfg_fn:
        defaults = dict(basedir=os.path.abspath(os.path.dirname(cfg_fn)), envdir=os.path.abspath(env.path))
        try:
            if not file_config(component.__dict__, cfg_fn, defaults=defaults, prefix='lx_'):
                log.error('Unable to read configuration file: %s', cfg_fn)
        except ConfigError as e:
            log.error('Configuration error: %s', str(e))

    else:
        log.warning('No configuration file found')
    return


def convert_request(request, options):
    request_uri = request.href(request.path_info)
    query_string = request.query_string
    if not query_string.startswith('?'):
        query_string = '?' + query_string
    request_uri += query_string
    request = PageRequest(host=options.get('host', request.environ.get('HTTP_HOST', '')), uri=normalize_uri(request_uri), cookies=request.incookie, remote_addr=request.remote_addr, meta=request.environ)
    return request