# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/toscawidgets/widgets/maps/widgets.py
# Compiled at: 2007-03-28 17:31:34
from toscawidgets.api import Widget, JSLink, CSSLink
__all__ = ['Maps']

class Maps(Widget):
    __module__ = __name__
    template = '<div id="${id}">${value}</div>'

    def __init__(self, id=None, parent=None, children=[], **kw):
        """Initialize the widget here. The widget's initial state shall be
        determined solely by the arguments passed to this function; two
        widgets initialized with the same args. should behave in *exactly* the
        same way. You should *not* rely on any external source to determine
        initial state."""
        super(Maps, self).__init__(id, parent, children, **kw)

    def update_params(self, d):
        """This method is called every time the widget is displayed. It's task
        is to prepare all variables that are sent to the template. Those
        variables can accessed as attributes of d."""
        super(Maps, self).update_params(d)