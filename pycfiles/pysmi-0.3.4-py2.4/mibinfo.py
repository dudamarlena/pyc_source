# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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