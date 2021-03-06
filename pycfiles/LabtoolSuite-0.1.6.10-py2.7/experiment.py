# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Labtools/experiment.py
# Compiled at: 2015-05-25 05:35:35
import os
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import PyQt4.QtGui as Widgets
from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
import sys, functools, random, scipy.optimize as optimize, scipy.fftpack as fftpack
from Labtools.templates import template_exp
import time, sys
from customui_rc import *
import custom_widgets as Widgets, numpy as np, pyqtgraph as pg, pyqtgraph.opengl as gl, sys

class QIPythonWidget(RichIPythonWidget):

    def __init__(self, customBanner=None, *args, **kwargs):
        print 'importing KernelManager'
        from IPython.qt.inprocess import QtInProcessKernelManager
        print 'import GuiSupport'
        from IPython.lib import guisupport
        if customBanner != None:
            self.banner = customBanner
        print 'initializing'
        super(QIPythonWidget, self).__init__(*args, **kwargs)
        print 'kernel manager creating'
        self.kernel_manager = kernel_manager = QtInProcessKernelManager()
        print 'kernel manager starting'
        kernel_manager.start_kernel()
        kernel_manager.kernel.gui = 'qt4'
        self.kernel_client = kernel_client = self._kernel_manager.client()
        kernel_client.start_channels()

        def stop():
            kernel_client.stop_channels()
            kernel_manager.shutdown_kernel()
            guisupport.get_app_qt4().exit()

        self.exit_requested.connect(stop)
        return

    def pushVariables(self, variableDict):
        """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
        self.kernel_manager.kernel.shell.push(variableDict)

    def clearTerminal(self):
        """ Clears the terminal """
        self._control.clear()

    def printText(self, text):
        """ Prints some plain text to the console """
        self._append_plain_text(text)

    def executeCommand(self, command):
        """ Execute a command in the frame of the console widget """
        self._execute(command, False)


class ConvenienceClass:
    """
        This class contains methods that simplify setting up and running
        an experiment.
        
        The :func:`arbitFit` method accepts two arrays, the fitting function,
        and a keyword argument 'guess' that is an array containing
        guess values for the various fiting parameters.
        Guess values can be obtained using the :func:`getGuessValues` based on
        a keyword argument 'func' which as of this moment can be either 'sine' 
        or 'damped sine'
        """
    timers = []

    def __init__(self):
        self.timers = []

    def loopTask(self, interval, func, *args):
        """
                Creates a QTimer that executes 'func' every 'interval' milliseconds
                all additional arguments passed to this function are passed on as
                arguments to func
                
                Refer to the source code for experiments such as diodeIV, Bandpass filter etc.
                
                
                """
        timer = QTimer()
        timerCallback = functools.partial(func, *args)
        timer.timeout.connect(timerCallback)
        timer.start(interval)
        self.timers.append(timer)
        return timer

    def delayedTask(self, interval, func, *args):
        """
                Creates a QTimer that executes 'func' once after 'interval' milliseconds.
                
                all additional arguments passed to this function are passed on as
                arguments to func
                
                
                """
        timer = QTimer()
        timerCallback = functools.partial(func, *args)
        timer.singleShot(interval, timerCallback)
        self.timers.append(timer)

    def random_color(self):
        c = (
         random.randint(20, 255), random.randint(20, 255), random.randint(20, 255))
        if np.average(c) < 150:
            c = self.random_color()
        return c

    def displayObjectContents(self, d):
        """
                The contents of the dictionary 'd' are displayed in a new QWindow
                
                """
        self.tree = pg.DataTreeWidget(data=d)
        self.tree.show()
        self.tree.setWindowTitle('Data')
        self.tree.resize(600, 600)

    def dampedSine(self, x, amp, freq, phase, offset, damp):
        """
                A damped sine wave function
                
                """
        return offset + amp * np.exp(-damp * x) * np.sin(abs(freq) * x + phase)

    def fitData(self, xReal, yReal, **args):

        def mysine(x, a1, a2, a3, a4):
            return a4 + a1 * np.sin(abs(a2) * x + a3)

        N = len(xReal)
        yhat = fftpack.rfft(yReal)
        idx = (yhat ** 2).argmax()
        freqs = fftpack.rfftfreq(N, d=(xReal[1] - xReal[0]) / (2 * np.pi))
        frequency = freqs[idx]
        amplitude = (yReal.max() - yReal.min()) / 2.0
        offset = yReal.max() - yReal.min()
        frequency = args.get('frequency', 1000000.0 * abs(frequency) / (2 * np.pi)) * (2 * np.pi) / 1000000.0
        phase = args.get('phase', 0.0)
        guess = [amplitude, frequency, phase, offset]
        try:
            (amplitude, frequency, phase, offset), pcov = optimize.curve_fit(mysine, xReal, yReal, guess)
            ph = phase * 180 / np.pi
            if frequency < 0:
                return (
                 0, 0, 0, 0, pcov)
            if amplitude < 0:
                ph -= 180
            if ph < -90:
                ph += 360
            if ph > 360:
                ph -= 360
            freq = 1000000.0 * abs(frequency) / (2 * np.pi)
            amp = abs(amplitude)
            if frequency:
                period = 1.0 / frequency
            else:
                period = 0
            pcov[0] *= 1000000.0
            return (amp, freq, ph, offset, pcov)
        except:
            return (
             0, 0, 0, 0, [[]])

    def getGuessValues(self, xReal, yReal, func='sine'):
        if func == 'sine' or func == 'damped sine':
            N = len(xReal)
            offset = np.average(yReal)
            yhat = fftpack.rfft(yReal - offset)
            idx = (yhat ** 2).argmax()
            freqs = fftpack.rfftfreq(N, d=(xReal[1] - xReal[0]) / (2 * np.pi))
            frequency = freqs[idx]
            amplitude = (yReal.max() - yReal.min()) / 2.0
            phase = 0.0
            if func == 'sine':
                return (amplitude, frequency, phase, offset)
            if func == 'damped sine':
                return (amplitude, frequency, phase, offset, 0)

    def arbitFit(self, xReal, yReal, func, **args):
        N = len(xReal)
        guess = args.get('guess', [])
        try:
            results, pcov = optimize.curve_fit(func, xReal, yReal, guess)
            pcov[0] *= 1000000.0
            return (True, results, pcov)
        except:
            return (
             False, [], [])


class Experiment(QMainWindow, template_exp.Ui_MainWindow, Widgets.CustomWidgets):

    def __init__(self, **args):
        self.qt_app = args.get('qt_app', QApplication(sys.argv))
        super(Experiment, self).__init__(args.get('parent', None))
        self.setupUi(self)
        Widgets.CustomWidgets.__init__(self)
        self.timers = []
        self.I = args.get('I', None)
        self.graphContainer2_enabled = False
        print 'HERE', self.I
        self.graphContainer1_enabled = False
        self.console_enabled = False
        self.output_enabled = False
        self.viewBoxes = []
        self.plot_areas = []
        self.plots3D = []
        self.plots2D = []
        self.total_plot_areas = 0
        self.widgetBay = False
        if args.get('showresult', True):
            dock = QDockWidget()
            dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
            dock.setWindowTitle('Results')
            self.output_text = QTextEdit()
            self.output_text.setReadOnly(True)
            fr = QFrame()
            plt = QGridLayout(fr)
            plt.setMargin(0)
            plt.addWidget(self.output_text)
            self.output_enabled = True
            sys.stdout = self.relay_to_console(self.output_text)
            dock.setWidget(fr)
            self.result_dock = dock
            self.output_text.setStyleSheet('color: rgb(255, 255, 255);')
            self.addDockWidget(Qt.BottomDockWidgetArea, dock)

            def __resizeHack__():
                self.result_dock.setMaximumHeight(100)
                self.qt_app.processEvents()
                self.result_dock.setMaximumHeight(2500)

            self.delayedTask(0, __resizeHack__)
        if args.get('handler', False):
            self.addHandler(args.get('handler'))
        return

    def addPlotArea(self):
        fr = QFrame(self.graph_splitter)
        fr.setFrameShape(QFrame.StyledPanel)
        fr.setFrameShadow(QFrame.Raised)
        fr.setMinimumHeight(250)
        self.total_plot_areas += 1
        fr.setObjectName('plot' + str(self.total_plot_areas))
        plt = QGridLayout(fr)
        plt.setMargin(0)
        self.plot_areas.append(plt)
        return len(self.plot_areas) - 1

    def add3DPlot(self):
        plot3d = gl.GLViewWidget()
        gz = gl.GLGridItem()
        plot3d.addItem(gz)
        plot3d.opts['distance'] = 40
        plot3d.opts['elevation'] = 5
        plot3d.opts['azimuth'] = 20
        pos = self.addPlotArea()
        self.plot_areas[pos].addWidget(plot3d)
        self.plots3D.append(plot3d)
        plot3d.plotLines3D = []
        return plot3d

    def add2DPlot(self):
        plot = pg.PlotWidget()
        pos = self.addPlotArea()
        self.plot_areas[pos].addWidget(plot)
        plot.viewBoxes = []
        plot.addLegend(offset=(-1, 1))
        self.plots2D.append(plot)
        return plot

    def add2DPlots(self, num):
        for a in range(num):
            yield self.add2DPlot()

    def add3DPlots(self, num):
        for a in range(num):
            yield self.add3DPlot()

    def enableRightAxis(self, plot):
        p = pg.ViewBox()
        plot.showAxis('right')
        plot.setMenuEnabled(False)
        plot.scene().addItem(p)
        plot.getAxis('right').linkToView(p)
        p.setXLink(plot)
        plot.viewBoxes.append(p)
        Callback = functools.partial(self.updateViews, plot)
        plot.getViewBox().sigStateChanged.connect(Callback)
        return p

    def updateViews(self, plot):
        for a in plot.viewBoxes:
            a.setGeometry(plot.getViewBox().sceneBoundingRect())

    def configureWidgetBay(self, name='controls'):
        if self.widgetBay:
            return
        dock = QDockWidget()
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        dock.setWindowTitle(name)
        fr = QFrame()
        fr.setStyleSheet('QLineEdit {color: rgb(0,0,0);}QPushButton, QLabel ,QComboBox{color: rgb(255, 255, 255);}')
        dock.setWidget(fr)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.frame_area = QVBoxLayout(fr)
        self.frame_area.setMargin(0)
        self.widgetBay = True

    def updateWidgetBay(self, obj):
        self.configureWidgetBay()
        self.frame_area.addWidget(obj)

    def addHandler(self, handler, name='Controls'):
        """
                Add handler instance(subclass of QFrame) to the left side of the window.
                The contents of the handler are QWidgets which control various aspects
                of the experiment that the handler has been designed for.
                """
        self.configureWidgetBay(name)
        self.frame = handler
        self.updateWidgetBay(self.frame)
        try:
            self.I = handler.I
            if self.console_enabled:
                self.ipyConsole.pushVariables({'I': self.I})
                self.ipyConsole.printText("Access hardware using the Instance 'I'.  e.g.  I.get_average_voltage(0)")
        except:
            print 'Device Not Connected.'

    def addConsole(self, **args):
        dock = QDockWidget()
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        dock.setWindowTitle('plot' + str(self.total_plot_areas + 1))
        fr = QFrame()
        dock.setWidget(fr)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)
        fr.setFrameShape(QFrame.StyledPanel)
        fr.setFrameShadow(QFrame.Raised)
        self.ipyConsole = QIPythonWidget(customBanner='This is an interactive Python Console\n')
        layout = QVBoxLayout(fr)
        layout.setMargin(0)
        layout.addWidget(self.ipyConsole)
        cmdDict = {'delayedTask': self.delayedTask, 'loopTask': self.loopTask, 'addWidget': self.addWidget, 'setCommand': self.setCommand, 'Widgets': Widgets}
        if self.I:
            cmdDict['I'] = self.I
            self.ipyConsole.printText("Access hardware using the Instance 'I'.  e.g.  I.get_average_voltage('CH1')")
        self.ipyConsole.pushVariables(cmdDict)
        self.console_enabled = True

    def new3dSurface(self, plot, **args):
        import scipy.ndimage as ndi
        surface3d = gl.GLSurfacePlotItem(z=np.array([[0.1, 0.1], [0.1, 0.1]]), **args)
        plot.addItem(surface3d)
        return surface3d

    def setSurfaceData(self, surf, z):
        surf.setData(z=np.array(z))

    def draw3dLine(self, plot, x, y, z, color=(100, 100, 100)):
        pts = np.vstack([x, y, z]).transpose()
        plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor(color), width=2)
        plot.addItem(plt)
        plot.plotLines3D.append(plt)
        return plt

    def clearLinesOnPlane(self, plot):
        for a in plot.plotLines3D:
            plot.removeItem(a)

        plot.plotLines3D = []

    class relay_to_console:

        def __init__(self, console):
            self.console = console
            self.cursor = self.console.textCursor()
            self.scroll = self.console.verticalScrollBar()

        def write(self, arg):
            f = open('b.txt', 'at')
            self.cursor.movePosition(QTextCursor.End)
            self.console.setTextCursor(self.cursor)
            self.console.insertPlainText(arg)
            f.write(arg)

        def flush(self):
            pass

    def graph(self, x, y):
        if self.graphContainer1_enabled:
            self.reserved_curve.setData(x, y)

    def setRange(self, plot, x, y, width, height):
        plot.setRange(QtCore.QRectF(x, y, width, height))

    def addCurve(self, plot, name='', col=(255, 255, 255), axis='left'):
        if len(name):
            curve = pg.PlotCurveItem(name=name)
        else:
            curve = pg.PlotCurveItem()
        plot.addItem(curve)
        curve.setPen(color=col, width=1)
        return curve

    def rebuildLegend(plot, self):
        self.plotLegend = plot.addLegend(offset=(-10, 30))

    def loopTask(self, interval, func, *args):
        timer = QTimer()
        timerCallback = functools.partial(func, *args)
        timer.timeout.connect(timerCallback)
        timer.start(interval)
        self.timers.append(timer)
        return timer

    def delayedTask(self, interval, func, *args):
        timer = QTimer()
        timerCallback = functools.partial(func, *args)
        timer.singleShot(interval, timerCallback)
        self.timers.append(timer)

    def run(self):
        self.show()
        self.qt_app.exec_()

    def add_a_widget(self):
        self.addButton('testing')

    def addButton(self, name, command, *args):
        b = QPushButton(None)
        b.setText(name)
        self.updateWidgetBay(b)
        self.setCommand(b, 'clicked()', command, *args)
        return b

    def addWidget(self, widget_type, **args):
        b = widget_type(**args)
        if args.has_key('object_name'):
            b.setObjectName(args.get('object_name'))
        if args.has_key('text'):
            b.setText(args.get('text'))
        if args.has_key('items'):
            for a in args.get('items'):
                b.addItem(a)

        self.updateWidgetBay(b)
        return b

    def setCommand(self, widget, signal, slot, *args):
        buttonCallback = functools.partial(slot, *args)
        QObject.connect(widget, SIGNAL(signal), buttonCallback)