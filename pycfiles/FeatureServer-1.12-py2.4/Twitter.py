# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/FeatureServer/DataSource/Twitter.py
# Compiled at: 2008-01-01 03:15:59
__author__ = 'MetaCarta'
__copyright__ = 'Copyright (c) 2006-2008 MetaCarta'
__license__ = 'Clear BSD'
__version__ = '$Id: Twitter.py 412 2008-01-01 08:15:59Z crschmidt $'
from FeatureServer.DataSource import DataSource
from FeatureServer.Feature import Feature
import urllib, simplejson

class Twitter(DataSource):
    """Specialized datasource allowing read-only access to a given 
       username's location via the Twittervision API."""
    __module__ = __name__

    def __init__(self, name, username, **args):
        DataSource.__init__(self, name, **args)
        self.username = username

    def select(self, action):
        data = urllib.urlopen('http://api.twittervision.com/user/current_status/%s.json' % self.username).read()
        user_data = simplejson.loads(data)
        geom = {'type': 'Point', 'coordinates': [[user_data['location']['longitude'], user_data['location']['latitude']]]}
        f = Feature(int(user_data['id']), geom)
        return [f]