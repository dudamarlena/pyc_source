# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/tests/tlib.py
# Compiled at: 2010-01-24 10:23:30
import os
from random import randint

class FileObject(object):
    pass


class MultiDict(object):

    def __init__(self):
        self.fields = []

    def get(self, item, default=None):
        for (itm, v) in self.fields:
            if itm == item:
                rvalue = v
                break
        else:
            rvalue = default

        return rvalue

    def getall(self, item, default=[]):
        rvalue = []
        for (itm, v) in self.fields:
            if itm == item:
                rvalue.append(v)

        rvalue = rvalue or default
        return rvalue

    def add(self, item, value):
        self.fields.append((item, value))

    def clearfields(self):
        self.fields = []


class RequestObject(object):

    def __init__(self):
        self.POST = MultiDict()
        self.params = MultiDict()

    def requestform(self):
        self.params.add('form', 'request')

    def submitform(self):
        self.params.add('form', 'submit')


class ContextObject(object):
    pass


def log_mheader(log, testdir, testfile, seed):
    logthead = '>> Setting up tests for `%s` with seed %s' % (
     os.path.join(testdir, testfile), seed)
    print '\n', logthead
    log.info(logthead)


def log_mfooter(log, testfile, testdir):
    logttail = '>> Tearing down tests for `%s` ' % os.path.join(testdir, testfile)
    print logttail
    log.info(logttail)


def genseed():
    return randint(1, 100000)