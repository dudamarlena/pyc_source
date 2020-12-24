# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ucloudclient/api/udisk.py
# Compiled at: 2015-11-11 06:54:58
__author__ = 'hyphen'
from ucloudclient.utils import base

class UdiskManager(base.Manager):
    """
    disk manager class
    """

    def get(self, region, udiskid):
        """

        :param region:
        :param udiskid:
        :return:
        """
        body = {}
        body['Region'] = region
        body['Action'] = 'DescribeUDisk'
        body['UDiskId.0'] = udiskid
        return self._get(body)

    def list(self, region, offset=None, limin=None, projectid=None):
        """

        :param region:
        :param offset:
        :param limin:
        :param projectid:
        :return:
        """
        body = {}
        body['Region'] = region
        body['Action'] = 'DescribeUDisk'
        if offset:
            body['Offset'] = offset
        if limin:
            body['Limit'] = limin
        if projectid:
            body['ProjectId'] = projectid
        return self._get(body)