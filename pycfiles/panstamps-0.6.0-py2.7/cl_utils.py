# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/panstamps/cl_utils.py
# Compiled at: 2020-05-07 14:43:36
"""
Documentation for panstamps can be found here: http://panstamps.readthedocs.org/en/stable

Usage:
    panstamps [options] [--width=<arcminWidth>] [--filters=<filterSet>] [--settings=<pathToSettingsFile>] [--downloadFolder=<path>] (warp|stack) <ra> <dec> [<mjdStart> <mjdEnd>]
    panstamps [options] --closest=<beforeAfter> [--width=<arcminWidth>] [--filters=<filterSet>] [--settings=<pathToSettingsFile>] [--downloadFolder=<path>] <ra> <dec> <mjd>

    -h, --help                              show this help message
    -f, --fits                              download fits (default on)
    -F, --nofits                            don't download fits (default off)
    -j, --jpeg                              download jepg (default off)
    -J, --nojpeg                            don't download jepg (default on)
    -c, --color                             download color jepg (default off)
    -C, --nocolor                           don't download color jepg (default on)
    -a, --annotate                          annotate jpeg (default true)
    -A, --noannotate                        don't annotate jpeg (default false)
    -t, --transient                         add a small red circle at transient location (default false)
    -T, --notransient                       don't add a small red circle at transient location (default true)
    -g, --greyscale                         convert jpeg to greyscale (default false)
    -G, --nogreyscale                       don't convert jpeg to greyscale (default true)
    -i, --invert                            invert jpeg colors (default false)
    -I, --noinvert                          don't invert jpeg colors (default true)
    --width=<arcminWidth>                   width of image in arcsec (default 1)
    --filters=<filterSet>                   filter set to download and use for color image (default gri)
    --downloadFolder=<path>                 path to the download folder, relative or absolute (folder created where command is run if not set)
    --settings=<pathToSettingsFile>         the settings file    
    --closest=<beforeAfter>                 return the warp closest in time to the given mjd. If you want to set a strict time window then pass in a positive or negative time in sec (before | after | secs)

    ra                                      right-ascension in sexagesimal or decimal degrees
    dec                                     declination in sexagesimal or decimal degrees
    mjdStart                                the start of the time-window within which to select images
    mjdEnd                                  the end of the time-window within which to select images
    mjd                                     report the warp closest in time to this mjd
"""
import sys, os
os.environ['TERM'] = 'vt100'
import readline, glob, pickle
from docopt import docopt
from fundamentals import tools, times
from subprocess import Popen, PIPE, STDOUT
from panstamps.downloader import downloader
from panstamps.image import image

def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]


