# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/flag_test.py
# Compiled at: 2017-05-17 13:34:19
# Size of source mod 2**32: 210 bytes
import sys
from .flag import FlagAdder

def test_flag_adder():
    sys.argv = [
     'command', '--foo', 'baz']
    adder = FlagAdder()
    adder.add_flag('foo', dest='bar')
    assert adder.flags['bar'] == 'baz'