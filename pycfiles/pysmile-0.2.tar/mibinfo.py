# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/mibinfo.py
# Compiled at: 2018-12-29 12:21:47


class MibInfo(object):
    __module__ = __name__
    name = ''
    alias = ''
    path = ''
    file = ''
    mtime = 0
    oid = ''
    revision = None
    oids = ()
    identity = ''
    enterprise = ()
    compliance = ()
    imported = ()

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])