def main(arguments=None):
    """
    *The main function used when `cl_utils.py` is run as a single script from the cl, or when installed as a cl command*
    """
    su = tools(arguments=arguments, docString=__doc__, logLevel='WARNING', options_first=True, projectName='panstamps', defaultSettingsFile=True)
    arguments, settings, log, dbConn = su.setup()
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind('tab: complete')
    readline.set_completer(tab_complete)
    a = {}
    for arg, val in list(arguments.items()):
        if arg[0] == '-':
            varname = arg.replace('-', '') + 'Flag'
        else:
            varname = arg.replace('<', '').replace('>', '')
        a[varname] = val
        if arg == '--dbConn':
            dbConn = val
            a['dbConn'] = val
        log.debug('%s = %s' % (varname, val))

    startTime = times.get_now_sql_datetime()
    log.info('--- STARTING TO RUN THE cl_utils.py AT %s' % (
     startTime,))
    if 'interactiveFlag' in a and a['interactiveFlag']:
        moduleDirectory = os.path.dirname(__file__) + '/resources'
        pathToPickleFile = '%(moduleDirectory)s/previousSettings.p' % locals()
        try:
            with open(pathToPickleFile):
                pass
            previousSettingsExist = True
        except:
            previousSettingsExist = False

        previousSettings = {}
        if previousSettingsExist:
            previousSettings = pickle.load(open(pathToPickleFile, 'rb'))
        pickleMeObjects = []
        pickleMe = {}
        theseLocals = locals()
        for k in pickleMeObjects:
            pickleMe[k] = theseLocals[k]

        pickle.dump(pickleMe, open(pathToPickleFile, 'wb'))
    if a['init']:
        from os.path import expanduser
        home = expanduser('~')
        filepath = home + '/.config/panstamps/panstamps.yaml'
        try:
            cmd = 'open %(filepath)s' % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass

        try:
            cmd = 'start %(filepath)s' % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass

        return
    fitsFlag = a['fitsFlag']
    nofitsFlag = a['nofitsFlag']
    jpegFlag = a['jpegFlag']
    nojpegFlag = a['nojpegFlag']
    colorFlag = a['colorFlag']
    nocolorFlag = a['nocolorFlag']
    annotateFlag = a['annotateFlag']
    noannotateFlag = a['noannotateFlag']
    transientFlag = a['transientFlag']
    notransientFlag = a['notransientFlag']
    greyscaleFlag = a['greyscaleFlag']
    nogreyscaleFlag = a['nogreyscaleFlag']
    invertFlag = a['invertFlag']
    noinvertFlag = a['noinvertFlag']
    widthFlag = a['widthFlag']
    filtersFlag = a['filtersFlag']
    downloadFolderFlag = a['downloadFolderFlag']
    closestFlag = a['closestFlag']
    ra = a['ra']
    dec = a['dec']
    mjdStart = a['mjdStart']
    mjdEnd = a['mjdEnd']
    mjd = a['mjd']
    if ra:
        try:
            ra = float(ra)
        except:
            if ':' not in ra:
                log.error('ERROR: ra must be in decimal degree or sexagesimal format')
                return

    if dec:
        try:
            dec = float(dec)
        except:
            if ':' not in dec:
                log.error('ERROR: dec must be in decimal degree or sexagesimal format')
                return

    kwargs = {}
    kwargs['log'] = log
    kwargs['settings'] = settings
    kwargs['ra'] = ra
    kwargs['dec'] = dec
    kwargs['fits'] = True
    if fitsFlag == False and nofitsFlag == True:
        kwargs['fits'] = False
    kwargs['jpeg'] = False
    if jpegFlag == True and nojpegFlag == False:
        kwargs['jpeg'] = True
    kwargs['color'] = False
    if colorFlag == True and nocolorFlag == False:
        kwargs['color'] = True
    kwargs['arcsecSize'] = 60
    if widthFlag:
        kwargs['arcsecSize'] = float(widthFlag) * 60.0
    kwargs['filterSet'] = 'gri'
    if filtersFlag:
        kwargs['filterSet'] = filtersFlag
    for i in kwargs['filterSet']:
        if i not in 'grizy':
            log.error('ERROR: the requested filter must be in the grizy filter set')
            return

    if stack:
        kwargs['imageType'] = 'stack'
    if warp:
        kwargs['imageType'] = 'warp'
    if closestFlag:
        kwargs['imageType'] = 'warp'
    kwargs['mjdStart'] = mjdStart
    kwargs['mjdEnd'] = mjdEnd
    kwargs['window'] = False
    try:
        kwargs['window'] = int(closestFlag)
    except:
        pass

    if not kwargs['window']:
        if mjd and closestFlag == 'before':
            kwargs['mjdEnd'] = mjd
        elif mjd and closestFlag == 'after':
            kwargs['mjdStart'] = mjd
    else:
        if mjd and kwargs['window'] < 0:
            kwargs['mjdEnd'] = mjd
        elif mjd and kwargs['window'] > 0:
            kwargs['mjdStart'] = mjd
        if downloadFolderFlag:
            home = expanduser('~')
            downloadFolderFlag = downloadFolderFlag.replace('~', home)
        kwargs['downloadDirectory'] = downloadFolderFlag
        images = downloader(**kwargs)
        fitsPaths, jpegPaths, colorPath = images.get()
        jpegPaths += colorPath
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['arcsecSize'] = 60
        if widthFlag:
            kwargs['arcsecSize'] = float(widthFlag) * 60.0
        kwargs['crosshairs'] = True
        kwargs['scale'] = True
        if annotateFlag == False and noannotateFlag == True:
            kwargs['crosshairs'] = False
            kwargs['scale'] = False
        kwargs['invert'] = False
        if invertFlag == True and noinvertFlag == False:
            kwargs['invert'] = True
        kwargs['greyscale'] = False
        if greyscaleFlag == True and nogreyscaleFlag == False:
            kwargs['greyscale'] = True
        kwargs['transient'] = False
        if transientFlag == True and notransientFlag == False:
            kwargs['transient'] = True
        for j in jpegPaths:
            kwargs['imagePath'] = j
            oneImage = image(**kwargs)
            oneImage.get()

    if 'dbConn' in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' % (
     endTime, runningTime))


if __name__ == '__main__':
    main()