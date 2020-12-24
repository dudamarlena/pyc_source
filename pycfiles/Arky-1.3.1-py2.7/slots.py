# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arky\slots.py
# Compiled at: 2017-10-17 14:00:10
from . import cfg
import datetime, pytz

def getTimestamp(**kw):
    delta = datetime.timedelta(**kw)
    return getTime(datetime.datetime.now(pytz.UTC) - delta)


def getTime(time=None):
    delta = ((time or datetime.datetime.now)(pytz.UTC) if 1 else time) - cfg.begintime
    return delta.total_seconds()


def getRealTime(epoch=None):
    epoch = getTime() if epoch == None else epoch
    return cfg.begintime + datetime.timedelta(seconds=epoch)


def getSlot(epoch=None):
    epoch = getTime() if epoch == None else epoch
    return int(epoch // cfg.blocktime)


def getSlotTime(slot):
    return slot * cfg.blocktime


def getSlotRealTime(slot):
    return getRealTime(slot * cfg.blocktime)


def getLastSlot(slot):
    return slot + cfg.delegate