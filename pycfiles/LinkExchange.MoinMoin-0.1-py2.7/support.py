# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/MoinMoin/support.py
# Compiled at: 2011-05-12 16:28:06
import re, Cookie, os, urllib, logging, MoinMoin.version
from linkexchange.utils import normalize_uri
from linkexchange.config import file_config, ConfigError
from linkexchange.platform import Platform
from linkexchange.clients import PageRequest
log = logging.getLogger('linkexchange.MoinMoin')
moin_version = tuple([ int(x) for x in MoinMoin.version.release.split('.') ])

def configure(config):

    def check_mod_dir(mod):
        try:
            mod = __import__(mod, {}, {}, [''])
        except ImportError:
            return

        fn = os.path.join(os.path.dirname(mod.__file__), 'linkexchange.cfg')
        if not os.path.exists(fn):
            return
        else:
            return fn

    try:
        cfg_fn = config.linkexchange_config
    except AttributeError:
        cfg_fn = None

    if not cfg_fn:
        cfg_fn = check_mod_dir('farmconfig')
    if not cfg_fn:
        cfg_fn = check_mod_dir('wikiconfig')
    vars = dict(linkexchange_options={}, linkexchange_platform=None)
    if cfg_fn:
        defaults = dict(basedir=os.path.abspath(os.path.dirname(cfg_fn)))
        try:
            if not file_config(vars, cfg_fn, defaults=defaults, prefix='linkexchange_'):
                log.error('Unable to read configuration file: %s', cfg_fn)
        except ConfigError as e:
            log.error('Configuration error: %s', str(e))

    for k, v in vars.items():
        if k == 'linkexchange_options':
            config.__dict__.setdefault(k, {})
            for o, ov in v.items():
                config.linkexchange_options.setdefault(o, ov)

        else:
            config.__dict__.setdefault(k, v)

    try:
        config.linkexchange_platform = Platform(config.linkexchange_clients)
    except AttributeError:
        pass

    if config.linkexchange_platform is None:
        log.warning('LinkExchange is not configured')
    return


def convert_request(request):
    """
    Converts MoinMoin request object to linkexchange.clients.PageRequest

    @param request: MoinMoin request object
    @return: linkexchange.clients.PageRequest object
    """
    if moin_version < (1, 9):
        host = request.http_host
        uri = request.request_uri
        cookies = Cookie.SimpleCookie(request.saved_cookie)
        try:
            meta = request.env
        except AttributeError:
            meta = {}

    else:
        host = request.host
        uri = urllib.quote(request.path.encode('utf-8'), '/')
        if request.query_string:
            uri += '?' + request.query_string
        cookies = request.cookies
        meta = request.environ
    request = PageRequest(host=request.cfg.linkexchange_options.get('host', host), uri=normalize_uri(uri), cookies=cookies, remote_addr=request.remote_addr, meta=meta)
    return request