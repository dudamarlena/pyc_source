# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\spacegroups.py
# Compiled at: 2018-08-27 17:21:06
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from PySide import QtCore, QtGui
import pyqtgraph as pg, spacegrp_peaks, numpy as np
from xicam import config
import msg
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


class vector(QtGui.QWidget):
    sigValueChanged = QtCore.Signal()
    sigChanged = sigValueChanged

    def __init__(self):
        super(vector, self).__init__()
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName(_fromUtf8('horizontalLayout'))
        self.UnitCellVec1LeftParenthesis3D = QtGui.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.UnitCellVec1LeftParenthesis3D.setFont(font)
        self.UnitCellVec1LeftParenthesis3D.setObjectName(_fromUtf8('UnitCellVec1LeftParenthesis3D'))
        self.horizontalLayout.addWidget(self.UnitCellVec1LeftParenthesis3D)
        self.value1 = QtGui.QDoubleSpinBox(self)
        self.value1.setDecimals(1)
        self.value1.setMinimum(-1000.0)
        self.value1.setMaximum(1000.0)
        self.value1.setSingleStep(0.5)
        self.value1.setProperty('value', 0.0)
        self.value1.setObjectName(_fromUtf8('value1'))
        self.horizontalLayout.addWidget(self.value1)
        self.UnitCellVec1Comma1 = QtGui.QLabel(self)
        self.UnitCellVec1Comma1.setObjectName(_fromUtf8('UnitCellVec1Comma1'))
        self.horizontalLayout.addWidget(self.UnitCellVec1Comma1)
        self.value2 = QtGui.QDoubleSpinBox(self)
        self.value2.setDecimals(1)
        self.value2.setMinimum(-1000.0)
        self.value2.setMaximum(1000.0)
        self.value2.setSingleStep(0.5)
        self.value2.setObjectName(_fromUtf8('value2'))
        self.horizontalLayout.addWidget(self.value2)
        self.UnitCellVec1Comma2 = QtGui.QLabel(self)
        self.UnitCellVec1Comma2.setObjectName(_fromUtf8('UnitCellVec1Comma2'))
        self.horizontalLayout.addWidget(self.UnitCellVec1Comma2)
        self.value3 = QtGui.QDoubleSpinBox(self)
        self.value3.setDecimals(1)
        self.value3.setMinimum(-1000.0)
        self.value3.setMaximum(1000.0)
        self.value3.setSingleStep(0.5)
        self.value3.setObjectName(_fromUtf8('value3'))
        self.horizontalLayout.addWidget(self.value3)
        self.UnitCellVec1RightParenthesis3D = QtGui.QLabel(self)
        self.UnitCellVec1RightParenthesis3D.setFont(font)
        self.UnitCellVec1RightParenthesis3D.setObjectName(_fromUtf8('UnitCellVec1RightParenthesis3D'))
        self.horizontalLayout.addWidget(self.UnitCellVec1RightParenthesis3D)
        self.UnitCellVec1LeftParenthesis3D.setText('(')
        self.UnitCellVec1Comma1.setText(',')
        self.UnitCellVec1Comma2.setText(',')
        self.UnitCellVec1RightParenthesis3D.setText(')')
        self.value1.valueChanged.connect(self.sigValueChanged)
        self.value2.valueChanged.connect(self.sigValueChanged)
        self.value3.valueChanged.connect(self.sigValueChanged)

    def value(self):
        return (
         self.value1.value(), self.value2.value(), self.value3.value())

    def setValue(self, v):
        self.value1.setValue(v[0])
        self.value2.setValue(v[1])
        self.value3.setValue(v[2])

    def setEnabled(self, enabled):
        self.value1.setEnabled(enabled)
        self.value2.setEnabled(enabled)
        self.value3.setEnabled(enabled)


class VectorParameterItem(pTypes.WidgetParameterItem):

    def makeWidget(self):
        w = vector()
        opts = self.param.opts
        value = opts.get('value', None)
        if value is not None:
            w.setValue(value)
        self.value = w.value
        self.setValue = w.setValue
        return w

    def valueChanged(self, *args, **kwargs):
        super(VectorParameterItem, self).valueChanged(*args, **kwargs)


class VectorParameter(Parameter):
    itemClass = VectorParameterItem

    def __init__(self, *args, **kwargs):
        super(VectorParameter, self).__init__(*args, **kwargs)

    def defaultValue(self):
        return (0, 0, 0)


