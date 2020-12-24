# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/logtools.py
# Compiled at: 2013-11-12 16:48:22
import logging, tempfile, os, sys, time, traceback
MAX_SIZE = 10000000.0
USE_DBE = False
IS_SETUP = False
LEVEL = None

def setup_logger(level=logging.INFO, filename='python.log', directory=None, format='%(levelname)s:%(name)s.%(funcName)s:%(message)s', ignoresize=False, dbeDisabled=False):
    global IS_SETUP
    global MAX_SIZE
    global USE_DBE
    if IS_SETUP:
        return
    else:
        if directory == None:
            directory = tempfile.gettempdir()
        fullpath = os.path.join(directory, filename)
        size = 0
        try:
            size = os.path.getsize(fullpath)
        except OSError:
            pass

        if size > MAX_SIZE and ignoresize == False:
            os.remove(fullpath)
        logging.basicConfig(filename=fullpath, format=format)
        from logging import handlers
        socketHandler = handlers.SocketHandler('localhost', handlers.DEFAULT_TCP_LOGGING_PORT)
        rootLog = logging.getLogger('')
        rootLog.addHandler(socketHandler)
        IS_SETUP = True
        if level == logging.DEBUG:
            print 'log at: ' + fullpath
            if dbeDisabled == False and USE_DBE == True:
                log_fatal_exception()
        mylog = get_logger('LogStart')
        mylog.setLevel(level)
        mylog.info(('\n{0:*^80}').format(' ##$ LOGGING STARTED ' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()) + ' $## '))
        return


def get_logger(logname=None, modname=None, funname=None, level=logging.INFO, dbeDisabled=False):
    """returns a logger with logname that will print to the temporary directory.
   If level is == logging.DEBUG it will automatically do post-exception 
   logging, and go into dbe (unless dbeDisabled is set).  In this way, the 
   operation of all my debugging can be set by a single variable."""
    if IS_SETUP == False:
        setup_logger(level=level, dbeDisabled=dbeDisabled)
    while logname == None:
        stack = traceback.extract_stack()
        if len(stack) < 2:
            funame, modname = ('unknown', 'unknown')
        else:
            stack = stack[(-2)]
        if funname == None:
            funname = stack[2] if not None else 'unknown'
        if modname == None:
            modname = ('').join(os.path.basename(stack[0]).split('.')[:-1]) if not None else 'unknown'
        logname = modname + '.' + funname
        break

    mylog = logging.getLogger(logname)
    mylog.setLevel(level)
    return mylog


def log_fatal_exception():
    """will log the exception on sys.excepthook"""

    def except_hook(exctype, value, tb):
        if previous_except_hook:
            previous_except_hook(exctype, value, tb)
        log = getLogger('FATAL_EXCEPTION')
        log.critical(str(exctype) + '\n' + str(value) + '\n' + ('').join(traceback.format_tb(tb)))

    previous_except_hook = sys.excepthook
    sys.excepthook = except_hook


if __name__ == '__main__':
    log = get_logger(__name__, level=logging.DEBUG)
    log.info('working?')
    log.info('yes, seems to be working')
    log2 = get_logger(__name__)
    log2.info('still working?')
    x = 1 / 0
# global LEVEL ## Warning: Unused global