# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\debugtools.py
# Compiled at: 2018-08-27 17:21:07
import time, inspect, pyqtgraph as pg, numpy as np
from pipeline import msg

def timeit(method):
    """
    Use this as a decorator to time a function
    """

    def timed(*args, **kw):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        msg.logMessage('%r  %2.3f sec' % (
         method.__name__, te - ts), msg.DEBUG)
        return result

    return timed


def frustration():
    msg.logMessage('(ﾉಥ益ಥ)ﾉ\ufeff ┻━┻', msg.CRITICAL)


def showimage(img):
    image = pg.image(np.fliplr(img))