class peakoverlay(pg.ScatterPlotItem):

    def __init__(self, peaks):
        self.peaks = peaks
        self.centerx = 0
        self.centery = 0
        if len(peaks):
            x, y = zip(*[ [p.x, p.y] for p in peaks ])
            symbols = [ 's' if p.mode == 'Transmission' else 'o' for p in peaks ]
            colors = [ pg.mkPen(0, 255, 0, 255) if p.mode == 'Transmission' else pg.mkPen(255, 0, 255, 255) for p in peaks ]
            super(peakoverlay, self).__init__(x, y, size=10, brush=None, pen=colors, symbol=symbols)
            self.display_text = pg.TextItem(text='', color=(255, 255, 255), anchor=(0,
                                                                                    1), fill=pg.mkBrush(255, 127, 0, 100))
            self.display_text.hide()
        return

    def setCenter(self, x, y):
        self.centerx = x
        self.centery = y
        self.displayRelative()

    def displayRelative(self):
        px, py = zip(*[ [p.x, p.y] for p in self.peaks ])
        symbols = [ 's' if p.mode == 'Transmission' else 'o' for p in self.peaks ]
        colors = [ pg.mkPen(0, 255, 0, 255) if p.mode == 'Transmission' else pg.mkPen(255, 0, 255, 255) for p in self.peaks ]
        self.setData(x=np.array(px) + self.centerx, y=np.array(py) + self.centery, size=10, brush=None, pen=colors, symbol=symbols)
        return

    def enable(self, parent):
        self.scene().sigMouseMoved.connect(self.onMove)
        parent.addItem(self.display_text)

    def peaksAtRelative(self, pos):
        x = pos.x() - self.centerx
        y = pos.y() - self.centery
        pw = self.pixelWidth()
        ph = self.pixelHeight()
        peaks = []
        ss = self.points()[0].size()
        for p in self.peaks:
            sx, sy = p.pos()
            s2x = s2y = ss * 0.5
            if self.opts['pxMode']:
                s2x *= pw
                s2y *= ph
            if x > sx - s2x and x < sx + s2x and y > sy - s2y and y < sy + s2y:
                peaks.append(p)

        return peaks[::-1]

    def onMove(self, pos):
        pos = self.mapFromScene(pos)
        peaks = self.peaksAtRelative(pos)
        if len(peaks) != 0:
            s = ''
            for peak in peaks:
                if s != '':
                    s += '\n\n'
                s += unicode(peak)

            self.display_text.setText(s)
            self.display_text.setPos(pos)
            self.display_text.show()
            msg.logMessage(s)
        else:
            self.display_text.hide()
        if len(peaks) > 6:
            self.display_text.setText('Too many points under cursor.\nZoom in or check Log info.')
            self.display_text.setPos(pos)
            self.display_text.show()


