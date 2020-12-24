# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bf3stats\api.py
# Compiled at: 2012-02-28 15:17:15
import urllib, time, base64, hashlib, hmac
from bf3stats.utils import _to_str
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise ImportError, 'Unable to load a json library'

class API(object):
    """A python interface for the bf3stats.com API"""

    def __init__(self, base_url=None, plattform='pc', secret=None, ident=None):
        if base_url is None:
            self._base_url = 'http://api.bf3stats.com'
        else:
            self._base_url = base_url
        self._plattform = plattform
        if ident:
            self._ident = ident
        if secret:
            self._secret = secret
        return

    def _request(self, post_data, data_group, sign=False, plattform=None):
        """Access bfstats.com API via HTTP POST"""
        if plattform is None:
            plattform = self._plattform
        api_url = '%s/%s/%s/' % (self._base_url, plattform, data_group)
        if sign:
            post_data = self._sign(post_data)
        try:
            con = urllib.urlopen(api_url, urllib.urlencode(post_data))
            result = con.read()
            con.close()
            raw_data = json.loads(result)
        except IOError as err:
            raw_data = {'status': 'error', 'error': err}

        return objDict(raw_data)

    def _sign(self, data_dict):
        """Sign data for a signed request"""
        data = base64.urlsafe_b64encode(json.dumps(data_dict)).rstrip('=')
        sig = base64.urlsafe_b64encode(hmac.new(self._secret, msg=data, digestmod=hashlib.sha256).digest()).rstrip('=')
        return {'data': data, 'sig': sig}

    def playerlist(self, players):
        """Request a list of players"""
        pass

    def player(self, player_name, parts=None):
        """Request a player"""
        post_data = {'player': player_name, 
           'opt': parts}
        return self._request(post_data, data_group='player')

    def dogtags(self, player_name):
        """Request Player dogtags"""
        return self._request(post_data={'player': player_name}, data_group='dogtags')

    def onlinestats(self):
        """Count of online players"""
        return self._request(post_data={}, data_group='onlinestats', plattform='global')

    def playerupdate(self, player_name, data_group='playerupdate'):
        """Request a playerupdate. (signed request)

        bf3stats.com request the current data from EA for this player.
        If the player was not in bf3stats.com database, they do automatically a lookup and add the player.

        Note: Clock should not have more than 1 minute difference to current time.
        """
        post_data = {'ident': self._ident, 
           'time': int(time.time()), 
           'player': player_name}
        return self._request(post_data, data_group, sign=True)

    def playerlookup(self, player_name):
        """Lookup a player. (signed request)"""
        return self.playerupdate(player_name, data_group='playerlookup')

    def setupkey(self, client_ident, name):
        """Generate an individual client key for every installation"""
        post_data = {'ident': self._ident, 
           'time': int(time.time()), 
           'clientident': client_ident, 
           'name': name}
        return self._request(post_data, data_group='setupkey', plattform='global', sign=True)

    def getkey(self, client_ident):
        """"Get information about a existing client key or your own key."""
        post_data = {'ident': self._ident, 
           'time': int(time.time()), 
           'clientident': client_ident}
        return self._request(post_data, data_group='getkey', plattform='global', sign=True)


class objDict(object):
    """The recursive class for building and representing objects with."""

    def __init__(self, obj):
        for k, v in obj.iteritems():
            if isinstance(v, dict):
                setattr(self, _to_str(k).title(), objDict(v))
            else:
                setattr(self, k, v)

    def __getitem__(self, val):
        return self.__dict__[val]

    def __repr__(self):
        return '{%s}' % str((', ').join('%s : %s' % (k, repr(v)) for k, v in self.__dict__.iteritems()))