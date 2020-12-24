# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/T_Aylott/Documents/Life/Job Applications/Bugsnag/Technical Challenge/Library/tinycrashreporter/tinycrashreporter/__init__.py
# Compiled at: 2017-05-27 06:16:45


def crashReportExceptHook(exctype, value, tb):
    try:
        print ('{0}: {1}').format(exctype.__name__, value)
    except:
        raise Exception('Unexpected error in Tiny Crash Reporter.')