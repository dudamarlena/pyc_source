# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/wsgixml/serializer.py
# Compiled at: 2006-10-01 00:17:49
"""
Middleware for processing any XML response body to a DOM or Amara binding

Copyright 2006 Uche Ogbuji
Licensed under the Academic Free License version 3.0
"""
from itertools import chain
from util import iterwrapper

class domlette_response_proxy:

    def __init__(blocks):
        from Ft.Xml.Domlette import Parse
        self.root = Parse(('').join(blocks))

    def serialize():
        from cStringIO import StringIO
        output = StringIO()
        from Ft.Xml.Domlette import Print
        Print(self.root, stream=output)
        return output.getvalue()


class bindery_response_proxy:

    def __init__(blocks):
        import amara
        self.root = amara.parse(('').join(blocks))

    def serialize():
        return self.root.xml()


class deserialize(object):
    """
    Middleware that deserializes any XML response body to a DOM or Amara binding
    """

    def __init__(self, app, response_proxy_class=bindery_response_proxy):
        self.wrapped_app = app

    def __call__(self, environ, start_response):

        def start_response_wrapper(status, response_headers, exc_info=None):
            environ['wsgixml.deserialize.active'] = False
            for (name, value) in response_headers:
                media_type = value.split(';')[0]
                if name.lower() == 'content-type' and (media_type.endswith('/xml') or media_type.find('/xml+') != -1):
                    environ['applyxslt.active'] = True

            start_response(status, response_headers, exc_info)

            def dummy_write(data):
                raise RuntimeError('deserialize does not support the deprecated write() callable in WSGI clients')

            return dummy_write

        iterable = self.wrapped_app(environ, start_response_wrapper)
        response_blocks = []

        def next_response_block(response_iter):
            for block in response_iter:
                if environ['wsgixml.deserialize.active']:
                    response_blocks.append(block)
                    yield ''
                else:
                    yield block

        def produce_final_output():
            if environ['wsgixml.deserialize.active']:
                response_proxy = response_proxy_class(response_blocks)
                environ['wsgixml.deserialize.object'] = response_proxy
            yield ''

        return chain(iterwrapper(iterable, next_response_block), produce_final_output())


class serialize(object):
    """
    Serializes response bodies processed by wsgixml.deserialize
    """

    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, environ, start_response):
        iterable = self.wrapped_app(environ, start_response)
        response_blocks = []

        def produce_final_output():
            if environ['wsgixml.deserialize.active']:
                response_proxy = environ['wsgixml.deserialize.object']
            yield response_proxy.serialize()

        return chain(iterable, produce_final_output())