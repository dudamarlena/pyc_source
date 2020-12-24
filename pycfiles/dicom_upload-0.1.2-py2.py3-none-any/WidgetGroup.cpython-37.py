# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/WidgetGroup.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 10002 bytes
__doc__ = '\nWidgetGroup.py -  WidgetGroup class for easily managing lots of Qt widgets\nCopyright 2010  Luke Campagnola\nDistributed under MIT/X11 license. See license.txt for more infomation.\n\nThis class addresses the problem of having to save and restore the state\nof a large group of widgets. \n'
from .Qt import QtCore, QtGui, USE_PYQT5
import weakref, inspect
from .python2_3 import asUnicode
__all__ = [
 'WidgetGroup']

def splitterState(w):
    s = str(w.saveState().toPercentEncoding())
    return s


def restoreSplitter(w, s):
    if type(s) is list:
        w.setSizes(s)
    elif type(s) is str:
        w.restoreState(QtCore.QByteArray.fromPercentEncoding(s))
    else:
        print("Can't configure QSplitter using object of type", type(s))
    if w.count() > 0:
        for i in w.sizes():
            if i > 0:
                return

        w.setSizes([50] * w.count())


def comboState(w):
    ind = w.currentIndex()
    data = w.itemData(ind)
    if data is not None:
        try:
            if not data.isValid():
                data = None
            else:
                data = data.toInt()[0]
        except AttributeError:
            pass

    if data is None:
        return asUnicode(w.itemText(ind))
    return data


def setComboState(w, v):
    if type(v) is int:
        ind = w.findData(v)
        if ind > -1:
            w.setCurrentIndex(ind)
            return
    w.setCurrentIndex(w.findText(str(v)))


