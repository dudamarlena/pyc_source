# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\athlinksresults.py
# Compiled at: 2020-02-27 16:28:30
# Size of source mod 2**32: 15861 bytes
"""
athlinksresults - manage race results data from athlinks
===================================================================

Usage::
    athlinksresults.py [-h] [-v] [-b BEGINDATE] [-e ENDDATE]
                                     searchfile outfile
    
        collect race results from athlinks
    
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
from running.running import version, athlinks
CAT_RUNNING = 2
CAT_TRAILS = 15
race_category = {CAT_RUNNING: 'Running', CAT_TRAILS: 'Trail Running'}
ag = agegrade.AgeGrade()

class invalidParameter(Exception):
    pass


resultfilehdr = 'GivenName,FamilyName,name,DOB,Gender,athlmember,athlid,race,date,loc,age,fuzzyage,miles,km,category,time,ag'.split(',')
resultattrs = 'firstname,lastname,name,dob,gender,member,id,racename,racedate,raceloc,age,fuzzyage,distmiles,distkm,racecategory,resulttime,resultagegrade'.split(',')
resultdates = 'dob,racedate'.split(',')
hdrtransform = dict(list(zip(resultfilehdr, resultattrs)))
ftime = timeu.asctime('%Y-%m-%d')

def collect(searchfile, outfile, begindate, enddate):
    """
    collect race results from athlinks
    
    :param searchfile: path to file containing names, genders, birth dates to search for
    :param outfile: output file path
    :param begindate: epoch time - choose races between begindate and enddate
    :param enddate: epoch time - choose races between begindate and enddate
    """
    _IN = open(searchfile, newline='')
    IN = csv.DictReader(_IN)
    _OUT = open(outfile, mode='w', newline='')
    OUT = csv.DictWriter(_OUT, resultfilehdr)
    OUT.writeheader()
    commonfields = 'GivenName,FamilyName,DOB,Gender'.split(',')
    athl = athlinks.Athlinks(debug=True)
    dt_begindate = timeu.epoch2dt(begindate)
    adj_begindate = datetime.datetime(dt_begindate.year, dt_begindate.month, dt_begindate.day, 0, 0, 0)
    begindate = timeu.dt2epoch(adj_begindate)
    dt_enddate = timeu.epoch2dt(enddate)
    adj_enddate = datetime.datetime(dt_enddate.year, dt_enddate.month, dt_enddate.day, 23, 59, 59)
    enddate = timeu.dt2epoch(adj_enddate)
    start = time.time()
    today = timeu.epoch2dt(start)
    for runner in IN:
        name = ' '.join([runner['GivenName'], runner['FamilyName']])
        e_dob = ftime.asc2epoch(runner['DOB'])
        dt_dob = ftime.asc2dt(runner['DOB'])
        results = athl.listathleteresults(name)
        for result in results:
            e_racedate = athlinks.gettime(result['Race']['RaceDate'])
            if not e_racedate < begindate:
                if e_racedate > enddate:
                    continue
                else:
                    outrec = {}
                    for field in commonfields:
                        outrec[field] = runner[field]

                    dt_racedate = timeu.epoch2dt(e_racedate)
                    racedateage = timeu.age(dt_racedate, dt_dob)
                    resultage = int(result['Age'])
                    if resultage != racedateage:
                        if resultage // 5 * 5 != resultage:
                            continue
                        elif racedateage // 5 * 5 == resultage:
                            outrec['fuzzyage'] = 'Y'
                        else:
                            continue
                    resultgen = result['Gender'][0]
                    if resultgen != runner['Gender'][0]:
                        continue
                course = athl.getcourse(result['Race']['RaceID'], result['CourseID'])
                thiscategory = course['Courses'][0]['RaceCatID']
                if thiscategory not in race_category:
                    pass
                else:
                    outrec['name'] = '{} {}'.format(runner['GivenName'], runner['FamilyName'])
                    outrec['age'] = result['Age']
                    athlmember = result['IsMember']
                    if athlmember:
                        outrec['athlmember'] = 'Y'
                        outrec['athlid'] = result['RacerID']
                    racename = csvu.unicode2ascii(course['RaceName'])
                    coursename = csvu.unicode2ascii(course['Courses'][0]['CourseName'])
                    outrec['race'] = '{} / {}'.format(racename, coursename)
                    outrec['date'] = ftime.epoch2asc(athlinks.gettime(course['RaceDate']))
                    outrec['loc'] = csvu.unicode2ascii(course['Home'])
                    distmiles = athlinks.dist2miles(course['Courses'][0]['DistUnit'], course['Courses'][0]['DistTypeID'])
                    distkm = athlinks.dist2km(course['Courses'][0]['DistUnit'], course['Courses'][0]['DistTypeID'])
                    if distkm < 0.05:
                        pass
                    else:
                        outrec['miles'] = distmiles
                        outrec['km'] = distkm
                        outrec['category'] = race_category[thiscategory]
                        resulttime = result['TicksString']
                        if resulttime[0] == ':':
                            resulttime = '0' + resulttime
                        while resulttime.count(':') < 2:
                            resulttime = '0:' + resulttime

                        outrec['time'] = resulttime
                        try:
                            agpercent, agresult, agfactor = ag.agegrade(racedateage, resultgen, distmiles, timeu.timesecs(resulttime))
                            outrec['ag'] = agpercent
                            if agpercent < 15 or agpercent >= 100:
                                continue
                        except:
                            pass

                        OUT.writerow(outrec)

    _OUT.close()
    _IN.close()
    finish = time.time()
    print('number of URLs retrieved = {}'.format(athl.geturlcount()))
    print('elapsed time (min) = {}'.format((finish - start) / 60))


class AthlinksResult:
    __doc__ = '\n    represents single result from athlinks\n    '

    def __init__(self, **myattrs):
        for attr in resultattrs:
            setattr(self, attr, None)

        for attr in myattrs:
            if attr not in resultattrs:
                raise invalidParameter('unknown attribute: {}'.format(attr))
            setattr(self, attr, myattrs[attr])

    def __repr__(self):
        reprstr = 'athlinksresult.AthlinksResult('
        for attr in resultattrs:
            reprstr += '{}={},'.format(attr, getattr(self, attr))

        reprstr = reprstr[:-1] + ')'
        return reprstr


class AthlinksResultFile:
    __doc__ = '\n    represents file of athlinks results collected from athlinks\n    \n    TODO:: add write methods, and update :func:`collect` to use :class:`AthlinksResult` class\n    '

    def __init__(self, filename):
        self.filename = filename

    def open(self, mode='r'):
        """
        open athlinks result file
        
        :param mode: 'r' or 'w' -- TODO: support 'w'
        """
        if mode[0] not in 'r':
            raise invalidParameter('mode {} not currently supported'.format(mode))
        self._fh = open((self.filename), mode, newline='')
        if mode[0] == 'r':
            self._csv = csv.DictReader(self._fh)

    def close(self):
        """
        close athlinks result file
        """
        if hasattr(self, '_fh'):
            self._fh.close()
            delattr(self, '_fh')
            delattr(self, '_csv')

    def __next__(self):
        """
        get next :class:`AthlinksResult`
        
        :rtype: :class:`AthlinksResult`, or None when end of file reached
        """
        try:
            fresult = next(self._csv)
        except StopIteration:
            return
        else:
            aresultargs = {}
            for fattr in hdrtransform:
                aattr = hdrtransform[fattr]
                if aattr == 'gender':
                    aresultargs[aattr] = fresult[fattr][0]
                else:
                    if aattr in resultdates:
                        aresultargs[aattr] = ftime.asc2dt(fresult[fattr])
                    else:
                        try:
                            aresultargs[aattr] = int(fresult[fattr])
                        except ValueError:
                            try:
                                aresultargs[aattr] = float(fresult[fattr])
                            except ValueError:
                                aresultargs[aattr] = fresult[fattr]

            return AthlinksResult(**aresultargs)


def main():
    descr = '\n    collect race results from athlinks\n    \n    searchfile must have at least the following headings:\n    \n        * GivenName - first name\n        * FamilyName - last name\n        * Gender - Male or Female (or M or F)\n        * DOB - date of birth in yyyy-mm-dd format\n        * City - city of residence [optional]\n        * State - state of residence [optional]\n    '
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