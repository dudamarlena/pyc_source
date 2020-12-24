# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/tests/test_dict2xml.py
# Compiled at: 2020-01-29 20:14:21
# Size of source mod 2**32: 1091 bytes
"""
Copyright 2019 Brain Electrophysiology Laboratory Company LLC

Licensed under the ApacheLicense, Version 2.0(the "License");
you may not use this module except in compliance with the License.
You may obtain a copy of the License at:

http: // www.apache.org / licenses / LICENSE - 2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied.
"""
from ..dict2xml import dict2xml, TEXT, ATTR

def test_dict2xml():
    rootname = 'myroot'
    content = {'a':{TEXT: '35', ATTR: {'hello': 'world'}}, 
     'b':[{TEXT: 'b' + str(i + 1)} for i in range(2)]}
    elem = dict2xml(content, rootname=rootname)
    elem.write('test.xml')
    root = elem.getroot()
    a = root.find('a')
    bs = root.findall('b')
    if not root.tag == 'myroot':
        raise AssertionError(root.tag)
    else:
        if not a.tag == 'a':
            raise AssertionError(a.tag)
        elif not a.text == '35':
            raise AssertionError(a.text)
        assert a.get('hello') == 'world'
    for i, b in enumerate(bs):
        assert b.text == 'b' + str(i + 1)