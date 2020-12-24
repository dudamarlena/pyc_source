# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nettools/provider/Provider.py
# Compiled at: 2017-04-03 08:47:09
import logging
from types import *
logger = logging.getLogger('net-tools')

class Provider(object):

    def __init__(self):
        self.regions = {}
        self.vpcs = {}
        self.subnets = {}
        self.instances = {}

    def discover(self, region_names=None):
        """
        @return: None
        """
        pass

    def listRegions(self, region_name=None):
        """
        @return: dictionary
        """
        return self.regions

    def listAvailabilityZones(self, region_name):
        """
        List AvailabilityZones of Regions
        @return: dictionary
        """
        pass

    def listVpcs(self, region_name):
        """
        List Vpcs of region
        @return: dictionary
        """
        pass

    def formatVpcs(self, region_name=None):
        pass

    def getValue(self, dic, name):
        """
        @param dic: dictionary
        @param name : key
        @return: dic[name]
        """
        if type(dic) != DictType:
            logger.error('%s is not Dictionary type' % dic)
            return None
        else:
            if dic.has_key(name) == False:
                logger.error('Dic does not have key:%s' % name)
                return None
            return dic[name]