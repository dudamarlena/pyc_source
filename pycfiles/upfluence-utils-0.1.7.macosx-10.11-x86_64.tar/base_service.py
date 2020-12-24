# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/upfluence/thrift/base_service.py
# Compiled at: 2016-05-06 20:10:26
import os, time, base.base_service.constants, version

class BaseService(object):

    def __init__(self, unit_name=None, interface_modules=[]):
        self._unit_name = unit_name or os.environ.get('UNIT_NAME')
        self._spawn_date = int(time.time())
        self._interface_modules = interface_modules

    def getName(self):
        return self._unit_name

    def getVersion(self):
        return version

    def getStatus(self):
        return base.base_service.constants.status.ALIVE

    def aliveSince(self):
        return self._spawn_date

    def getInterfaceVersion(self):

        def reduce_versions(acc, module):
            acc[module.__name__.split('.')[0]] = module.base_version
            return acc

        return reduce(reduce_versions, self._interface_modules)