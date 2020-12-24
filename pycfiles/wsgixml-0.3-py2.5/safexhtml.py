# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/wsgixml/safexhtml.py
# Compiled at: 2006-09-30 20:13:04
"""
Middleware that checks for XHTML capability in the client and translates
XHTML to HTML if the client can't handle it

Copyright 2006 Uche Ogbuji
Licensed under the Academic Free License version 3.0
"""
import cStringIO
from itertools import chain
from xml import sax
from Ft.Xml import CreateInputSource
from Ft.Xml.Sax import SaxPrinter
from Ft.Xml.Lib.HtmlPrinter import HtmlPrinter
from util import iterwrapper, get_request_url
XHTML_IMT = 'application/xhtml+xml'
HTML_CONTENT_TYPE = 'text/html; charset=UTF-8'

class safexhtml(object):
    """
    Middleware that checks for XHTML capability in the client and translates
    XHTML to HTML if the client can't handle it
    """

    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, environ, start_response):
        xhtml_ok = XHTML_IMT in environ.get('HTTP_ACCEPT', '')

        def start_response_wrapper(status, response_headers, exc_info=None):
            environ['wsgixml.safexhtml.active'] = False
            for (name, value) in response_headers:
                if name.lower() == 'content-type' and value.split(';')[0] == XHTML_IMT:
                    response_headers = [ (name, value) for (name, value) in response_headers if name.lower() not in ('content-length',
                                                                                                                     'content-type')
                                       ]
                    response_headers.append(('content-type', HTML_CONTENT_TYPE))
                    environ['wsgixml.safexhtml.active'] = True
                    break

            start_response(status, response_headers, exc_info)

            def dummy_write(data):
                raise RuntimeError('safexhtml does not support the deprecated write() callable in WSGI clients')

            return dummy_write

        iterable = self.wrapped_app(environ, start_response_wrapper)
        response_blocks = []

        def next_response_block(response_iter):
            for block in response_iter:
                if xhtml_ok:
                    yield block
                elif environ['wsgixml.safexhtml.active']:
                    response_blocks.append(block)
                    yield ''
                else:
                    yield block

        def produce_final_output():
            if not xhtml_ok and environ['wsgixml.safexhtml.active']:
                xhtmlstr = ('').join(response_blocks)
                htmlstr = cStringIO.StringIO()
                parser = sax.make_parser(['Ft.Xml.Sax'])
                handler = SaxPrinter(HtmlPrinter(htmlstr, 'UTF-8'))
                parser.setContentHandler(handler)
                parser.setFeature(sax.handler.feature_external_pes, False)
                parser.parse(CreateInputSource(xhtmlstr))
                yield htmlstr.getvalue()

        return chain(iterwrapper(iterable, next_response_block), produce_final_output())