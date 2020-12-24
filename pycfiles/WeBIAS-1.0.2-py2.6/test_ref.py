# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_ref.py
# Compiled at: 2015-04-13 16:10:48
"""Demonstrate what happens with/without DEEPCOPY  --fpm"""
import gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle.util import setParanoia, setDeepCopy
from UserList import UserList
import sys, funcs
funcs.set_parser()
a = (1, 2, 3)
b = [4, 5, 6]
c = {'a': 1, 'b': 2, 'c': 3, 'd': [100, 200, 300]}
dd = c['d']
uu = UserList([10, 11, 12])
u = UserList([[uu, c, b, a], [a, b, c, uu], [c, a, b, uu], dd])
setParanoia(0)
x1 = xml_pickle.dumps(u)
g = xml_pickle.loads(x1)
if u != g:
    raise 'ERROR(1)'
setDeepCopy(1)
x2 = xml_pickle.dumps(g)
z = xml_pickle.loads(x2)
if len(x2) - len(x1) < 1000:
    raise 'ERROR(2)'
if z != g:
    raise 'ERROR(3)'
print '** OK **'