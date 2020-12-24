# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/PyPlotter/gtkSupport.py
# Compiled at: 2015-02-27 13:11:06
# Size of source mod 2**32: 5079 bytes
import gtk
from gtk import gdk
try:
    import Gfx, gtkGfx, Graph
except ImportError:
    from . import Gfx, gtkGfx, Graph

class Canvas(object):

    def __init__(self, canvas, pixmap, gfxDriver):
        self.canvas = canvas
        self.pixmap = pixmap
        self.gfxDriver = gfxDriver

    __slots__ = ('canvas', 'pixmap', 'gfxDriver', 'configured')


class NotebookWindow(object):
    __doc__ = 'A gtk window that contains a notbook on canvas pages.'

    def __init__(self, labels=[
 'page 1', 'page 2'], size=(800, 600), title='Gtk Notebook Window'):
        self.redrawHooks = dict.fromkeys(labels, lambda win, label: 1)
        self.numPages = len(labels)
        self.pages = {}
        self.win = gtk.Window()
        (self.win.set_default_size)(*size)
        self.win.set_size_request(512, 384)
        self.win.set_resizable(True)
        self.win.set_title(title)
        self.notebook = gtk.Notebook()
        for l in labels:
            canvas = gtk.DrawingArea()
            canvas.set_size_request(320, 240)
            pixmap = None
            gfxDriver = gtkGfx.Driver(canvas, canvas.create_pango_layout(''))
            self.pages[l] = Canvas(canvas, pixmap, gfxDriver)
            self.notebook.append_page(canvas, gtk.Label(l))
            canvas.connect('configure-event', self.onConfigure)
            canvas.connect('expose-event', self.onExpose)

        self.win.add(self.notebook)
        self.notebook.show()
        self.win.connect('destroy', lambda w: gtk.main_quit())

    def addRedrawHook(self, label, redrawHook=lambda win, label: 1):
        self.redrawHooks[label] = redrawHook

    def get_gfxDriver(self, pageLabel):
        """-> gfxDriver of the page with label 'pageLabel'"""
        return self.pages[pageLabel].gfxDriver

    def get_currentPage(self):
        """-> label of the current page."""
        page = self.notebook.get_nth_page(self.notebook.get_current_page())
        label = self.notebook.get_tab_label(page).get_text()
        return label

    def refresh(self):
        """Refresh the display."""
        page = self.notebook.get_nth_page(self.notebook.get_current_page())
        label = self.notebook.get_tab_label(page).get_text()
        cv = self.pages[label]
        gc = cv.canvas.get_style().fg_gc[gtk.STATE_NORMAL]
        w, h = cv.pixmap.get_size()
        cv.canvas.window.draw_drawable(gc, cv.pixmap, 0, 0, 0, 0, w, h)

    def show(self):
        self.win.show_all()

    def close(self):
        """Close window and finish application."""
        self.win.destroy()
        gtk.main_quit()

    def waitUntilClosed(self):
        self.win.show_all()
        gtk.main()

    def onConfigure(self, widget, event):
        for label, cv in list(self.pages.items()):
            if cv.canvas == widget:
                break
        else:
            raise AssertionError('Cannot find widget!')

        w, h = widget.window.get_size()
        cv.pixmap = gdk.Pixmap(widget.window, w, h)
        cv.gfxDriver.changeDrawable(cv.pixmap)
        self.redrawHooks[label](self.get_gfxDriver(label))
        gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
        widget.window.draw_drawable(gc, cv.pixmap, 0, 0, 0, 0, w, h)
        return True

    def onExpose(self, widget, event):
        for label, cv in list(self.pages.items()):
            if cv.canvas == widget:
                break
        else:
            raise AssertionError('Cannot find widget!')

        x, y, w, h = event.area
        gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
        widget.window.draw_drawable(gc, cv.pixmap, x, y, x, y, w, h)
        return False

    def savePage(self, label=None, name=None, format='png'):
        if label == None:
            label = self.get_currentPage()
        else:
            if name == None:
                name = label
            cv = self.pages[label]
            if cv.pixmap == None:
                return
        pixmap = cv.pixmap
        w, h = pixmap.get_size()
        buf = gdk.Pixbuf(gdk.COLORSPACE_RGB, False, 8, w, h)
        buf.get_from_drawable(pixmap, pixmap.get_colormap(), 0, 0, 0, 0, w, h)
        buf.save(name, format)


def Test():

    def redraw1(gfxDriver):
        if isinstance(graph1.gfx, Gfx.nilDriver):
            graph1.changeGfx(gfxDriver)
        graph1.resizedGfx()

    def redraw2(gfxDriver):
        if isinstance(graph2.gfx, Gfx.nilDriver):
            graph2.changeGfx(gfxDriver)
        graph2.resizedGfx()

    graph1 = Graph.Cartesian(Gfx.nilDriver(), 0.0, 0.0, 1.0, 1.0)
    graph2 = Graph.Cartesian(Gfx.nilDriver(), -1.0, -1.0, 1.0, 1.0)
    win = NotebookWindow(labels=['graph1', 'graph2'])
    win.addRedrawHook('graph1', redraw1)
    win.addRedrawHook('graph2', redraw2)
    win.show()
    win.waitUntilClosed()


if __name__ == '__main__':
    Test()