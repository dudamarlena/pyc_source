# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/apify/md5crack.py
# Compiled at: 2014-12-25 06:48:18
import sys, json, urllib2, i3visiotools.config_api_keys as config_api_keys

def checkIfCrackedInMD5crack(hash=None, api_key=None):
    """ 
                Method that checks if the given hash is stored in the md5crack.com website. An example of the json received:

                :param hash:    hash to verify.

                :return:        Python structure for the Json received.
        """
    if api_key == None:
        allKeys = config_api_keys.returnListOfAPIKeys()
        try:
            api_key = allKeys['md5crack']
        except:
            return {}

    apiURL = 'http://api.md5crack.com/crack/' + api_key + '/' + hash
    data = urllib2.urlopen(apiURL).read()
    if '"parsed":null' in data:
        data = data.replace('"parsed":null', '"parsed":""')
    jsonData = json.loads(data)
    return jsonData


if __name__ == '__main__':
    checkIfCrackedInMD5crack(hash=sys.argv[1])