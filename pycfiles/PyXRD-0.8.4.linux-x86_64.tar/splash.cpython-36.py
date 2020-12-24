# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/application/splash.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 7127 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from time import time, sleep
from pyxrd.application.icons import get_icon_list

def scale_ratio(src_width, src_height, dest_width, dest_height):
    """Return a size fitting into dest preserving src's aspect ratio."""
    if src_height > dest_height:
        if src_width > dest_width:
            ratio = min(float(dest_width) / src_width, float(dest_height) / src_height)
        else:
            ratio = float(dest_height) / src_height
    else:
        if src_width > dest_width:
            ratio = float(dest_width) / src_width
        else:
            ratio = 1
    return (
     int(ratio * src_width), int(ratio * src_height))


class ScalableImage(Gtk.Image):
    __doc__ = 'A Gtk.Image that rescales to fit whatever size is available.\n\n    Only Pixbuf data is supported; it can be loaded from a file or\n    passed directly.\n    '

    def __init__(self, pixbuf=None):
        super(ScalableImage, self).__init__()
        self._pixbuf = None
        self.connect('size-allocate', self._on_size_allocate)
        self.set_size_request(1, 1)
        self._hyper_id = None
        if pixbuf is not None:
            self.set_from_pixbuf(pixbuf)

    def _on_timeout_hyper(self):
        self._hyper_id = None
        allocation = self.get_allocation()
        target_width, target_height = scale_ratio(self._pixbuf.get_width(), self._pixbuf.get_height(), allocation.width, allocation.height)
        if target_width > 0:
            if target_height > 0:
                pixbuf = self._pixbuf.scale_simple(target_width, target_height, GdkPixbuf.InterpType.HYPER)
                super(ScalableImage, self).set_from_pixbuf(pixbuf)

    def _on_size_allocate(self, image, allocation, force=False):
        """Scale the internal pixbuf copy to a new size."""
        if self._pixbuf is None:
            return
        else:
            pix_width = self._pixbuf.get_width()
            pix_height = self._pixbuf.get_height()
            target_width, target_height = scale_ratio(pix_width, pix_height, allocation.width, allocation.height)
            old_pix = self.get_pixbuf()
            if target_width < pix_width or target_height < pix_height:
                if force or not old_pix or old_pix.get_width() != target_width or old_pix.get_height() != target_height:
                    if self._hyper_id:
                        GObject.source_remove(self._hyper_id)
                        self._hyper_id = None
                    if target_width > 0:
                        if target_height > 0:
                            pixbuf = self._pixbuf.scale_simple(target_width, target_height, GdkPixbuf.InterpType.HYPER if force else GdkPixbuf.InterpType.NEAREST)
                            if not force:
                                self._hyper_id = GObject.timeout_add(100, self._on_timeout_hyper)
                            super(ScalableImage, self).set_from_pixbuf(pixbuf)
            elif old_pix != self._pixbuf:
                if self._hyper_id:
                    GObject.source_remove(self._hyper_id)
                    self._hyper_id = None
                super(ScalableImage, self).set_from_pixbuf(self._pixbuf)

    def set_from_file(self, filename):
        """Set the image by loading a file."""
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
        self.set_from_pixbuf(pixbuf)

    def set_from_pixbuf(self, pixbuf):
        """Set the image from a GdkPixbuf.Pixbuf."""
        self._pixbuf = pixbuf
        self._on_size_allocate(None, (self.get_allocation()), force=True)

    def __not_implemented(self, *args):
        """This Gtk.Image storage type is not supported."""
        raise NotImplementedError('only pixbuf images are currently supported')

    set_from_animation = _ScalableImage__not_implemented
    set_from_gicon = _ScalableImage__not_implemented
    set_from_icon_name = _ScalableImage__not_implemented
    set_from_icon_set = _ScalableImage__not_implemented
    set_from_image = _ScalableImage__not_implemented
    set_from_pixmap = _ScalableImage__not_implemented
    set_from_stock = _ScalableImage__not_implemented


class SplashScreen(object):

    def __init__(self, filename, version=''):
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_auto_startup_notification(False)
        self.window.set_default_icon_list(get_icon_list())
        self.window.set_icon_list(get_icon_list())
        self.window.set_title('PyXRD')
        self.window.set_skip_taskbar_hint(True)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_decorated(False)
        self.window.set_resizable(False)
        self.window.set_border_width(1)
        self.window.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('white'))
        ebox = Gtk.EventBox()
        self.window.add(ebox)
        main_vbox = Gtk.VBox(False, 1)
        main_vbox.set_border_width(10)
        ebox.add(main_vbox)
        self.img = ScalableImage()
        self.img.set_from_file(filename)
        self.img.set_size_request(500, 300)
        main_vbox.pack_start(self.img, True, True, 0)
        self.lbl = Gtk.Label()
        self.lbl.set_markup('<span size="larger"><b>Loading ...</b></span>')
        self.lbl.set_alignment(0.5, 0.5)
        main_vbox.pack_end(self.lbl, True, True, 0)
        self.version_lbl = Gtk.Label()
        self.version_lbl.set_markup('<i>Version %s</i>' % version)
        self.version_lbl.set_alignment(0.5, 0.5)
        main_vbox.pack_end(self.version_lbl, True, True, 0)
        self.window.show_all()
        while Gtk.events_pending():
            Gtk.main_iteration()

        self.start_time = time()
        self.closed = False

    def set_message(self, message):
        self.lbl.set_markup('<span size="larger"><b>%s</b></span>' % message)
        while Gtk.events_pending():
            Gtk.main_iteration()

    def close(self):
        if not self.closed:
            self.window.set_auto_startup_notification(True)
            while max(5 - (time() - self.start_time), 0) != 0:
                sleep(0.1)
                while Gtk.events_pending():
                    Gtk.main_iteration()

            self.window.destroy()
            del self.window
            del self.lbl
            del self.img
            del self.version_lbl
            self.closed = True