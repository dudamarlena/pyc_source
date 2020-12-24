# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/git_repos/dryxDropboxCL/dryxDropboxCL/start_if_not_running.py
# Compiled at: 2016-06-17 04:40:52
"""
*Start dropbox daemon if not running*

:Author:
    David Young

:Date Created:
    September 5, 2014

.. todo::
    
    @review: when complete pull all general functions and classes into dryxPython
"""
import sys, os, time
from docopt import docopt
from fundamentals import tools, times
from .original import dropbox

def start_if_not_running(log):
    """
    *start if not running*

    **Key Arguments:**
        - ``log`` -- logger

    **Return:**
        - None

    .. todo::

        - @review: when complete, clean start_if_not_running function
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract function to another module
    """
    log.info('starting the ``start_if_not_running`` function')
    isRunning = dropbox.is_dropbox_running()
    if isRunning is False:
        log.warning('dropbox was not running - starting now' % locals())
        try:
            log.debug('attempting to start dropbox')
            dropbox.start([])
            time.sleep(10)
        except Exception as e:
            log.error('could not start dropbox - failed with this error: %s ' % (str(e),))
            return

    else:
        log.info('dropbox is running fine')
    log.info('completed the ``start_if_not_running`` function')
    return


if __name__ == '__main__':
    main()