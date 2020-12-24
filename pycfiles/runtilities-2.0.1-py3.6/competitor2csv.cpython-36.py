# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\competitor2csv.py
# Compiled at: 2020-02-26 14:50:54
# Size of source mod 2**32: 5644 bytes
"""
getmembers-competitor - get members who ran competitor race (e.g., Rock 'n' Roll Marathon)
==============================================================================================

Usage::

    TBA
"""
import csv, argparse
from string import maketrans
from collections import OrderedDict
from running.running import version
from .competitor import Competitor
competitor2raceresult = OrderedDict([
 ('oaplace', 'place'),
 ('name', 'name'),
 ('genplace', 'gender place'),
 ('divplace', 'division place'),
 ('age', 'age'),
 ('gender', 'gender'),
 ('hometown', 'hometown'),
 ('racetime', 'time'),
 ('racedate', 'race date'),
 ('raceloc', 'race location'),
 ('racename', 'race name'),
 ('distmiles', 'miles'),
 ('distkm', 'km')])

def getcompetitorrace(outfile, eventid, eventinstanceid, singleeventid, limit=None):
    """
    create file for competitor race based on eventid, eventinstanceid, singleeventid
    
    :param outfile: base filename for output file, event and distance are appended to name
    :param eventid: event id from running.competitor.com
    :param eventinstanceid: event instance id from running.competitor.com
    :param singleeventid: single event id from running.competitor.com
    :param limit: limit number of records (for testing only)
    
    :rtype: name of file which was created
    """
    cc = Competitor()
    cc.setraceyear(eventid, eventinstanceid, singleeventid)
    results = cc.getresults(limit)
    racename = str(results[0].racename)
    dist = '{:.1f}'.format(results[0].distmiles)
    if dist == 13.1:
        dist = 'halfmarathon'
    else:
        if dist == 26.2:
            dist = 'marathon'
        else:
            dist = '{}miles'.format(dist)
    transtab = maketrans(' \'"', '-xx')
    tracename = racename.translate(transtab)
    outfilename = '{}-{}-{}.csv'.format(outfile, tracename, dist)
    RS_ = open(outfilename, 'w', newline='')
    RS = csv.DictWriter(RS_, list(competitor2raceresult.values()))
    RS.writeheader()
    for result in results:
        filerow = {}
        for attr in result.attrs:
            filerow[competitor2raceresult[attr]] = getattr(result, attr)

        RS.writerow(filerow)

    RS_.close()
    return outfilename


def getcompetitor(outfile):
    """
    put competitor results into csv file per race
    
    :param outfile: base of output file name for competitor files
    
    :rtype: list containing names of files which were created
    """
    resultfiles = []
    thisfile = getcompetitorrace(outfile, 54, 227, 797)
    resultfiles.append(thisfile)
    thisfile = getcompetitorrace(outfile, 54, 227, 791)
    resultfiles.append(thisfile)
    return resultfiles


def main():
    parser = argparse.ArgumentParser(version=('running {0}'.format(version.__version__)))
    parser.add_argument('outfile', help='base name for output file')
    parser.add_argument('-e', '--eventid', help='eventid for competitor.com', type=int, default=None)
    parser.add_argument('-i', '--instanceid', help='event instance for competitor.com (which year)', type=int, default=None)
    parser.add_argument('-s', '--singleeventid', help='single eventid for competitor.com (which distance)', type=int, default=None)
    parser.add_argument('-l', '--limit', help='limit number of records (for testing only)', type=int, default=None)
    args = parser.parse_args()
    outfile = args.outfile
    eventid = args.eventid
    instanceid = args.instanceid
    singleeventid = args.singleeventid
    limit = args.limit
    resultfile = getcompetitorrace(outfile, eventid, instanceid, singleeventid, limit)
    print('generated {}'.format(resultfile))


if __name__ == '__main__':
    main()