# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/log.py
# Compiled at: 2010-10-14 14:04:23
"""
Logging

NOTE(g): Logging is currently a thin shell.  Will flush out with previous
code with real depth shortly.

TODO(g): Many more things for system-wide logging.  This will handle many
different streams of logging that may be required by unidist based programs,
which are small and numerous.
"""
import sys, logging, logging.handlers, time, os, stack
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
ALERT = 100
LOG_FUNCTION = {DEBUG: 'debug', 
   INFO: 'info', 
   WARN: 'warn', 
   ERROR: 'error', 
   CRITICAL: 'critical', 
   ALERT: 'critical'}
DEFAULT_LOG_LEVEL = DEBUG
DEFAULT_LOG_FILE = 'procblock.log'
LOG_TO_STDOUT = True
LOGGER = None
DISABLE_LOGGING = False

def SetLogFile(path):
    global DEFAULT_LOG_FILE
    DEFAULT_LOG_FILE = path


def Disable():
    """Logging will be disabled for this program.  Do not run for REM Client."""
    global DISABLE_LOGGING
    DISABLE_LOGGING = True


def _GetLogger():
    """Gets a singleton logger."""
    global LOGGER
    log_file = DEFAULT_LOG_FILE
    MAX_FILESIZE = 10485760
    MAX_BACKUPS = 5
    if not LOGGER:
        LOGGER = logging.getLogger('procblock')
        LOGGER.setLevel(DEFAULT_LOG_LEVEL)
        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=MAX_FILESIZE, backupCount=MAX_BACKUPS)
        LOGGER.addHandler(handler)
    return LOGGER


def log(text, level=DEFAULT_LOG_LEVEL):
    """Log data."""
    if DISABLE_LOGGING:
        return
    logger = _GetLogger()
    text = '%s:%s: %s' % (GetTimeStamp(), stack.Mini(1, 1), text)
    func_name = LOG_FUNCTION[level]
    func = getattr(logger, func_name)
    console_out = '%s:%s' % (LOG_FUNCTION[level].upper(), text)
    sys.stderr.write(console_out + '\n')
    sys.stderr.flush()
    if level in (CRITICAL, ALERT):
        Alert(text)
    func(text)


ALERT_CACHE = {}
ALERT_DELAY = 1800

def Alert(text):
    """Alert that something critical happened inside REM."""
    global ALERT_CACHE
    global ALERT_DELAY
    if text not in ALERT_CACHE or ALERT_CACHE[text]['last_alerted'] + ALERT_DELAY < time.time():
        if text not in ALERT_CACHE:
            ALERT_CACHE[text] = {'last_alerted': None, 'count': 0}
        ALERT_CACHE[text]['last_alerted'] = time.time()
        ALERT_CACHE[text]['count'] += 1
        log('Todo(g): ALERT: %s' % text)
    return


def GetTimeStamp(minutes=True, seconds=True):
    """Gets time stamps, for use in dating backup files and other things."""
    import time
    (year, month, day, hour, minute, second, _, _, _) = time.localtime()
    if seconds:
        output = '%02d%02d%02d%02d%02d%02d' % (year, month, day, hour, minute, second)
    elif minutes:
        output = '%02d%02d%02d%02d%02d' % (year, month, day, hour, minute)
    else:
        output = '%02d%02d%02d%02d' % (year, month, day, hour)
    return output


if __name__ == '__main__':

    def TestMe():
        for count in range(0, 5):
            log('Bingo: %d!' % count)


    TestMe()