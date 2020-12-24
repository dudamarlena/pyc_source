# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/types/channel_order.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 785 bytes
import functools
from ...drivers.channel_order import ChannelOrder
USAGE = "\nA ChannelOrder can be initialized with:\n\n* A list, tuple or string of length three: '012', 'bgr', (0, 2, 1)\n* An integer from 0 to 5."
NAMES = {'r':0, 
 'g':1, 
 'b':2, 
 'R':0, 
 'G':1, 
 'B':2, 
 '0':0, 
 '1':1, 
 '2':2, 
 0:0, 
 1:1, 
 2:2}

@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(tuple)
@make.register(list)
@make.register(str)
def _(c):
    i = ChannelOrder.ORDERS.index(tuple(NAMES[i] for i in c))
    return ChannelOrder.ORDERS[i]


@make.register(int)
def _(c):
    if c < 0:
        raise IndexError('RGB indices cannot be negative')
    return ChannelOrder.ORDERS[c]