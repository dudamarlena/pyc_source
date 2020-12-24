# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/etk/docking/dockframe.py
# Compiled at: 2011-01-14 09:31:43
from __future__ import absolute_import
from logging import getLogger
import gtk, gtk.gdk as gdk

class DockFrame(gtk.Bin):
    """
    The etk.DockFrame widget is a gtk.Bin that acts as the toplevel widget
    for a dock layout hierarchy.
    """
    __gtype_name__ = 'EtkDockFrame'

    def __init__(self):
        gtk.Bin.__init__(self)
        self.log = getLogger('%s.%s' % (self.__gtype_name__, hex(id(self))))
        self._placeholder = None
        return

    def do_size_request(self, requisition):
        requisition.width = 0
        requisition.height = 0
        if self.child and self.child.flags() & gtk.VISIBLE:
            requisition.width, requisition.height = self.child.size_request()
            requisition.width += self.border_width * 2
            requisition.height += self.border_width * 2

    def do_size_allocate(self, allocation):
        self.allocation = allocation
        if self.child and self.child.flags() & gtk.VISIBLE:
            child_allocation = gdk.Rectangle()
            child_allocation.x = allocation.x + self.border_width
            child_allocation.y = allocation.y + self.border_width
            child_allocation.width = allocation.width - 2 * self.border_width
            child_allocation.height = allocation.height - 2 * self.border_width
            self.child.size_allocate(child_allocation)

    def set_placeholder(self, placeholder):
        """
        Set a new placeholder widget on the frame. The placeholder is drawn on top
        of the dock items.

        If a new placeholder is set, an existing placeholder is destroyed.
        """
        if self._placeholder:
            self._placeholder.unparent()
            self._placeholder.destroy()
            self._placeholder = None
        if placeholder:
            self._placeholder = placeholder
            self._placeholder.set_parent(self)
        return