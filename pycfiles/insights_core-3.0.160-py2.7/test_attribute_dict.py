# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_attribute_dict.py
# Compiled at: 2019-05-16 13:41:33
from insights.core import AttributeDict
DICT = {'dmode': '0500', 'relatime': True, 'uid': '0', 'iocharset': 'utf8', 
   'gid': '0', 'mode': '0400', 'ro': True, 'nosuid': True, 
   'uhelper': 'udisks2', 'nodev': True}

def test_attribute_dict():
    d_obj = AttributeDict(DICT)
    assert d_obj['dmode'] == '0500'
    assert d_obj.get('relatime') is True
    assert d_obj.nosuid is True
    assert 'uid' in d_obj
    assert d_obj.get('mode', None) == '0400'
    assert d_obj.get('xmode', None) is None
    for d, v in d_obj.items():
        if d.startswith('nod'):
            assert v is True

    return