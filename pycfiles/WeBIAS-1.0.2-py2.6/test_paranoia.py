# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_paranoia.py
# Compiled at: 2015-04-13 16:10:48
"""Test that the PARANOIA setting works --fpm"""
import gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle.util import setParanoia, getParanoia, add_class_to_store
import funcs
funcs.set_parser()
ud_xml = '<?xml version="1.0"?>\n<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">\n<PyObject module="UserDict" class="UserDict" id="136115060">\n<attr name="data" type="dict" id="136066676">\n  <entry>\n    <key type="string" value="One" />\n    <val type="numeric" value="1" />\n  </entry>\n  <entry>\n    <key type="string" value="Two" />\n    <val type="numeric" value="2" />\n  </entry>\n</attr>\n</PyObject>\n'
COUNTER = 0

def incOK():
    global COUNTER
    COUNTER += 1


x = xml_pickle.XML_Pickler()
setParanoia(2)
try:
    ud = x.loads(ud_xml)
    raise 'FAILED 1!!'
except:
    incOK()

setParanoia(1)
ud = x.loads(ud_xml)
try:
    a = ud['Two']
    raise 'FAILED 2!!'
except:
    incOK()

setParanoia(-1)
ud = x.loads(ud_xml)
try:
    i = ud['Two']
    incOK()
except:
    raise 'FAILED 3!!'

setParanoia(2)
try:
    ud = x.loads(ud_xml)
    raise 'FAILED 4!!'
except:
    incOK()

from UserDict import UserDict
setParanoia(0)
ud = x.loads(ud_xml)
try:
    i = ud['One']
    incOK()
except:
    raise 'FAILED 5!!'

setParanoia(2)
try:
    ud = x.loads(ud_xml)
    raise 'FAILED 6!!'
except:
    incOK()

class MyDict(UserDict):
    pass


add_class_to_store('UserDict', MyDict)
setParanoia(1)
ud = x.loads(ud_xml)
try:
    if ud.__class__.__name__ != 'MyDict':
        raise 'FAILED 7!!'
    else:
        i = ud['One']
        incOK()
except:
    raise 'FAILED 8!!'

if COUNTER != 7:
    raise 'FAILED 9!!'
print '** OK **'