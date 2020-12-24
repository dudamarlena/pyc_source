# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/vmname.py
# Compiled at: 2017-04-23 10:30:41
from cloudmesh_client.default import Default
from cloudmesh_client.common.ConfigDict import ConfigDict

class VMName(object):

    @staticmethod
    def format(name=None):
        """
        given a name that returns the following information as a tuple.

            prefix - the prefix of the vm name
            index - the current index
            padding - the padding factor to fill the index with leading 0

        The input name format is as follows prefix-0011 upon return you will get

            (prefix, 11, 4)

        if None is specified the current os user name will be used,
        the index will start as 1, and we will use four digits all in all
        for the padding.

        :param name: the name that derives a format for
        :return: prefix, index, padding
        """
        raise ValueError('implement me')

    @staticmethod
    def get(prefix=None, idx=None, user=None):
        """Return a vm name to use next time. prefix or index can be
        given to update a vm name (optional)

        Args:
            prefix (str, optional): the name of prefix
            idx (int, str, optional): the index to increment. This can be a
            digit or arithmetic e.g. +5 or -3 can be used

        """
        user = user or ConfigDict('cloudmesh.yaml')['cloudmesh.profile.user']
        prefix = prefix or user
        if type(idx) is not int:
            idx = int(idx)
        Default.set('index', idx)
        return ('%{:}_%{:}').format()

    @staticmethod
    def next():
        return VMName.vmname(idx='+1')