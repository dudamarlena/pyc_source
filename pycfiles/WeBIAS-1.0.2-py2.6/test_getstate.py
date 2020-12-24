# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_getstate.py
# Compiled at: 2015-04-13 16:10:48
""" using getstate() to rename attributes into a more verbose
form for XML output (also tests setstate)  --fpm"""

class contact:

    def __init__(self, first, last, addr, city, state):
        self.first = first
        self.last = last
        self.addr = addr
        self.city = city
        self.state = state

    def __getstate__(self):
        d = {'FirstName': self.first, 'LastName': self.last, 
           'Address': self.addr, 
           'City': self.city, 
           'State': self.state}
        return d

    def __setstate__(self, d):
        self.first = d['FirstName']
        self.last = d['LastName']
        self.addr = d['Address']
        self.city = d['City']
        self.state = d['State']


import gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle.util import setParanoia
import funcs
funcs.set_parser()
setParanoia(0)

def checkit(o1, o2):
    for attr in ['first', 'last', 'addr', 'city', 'state']:
        if getattr(o1, attr) != getattr(o2, attr):
            raise 'ERROR(1)'


c = contact('Joe', 'Jones', '1744 Elk Road', 'Manchester', 'NH')
x = xml_pickle.dumps(c)
d = xml_pickle.loads(x)
checkit(c, d)
import pickle
s = pickle.dumps(d)
q = pickle.loads(s)
checkit(c, q)
print '** OK **'