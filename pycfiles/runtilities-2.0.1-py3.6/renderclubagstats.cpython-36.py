# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\renderclubagstats.py
# Compiled at: 2020-02-26 14:50:54
# Size of source mod 2**32: 20993 bytes
"""
renderclubagstats - render age grade statistics for a club
===================================================================

Render club age grade statistics, based on collected athlinks statistics (collectathlinksresults),
club data in runningahead ( (TODO: RA data) analyzeagegrade) and club results (runningclub.exportresults)

Usage::
    TBA
    
"""
import argparse, csv, datetime, collections, time
from IPython.core.debugger import Tracer
debug_here = Tracer()
import matplotlib.pyplot as plt
from loutilities import timeu
from runningclub import render as ren
from running.running import ultrasignupresults, analyzeagegrade, athlinksresults, version, runningaheadresults

class invalidParameter(Exception):
    pass


METERSPERMILE = 1609.344
TRENDLIMITS = collections.OrderedDict([
 ((0, 4999.99), ('<5K', 'b')),
 ((5000.0, 21097.5), ('5K - <HM', 'g')),
 ((21097.51, 42194.99), ('HM - Mara', 'orange')),
 ((42195.0, 200000), ('Ultra', 'r'))])
PRIO_CLUBRACES = 1
PRIO_ULTRASIGNUP = 2
PRIO_ATHLINKS = 3
PRIO_RUNNINGAHEAD = 4

def mean(items):
    if len(items) > 0:
        return float(sum(items)) / len(items)
    else:
        return float('nan')


def initaagrunner(aag, thisname, gender, dob):
    """
    initializaze :class:`AnalyzeAgeGrade` object, if not already initialized
    
    :param aag: :class:`AnalyzeAgeGrade` objects, by runner name
    :param thisname: runner name
    :param gender: M or F
    :param dob: datetime date of birth
    """
    if thisname not in aag:
        aag[thisname] = analyzeagegrade.AnalyzeAgeGrade()
        aag[thisname].set_runner(thisname, gender, dob)


def collectathlinks(aag, athlinksfile):
    """
    Collect club age grade statistics, based on collected athlinks statistics (collectathlinksresults)
    
    :param aag: :class:`AnalyzeAgeGrade` objects, by runner name
    :param athlinksfile: file with athlinks results, output from athlinksresults
    """
    athlf = athlinksresults.AthlinksResultFile(athlinksfile)
    athlf.open()
    while 1:
        result = next(athlf)
        if result is None:
            break
        thisname = result.name.lower()
        initaagrunner(aag, thisname, result.gender, result.dob)
        timesecs = timeu.timesecs(result.resulttime)
        if timesecs > 0:
            aag[thisname].add_stat((result.racedate), (result.distkm * 1000), timesecs, race=(result.racename), loc=(result.raceloc),
              fuzzyage=(result.fuzzyage),
              source='athlinks',
              priority=PRIO_ATHLINKS)


def collectultrasignup(aag, ultrasignupfile):
    """
    Collect club age grade statistics, based on collected ultrasignup statistics (collectultrasignupresults)
    
    :param aag: :class:`AnalyzeAgeGrade` objects, by runner name
    :param ultrasignupfile: file with ultrasignup results, output from ultrasignupresults
    """
    ultra = ultrasignupresults.UltraSignupResultFile(ultrasignupfile)
    ultra.open()
    while 1:
        result = next(ultra)
        if result is None:
            break
        thisname = result.name.lower()
        initaagrunner(aag, thisname, result.gender, result.dob)
        timesecs = timeu.timesecs(result.time)
        if timesecs > 0:
            aag[thisname].add_stat((result.date), (result.km * 1000), timesecs, race=(result.race), loc=(result.loc),
              source='ultrasignup',
              priority=PRIO_ULTRASIGNUP)


