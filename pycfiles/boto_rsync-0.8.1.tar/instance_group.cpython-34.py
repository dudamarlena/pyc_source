# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/emr/instance_group.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2079 bytes


class InstanceGroup(object):

    def __init__(self, num_instances, role, type, market, name, bidprice=None):
        self.num_instances = num_instances
        self.role = role
        self.type = type
        self.market = market
        self.name = name
        if market == 'SPOT':
            if not bidprice:
                raise ValueError('bidprice must be specified if market == SPOT')
            self.bidprice = str(bidprice)

    def __repr__(self):
        if self.market == 'SPOT':
            return '%s.%s(name=%r, num_instances=%r, role=%r, type=%r, market = %r, bidprice = %r)' % (
             self.__class__.__module__, self.__class__.__name__,
             self.name, self.num_instances, self.role, self.type, self.market,
             self.bidprice)
        else:
            return '%s.%s(name=%r, num_instances=%r, role=%r, type=%r, market = %r)' % (
             self.__class__.__module__, self.__class__.__name__,
             self.name, self.num_instances, self.role, self.type, self.market)