# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/apify/ip_api.py
# Compiled at: 2014-12-25 06:48:18
import sys, json, urllib2

def checkIPDetails(query=None):
    r""" 
                Method that checks if the given hash is stored in the md5crack.com website. An example of the json received:

                :param query:   Query to verify. It can be either a domain or an IPv4 address.

                :return:        Python structure for the Json received. The format is as follows:
                
                {
                        "as": "AS8560 1\u00261 Internet AG",
                        "city": "",
                        "country": "Germany",
                        "countryCode": "DE",
                        "isp": "1\u00261 Internet AG",
                        "lat": 51,
                        "lon": 9,
                        "org": "1\u00261 Internet AG",
                        "query": "217.160.251.126",
                        "region": "",
                        "regionName": "",
                        "status": "success",
                        "timezone": "",
                        "zip": ""
                }
        """
    apiURL = 'http://ip-api.com/json/' + query
    data = urllib2.urlopen(apiURL).read()
    jsonData = json.loads(data)
    return jsonData


if __name__ == '__main__':
    checkIPDetails(query=sys.argv[1])