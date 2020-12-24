# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geocoord/locations_repo.py
# Compiled at: 2016-05-30 07:56:08
import requests, yaml
BASE_URL = 'https://raw.githubusercontent.com'
LOCATIONS_PATH = '/YujiAzama/locations/master/locations'
COMPLEMENTS_PATH = '/YujiAzama/locations/master/complements/%s'

class LocationsRepository(object):

    def yaml_to_object(self, yml):
        return yaml.load(yml)

    def find_path(self, city):
        city = city.lower()
        res = requests.get(BASE_URL + COMPLEMENTS_PATH % city[0])
        return self.yaml_to_object(res.text).get(city)['region']

    def get_cities(self, city):
        locations_path = self.find_path(city).split('.')
        path = ''
        locations_path[(len(locations_path) - 2)] += '.yaml'
        for i in range(0, len(locations_path) - 1):
            path += '/' + locations_path[i]

        res = requests.get(BASE_URL + LOCATIONS_PATH + path)
        body = self.yaml_to_object(res.text)
        return body[locations_path[(len(locations_path) - 1)]]