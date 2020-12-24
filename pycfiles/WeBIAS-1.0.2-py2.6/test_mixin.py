# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_mixin.py
# Compiled at: 2015-04-13 16:10:48
import gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle import XML_Pickler
from gnosis.xml.pickle.util import setParanoia
from UserList import UserList
import funcs
funcs.set_parser()

class Foo:

    def hello(self):
        return 'FOO!'


class Bar(Foo, XML_Pickler):

    def __init__(self):
        XML_Pickler.__init__(self)

    def hello(self):
        return 'BAR!'


class Bat(Foo, XML_Pickler):

    def __init__(self):
        XML_Pickler.__init__(self)

    def hello(self):
        return 'BAT!'


class FunList(UserList, XML_Pickler):

    def __init__(self):
        XML_Pickler.__init__(self)
        UserList.__init__(self)


setParanoia(0)
l = FunList()
l.append(Foo())
l.append(Bar())
l.append(Bat())
x = l.dumps()
o = XML_Pickler().loads(x)
if o[0].hello() != 'FOO!' or o[1].hello() != 'BAR!' or o[2].hello() != 'BAT!':
    raise 'ERROR(1)'
print '** OK **'