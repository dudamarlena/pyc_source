# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/charteditor.py
# Compiled at: 2013-04-11 17:47:52
import logging
from PyQt4 import QtGui
from PyQt4 import QtCore
from camelot.admin.action.list_action import ListActionGuiContext
from camelot.core.utils import ugettext as _
from camelot.view.controls.editors.customeditor import AbstractCustomEditor
from camelot.view.controls.editors.wideeditor import WideEditor
from camelot.view.proxy import ValueLoading
from camelot.view.art import Icon
PAD_INCHES = 0.1
LOGGER = logging.getLogger('camelot.view.controls.editors.charteditor')

class ChartEditor(QtGui.QFrame, AbstractCustomEditor, WideEditor):
    """Editor to display and manipulate matplotlib charts.  The editor
    itself is generic for all kinds of plots,  it simply provides the
    data to be ploted with a set of axes.  The data itself should know
    how exactly to plot itself.
    """
    show_fullscreen_signal = QtCore.pyqtSignal()
    editingFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None, width=50, height=40, dpi=50, field_name='chart', **kwargs):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
        super(ChartEditor, self).__init__(parent)
        AbstractCustomEditor.__init__(self)
        self.setObjectName(field_name)
        chart_frame = QtGui.QFrame(self)
        chart_frame.setFrameShape(self.Box)
        chart_frame.setContentsMargins(1, 1, 1, 1)
        chart_frame_layout = QtGui.QHBoxLayout()
        chart_frame_layout.setContentsMargins(0, 0, 0, 0)
        chart_frame.setLayout(chart_frame_layout)
        self.fig = Figure(figsize=(
         width, height), dpi=dpi, facecolor='#ffffff')
        layout = QtGui.QHBoxLayout()
        self.canvas = FigureCanvas(self.fig)
        chart_frame_layout.addWidget(self.canvas)
        layout.addWidget(chart_frame)
        button_layout = QtGui.QVBoxLayout()
        button_layout.setSpacing(0)
        icon = Icon('tango/16x16/actions/document-print-preview.png').getQIcon()
        button_layout.addStretch()
        print_button = QtGui.QToolButton()
        print_button.setIcon(icon)
        print_button.setAutoRaise(True)
        print_button.setToolTip(_('Print Preview'))
        print_button.clicked.connect(self.print_preview)
        button_layout.addWidget(print_button)
        icon = Icon('tango/16x16/actions/edit-copy.png').getQIcon()
        copy_button = QtGui.QToolButton()
        copy_button.setIcon(icon)
        copy_button.setAutoRaise(True)
        copy_button.setToolTip(_('Copy to clipboard'))
        copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(copy_button)
        layout.addLayout(button_layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.canvas.installEventFilter(self)
        self.show_fullscreen_signal.connect(self.show_fullscreen)
        self.canvas.updateGeometry()
        self._litebox = None
        self.gui_context = ListActionGuiContext()
        return

    @QtCore.pyqtSlot()
    def copy_to_clipboard(self):
        """Copy the chart to the clipboard"""
        clipboard = QtGui.QApplication.clipboard()
        pixmap = QtGui.QPixmap.grabWidget(self.canvas)
        clipboard.setPixmap(pixmap)

    @QtCore.pyqtSlot()
    def print_preview(self):
        """Popup a print preview dialog for the Chart"""
        from camelot.view.action_steps import PrintChart
        print_chart = PrintChart(self._value)
        print_chart.gui_run(self.gui_context)

    def set_field_attributes(self, *args, **kwargs):
        """Overwrite set_field attributes because a ChartEditor cannot be disabled
        or have its background color changed"""
        pass

    @staticmethod
    def show_fullscreen_chart(chart, parent):
        """
        :param chart: a chart container
        :return: the widget showing the chart, by default a LiteBoxView
        """
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
        from camelot.view.controls.liteboxview import LiteBoxView
        from camelot.container.chartcontainer import structure_to_figure_container
        figure_container = structure_to_figure_container(chart)
        litebox = LiteBoxView(parent)
        fig = Figure(facecolor='#ffffff')
        canvas = FigureCanvas(fig)
        canvas.updateGeometry()
        figure_container.plot_on_figure(fig)
        proxy = QtGui.QGraphicsProxyWidget()
        proxy.setWidget(canvas)
        litebox.show_fullscreen_item(proxy)
        canvas.draw()
        return litebox

    @QtCore.pyqtSlot()
    def show_fullscreen(self):
        """Show the plot full screen, using the litebox"""
        if self._value:
            self._litebox = self.show_fullscreen_chart(self._value, None)
        return

    def eventFilter(self, object, event):
        """intercept mouse clicks on a chart to show the chart fullscreen"""
        if not object.isWidgetType():
            return False
        if event.type() != QtCore.QEvent.MouseButtonPress:
            return False
        if event.modifiers() != QtCore.Qt.NoModifier:
            return False
        if event.buttons() == QtCore.Qt.LeftButton:
            self.show_fullscreen_signal.emit()
            return True
        return False

    def set_value(self, value):
        """Accepts a camelot.container.chartcontainer.FigureContainer or a 
        camelot.container.chartcontainer.AxesContainer """
        from camelot.container.chartcontainer import structure_to_figure_container
        self._value = structure_to_figure_container(AbstractCustomEditor.set_value(self, value))
        self.on_draw()

    def get_value(self):
        return AbstractCustomEditor.get_value(self) or self._value

    def on_draw(self):
        """draw the matplotlib figure on the canvas"""
        if self._value not in (None, ValueLoading):
            self._value.plot_on_figure(self.fig)
            self.canvas.draw()
        return