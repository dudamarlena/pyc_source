# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/template_test.py
# Compiled at: 2019-03-07 00:50:04
# Size of source mod 2**32: 286 bytes
from parser_engine.template import PETemplate
if __name__ == '__main__':
    if not PETemplate('name', None, ha=10).ha == 10:
        raise AssertionError
    else:
        assert PETemplate('name', None, ha=10).get('ha') == 10
        assert PETemplate('name', None).get('ha') is None
    if not PETemplate('name', None).ha is None:
        raise AssertionError