# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/wsgixml/applyxslt.py
# Compiled at: 2007-01-01 13:27:07
"""
WSGI middleware that applies XSLT to an XML response body if needed

Copyright 2006 Uche Ogbuji
Licensed under the Academic Free License version 3.0

See also:
  http://4suite.org/docs/CoreManual.xml#id1964053292
  http://trac.defuze.org/wiki/Picket
  http://projects.dowski.com/view/buffetxslt
"""
import re, sys, time
from cStringIO import StringIO
from itertools import chain
from xml import sax
from Ft.Xml import Sax, InputSource, CreateInputSource
from Ft.Xml.Xslt import Processor
from util import iterwrapper, get_request_url
USER_AGENT_REGEXEN = [
 '.*MSIE 5.5.*',
 '.*MSIE 6.0.*',
 '.*MSIE 7.0.*',
 '.*Gecko/2005.*',
 '.*Gecko/2006.*',
 '.*Opera/9.*',
 '.*AppleWebKit/31.*',
 '.*AppleWebKit/4.*']
USER_AGENT_REGEXEN = [ re.compile(regex) for regex in USER_AGENT_REGEXEN ]
WSGI_NS = 'http://www.wsgi.org/'
MTYPE_PAT = re.compile('.*/.*xml.*')

def xsltize(obj):
    if isinstance(obj, unicode):
        return obj
    elif isinstance(obj, str):
        try:
            return obj.decode('utf-8')
        except UnicodeError:
            return

    elif isinstance(obj, int) or isinstance(obj, long) or isinstance(obj, float):
        return obj
    elif isinstance(obj, bool):
        return obj
    elif isinstance(obj, list) or isinstance(obj, tuple):
        obj = [ xsltize(o) for o in obj ]
        if [ o for o in obj if obj is None or isinstance(obj, list) or isinstance(obj, tuple) ]:
            return
        else:
            return obj
    else:
        return
    return


def setup_xslt_params(ns, params):
    xsltparams = dict([ (k, params[k]) for k in params if xsltize(params[k]) is not None
                      ])
    return xsltparams


class find_xslt_pis(sax.ContentHandler):

    def __init__(self, parser):
        parser.setContentHandler(self)
        self.parser = parser

    def startDocument(self):
        self.ecount = 0
        self.xslt_pi = None
        return

    def startElementNS(self, name, qname, attribs):
        self.ecount += 1
        if self.ecount == 2:
            self.parser.setProperty(Sax.PROPERTY_YIELD_RESULT, self.xslt_pi)

    def processingInstruction(self, target, data):
        if target == 'xml-stylesheet':
            data = data.split()
            pseudo_attrs = {}
            for d in data:
                seg = d.split('=')
                if len(seg) == 2:
                    pseudo_attrs[seg[0]] = seg[1][1:-1]

            if pseudo_attrs.has_key('href') and pseudo_attrs.has_key('type') and pseudo_attrs['type'] in Processor.XSLT_IMT:
                self.xslt_pi = pseudo_attrs['href']
                self.parser.setProperty(Sax.PROPERTY_YIELD_RESULT, self.xslt_pi)


