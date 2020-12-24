# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/parametertree/parameterTypes.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 25056 bytes
from ..Qt import QtCore, QtGui
from ..python2_3 import asUnicode
from .Parameter import Parameter, registerParameterType
from .ParameterItem import ParameterItem
import widgets.SpinBox as SpinBox
import widgets.ColorButton as ColorButton
from .. import pixmaps
from .. import functions as fn
import os
from ..pgcollections import OrderedDict

class WidgetParameterItem(ParameterItem):
    __doc__ = '\n    ParameterTree item with:\n    \n    * label in second column for displaying value\n    * simple widget for editing value (displayed instead of label when item is selected)\n    * button that resets value to default\n    \n    ==========================  =============================================================\n    **Registered Types:**\n    int                         Displays a :class:`SpinBox <pyqtgraph.SpinBox>` in integer\n                                mode.\n    float                       Displays a :class:`SpinBox <pyqtgraph.SpinBox>`.\n    bool                        Displays a QCheckBox\n    str                         Displays a QLineEdit\n    color                       Displays a :class:`ColorButton <pyqtgraph.ColorButton>`\n    colormap                    Displays a :class:`GradientWidget <pyqtgraph.GradientWidget>`\n    ==========================  =============================================================\n    \n    This class can be subclassed by overriding makeWidget() to provide a custom widget.\n    '

    def __init__(self, param, depth):
        ParameterItem.__init__(self, param, depth)
        self.hideWidget = True
        w = self.makeWidget()
        self.widget = w
        self.eventProxy = EventProxy(w, self.widgetEventFilter)
        opts = self.param.opts
        if 'tip' in opts:
            w.setToolTip(opts['tip'])
        else:
            self.defaultBtn = QtGui.QPushButton()
            self.defaultBtn.setFixedWidth(20)
            self.defaultBtn.setFixedHeight(20)
            modDir = os.path.dirname(__file__)
            self.defaultBtn.setIcon(QtGui.QIcon(pixmaps.getPixmap('default')))
            self.defaultBtn.clicked.connect(self.defaultClicked)
            self.displayLabel = QtGui.QLabel()
            layout = QtGui.QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(2)
            layout.addWidget(w)
            layout.addWidget(self.displayLabel)
            layout.addWidget(self.defaultBtn)
            self.layoutWidget = QtGui.QWidget()
            self.layoutWidget.setLayout(layout)
            if w.sigChanged is not None:
                w.sigChanged.connect(self.widgetValueChanged)
            if hasattr(w, 'sigChanging'):
                w.sigChanging.connect(self.widgetValueChanging)
            if opts.get('value', None) is not None:
                self.valueChanged(self, (opts['value']), force=True)
            else:
                self.widgetValueChanged()
        self.updateDefaultBtn()

    def makeWidget(self):
        """
        Return a single widget that should be placed in the second tree column.
        The widget must be given three attributes:
        
        ==========  ============================================================
        sigChanged  a signal that is emitted when the widget's value is changed
        value       a function that returns the value
        setValue    a function that sets the value
        ==========  ============================================================
            
        This is a good function to override in subclasses.
        """
        opts = self.param.opts
        t = opts['type']
        if t == 'int':
            defs = {'value':0,  'min':None,  'max':None,  'int':True,  'step':1.0, 
             'minStep':1.0,  'dec':False,  'siPrefix':False, 
             'suffix':''}
            defs.update(opts)
            if 'limits' in opts:
                defs['bounds'] = opts['limits']
            w = SpinBox()
            (w.setOpts)(**defs)
            w.sigChanged = w.sigValueChanged
            w.sigChanging = w.sigValueChanging
        else:
            if t == 'float':
                defs = {'value':0,  'min':None,  'max':None,  'step':1.0, 
                 'dec':False,  'siPrefix':False, 
                 'suffix':''}
                defs.update(opts)
                if 'limits' in opts:
                    defs['bounds'] = opts['limits']
                w = SpinBox()
                (w.setOpts)(**defs)
                w.sigChanged = w.sigValueChanged
                w.sigChanging = w.sigValueChanging
            else:
                if t == 'bool':
                    w = QtGui.QCheckBox()
                    w.sigChanged = w.toggled
                    w.value = w.isChecked
                    w.setValue = w.setChecked
                    w.setEnabled(not opts.get('readonly', False))
                    self.hideWidget = False
                else:
                    if t == 'str':
                        w = QtGui.QLineEdit()
                        w.sigChanged = w.editingFinished
                        w.value = lambda : asUnicode(w.text())
                        w.setValue = lambda v: w.setText(asUnicode(v))
                        w.sigChanging = w.textChanged
                    else:
                        if t == 'color':
                            w = ColorButton()
                            w.sigChanged = w.sigColorChanged
                            w.sigChanging = w.sigColorChanging
                            w.value = w.color
                            w.setValue = w.setColor
                            self.hideWidget = False
                            w.setFlat(True)
                            w.setEnabled(not opts.get('readonly', False))
                        else:
                            if t == 'colormap':
                                import widgets.GradientWidget as GradientWidget
                                w = GradientWidget(orientation='bottom')
                                w.sigChanged = w.sigGradientChangeFinished
                                w.sigChanging = w.sigGradientChanged
                                w.value = w.colorMap
                                w.setValue = w.setColorMap
                                self.hideWidget = False
                            else:
                                raise Exception("Unknown type '%s'" % asUnicode(t))
        return w

    def widgetEventFilter(self, obj, ev):
        if ev.type() == ev.KeyPress:
            if ev.key() == QtCore.Qt.Key_Tab:
                self.focusNext(forward=True)
                return True
            if ev.key() == QtCore.Qt.Key_Backtab:
                self.focusNext(forward=False)
                return True
        return False

    def setFocus(self):
        self.showEditor()

    def isFocusable(self):
        return self.param.writable()

    def valueChanged(self, param, val, force=False):
        ParameterItem.valueChanged(self, param, val)
        self.widget.sigChanged.disconnect(self.widgetValueChanged)
        try:
            if force or val != self.widget.value():
                self.widget.setValue(val)
            self.updateDisplayLabel(val)
        finally:
            self.widget.sigChanged.connect(self.widgetValueChanged)

        self.updateDefaultBtn()

    def updateDefaultBtn(self):
        self.defaultBtn.setEnabled(not self.param.valueIsDefault() and self.param.writable())
        self.defaultBtn.setVisible(not self.param.readonly())

    def updateDisplayLabel(self, value=None):
        """Update the display label to reflect the value of the parameter."""
        if value is None:
            value = self.param.value()
        else:
            opts = self.param.opts
            if isinstance(self.widget, QtGui.QAbstractSpinBox):
                text = asUnicode(self.widget.lineEdit().text())
            else:
                if isinstance(self.widget, QtGui.QComboBox):
                    text = self.widget.currentText()
                else:
                    text = asUnicode(value)
        self.displayLabel.setText(text)

    def widgetValueChanged(self):
        val = self.widget.value()
        newVal = self.param.setValue(val)

    def widgetValueChanging(self, *args):
        """
        Called when the widget's value is changing, but not finalized.
        For example: editing text before pressing enter or changing focus.
        """
        self.param.sigValueChanging.emit(self.param, args[(-1)])

    def selected(self, sel):
        """Called when this item has been selected (sel=True) OR deselected (sel=False)"""
        ParameterItem.selected(self, sel)
        if self.widget is None:
            return
        if sel and self.param.writable():
            self.showEditor()
        else:
            if self.hideWidget:
                self.hideEditor()

    def showEditor(self):
        self.widget.show()
        self.displayLabel.hide()
        self.widget.setFocus(QtCore.Qt.OtherFocusReason)
        if isinstance(self.widget, SpinBox):
            self.widget.selectNumber()

    def hideEditor(self):
        self.widget.hide()
        self.displayLabel.show()

    def limitsChanged(self, param, limits):
        """Called when the parameter's limits have changed"""
        ParameterItem.limitsChanged(self, param, limits)
        t = self.param.opts['type']
        if t == 'int' or t == 'float':
            self.widget.setOpts(bounds=limits)
        else:
            return

    def defaultChanged(self, param, value):
        self.updateDefaultBtn()

    def treeWidgetChanged(self):
        """Called when this item is added or removed from a tree."""
        ParameterItem.treeWidgetChanged(self)
        if self.widget is not None:
            tree = self.treeWidget()
            if tree is None:
                return
            tree.setItemWidget(self, 1, self.layoutWidget)
            self.displayLabel.hide()
            self.selected(False)

    def defaultClicked(self):
        self.param.setToDefault()

    def optsChanged(self, param, opts):
        """Called when any options are changed that are not
        name, value, default, or limits"""
        ParameterItem.optsChanged(self, param, opts)
        if 'readonly' in opts:
            self.updateDefaultBtn()
            if isinstance(self.widget, (QtGui.QCheckBox, ColorButton)):
                self.widget.setEnabled(not opts['readonly'])
        if isinstance(self.widget, SpinBox):
            if 'units' in opts:
                if 'suffix' not in opts:
                    opts['suffix'] = opts['units']
            (self.widget.setOpts)(**opts)
            self.updateDisplayLabel()


