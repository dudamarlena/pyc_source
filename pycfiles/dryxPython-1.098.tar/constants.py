# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/constants.py
# Compiled at: 2013-08-06 05:10:43
"""
constants
===============
:Summary:
    Some commonly used constants

:Author:
    David Young

:Date Created:
    March 22, 2013

:dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script please email me: d.r.young@qub.ac.uk
"""
import sys, os

def main():
    """one-line summary

    Key Arguments:
        -
        - dbConn -- mysql database connection
        - log -- logger

    Return:
        - None
    """
    import pesstoMarshallPythonPath as pp
    pp.set_python_path()
    import pmCommonUtils as p, dryxPython.commonutils as cu
    dbConn, log = p.settings()
    startTime = cu.get_now_sql_datetime()
    log.info('--- STARTING TO RUN THE constants AT %s' % (startTime,))
    dbConn.commit()
    dbConn.close()
    endTime = cu.get_now_sql_datetime()
    runningTime = cu.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE constants AT %s (RUNTIME: %s) --' % (endTime, runningTime))


if __name__ == '__main__':
    main()