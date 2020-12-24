# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/messense/Projects/extender/tests/test_safe.py
# Compiled at: 2014-06-08 06:33:00
# Size of source mod 2**32: 231 bytes
import nose

def test_safe_execute():
    from extender import safe_execute

    def raise_error(e):
        raise e

    safe_execute(raise_error, KeyError)


if __name__ == '__main__':
    nose.runmodule()