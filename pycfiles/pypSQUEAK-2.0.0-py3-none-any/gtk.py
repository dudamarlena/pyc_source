# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/dswistowski/pso/pypso/src/pypso/ui/gtk.py
# Compiled at: 2007-06-30 10:45:12
__doc__ = 'Wyświetlanie ruch cząsteczek w okienu gtk\n'
from Numeric import array, average
import pygtk
pygtk.require('2.0')
import gtk
from gtk import gdk, glade
import gobject, threading, thread
from pypso.widgets import PsoPainter
from pypso.ui import uiPsoAbstract

class Window(gtk.Window):
    u"""Okienko służące do wyświetlania podgłądu stada"""

    def __init__(self, pso):
        gtk.Window.__init__(self)
        self.set_title('PSO, podgląd stada')
        self.set_default_size(700, 700)
        self.pso_painter = PsoPainter()
        self.pso_painter.setModel(pso)
        self.add(self.pso_painter)
        self.show_all()


class uiPso(uiPsoAbstract):
    u"""Element ui, umożliwiający wyświetlanie stada w okienku rzutującym położenie osobników na płąszczyznę."""

    def _initialize(self):
        gtk.gdk.threads_init()
        mw = Window(self._pso)
        self._pso._gtkwidget = mw.pso_painter
        thread.start_new_thread(gtk.main, ())

        def step(self):
            i = self.old_step()
            return i