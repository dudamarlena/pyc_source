# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/shouter/shouter.py
# Compiled at: 2018-03-24 13:07:44
# Size of source mod 2**32: 536 bytes
import urllib.parse, urllib.request, urllib.response
SHOUT_ENDPOINT = 'https://shout-app.tk/shouter'

class Shouter:

    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def shout(self, message: str) -> urllib.response:
        message = message.encode('UTF-8')
        query = 'apiToken={}&message={}'.format(self.api_token, urllib.parse.quote(message))
        url = '{}/shout?{}'.format(SHOUT_ENDPOINT, query)
        response = urllib.request.urlopen(url)
        return response