# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/updater4pyi/upd_log.py
# Compiled at: 2014-12-07 12:31:14
"""
Set up a minimal logger. To integrate logging in your application, configure your Python
`logging`_ as you wish. Updater4Pyi gets its logger by calling
``logging.getLogger('updater4pyi')``, i.e. the Updater4Pyi's logger is called
'updater4pyi'.

.. _logging: https://docs.python.org/2/library/logging.html

"""
import logging
logger = logging.getLogger('updater4pyi')
formatter = logging.Formatter('%(name)s - %(asctime)-15s\n\t%(levelname)s: %(message)s')

def setup_logger(level=logging.INFO):
    """
    A utility function that you can call to set up a simple logging to the console. No
    hassles.
    """
    ch = logging.StreamHandler()
    ch.setLevel(logging.NOTSET)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(level)
    logger.debug('logger set up. level=%d', level)