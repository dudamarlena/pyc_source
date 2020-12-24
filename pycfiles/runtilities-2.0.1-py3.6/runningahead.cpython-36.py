# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\runningahead.py
# Compiled at: 2020-01-13 13:07:06
# Size of source mod 2**32: 18067 bytes
"""
runningahead - access methods for runningahead.com
===================================================
"""
import pdb, argparse, os.path, logging, json
from tempfile import NamedTemporaryFile
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from loutilities import apikey
auth_url = 'https://www.runningahead.com/oauth2/authorize'
token_url = 'https://api.runningahead.com/oauth2/token'
FIELD = {}
FIELD['workout'] = {'eventtype':10, 
 'eventsubtype':11, 
 'date':12, 
 'distance':20, 
 'duration':21, 
 'coursename':22}
KMPERMILE = 1.609344

class accessError(Exception):
    pass


def dist2miles(distance):
    """
    convert distance to miles for distance returned from runningahead
    
    :param dist: distance field from runningahead
    :rtype: float - number of miles represented by the distance field
    """
    mpermile = KMPERMILE * 1000
    unit = distance['unit']
    if unit == 'mi':
        distmiles = distance['value']
    else:
        if unit == 'km':
            distmiles = distance['value'] / KMPERMILE
        else:
            if unit == 'm':
                distmiles = distance['value'] / mpermile
            else:
                raise parameterError('{0}: invalid unit returned for runningahead distance'.format(unit))
    return distmiles


def dist2meters(distance):
    """
    convert distance to meters for distance returned from runningahead
    
    :param dist: distance field from runningahead
    :rtype: float - number of meters represented by the distance field
    """
    mpermile = KMPERMILE * 1000
    unit = distance['unit']
    if unit == 'mi':
        distmeters = distance['value'] * mpermile
    else:
        if unit == 'km':
            distmeters = distance['value'] * 1000.0
        else:
            if unit == 'm':
                distmeters = distance['value']
            else:
                raise parameterError('{0}: invalid unit returned for runningahead distance'.format(unit))
    return distmeters


