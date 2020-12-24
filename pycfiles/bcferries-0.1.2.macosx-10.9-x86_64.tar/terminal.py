# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yasyf/.virtualenvs/bcferries/lib/python2.7/site-packages/bcferries/terminal.py
# Compiled at: 2014-12-29 06:02:22
from abstract import BCFerriesAbstractObject
from decorators import cacheable, fuzzy, lazy_cache
import re, dateutil.parser, datetime
from route import BCFerriesRoute

class BCFerriesTerminal(BCFerriesAbstractObject):

    def __init__(self, name, url, api):
        super(BCFerriesTerminal, self).__init__(self)
        self.name = name
        self.__url = url
        self._api = api
        self._register_properties(['updated_at', 'routes', 'location'])

    @cacheable
    def updated_at(self):
        page = self._api.get_page(self.__url)
        updated = page.find_by_selector('div.conditions > div.white-small-text')[0]
        time = re.match('Conditions as at (.*)', updated.text.strip()).group(1)
        return dateutil.parser.parse(time)

    @fuzzy
    @cacheable
    def routes(self):
        page = self._api.get_page(self.__url)
        divs = page.find_by_selector('div.ferry_name > div.td')
        return {x.text:BCFerriesRoute(self._api, page, i) for i, x in enumerate(divs)}

    @cacheable
    def route(self, name):
        return self.routes()[name]

    @cacheable
    def next_crossing(self):
        next_crossings = [ x.next_crossing() for x in self.routes().values() ]
        next_crossings = [ x for x in next_crossings if x ]
        if next_crossings:
            return min(next_crossings, key=lambda x: x.time - datetime.datetime.now())

    @lazy_cache
    def location(self):
        lat_lon = self._api.geocode(('{} BC Ferry Terminal').format(self.name))
        return self._api.reverse(lat_lon[1], exactly_one=True)