# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\comparegpx.py
# Compiled at: 2020-01-13 13:13:28
# Size of source mod 2**32: 4435 bytes
"""
comparegpx - compare two gpx files
=======================================
"""
import pdb, optparse, datetime, os.path, csv, collections
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
import gpxpy, gpxpy.geo
from loutilities import timeu
METERPMILE = 1609.3439941
t = timeu.asctime('%Y-%m-%dT%H:%M:%SZ')

class invalidCoeff(Exception):
    pass


def main():
    usage = 'usage: %prog [options] <gpxfile1> <gpxfile2>\n\n'
    usage += 'where:\n'
    usage += '  <gpxfile>\tgpx formatted file'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-o', '--output', dest='output', help='output file', default=None)
    options, args = parser.parse_args()
    gpxfile = {}
    _GPX = {}
    gpx = {}
    for f in range(2):
        gpxfile[f] = args.pop(0)
        _GPX[f] = open(gpxfile[f], 'r')
        gpx[f] = gpxpy.parse(_GPX[f])
        _GPX[f].close()

    times = {}
    dists = {}
    for f in range(2):
        times[f] = []
        dists[f] = []
        lastpoint = None
        totdist = 0
        for track in gpx[f].tracks:
            for segment in track.segments:
                for point in segment.points:
                    if not lastpoint:
                        lastpoint = point
                    plon = point.longitude
                    plat = point.latitude
                    pelev = point.elevation
                    thisdist = gpxpy.geo.distance(lastpoint.latitude, lastpoint.longitude, lastpoint.elevation, plat, plon, pelev)
                    lastpoint = point
                    totdist += thisdist
                    dists[f].append(totdist)
                    times[f].append(timeu.dt2epoch(point.time))

    earliest = max(times[0][0], times[1][0])
    latest = min(times[0][(-1)], times[1][(-1)])
    earliest = int(earliest + 5) // 5 * 5
    latest = int(latest) // 5 * 5
    results = {}
    for f in range(2):
        titer = iter(times[f])
        diter = iter(dists[f])
        tdeq = collections.deque([], 2)
        ddeq = collections.deque([], 2)
        try:
            for time in range(earliest, latest, 5):
                if time not in results:
                    results[time] = {0:None, 
                     1:None}
                while len(tdeq) < 2 or tdeq[(-1)] < time:
                    tdeq.append(next(titer))
                    ddeq.append(next(diter))

                interpcoeff = float(time - tdeq[0]) / (tdeq[1] - tdeq[0])
                if interpcoeff < 0 or interpcoeff > 1:
                    raise invalidCoeff
                thisdist = ddeq[0] + interpcoeff * (ddeq[1] - ddeq[0])
                results[time][f] = thisdist

        except StopIteration:
            pass

    if options.output == None:
        outfile = os.path.basename(gpxfile[0]) + '.csv'
    else:
        outfile = options.output
    OUT = open(outfile, 'w')
    OUT.write('time,{0},{1}\n'.format(gpxfile[0], gpxfile[1]))
    for time in range(earliest, latest, 5):
        OUT.write('{0},{1},{2}\n'.format(t.epoch2asc(time), results[time][0], results[time][1]))

    OUT.close()


if __name__ == '__main__':
    main()