def collectrunningahead(aag, runningaheadfile):
    """
    Collect club age grade statistics, based on collected runningahead statistics (collectrunningaheadresults)
    
    :param aag: :class:`AnalyzeAgeGrade` objects, by runner name
    :param runningaheadfile: file with runningahead results, output from runningaheadresults
    """
    rafile = runningaheadresults.RunningAheadResultFile(runningaheadfile)
    rafile.open()
    while 1:
        result = next(rafile)
        if result is None:
            break
        thisname = result.name.lower()
        initaagrunner(aag, thisname, result.gender, result.dob)
        timesecs = timeu.timesecs(result.time)
        if timesecs > 0:
            aag[thisname].add_stat((result.date), (result.km * 1000), timesecs, race=(result.race), source='runningahead', priority=PRIO_RUNNINGAHEAD)


def collectclub(aag, clubfile):
    """
    Collect club age grade statistics, based on collected athlinks statistics (collectathlinksresults)
    
    :param aag: :class:`AnalyzeAgeGrade` objects, by runner name
    :param clubfile: file with club results, output from runningclub.exportresults
    """
    _clubf = open(clubfile, 'r', newline='')
    clubf = csv.DictReader(_clubf)
    tfile = timeu.asctime('%Y-%m-%d')

    class ClubResult:

        def __init__(self, name, dob, gender, racename, racedate, distmiles, distkm, resulttime, ag):
            self.name = name
            self.dob = tfile.asc2dt(dob)
            self.gender = gender
            self.racename = racename
            self.racedate = tfile.asc2dt(racedate)
            self.distmiles = float(distmiles)
            self.distkm = float(distkm)
            self.resulttime = timeu.timesecs(resulttime)
            self.ag = float(ag)

    while 1:
        try:
            row = next(clubf)
            result = ClubResult(row['name'], row['dob'], row['gender'], row['race'], row['date'], row['miles'], row['km'], row['time'], row['ag'])
        except StopIteration:
            result = None

        if result is None:
            break
        thisname = result.name.lower()
        initaagrunner(aag, thisname, result.gender, result.dob)
        timesecs = result.resulttime
        if timesecs > 0:
            aag[thisname].add_stat((result.racedate), (result.distkm * 1000), timesecs, race=(result.racename), source='clubraces', priority=PRIO_CLUBRACES)


