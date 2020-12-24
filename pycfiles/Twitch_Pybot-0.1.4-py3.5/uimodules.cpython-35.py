# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/web/uimodules.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 1612 bytes
import tornado, pybot.globals as globals
from pybot.pybotextra import allFilters
import json

class Raffle(tornado.web.UIModule):

    def render(self):
        return self.render_string('templates/rafflemodule.html', data=globals.data)


class UserPoints(tornado.web.UIModule):

    def render(self, top=0):
        return self.render_string('templates/userpointsmodule.html', data=globals.data, top=top)


class Logs(tornado.web.UIModule):

    def render(self):
        return self.render_string('templates/logmodule.html', data=globals.data)


class Links(tornado.web.UIModule):

    def render(self, link=False):
        return self.render_string('templates/linksmodule.html', settings=globals.settings, data=globals.data, link=link)


class Filters(tornado.web.UIModule):

    def render(self):
        activeFilters = json.loads(globals.settings.config['filters']['activeFilters'])
        return self.render_string('templates/filtersmodule.html', data=globals.data, activeFilters=activeFilters, allfilters=allFilters())


class Chart(tornado.web.UIModule):

    def render(self, values=[], settings={}):
        values.append({'value': '25', 'color': '#F7464A', 'highlight': '#FF5A5E', 'label': 'test1'})
        values.append({'value': '75', 'color': '#ffffff', 'highlight': '#FF5A5E', 'label': 'test2'})
        return self.render_string('templates/chartmodule.html', values=values, settings=settings)