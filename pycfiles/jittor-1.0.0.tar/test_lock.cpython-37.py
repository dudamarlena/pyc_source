# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_lock.py
# Compiled at: 2020-04-11 06:08:16
# Size of source mod 2**32: 1046 bytes
import unittest, os, sys, jittor as jt
from pathlib import Path

class TestLock(unittest.TestCase):

    def test(self):
        if os.environ.get('lock_full_test', '0') == '1':
            cache_path = os.path.join(str(Path.home()), '.cache', 'jittor', 'lock')
            assert os.system(f"rm -rf {cache_path}") == 0
            cmd = f"cache_name=lock {sys.executable} -m jittor.test.test_example"
        else:
            cmd = f"{sys.executable} -m jittor.test.test_example"
        print('run cmd twice', cmd)
        assert os.system(f"{cmd} & {cmd} & wait %1 && wait %2") == 0


if __name__ == '__main__':
    unittest.main()