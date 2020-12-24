# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/current_time.py
# Compiled at: 2012-02-11 12:17:52
import datetime

class CurrentTime(object):

    def __str__(self):
        return datetime.datetime.now().strftime('%c')

    def __repr__(self):
        return ('CurrentTime({})').format(self)

    @staticmethod
    def name():
        return 'linseed_current_time'

    @staticmethod
    def description():
        return 'Current timestamp'