# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\strava.py
# Compiled at: 2020-01-15 16:12:19
# Size of source mod 2**32: 16841 bytes
"""
strava - access methods for strava.com
===================================================
"""
import argparse, json, time, logging
from tempfile import NamedTemporaryFile
import sys, os.path
from collections import OrderedDict, defaultdict
import requests
from running.running import version
from loutilities import apikey
from loutilities import timeu
from loutilities.csvwt import record2csv
from loutilities.csvu import unicode2ascii
stravatime = timeu.asctime('%Y-%m-%dT%H:%M:%SZ')
KMPERMILE = 1.609344
DATEFIELD = 'start_date'
xworkout_type = {None:'default', 
 0:'default', 
 1:'race', 
 2:'long run', 
 3:'workout', 
 10:'default', 
 11:'race', 
 12:'workout'}
workout_type = defaultdict((lambda : 'unknown'), **xworkout_type)

def dist2miles(distance):
    """
    convert distance to miles for distance returned from strava (meters)
    
    :param distance: distance field from strava
    :rtype: float - number of miles represented by the distance field
    """
    mpermile = KMPERMILE * 1000
    distmiles = distance / mpermile
    return distmiles


class Strava:
    __doc__ = '\n    access methods for Strava.com\n\n    :param cachefilename: name of cache file\n    '

    def __init__(self, clubactivitycachefilename=None, debug=False, key=None):
        """
        initialize 
        """
        if not key:
            ak = apikey.ApiKey('Lou King', 'running')
            try:
                user = ak.getkey('stravauser')
            except apikey.unknownKey:
                raise parameterError("'stravauser' needs to be configured using apikey")

        else:
            user = key
        self.user = user
        if debug:
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger('requests.packages.urllib3')
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
        self.clubactivitycache = {}
        self.clubactivitycachefilename = clubactivitycachefilename
        if self.clubactivitycachefilename:
            if os.path.isfile(clubactivitycachefilename):
                with open(clubactivitycachefilename, 'r') as (clubactivitycachefile):
                    for line in clubactivitycachefile:
                        activity = json.loads(line)
                        id = activity['id']
                        if id not in self.clubactivitycache:
                            self.clubactivitycache[id] = activity

        self.clubactivitycachesize = len(self.clubactivitycache)
        self.clubactivitycacheadded = 0

    def close(self):
        """
        close the connection when we're done, and save the cache
        """
        if self.clubactivitycachefilename:
            if self.clubactivitycacheadded > 0:
                cachedir = os.path.dirname(os.path.abspath(self.clubactivitycachefilename))
                with NamedTemporaryFile(mode='w', suffix='.stravacache', delete=False, dir=cachedir) as (tempcache):
                    tempclubactivitycachefilename = tempcache.name
                    for id in self.clubactivitycache:
                        tempcache.write('{}\n'.format(json.dumps(self.clubactivitycache[id])))

                try:
                    os.rename(tempclubactivitycachefilename, self.clubactivitycachefilename)
                except OSError:
                    os.remove(self.clubactivitycachefilename)
                    os.rename(tempclubactivitycachefilename, self.clubactivitycachefilename)

    def getathleteclubs(self):
        """
        retrieve current athlete's clubs
        """
        url = 'https://www.strava.com/api/v3/athlete/clubs'
        payload = {'access_token': self.user}
        r = requests.get(url, params=payload)
        r.raise_for_status()
        return r.json()

    def getclubdetails(self, clubid):
        """
        retrieve club information

        :param clubid: strava id for club
        """
        url = 'https://www.strava.com/api/v3/clubs/{}'.format(clubid)
        payload = {'access_token': self.user}
        r = requests.get(url, params=payload)
        r.raise_for_status()
        return r.json()

    def getclubactivities(self, clubid, before=None, after=None, perpage=200, maxactivities=None, **filters):
        """
        retrieve activities for a club

        :param clubid: strava id for club
        :param before: epoch time activities should be before
        :param after: epoch time activities should be after
        :param perpage: (debug) how many activities per request, max 200 per strava api docs
        :param maxactivities: (debug) max number of activities to return, None means all
        :param filters: additional filters to compare against returned activities {'field1':value, 'field2':[list,of,values]}
        """
        url = 'https://www.strava.com/api/v3/clubs/{}/activities'.format(clubid)
        if not before:
            before = int(time.time())
        payload = {'access_token':self.user, 
         'per_page':perpage}
        payload['page'] = 1
        activities = []
        more = True
        while more:
            r = requests.get(url, params=payload)
            r.raise_for_status()
            theseactivities = r.json()
            if len(theseactivities) > 0:
                earliestactivity = theseactivities[(-1)]
                earliesttime = stravatime.asc2epoch(earliestactivity[DATEFIELD])
                if after:
                    if earliesttime < after:
                        more = False
                        while earliesttime < after:
                            theseactivities.pop()
                            if len(theseactivities) == 0:
                                break
                            earliestactivity = theseactivities[(-1)]
                            earliesttime = stravatime.asc2epoch(earliestactivity[DATEFIELD])

            if len(theseactivities) > 0:
                activities += theseactivities
                payload['page'] += 1
            else:
                more = False
            if maxactivities and len(activities) >= maxactivities:
                more = False
                activities = activities[:maxactivities]

        for activity in activities:
            id = activity['id']
            if id not in self.clubactivitycache:
                self.clubactivitycache[id] = activity
                self.clubactivitycacheadded += 1

        self.clubactivitycachesize = len(self.clubactivitycache)
        return activities

    def getathleteactivities(self, athlete, after=None, perpage=200, maxactivities=None, **filters):
        """
        This doesn't work. Why does strava not allow viewing other athlete data?
        """
        url = 'https://www.strava.com/api/v3/athletes/{}/activities'.format(athlete)
        payload = {'access_token': self.user}
        r = requests.get(url, params=payload)
        r.raise_for_status()
        return r.json()

    def clubactivitycache2csv(self, mapping=None, outfile=None):
        """
        dump the club activity cache to a csv file

       :param mapping: OrderedDict {'outfield1':'infield1', 'outfield2':outfunction(cacherecord), ...} or ['inoutfield1', 'inoutfield2', ...]
       :param outfile: optional output file
       :rtype: lines from output file
           """
        if not mapping:
            mapping = OrderedDict([
             ('workout_id', 'id'),
             ('start_date', 'start_date_local'),
             (
              'name', lambda rec: '{} {}'.format(unicode2ascii(rec['athlete']['firstname']), unicode2ascii(rec['athlete']['lastname']))),
             (
              'fname', lambda rec: '{} {}'.format(unicode2ascii(rec['athlete']['firstname']))),
             (
              'lname', lambda rec: '{} {}'.format(unicode2ascii(rec['athlete']['lastname']))),
             (
              'gender', lambda rec: '{} {}'.format(unicode2ascii(rec['athlete']['sex']))),
             ('type', 'type'),
             (
              'workout_type', lambda rec: workout_type[rec['workout_type']]),
             (
              'activity_name', lambda rec: unicode2ascii(rec['name'])),
             ('distance(m)', 'distance'),
             ('time(s)', 'elapsed_time')])
        activities = list(self.clubactivitycache.values())
        csvrecords = record2csv(activities, mapping, outfile=outfile)
        return csvrecords