class spacegroupwidget(ParameterTree):
    sigDrawSGOverlay = QtCore.Signal(peakoverlay)

    def __init__(self):
        super(spacegroupwidget, self).__init__()
        self.parameter = pTypes.GroupParameter(name='')
        self.setParameters(self.parameter, showTop=False)
        self.crystalsystem = pTypes.ListParameter(type='list', name='Crystal System', values=spacegrouptypes, value=None)
        self.spacegroupparameter = pTypes.ListParameter(type='list', name='Space Group', values=spacegroupnames[0], value=None)
        self.rotationstyle = pTypes.ListParameter(type='list', name='Rotation Mode', values=[
         'Sample-frame vector', 'Crystal-frame vector',
         'Crystal plane'])
        self.rotationstyle.sigValueChanged.connect(self.rotationmodechanged)
        self.rotationxyz = VectorParameter(name='Vector (x,y,z)')
        self.rotationvectorsample = hideableGroup(name='Rotation (sample-frame vector)', children=[self.rotationxyz])
        self.rotationxyz.setValue([0, 0, 1])
        self.rotationuvw = VectorParameter(name='Vector (u,v,w)')
        self.rotationvectorcrystal = hideableGroup(name='Rotation (crystal-frame vector)', children=[self.rotationuvw])
        self.rotationuvw.setValue([0, 0, 1])
        self.rotationhkl = VectorParameter(name='Vector (h,k,l)')
        self.rotationplane = hideableGroup(name='Rotation (crystal plane)', children=[self.rotationhkl])
        self.rotationhkl.setValue([0, 0, 1])
        self.spacegroupeditors = [
         triclinicparameter(), monoclinicparameter(), orthorhombicparameter(),
         tetragonalparameter(), trigonalparameter(), hexagonalparameter(), cubicparameter()]
        self.rotations = [self.rotationvectorsample, self.rotationvectorcrystal, self.rotationplane]
        self.delta = pTypes.SimpleParameter(name='δ', type='float', value=2.67150153e-06)
        self.beta = pTypes.SimpleParameter(name='β', type='float', value=3.71373554e-09)
        self.refractiveindex = pTypes.GroupParameter(name='Refractive Index', children=[self.delta, self.beta])
        self.redrawsg = pTypes.ActionParameter(name='Overlay space group')
        self.redrawsg.sigActivated.connect(self.drawoverlay)
        self.parameter.addChildren([
         self.crystalsystem, self.spacegroupparameter] + self.spacegroupeditors + [self.rotationstyle] + self.rotations + [self.refractiveindex, self.redrawsg])
        self.hidechildren()
        self.hiderotations()
        self.parameter.children()[2].show()
        self.rotations[0].show()
        self.crystalsystem.sigValueChanged.connect(self.crystalsystemchanged)
        return

    def activelatticetype(self):
        return self.spacegroupeditors[self.crystalsystem.reverse[0].index(self.crystalsystem.value())]

    def _getRotationVector(self):
        return [
         self.rotationxyz, self.rotationuvw, self.rotationhkl][self._getRotationType()].value()

    def _getRotationType(self):
        return self.rotationstyle.reverse[0].index(self.rotationstyle.value())

    def drawoverlay(self):
        activelatticetype = self.activelatticetype()
        SG = self.spacegroupparameter.value()
        refbeta = self.beta.value()
        refdelta = self.delta.value()
        peaks = spacegrp_peaks.find_peaks(float(activelatticetype.a.value()), float(activelatticetype.b.value()), float(activelatticetype.c.value()), activelatticetype.alpha.value(), activelatticetype.beta.value(), activelatticetype.gamma.value(), normal=self._getRotationVector(), norm_type=['xyz', 'hkl', 'uvw'][self._getRotationType()], refdelta=refdelta, refbeta=refbeta, order=5, unitcell=None, space_grp=SG)
        for peak in peaks:
            msg.logMessage(unicode(peak), msg.DEBUG)
            center = config.activeExperiment.center
            sdd = config.activeExperiment.getvalue('Detector Distance')
            pixelsize = config.activeExperiment.getvalue('Pixel Size X')
            peak.position(center, sdd, pixelsize)

        self.sigDrawSGOverlay.emit(peakoverlay(peaks))
        return

    def hidechildren(self):
        for child in self.spacegroupeditors:
            child.hide()

    def hiderotations(self):
        for child in self.rotations:
            child.hide()

    def rotationmodechanged(self, _, value):
        self.hiderotations()
        self.rotations[self.rotationstyle.reverse[0].index(value)].show()

    def crystalsystemchanged(self, _, value):
        self.hidechildren()
        self.parameter.param(value).show()
        self.spacegroupparameter.setLimits(spacegroupnames[spacegrouptypes.index(value)])


class hideableGroupParameterItem(pTypes.GroupParameterItem):

    def optsChanged(self, param, opts):
        super(hideableGroupParameterItem, self).optsChanged(param, opts)
        if 'visible' in opts:
            self.setHidden(not opts['visible'])


class hideableGroup(pTypes.GroupParameter):
    itemClass = hideableGroupParameterItem


class spacegroup(hideableGroup):
    crystalsystem = None

    def __init__(self, name):
        super(spacegroup, self).__init__(name=name)
        self.alpha = pTypes.SimpleParameter(type='float', name='α', value=90, step=0.01)
        self.beta = pTypes.SimpleParameter(type='float', name='β', value=90, step=0.01)
        self.gamma = pTypes.SimpleParameter(type='float', name='γ', value=90, step=0.01)
        self.a = pTypes.SimpleParameter(type='float', name='a', value=1e-08, step=1e-09, suffix='m', siPrefix=True)
        self.b = pTypes.SimpleParameter(type='float', name='b', value=1e-08, step=1e-09, suffix='m', siPrefix=True)
        self.c = pTypes.SimpleParameter(type='float', name='c', value=1e-08, step=1e-09, suffix='m', siPrefix=True)
        self.addChildren([self.alpha, self.beta, self.gamma, self.a, self.b, self.c])

    def _setb(self, _, value):
        self.b.setValue(value, blockSignal=self.b.sigValueChanged)

    def _setc(self, _, value):
        self.c.setValue(value, blockSignal=self.c.sigValueChanged)