class applyxslt(object):
    """
    Middleware that checks for XSLT transform capability in the client and
    performs the transform on the server side if one is required, and the
    client can't do it
    """

    def __init__(self, app, use_wsgi_env=True, stock_xslt_params=None, ext_modules=None):
        """
        use_wsgi_env - Optional bool determining whether to make the
            WSGI environment available to the XSLT as top level parameter
            overrides (e.g. wsgi:SCRIPT_NAME and wsgi:wsgi.url_scheme).
            Only passes on values it can handle (UTF-8 strings, Unicode,
            numbers, boolean, lists of "nodes").  Default to True
        stock_xslt_params - optional dict of dicts to also pass along as XSLT
            params.  The outer dict is onf the form: {<namespace>: <inner-dict>}
            And the inner dicts are of the form {pname: pvalue}.  The keys
            (pname) may be given as unicode objects if they have no namespace,
            or as (uri, localname) tuples if they do.  The values are
            (UTF-8 strings, Unicode, numbers, boolean, lists of "nodes").
            This is usually used for passing configuration info into XSLT
        ext_modules - Optional list of modules with XPath and XSLT extensions
        """
        self.wrapped_app = app
        self.use_wsgi_env = use_wsgi_env
        self.stock_xslt_params = stock_xslt_params or {}
        self.ext_modules = ext_modules or []
        self.processor_cache = {}

    def __call__(self, environ, start_response):
        client_ua = environ.get('HTTP_USER_AGENT', '')
        xslt_ok = True in [ ua_pat.match(client_ua) is not None for ua_pat in USER_AGENT_REGEXEN
                          ]
        response_params = []

        def start_response_wrapper(status, response_headers, exc_info=None):
            environ['wsgixml.applyxslt.active'] = False
            for (name, value) in response_headers:
                media_type = value.split(';')[0]
                if name.lower() == 'content-type' and MTYPE_PAT.match(media_type):
                    environ['wsgixml.applyxslt.active'] = True

            response_params.extend([status, response_headers, exc_info])

            def dummy_write(data):
                raise RuntimeError('applyxslt does not support the deprecated write() callable in WSGI apps')

            return dummy_write

        iterable = self.wrapped_app(environ, start_response_wrapper)
        (status, response_headers, exc_info) = response_params
        force_server_side = environ.get('wsgixml.applyxslt.force_server_side', False)
        xslt_ok = xslt_ok and not force_server_side

        def next_response_block(response_iter):
            if xslt_ok or not environ['wsgixml.applyxslt.active']:
                start_response(status, response_headers, exc_info)
                for block in response_iter.next():
                    yield block

            else:
                yield produce_final_output(('').join(response_iter))
                return

        def produce_final_output(response, response_headers=response_headers):
            if not xslt_ok and environ['wsgixml.applyxslt.active']:
                use_pi = False
                if force_server_side and force_server_side != True:
                    xslt = force_server_side
                else:
                    parser = Sax.CreateParser()
                    parser.setFeature(Sax.FEATURE_GENERATOR, True)
                    handler = find_xslt_pis(parser)
                    pi_iter = parser.parse(CreateInputSource(response))
                    try:
                        xslt = pi_iter.next()
                    except StopIteration:
                        xslt = None

                    use_pi = True
                if xslt:
                    xslt = xslt.encode('utf-8')
                    result = StringIO()
                    source = InputSource.DefaultFactory.fromString(response, uri=get_request_url(environ))
                    params = {}
                    for ns in self.stock_xslt_params:
                        params.update(setup_xslt_params(ns, self.stock_xslt_params[ns]))

                    start = time.time()
                    if self.processor_cache and xslt in self.processor_cache:
                        processor = self.processor_cache[xslt]
                        use_pi = False
                        print >> sys.stderr, 'Using cached processor instance for transform', xslt
                    else:
                        print >> sys.stderr, 'Creating new processor instance for transform', xslt
                        processor = Processor.Processor()
                        if self.ext_modules:
                            processor.registerExtensionModules(self.ext_modules)
                        if self.use_wsgi_env:
                            params.update(setup_xslt_params(WSGI_NS, environ))
                        if environ.has_key('paste.recursive.include'):
                            xslt_resp = environ['paste.recursive.include'](xslt)
                            isrc = InputSource.DefaultFactory.fromString(xslt_resp.body, get_request_url(environ))
                            processor.appendStylesheet(isrc)
                        elif not use_pi:
                            isrc = InputSource.DefaultFactory.fromUri(xslt, get_request_url(environ))
                            processor.appendStylesheet(isrc)
                        self.processor_cache[xslt] = processor
                    processor.run(source, outputStream=result, ignorePis=not use_pi, topLevelParams=params)
                    response_headers = [ (name, value) for (name, value) in response_headers if name.lower() not in ('content-length',
                                                                                                                     'content-type')
                                       ]
                    imt = processor.outputParams.mediaType
                    response_headers.append(('content-type', imt))
                    start_response(status, response_headers, exc_info)
                    end = time.time()
                    print >> sys.stderr, '%s: elapsed time: %0.3f\n' % (xslt, end - start)
                    return result.getvalue()
            return

        return iterwrapper(iterable, next_response_block)