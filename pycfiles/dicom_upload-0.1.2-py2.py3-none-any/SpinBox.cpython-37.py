# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/SpinBox.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 20602 bytes
from ..Qt import QtGui, QtCore
from ..python2_3 import asUnicode
from ..SignalProxy import SignalProxy
from .. import functions as fn
from math import log
from decimal import Decimal as D
from decimal import *
import weakref
__all__ = [
 'SpinBox']

class SpinBox(QtGui.QAbstractSpinBox):
    """SpinBox"""
    valueChanged = QtCore.Signal(object)
    sigValueChanged = QtCore.Signal(object)
    sigValueChanging = QtCore.Signal(object, object)

    def __init__(self, parent=None, value=0.0, **kwargs):
        """
        ============== ========================================================================
        **Arguments:**
        parent         Sets the parent widget for this SpinBox (optional). Default is None.
        value          (float/int) initial value. Default is 0.0.
        bounds         (min,max) Minimum and maximum values allowed in the SpinBox. 
                       Either may be None to leave the value unbounded. By default, values are unbounded.
        suffix         (str) suffix (units) to display after the numerical value. By default, suffix is an empty str.
        siPrefix       (bool) If True, then an SI prefix is automatically prepended
                       to the units and the value is scaled accordingly. For example,
                       if value=0.003 and suffix='V', then the SpinBox will display
                       "300 mV" (but a call to SpinBox.value will still return 0.003). Default is False.
        step           (float) The size of a single step. This is used when clicking the up/
                       down arrows, when rolling the mouse wheel, or when pressing 
                       keyboard arrows while the widget has keyboard focus. Note that
                       the interpretation of this value is different when specifying
                       the 'dec' argument. Default is 0.01.
        dec            (bool) If True, then the step value will be adjusted to match 
                       the current size of the variable (for example, a value of 15
                       might step in increments of 1 whereas a value of 1500 would
                       step in increments of 100). In this case, the 'step' argument
                       is interpreted *relative* to the current value. The most common
                       'step' values when dec=True are 0.1, 0.2, 0.5, and 1.0. Default is False.
        minStep        (float) When dec=True, this specifies the minimum allowable step size.
        int            (bool) if True, the value is forced to integer type. Default is False
        decimals       (int) Number of decimal values to display. Default is 2. 
        ============== ========================================================================
        """
        QtGui.QAbstractSpinBox.__init__(self, parent)
        self.lastValEmitted = None
        self.lastText = ''
        self.textValid = True
        self.setMinimumWidth(0)
        self.setMaximumHeight(20)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.opts = {'bounds':[
          None, None], 
         'step':D('0.01'), 
         'log':False, 
         'dec':False, 
         'int':False, 
         'suffix':'', 
         'siPrefix':False, 
         'delay':0.3, 
         'delayUntilEditFinished':True, 
         'decimals':2}
        self.decOpts = [
         'step', 'minStep']
        self.val = D(asUnicode(value))
        self.updateText()
        self.skipValidate = False
        self.setCorrectionMode(self.CorrectToPreviousValue)
        self.setKeyboardTracking(False)
        (self.setOpts)(**kwargs)
        self.editingFinished.connect(self.editingFinishedEvent)
        self.proxy = SignalProxy((self.sigValueChanging), slot=(self.delayedChange), delay=(self.opts['delay']))

    def event(self, ev):
        ret = QtGui.QAbstractSpinBox.event(self, ev)
        if ev.type() == QtCore.QEvent.KeyPress:
            if ev.key() == QtCore.Qt.Key_Return:
                ret = True
        return ret

    def setOpts(self, **opts):
        """
        Changes the behavior of the SpinBox. Accepts most of the arguments 
        allowed in :func:`__init__ <pyqtgraph.SpinBox.__init__>`.
        
        """
        for k in opts:
            if k == 'bounds':
                self.setMinimum((opts[k][0]), update=False)
                self.setMaximum((opts[k][1]), update=False)
            elif k in ('step', 'minStep'):
                self.opts[k] = D(asUnicode(opts[k]))
            else:
                if k == 'value':
                    continue
                self.opts[k] = opts[k]

        if 'value' in opts:
            self.setValue(opts['value'])
        elif 'bounds' in opts:
            if 'value' not in opts:
                self.setValue()
        elif self.opts['int']:
            if 'step' in opts:
                step = opts['step']
            else:
                self.opts['step'] = int(self.opts['step'])
            if 'minStep' in opts:
                step = opts['minStep']
                if int(step) != step:
                    raise Exception('Integer SpinBox must have integer minStep size.')
            else:
                ms = int(self.opts.get('minStep', 1))
                if ms < 1:
                    ms = 1
            self.opts['minStep'] = ms
        if 'delay' in opts:
            self.proxy.setDelay(opts['delay'])
        self.updateText()

    def setMaximum(self, m, update=True):
        """Set the maximum allowed value (or None for no limit)"""
        if m is not None:
            m = D(asUnicode(m))
        self.opts['bounds'][1] = m
        if update:
            self.setValue()

    def setMinimum(self, m, update=True):
        """Set the minimum allowed value (or None for no limit)"""
        if m is not None:
            m = D(asUnicode(m))
        self.opts['bounds'][0] = m
        if update:
            self.setValue()

    def setPrefix(self, p):
        self.setOpts(prefix=p)

    def setRange(self, r0, r1):
        self.setOpts(bounds=[r0, r1])

    def setProperty(self, prop, val):
        if prop == 'value':
            self.setValue(val)
        else:
            print("Warning: SpinBox.setProperty('%s', ..) not supported." % prop)

    def setSuffix(self, suf):
        self.setOpts(suffix=suf)

    def setSingleStep(self, step):
        self.setOpts(step=step)

    def setDecimals(self, decimals):
        self.setOpts(decimals=decimals)

    def selectNumber(self):
        """
        Select the numerical portion of the text to allow quick editing by the user.
        """
        le = self.lineEdit()
        text = asUnicode(le.text())
        if self.opts['suffix'] == '':
            le.setSelection(0, len(text))
        else:
            try:
                index = text.index(' ')
            except ValueError:
                return
            else:
                le.setSelection(0, index)

    def value(self):
        """
        Return the value of this SpinBox.
        
        """
        if self.opts['int']:
            return int(self.val)
        return float(self.val)

    def setValue(self, value=None, update=True, delaySignal=False):
        """
        Set the value of this spin. 
        If the value is out of bounds, it will be clipped to the nearest boundary.
        If the spin is integer type, the value will be coerced to int.
        Returns the actual value set.
        
        If value is None, then the current value is used (this is for resetting
        the value after bounds, etc. have changed)
        """
        if value is None:
            value = self.value()
        else:
            bounds = self.opts['bounds']
            if bounds[0] is not None:
                if value < bounds[0]:
                    value = bounds[0]
            if bounds[1] is not None:
                if value > bounds[1]:
                    value = bounds[1]
            if self.opts['int']:
                value = int(value)
            value = D(asUnicode(value))
            if value == self.val:
                return
            prev = self.val
            self.val = value
            if update:
                self.updateText(prev=prev)
            self.sigValueChanging.emit(self, float(self.val))
            delaySignal or self.emitChanged()
        return value

    def emitChanged(self):
        self.lastValEmitted = self.val
        self.valueChanged.emit(float(self.val))
        self.sigValueChanged.emit(self)

    def delayedChange(self):
        try:
            if self.val != self.lastValEmitted:
                self.emitChanged()
        except RuntimeError:
            pass

    def widgetGroupInterface(self):
        return (
         self.valueChanged, SpinBox.value, SpinBox.setValue)

    def sizeHint(self):
        return QtCore.QSize(120, 0)

    def stepEnabled(self):
        return self.StepUpEnabled | self.StepDownEnabled

    def stepBy(self, n):
        n = D(int(n))
        s = [D(-1), D(1)][(n >= 0)]
        val = self.val
        for i in range(int(abs(n))):
            if self.opts['log']:
                raise Exception('Log mode no longer supported.')
            elif self.opts['dec']:
                if val == 0:
                    step = self.opts['minStep']
                    exp = None
                else:
                    vs = [
                     D(-1), D(1)][(val >= 0)]
                    fudge = D('1.01') ** (s * vs)
                    exp = abs(val * fudge).log10().quantize(1, ROUND_FLOOR)
                    step = self.opts['step'] * D(10) ** exp
                if 'minStep' in self.opts:
                    step = max(step, self.opts['minStep'])
                val += s * step
            else:
                val += s * self.opts['step']
            if 'minStep' in self.opts and abs(val) < self.opts['minStep']:
                val = D(0)

        self.setValue(val, delaySignal=True)

    def valueInRange(self, value):
        bounds = self.opts['bounds']
        if bounds[0] is not None:
            if value < bounds[0]:
                return False
        if bounds[1] is not None:
            if value > bounds[1]:
                return False
        if self.opts.get('int', False):
            if int(value) != value:
                return False
        return True

    def updateText(self, prev=None):
        self.skipValidate = True
        if self.opts['siPrefix']:
            if self.val == 0 and prev is not None:
                s, p = fn.siScale(prev)
                txt = '0.0 %s%s' % (p, self.opts['suffix'])
            else:
                txt = fn.siFormat((float(self.val)), suffix=(self.opts['suffix']))
        else:
            txt = '%g%s' % (self.val, self.opts['suffix'])
        self.lineEdit().setText(txt)
        self.lastText = txt
        self.skipValidate = False

    def validate(self, strn, pos):
        if self.skipValidate:
            ret = QtGui.QValidator.Acceptable
        else:
            try:
                suff = self.opts.get('suffix', '')
                if len(suff) > 0 and asUnicode(strn)[-len(suff):] != suff:
                    ret = QtGui.QValidator.Invalid
                else:
                    val = self.interpret()
                    if val is False:
                        ret = QtGui.QValidator.Intermediate
                    elif self.valueInRange(val):
                        if not self.opts['delayUntilEditFinished']:
                            self.setValue(val, update=False)
                        ret = QtGui.QValidator.Acceptable
                    else:
                        ret = QtGui.QValidator.Intermediate
            except:
                ret = QtGui.QValidator.Intermediate

        if ret == QtGui.QValidator.Intermediate:
            self.textValid = False
        elif ret == QtGui.QValidator.Acceptable:
            self.textValid = True
        self.update()
        if hasattr(QtCore, 'QString'):
            return (ret, pos)
        return (
         ret, strn, pos)

    def paintEvent(self, ev):
        QtGui.QAbstractSpinBox.paintEvent(self, ev)
        if not self.textValid:
            p = QtGui.QPainter(self)
            p.setRenderHint(p.Antialiasing)
            p.setPen(fn.mkPen((200, 50, 50), width=2))
            p.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 4, 4)
            p.end()

    def interpret(self):
        """Return value of text. Return False if text is invalid, raise exception if text is intermediate"""
        strn = self.lineEdit().text()
        suf = self.opts['suffix']
        if len(suf) > 0:
            if strn[-len(suf):] != suf:
                return False
            strn = strn[:-len(suf)]
        try:
            val = fn.siEval(strn)
        except:
            return False
            return val

    def editingFinishedEvent(self):
        """Edit has finished; set value."""
        if asUnicode(self.lineEdit().text()) == self.lastText:
            return
        try:
            val = self.interpret()
        except:
            return
        else:
            if val is False:
                return
            if val == self.val:
                return
            self.setValue(val, delaySignal=False)