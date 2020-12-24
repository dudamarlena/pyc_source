# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\test\test_schema.py
# Compiled at: 2016-01-04 11:02:19
# Size of source mod 2**32: 240 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from jep_py.schema import Message, Shutdown, CompletionResponse

def test_message_class_by_name():
    @py_assert1 = Message.class_by_name
    @py_assert3 = 'Shutdown'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 is Shutdown
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.class_by_name\n}(%(py4)s)\n} is %(py8)s', ), (@py_assert5, Shutdown)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(Shutdown) if 'Shutdown' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Shutdown) else 'Shutdown', 'py0': @pytest_ar._saferepr(Message) if 'Message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Message) else 'Message', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = Message.class_by_name
    @py_assert3 = 'CompletionResponse'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 is CompletionResponse
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.class_by_name\n}(%(py4)s)\n} is %(py8)s', ), (@py_assert5, CompletionResponse)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(CompletionResponse) if 'CompletionResponse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(CompletionResponse) else 'CompletionResponse', 'py0': @pytest_ar._saferepr(Message) if 'Message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Message) else 'Message', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None