# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/mpleditor.py
# Compiled at: 2015-06-08 14:22:06
from traits.trait_base import ETSConfig
_tk = ETSConfig.toolkit
if _tk is None or _tk == 'null':
    raise NotImplementedError('We must independently set the toolkit')
from traits.api import Any, Int, Bool, Instance, Either
from traitsui.basic_editor_factory import BasicEditorFactory
from matplotlib.figure import Figure
FigureCanvas = getattr(__import__('matplotlib.backends.backend_%sagg' % _tk, fromlist=[
 'FigureCanvas']), 'FigureCanvas%sAgg' % ('Wx' if _tk == 'wx' else 'QT'))
Editor = __import__('traitsui.%s.editor' % _tk, fromlist=['Editor']).Editor
import numpy as np, time

class _MPLFigureEditor(Editor):
    scrollable = True
    parent = Any
    canvas = Instance(FigureCanvas)
    tooltip = Any
    release_cid = Int
    motion_cid = Int
    waiting_for_tooltip = Bool(False)

    def init(self, parent):
        self.parent = parent
        self.control = self._create_canvas(parent)

    def update_editor(self):
        pass

    def _create_canvas(self, *args):
        return getattr(self, '_create_canvas_%s' % _tk)(*args)

    def _create_canvas_wx(self, parent):
        import wx
        fig = self.object.circ
        panel = wx.Panel(parent, -1)
        self.canvas = canvas = FigureCanvas(panel, -1, fig)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 1)
        panel.SetSizer(sizer)
        canvas.mpl_connect('button_press_event', self.object.circle_click)
        canvas.mpl_connect('motion_notify_event', lambda ev: self.object.circle_mouseover(ev, self._update_tooltip_wx))
        self.tooltip = wx.ToolTip(tip='')
        self.tooltip.SetDelay(2000)
        canvas.SetToolTip(self.tooltip)
        return panel

    def _update_tooltip_wx(self, tooltip_on, text=''):
        if tooltip_on:
            self.tooltip.Enable(True)
            self.tooltip.SetTip(text)
        else:
            self.tooltip.Enable(False)

    def _create_canvas_qt4(self, parent):
        import matplotlib
        from pyface.qt import QtCore, QtGui
        self.tooltip = panel = QtGui.QWidget()
        fig = self.object.circ
        self.canvas = canvas = FigureCanvas(fig)
        layout = QtGui.QVBoxLayout(panel)
        layout.addWidget(canvas)
        canvas.mpl_connect('button_press_event', self.object.circle_click)
        canvas.mpl_connect('motion_notify_event', lambda ev: self.object.circle_mouseover(ev, self._update_tooltip_qt))
        return panel

    def _update_tooltip_qt(self, tooltip_on, text=''):
        if tooltip_on:
            self.tooltip.setToolTip(text)
        else:
            self.tooltip.setToolTip(None)
        return

    def _process_circ_click(self, event, cvu):
        if event.button == 3:
            cvu.display_all()
            return
        if event.button == 2:
            self.object.mpleditor = self
            return
        self.release_cid = self.canvas.mpl_connect('button_release_event', lambda ignore: self._single_click(event, cvu))

    def _single_click(self, event, cvu):
        self._clear_callbacks()
        if event.button == 1 and event.ydata >= 7 and event.ydata <= 8:
            nod = cvu.nr_labels * event.xdata / (np.pi * 2) + 0.5 * np.pi / cvu.nr_labels
            cvu.display_node(int(np.floor(nod)))

    def _possibly_show_tooltip(self, event, cvu):
        self._clear_callbacks()
        if event.ydata >= 7 and event.ydata <= 8:
            nod = int(np.floor(cvu.nr_labels * event.xdata / (np.pi * 2) + 0.5 * np.pi / cvu.nr_labels))
            self.tooltip.Enable(True)
            self.tooltip.SetTip(cvu.labnam[nod])
        else:
            self.tooltip.Enable(False)

    def _move_unset_tooltip(self, ignore):
        self.waiting_for_tooltip = False

    def _clear_callbacks(self):
        self.canvas.mpl_disconnect(self.release_cid)

    def _pan_decide(self, event):
        ax = self.canvas.figure.get_axes()[0]
        ax.set_navigate_mode('PAN')
        ax.start_pan(event.x, event.y, 1)
        self._pan(event)
        self._clear_callbacks()
        self.release_cid = self.canvas.mpl_connect('button_release_event', self._end_pan)
        self.motion_cid = self.canvas.mpl_connect('motion_notify_event', self._pan)

    def _pan(self, event):
        ax = self.canvas.figure.get_axes()[0]
        ax.drag_pan(1, event.key, event.x, event.y)
        self.canvas.draw()

    def _end_pan(self, event):
        ax = self.canvas.figure.get_axes()[0]
        ax.end_pan()
        self._clear_callbacks()


class MPLFigureEditor(BasicEditorFactory):
    klass = _MPLFigureEditor