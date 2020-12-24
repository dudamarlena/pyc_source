# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/CherrypyMako/mako_tool.py
# Compiled at: 2012-12-24 17:38:00
import cherrypy
from mako.lookup import TemplateLookup

class MakoHandler(cherrypy.dispatch.LateParamPageHandler):
    """Callable which sets response.body."""

    def __init__(self, template, next_handler):
        self.template = template
        self.next_handler = next_handler

    def __call__(self):
        env = globals().copy()
        env.update(self.next_handler())
        return self.template.render(**env)


class MakoLoader(object):

    def __init__(self):
        self.lookups = {}

    def __call__(self, filename, directories, module_directory=None, collection_size=-1):
        key = (
         tuple(directories), module_directory)
        try:
            lookup = self.lookups[key]
        except KeyError:
            lookup = TemplateLookup(directories=directories, module_directory=module_directory, collection_size=collection_size, input_encoding='utf8')
            self.lookups[key] = lookup

        cherrypy.request.lookup = lookup
        cherrypy.request.template = t = lookup.get_template(filename)
        cherrypy.request.handler = MakoHandler(t, cherrypy.request.handler)


def setup():
    cherrypy.tools.mako = cherrypy.Tool('on_start_resource', MakoLoader())