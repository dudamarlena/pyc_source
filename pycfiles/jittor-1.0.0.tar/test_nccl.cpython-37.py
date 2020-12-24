# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_nccl.py
# Compiled at: 2020-04-02 06:47:38
# Size of source mod 2**32: 676 bytes
import jittor as jt, unittest

@unittest.skipIf(jt.compile_extern.nccl_ops is None, 'no nccl found')
class TestNccl(unittest.TestCase):

    @jt.flag_scope(use_cuda=1)
    def test_nccl(self):
        assert jt.compile_extern.nccl_ops.nccl_test('').data == 123


if __name__ == '__main__':
    unittest.main()