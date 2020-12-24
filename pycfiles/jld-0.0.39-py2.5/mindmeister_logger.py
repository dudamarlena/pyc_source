# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\backup\mindmeister_logger.py
# Compiled at: 2009-01-13 14:40:20
"""
    MinMeister Logger
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: mindmeister_logger.py 729 2008-12-11 18:30:12Z jeanlou.dupont $'
import logging, logging.handlers

def Logger(console_quiet=False, syslog_address='/dev/log/mm.log'):
    """ Builds a Logger
        By default, outputs to stdout & syslog
        
        @param console_quiet: if True, disables logging to stdout
        @param syslog_address: the address to use for syslog
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s: %(message)s ', datefmt='%y-%m-%d %H:%M')
    hconsole = logging.StreamHandler()
    hsyslog = logging.handlers.SysLogHandler(address=syslog_address)
    loggr = logging.getLogger('')
    loggr.addHandler(hconsole)
    loggr.addHandler(hsyslog)
    return loggr


if __name__ == '__main__':
    log = Logger()
    log.info('test')