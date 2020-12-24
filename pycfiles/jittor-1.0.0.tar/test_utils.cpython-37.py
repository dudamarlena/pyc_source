# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_utils.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 2084 bytes
import unittest, os
from jittor import LOG

def find_jittor_path():
    path = os.path.realpath(__file__)
    suffix = 'test/test_utils.py'
    assert path.endswith(suffix), path
    return path[:-len(suffix)]


def find_cache_path():
    from pathlib import Path
    path = str(Path.home())
    dirs = ['.cache', 'jittor']
    for d in dirs:
        path = os.path.join(path, d)
        if not os.path.isdir(path):
            os.mkdir(path)
        assert os.path.isdir(path)

    return path


cache_path = find_cache_path()
jittor_path = find_jittor_path()
cc_flags = f" -g -O0 -DTEST --std=c++14 -I{jittor_path}/test -I{jittor_path}/src "

class TestUtils(unittest.TestCase):

    def test_cache_compile(self):
        cmd = f"cd {cache_path} && g++ {jittor_path}/src/utils/log.cc {jittor_path}/src/utils/tracer.cc {jittor_path}/src/utils/cache_compile.cc -lpthread {cc_flags} -o cache_compile && cache_path={cache_path} jittor_path={jittor_path} ./cache_compile"
        self.assertEqual(os.system(cmd), 0)

    def test_log(self):
        cc_flags = f" -g -O3 -DTEST_LOG --std=c++14 -I{jittor_path}/test -I{jittor_path}/src -lpthread "
        cmd = f"cd {cache_path} && g++ {jittor_path}/src/utils/log.cc {jittor_path}/src/utils/tracer.cc {cc_flags} -o log && log_v=1000 log_sync=0 ./log"
        LOG.v(cmd)
        assert os.system(cmd) == 0

    def test_mwsr_list(self):
        cc_flags = f" -g -O3 -DTEST --std=c++14 -I{jittor_path}/test -I{jittor_path}/src -lpthread "
        cmd = f"cd {cache_path} && g++ {jittor_path}/src/utils/mwsr_list.cc {cc_flags} -o mwsr_list && ./mwsr_list"
        LOG.v(cmd)
        assert os.system(cmd) == 0


if __name__ == '__main__':
    unittest.main()