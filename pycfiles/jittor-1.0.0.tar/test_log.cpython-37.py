# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_log.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1836 bytes
import unittest, os, re, jittor as jt
from jittor import LOG

def find_log_with_re(logs, pattern=None, **args):
    if pattern:
        pattern = re.compile(pattern)
    flogs = []
    for log in logs:
        for arg in args:
            if log[arg] != args[arg]:
                break
        else:
            if pattern:
                res = re.findall(pattern, log['msg'])
                if len(res):
                    flogs.append(res[0])

    return flogs


class TestLog(unittest.TestCase):

    def test_log_capture(self):
        LOG.log_capture_start()
        with jt.var_scope(log_v=1000, log_vprefix=''):
            LOG.v('1')
            LOG.vv('2')
            LOG.i('3')
            LOG.w('4')
            LOG.e('5')
            a = jt.zeros([10])
            a.sync()
        LOG.log_capture_stop()
        del a
        logs = LOG.log_capture_read()
        logs2 = LOG.log_capture_read()
        assert len(logs2) == 0
        for i in range(5):
            assert logs[i]['msg'] == str(i + 1)
            assert logs[i]['level'] == 'iiiwe'[i]
            assert logs[i]['name'] == 'test_log.py'

        finished_log = [l['msg'] for l in logs if l['name'] == 'executor.cc' if 'return vars:' in l['msg']]
        if not (len(finished_log) == 1 and '[10,]' in finished_log[0]):
            raise AssertionError


if __name__ == '__main__':
    unittest.main()