class RunningAhead:
    __doc__ = '\n    access methods for RunningAhead.com\n\n    :param membercachefilename: name of optional file to cache detailed member data\n    :param debug: set to True for debug logging of http requests, default False\n    :param key: ra key for oauth, if omitted retrieved from apikey\n    :param secret: ra secret for oauth, if omitted retrieved from apikey\n    '

    def __init__(self, membercachefilename=None, debug=False, key=None, secret=None):
        """
        initialize oauth authentication, and load member cache
        """
        if debug:
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger('requests.packages.urllib3')
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
        if not (key and secret):
            ak = apikey.ApiKey('Lou King', 'running')
            try:
                key = ak.getkey('ra')
                secret = ak.getkey('rasecret')
            except apikey.unknownKey:
                raise parameterError("'ra' and 'rasecret' keys needs to be configured using apikey")

        client = BackendApplicationClient(client_id=key)
        oauth = OAuth2Session(client=client)
        data = oauth.fetch_token(token_url='https://api.runningahead.com/oauth2/token', client_id=key, client_secret=secret)
        self.client_credentials = data['access_token']
        self.rasession = requests.Session()
        self.membercache = {}
        self.membercachefilename = membercachefilename
        if self.membercachefilename:
            if os.path.isfile(membercachefilename):
                with open(membercachefilename, 'r') as (membercachefile):
                    for line in membercachefile:
                        member = json.loads(line)
                        self.membercache[member['id']] = member

        self.membercacheupdated = False

    def close(self):
        """
        close the connection when we're done, and save the cache
        """
        self.rasession.close()
        if self.membercachefilename:
            if self.membercacheupdated:
                cachedir = os.path.dirname(os.path.abspath(self.membercachefilename))
                with NamedTemporaryFile(mode='w', suffix='.racache', delete=False, dir=cachedir) as (tempcache):
                    tempmembercachefilename = tempcache.name
                    for id in self.membercache:
                        tempcache.write('{}\n'.format(json.dumps(self.membercache[id])))

                cachemode = os.stat(self.membercachefilename).st_mode & 511
                os.chmod(tempmembercachefilename, cachemode)
                try:
                    os.rename(tempmembercachefilename, self.membercachefilename)
                except OSError:
                    os.remove(self.membercachefilename)
                    os.rename(tempmembercachefilename, self.membercachefilename)

    def listusers(self):
        """
        return users accessible to this application
        """
        BITESIZE = 100
        offset = 0
        users = []
        while 1:
            data = self._raget('users', (self.client_credentials),
              limit=BITESIZE,
              offset=offset)
            if data['numEntries'] == 0:
                break
            theseusers = data['entries']
            users += theseusers
            offset += BITESIZE
            if offset >= data['numEntries']:
                break

        return users

    def listactivitytypes(self, accesstoken):
        """
        return activity types for this user

        :param accesstoken: access_token to use for api call
        """
        data = self._raget('logs/me/activity_types', accesstoken)
        activity_types = data['entries']
        return activity_types

    def listworkouts(self, accesstoken, begindate=None, enddate=None, getfields=None):
        """
        return run workouts within date range
        
        :param accesstoken: access_token to use for api call
        :param begindate: date in format yyyy-mm-dd
        :param enddate: date in format yyyy-mm-dd
        :param getfields: list of fields to get in response.  See runningahead.FIELD['workout'].keys() for valid codes
        """
        if getfields:
            lpfield = []
            for f in getfields:
                lpfield.append(str(FIELD['workout'][f]))

            fields = ','.join(lpfield)
        else:
            optargs = {}
            optargs['activityID'] = 10
            filters = []
            if begindate:
                filters.append(['date', 'ge', begindate])
            if enddate:
                filters.append(['date', 'le', enddate])
            if getfields:
                optargs['fields'] = fields
            if filters:
                optargs['filters'] = json.dumps(filters)
        BITESIZE = 100
        offset = 0
        workouts = []
        while 1:
            data = (self._raget)('logs/me/workouts', accesstoken, limit=BITESIZE, 
             offset=offset, **optargs)
            if data['numEntries'] == 0:
                break
            theseworkouts = data['entries']
            workouts += theseworkouts
            offset += BITESIZE
            if offset >= data['numEntries']:
                break

        return workouts

    def getworkout(self, accesstoken, id):
        """
        return workout for specified id
        
        :param accesstoken: access_token to use for api call
        :param id: id retrieved from listworkouts for desireed workout
        """
        data = self._raget('logs/me/workouts/{0}'.format(id), accesstoken)
        workout = data['workout']
        return workout

    def getuser(self, accesstoken):
        """
        return workout for specified id
        
        :param accesstoken: access_token to use for api call
        """
        data = self._raget('users/me', accesstoken)
        rauser = data['user']
        user = {}
        for raf in rauser:
            if isinstance(rauser[raf], dict):
                for f in rauser[raf]:
                    user[f] = rauser[raf][f]

            else:
                user[raf] = rauser[raf]

        return user

    def listmemberships(self, club, accesstoken, **filters):
        """
        return list of club memberships
        
        :param club: RA slug name of club
        :param accesstoken: access token for a priviledged viewer for this club
        :param filters: see http://api.runningahead.com/docs/club/list_members for valid filters
        :rtype: list of memberships
        """
        method = 'clubs/{}/members'.format(club)
        data = (self._raget)(method, accesstoken, **filters)
        memberships = data['entries']
        return memberships

    def getmember(self, club, id, accesstoken, update=False):
        """
        return list of club members
        
        :param club: RA slug name of club
        :param id: id of member
        :param accesstoken: access token for a priviledged viewer
        :param update: update based on latest information from RA
        :rtype: member record
        """
        if update or id not in self.membercache:
            method = 'clubs/{}/members/{}'.format(club, id)
            data = self._raget(method, accesstoken)
            member = data['member']
            self.membercache[id] = member
            self.membercacheupdated = True
        else:
            member = self.membercache[id]
        return member

    def listmembershiptypes(self, club, accesstoken):
        """
        return list of club membership types
        
        :param club: RA slug name of club
        :param accesstoken: access token for a priviledged viewer for this club
        :rtype: list of memberships
        """
        method = 'clubs/{}/memberships'.format(club)
        data = self._raget(method, accesstoken)
        membershiptypes = data['entries']
        return membershiptypes

    def _raget(self, method, accesstoken, **payload):
        """
        get method for runningahead access
        
        :param method: runningahead method to call
        :param accesstoken: access_token to use for api call
        :param **payload: parameters for the method
        """
        payload['access_token'] = accesstoken
        url = 'https://api.runningahead.com/rest/{0}'.format(method)
        r = self.rasession.get(url, params=payload)
        if r.status_code != 200:
            raise accessError('HTTP response code={}, url={}'.format(r.status_code, r.url))
        content = r.json()
        if content['code'] != 0:
            raise accessError('RA response code={}, url={}'.format(content['code'], r.url))
        data = content['data']
        return data


def main():
    descr = '\n    unit test for runningahead.py\n    '
    parser = argparse.ArgumentParser(description=descr, formatter_class=(argparse.RawDescriptionHelpFormatter), version=('{0} {1}'.format('running', version.__version__)))
    args = parser.parse_args()


if __name__ == '__main__':
    main()