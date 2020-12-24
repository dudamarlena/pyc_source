# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/turbofeeds/util.py
# Compiled at: 2009-09-26 19:08:14
"""TurboFeed utility functions."""
__docformat__ = 'restructuredtext'
__all__ = [
 'absolute_url',
 'xml_stylesheet']
try:
    from kid import ProcessingInstruction as KidPI
except ImportError:
    KidPI = False

try:
    from genshi.core import PI as GenshiPI
except ImportError:
    GenshiPI = False

try:
    from turbogears.controllers import absolute_url
except:
    from turbogears import url, config
    from cherrypy import request

    def get_server_name():
        """Return name of the server this application runs on."""
        get = config.get
        h = request.headers
        host = get('tg.url_domain') or h.get('X-Forwarded-Host', h.get('Host'))
        if not host:
            host = '%s:%s' % (get('server.socket_host', 'localhost'),
             get('server.socket_port', 8080))
        return host


    def absolute_url(tgpath='/', params=None, **kw):
        """Return absolute URL (including schema and host to this server)."""
        get = config.get
        use_xfh = get('base_url_filter.use_x_forwarded_host', False)
        if request.headers.get('X-Use-SSL'):
            scheme = 'https'
        else:
            scheme = get('tg.url_scheme')
        if not scheme:
            scheme = request.scheme
        base_url = '%s://%s' % (scheme, get_server_name())
        if get('base_url_filter.on', False) and not use_xfh:
            base_url = get('base_url_filter.base_url').rstrip('/')
        return '%s%s' % (base_url, url(tgpath, params, **kw))


def xml_stylesheet(href, type='text/css', engine='text'):
    """Returns an xml-stylesheet processing instruction element for given URL.

    ``href`` can be a string with the URL to the stylesheet or a dict with
    members ``href`` and ``type`` (see below) or a callable returning either.

    ``type`` specifies the value of the "type" atribute of the PI.
    The default type is 'text/css'.

    ``engine`` specifies the template engine used. Can be one of ``"kid"``,
    ``"genshi"``, or ``"text"``. Defaults to ``"text"``.

    """
    if callable(href):
        href = href()
    if isinstance(href, dict):
        type = href.get('type', type)
        href = href['href']
    if engine == 'kid' and KidPI:
        return KidPI('xml-stylesheet type="%s" href="%s"' % (type, href))
    elif engine == 'genshi' and GenshiPI:
        return [(
          GenshiPI,
          ('xml-stylesheet',
           'type="%s" href="%s"' % (
            type, href)), None)]
    elif engine == 'text':
        return '<?xml-stylesheet type="%s" href="%s"?>' % (type, href)
    else:
        raise ValueError('Unsupported template engine.')
    return