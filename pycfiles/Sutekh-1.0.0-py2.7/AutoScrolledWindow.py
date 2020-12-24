# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/AutoScrolledWindow.py
# Compiled at: 2019-12-11 16:37:48
"""Utility wrapper around gtk.ScrolledWindow"""
import gtk

class AutoScrolledWindow(gtk.ScrolledWindow):
    """Wrap a widget in a gtk.ScrolledWindow.

       Set the Scrollbar property to Autmoatic, so scrollbars only so up
       when needed. The widget can also be wrapped in a viewport if needed
       """

    def __init__(self, oWidgetToWrap, bUseViewport=False):
        super(AutoScrolledWindow, self).__init__()
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_IN)
        if bUseViewport:
            self.add_with_viewport(oWidgetToWrap)
        else:
            self.add(oWidgetToWrap)