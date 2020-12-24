# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/git_repos/dryxDropboxCL/dryxDropboxCL/cl_utils.py
# Compiled at: 2016-06-17 05:56:18
"""
*The CL utils for dryxDropboxCL*

:Author:
    David Young

:Date Created:
    September 5, 2014

Usage:
    dryxDropboxCL bump
    dryxDropboxCL resync -s <pathToSettingsFile>

    -h, --help            show this help message
    -v, --version         show version
    -s, --settings        the settings file
"""
import sys, os
from docopt import docopt
from fundamentals import tools, times
from .start_if_not_running import start_if_not_running
from .setup_selective_sync import setup_selective_sync

def main(arguments=None):
    """
    *The main function used when ``cl_utils.py`` is run as a single script from the cl, or when installed as a cl command*
    """
    su = tools(arguments=arguments, docString=__doc__, logLevel='DEBUG')
    arguments, settings, log, dbConn = su.setup()
    for arg, val in arguments.iteritems():
        if arg[0] == '-':
            varname = arg.replace('-', '') + 'Flag'
        else:
            varname = arg.replace('<', '').replace('>', '')
        if isinstance(val, str) or isinstance(val, unicode):
            exec varname + " = '%s'" % (val,)
        else:
            exec varname + ' = %s' % (val,)
        if arg == '--dbConn':
            dbConn = val
        log.debug('%s = %s' % (varname, val))

    startTime = times.get_now_sql_datetime()
    log.info('--- STARTING TO RUN THE cl_utils.py AT %s' % (
     startTime,))
    if 'bump' in locals() and bump:
        start_if_not_running(log=log)
    if 'resync' in locals() and resync:
        setup_selective_sync(log=log, settings=settings)
    if 'dbConn' in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' % (
     endTime, runningTime))


if __name__ == '__main__':
    main()