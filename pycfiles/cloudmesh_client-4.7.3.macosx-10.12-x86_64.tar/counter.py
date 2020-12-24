# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/counter.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.db import CloudmeshDatabase

class Counter(object):
    """
    A counter is used to keep track of some value that can be increased
    and is associated with a user. Typically it is used to increment the
    vm id or the job id.
    """
    cm = CloudmeshDatabase()

    @classmethod
    def incr(cls, name='counter', user=None):
        """
        increments the counter by one

        :param name: name of the counter
        :param user: username associated with the counter
        :return:
        """
        cls.cm.counter_incr(name=name, user=user)

    @classmethod
    def get(cls, name='counter', user=None):
        """
        returns the value of the counter

        :param name: name of the counter
        :param user: username associated with the counter
        :return: the value of the counter
        """
        return cls.cm.counter_get(name=name, user=user)

    @classmethod
    def set(cls, name='counter', value=None, user=None):
        """
        sets a counter associated with a particular user
        :param name: name of the counter
        :param user: username associated with the counter
        :param value: the value
        :return:
        """
        cls.cm.counter_set(name=name, value=value, user=user)