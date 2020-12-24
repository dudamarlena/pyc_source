# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CellRendererSutekhButton.py
# Compiled at: 2019-12-11 16:37:48
"""Render a icon in a TreeView"""
import gtk, gobject

class CellRendererSutekhButton(gtk.GenericCellRenderer):
    """Render a icon in a cell in a TreeView.

       Used to render the arrows for incrementing and decrementing cards
       in the CardListView's
       """
    __gproperties__ = {'showicon': (
                  gobject.TYPE_BOOLEAN, 'showicon property',
                  'whether to show the icon', 0, gobject.PARAM_READWRITE)}

    def __init__(self, bShowIcon=False):
        super(CellRendererSutekhButton, self).__init__()
        self.__gobject_init__()
        self.oPixbuf = None
        self.set_property('mode', gtk.CELL_RENDERER_MODE_ACTIVATABLE)
        self.bShowIcon = bShowIcon
        self.bClicked = False
        self.oClickedBackgroundArea = None
        return

    def load_icon(self, sName, oWidget):
        """Load the icon specified in name"""
        self.oPixbuf = oWidget.render_icon(sName, gtk.ICON_SIZE_MENU)

    def do_get_property(self, oProp):
        """Allow reading the showicon property"""
        if oProp.name == 'showicon':
            return self.bShowIcon
        raise AttributeError('unknown property %s' % oProp.name)

    def do_set_property(self, oProp, oValue):
        """Allow setting the showicon property"""
        if oProp.name == 'showicon':
            self.bShowIcon = oValue
        else:
            raise AttributeError('unknown property %s' % oProp.name)

    def on_get_size(self, _oWidget, oCellArea):
        """Handle get_size requests"""
        if self.oPixbuf is None:
            return (0, 0, 0, 0)
        else:
            iPixbufWidth = self.oPixbuf.get_width()
            iPixbufHeight = self.oPixbuf.get_height()
            fCalcWidth = self.get_property('xpad') * 2 + iPixbufWidth
            fCalcHeight = self.get_property('ypad') * 2 + iPixbufHeight
            iXOffset = 0
            iYOffset = 0
            if oCellArea is not None and iPixbufWidth > 0 and iPixbufHeight > 0:
                iXOffset = int(self.get_property('xalign') * (oCellArea.width - fCalcWidth - self.get_property('xpad')))
                iYOffset = int(self.get_property('yalign') * (oCellArea.height - fCalcHeight - self.get_property('ypad')))
            return (iXOffset, iYOffset, int(fCalcWidth), int(fCalcHeight))

    def on_activate(self, _oEvent, _oWidget, oPath, oBackgroundArea, _oCellArea, _iFlags):
        """Activate signal received from the TreeView"""
        self.bClicked = True
        self.oClickedBackgroundArea = oBackgroundArea
        self.emit('clicked', oPath)
        return True

    def on_render(self, oWindow, oWidget, oBackgroundArea, oCellArea, oExposeArea, _iFlags):
        """Render the icon for the button"""
        bDrawOffset = False
        if self.bClicked and oBackgroundArea.x == self.oClickedBackgroundArea.x:
            if oBackgroundArea.y == self.oClickedBackgroundArea.y:
                bDrawOffset = True
                self.bClicked = False
        if self.oPixbuf is None:
            return
        else:
            if not self.bShowIcon:
                return
            oPixRect = gtk.gdk.Rectangle()
            oPixRect.x, oPixRect.y, oPixRect.width, oPixRect.height = self.on_get_size(oWidget, oCellArea)
            oPixRect.x += oCellArea.x
            oPixRect.y += oCellArea.y
            oPixRect.width -= int(2 * self.get_property('xpad'))
            oPixRect.height -= int(2 * self.get_property('ypad'))
            if bDrawOffset:
                oPixRect.x += 1
                oPixRect.y += 1
                gobject.timeout_add(200, self.restore_offset, oWindow, oBackgroundArea)
            oDrawRect = oCellArea.intersect(oPixRect)
            oDrawRect = oExposeArea.intersect(oDrawRect)
            oWindow.draw_pixbuf(oWidget.style.black_gc, self.oPixbuf, oDrawRect.x - oPixRect.x, oDrawRect.y - oPixRect.y, oDrawRect.x, oDrawRect.y, oDrawRect.width, oDrawRect.height, gtk.gdk.RGB_DITHER_NONE, 0, 0)
            return

    def restore_offset(self, oWindow, oArea):
        """queue a redraw so we restore the button."""
        if not self.bClicked:
            oWindow.invalidate_rect(oArea, False)


gobject.type_register(CellRendererSutekhButton)
gobject.signal_new('clicked', CellRendererSutekhButton, gobject.SIGNAL_RUN_FIRST | gobject.SIGNAL_ACTION, gobject.TYPE_NONE, (
 gobject.TYPE_STRING,))