class triclinicparameter(spacegroup):
    crystalsystem = 'Triclinic'

    def __init__(self):
        super(triclinicparameter, self).__init__(name=self.crystalsystem)


class monoclinicparameter(spacegroup):
    crystalsystem = 'Monoclinic'

    def __init__(self):
        super(monoclinicparameter, self).__init__(name=self.crystalsystem)
        self.alpha.setValue(90)
        self.gamma.setValue(90)
        self.alpha.setReadonly(True)
        self.gamma.setReadonly(True)


class orthorhombicparameter(spacegroup):
    crystalsystem = 'Orthorhombic'

    def __init__(self):
        super(orthorhombicparameter, self).__init__(name=self.crystalsystem)
        self.alpha.setValue(90)
        self.beta.setValue(90)
        self.gamma.setValue(90)
        self.alpha.setReadonly(True)
        self.beta.setReadonly(True)
        self.gamma.setReadonly(True)


class tetragonalparameter(spacegroup):
    crystalsystem = 'Tetragonal'

    def __init__(self):
        super(tetragonalparameter, self).__init__(name=self.crystalsystem)
        self.alpha.setValue(90)
        self.beta.setValue(90)
        self.gamma.setValue(90)
        self.alpha.setReadonly(True)
        self.beta.setReadonly(True)
        self.gamma.setReadonly(True)
        self.b.setReadonly(True)
        self.a.sigValueChanged.connect(self._setb)


class trigonalparameter(spacegroup):
    crystalsystem = 'Trigonal'

    def __init__(self):
        super(trigonalparameter, self).__init__(name=self.crystalsystem)
        self.alpha.setValue(90)
        self.beta.setValue(90)
        self.gamma.setValue(120)
        self.alpha.setReadonly(True)
        self.beta.setReadonly(True)
        self.gamma.setReadonly(True)
        self.b.setReadonly(True)
        self.a.sigValueChanged.connect(self._setb)


class hexagonalparameter(spacegroup):
    crystalsystem = 'Hexagonal'

    def __init__(self):
        super(hexagonalparameter, self).__init__(name=self.crystalsystem)
        self.alpha.setValue(90)
        self.beta.setValue(90)
        self.gamma.setValue(120)
        self.gamma.setReadonly(True)
        self.b.setReadonly(True)
        self.a.sigValueChanged.connect(self._setb)


class cubicparameter(spacegroup):
    crystalsystem = 'Cubic'

    def __init__(self):
        super(cubicparameter, self).__init__(name=self.crystalsystem)
        self.alpha.setValue(90)
        self.beta.setValue(90)
        self.gamma.setValue(90)
        self.alpha.setReadonly(True)
        self.beta.setReadonly(True)
        self.gamma.setReadonly(True)
        self.b.setReadonly(True)
        self.c.setReadonly(True)
        self.a.sigValueChanged.connect(self._setb)
        self.a.sigValueChanged.connect(self._setc)


triclinicspacegroupnames = [
 'P1', 'P-1']
monoclinicspacegroupnames = ['P2', 'P2₁', 'Pm', 'Pc', 'Cm', 'Cc', 'P2/m', 'P2₁/m', 'C2/m', 'P2/c', 'P2₁/c', 'C2/c']
orhorhombicspacegroupnames = ['P222', 'P222₁', 'P2₁2₁2', 'P2₁2₁2₁', 'C222₁', 'C222', 'F222', 'I222', 'I2₁2₁2₁',
 'Pmm2', 'Pmc2₁',
 'Pcc2', 'Pma2', 'Pca2₁', 'Pnc2', 'Pmn2₁', 'Pba2', 'Pna2₁', 'Pnn2', 'Cmm2', 'Cmc2₁',
 'Ccc2', 'Amm2',
 'Aem2', 'Ama2', 'Aea2', 'Fmm2', 'Fdd2', 'Imm2', 'Iba2', 'Ima2', 'Pmmm', 'Pnnn', 'Pccm',
 'Pban', 'Pmma',
 'Pnna', 'Pmna', 'Pcca', 'Pbam', 'Pccn', 'Pbcm', 'Pnnm', 'Pmmn', 'Pbcn', 'Pbca', 'Pnma',
 'Cmcm', 'Cmce',
 'Cmmm', 'Cccm', 'Cmme', 'Ccce', 'Fmmm', 'Fddd', 'Immm', 'Ibam', 'Ibca', 'Imma']
