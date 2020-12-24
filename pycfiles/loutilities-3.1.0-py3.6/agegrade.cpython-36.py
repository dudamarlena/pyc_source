# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\agegrade.py
# Compiled at: 2019-11-20 12:30:05
# Size of source mod 2**32: 13494 bytes
"""
agegrade - calculate age grade statistics
===================================================
"""
import argparse, csv, os.path, pickle, shutil
from . import version
from .config import *
from . import csvwt

class missingConfiguration(Exception):
    pass


class parameterError(Exception):
    pass


def getagtable(agegradewb):
    """
    in return data structure:
    
    dist is distance in meters (approx)
    openstd is number of seconds for open standard for this distance
    age is age in years (integer)
    factor is age grade factor
    
    :param agegradewb: excel workbook containing age grade factors (e.g., from http://www.howardgrubb.co.uk/athletics/data/wavacalc10.xls)
    
    :rtype: {'F':{dist:{'OC':openstd,age:factor,age:factor,...},...},'M':{dist:{'OC':openstd,age:factor,age:factor,...},...}}
    """
    agegradedata = {}
    c = csvwt.Xls2Csv(agegradewb)
    gen2sheet = {'F':'Women',  'M':'Men'}
    sheets = c.getfiles()
    for gen in ('F', 'M'):
        SHEET = open(sheets[gen2sheet[gen]], 'rb')
        sheet = csv.DictReader(SHEET)
        f2age = {}
        for f in sheet.fieldnames:
            try:
                k = int(float(f))
                f2age[f] = k
            except ValueError:
                pass

        agegradedata[gen] = {}
        for r in sheet:
            if r['dist(km)'] == '0.0':
                pass
            else:
                dist = int(round(float(r['dist(km)']) * 1000))
                if dist in agegradedata[gen]:
                    pass
                else:
                    openstd = float(r['OC'])
                    agegradedata[gen][dist] = {'OC': openstd}
                    for f in sheet.fieldnames:
                        if f in f2age:
                            age = f2age[f]
                            agegradedata[gen][dist][age] = float(r[f])

        SHEET.close()

    del c
    return agegradedata


