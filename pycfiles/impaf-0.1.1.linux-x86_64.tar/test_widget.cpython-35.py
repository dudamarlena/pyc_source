# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/example/venv_impex/lib/python3.5/site-packages/impaf/tests/test_widget.py
# Compiled at: 2015-07-06 13:54:14
# Size of source mod 2**32: 701 bytes
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
        assert widget.context == {'request': widget.mrequest.return_value, 
         'widget': widget}