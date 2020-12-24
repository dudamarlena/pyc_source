# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/web/support.py
# Compiled at: 2011-05-13 04:42:02
import os, os.path, urllib, logging, web
from linkexchange.utils import normalize_uri
from linkexchange.utils import rearrange_blocks, parse_rearrange_map
from linkexchange.config import file_config, ConfigError
from linkexchange.clients import PageRequest
from linkexchange.platform import Platform
log = logging.getLogger('linkexchange.web')

def convert_request(app):
    request_uri = web.ctx.homepath + web.ctx.path
    if isinstance(request_uri, unicode):
        request_uri = request_uri.encode('utf-8')
    request_uri = urllib.quote(request_uri) + web.ctx.query
    return PageRequest(host=app.linkexchange_options.get('host', web.ctx.host), uri=normalize_uri(request_uri), cookies=web.cookies(), remote_addr=web.ctx.ip, meta=web.ctx.env)


def handle_request(app):
    req = convert_request(app)
    if app.linkexchange_formatters:
        web.ctx.linkexchange_blocks = app.linkexchange_platform.get_blocks(req, app.linkexchange_formatters)
        try:
            rearrange_map = parse_rearrange_map(app.linkexchange_options['rearrange_map'])
        except KeyError:
            pass
        except ValueError:
            log.warning('Unable to parse rearrange_map')
        else:
            web.ctx.linkexchange_blocks = rearrange_blocks(req, web.ctx.linkexchange_blocks, rearrange_map)

    if app.linkexchange_options.get('use_raw_links', False):
        web.ctx.linkexchange_links = app.linkexchange_platform.get_raw_links(req)


def content_filter(app, content):
    req = convert_request(app)
    return app.linkexchange_platform.content_filter(req, unicode(content))


def configure(app):

    def request_processor(handler):
        handle_request(app)
        result = handler()
        return result

    try:
        cfg_fn = web.config.linkexchange_config
    except AttributeError:
        cfg_fn = None

    vars = dict(linkexchange_options={}, linkexchange_platform=None, linkexchange_formatters=None)
    if cfg_fn:
        defaults = dict(basedir=os.path.abspath(os.path.dirname(cfg_fn)))
        try:
            if not file_config(vars, cfg_fn, defaults=defaults, prefix='linkexchange_'):
                log.error('Unable to read configuration file: %s', cfg_fn)
        except ConfigError as e:
            log.error('Configuration error: %s', str(e))

    for k, v in vars.items():
        setattr(app, k, getattr(web.config, k, v))
        if k == 'linkexchange_options':
            for o, ov in v.items():
                app.linkexchange_options.setdefault(o, ov)

    try:
        app.linkexchange_platform = Platform(web.config.linkexchange_clients)
    except AttributeError:
        pass

    if app.linkexchange_platform is None:
        log.warning('LinkExchange is not configured')
    else:
        app.add_processor(request_processor)
    return


class linkexchange_handler:

    def GET(self):
        app = web.ctx.app_stack[(-1)]
        if app.linkexchange_platform is None:
            raise web.notfound()
        page_request = convert_request(app)
        page_response = app.linkexchange_platform.handle_request(page_request)
        if page_response.status == 200:
            web.ctx.status = '200 OK'
        else:
            if page_response.status == 404:
                web.ctx.status = '404 Not found'
            else:
                web.ctx.status = str(page_response.status)
            for k, v in page_response.headers.items():
                web.header(k, v, unique=None)

        return page_response.body

    POST = GET