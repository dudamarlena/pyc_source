# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\tools\debug\memoryprofiler.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'GrosBedo'
__version__ = '0.1.1'
import os, sys
pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(pathname, 'b3', 'lib'))
import threading, time
try:
    from guppy import hpy
except:
    pass

def memoryprofile(val):
    hpy().heap().stat.dump(val)
    time.sleep(0.1)


def runmemoryprofile(val):
    memorythread = threading.Thread(target=memoryprofile, args=(val,))
    memorythread.start()


def memoryinteractive():
    hpy().monitor()


def memorygui(val):
    hpy().pb(val)