# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/clusterprocessing/tests/test_cluster.py
# Compiled at: 2013-10-25 00:23:15
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_cluster(cluster):
    if not True:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))