# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\ultrasignup.py
# Compiled at: 2020-01-13 13:07:07
# Size of source mod 2**32: 14482 bytes
"""
ultrasignup - access methods for ultrasignup.com
===================================================
"""
import argparse, os.path, urllib.request, urllib.parse, urllib.error, unicodedata, logging, json
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
import httplib2
from loutilities import timeu
from loutilities import csvu
from loutilities import renderrun as render
from running import accessError, parameterError
ULTRASIGNUP_URL = 'http://ultrasignup.com'
RESULTS_SEARCH = 'service/events.svc/history/{fname}/{lname}'
HTTPTIMEOUT = 10
MPERMILE = 1609.344
tindate = timeu.asctime('%m/%d/%Y %I:%M:%S %p')
toutdate = timeu.asctime('%Y-%m-%d')

def racenameanddist(eventname):
    """
    get race name and distance 
    
    :param eventname: eventname from untrasignup.com
    :rtype: racename, distmiles, distkm
    """
    racetext = eventname.strip()
    fields = racetext.split('-')
    racename = racetext
    distfield = fields[(-1)].strip()
    dist = 0
    startunits = 0
    for digit in distfield:
        if not digit.isdigit():
            break
        dist *= 10
        dist += int(digit)
        startunits += 1

    units = distfield[startunits:].strip()
    if distfield == 'Marathon':
        distmiles = 26.21875
        distkm = distmiles * (MPERMILE / 1000)
    else:
        if distfield == '1/2 Marathon':
            distmiles = 13.109375
            distkm = distmiles * (MPERMILE / 1000)
        else:
            if units == 'K':
                distkm = dist
                distmiles = dist * 1000 / MPERMILE
            else:
                if units == 'Miler':
                    if dist == 13:
                        distmiles = 13.109375
                    else:
                        if dist == 26:
                            distmiles = 26.21875
                        else:
                            distmiles = dist
                    distkm = distmiles * (MPERMILE / 1000)
                else:
                    distmiles = None
                    distkm = None
    return (
     racename, distmiles, distkm)


def racenameanddur(eventname):
    """
    get race name and duration 
    
    :param eventname: eventname from untrasignup.com
    :rtype: racename, duration
    """
    racetext = eventname.strip()
    fields = racetext.split('-')
    racename = racetext
    durfield = fields[(-1)].strip()
    dur = 0
    startunits = 0
    for digit in durfield:
        if not digit.isdigit():
            break
        dur *= 10
        dur += int(digit)
        startunits += 1

    units = durfield[startunits:]
    if units == 'hrs':
        duration = dur
    else:
        duration = None
    return (racename, duration)


class UltraSignupResult:
    __doc__ = '\n    holds result from ultrasignup.com\n    \n    :param ranking: ultra ranking achieved during race\n    :param oaplace: overall place\n    :param genplace: gender place\n    :param age: age on race day\n    :param gender: gender\n    :param racetime: finishing time h:mm:ss\n    :param racedate: date of race yyyy-mm-dd\n    :param raceloc: location of race\n    :param racename: name of race\n    :param distmiles: distance in miles\n    :param distkm: distance in kilometers\n    '
    us_event_attrs = 'runner_rank,place,gender_place,age,time,eventdate,city,state'.split(',')
    attrs = 'ranking,oaplace,genplace,age,racetime,racedate,racecity,racestate,racename,distmiles,distkm,gender'.split(',')

    def __init__(self, ranking=None, oaplace=None, genplace=None, age=None, gender=None, racetime=None, racedate=None, raceloc=None, racename=None, distmiles=None, distkm=None):
        self.ranking = ranking
        self.oaplace = oaplace
        self.genplace = genplace
        self.age = age
        self.gender = gender
        self.racetime = racetime
        self.racedate = racedate
        self.raceloc = raceloc
        self.racename = racename
        self.distmiles = distmiles
        self.distkm = distkm

    def __repr__(self):
        reprval = '{}('.format(self.__class__)
        for attr in self.attrs:
            reprval += '{}={},'.format(attr, getattr(self, attr))

        reprval = reprval[:-1]
        reprval += ')'
        return reprval

    def set(self, attrvals):
        """
        set attributes based on list of attr,val pairs
        
        :param attrvals: [(attr,val),...]
        """
        for attr, inval in attrvals:
            val = csvu.str2num(inval)
            if attr in ('racedate', ):
                val = toutdate.epoch2asc(tindate.asc2epoch(val))
            setattr(self, attr, val)


