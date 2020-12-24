# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/haus/components/status.py
# Compiled at: 2008-11-12 23:57:47
""".. _HTTPStatusComponent:

``status`` -- HTTP Status Handlers
==================================

Provides standard handlers for various HTTP status responses.

"""
from pkg_resources import resource_filename
from haus.components.abstract import Component

class HTTPStatusComponent(Component):
    __module__ = __name__
    consumes = [
     'render_template']
    provides = ['status404', 'status405', 'status500']

    def __init__(self, wrk):
        config = wrk.config.get('status.templates', {})
        haus_resource = wrk.haus_resource
        self.template404 = config.get('status404', resource_filename(haus_resource, 'haus/html/status404.html'))
        self.template405 = config.get('status405', resource_filename(haus_resource, 'haus/html/status405.html'))
        self.template500 = config.get('status500', resource_filename(haus_resource, 'haus/html/status500.html'))
        self.layout = config.get('layout', wrk.pdfilename('html/_layouts/default.html'))
        wrk.functions['status404'] = self.status404
        wrk.functions['status405'] = self.status405
        wrk.functions['status500'] = self.status500

    def status404(self, environ, start_response):
        start_response('404 Not Found', [('Content-type', 'text/html')])
        render = environ['haus.functions']['render_view']
        return render(self.template404, {'layout': self.layout})

    def status405(self, environ, start_response):
        start_response('405 Method Not Supported', [('Content-type', 'text/html')])
        render = environ['haus.functions']['render_view']
        return render(self.template405, {'layout': self.layout})

    def status500(self, environ, start_response):
        start_response('500 An Error Occurred', [('Content-type', 'text/html')])
        render = environ['haus.functions']['render_view']
        return render(self.template500, {'layout': self.layout})