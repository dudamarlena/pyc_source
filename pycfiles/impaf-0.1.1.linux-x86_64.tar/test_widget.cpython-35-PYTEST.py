# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/tests/test_widget.py
# Compiled at: 2015-07-06 13:54:14
# Size of source mod 2**32: 701 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from mock import MagicMock
from pytest import fixture
from ..widget import Widget

class ExampleWidget(Widget):

    def __init__(self):
        super().__init__()
        self.mrequest = MagicMock()

    def _get_request_cls(self):
        return self.mrequest


class TestWidget(object):

    @fixture
    def mrequest(self):
        return MagicMock()

    @fixture
    def widget(self):
        return ExampleWidget()

    def test_feed_request(self, widget, mrequest):
        widget.feed_request(mrequest)
        widget.mrequest.assert_called_once_with(mrequest)
        @py_assert1 = widget.context
        @py_assert4 = {'request': widget.mrequest.return_value, 'widget': widget}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.context\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(widget) if 'widget' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(widget) else 'widget', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None