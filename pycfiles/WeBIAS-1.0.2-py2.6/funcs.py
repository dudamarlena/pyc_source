# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/funcs.py
# Compiled at: 2015-04-13 16:10:47
"""
each test_*.py imports this to auto-set the parser based on
the presence of a USE_... file

-- frankm@hiwaay.net
"""
import os, sys, string, gnosis.xml.pickle as xml_pickle

def set_parser():
    if os.path.isfile('USE_SAX'):
        xml_pickle.setParser('SAX')
    elif os.path.isfile('USE_CEXPAT'):
        xml_pickle.setParser('cEXPAT')
    else:
        xml_pickle.setParser('DOM')


def unlink(filename):
    if not os.path.isfile(filename):
        return
    try:
        os.unlink(filename)
    except:
        pass

    try:
        os.remove(filename)
    except:
        pass


def touch(filename):
    open(filename, 'w')