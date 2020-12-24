# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/shodan/wps.py
# Compiled at: 2013-12-11 13:12:06
"""
WiFi Positioning System

Wrappers around the SkyHook and Google Locations APIs to resolve
wireless routers' MAC addresses (BSSID) to physical locations.
"""
try:
    from json import dumps, loads
except:
    from simplejson import dumps, loads

try:
    from urllib2 import Request, urlopen
    from urllib import urlencode
except:
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode

class Skyhook:
    """Not yet ready for production, use the GoogleLocation class instead."""

    def __init__(self, username='api', realm='shodan'):
        self.username = username
        self.realm = realm
        self.url = 'https://api.skyhookwireless.com/wps2/location'

    def locate(self, mac):
        mac = mac.replace(':', '')
        data = "<?xml version='1.0'?>  \n        <LocationRQ xmlns='http://skyhookwireless.com/wps/2005' version='2.6' street-address-lookup='full'>  \n          <authentication version='2.0'>  \n            <simple>  \n              <username>%s</username>  \n              <realm>%s</realm>  \n            </simple>  \n          </authentication>  \n          <access-point>  \n            <mac>%s</mac>  \n            <signal-strength>-50</signal-strength>  \n          </access-point>  \n        </LocationRQ>" % (self.username, self.realm, mac)
        request = Request(url=self.url, data=data, headers={'Content-type': 'text/xml'})
        response = urlopen(request)
        result = response.read()
        return result


class GoogleLocation:

    def __init__(self):
        self.url = 'http://www.google.com/loc/json'

    def locate(self, mac):
        data = {'version': '1.1.0', 
           'request_address': True, 
           'wifi_towers': [
                         {'mac_address': mac, 
                            'ssid': 'g', 
                            'signal_strength': -72}]}
        response = urlopen(self.url, dumps(data))
        data = response.read()
        return loads(data)