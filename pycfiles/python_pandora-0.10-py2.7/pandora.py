# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pandora/pandora.py
# Compiled at: 2013-07-04 08:22:35
import urllib2
from connection import PandoraConnection

def authenticated(f):

    def check_authentication(self, *args):
        if self.user is None:
            raise ValueError('User not yet authenticated')
        return f(self, *args)

    return check_authentication


class Pandora(object):
    current_station = None
    user = None
    backlog = []
    stations = []

    def __init__(self, connection=PandoraConnection()):
        self.connection = connection

    def authenticate(self, username, password):
        self.user = self.connection.authenticate_user(username, password)
        if self.user is not None:
            self.stations = self.user['stationListResult']['stations']
        return self.user is not None

    @authenticated
    def search(self, text):
        return self.connection.search(self.user, text)

    @authenticated
    def update_station_list(self):
        self.stations = self.connection.get_stations(self.user)['stations']

    @authenticated
    def get_genre_stations(self):
        return self.connection.get_genre_stations(self.user)

    @authenticated
    def get_station(self, station):
        return self.connection.get_station(self.user, station)

    @authenticated
    def delete_station(self, station):
        self.connection.delete_station(self.user, station)
        self.update_station_list()

    @authenticated
    def add_seed(self, station, music):
        return self.connection.add_seed(self.user, station, music)

    @authenticated
    def delete_seed(self, station, seed):
        self.connection.delete_seed(self.user, station, seed)

    @authenticated
    def add_feedback(self, station, track, is_positive_feedback=True):
        return self.connection.add_feedback(self.user, station, track, is_positive_feedback)

    @authenticated
    def delete_feedback(self, station, feedback):
        self.connection.delete_feedback(self.user, station, feedback)

    @authenticated
    def switch_station(self, station):
        self.backlog = []
        self.current_station = station
        self.backlog = self.connection.get_fragment(self.user, self.current_station) + self.backlog

    @authenticated
    def get_next_song(self):
        if self.current_station is None:
            raise ValueError('No station selected')
        if len(self.backlog) < 2:
            self.backlog = self.connection.get_fragment(self.user, self.current_station) + self.backlog
        return self.backlog.pop()


if __name__ == '__main__':
    import getpass
    pandora = Pandora()
    username = raw_input('Username: ')
    password = getpass.getpass()
    proxy = raw_input('Proxy: ')
    if proxy:
        proxy_support = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
    print 'Authenthicated: ' + str(pandora.authenticate(username, password))
    print 'users stations:'
    for station in pandora.stations:
        if station['isQuickMix']:
            quickmix = station
            print '\t' + station['stationName'] + '*'
        else:
            print '\t' + station['stationName']

    pandora.switch_station(quickmix)
    print 'next song from quickmix:'
    next = pandora.get_next_song()
    print next['artistName'] + ': ' + next['songName']
    print next['audioUrlMap']['highQuality']['audioUrl']