# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: snapeda/queries.py
# Compiled at: 2017-10-26 10:58:44
from snapeda import models
import json, urllib, cfscrape
from connection import snapeda_connection
scraper = cfscrape.create_scraper()

class SnapedaQuery(object):
    baseurl = 'https://www.snapeda.com/api/v1/parts/'
    start = 0
    limit = 50

    def get(self, *args, **kwargs):
        self.args = [
         (
          'limit', self.limit)]
        for arg in kwargs:
            self.args.append((arg, kwargs[arg]))

        url = self.baseurl + self.path + '?' + urllib.urlencode(self.args)
        print url
        data = scraper.get(url).content
        return json.loads(data)

    def post(self, *args, **kwargs):
        url = self.baseurl + self.path
        print url
        data = scraper.post(url, data=kwargs).content
        print '--', url, kwargs
        return json.loads(data)


class PartsQuery(SnapedaQuery):
    path = 'search'

    def get(self, pattern):
        self.json = SnapedaQuery.get(self, q=pattern)
        return self.json

    def pages(self):
        list = []
        for item in self.json['pages']:
            list.append(models.SearchPage(item))

        return list

    def message(self):
        return self.json['message']

    def error(self):
        return self.json['error']

    def hits(self):
        return self.json['hits']

    def type(self):
        return self.json['type']

    def results(self):
        list = []
        for item in self.json['results']:
            list.append(models.SearchResult(item))

        return list


class DownloadQuery(SnapedaQuery):
    path = 'download'

    def get(self, part_number, manufacturer, uniqueid, has_symbol, has_footprint):
        if snapeda_connection.token == '':
            snapeda_connection.connect()
        self.json = SnapedaQuery.post(self, part_number=part_number, manufacturer=manufacturer, uniqueid=uniqueid, has_symbol=has_symbol, has_footprint=has_footprint, token=snapeda_connection.token, format='kicad')
        if self.json['status'] == 'not_logged_in':
            snapeda_connection.connect()
            self.json = SnapedaQuery.post(self, part_number=part_number, manufacturer=manufacturer, uniqueid=uniqueid, has_symbol=has_symbol, has_footprint=has_footprint, token=snapeda_connection.token, format='kicad')
        return self.json

    def url(self):
        return self.json['url']

    def status(self):
        return self.json['status']

    def error(self):
        return self.json['error']