# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\runningaheadresults.py
# Compiled at: 2020-02-26 14:48:04
# Size of source mod 2**32: 15840 bytes
"""
runningaheadresults - manage race results data from runningahead
===================================================================

Usage::
    runningaheadresults.py [-h] [-v] [-b BEGINDATE] [-e ENDDATE]
                                     searchfile outfile
    
        collect race results from runningahead
    
        searchfile must have at least the following headings:
    
            * GivenName - first name
            * FamilyName - last name
            * Gender - Male or Female (or M or F)
            * DOB - date of birth in yyyy-mm-dd format
            * City - city of residence [optional]
            * State - state of residence [optional]
    
    
    positional arguments:
      searchfile            file with names, genders and birth dates of athletes
                            to search for
      outfile               output file contains race results
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -b BEGINDATE, --begindate BEGINDATE
                            choose races between begindate and enddate, yyyy-mm-dd
      -e ENDDATE, --enddate ENDDATE
                            choose races between begindate and enddate, yyyy-mm-dd
                        
"""
import argparse, csv, datetime, time, logging
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
log = logging.getLogger('running.runningahead')
log.setLevel(logging.DEBUG)
from loutilities import timeu
from loutilities import csvu
from runningclub import agegrade
from runningclub import render
from .runningahead import FIELD
from running.running import version, runningahead
ag = agegrade.AgeGrade()

class invalidParameter(Exception):
    pass


fdate = timeu.asctime('%Y-%m-%d')
METERSPERMILE = 1609.344

def collect(searchfile, outfile, begindate, enddate):
    """
    collect race results from runningahead
    
    :param searchfile: path to file containing names, genders, birth dates to search for
    :param outfile: output file path
    :param begindate: epoch time - choose races between begindate and enddate
    :param enddate: epoch time - choose races between begindate and enddate
    """
    outfilehdr = 'GivenName,FamilyName,name,DOB,Gender,race,date,age,miles,km,time'.split(',')
    _IN = open(searchfile, 'r', newline='')
    IN = csv.DictReader(_IN)
    _OUT = open(outfile, 'w', newline='')
    OUT = csv.DictWriter(_OUT, outfilehdr)
    OUT.writeheader()
    commonfields = 'GivenName,FamilyName,DOB,Gender'.split(',')
    ra = runningahead.RunningAhead()
    users = ra.listusers()
    rausers = []
    for user in users:
        rauser = ra.getuser(user['token'])
        rausers.append((user, rauser))

    dt_begindate = timeu.epoch2dt(begindate)
    a_begindate = fdate.dt2asc(dt_begindate)
    adj_begindate = datetime.datetime(dt_begindate.year, dt_begindate.month, dt_begindate.day, 0, 0, 0)
    e_begindate = timeu.dt2epoch(adj_begindate)
    dt_enddate = timeu.epoch2dt(enddate)
    a_enddate = fdate.dt2asc(dt_enddate)
    adj_enddate = datetime.datetime(dt_enddate.year, dt_enddate.month, dt_enddate.day, 23, 59, 59)
    e_enddate = timeu.dt2epoch(adj_enddate)
    start = time.time()
    today = timeu.epoch2dt(start)
    for runner in IN:
        fname, lname = runner['GivenName'], runner['FamilyName']
        membername = '{} {}'.format(fname, lname)
        log.debug('looking for {}'.format(membername))
        e_dob = fdate.asc2epoch(runner['DOB'])
        dt_dob = fdate.asc2dt(runner['DOB'])
        dob = runner['DOB']
        gender = runner['Gender'][0]
        foundmember = False
        for user, rauser in rausers:
            if not 'givenName' not in rauser:
                if 'birthDate' not in rauser:
                    continue
                givenName = rauser['givenName'] if 'givenName' in rauser else ''
                familyName = rauser['familyName'] if 'familyName' in rauser else ''
                rausername = '{} {}'.format(givenName, familyName)
                if rausername == membername and dt_dob == fdate.asc2dt(rauser['birthDate']):
                    foundmember = True
                    log.debug('found {}'.format(membername))
                    break

        if not foundmember:
            pass
        else:
            workouts = ra.listworkouts((user['token']), begindate=a_begindate, enddate=a_enddate, getfields=(list(FIELD['workout'].keys())))
            results = []
            if workouts:
                for wo in workouts:
                    if wo['workoutName'].lower() != 'race':
                        pass
                    else:
                        if 'duration' not in wo['details']:
                            pass
                        else:
                            thisdate = wo['date']
                            dt_thisdate = fdate.asc2dt(thisdate)
                            thisdist = runningahead.dist2meters(wo['details']['distance'])
                            thistime = wo['details']['duration']
                            thisrace = wo['course']['name'] if 'course' in wo else 'unknown'
                            if thistime == 0:
                                log.warning('{} has 0 time for {} {}'.format(membername, thisrace, thisdate))
                            else:
                                stat = {'GivenName':fname, 
                                 'FamilyName':lname,  'name':membername,  'DOB':dob, 
                                 'Gender':gender,  'race':thisrace,  'date':thisdate,  'age':timeu.age(dt_thisdate, dt_dob),  'miles':thisdist / METERSPERMILE, 
                                 'km':thisdist / 1000.0,  'time':render.rendertime(thistime, 0)}
                                results.append(stat)

            for result in results:
                e_racedate = fdate.asc2epoch(result['date'])
                if not e_racedate < begindate:
                    if e_racedate > enddate:
                        pass
                    else:
                        outrec = result
                        resulttime = result['time']
                        if resulttime[0] == ':':
                            resulttime = '0' + resulttime
                        while resulttime.count(':') < 2:
                            resulttime = '0:' + resulttime

                        outrec['time'] = resulttime
                        OUT.writerow(outrec)

    _OUT.close()
    _IN.close()
    finish = time.time()
    print('elapsed time (min) = {}'.format((finish - start) / 60))


