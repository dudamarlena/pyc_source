# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/prologic/work/clusterprocessing/tests/test_cluster.py
# Compiled at: 2013-10-25 00:23:15
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_cluster(cluster):
    if not True:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))