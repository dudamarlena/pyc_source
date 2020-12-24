# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/signals_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 1521 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, signal, pytest, paleomix.common.signals as signals

def test_signal__sigterm_to_str():
    @py_assert1 = signals.to_str
    @py_assert4 = signal.SIGTERM
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = 'SIGTERM'
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/signals_test.py', lineno=32)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.to_str\n}(%(py5)s\n{%(py5)s = %(py3)s.SIGTERM\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(signals) if 'signals' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(signals) else 'signals',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(signal) if 'signal' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(signal) else 'signal',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_signal__to_str__unknown_signal():
    with pytest.raises(KeyError):
        signals.to_str(1024)


def test_signal__to_str__wrong_type():
    with pytest.raises(TypeError):
        signals.to_str('SIGTERM')