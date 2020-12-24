# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/gnatirac/gui/hildon/widget.py
# Compiled at: 2012-03-21 06:33:46
"""
Created on Dec 29, 2011

@author: maemo
"""
import gtk, hildon, urllib, logging
from gnatirac.gui.gtk.utils import LOGO_PIXBUF

class AlbumThumbnail(gtk.VBox):

    def __init__(self, album):
        gtk.VBox.__init__(self)
        miniature = None
        if album.thumbnail_url:
            logging.debug('retrieving thumbnail %s' % album.thumbnail_url)
            miniature = gtk.gdk.pixbuf_new_from_file(urllib.urlretrieve(album.thumbnail_url)[0])
        else:
            miniature = LOGO_PIXBUF
        image = gtk.Image()
        image.set_from_pixbuf(miniature)
        self.pack_start(image, False, False, 0)
        self.button = hildon.Button(gtk.HILDON_SIZE_FINGER_HEIGHT | gtk.HILDON_SIZE_HALFSCREEN_WIDTH, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        self.button.set_title(album.title)
        self.button.set_value(str(album.numphotos))
        self.pack_start(self.button, False, False, 0)
        return

    def connect_action(self, *argv, **kwarg):
        self.button.connect('clicked', *argv, **kwarg)


class ShotThumbnail(gtk.VBox):

    def __init__(self, shot, prev=None, next=None):
        gtk.VBox.__init__(self)
        self.prev = prev
        self.next = next
        self.shot = shot
        miniature = None
        if shot.thumbnail_url:
            logging.debug('retrieving thumbnail %s' % shot.thumbnail_url)
            miniature = gtk.gdk.pixbuf_new_from_file(urllib.urlretrieve(shot.thumbnail_url)[0])
        else:
            miniature = LOGO_PIXBUF
        image = gtk.Image()
        image.set_from_pixbuf(miniature)
        self.pack_start(image, False, False, 0)
        self.button = hildon.Button(gtk.HILDON_SIZE_FINGER_HEIGHT | gtk.HILDON_SIZE_HALFSCREEN_WIDTH, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        self.button.set_title(shot.title)
        self.pack_start(self.button, False, False, 0)
        return

    def connect_action(self, *argv, **kwarg):
        self.button.connect('clicked', *argv, **kwarg)