class RunningAheadFileResult:
    __doc__ = '\n    holds result from runningahead file\n    \n    :param firstname: first name\n    :param lastname: last name\n    :param name: firstname lastname\n    :param dob: date of birth, datetime\n    :param gender: M or F\n    :param race: name of race\n    :param date: date of race, datetime\n    :param age: age on race day\n    :param miles: race distance, miles\n    :param km: race distance, kilometers\n    :param time: race time, seconds\n    '
    attrs = 'firstname,lastname,name,dob,gender,race,date,age,miles,km,time'.split(',')

    def __init__(self, firstname=None, lastname=None, name=None, dob=None, gender=None, race=None, date=None, age=None, miles=None, km=None, time=None):
        self.firstname = firstname
        self.lastname = lastname
        self.name = name
        self.dob = dob
        self.gender = gender
        self.race = race
        self.date = date
        self.age = age
        self.miles = miles
        self.km = km
        self.time = time

    def __repr__(self):
        reprval = '{}('.format(self.__class__)
        for attr in self.attrs:
            val = getattr(self, attr)
            if attr in ('dob', 'date'):
                val = fdate.dt2asc(val)
            reprval += '{}={},'.format(attr, val)

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
            setattr(self, attr, val)


class RunningAheadResultFile:
    __doc__ = '\n    represents file of runningahead results collected from runningahead\n    \n    TODO:: add write methods, and update :func:`collect` to use :class:`RunningAheadFileResult` class\n    '
    filehdr = 'GivenName,FamilyName,name,DOB,Gender,race,date,age,miles,km,time'.split(',')
    hdrtransform = dict(list(zip(filehdr, RunningAheadFileResult.attrs)))
    resultdates = 'dob,date'.split(',')

    def __init__(self, filename):
        self.filename = filename

    def open(self, mode='r'):
        """
        open runningahead result file
        
        :param mode: 'r' or 'w' -- TODO: support 'w'
        """
        if mode[0] not in 'r':
            raise invalidParameter('mode {} not currently supported'.format(mode))
        self._fh = open((self.filename), mode, newline='')
        if mode[0] == 'r':
            self._csv = csv.DictReader(self._fh)

    def close(self):
        """
        close runningahead result file
        """
        if hasattr(self, '_fh'):
            self._fh.close()
            delattr(self, '_fh')
            delattr(self, '_csv')

    def __next__(self):
        """
        get next :class:`RunningAheadFileResult`
        
        :rtype: :class:`RunningAheadFileResult`, or None when end of file reached
        """
        try:
            fresult = next(self._csv)
        except StopIteration:
            return
        else:
            aresultargs = {}
            for fattr in self.hdrtransform:
                aattr = self.hdrtransform[fattr]
                if aattr == 'gender':
                    aresultargs[aattr] = fresult[fattr][0]
                else:
                    if aattr in self.resultdates:
                        aresultargs[aattr] = fdate.asc2dt(fresult[fattr])
                    else:
                        aresultargs[aattr] = csvu.str2num(fresult[fattr])

            return RunningAheadFileResult(**aresultargs)


def main():
    descr = '\n    collect race results from runningahead\n    \n    searchfile must have at least the following headings:\n    \n        * GivenName - first name\n        * FamilyName - last name\n        * Gender - Male or Female (or M or F)\n        * DOB - date of birth in yyyy-mm-dd format\n        * City - city of residence [optional]\n        * State - state of residence [optional]\n    '
    parser = argparse.ArgumentParser(description=descr, formatter_class=(argparse.RawDescriptionHelpFormatter), version=('{0} {1}'.format('running', version.__version__)))
    parser.add_argument('searchfile', help='file with names, genders and birth dates of athletes to search for')
    parser.add_argument('outfile', help='output file contains race results')
    parser.add_argument('-b', '--begindate', help='choose races between begindate and enddate, yyyy-mm-dd', default=None)
    parser.add_argument('-e', '--enddate', help='choose races between begindate and enddate, yyyy-mm-dd', default=None)
    args = parser.parse_args()
    searchfile = args.searchfile
    outfile = args.outfile
    argtime = timeu.asctime('%Y-%m-%d')
    if args.begindate:
        begindate = argtime.asc2epoch(args.begindate)
    else:
        begindate = argtime.asc2epoch('1970-01-01')
    if args.enddate:
        enddate = argtime.asc2epoch(args.enddate)
    else:
        enddate = argtime.asc2epoch('2030-12-31')
    collect(searchfile, outfile, begindate, enddate)


if __name__ == '__main__':
    main()