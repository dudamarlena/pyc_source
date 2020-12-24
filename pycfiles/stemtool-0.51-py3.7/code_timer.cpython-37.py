# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/stemtool/code_timer.py
# Compiled at: 2020-05-01 17:03:36
# Size of source mod 2**32: 845 bytes
import time

def TicTocGenerator():
    """
    Generator that returns time differences
    """
    time_initl = 0
    time_final = time.time()
    while True:
        time_initl = time_final
        time_final = time.time()
        yield time_final - time_initl


TicToc = TicTocGenerator()

def toc(tempBool=True):
    """
    Prints the time difference yielded by generator instance TicToc
    """
    tempTimeInterval = next(TicToc)
    if tempBool:
        print('Elapsed time: %f seconds.\n' % tempTimeInterval)


def tic():
    """ 
    Starts the timer
    Records a time in TicToc, marks the beginning of a time interval
    """
    toc(False)