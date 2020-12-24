# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/txoids/utils.py
# Compiled at: 2017-10-19 01:32:12
# Size of source mod 2**32: 901 bytes
from twisted.internet import reactor
from twisted.internet.task import deferLater
import six

def full_dict2_dict(full_dict):
    for item in full_dict:
        if isinstance(full_dict[item], FullDict):
            full_dict[item] = full_dict2_dict(full_dict[item])

    return dict(full_dict)


class FullDict(dict):

    def __getitem__(self, item):
        if item not in self:
            self[item] = FullDict()
        return super(FullDict, self).__getitem__(item)

    def to_dict(self):
        return full_dict2_dict(self.copy())


def pretty_mac(mac_string):
    if six.PY3:
        return ':'.join('%02x' % b for b in mac_string)
    else:
        return ':'.join('%02x' % ord(b) for b in mac_string)


def deferredSleep(howLong):
    return deferLater(reactor, howLong, lambda : None)


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]