class EventProxy(QtCore.QObject):

    def __init__(self, qobj, callback):
        QtCore.QObject.__init__(self)
        self.callback = callback
        qobj.installEventFilter(self)

    def eventFilter(self, obj, ev):
        return self.callback(obj, ev)


class SimpleParameter(Parameter):
    itemClass = WidgetParameterItem

    def __init__(self, *args, **kargs):
        (Parameter.__init__)(self, *args, **kargs)
        if self.opts['type'] == 'color':
            self.value = self.colorValue
            self.saveState = self.saveColorState

    def colorValue(self):
        return fn.mkColor(Parameter.value(self))

    def saveColorState(self, *args, **kwds):
        state = (Parameter.saveState)(self, *args, **kwds)
        state['value'] = fn.colorTuple(self.value())
        return state


registerParameterType('int', SimpleParameter, override=True)
registerParameterType('float', SimpleParameter, override=True)
registerParameterType('bool', SimpleParameter, override=True)
registerParameterType('str', SimpleParameter, override=True)
registerParameterType('color', SimpleParameter, override=True)
registerParameterType('colormap', SimpleParameter, override=True)

class GroupParameterItem(ParameterItem):
    __doc__ = '\n    Group parameters are used mainly as a generic parent item that holds (and groups!) a set\n    of child parameters. It also provides a simple mechanism for displaying a button or combo\n    that can be used to add new parameters to the group.\n    '

    def __init__(self, param, depth):
        ParameterItem.__init__(self, param, depth)
        self.updateDepth(depth)
        self.addItem = None
        if 'addText' in param.opts:
            addText = param.opts['addText']
            if 'addList' in param.opts:
                self.addWidget = QtGui.QComboBox()
                self.addWidget.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
                self.updateAddList()
                self.addWidget.currentIndexChanged.connect(self.addChanged)
            else:
                self.addWidget = QtGui.QPushButton(addText)
                self.addWidget.clicked.connect(self.addClicked)
            w = QtGui.QWidget()
            l = QtGui.QHBoxLayout()
            l.setContentsMargins(0, 0, 0, 0)
            w.setLayout(l)
            l.addWidget(self.addWidget)
            l.addStretch()
            self.addWidgetBox = w
            self.addItem = QtGui.QTreeWidgetItem([])
            self.addItem.setFlags(QtCore.Qt.ItemIsEnabled)
            ParameterItem.addChild(self, self.addItem)

    def updateDepth(self, depth):
        if depth == 0:
            for c in (0, 1):
                self.setBackground(c, QtGui.QBrush(QtGui.QColor(100, 100, 100)))
                self.setForeground(c, QtGui.QBrush(QtGui.QColor(220, 220, 255)))
                font = self.font(c)
                font.setBold(True)
                font.setPointSize(font.pointSize() + 1)
                self.setFont(c, font)
                self.setSizeHint(0, QtCore.QSize(0, 25))

        else:
            for c in (0, 1):
                self.setBackground(c, QtGui.QBrush(QtGui.QColor(220, 220, 220)))
                font = self.font(c)
                font.setBold(True)
                self.setFont(c, font)
                self.setSizeHint(0, QtCore.QSize(0, 20))

    def addClicked(self):
        """Called when "add new" button is clicked
        The parameter MUST have an 'addNew' method defined.
        """
        self.param.addNew()

    def addChanged(self):
        """Called when "add new" combo is changed
        The parameter MUST have an 'addNew' method defined.
        """
        if self.addWidget.currentIndex() == 0:
            return
        typ = asUnicode(self.addWidget.currentText())
        self.param.addNew(typ)
        self.addWidget.setCurrentIndex(0)

    def treeWidgetChanged(self):
        ParameterItem.treeWidgetChanged(self)
        self.treeWidget().setFirstItemColumnSpanned(self, True)
        if self.addItem is not None:
            self.treeWidget().setItemWidget(self.addItem, 0, self.addWidgetBox)
            self.treeWidget().setFirstItemColumnSpanned(self.addItem, True)

    def addChild(self, child):
        if self.addItem is not None:
            ParameterItem.insertChild(self, self.childCount() - 1, child)
        else:
            ParameterItem.addChild(self, child)

    def optsChanged(self, param, changed):
        if 'addList' in changed:
            self.updateAddList()

    def updateAddList(self):
        self.addWidget.blockSignals(True)
        try:
            self.addWidget.clear()
            self.addWidget.addItem(self.param.opts['addText'])
            for t in self.param.opts['addList']:
                self.addWidget.addItem(t)

        finally:
            self.addWidget.blockSignals(False)


