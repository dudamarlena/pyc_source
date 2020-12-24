# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\tools\logger.py
# Compiled at: 2009-01-20 09:37:44
""" Cross-platform logger
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: logger.py 835 2009-01-20 14:35:48Z JeanLou.Dupont $'
import sys, logging, logging.handlers

def logger(name, include_console=True, include_syslog=True):
    """ Returns a simple cross-platform logger
        E.g.
        log = logger.logger('my_logger')
        log.info('message')
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s: %(message)s ')
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s: %(message)s ')
    syslog = xcLogger(name)
    syslog.setFormatter(formatter)
    _logger = logging.getLogger(name)
    if include_syslog:
        _logger.addHandler(syslog)
    if include_console:
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        _logger.addHandler(console)
    return _logger


def xcLogger(appname):
    """ Cross-platform log handler
        Returns a NTEventLogHandler for win32 platform
        Returns a SysLogHandler for *nix platform
    """
    if sys.platform[:3] == 'win':
        return logging.handlers.NTEventLogHandler(appname)
    return logging.handlers.TimedRotatingFileHandler('/var/log/%s.log' % appname)


if __name__ == '__main__':
    log = logger('Test_xcLogger', True)
    log.info('TestMessage')
    log = logger('Test_xcLogger2', False, False)
    log.info('TestMessage2')
    log = logger('Test_xcLogger3', False, True)
    log.info('TestMessage3')