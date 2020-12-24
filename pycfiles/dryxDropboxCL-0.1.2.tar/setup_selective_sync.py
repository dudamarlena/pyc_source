# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/git_repos/dryxDropboxCL/dryxDropboxCL/setup_selective_sync.py
# Compiled at: 2016-06-17 04:40:55
"""
*Setup the selective sync with dropbox -- using a list of included folders, will exclude all others*

:Author:
    David Young

:Date Created:
    September 8, 2014

.. todo::
    
    @review: when complete pull all general functions and classes into dryxPython
"""
import sys, os
from docopt import docopt
from fundamentals import tools, times
from dryxDropboxCL import start_if_not_running
from dryxDropboxCL.original import dropbox

def main(arguments=None):
    """
    *The main function used when ``setup_selective_sync.py`` is run as a single script from the cl, or when installed as a cl command*
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
    log.info('--- STARTING TO RUN THE setup_selective_sync.py AT %s' % (
     startTime,))
    setup_selective_sync(log=log, settings=settings)
    if 'dbConn' in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE setup_selective_sync.py AT %s (RUNTIME: %s) --' % (
     endTime, runningTime))


def setup_selective_sync(log, settings):
    """
    *setup selective sync*

    **Key Arguments:**
        - ``log`` -- logger

    **Return:**
        - None

    .. todo::

        - @review: when complete, clean setup_selective_sync function
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract function to another module
    """
    log.info('starting the ``setup_selective_sync`` function')
    start_if_not_running.start_if_not_running(log=log)
    with dropbox.closing(dropbox.DropboxCommand()) as (dc):
        try:
            log.debug('attempting to list dropbox excluded folders')
            currentlyExcluded = dc.get_ignore_set()['ignore_set']
        except Exception as e:
            log.error('could not list dropbox excluded folders - failed with this error: %s ' % (str(e),))
            return

    log.debug('currentlyExcluded: %(currentlyExcluded)s' % locals())
    dropboxPath = settings['dropbox path']
    basePath = dropboxPath
    tmpCurrentlyIncluded = os.listdir(basePath)
    currentlyIncluded = []
    currentlyIncluded[:] = [ '%(dropboxPath)s/%(c)s' % locals() for c in tmpCurrentlyIncluded ]
    log.debug('currentlyIncluded: %(currentlyIncluded)s' % locals())
    settingsIncludedFolders = settings['dropbox folders to sync']
    shouldBeincludedFolders = []
    shouldBeincludedFolders[:] = [ '%(dropboxPath)s/%(i)s' % locals() for i in settingsIncludedFolders ]
    log.debug('settingsIncludedFolders: %(settingsIncludedFolders)s' % locals())
    settingsExcludedFolders = settings['dropbox folders to unsync']
    shouldBeExcludedFolders = []
    shouldBeExcludedFolders[:] = [ '%(dropboxPath)s/%(i)s' % locals() for i in settingsExcludedFolders ]
    log.debug('settingsExcludedFolders: %(settingsExcludedFolders)s' % locals())
    for include in shouldBeincludedFolders:
        if include.lower() in [ l.lower() for l in currentlyExcluded ]:
            log.debug('SHOULD NOT BE EXCLUDED: %(include)s' % locals())
            dropbox.exclude(['remove', include])

    for exclude in shouldBeExcludedFolders:
        if exclude.lower() not in [ l.lower() for l in currentlyExcluded ]:
            log.debug('SHOULD BE EXCLUDED: %(exclude)s' % locals())
            dropbox.exclude(['add', exclude])

    for currentInclude in currentlyIncluded:
        if currentInclude.lower() not in [ l.lower() for l in shouldBeincludedFolders ] and 'dropbox.cache' not in currentInclude and '.dropbox' not in currentInclude:
            log.debug('SHOULD BE EXCLUDED: %(currentInclude)s' % locals())
            dropbox.exclude(['add', currentInclude])

    log.info('completed the ``setup_selective_sync`` function')
    return


if __name__ == '__main__':
    main()