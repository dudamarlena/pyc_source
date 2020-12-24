# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/laureano/desarrollo/eggs/tw/twtools/projects/tw.jsunit/trunk/tw/jsunit/widgets.py
# Compiled at: 2008-04-30 19:23:36
from tw.api import Widget, JSLink, CSSLink
from tw.jsunit import jsunit_js
__all__ = ['JSUnit']

class JSUnit(Widget):
    __module__ = __name__
    template = '\n    '
    javascript = [
     jsunit_js]

    def __init__(self, id=None, parent=None, children=[], **kw):
        """Initialize the widget here. The widget's initial state shall be
        determined solely by the arguments passed to this function; two
        widgets initialized with the same args. should behave in *exactly* the
        same way. You should *not* rely on any external source to determine
        initial state."""
        super(JSUnit, self).__init__(id, parent, children, **kw)

    def update_params(self, d):
        """This method is called every time the widget is displayed. It's task
        is to prepare all variables that are sent to the template. Those
        variables can accessed as attributes of d."""
        super(JSUnit, self).update_params(d)