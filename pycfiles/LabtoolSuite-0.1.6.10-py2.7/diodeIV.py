# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Labtools/Apps/diodeIV.py
# Compiled at: 2015-05-19 05:34:11
import Labtools.interface as interface
from Labtools import experiment
from Labtools.templates.template_diode import Ui_Form
from PyQt4.QtGui import QFrame
from PyQt4.QtCore import QTimer
import numpy as np

class Handler(QFrame, Ui_Form):

    def __init__(self, Exp):
        super(Handler, self).__init__()
        self.setupUi(self)
        self.I = interface.Interface()
        self.timegap = 0
        self.looptimer = QTimer()
        self.plot = Exp.add2DPlot()
        self.plot3d = Exp.add3DPlot()
        self.trace = Exp.addCurve(self.plot, 'IV', (255, 0, 255))
        Exp.setRange(self.plot, 0, 0, 1.0, 0.0015)
        self.plot.setLabel('bottom', 'Voltage -->>', units='V')
        self.plot.setLabel('left', 'Current -->>', units='A')

    def start(self, x=None):
        self.Vval = 0.0
        self.num = 0
        Exp.clearLinesOnPlane(self.plot3d)
        self.X = []
        self.Y = []
        self.scaleX = 20 / 0.6
        self.offX = -10
        self.scaleY = 20 / 0.001
        self.offY = -10
        if not self.looptimer.isActive():
            self.looptimer = Exp.loopTask(self.timegap, self.acquire, 0)

    def acquire(self, chan):
        self.I.set_pvs2(self.Vval)
        V = self.I.get_average_voltage('CH4')
        I = self.I.get_average_voltage('CH1') / 441
        self.VLabel.setText('V = %0.2fV' % V)
        self.ILabel.setText('I = %0.2fmA' % (I * 1000.0))
        self.X.append(V)
        self.Y.append(I)
        self.progress.setValue(round(self.Vval * 100 / 1.5))
        self.Vval += 0.005
        self.trace.setData(self.X, self.Y)
        if self.Vval > 1.5:
            Z = [
             20 - 20.0 * self.num / 50 - 10] * len(self.X)
            Exp.draw3dLine(self.plot3d, Z, np.array(self.X) * self.scaleX + self.offX, np.array(self.Y) * self.scaleY + self.offY, (0,
                                                                                                                                    100,
                                                                                                                                    255))
            self.X = []
            self.Y = []
            self.Vval = 0
            self.num += 1
        if self.num == 50:
            self.looptimer.stop()


if __name__ == '__main__':
    Exp = experiment.Experiment(parent=None, showresult=False)
    handler = Handler(Exp)
    Exp.addHandler(handler)
    Exp.run()