# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/input_yoke.py
# Compiled at: 2014-02-03 13:19:08
"""
An input yoke provides knowledge of the Qt property names and signals 
associated with widget input.  This ties the input widgets to the model 
attributes.

The yokes work with a mapper object which holds the object whose attributes 
are being edited.
"""
from .PyQtModels import *
from .PyQtHelpers import *

class InputYoke(object):
    """
    InputYoke is an abstract base class.
    """

    class Label(object):
        External = 0
        Internal = 1

    def __init__(self, mapper):
        self.mapper = mapper
        self.knowable_dirty = False
        self.is_dirty = False

    def mark_dirty(self):
        self.is_dirty = True

    def _save_dirty_blowout(self):
        if hasattr(self, 'attr') and attrReadonly(self.mapper.cls, self.attr):
            return True
        if not self.mapper.connected():
            return True
        if self.knowable_dirty and not self.is_dirty:
            return True
        return False

    def Factory(self):
        """
        In this event you should:
        
        #. Create the widget
        #. Set size hints and other widget attributes
        #. Connect to signals
        #. Return the newly created widet
        """
        return

    def AdoptWidget(self, widget):
        self.widget = widget
        self._baseAdoptWidget(self.widget)

    def _baseAdoptWidget(self, widget):
        widget.setWhatsThis(ClassAttributeWhatsThis(getattr(self.mapper.cls, self.attr)))
        widget.setProperty('BoundClassField', ('{0}.{1}').format(self.mapper.cls.__name__, self.attr))

    def focus(self):
        self.widget.setFocus(QtCore.Qt.OtherFocusReason)

    def mainWidget(self):
        return self.widget

    def Bind(self):
        """
        Data initialization.
        """
        pass

    def Update(self, key):
        self.Bind()

    def Save(self):
        """
        Data initialization.
        """
        pass

    def LabelStyle(self):
        return InputYoke.Label.External


class LineYoke(InputYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        self.widget = QtGui.QLineEdit()
        self.widget.editingFinished.connect(self.Save)
        self.widget.textChanged.connect(lambda text: self.mark_dirty())
        self.knowable_dirty = True
        self._baseAdoptWidget(self.widget)
        if attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def AdoptWidget(self, widget):
        self.widget = widget
        self._baseAdoptWidget(self.widget)
        if isinstance(self.widget, QtGui.QLineEdit):
            self.widget.editingFinished.connect(self.Save)
            self.widget.textChanged.connect(lambda text: self.mark_dirty())
            self.knowable_dirty = True
        if hasattr(self.widget, 'setReadOnly') and attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)

    def Bind(self):
        if isinstance(self.widget, QtGui.QLineEdit):
            self.widget.setText(self.mapper.getObjectAttr(self.attr))
            self.is_dirty = False
        elif isinstance(self.widget, QtGui.QComboBox):
            if self.widget.isEditable():
                self.widget.setEditText(self.mapper.getObjectAttr(self.attr))
            else:
                self.widget.setCurrentIndex(self.widget.findText(self.mapper.getObjectAttr(self.attr), QtCore.Qt.MatchFixedString))
        else:
            raise ValueError(('The widget {0} is not supported by a {1}').format(self.widget, self.__class__.__name__))

    def Save(self):
        if self._save_dirty_blowout():
            return
        if isinstance(self.widget, QtGui.QLineEdit):
            self.mapper.setObjectAttr(self.attr, self.widget.text())
        elif isinstance(self.widget, QtGui.QComboBox):
            self.mapper.setObjectAttr(self.attr, self.widget.currentText())
        else:
            raise ValueError(('The widget {0} is not supported by a {1}').format(self.widget, self.__class__.__name__))


class SelectionYoke(LineYoke):
    """
    This yoke drives combo boxes.  Note that this yoke is not directly 
    usable as a yoke factory due to the options parameter.  It is intended 
    to be wrapped in a factory function and exposed to the global yoke 
    factory with :func:`addGlobalYoke`.
    
    >>> def ColorComboYoke(mapper, attr):
    ...     return SelectionYoke(mapper, attr, ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"])
    ...
    >>> addGlobalYoke('color', ColorComboYoke)
    
    :param options:  a list of strings to include in the combo box
    """

    def __init__(self, mapper, attr, options):
        LineYoke.__init__(self, mapper, attr)
        self.options = options

    def Factory(self):
        self.widget = QtGui.QComboBox()
        self.widget.currentIndexChanged.connect(lambda text: self.Save())
        self._baseAdoptWidget(self.widget)
        self._loadOptions()
        if attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def AdoptWidget(self, widget):
        self.widget = widget
        self._baseAdoptWidget(self.widget)
        self._loadOptions()
        if hasattr(self.widget, 'currentIndexChanged'):
            self.widget.currentIndexChanged.connect(lambda text: self.Save())
        if hasattr(self.widget, 'setReadOnly') and attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)

    def _loadOptions(self):
        for o in self.options:
            self.widget.addItem(o)


