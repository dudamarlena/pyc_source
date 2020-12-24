# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/test_pos.py
# Compiled at: 2020-04-02 20:24:03
# Size of source mod 2**32: 152 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, hama

def test_nouns():
    text = '버스 타고 가자.'
    print(hama.tag(text))
    @py_assert1 = hama.nouns
    @py_assert4 = @py_assert1(text)
    @py_assert7 = [
     '버스']
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.nouns\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(hama) if 'hama' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hama) else 'hama',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(text) if 'text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text) else 'text',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None