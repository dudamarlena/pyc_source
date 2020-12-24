# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattkoskela/Websites/venvs/temp/lib/python2.7/site-packages/trulia/stats.py
# Compiled at: 2014-06-29 18:26:04
"""
stats.py

This file contains an interface for Trulia's TruliaStats Library.

Documentation about Trulia's TruliaStats Library can be found here:
http://developer.trulia.com/docs/read/TruliaStats
"""
import requests, xmltodict

class TruliaStats(object):
    """
    The TruliaStats class is used to retrieve stats data from the Trulia API
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def get_city_stats(self, city, state, start_date, end_date, stat_type='all'):
        """This method returns an OrderedDict of all stats for a city"""
        url = 'http://api.trulia.com/webservices.php'
        payload = {'library': 'TruliaStats', 
           'function': 'getCityStats', 
           'city': city, 
           'state': state, 
           'startDate': start_date, 
           'endDate': end_date, 
           'statType': stat_type, 
           'apikey': self.api_key}
        xml = requests.get(url, params=payload)
        results = xmltodict.parse(xml.content)
        city_stats = results['TruliaWebServices']['response']['TruliaStats']
        return city_stats

    def get_county_stats(self, county, state, start_date, end_date, stat_type='all'):
        """This method returns an OrderedDict of all stats for a county"""
        url = 'http://api.trulia.com/webservices.php'
        payload = {'library': 'TruliaStats', 
           'function': 'getCountyStats', 
           'county': county, 
           'state': state, 
           'startDate': start_date, 
           'endDate': end_date, 
           'statType': stat_type, 
           'apikey': self.api_key}
        xml = requests.get(url, params=payload)
        results = xmltodict.parse(xml.content)
        county_stats = results['TruliaWebServices']['response']['TruliaStats']
        return county_stats

    def get_neighborhood_stats(self, neighborhood_id, start_date, end_date, stat_type='all'):
        """This method returns an OrderedDict of all stats for a neighborhood"""
        url = 'http://api.trulia.com/webservices.php'
        payload = {'library': 'TruliaStats', 
           'function': 'getNeighborhoodStats', 
           'neighborhoodId': neighborhood_id, 
           'startDate': start_date, 
           'endDate': end_date, 
           'statType': stat_type, 
           'apikey': self.api_key}
        xml = requests.get(url, params=payload)
        results = xmltodict.parse(xml.content)
        neighborhood_stats = results['TruliaWebServices']['response']['TruliaStats']
        return neighborhood_stats

    def get_state_stats(self, state, start_date, end_date, stat_type='all'):
        """This method returns an OrderedDict of all stats for a state"""
        url = 'http://api.trulia.com/webservices.php'
        payload = {'library': 'TruliaStats', 
           'function': 'getStateStats', 
           'state': state, 
           'startDate': start_date, 
           'endDate': end_date, 
           'statType': stat_type, 
           'apikey': self.api_key}
        xml = requests.get(url, params=payload)
        results = xmltodict.parse(xml.content)
        state_stats = results['TruliaWebServices']['response']['TruliaStats']
        return state_stats

    def get_zip_code_stats(self, zip_code, start_date, end_date, stat_type='all'):
        """This method returns an OrderedDict of all stats for a zip_code"""
        url = 'http://api.trulia.com/webservices.php'
        payload = {'library': 'TruliaStats', 
           'function': 'getZipCodeStats', 
           'zipCode': zip_code, 
           'startDate': start_date, 
           'endDate': end_date, 
           'statType': stat_type, 
           'apikey': self.api_key}
        xml = requests.get(url, params=payload)
        results = xmltodict.parse(xml.content)
        zip_code_stats = results['TruliaWebServices']['response']['TruliaStats']
        return zip_code_stats