class WidgetGroup(QtCore.QObject):
    """WidgetGroup"""
    classes = {QtGui.QSpinBox: (
                      lambda w: w.valueChanged,
                      QtGui.QSpinBox.value,
                      QtGui.QSpinBox.setValue), 
     
     QtGui.QDoubleSpinBox: (
                            lambda w: w.valueChanged,
                            QtGui.QDoubleSpinBox.value,
                            QtGui.QDoubleSpinBox.setValue), 
     
     QtGui.QSplitter: (
                       None,
                       splitterState,
                       restoreSplitter,
                       True), 
     
     QtGui.QCheckBox: (
                       lambda w: w.stateChanged,
                       QtGui.QCheckBox.isChecked,
                       QtGui.QCheckBox.setChecked), 
     
     QtGui.QComboBox: (
                       lambda w: w.currentIndexChanged,
                       comboState,
                       setComboState), 
     
     QtGui.QGroupBox: (
                       lambda w: w.toggled,
                       QtGui.QGroupBox.isChecked,
                       QtGui.QGroupBox.setChecked,
                       True), 
     
     QtGui.QLineEdit: (
                       lambda w: w.editingFinished,
                       lambda w: str(w.text()),
                       QtGui.QLineEdit.setText), 
     
     QtGui.QRadioButton: (
                          lambda w: w.toggled,
                          QtGui.QRadioButton.isChecked,
                          QtGui.QRadioButton.setChecked), 
     
     QtGui.QSlider: (
                     lambda w: w.valueChanged,
                     QtGui.QSlider.value,
                     QtGui.QSlider.setValue)}
    sigChanged = QtCore.Signal(str, object)

    def __init__(self, widgetList=None):
        """Initialize WidgetGroup, adding specified widgets into this group.
        widgetList can be: 
         - a list of widget specifications (widget, [name], [scale])
         - a dict of name: widget pairs
         - any QObject, and all compatible child widgets will be added recursively.
        
        The 'scale' parameter for each widget allows QSpinBox to display a different value than the value recorded
        in the group state (for example, the program may set a spin box value to 100e-6 and have it displayed as 100 to the user)
        """
        QtCore.QObject.__init__(self)
        self.widgetList = weakref.WeakKeyDictionary()
        self.scales = weakref.WeakKeyDictionary()
        self.cache = {}
        self.uncachedWidgets = weakref.WeakKeyDictionary()
        if isinstance(widgetList, QtCore.QObject):
            self.autoAdd(widgetList)
        elif isinstance(widgetList, list):
            for w in widgetList:
                (self.addWidget)(*w)

        elif isinstance(widgetList, dict):
            for name, w in widgetList.items():
                self.addWidget(w, name)

        else:
            if widgetList is None:
                return
            raise Exception('Wrong argument type %s' % type(widgetList))

    def addWidget(self, w, name=None, scale=None):
        if not self.acceptsType(w):
            raise Exception('Widget type %s not supported by WidgetGroup' % type(w))
        else:
            if name is None:
                name = str(w.objectName())
            else:
                if name == '':
                    raise Exception("Cannot add widget '%s' without a name." % str(w))
                self.widgetList[w] = name
                self.scales[w] = scale
                self.readWidget(w)
                if type(w) in WidgetGroup.classes:
                    signal = WidgetGroup.classes[type(w)][0]
                else:
                    signal = w.widgetGroupInterface()[0]
            if signal is not None and not inspect.isfunction(signal):
                if inspect.ismethod(signal):
                    signal = signal(w)
                signal.connect(self.mkChangeCallback(w))
            else:
                self.uncachedWidgets[w] = None

    def findWidget(self, name):
        for w in self.widgetList:
            if self.widgetList[w] == name:
                return w

    def interface(self, obj):
        t = type(obj)
        if t in WidgetGroup.classes:
            return WidgetGroup.classes[t]
        return obj.widgetGroupInterface()

    def checkForChildren(self, obj):
        """Return true if we should automatically search the children of this object for more."""
        iface = self.interface(obj)
        return len(iface) > 3 and iface[3]

    def autoAdd(self, obj):
        accepted = self.acceptsType(obj)
        if accepted:
            self.addWidget(obj)
        if not accepted or self.checkForChildren(obj):
            for c in obj.children():
                self.autoAdd(c)

    def acceptsType(self, obj):
        for c in WidgetGroup.classes:
            if isinstance(obj, c):
                return True

        if hasattr(obj, 'widgetGroupInterface'):
            return True
        return False

    def setScale(self, widget, scale):
        val = self.readWidget(widget)
        self.scales[widget] = scale
        self.setWidget(widget, val)

    def mkChangeCallback(self, w):
        return lambda *args: (self.widgetChanged)(w, *args)

    def widgetChanged(self, w, *args):
        n = self.widgetList[w]
        v1 = self.cache[n]
        v2 = self.readWidget(w)
        if v1 != v2:
            if not USE_PYQT5:
                self.emit(QtCore.SIGNAL('changed'), self.widgetList[w], v2)
            self.sigChanged.emit(self.widgetList[w], v2)

    def state(self):
        for w in self.uncachedWidgets:
            self.readWidget(w)

        return self.cache.copy()

    def setState(self, s):
        for w in self.widgetList:
            n = self.widgetList[w]
            if n not in s:
                continue
            self.setWidget(w, s[n])

    def readWidget(self, w):
        if type(w) in WidgetGroup.classes:
            getFunc = WidgetGroup.classes[type(w)][1]
        else:
            getFunc = w.widgetGroupInterface()[1]
        if getFunc is None:
            return
        if inspect.ismethod(getFunc) and getFunc.__self__ is not None:
            val = getFunc()
        else:
            val = getFunc(w)
        if self.scales[w] is not None:
            val /= self.scales[w]
        n = self.widgetList[w]
        self.cache[n] = val
        return val

    def setWidget(self, w, v):
        v1 = v
        if self.scales[w] is not None:
            v *= self.scales[w]
        elif type(w) in WidgetGroup.classes:
            setFunc = WidgetGroup.classes[type(w)][2]
        else:
            setFunc = w.widgetGroupInterface()[2]
        if inspect.ismethod(setFunc) and setFunc.__self__ is not None:
            setFunc(v)
        else:
            setFunc(w, v)