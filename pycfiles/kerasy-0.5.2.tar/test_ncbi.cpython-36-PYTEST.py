# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/datasets/test_ncbi.py
# Compiled at: 2020-05-11 02:09:16
# Size of source mod 2**32: 183 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.datasets import ncbi

def test_get_seq():
    sequence = ncbi.getSeq('NC_004718')
    @py_assert2 = None
    @py_assert1 = sequence is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (sequence, @py_assert2)) % {'py0':@pytest_ar._saferepr(sequence) if 'sequence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sequence) else 'sequence',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None