class PasswordYoke(LineYoke):

    def Factory(self):
        LineYoke.Factory(self)
        self.widget.setEchoMode(QtGui.QLineEdit.Password)
        return self.widget

    def AdoptWidget(self, widget):
        LineYoke.AdoptWidget(self, widget)
        self.widget.setEchoMode(QtGui.QLineEdit.Password)


class BlankIntValidator(QtGui.QIntValidator):

    def validate(self, input, pos):
        if input == '':
            return (QtGui.QValidator.Acceptable, input, pos)
        else:
            return QtGui.QIntValidator.validate(self, input, pos)


class IntegerYoke(LineYoke):

    def Factory(self):
        self.widget = QtGui.QLineEdit()
        self.widget.setMaximumWidth(100)
        self._baseAdoptWidget(self.widget)
        self.widget.setValidator(BlankIntValidator())
        self.widget.editingFinished.connect(self.Save)
        if attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def Bind(self):
        x = self.mapper.getObjectAttr(self.attr)
        if x is None:
            x = 0
        self.widget.setText(str(x))
        return

    def Save(self):
        if self._save_dirty_blowout():
            return
        else:
            t = self.widget.text()
            x = 0 if t in (None, '') else int(t)
            self.mapper.setObjectAttr(self.attr, x)
            return


class BlankFloatValidator(QtGui.QDoubleValidator):

    def validate(self, input, pos):
        if input == '':
            return (QtGui.QValidator.Acceptable, input, pos)
        else:
            return QtGui.QDoubleValidator.validate(self, input, pos)


class FloatingPointYoke(LineYoke):

    def Factory(self):
        self.widget = QtGui.QLineEdit()
        self.widget.setMaximumWidth(120)
        self._baseAdoptWidget(self.widget)
        self.widget.setValidator(BlankFloatValidator(self.widget))
        self.widget.editingFinished.connect(self.Save)
        if attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def Bind(self):
        x = self.mapper.getObjectAttr(self.attr)
        if x is None:
            x = 0.0
        self.widget.setText(str(x))
        return

    def Save(self):
        if self._save_dirty_blowout():
            return
        else:
            t = self.widget.text()
            x = decimal.Decimal('0') if t in (None, '') else decimal.Decimal(t)
            self.mapper.setObjectAttr(self.attr, x)
            return


