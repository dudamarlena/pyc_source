# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/turbogears/support.py
# Compiled at: 2011-05-13 04:29:22
import os.path, urllib, logging
try:
    import kid
except ImportError:
    kid = None

from turbogears import config
from cherrypy import request
from linkexchange.utils import rearrange_blocks, parse_rearrange_map
from linkexchange.utils import normalize_uri
from linkexchange.config import file_config, ConfigError
from linkexchange.clients import PageRequest
log = logging.getLogger('linkexchange.turbogears')
configured = False
platform = None
formatters = None
options = None

def configure():
    global configured

    def check_mod_dir(mod, parent=False):
        try:
            mod = __import__(mod, {}, {}, [''])
        except (ImportError, ValueError):
            return

        dir = os.path.dirname(mod.__file__)
        if parent:
            dir = os.path.dirname(dir)
        fn = os.path.join(dir, 'linkexchange.cfg')
        if not os.path.exists(fn):
            return
        else:
            return fn

    cfg_fn = config.get('linkexchange.config', None)
    if not cfg_fn:
        cfg_fn = check_mod_dir(config.get('package', ''), True)
    if cfg_fn:
        defaults = dict(basedir=os.path.abspath(os.path.dirname(cfg_fn)))
        try:
            if not file_config(globals(), cfg_fn, defaults=defaults):
                log.error('Unable to read configuration file: %s', cfg_fn)
        except ConfigError as e:
            log.error('Configuration error: %s', str(e))

    else:
        log.warning('No configuration file found')
    configured = True
    return


def convert_request(request):
    """
    Converts cherrypy.request object to linkexchange.PageRequest object.
    """
    try:
        script_name = request.script_name
    except AttributeError:
        script_name = ''

    try:
        path = request.original_path
    except AttributeError:
        path = request.path_info

    try:
        cookies = request.cookie
    except AttributeError:
        cookies = request.simple_cookie

    try:
        remote_addr = request.remote.ip
    except AttributeError:
        remote_addr = request.remote_host

    request_uri = script_name + path
    if type(request_uri) == unicode:
        request_uri = request_uri.encode('utf-8')
    request_uri = urllib.quote(request_uri)
    if request.query_string:
        request_uri += '?' + request.query_string
    meta = {}
    for k, v in request.header_list:
        meta['HTTP_' + k.upper().replace('-', '_')] = v

    request = PageRequest(host=options.get('host', request.headers['Host']), uri=normalize_uri(request_uri), cookies=cookies, remote_addr=remote_addr, meta=meta)
    return request


def content_filter(content):
    if not configured:
        configure()
    if platform is None:
        return content
    else:
        as_kid_xml = False
        if kid is not None:
            if isinstance(content, kid.ElementStream):
                content = content.expand()
            if hasattr(content, 'tag') and hasattr(content, 'attrib'):
                content = [
                 content]
            if type(content) == list:
                as_kid_xml = True
                orig_content = content
                s = kid.XMLSerializer(namespaces={'http://www.w3.org/1999/xhtml': ''})

                def serialize(item):
                    if isinstance(item, basestring):
                        return s.escape_cdata(item)
                    return unicode(s.serialize(kid.ElementStream(item), encoding='utf-8', fragment=True), 'utf-8')

                content = ('').join(map(serialize, content))
        content = platform.content_filter(convert_request(request), content)
        if as_kid_xml:
            try:
                content = kid.XML(content).expand()
            except Exception as e:
                log.error('Error parsing XML', exc_info=True)
                return orig_content

        return content


def add_stdvars(varss):

    def as_kid_xml(value):
        try:
            return kid.XML(value).expand()
        except Exception as e:
            log.error('Error parsing XML', exc_info=True)
            return kid.XML('<!-- Error parsing XML -->')

    if not configured:
        configure()
    if platform is None:
        return
    else:
        lx_request = convert_request(request)
        vars = {}
        if formatters:
            vars['linkexchange_blocks'] = platform.get_blocks(lx_request, formatters)
            try:
                rearrange_map = parse_rearrange_map(options['rearrange_map'])
            except KeyError:
                pass
            except ValueError:
                log.warning('Unable to parse rearrange_map')
            else:
                vars['linkexchange_blocks'] = rearrange_blocks(lx_request, vars['linkexchange_blocks'], rearrange_map)

            if options.get('as_kid_xml', False):
                vars['linkexchange_blocks'] = map(as_kid_xml, vars['linkexchange_blocks'])
        if options.get('use_raw_links', False):
            vars['linkexchange_links'] = platform.get_raw_links(lx_request)
            if options.get('as_kid_xml', False):
                vars['linkexchange_links'] = map(as_kid_xml, vars['linkexchange_links'])
        vars['linkexchange_filter'] = content_filter
        return varss.update(vars)