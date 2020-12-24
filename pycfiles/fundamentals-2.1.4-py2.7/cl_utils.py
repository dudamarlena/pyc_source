# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/cl_utils.py
# Compiled at: 2020-04-30 14:03:27
"""
Documentation for fundamentals can be found here: http://fundamentals.readthedocs.org

Usage:
    fundamentals init
    fundamentals [-s <pathToSettingsFile>]  

Options:
    init                                   setup the fundamentals settings file for the first time
    -h, --help                             show this help message
    -v, --version                          show version
    -s, --settings <pathToSettingsFile>    the settings file
"""
import sys, os
os.environ['TERM'] = 'vt100'
import readline, glob, pickle
from docopt import docopt
from fundamentals import tools, times
from subprocess import Popen, PIPE, STDOUT

def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]


def main(arguments=None):
    """
    *The main function used when `cl_utils.py` is run as a single script from the cl, or when installed as a cl command*
    """
    su = tools(arguments=arguments, docString=__doc__, logLevel='WARNING', options_first=False, projectName='fundamentals', defaultSettingsFile=True)
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
        filepath = home + '/.config/fundamentals/fundamentals.yaml'
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
    if 'dbConn' in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' % (
     endTime, runningTime))


if __name__ == '__main__':
    main()