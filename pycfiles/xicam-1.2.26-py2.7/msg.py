# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\msg.py
# Compiled at: 2018-08-27 17:21:06
import logging, inspect, sys, time
statusbar = None
progressbar = None
stdch = logging.StreamHandler(sys.stdout)
guilogcallable = None
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
logbacklog = []

def showProgress(value, min=0, max=100):
    if progressbar:
        progressbar.show()
        progressbar.setRange(min, max)
        progressbar.setValue(value)


def showBusy():
    if progressbar:
        progressbar.show()
        progressbar.setRange(0, 0)


def hideBusy():
    if progressbar:
        progressbar.hide()
        progressbar.setRange(0, 100)


hideProgress = hideBusy

def showMessage(s, timeout=0):
    if statusbar is not None:
        statusbar.showMessage(s, timeout * 1000)
    logMessage(s)
    return


def logMessage(stuple, level=INFO, loggername=None, timestamp=None, image=None, suppressreprint=False):
    global logbacklog
    if loggername is not None:
        loggername = inspect.stack()[1][3]
    logger = logging.getLogger(loggername)
    try:
        stdch.setLevel(level)
    except ValueError:
        print stuple, level

    logger.addHandler(stdch)
    if timestamp is None:
        timestamp = time.asctime()
    if type(stuple) is not tuple:
        stuple = [
         stuple]
    stuple = (unicode(s) for s in stuple)
    s = (' ').join(stuple)
    m = timestamp + '\t' + unicode(s)
    logger.log(level, m)
    if guilogcallable:
        guilogcallable(level, timestamp, s, image)
    else:
        logbacklog.append({'stuple': s, 'level': level, 'loggername': loggername, 'timestamp': timestamp, 'image': image})
    try:
        if not suppressreprint:
            print m
    except UnicodeEncodeError:
        print 'A unicode string could not be written to console. Some logging will not be displayed.'

    return


def flushbacklog():
    global logbacklog
    for l in logbacklog:
        l['suppressreprint'] = True
        logMessage(**l)

    logbacklog = []


def clearMessage():
    statusbar.clearMessage()