def render(aag, outfile, summaryfile, detailfile, minagegrade, minraces, mintrend, begindate, enddate):
    """
    render collected results

    :param outfile: output file name template, like '{who}-ag-analysis-{date}-{time}.png'
    :param summaryfile: summary file name template (.csv), may include {date} field
    :param detailfile: summary file name template (.csv), may include {date} field
    :param minagegrade: minimum age grade
    :param minraces: minimum races in the same year as enddate
    :param mintrend: minimum races over the full period for trendline
    :param begindate: render races between begindate and enddate, datetime
    :param enddate: render races between begindate and enddate, datetime
    """
    firstyear = begindate.year
    lastyear = enddate.year
    yearrange = list(range(firstyear, lastyear + 1))
    summfields = [
     'name', 'age', 'gender']
    distcategories = ['overall'] + [TRENDLIMITS[tlimit][0] for tlimit in TRENDLIMITS]
    for stattype in ('1yr agegrade', 'avg agegrade', 'trend', 'numraces', 'stderr',
                     'r-squared', 'pvalue'):
        for distcategory in distcategories:
            summfields.append('{}\n{}'.format(stattype, distcategory))

        if stattype == 'numraces':
            for year in yearrange:
                summfields.append('{}\n{}'.format(stattype, year))

    tfile = timeu.asctime('%Y-%m-%d')
    summaryfname = summaryfile.format(date=(tfile.epoch2asc(time.time())))
    _SUMM = open(summaryfname, 'w', newline='')
    SUMM = csv.DictWriter(_SUMM, summfields)
    SUMM.writeheader()
    detailfname = detailfile.format(date=(tfile.epoch2asc(time.time())))
    detlfields = ['name', 'dob', 'gender'] + analyzeagegrade.AgeGradeStat.attrs + ['distmiles', 'distkm', 'rendertime']
    detlfields.remove('priority')
    _DETL = open(detailfname, 'w', newline='')
    DETL = csv.DictWriter(_DETL, detlfields, extrasaction='ignore')
    DETL.writeheader()
    fig = plt.figure()
    for thisname in aag:
        rendername = thisname.title()
        aag[thisname].deduplicate()
        aag[thisname].crunch()
        stats = aag[thisname].get_stats()
        name, gender, dob = aag[thisname].get_runner()
        detlout = {'name':rendername,  'gender':gender,  'dob':tfile.dt2asc(dob)}
        for stat in stats:
            for attr in analyzeagegrade.AgeGradeStat.attrs:
                detlout[attr] = getattr(stat, attr)
                if attr == 'date':
                    detlout[attr] = tfile.dt2asc(detlout[attr])

            detlout['distkm'] = detlout['dist'] / 1000.0
            detlout['distmiles'] = detlout['dist'] / METERSPERMILE
            rendertime = ren.rendertime(detlout['time'], 0)
            while len(rendertime.split(':')) < 3:
                rendertime = '0:' + rendertime

            detlout['rendertime'] = rendertime
            DETL.writerow(detlout)

        jan1 = tfile.asc2dt('{}-1-1'.format(lastyear))
        runnerage = timeu.age(jan1, dob)
        if runnerage < 14:
            continue
        stats = aag[thisname].get_stats()
        if enddate:
            lastyear = enddate.year
        else:
            lastyear = timeu.epoch2dt(time.time()).year
        lastyearstats = [s for s in stats if s.date.year == lastyear]
        if len(lastyearstats) < minraces:
            continue
        if outfile:
            aag[thisname].set_renderfname(outfile)
        aag[thisname].set_xlim(begindate, enddate)
        aag[thisname].set_ylim(minagegrade, 100)
        aag[thisname].set_colormap([200, 100 * METERSPERMILE])
        fig.clear()
        ax = fig.add_subplot(111)
        aag[thisname].render_stats(fig)
        avg = collections.OrderedDict()
        allstats = aag[thisname].get_stats()
        avg['overall'] = mean([s.ag for s in allstats])
        trend = aag[thisname].render_trendline(fig, 'overall', color='k')
        thisoutfile = aag[thisname].get_outfilename()
        summout = {}
        summout['name'] = '=HYPERLINK("{}","{}")'.format(thisoutfile, rendername)
        summout['age'] = runnerage
        summout['gender'] = gender
        oneyrstats = [s.ag for s in allstats if s.date.year == lastyear]
        if len(oneyrstats) > 0:
            summout['1yr agegrade\noverall'] = mean(oneyrstats)
        summout['avg agegrade\noverall'] = avg['overall']
        if len(allstats) >= mintrend:
            summout['trend\noverall'] = trend.slope
            summout['stderr\noverall'] = trend.stderr
            summout['r-squared\noverall'] = trend.rvalue ** 2
            summout['pvalue\noverall'] = trend.pvalue
        summout['numraces\noverall'] = len(allstats)
        for year in yearrange:
            summout['numraces\n{}'.format(year)] = len([s for s in allstats if s.date.year == year])

        for tlimit in TRENDLIMITS:
            distcategory, distcolor = TRENDLIMITS[tlimit]
            tstats = [s for s in allstats if s.dist >= tlimit[0] if s.dist <= tlimit[1]]
            if len(tstats) < mintrend:
                continue
            avg[distcategory] = mean([s.ag for s in tstats])
            trend = aag[thisname].render_trendline(fig, distcategory, thesestats=tstats, color=distcolor)
            oneyrcategory = [s.ag for s in tstats if s.date.year == lastyear]
            if len(oneyrcategory) > 0:
                summout['1yr agegrade\n{}'.format(distcategory)] = mean(oneyrcategory)
            summout['avg agegrade\n{}'.format(distcategory)] = avg[distcategory]
            summout['trend\n{}'.format(distcategory)] = trend.slope
            summout['stderr\n{}'.format(distcategory)] = trend.stderr
            summout['r-squared\n{}'.format(distcategory)] = trend.rvalue ** 2
            summout['pvalue\n{}'.format(distcategory)] = trend.pvalue
            summout['numraces\n{}'.format(distcategory)] = len(tstats)

        SUMM.writerow(summout)
        avgstr = 'averages\n'
        for lab in avg:
            thisavg = int(round(avg[lab]))
            avgstr += '  {}: {}%\n'.format(lab, thisavg)

        avgstr += 'age (1/1/{}): {}'.format(lastyear, runnerage)
        x1, xn = ax.get_xlim()
        y1, yn = ax.get_ylim()
        xy = (x1 + 10, y1 + 10)
        aag[thisname].render_annotate(fig, avgstr, xy)
        aag[thisname].save(fig)

    _SUMM.close()
    _DETL.close()


