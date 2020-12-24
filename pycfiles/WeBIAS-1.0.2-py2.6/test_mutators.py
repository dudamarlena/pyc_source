# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_mutators.py
# Compiled at: 2015-04-13 16:10:48
"""
Examples of several different things mutators can do. --fpm
"""
import gnosis.xml.pickle as xml_pickle, gnosis.xml.pickle.ext as mutate, gnosis.xml.pickle.util as util
from gnosis.xml.pickle.ext import XMLP_Mutator, XMLP_Mutated
from types import *
import sys
from UserList import UserList
import funcs
funcs.set_parser()

class mystring(XMLP_Mutator):

    def mutate(self, obj):
        print '** mystring.mutate()'
        return XMLP_Mutated(obj)

    def unmutate(self, mobj):
        print '** mystring.unmutate()'
        return mobj.obj


print '*** TEST 1 ***'
my1 = mystring(StringType, 'MyString', in_body=1)
my2 = mystring(UnicodeType, 'MyString', in_body=1)
mutate.add_mutator(my1)
mutate.add_mutator(my2)
u = UserList(['aaa', 'bbb', 'ccc'])
print u
x = xml_pickle.dumps(u)
print x
del u
z = xml_pickle.loads(x)
print z
mutate.remove_mutator(my1)
mutate.remove_mutator(my2)
print '*** TEST 2 ***'
my1 = mystring(StringType, 'string', in_body=1)
my2 = mystring(UnicodeType, 'string', in_body=1)
mutate.add_mutator(my1)
mutate.add_mutator(my2)
u = UserList(['aaa', 'bbb', 'ccc'])
print u
x = xml_pickle.dumps(u)
print x
del u
mutate.remove_mutator(my1)
mutate.remove_mutator(my2)
z = xml_pickle.loads(x)
print z

class mynumlist(XMLP_Mutator):

    def wants_obj(self, obj):
        for i in obj:
            if type(i) is not IntType:
                return 0

        return 1

    def mutate(self, obj):
        t = '%d' % obj[0]
        for i in obj[1:]:
            t = t + ',%d' % i

        return XMLP_Mutated(t)

    def unmutate(self, mobj):
        l = map(int, mobj.obj.split(','))
        return l


class mycharlist(XMLP_Mutator):

    def wants_obj(self, obj):
        for i in obj:
            if type(i) is not StringType or len(i) != 1:
                return 0

        return 1

    def mutate(self, obj):
        t = '%s' % obj[0]
        for i in obj[1:]:
            t = t + ',%s' % i

        return XMLP_Mutated(t)

    def unmutate(self, mobj):
        l = mobj.obj.split(',')
        return l


print '*** TEST 3 ***'
my1 = mynumlist(ListType, 'NumList', in_body=1)
my2 = mycharlist(ListType, 'CharList', in_body=1)
mutate.add_mutator(my1)
mutate.add_mutator(my2)
u = UserList([[1, 2, 3], ['mmm', 'nnn', 'ooo'], ['a', 'b', 'c'], [4.1, 5.2, 6.3]])
print u
x = xml_pickle.dumps(u)
print x
del u
g = xml_pickle.loads(x)
print g
mutate.remove_mutator(my1)
mutate.remove_mutator(my2)

class mutate_userlist(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, type(UserList()), 'userlist')

    def wants_obj(self, obj):
        return isinstance(obj, UserList)

    def mutate(self, obj):
        return XMLP_Mutated(obj.data, '%s.%s' % (util._module(obj), util._klass(obj)))

    def unmutate(self, mobj):
        p = mobj.extra.split('.')
        klass = util.get_class_from_name(p[1], p[0], xml_pickle.getParanoia())
        return klass(mobj.obj)


print '*** TEST 4 ***'
xml_pickle.setParanoia(0)
my1 = mutate_userlist()
mutate.add_mutator(my1)

class mylist(UserList):
    pass


class zlist(mylist):
    pass


class foo:
    pass


f = foo()
f.u = UserList([1, 2, 3, 4])
f.m = mylist([5, 6, 7, 8])
f.z = zlist([9, 10, 11, 12])
print f.u.__class__, f.u
print f.m.__class__, f.m
print f.z.__class__, f.z
x = xml_pickle.dumps(f)
print x
del f
g = xml_pickle.loads(x)
print g.u.__class__, g.u
print g.m.__class__, g.m
print g.z.__class__, g.z
mutate.remove_mutator(my1)
try:
    import Numeric
except:
    sys.exit(0)

class mutate_multidim(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, Numeric.ArrayType, 'numpy_matrix', in_body=1)

    def mutate(self, obj):
        s = '\n'
        for arr in obj:
            for elem in arr:
                s += '%f ' % elem

            s += '\n'

        return XMLP_Mutated(s)

    def unmutate(self, mobj):
        text = mobj.obj
        lines = text.split('\n')
        list = []
        for line in lines:
            a = map(float, line.split())
            if len(a):
                list.append(a)

        a = Numeric.array(list)
        return a


my1 = mutate_multidim()
mutate.add_mutator(my1)
f = foo()
f.a = Numeric.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], 'f')
print 'ORIG: ', f.a
x = xml_pickle.dumps(f)
print x
del f
g = xml_pickle.loads(x)
print 'COPY: ', g.a
mutate.remove_mutator(my1)
try:
    import mx.DateTime, re
    mxDateTime_type = type(mx.DateTime.localtime())
except:
    sys.exit(0)

class mutate_mxdatetime(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, mxDateTime_type, 'mxDateTime', paranoia=0)

    def mutate(self, obj):
        d = {}
        d['YMD'] = '%d/%d/%d' % (obj.year, obj.month, obj.day)
        d['HMS'] = '%d:%d:%f' % (obj.hour, obj.minute, obj.second)
        return XMLP_Mutated(d)

    def unmutate(self, mobj):
        obj = mobj.obj
        fmt = '\\s*([0-9]+)\\s*/\\s*([0-9]+)\\s*/\\s*([0-9]+)'
        m1 = re.match(fmt, obj['YMD'])
        fmt = '\\s*([0-9]+)\\s*:\\s*([0-9]+)\\s*:\\s*([0-9\\.]+)'
        m2 = re.match(fmt, obj['HMS'])
        return apply(mx.DateTime.DateTime, map(int, m1.groups()) + map(int, m2.groups()[:2]) + [float(m2.group(3))])


my1 = mutate_mxdatetime()
mutate.add_mutator(my1)
f = foo()
f.a = mx.DateTime.now()
print 'ORIG: ', f.a
x = xml_pickle.dumps(f)
print x
del f
g = xml_pickle.loads(x)
print 'COPY: ', g.a
mutate.remove_mutator(my1)