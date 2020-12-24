# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/common.py
# Compiled at: 2014-01-02 09:53:02


class CptCommon(object):
    manager = None
    downloadManager = None
    mainWindow = None
    cmdline = None
    config = None
    systray = None
    info = {}


class PreparedCaller(object):

    def __init__(self, function, *args, **kwargs):
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs.update(self._kwargs)
        self._function(*(self._args + args), **kwargs)


def ignoreParams(func):

    def ignorebis(obj, *args, **kwargs):
        func(obj)

    return ignorebis


def ignoreParamsFn(func):

    def ignorebis(*args, **kwargs):
        func()

    return ignorebis