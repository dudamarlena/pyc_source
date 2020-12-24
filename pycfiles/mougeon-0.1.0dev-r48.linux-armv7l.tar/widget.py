# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mougeon/gui/hildon/widget.py
# Compiled at: 2012-03-01 11:28:37
"""
Created on 01 March 2012 04:19:29

@author: maemo
"""
import gtk, hildon
from mougeon.common import version
from mougeon.core import model
version.getInstance().submitRevision('$Revision: 4 $')
from mougeon.gui.gtk.utils import FREE_PIXBUF, ORAGNE_PIXBUF

class OperatorThumbnail(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self)

    def add_picture(self, miniature):
        image = gtk.Image()
        image.set_from_pixbuf(miniature)
        self.pack_start(image, False, False, 0)

    def add_button(self, op_name, usage_percent, miniature):
        self.button = hildon.Button(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        self.button.set_title(op_name)
        self.button.set_value(str(usage_percent))
        image = gtk.Image()
        image.set_from_pixbuf(miniature)
        self.button.set_image(image)
        self.pack_start(self.button, False, False, 0)

    def connect_action(self, *argv, **kwarg):
        self.button.connect('clicked', *argv, **kwarg)


class FreeThumbnail(OperatorThumbnail):

    def __init__(self, facade):
        OperatorThumbnail.__init__(self)
        self.add_button(model.FREE_OPERATOR.name, facade.freemobile_percent(), FREE_PIXBUF)


class OrangeThumbnail(OperatorThumbnail):

    def __init__(self, facade):
        OperatorThumbnail.__init__(self)
        self.add_button(model.ORANGE_OPERATOR.name, facade.orange_percent(), ORAGNE_PIXBUF)