tetragonalspacegroupnames = ['P4', 'P4₁', 'P4₂', 'P4₃', 'I4', 'I4₁', 'P-4', 'I-4', 'P4/m', 'P4₂/m', 'P4/n',
 'P4₂/n', 'I4/m', 'I4₁/a',
 'P422', 'P42₁2', 'P4₁22', 'P4₁2₁2', 'P4₂22', 'P4₂2₁2', 'P4₃22', 'P4₃2₁2', 'I422',
 'I4₁22', 'P4mm',
 'P4bm', 'P4₂cm', 'P4₂nm', 'P4cc', 'P4nc', 'P4₂mc', 'P4₂bc', 'I4mm', 'I4cm', 'I4₁md',
 'I4₁cd', 'P-42m',
 'P-42c', 'P-42₁m', 'P-42₁c', 'P-4m2', 'P-4c2', 'P-4b2', 'P-4n2', 'I-4m2', 'I-4c2', 'I-42m',
 'I-42d',
 'P4/mmm', 'P4/mcc', 'P4/nbm', 'P4/nnc', 'P4/mbm', 'P4/mnc', 'P4/nmm', 'P4/ncc', 'P4₂/mmc',
 'P4₂/mcm',
 'P4₂/nbc', 'P4₂/nnm', 'P4₂/mbc', 'P4₂/mnm', 'P4₂/nmc', 'P4₂/ncm', 'I4/mmm', 'I4/mcm',
 'I4₁/amd',
 'I4₁/acd']
trigonalspacegroupnames = ['P3', 'P3₁', 'P3₂', 'R3', 'P-3', 'R-3', 'P312', 'P321', 'P3₁12', 'P3₁21', 'P3₂12',
 'P3₂21', 'R32', 'P3m1',
 'P31m', 'P3c1', 'P31c', 'R3m', 'R3c', 'P-31m', 'P-31c', 'P-3m1', 'P-3c1', 'R-3m', 'R-3c']
hexagonalspacegroupnames = ['P6', 'P6₁', 'P6₅', 'P6₂', 'P6₄', 'P6₃', 'P-6', 'P6/m', 'P6₃/m', 'P622', 'P6₁22',
 'P6₅22', 'P6₂22',
 'P6₄22', 'P6₃22', 'P6mm', 'P6cc', 'P6₃cm', 'P6₃mc', 'P-6m2', 'P-6c2', 'P-62m', 'P-62c',
 'P6/mmm',
 'P6/mcc', 'P6₃/mcm', 'P6₃/mmc']
cubicspacegroupnames = ['P23', 'F23', 'I23', 'P2₁3', 'I2₁3', 'Pm-3', 'Pn-3', 'Fm-3', 'Fd-3', 'Im-3', 'Pa-3', 'Ia-3',
 'P432', 'P4₂32',
 'F432', 'F4₁32', 'I432', 'P4₃32', 'P4₁32', 'I4₁32', 'P-43m', 'F-43m', 'I-43m', 'P-43n',
 'F-43c', 'I-43d',
 'Pm-3m', 'Pn-3n', 'Pm-3n', 'Pn-3m', 'Fm-3m', 'Fm-3c', 'Fd-3m', 'Fd-3c', 'Im-3m', 'Ia-3d']
import sgexclusions
spacegroupnames = [sgexclusions.Triclinic.conditions.keys(), sgexclusions.Monoclinic.conditions.keys(), sgexclusions.Orthorhombic.conditions.keys(),
 sgexclusions.Tetragonal.conditions.keys(), sgexclusions.Trigonal.conditions.keys(), sgexclusions.Hexagonal.conditions.keys(), sgexclusions.Cubic.conditions.keys()]
spacegrouptypes = ['Triclinic', 'Monoclinic', 'Orthorhombic', 'Tetragonal', 'Trigonal', 'Hexagonal', 'Cubic']