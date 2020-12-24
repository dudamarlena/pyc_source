# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\parserun-bk3.py
# Compiled at: 2020-01-15 16:12:19
# Size of source mod 2**32: 6213 bytes
import optparse, datetime, re, os, math
from running.running import xmldict
MHR = 204
METERPMILE = 1609.3439941
EPSILON = METERPMILE - 1600 + 1

def timestr(tsm):
    tsec = int(tsm)
    tusec = (tsm - tsec) * 1000000.0 + 500000.0
    d = datetime.timedelta(0, tsec, tusec)
    dt1 = datetime.datetime(2009, 1, 1, 0, 0, 0)
    dt2 = dt1 + d
    if tsec + tusec / 1000000.0 > 3600:
        fmt = '%H:%M:%S'
    else:
        fmt = '%M:%S'
    s = dt2.strftime(fmt)
    s = re.sub('^0', '', s)
    return s


def pace(ts, d):
    tsm = ts * (METERPMILE / d)
    return timestr(tsm)


usage = 'usage: %prog [options] <tcxfile> <laplist>\n\n'
usage += 'where:\n'
usage += '  <tcxfile>\tfile output from Garmin Training Center\n'
usage += '  <laplist> is one of two formats:\n'
usage += '     no switches\tsets of laps to be averaged, i.e., 5,3 means average first 5 laps, next 3 laps, then remaining\n'
usage += '     -interval\tnum laps before first workout then num repeats\n'
parser = optparse.OptionParser(usage=usage)
parser.add_option('-i', '--interval', dest='interval', action='store_true', help='treat input as intervals: num laps before first workout then num repeats')
parser.set_defaults(interval=False)
options, args = parser.parse_args()
tcxfile = args.pop(0)
laplist = args.pop(0)
sets = [int(si) for si in laplist.split(',')]
numsets = len(sets)
root = xmldict.readXmlFile(tcxfile)
laps = root['TrainingCenterDatabase']['Activities']['Activity']['Lap']
numlaps = len(laps)
ul = [True for i in range(numlaps)]
if options.interval:
    ul = [False for i in range(numlaps)]
    numbefore, numint = sets
    for i in range(numint):
        ul[numbefore + i * 2] = True

    sets = [numlaps]
    numsets = 0
more = True
l = 0
tttime = 0
tthrtime = 0
tthr = 0
ttdist = 0
setstr = ''
csvstr = 'distance,time,pace,avghr\n'
pacesstr = {}
for s in range(numsets + 1):
    ttime = 0
    thrtime = 0
    thr = 0
    tdist = 0
    if s < numsets:
        setlimit = sets[s]
    else:
        setlimit = numlaps
    for i in range(setlimit):
        time = float(laps[l]['TotalTimeSeconds'])
        hr = int(laps[l]['AverageHeartRateBpm']['Value'])
        dist = float(laps[l]['DistanceMeters'])
        if dist != 0.0:
            if ul[l]:
                ttime += time
                if l != 0:
                    thrtime += time
                    thr += hr * time
                tdist += dist
            else:
                tttime += time
                if l != 0:
                    tthrtime += time
                    tthr += hr * time
                ttdist += dist
                pacesstr[l] = pacesstr.setdefault(l, '') + timestr(time) + '({0:d})'.format(hr)
                csvstr += '{0:.2f},{1},{2},{3}\n'.format(dist / METERPMILE, timestr(time), pace(time, dist), hr)
                if dist != METERPMILE:
                    pacesstr[l] += ' [{0:.2f}={1}]'.format(dist / METERPMILE, pace(time, dist))
                else:
                    pacesstr[l] = pacesstr.setdefault(l, '') + timestr(time) + '({0:d})'.format(hr)
            l += 1
            if l == numlaps:
                more = False
                break

    if thrtime > 0:
        ahr = int(thr / thrtime + 0.5)
    else:
        ahr = 'n/a'
    apace = pace(ttime, tdist)
    adist = tdist / METERPMILE
    if s < numsets:
        intmiles = int(adist + 0.5)
        if math.fabs(tdist / intmiles - METERPMILE) < EPSILON:
            adistpr = int(adist + EPSILON / METERPMILE)
        else:
            adistpr = adist
    else:
        adistpr = '{0:.2f}'.format(adist)
    if s > 0:
        setstr += ', '
    setstr += '{0}@{1}({2})'.format(adistpr, apace, ahr)
    if not more:
        break

athr = int(tthr / tthrtime + 0.5)
atpace = pace(tttime, ttdist)
atdist = ttdist / METERPMILE
totstr = '{0:.1f} miles, {1}, {2}/mi, AHR {3} ({4}% MHR)'.format(atdist, timestr(tttime), atpace, athr, int(athr * 100 / MHR + 0.5))
CSV = open('history.csv', 'w')
CSV.write(csvstr)
CSV.close()
OUT = open('temp.txt', 'w')
OUT.write('{0}\n'.format(totstr))
OUT.write('{0}\n\n'.format(setstr))
if options.interval:
    OUT.write('splits:\n')
    for l in range(numlaps):
        if ul[l]:
            OUT.write('{0}\n'.format(pacesstr[l]))

    OUT.write('\n')
OUT.write('all splits:\n')
for l in range(numlaps):
    split = l + 1
    OUT.write('{0} - {1}\n'.format(split, pacesstr[l]))

OUT.close()
os.startfile('temp.txt')