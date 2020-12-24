# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_selfref.py
# Compiled at: 2015-04-13 16:10:48
"""This started out as a test of toplevel-pickling of builtins, but has
turned into more of a test of pickling self-referencing objects (toplevels are
still tested, however). --fpm"""
import gnosis.xml.pickle as xml_pickle, random, re, sys
from gnosis.xml.pickle.ext import XMLP_Mutator, XMLP_Mutated
import gnosis.xml.pickle.ext as mutate
from UserList import UserList
import funcs
funcs.set_parser()

class foo:
    pass


xml_pickle.setParanoia(0)
l = [
 1, 2]
l.append(l)
x = xml_pickle.dumps(l)
g = xml_pickle.loads(x)
if g[0] != l[0] or g[1] != l[1] or id(g[2]) != id(g):
    raise 'ERROR(1)'
d = {'a': 1}
d['b'] = d
x = xml_pickle.dumps(d)
g = xml_pickle.loads(x)
if g['a'] != 1 or id(g['b']) != id(g):
    raise 'ERROR(2)'
bltin_objs = [
 'abc', 123, 123.45, complex(12.0, 34.0), {'A': 1, 'B': 2, 'C': 3},
 [
  1, 2, 'a', 'b'], ('a', 'b', 1, 2)]
for o in bltin_objs:
    x = xml_pickle.dumps(o)
    o2 = xml_pickle.loads(x)
    if o != o2:
        raise 'ERROR(3)'

r = re.compile('this\\s*is (not)?a\npattern$')
x = xml_pickle.dumps(r)
g = xml_pickle.loads(x)
if r.pattern != g.pattern:
    raise 'ERROR(4)'
for o in bltin_objs:
    f = foo()
    f.s = o
    x = xml_pickle.dumps(f)
    g = xml_pickle.loads(x)
    if g.s != f.s:
        raise 'ERROR(5)'

f = foo()
f.s = re.compile('this\\s*is (not)?a\npattern$')
x = xml_pickle.dumps(f)
g = xml_pickle.loads(x)
if f.s.pattern != g.s.pattern:
    raise 'ERROR(6)'

class foomu(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, type(foo()), 'foomu')

    def wants_obj(self, obj):
        return obj.__class__ == foo

    def mutate(self, obj):
        obj.breakage = obj
        return XMLP_Mutated(obj)

    def unmutate(self, mobj):
        return mobj.obj


my = foomu()
mutate.add_mutator(my)
f = foo()
f.a = UserList([4, 5, 6])
f.b = 'abc'
x = xml_pickle.dumps(f)
g = xml_pickle.loads(x)
if g.__class__ != foo or g.a != f.a or g.b != f.b:
    raise 'ERROR(7)'
mutate.remove_mutator(my)
s = '<?xml version="1.0"?>\n<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">\n<PyObject class="Spam" id="1111">\n<attr name="lst" type="list" id="2222">\n  <item type="PyObject" refid="1111" />\n  <item type="list" refid="2222" />\n</attr>\n</PyObject>\n'
o2 = xml_pickle.loads(s)
s = '<?xml version="1.0"?>\n<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">\n<PyObject class="Spam" id="1111">\n<attr name="parent" type="PyObject" refid="1111" />\n</PyObject>\n'
o2 = xml_pickle.loads(s)
if id(o2) != id(o2.parent):
    raise 'ERROR(8)'

class A:

    def __init__(self, x=0):
        self.__parent__ = None
        self.x = x
        return

    def setParent(self, p):
        self.__parent__ = p


x = A(1)
x.y = A(2)
x.y.z = A(3)
x.y.z.setParent(x.y)
s = xml_pickle.dumps(x)
p = xml_pickle.loads(s)
if [
 x.x, x.y.x, x.y.z.x, x.y.z.__parent__.x] != [
 p.x, p.y.x, p.y.z.x, p.y.z.__parent__.x]:
    raise 'ERROR(9)'
print '** OK **'