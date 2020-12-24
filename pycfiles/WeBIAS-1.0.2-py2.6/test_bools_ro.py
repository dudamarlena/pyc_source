# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_bools_ro.py
# Compiled at: 2015-04-13 16:10:47
import gnosis.xml.pickle as xmp
from gnosis.xml.pickle.util import setVerbose, setParser, setParanoia
from funcs import set_parser, unlink
import gnosis.pyconfig as pyconfig
from types import *
set_parser()
setParanoia(0)
x1 = '<?xml version="1.0"?>\n<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">\n<PyObject module="__main__" class="foo" id="168690156">\n<attr name="a" family="uniq" type="False" value="" />\n<attr name="c" family="none" type="None" />\n<attr name="b" family="uniq" type="True" value="" />\n<attr name="k" family="lang" type="class" module="__main__" class="a_test_class"/>\n<attr name="f" family="lang" type="function" module="__main__" class="a_test_function"/>\n</PyObject>\n'
x2 = '<?xml version="1.0"?>\n<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">\n<PyObject family="obj" type="builtin_wrapper"  class="_EmptyClass">\n<attr name="__toplevel__" family="seq" type="tuple" id="169764140" >\n  <item family="uniq" type="True" value="" />\n  <item family="uniq" type="False" value="" />\n</attr>\n</PyObject>\n'
x3 = '<?xml version="1.0"?>\n<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">\n<PyObject family="obj" type="builtin_wrapper"  class="_EmptyClass">\n<attr name="__toplevel__" family="uniq" type="True" value="" />\n</PyObject>\n'

class a_test_class:

    def __init__(self):
        pass


def a_test_function():
    pass


class foo:

    def __init__(self):
        self.a = False
        self.b = True
        self.c = None
        self.f = a_test_function
        self.k = a_test_class
        return


if not pyconfig.Have_TrueFalse():
    True = 1
    False = 0
x = xmp.loads(x1)
if x.a != False or x.b != True or x.c != None or x.f != a_test_function or x.k != a_test_class:
    raise 'ERROR(1)'
x = xmp.loads(x2)
if x[0] != True or x[1] != False:
    raise 'ERROR(2)'
x = xmp.loads(x3)
if x != True:
    raise 'ERROR(3)'
print '** OK **'