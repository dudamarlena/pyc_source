# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_init.py
# Compiled at: 2015-04-13 16:10:48
"""demo of instance_noinit"""
import pickle, sys, string, gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle.util import setParanoia
from UserList import UserList
import funcs, gnosis.pyconfig as pyconfig
funcs.set_parser()
from gnosis.util.introspect import instance_noinit
COUNTER = 0

def inc():
    global COUNTER
    COUNTER += 1


class Old_noinit:

    def work(self):
        inc()


class Old_init:

    def __init__(self):
        raise 'ERROR - Init in Old'

    def work(self):
        inc()


if pyconfig.Have_Slots():

    class New_slots_and_init(int):
        __slots__ = ('this', 'that')

        def __init__(self):
            raise 'ERROR - Init in New w/slots'

        def work(self):
            inc()


    class New_init_no_slots(int):

        def __init__(self):
            raise 'Init in New w/o slots'

        def work(self):
            inc()


    class New_slots_no_init(int):
        __slots__ = ('this', 'that')

        def work(self):
            inc()


    class New_no_slots_no_init(int):

        def work(self):
            inc()


olist = []
olist.append(instance_noinit(Old_noinit))
olist.append(instance_noinit(Old_init))
if pyconfig.Have_Slots():
    olist.append(instance_noinit(New_slots_and_init))
    olist.append(instance_noinit(New_slots_no_init))
    olist.append(instance_noinit(New_init_no_slots))
    olist.append(instance_noinit(New_no_slots_no_init))
for o in olist:
    o.work()

if pyconfig.Have_Slots() and COUNTER != 6 or not pyconfig.Have_Slots() and COUNTER != 2:
    raise 'Bad count'
print '** OK **'