class UltraSignup:
    __doc__ = '\n    access methods for ultrasignup.com\n    '

    def __init__(self, debug=False):
        """
        initialize http 
        """
        self.http = httplib2.Http(timeout=HTTPTIMEOUT)
        self.log = logging.getLogger('running.ultrasignup')
        self.setdebug(debug)
        self.urlcount = 0

    def setdebug(self, debugval):
        """
        set debugging attribute for this class
        
        :param debugval: set to True to enable debugging
        """
        if not debugval:
            level = logging.INFO
        else:
            level = logging.DEBUG
        self.log.setLevel(level)

    def geturlcount(self):
        """
        each time a url is retrieved, this counter is bumped
        
        :rtype: integer, number of url's retrieved
        """
        return self.urlcount

    def listresults(self, fname, lname, **filt):
        """
        return results which match an athlete's name
        
        :param fname: first name of athlete
        :param lname: last name of athlete
        :param **filt: keyword parameters to filter with
        :rtype: list of ultrasignup Race dicts
        """
        races = []
        data = self._get(RESULTS_SEARCH.format(fname=(urllib.parse.quote(fname)),
          lname=(urllib.parse.quote(lname))))
        content = json.loads(data)
        results = []
        for runner in content:
            usresults = runner['Results']
            gender = runner['Gender']
            for usresult in usresults:
                if usresult['status'] != 1:
                    pass
                else:
                    vals = []
                    for a in UltraSignupResult.us_event_attrs:
                        vals.append(usresult[a])

                    result = UltraSignupResult()
                    result.set(list(zip(UltraSignupResult.attrs, vals)))
                    result.racename, result.distmiles, result.distkm = racenameanddist(usresult['eventname'])
                    if result.distmiles == None:
                        result.racename, duration = racenameanddur(usresult['eventname'])
                        if duration is None:
                            pass
                        else:
                            result.distmiles = result.racetime
                            result.distkm = result.distmiles * (MPERMILE / 1000)
                            result.racetime = render.rendertime(duration * 60 * 60.0, 0)
                    result.gender = gender
                    results.append(result)

        def _checkfilter(check):
            for key in filt:
                if not hasattr(check, key) or getattr(check, key) != filt[key]:
                    return False

            return True

        results = list(filter(_checkfilter, results))
        return results

    def _get(self, method, **params):
        """
        get method for ultrasignup access
        
        :param method: ultrasignup method to call
        :param **params: parameters for the method
        """
        body = urllib.parse.urlencode(params)
        url = '{}/{}?{}'.format(ULTRASIGNUP_URL, method, body)
        retries = 10
        while retries > 0:
            retries -= 1
            try:
                self.log.debug(url)
                resp, content = self.http.request(url)
                self.urlcount += 1
                break
            except Exception as e:
                if retries == 0:
                    self.log.info('{} requests attempted'.format(self.geturlcount()))
                    self.log.error('http request failure, retries exceeded: {0}'.format(e))
                    raise
                self.log.warning('http request failure: {0}'.format(e))

        if resp.status != 200:
            raise accessError('URL response status = {0}'.format(resp.status))
        return content


def main():
    descr = '\n    unit test for ultrasignup.py\n    '
    parser = argparse.ArgumentParser(description=descr, formatter_class=(argparse.RawDescriptionHelpFormatter), version=('{0} {1}'.format('running', version.__version__)))
    args = parser.parse_args()


if __name__ == '__main__':
    main()