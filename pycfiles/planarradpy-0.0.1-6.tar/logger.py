# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marrabld/Projects/planarradpy/libplanarradpy/logger.py
# Compiled at: 2015-05-30 00:32:37
__author__ = 'marrabld'
import logging.config, os
log_conf_file = os.path.join(os.path.dirname(__file__), 'logging.conf')
print log_conf_file
logging.config.fileConfig(log_conf_file)
logger = logging.getLogger('libplanarradpy')

def clear_log():
    """
    This method will clear the log file by reopening the file for writing.
    """
    with open('libplanarradpy.log', 'w'):
        pass


def clear_err():
    """
    This method will clear the log file by reopening the file for writing.
    """
    with open('libplanarradpy.err', 'w'):
        pass