class AgeGrade:
    __doc__ = '\n    AgeGrade object \n    \n    agegradewb is in format per http://www.howardgrubb.co.uk/athletics/wmalookup06.html\n    if agegradewb parameter is missing, previous configuration is used\n    configuration is created through command line: agegrade.py [-a agworkbook | -c agconfigfile]\n    \n    :param agegradewb: excel workbook containing age grade factors\n    :param DEBUG: file handle for debug output\n    '

    def __init__(self, agegradewb=None, DEBUG=None):
        self.DEBUG = DEBUG
        if self.DEBUG:
            self.DEBUG.write('distmeters,age,gen,openstd,factor,time,agresult,agpercentage\n')
        if agegradewb:
            self.agegradedata = getagtable(agegradewb)
        else:
            pathn = os.path.join(CONFIGDIR, 'agegrade.cfg')
            if not os.path.exists(pathn):
                raise missingConfiguration('agegrade configuration not found, run agegrade.py to configure')
            C = open(pathn)
            self.agegradedata = pickle.load(C)
            C.close()

    def getfactorstd(self, age, gen, distmeters):
        """
        interpolate factor and openstd based on distance for this age
        
        :param age: integer age.  If float is supplied, integer portion is used (no interpolation of fractional age)
        :param gen: gender - M or F
        :param distmeters: distance (meters)
        
        :rtype: (factor, openstd) - factor (age grade factor) is between 0 and 1, openstd (open standard) is in seconds
        """
        distmeters = round(distmeters)
        distlist = sorted(list(self.agegradedata[gen].keys()))
        lastd = distlist[0]
        for i in range(1, len(distlist)):
            if distmeters <= distlist[i]:
                x0 = lastd
                x1 = distlist[i]
                f0 = self.agegradedata[gen][x0][age]
                f1 = self.agegradedata[gen][x1][age]
                oc0 = self.agegradedata[gen][x0]['OC']
                oc1 = self.agegradedata[gen][x1]['OC']
                break
            lastd = distlist[i]

        factor = f0 + (f1 - f0) * ((distmeters - x0) / (x1 - x0))
        openstd = oc0 + (oc1 - oc0) * ((distmeters - x0) / (x1 - x0))
        return (
         factor, openstd)

    def agegrade(self, age, gen, distmiles, time):
        """
        returns age grade statistics for the indicated age, gender, distance, result time
        
        :param age: integer age.  If float is supplied, integer portion is used (no interpolation of fractional age)
        :param gen: gender - M or F
        :param distmiles: distance (miles)
        :param time: time for distance (seconds)
        
        :rtype: (age performance percentage, age graded result, age grade factor) - percentage is between 0 and 100, result is in seconds
        """
        gen = gen.upper()
        if gen not in ('F', 'M'):
            raise parameterError('gen must be M or F')
        else:
            mpermile = 1609.344
            cdist = {26.2:42195, 
             13.1:21098}
            if distmiles in cdist:
                distmeters = cdist[distmiles]
            else:
                distmeters = distmiles * mpermile
        distlist = list(self.agegradedata[gen].keys())
        minmeters = min(distlist) * 1.0
        maxmeters = max(distlist) * 1.0
        if distmeters < minmeters or distmeters > maxmeters:
            raise parameterError('distmiles must be between {:0.3f} and {:0.1f}'.format(minmeters / mpermile, maxmeters / mpermile))
        age = int(age)
        if age in range(5, 100):
            factor, openstd = self.getfactorstd(age, gen, distmeters)
        else:
            if age < 5:
                factor, openstd = self.getfactorstd(5, gen, distmeters)
            elif age > 99:
                factor, openstd = self.getfactorstd(99, gen, distmeters)
        agpercentage = 100 * (openstd / factor) / time
        agresult = time * factor
        if self.DEBUG:
            self.DEBUG.write('{},{},{},{},{},{},{},{}\n'.format(distmeters, age, gen, openstd, factor, time, agresult, agpercentage))
        return (
         agpercentage, agresult, factor)


def main():
    descr = '\n    Update configuration for agegrade.py.  One of --agworkbook or --agconfigfile must be used,\n    but not both.\n    \n    --agworkbook creates an agconfigfile and puts it in the configuration directory.\n    --agconfigfile simply places the indicated file into the configuration directory.\n    '
    parser = argparse.ArgumentParser(description=descr, formatter_class=(argparse.RawDescriptionHelpFormatter), version=('{0} {1}'.format('loutilities', version.__version__)))
    parser.add_argument('-a', '--agworkbook', help='filename of age grade workbook.', default=None)
    parser.add_argument('-c', '--agconfigfile', help='filename of age grade config file', default=None)
    args = parser.parse_args()
    if not args.agworkbook:
        if not args.agconfigfile:
            print('one of --agworkbook or --agconfigfile must be specified')
            return
    if args.agworkbook:
        if args.agconfigfile:
            print('only one of --agworkbook or --agconfigfile should be specified')
            return
    else:
        pathn = os.path.join(CONFIGDIR, 'agegrade.cfg')
        if args.agworkbook:
            agegradedata = getagtable(args.agworkbook)
            C = open(pathn, 'w')
            pickle.dump(agegradedata, C)
            C.close()
        else:
            try:
                C = open(args.agconfigfile)
                test = pickle.load(C)
                C.close()
            except IOError:
                print('{0}: not found'.format(args.agconfigfile))
                return
            except KeyError:
                print('{0}: invalid format'.format(args.agconfigfile))
                return
            else:
                shutil.copyfile(args.agconfigfile, pathn)
    print('updated {0}'.format(pathn))


if __name__ == '__main__':
    main()