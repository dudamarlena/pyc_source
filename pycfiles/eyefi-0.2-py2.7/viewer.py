# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eyefi/viewer.py
# Compiled at: 2010-11-28 08:25:57
from enthought.traits.api import HasTraits, Int, File, Str
from enthought.traits.ui.api import ImageEditor, Item, View, HGroup, VGroup, Image
from twisted.internet import gtk2reactor
import wx

class Viewer(HasTraits):
    view = View(Item('image', editor=ImageEditor(), show_label=False, resizable=True), resizable=True)
    image = Image('/home/rj/test.jpg')


def main():
    reactor = gtk2reactor.install()
    v = Viewer()
    view = v.edit_traits()
    view.control.ShowFullScreen(True)
    reactor.callLater(1, reactor.stop)
    reactor.run()
    return v


if __name__ == '__main__':
    v = main()