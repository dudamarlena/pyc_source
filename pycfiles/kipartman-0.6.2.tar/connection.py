# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: snapeda/connection.py
# Compiled at: 2018-04-25 05:32:06
import json, urllib, cfscrape
from configuration import configuration
scraper = cfscrape.create_scraper()

class SnapedaConnectionException(Exception):

    def __init__(self, error):
        self.error = error


class SnapedaConnection(object):
    baseurl = 'https://www.snapeda.com/account/api-login/'

    def __init__(self):
        self.token = ''

    def connect(self, user=configuration.snapeda_user, password=configuration.snapeda_password):
        self.url = self.baseurl
        try:
            data = scraper.post(self.url, data={'username': user, 'password': password}).content
            content = json.loads(data)
        except BaseException as e:
            raise SnapedaConnectionException(e)

        if content['status'] != 'logged_in':
            raise SnapedaConnectionException('Incorrect user name or password')
        self.token = content['token']
        return content['token']


snapeda_connection = SnapedaConnection()