def main():
    descr = '\n    render race results from athlinks, club\n    '
    parser = argparse.ArgumentParser(description=descr, formatter_class=(argparse.RawDescriptionHelpFormatter), version=('{0} {1}'.format('running', version.__version__)))
    parser.add_argument('-c', '--clubfile', help='file with club results, output from exportresults', default=None)
    parser.add_argument('-a', '--athlinksfile', help='file with athlinks results, output from athlinksresults', default=None)
    parser.add_argument('-u', '--ultrasignupfile', help='file with club results, output from ultrasignupresults', default=None)
    parser.add_argument('-R', '--runningaheadfile', help='file with club results, output from runningaheadresults', default=None)
    parser.add_argument('-o', '--outfile', help="output file name template, like '{who}-ag-analysis-{date}-{time}.png', default=%(default)s", default='{who}-ag-analysis-{date}.png')
    parser.add_argument('-s', '--summaryfile', help='summary file name template, default=%(default)s', default='ag-analysis-summary-{date}.csv')
    parser.add_argument('-d', '--detailfile', help='detail file name template, default=%(default)s', default='ag-analysis-detail-{date}.csv')
    parser.add_argument('-g', '--minagegrade', help='minimum age grade for charts, default=%(default)s', default=25)
    parser.add_argument('-r', '--minraces', help='minimum races in the same year as ENDDATE, default=%(default)s', default=3)
    parser.add_argument('-t', '--mintrend', help='minimum races between BEGINDATE and ENDDATE for trendline, default=%(default)s', default=5)
    parser.add_argument('-b', '--begindate', help='render races between begindate and enddate, yyyy-mm-dd', default=None)
    parser.add_argument('-e', '--enddate', help='render races between begindate and enddate, yyyy-mm-dd', default=None)
    args = parser.parse_args()
    athlinksfile = args.athlinksfile
    ultrasignupfile = args.ultrasignupfile
    runningaheadfile = args.runningaheadfile
    clubfile = args.clubfile
    outfile = args.outfile
    summaryfile = args.summaryfile
    detailfile = args.detailfile
    minagegrade = args.minagegrade
    minraces = args.minraces
    mintrend = args.mintrend
    argtime = timeu.asctime('%Y-%m-%d')
    if args.begindate:
        begindate = argtime.asc2dt(args.begindate)
    else:
        begindate = None
    if args.enddate:
        tmpenddate = argtime.asc2dt(args.enddate)
        enddate = datetime.datetime(tmpenddate.year, tmpenddate.month, tmpenddate.day, 23, 59, 59)
    else:
        enddate = None
    aag = {}
    if not athlinksfile:
        if not clubfile:
            if not ultrasignupfile:
                if not runningaheadfile:
                    raise invalidParameter('athlinksfile, ultrasignupfile, runningaheadfile and/or clubfile required')
    if athlinksfile:
        collectathlinks(aag, athlinksfile)
    if ultrasignupfile:
        collectultrasignup(aag, ultrasignupfile)
    if runningaheadfile:
        collectrunningahead(aag, runningaheadfile)
    if clubfile:
        collectclub(aag, clubfile)
    render(aag, outfile, summaryfile, detailfile, minagegrade, minraces, mintrend, begindate, enddate)


if __name__ == '__main__':
    main()