def updatestravaclubactivitycache():
    """
    script to update the strava club activity cache

    usage: updatestravaclubactivitycache [-h] [-v] cachefile clubname

        script to update the strava club activity cache

    positional arguments:
      cachefile      pathname of file in which cache is saved
      clubname       full name of club as known to strava

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  show program's version number and exit
    """
    descr = '\n    script to update the strava club activity cache\n    '
    parser = argparse.ArgumentParser(description=descr, formatter_class=(argparse.RawDescriptionHelpFormatter), version=('{0} {1}'.format('running', version.__version__)))
    parser.add_argument('cachefile', help='pathname of file in which cache is saved')
    parser.add_argument('clubname', help='full name of club as known to strava')
    parser.add_argument('--configfile', help='optional configuration filename', default=None)
    args = parser.parse_args()
    print('Updating Strava club activity cache for "{}"'.format(args.clubname))
    if args.configfile:
        from loutilities.configparser import getitems
        appconfig = getitems(args.configfile, 'app')
        stravakey = appconfig['STRAVAKEY']
    else:
        stravakey = None
    ss = Strava((args.cachefile), key=stravakey)
    clubs = ss.getathleteclubs()
    clubid = None
    for club in clubs:
        if club['name'] == args.clubname:
            clubid = club['id']
            break

    if not clubid:
        sys.exit('ERROR: club "{}" not found'.format(args.clubname))
    activities = ss.getclubactivities(clubid)
    numadded = ss.clubactivitycacheadded
    cachesize = ss.clubactivitycachesize
    ss.close()
    print('   update complete:')
    print('      {} activities received from Strava'.format(len(activities)))
    print('      added {} of these to cache'.format(numadded))
    print('      new cache size = {}'.format(cachesize))


def main():
    descr = '\n    unit test for strava.py\n    '
    parser = argparse.ArgumentParser(description=descr, formatter_class=(argparse.RawDescriptionHelpFormatter), version=('{0} {1}'.format('running', version.__version__)))
    args = parser.parse_args()


if __name__ == '__main__':
    main()