class GroupParameter(Parameter):
    __doc__ = "\n    Group parameters are used mainly as a generic parent item that holds (and groups!) a set\n    of child parameters. \n    \n    It also provides a simple mechanism for displaying a button or combo\n    that can be used to add new parameters to the group. To enable this, the group \n    must be initialized with the 'addText' option (the text will be displayed on\n    a button which, when clicked, will cause addNew() to be called). If the 'addList'\n    option is specified as well, then a dropdown-list of addable items will be displayed\n    instead of a button.\n    "
    itemClass = GroupParameterItem

    def addNew(self, typ=None):
        """
        This method is called when the user has requested to add a new item to the group.
        """
        raise Exception('Must override this function in subclass.')

    def setAddList(self, vals):
        """Change the list of options available for the user to add to the group."""
        self.setOpts(addList=vals)


registerParameterType('group', GroupParameter, override=True)

class ListParameterItem(WidgetParameterItem):
    __doc__ = '\n    WidgetParameterItem subclass providing comboBox that lets the user select from a list of options.\n    \n    '

    def __init__(self, param, depth):
        self.targetValue = None
        WidgetParameterItem.__init__(self, param, depth)

    def makeWidget(self):
        opts = self.param.opts
        t = opts['type']
        w = QtGui.QComboBox()
        w.setMaximumHeight(20)
        w.sigChanged = w.currentIndexChanged
        w.value = self.value
        w.setValue = self.setValue
        self.widget = w
        self.limitsChanged(self.param, self.param.opts['limits'])
        if len(self.forward) > 0:
            self.setValue(self.param.value())
        return w

    def value(self):
        key = asUnicode(self.widget.currentText())
        return self.forward.get(key, None)

    def setValue(self, val):
        self.targetValue = val
        if val not in self.reverse[0]:
            self.widget.setCurrentIndex(0)
        else:
            key = self.reverse[1][self.reverse[0].index(val)]
            ind = self.widget.findText(key)
            self.widget.setCurrentIndex(ind)

    def limitsChanged(self, param, limits):
        if len(limits) == 0:
            limits = [
             '']
        self.forward, self.reverse = ListParameter.mapping(limits)
        try:
            self.widget.blockSignals(True)
            val = self.targetValue
            self.widget.clear()
            for k in self.forward:
                self.widget.addItem(k)
                if k == val:
                    self.widget.setCurrentIndex(self.widget.count() - 1)
                    self.updateDisplayLabel()

        finally:
            self.widget.blockSignals(False)


