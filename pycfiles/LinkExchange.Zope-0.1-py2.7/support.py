# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/zope/support.py
# Compiled at: 2011-04-12 15:58:01
import os, os.path, urllib, Cookie, logging
from linkexchange.utils import normalize_uri
from linkexchange.utils import rearrange_blocks, parse_rearrange_map
from linkexchange.config import file_config, ConfigError
from linkexchange.clients import PageRequest
log = logging.getLogger('linkexchange.zope')
platform = None
formatters = None
options = None

def configure():
    """
    Configures the module: reads linkexchange.cfg file and setups platform,
    formatters and options.
    """
    global options
    global platform
    try:
        cfg_fn = os.environ['LINKEXCHANGE_CONFIG']
    except KeyError:
        cfg_fn = os.path.join(os.getcwd(), 'linkexchange.cfg')
        if not os.path.exists(cfg_fn):
            cfg_fn = None

    if cfg_fn:
        defaults = dict(basedir=os.path.abspath(os.path.dirname(cfg_fn)))
        try:
            if not file_config(globals(), cfg_fn, defaults=defaults):
                log.error('Unable to read configuration file: %s', cfg_fn)
        except ConfigError as e:
            log.error('Configuration error: %s', str(e))

    if options is None:
        options = {}
    if platform is None:
        log.warning('LinkExchange is not configured')
    return


def convert_request(request):
    """
    Converts Zope Request object to LinkExchange PageRequest object.
    """
    host = request['HTTP_HOST']
    path = request['PATH_INFO']
    if type(path) == unicode:
        path = path.encode('utf-8')
    path_list = path.split('/')
    del path_list[1:1 + int(options.get('remove_path_components', '0'))]
    query_string = request['QUERY_STRING']
    request_uri = urllib.quote(('/').join(path_list)) + (query_string and '?' + query_string or '')
    cookies = Cookie.SimpleCookie(request.get_header('HTTP_COOKIE', ''))
    request = PageRequest(host=options.get('host', host), uri=normalize_uri(request_uri), cookies=cookies, remote_addr=request.get_header('REMOTE_ADDR', None), meta=request)
    return request


def get_blocks(request):
    """
    Returns links blocks for request.
    """
    global formatters
    if platform is None:
        return []
    else:
        if formatters is None:
            log.warning('No formatters defined')
            return []
        if request.has_key('LINKEXCHANGE_BLOCKS'):
            return request['LINKEXCHANGE_BLOCKS']
        lx_request = convert_request(request)
        blocks = platform.get_blocks(lx_request, formatters)
        try:
            rearrange_map = parse_rearrange_map(options['rearrange_map'])
        except KeyError:
            pass
        except ValueError:
            log.warning('Unable to parse rearrange_map')
        else:
            blocks = rearrange_blocks(lx_request, blocks, rearrange_map)

        request.set('LINKEXCHANGE_BLOCKS', blocks)
        return blocks


def get_links(request):
    """
    Returns raw links for request.
    """
    if platform is None:
        return []
    else:
        if request.has_key('LINKEXCHANGE_LINKS'):
            return request['LINKEXCHANGE_LINKS']
        lx_request = convert_request(request)
        links = platform.get_raw_links(lx_request)
        request.set('LINKEXCHANGE_LINKS', links)
        return links


def content_filter(request, content):
    """
    Filters content through clients content_filter().
    """
    if platform is None:
        return content
    else:
        lx_request = convert_request(request)
        return platform.content_filter(lx_request, content)


configure()