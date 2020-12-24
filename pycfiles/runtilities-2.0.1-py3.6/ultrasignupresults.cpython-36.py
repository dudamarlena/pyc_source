# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\ultrasignupresults.py
# Compiled at: 2020-02-26 14:48:04
# Size of source mod 2**32: 15182 bytes
"""
ultrasignupresults - manage race results data from ultrasignup
===================================================================

Usage::
    ultrasignupresults.py [-h] [-v] [-b BEGINDATE] [-e ENDDATE]
                                     searchfile outfile
    
        collect race results from ultrasignup
    
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
import argparse, csv, datetime, time
from loutilities import timeu
from loutilities import csvu
from runningclub import agegrade
from running.running import version, ultrasignup
ag = agegrade.AgeGrade()

class invalidParameter(Exception):
    pass


ftime = timeu.asctime('%Y-%m-%d')

def collect(searchfile, outfile, begindate, enddate):
    """
    collect race results from ultrasignup
    
    :param searchfile: path to file containing names, genders, birth dates to search for
    :param outfile: output file path
    :param begindate: epoch time - choose races between begindate and enddate
    :param enddate: epoch time - choose races between begindate and enddate
    """
    _IN = open(searchfile, 'r', newline='')
    IN = csv.DictReader(_IN)
    _OUT = open(outfile, 'w', newline='')
    OUT = csv.DictWriter(_OUT, UltraSignupResultFile.filehdr)
    OUT.writeheader()
    commonfields = 'GivenName,FamilyName,DOB,Gender'.split(',')
    ultra = ultrasignup.UltraSignup(debug=True)
    dt_begindate = timeu.epoch2dt(begindate)
    adj_begindate = datetime.datetime(dt_begindate.year, dt_begindate.month, dt_begindate.day, 0, 0, 0)
    begindate = timeu.dt2epoch(adj_begindate)
    dt_enddate = timeu.epoch2dt(enddate)
    adj_enddate = datetime.datetime(dt_enddate.year, dt_enddate.month, dt_enddate.day, 23, 59, 59)
    enddate = timeu.dt2epoch(adj_enddate)
    start = time.time()
    today = timeu.epoch2dt(start)
    for runner in IN:
        fname, lname = runner['GivenName'], runner['FamilyName']
        e_dob = ftime.asc2epoch(runner['DOB'])
        dt_dob = ftime.asc2dt(runner['DOB'])
        gender = runner['Gender'][0]
        results = ultra.listresults(fname, lname)
        for result in results:
            e_racedate = ftime.asc2epoch(result.racedate)
            if not e_racedate < begindate:
                if e_racedate > enddate:
                    continue
                else:
                    dt_racedate = timeu.epoch2dt(e_racedate)
                    racedateage = timeu.age(dt_racedate, dt_dob)
                    if result.age != racedateage:
                        continue
                    resultgen = result.gender
                    if resultgen != runner['Gender'][0]:
                        continue
                outrec = {}
                for field in commonfields:
                    outrec[field] = runner[field]

                outrec['name'] = '{} {}'.format(runner['GivenName'], runner['FamilyName'])
                outrec['age'] = result.age
                racename = result.racename
                outrec['race'] = racename
                outrec['date'] = ftime.epoch2asc(e_racedate)
                outrec['loc'] = '{}, {}'.format(result.racecity, result.racestate)
                distmiles = result.distmiles
                distkm = result.distkm
                if not distkm is None:
                    if distkm < 0.05:
                        pass
                    else:
                        outrec['miles'] = distmiles
                        outrec['km'] = distkm
                        resulttime = result.racetime
                        if isinstance(resulttime, int):
                            pass
                        else:
                            if resulttime[0] == ':':
                                resulttime = '0' + resulttime
                            while resulttime.count(':') < 2:
                                resulttime = '0:' + resulttime

                            outrec['time'] = resulttime
                            try:
                                agpercent, agresult, agfactor = ag.agegrade(racedateage, gender, distmiles, timeu.timesecs(resulttime))
                                outrec['ag'] = agpercent
                                if agpercent < 15 or agpercent >= 100:
                                    continue
                            except:
                                pass

                            OUT.writerow(outrec)

    _OUT.close()
    _IN.close()
    finish = time.time()
    print('number of URLs retrieved = {}'.format(ultra.geturlcount()))
    print('elapsed time (min) = {}'.format((finish - start) / 60))


class UltraSignupFileResult:
    __doc__ = '\n    holds result from ultrasignup file\n    \n    :param firstname: first name\n    :param lastname: last name\n    :param name: firstname lastname\n    :param dob: date of birth, datetime\n    :param gender: M or F\n    :param race: name of race\n    :param date: date of race, datetime\n    :param loc: location of race\n    :param age: age on race day\n    :param miles: race distance, miles\n    :param km: race distance, kilometers\n    :param time: race time, seconds\n    :param ag: age grade percentage\n    '
    attrs = 'firstname,lastname,name,dob,gender,race,date,loc,age,miles,km,time,ag'.split(',')

    def __init__(self, firstname=None, lastname=None, name=None, dob=None, gender=None, race=None, date=None, loc=None, age=None, miles=None, km=None, time=None, ag=None):
        self.firstname = firstname
        self.lastname = lastname
        self.name = name
        self.dob = dob
        self.gender = gender
        self.race = race
        self.date = date
        self.loc = loc
        self.age = age
        self.miles = miles
        self.km = km
        self.time = time
        self.ag = ag

    def __repr__(self):
        reprval = '{}('.format(self.__class__)
        for attr in self.attrs:
            val = getattr(self, attr)
            if attr in ('dob', 'date'):
                val = ftime.dt2asc(val)
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


class UltraSignupResultFile:
    __doc__ = '\n    represents file of ultrasignup results collected from ultrasignup\n    \n    TODO:: add write methods, and update :func:`collect` to use :class:`UltraSignupFileResult` class\n    '
    filehdr = 'GivenName,FamilyName,name,DOB,Gender,race,date,loc,age,miles,km,time,ag'.split(',')
    hdrtransform = dict(list(zip(filehdr, UltraSignupFileResult.attrs)))
    resultdates = 'dob,date'.split(',')

    def __init__(self, filename):
        self.filename = filename

    def open(self, mode='r'):
        """
        open ultrasignup result file
        
        :param mode: 'r' or 'w' -- TODO: support 'w'
        """
        if mode[0] not in 'r':
            raise invalidParameter('mode {} not currently supported'.format(mode))
        self._fh = open((self.filename), mode, newline='')
        if mode[0] == 'r':
            self._csv = csv.DictReader(self._fh)

    def close(self):
        """
        close ultrasignup result file
        """
        if hasattr(self, '_fh'):
            self._fh.close()
            delattr(self, '_fh')
            delattr(self, '_csv')

    def __next__(self):
        """
        get next :class:`UltraSignupFileResult`
        
        :rtype: :class:`UltraSignupFileResult`, or None when end of file reached
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
                        aresultargs[aattr] = ftime.asc2dt(fresult[fattr])
                    else:
                        aresultargs[aattr] = csvu.str2num(fresult[fattr])

            return UltraSignupFileResult(**aresultargs)


def main():
    descr = '\n    collect race results from ultrasignup\n    \n    searchfile must have at least the following headings:\n    \n        * GivenName - first name\n        * FamilyName - last name\n        * Gender - Male or Female (or M or F)\n        * DOB - date of birth in yyyy-mm-dd format\n        * City - city of residence [optional]\n        * State - state of residence [optional]\n    '
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