class ListParameter(Parameter):
    itemClass = ListParameterItem

    def __init__(self, **opts):
        self.forward = OrderedDict()
        self.reverse = ([], [])
        if 'values' in opts:
            opts['limits'] = opts['values']
        if opts.get('limits', None) is None:
            opts['limits'] = []
        (Parameter.__init__)(self, **opts)
        self.setLimits(opts['limits'])

    def setLimits(self, limits):
        self.forward, self.reverse = self.mapping(limits)
        Parameter.setLimits(self, limits)
        if len(self.reverse[0]) > 0:
            if self.value() not in self.reverse[0]:
                self.setValue(self.reverse[0][0])

    @staticmethod
    def mapping(limits):
        forward = OrderedDict()
        reverse = ([], [])
        if isinstance(limits, dict):
            for k, v in limits.items():
                forward[k] = v
                reverse[0].append(v)
                reverse[1].append(k)

        else:
            for v in limits:
                n = asUnicode(v)
                forward[n] = v
                reverse[0].append(v)
                reverse[1].append(n)

        return (
         forward, reverse)


registerParameterType('list', ListParameter, override=True)

class ActionParameterItem(ParameterItem):

    def __init__(self, param, depth):
        ParameterItem.__init__(self, param, depth)
        self.layoutWidget = QtGui.QWidget()
        self.layout = QtGui.QHBoxLayout()
        self.layoutWidget.setLayout(self.layout)
        self.button = QtGui.QPushButton(param.name())
        self.layout.addWidget(self.button)
        self.layout.addStretch()
        self.button.clicked.connect(self.buttonClicked)
        param.sigNameChanged.connect(self.paramRenamed)
        self.setText(0, '')

    def treeWidgetChanged(self):
        ParameterItem.treeWidgetChanged(self)
        tree = self.treeWidget()
        if tree is None:
            return
        tree.setFirstItemColumnSpanned(self, True)
        tree.setItemWidget(self, 0, self.layoutWidget)

    def paramRenamed(self, param, name):
        self.button.setText(name)

    def buttonClicked(self):
        self.param.activate()


class ActionParameter(Parameter):
    __doc__ = 'Used for displaying a button within the tree.'
    itemClass = ActionParameterItem
    sigActivated = QtCore.Signal(object)

    def activate(self):
        self.sigActivated.emit(self)
        self.emitStateChanged('activated', None)


registerParameterType('action', ActionParameter, override=True)

class TextParameterItem(WidgetParameterItem):

    def __init__(self, param, depth):
        WidgetParameterItem.__init__(self, param, depth)
        self.hideWidget = False
        self.subItem = QtGui.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.textBox)
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def makeWidget(self):
        self.textBox = QtGui.QTextEdit()
        self.textBox.setMaximumHeight(100)
        self.textBox.setReadOnly(self.param.opts.get('readonly', False))
        self.textBox.value = lambda : str(self.textBox.toPlainText())
        self.textBox.setValue = self.textBox.setPlainText
        self.textBox.sigChanged = self.textBox.textChanged
        return self.textBox


class TextParameter(Parameter):
    __doc__ = 'Editable string; displayed as large text box in the tree.'
    itemClass = TextParameterItem


registerParameterType('text', TextParameter, override=True)