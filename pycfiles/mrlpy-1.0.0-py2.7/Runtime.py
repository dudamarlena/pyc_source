# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/org/myrobotlab/service/Runtime.py
# Compiled at: 2017-06-05 00:11:16
from mrlpy import mcommand
from Test import Test
compatMode = False
compatObj = None

def createAndStart(name, type):
    return mcommand.callService('runtime', 'createAndStart', [name, type])


def shutdown():
    mcommand.sendCommand('runtime', 'shutdown', [])


def getRuntime():
    return mcommand.callService('runtime', 'start', ['runtime', 'Runtime'])


def start(name, type):
    return mcommand.callService('runtime', 'start', [name, type])


def setCompat(mode):
    global compatMode
    compatMode = mode


def setCompatServiceObject(obj):
    global compatObj
    compatObj = obj