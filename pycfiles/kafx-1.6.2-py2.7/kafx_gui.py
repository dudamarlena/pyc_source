# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\kafx_gui.py
# Compiled at: 2012-02-17 22:06:06
import gtk, gtk.glade, gobject, weakref, gc

class Window:
    window = None

    def __init__(self):
        xml = gtk.glade.XML('gui.glade')
        self.window = xml.get_widget('Window')

    def Show(self):
        if self.window:
            self.window.show()
        else:
            print 'No pude cargar la ventana, D:!'

    def Process_Click(self):
        print 'asldk'


if __name__ == '__main__':
    ventana = Window()
    ventana.Show()
    gtk.main()