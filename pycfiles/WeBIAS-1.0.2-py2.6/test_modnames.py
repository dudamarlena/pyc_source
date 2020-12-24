# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_modnames.py
# Compiled at: 2015-04-13 16:10:48
"""Demonstrate that on-the-fly and gnosis.xml.* namespaces not saved in XML file --fpm"""
import gnosis.xml.pickle as xml_pickle
from UserList import UserList
import funcs, re
funcs.set_parser()
ud_xml = '<?xml version="1.0"?>\n<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">\n<PyObject module="__main__" class="Foo">\n</PyObject>\n'

class myfoo:
    pass


class Foo:
    pass


p = xml_pickle.loads(ud_xml)
if str(p.__class__) != 'gnosis.xml.pickle.util._util.Foo':
    raise 'ERROR(1)'
s = xml_pickle.dumps(p)
if re.search(s, 'module'):
    raise 'ERROR(2)'
xml_pickle.Foo = myfoo
p = xml_pickle.loads(ud_xml)
if str(p.__class__) != '__main__.myfoo':
    raise 'ERROR(3)'
s = xml_pickle.dumps(p)
if re.search(s, 'module'):
    raise 'ERROR(4)'
del xml_pickle.Foo
xml_pickle.add_class_to_store('Foo', myfoo)
p = xml_pickle.loads(ud_xml)
if str(p.__class__) != '__main__.myfoo':
    raise 'ERROR(5)'
s = xml_pickle.dumps(p)
if re.search('module', s):
    raise 'ERROR(6)'
xml_pickle.remove_class_from_store('Foo')
xml_pickle.setParanoia(0)
p = xml_pickle.loads(ud_xml)
if str(p.__class__) != '__main__.Foo':
    raise 'ERROR(7)'
s = xml_pickle.dumps(p)
if not re.search('PyObject\\s+module="__main__"\\s+class="Foo"', s):
    raise 'ERROR(8)'
print '** OK **'