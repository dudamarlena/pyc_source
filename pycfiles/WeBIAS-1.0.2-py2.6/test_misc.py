# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_misc.py
# Compiled at: 2015-04-13 16:10:48
"""

Here are collected miscellaneous tests (from bug reports,etc.)
that don't clearly fit elsewhere. --fpm

"""
import gnosis.xml.pickle as xml_pickle
from funcs import set_parser
import gnosis.pyconfig as pyconfig
set_parser()
xml_pickle.setParanoia(0)
if pyconfig.Have_ObjectClass():

    class PickleMeOld:

        def __init__(self):
            pass


    class PickleMeNew(object):

        def __init__(self):
            pass


    class Container(object):

        def __init__(self, klass):
            self.classRef = klass


    x = xml_pickle.dumps(Container(PickleMeOld))
    o = xml_pickle.loads(x)
    if o.classRef != PickleMeOld:
        raise 'ERROR(1)'
    x = xml_pickle.dumps(Container(PickleMeNew))
    o = xml_pickle.loads(x)
    if o.classRef != PickleMeNew:
        raise 'ERROR(2)'
print '** OK **'