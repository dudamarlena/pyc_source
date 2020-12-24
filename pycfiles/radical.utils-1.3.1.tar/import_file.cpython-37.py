# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/radical/radical.utils.devel/tests/unittests/data/import_file.py
# Compiled at: 2020-04-13 09:15:55
# Size of source mod 2**32: 469 bytes
import time

def foo(bar, buz=1):
    assert bar == buz
    time.sleep(0.1)
    return True


class Foo(object):

    def foo(self, bar, buz=1):
        assert bar == buz
        time.sleep(0.1)
        return True