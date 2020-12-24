# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/fusion/indexpage.py
# Compiled at: 2015-06-10 05:29:57
import pkg_resources
from py3o.fusion.log import logging
from twisted.web.template import Element, renderer
from twisted.web.resource import Resource
from twisted.web.template import flatten
from twisted.web.server import NOT_DONE_YET
from py3o.fusion.template import tloader

class IndexElement(Element):
    cssurls = [
     '/static/bootstrap/css/bootstrap.min.css',
     '/static/css/cover.css']
    loader = tloader('index.xml')
    header_loader = tloader('header.xml')
    scripts_loader = tloader('scripts.xml')

    @renderer
    def csslinks(self, request, tag):
        for cssurl in self.cssurls:
            yield tag.clone().fillSlots(cssurl=cssurl)

    @renderer
    def scripts(self, request, tag):
        return self.scripts_loader.load()

    @renderer
    def header(self, request, tag):
        return self.header_loader.load()

    @renderer
    def title(self, request, tag):
        return tag('py3o.fusion server')

    @renderer
    def version(self, request, tag):
        return tag(pkg_resources.get_distribution('py3o.fusion').version)


class RootPage(Resource):

    def flattened(self, output, request):
        request.finish()

    def render_GET(self, request):
        logging.info(('GET request from {}').format(request.getClientIP()))
        request.write('<!DOCTYPE html>\n')
        d = flatten(request, IndexElement(), request.write)
        d.addCallback(self.flattened, request)
        return NOT_DONE_YET