class TextYoke(InputYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        self.widget = QtGui.QTextEdit()
        self._baseAdoptWidget(self.widget)
        self.widget.setAcceptRichText(False)
        self.widget.setTabChangesFocus(True)
        if hasattr(self.widget, 'setReadOnly') and attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def Bind(self):
        if isinstance(self.widget, QtGui.QLineEdit) or isinstance(self.widget, QtGui.QTextEdit):
            self.widget.setText(self.mapper.getObjectAttr(self.attr))
        elif isinstance(self.widget, QtGui.QPlainTextEdit):
            self.widget.setPlainText(self.mapper.getObjectAttr(self.attr))
        elif isinstance(self.widget, QtGui.QComboBox):
            self.widget.setEditText(self.mapper.getObjectAttr(self.attr))
        else:
            raise ValueError(('The widget {0} is not supported by a {1}').format(self.widget, self.__class__.__name__))

    def Save(self):
        if self._save_dirty_blowout():
            return
        if isinstance(self.widget, QtGui.QTextEdit) or isinstance(self.widget, QtGui.QPlainTextEdit):
            self.mapper.setObjectAttr(self.attr, self.widget.toPlainText())
        elif isinstance(self.widget, QtGui.QLineEdit):
            self.mapper.setObjectAttr(self.attr, self.widget.text())
        elif isinstance(self.widget, QtGui.QComboBox):
            self.mapper.setObjectAttr(self.attr, self.widget.currentText())
        else:
            raise ValueError(('The widget {0} is not supported by a {1}').format(self.widget, self.__class__.__name__))


class FormattedYoke(InputYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        self.widget = QtGui.QTextEdit()
        self._baseAdoptWidget(self.widget)
        self.widget.setTabChangesFocus(True)
        if hasattr(self.widget, 'setReadOnly') and attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def Bind(self):
        if isinstance(self.widget, QtGui.QTextEdit):
            self.widget.setHtml(self.mapper.getObjectAttr(self.attr))
        else:
            raise ValueError(('The widget {0} is not supported by a {1}').format(self.widget, self.__class__.__name__))

    def Save(self):
        if self._save_dirty_blowout():
            return
        if isinstance(self.widget, QtGui.QTextEdit):
            self.mapper.setObjectAttr(self.attr, self.widget.toHtml())
        else:
            raise ValueError(('The widget {0} is not supported by a {1}').format(self.widget, self.__class__.__name__))


class CodeYoke(InputYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        self.widget = QtGui.QPlainTextEdit()
        self.widget.setFont(QtGui.QFont('Courier', 10))
        self.widget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self._baseAdoptWidget(self.widget)
        if hasattr(self.widget, 'setReadOnly') and attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def Bind(self):
        if isinstance(self.widget, QtGui.QPlainTextEdit):
            self.widget.setPlainText(self.mapper.getObjectAttr(self.attr))
        else:
            raise ValueError(('The widget {0} is not supported by a {1}').format(self.widget, self.__class__.__name__))

    def Save(self):
        if self._save_dirty_blowout():
            return
        if isinstance(self.widget, QtGui.QPlainTextEdit):
            self.mapper.setObjectAttr(self.attr, self.widget.toPlainText())
        else:
            raise ValueError(('The widget {0} is not supported by a {1}').format(self.widget, self.__class__.__name__))


class DateYoke(LineYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        from .widgets import PBDateEdit
        self.widget = PBDateEdit()
        self._baseAdoptWidget(self.widget)
        self.widget.editingFinished.connect(self.Save)
        self.widget.textChanged.connect(lambda text: self.mark_dirty())
        self.knowable_dirty = True
        if hasattr(self.widget, 'setReadOnly') and attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def Bind(self):
        d = self.mapper.getObjectAttr(self.attr)
        if d is not None:
            d = toQType(d)
        self.widget.setDate(d)
        self.is_dirty = False
        return

    def Save(self):
        if self._save_dirty_blowout():
            return
        else:
            d = self.widget.date
            if d is None:
                self.mapper.setObjectAttr(self.attr, None)
            else:
                self.mapper.setObjectAttr(self.attr, fromQType(d, datetime.date))
            return


class TimeYoke(LineYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        self.widget = QTimeEdit()
        self._baseAdoptWidget(self.widget)
        self.widget.editingFinished.connect(self.Save)
        if hasattr(self.widget, 'setReadOnly') and attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def AdoptWidget(self, widget):
        self.widget = widget
        if isinstance(self.widget, QtGui.QLineEdit):
            self.widget.editingFinished.connect(self.Save)
        if hasattr(self.widget, 'setReadOnly') and attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)

    def Bind(self):
        d = self.mapper.getObjectAttr(self.attr)
        if d is not None:
            d = toQType(d)
        else:
            d = QtCore.QTime(0, 0)
        self.widget.setTime(d)
        return

    def Save(self):
        if self._save_dirty_blowout():
            return
        else:
            d = self.widget.time()
            if d is None:
                self.mapper.setObjectAttr(self.attr, None)
            else:
                self.mapper.setObjectAttr(self.attr, fromQType(d, datetime.time))
            return


class BooleanYoke(InputYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        self.widget = QtGui.QCheckBox(ClassAttributeLabel(getattr(self.mapper.cls, self.attr)))
        self._baseAdoptWidget(self.widget)
        self.widget.toggled.connect(self.Save)
        return self.widget

    def AdoptWidget(self, widget):
        self.widget = widget
        if isinstance(self.widget, QtGui.QAbstractButton):
            self.widget.toggled.connect(self.Save)

    def Bind(self):
        self.widget.setChecked(toQType(self.mapper.getObjectAttr(self.attr), bool))

    def Save(self):
        if self._save_dirty_blowout():
            return
        self.mapper.setObjectAttr(self.attr, fromQType(self.widget.isChecked()))

    def LabelStyle(self):
        return InputYoke.Label.Internal


class BooleanRadioYoke(InputYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        raise NotImplementedError('somebody needs to make a UserAttr with descriptions for the radio buttons')

    def AdoptWidget(self, widget):
        """
        The widget parameter to :method:`WidgetAttributeMapper.bind` must be a 
        two-tuple of radio buttons when the bound yoke is a :class:`BooleanRadioYoke`. 
        The first widget is the radio button mapped to true and the second is 
        mapped to False.
        """
        assert len(widget) == 2, "I don't know what do to with this if it's not a list of length 2"
        self.true_radio = widget[0]
        self.false_radio = widget[1]
        if self.true_radio.group() is None:
            self.group = QtGui.QButtonGroup(self.true_radio.parent())
            self.group.addButton(self.true_radio)
            self.group.addButton(self.false_radio)
        self.true_radio.toggled.connect(lambda checked, value=True: self.radioChange(value, checked))
        self.false_radio.toggled.connect(lambda checked, value=False: self.radioChange(value, checked))
        for w in [self.true_radio, self.false_radio]:
            self._baseAdoptWidget(w)

        return

    def radioChange(self, value, clicked):
        if clicked:
            self.Save(value)

    def Bind(self):
        value = toQType(self.mapper.getObjectAttr(self.attr), bool)
        if value:
            self.true_radio.setChecked(True)
        else:
            self.false_radio.setChecked(True)

    def Save(self, value=None):
        if self._save_dirty_blowout():
            return
        else:
            if value is None:
                if self.true_radio.isChecked():
                    value = True
                if self.false_radio.isChecked():
                    value = False
            self.mapper.setObjectAttr(self.attr, value)
            return

    def LabelStyle(self):
        return InputYoke.Label.Internal


class ImageYoke(InputYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def _baseAdoptWidget(self, widget):
        widget.setMaximumSize(250, 200)
        widget.setFrameShape(QtGui.QFrame.StyledPanel)
        widget.setScaledContents(True)
        if not attrReadonly(self.mapper.cls, self.attr):
            widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
            self.action_set_image = QtGui.QAction('Assign &Image...', widget)
            self.action_set_image.triggered.connect(self.assign_image)
            widget.addAction(self.action_set_image)

    def assign_image(self):
        filename = qtGetOpenFileName(self.widget.window(), 'Select Image', 'Images (*.png *.jpg)')
        if filename != None:
            self.mapper.setObjectAttr(self.attr, open(filename, 'rb').read())
            self.Bind()
        return

    def Factory(self):
        self.widget = QtGui.QLabel()
        self.widget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self._baseAdoptWidget(self.widget)
        return self.widget

    def Bind(self):
        if isinstance(self.widget, QtGui.QLabel):
            value = self.mapper.getObjectAttr(self.attr)
            pixmap = None
            if value == None or len(value) == 0:
                pixmap = QtGui.QPixmap(250, 200)
                pixmap.fill()
            else:
                try:
                    pixmap = QtGui.QPixmap.fromImage(QtGui.QImage.fromData(self.mapper.getObjectAttr(self.attr)))
                except Exception as e:
                    self.widget.setText(('Corrupt Image ({})').format(str(e)))

            if pixmap != None:
                self.widget.setPixmap(pixmap)
        else:
            raise ValueError(('The widget {0} is not supported by a {1}').format(self.widget, self.__class__.__name__))
        return

    def Save(self):
        pass


def yokes_dict():
    d = {}
    d['date'] = DateYoke
    d['time'] = TimeYoke
    d['bool'] = BooleanYoke
    d['bool:options'] = BooleanRadioYoke
    d['int'] = IntegerYoke
    d['float'] = FloatingPointYoke
    d['text'] = TextYoke
    d['code'] = CodeYoke
    d['formatted'] = FormattedYoke
    d['line'] = LineYoke
    d['password'] = PasswordYoke
    d['image'] = ImageYoke
    from .widgets import StreetAddressYoke
    d['address'] = StreetAddressYoke
    from . import foreign_key
    d['foreign_key'] = foreign_key.ForeignKeyEditYoke
    d['foreign_key_edit'] = foreign_key.ForeignKeyEditYoke
    d['foreign_key_combo'] = foreign_key.ForeignKeyComboYoke
    if QtCore.QCoreApplication.instance() and hasattr(QtCore.QCoreApplication.instance(), 'yokes'):
        d.update(QtCore.QCoreApplication.instance().yokes)
    return d


def addGlobalYoke(yoke, yokeFactory):
    """
    Add the yoke and yokeFactory to the global list of yokes.  Currently this 
    relies on the singleton QtCore.QCoreApplication.instance() by adding the 
    yoke to a dictionary set up in the yokes attribute of this class.  This 
    implementation detail has user ramifications, but is not considered an 
    ideal implementation.
    
    :param yoke:  the name of the yoke
    :param yokeFactory:  a callable taking a mapper class and an attribute
    """
    if not QtCore.QCoreApplication.instance():
        raise RuntimeError('The addGlobalYoke function relies on having a QtCore.QCoreApplication instance available')
    if not hasattr(QtCore.QCoreApplication.instance(), 'yokes'):
        QtCore.QCoreApplication.instance().yokes = {}
    QtCore.QCoreApplication.instance().yokes[yoke] = yokeFactory


def YokeFactory(cls, attr, mapper, parent=None, index=None):
    """
    Create a yoke for the attribute `attr` in class `cls`.  Each sqlalchemy 
    column attribute and UserAttr can have a yoke specified for it in the 
    following ways:
      - specify a named yoke in a sqlalchemy column by including an info 
        parameter to the Column constructor.  For example::
        
            Column('name', Text, info={"yoke": "line"})

      - specify a named yoke in a UserAttr derived class by overriding the 
        yoke_specifier method and returning the name of the yoke

    The list of yoke names is extensible and individual yokes can be replaced by 
    calling :func:`addGlobalYoke`.
    """
    userattr = getattr(cls, attr)
    spec = ClassAttributeYoke(userattr)
    yoke_class = yokes_dict()[spec]
    return yoke_class(mapper, attr)