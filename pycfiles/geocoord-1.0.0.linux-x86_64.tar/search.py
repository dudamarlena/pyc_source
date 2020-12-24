# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geocoord/search.py
# Compiled at: 2016-05-30 08:10:44
from geocoord import locations_repo as lr

class Search(object):

    def __init__(self):
        self.repo = lr.LocationsRepository()

    def find_coord_by_city(self, keyword):
        return self.repo.get_cities(keyword)

    def find_city_by_coord(self, lat, lon):
        pass


if __name__ == '__main__':
    search = Search()
    print search.find_coord_by_city('tokyo')