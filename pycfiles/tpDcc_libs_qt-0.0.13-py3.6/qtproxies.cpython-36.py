# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/externals/pysideuic/Compiler/qtproxies.py
# Compiled at: 2020-05-13 19:31:15
# Size of source mod 2**32: 13920 bytes
import sys, re
from pysideuic.Compiler.indenter import write_code
from pysideuic.Compiler.misc import Literal, moduleMember
if sys.hexversion >= 50331648:
    from pysideuic.port_v3.proxy_base import ProxyBase
    from pysideuic.port_v3.as_string import as_string
else:
    from pysideuic.port_v2.proxy_base import ProxyBase
    from pysideuic.port_v2.as_string import as_string
i18n_strings = []
i18n_context = ''

def i18n_print(string):
    i18n_strings.append(string)


def i18n_void_func(name):

    def _printer(self, *args):
        i18n_print('%s.%s(%s)' % (self, name, ', '.join(map(as_string, args))))

    return _printer


def i18n_func(name):

    def _printer(self, rname, *args):
        i18n_print('%s = %s.%s(%s)' % (rname, self, name, ', '.join(map(as_string, args))))
        return Literal(rname)

    return _printer


def strict_getattr(module, clsname):
    cls = getattr(module, clsname)
    if issubclass(cls, LiteralProxyClass):
        raise AttributeError(cls)
    else:
        return cls


class i18n_string(object):

    def __init__(self, string, disambig):
        self.string = string
        self.disambig = disambig

    def __str__(self):
        if self.disambig is None:
            disambig = 'None'
        else:
            disambig = as_string((self.disambig), encode=False)
        return 'QtGui.QApplication.translate("%s", %s, %s, QtGui.QApplication.UnicodeUTF8)' % (i18n_context, as_string((self.string), encode=False), disambig)


AS_ARGUMENT = 2

class ProxyClassMember(object):

    def __init__(self, proxy, function_name, flags):
        self.proxy = proxy
        self.function_name = function_name
        self.flags = flags

    def __str__(self):
        return '%s.%s' % (self.proxy, self.function_name)

    def __call__(self, *args):
        func_call = '%s.%s(%s)' % (self.proxy,
         self.function_name,
         ', '.join(map(as_string, args)))
        if self.flags & AS_ARGUMENT:
            self.proxy._uic_name = func_call
            return self.proxy
        else:
            needs_translation = False
            for arg in args:
                if isinstance(arg, i18n_string):
                    needs_translation = True

            if needs_translation:
                i18n_print(func_call)
            else:
                write_code(func_call)


class ProxyClass(ProxyBase):
    flags = 0

    def __init__(self, objectname, is_attribute, args=(), noInstantiation=False):
        if objectname:
            if is_attribute:
                objectname = 'self.' + objectname
            self._uic_name = objectname
        else:
            self._uic_name = 'Unnamed'
        if not noInstantiation:
            funcall = '%s(%s)' % (
             moduleMember(self.module, self.__class__.__name__),
             ', '.join(map(str, args)))
            if objectname:
                funcall = '%s = %s' % (objectname, funcall)
            write_code(funcall)

    def __str__(self):
        return self._uic_name

    def __getattribute__(self, attribute):
        try:
            return object.__getattribute__(self, attribute)
        except AttributeError:
            return ProxyClassMember(self, attribute, self.flags)


class LiteralProxyClass(ProxyClass):
    __doc__ = 'LiteralObject(*args) -> new literal class\n\n    a literal class can be used as argument in a function call\n\n    >>> class Foo(LiteralProxyClass): pass\n    >>> str(Foo(1,2,3)) == "Foo(1,2,3)"\n    '
    flags = AS_ARGUMENT

    def __init__(self, *args):
        self._uic_name = '%s(%s)' % (
         moduleMember(self.module, self.__class__.__name__),
         ', '.join(map(as_string, args)))


class ProxyNamespace(ProxyBase):
    pass


class QtCore(ProxyNamespace):

    class Qt(ProxyNamespace):
        pass

    class QMetaObject(ProxyClass):

        def connectSlotsByName(cls, *args):
            (ProxyClassMember(cls, 'connectSlotsByName', 0))(*args)

        connectSlotsByName = classmethod(connectSlotsByName)

    class QObject(ProxyClass):

        def metaObject(self):

            class _FakeMetaObject(object):

                def className(*args):
                    return self.__class__.__name__

            return _FakeMetaObject()

        def objectName(self):
            return self._uic_name.split('.')[(-1)]

        def connect(cls, *args):
            slot_name = str(args[(-1)])
            if slot_name.endswith('.raise'):
                args = list(args[:-1])
                args.append(Literal(slot_name + '_'))
            (ProxyClassMember(cls, 'connect', 0))(*args)

        connect = classmethod(connect)


_qwidgets = ('QCalendarWidget', 'QDialogButtonBox', 'QDockWidget', 'QGroupBox', 'QLineEdit',
             'QMainWindow', 'QMenuBar', 'QProgressBar', 'QStatusBar', 'QToolBar',
             'QWizardPage')

class QtGui(ProxyNamespace):

    class QApplication(QtCore.QObject):

        def translate(uiname, text, disambig, encoding):
            return i18n_string(text or '', disambig)

        translate = staticmethod(translate)

    class QIcon(ProxyClass):
        pass

    class QConicalGradient(ProxyClass):
        pass

    class QLinearGradient(ProxyClass):
        pass

    class QRadialGradient(ProxyClass):
        pass

    class QBrush(ProxyClass):
        pass

    class QPainter(ProxyClass):
        pass

    class QPalette(ProxyClass):
        pass

    class QFont(ProxyClass):
        pass

    class QSpacerItem(ProxyClass):
        pass

    class QSizePolicy(ProxyClass):
        pass

    class QAction(QtCore.QObject):
        pass

    class QActionGroup(QtCore.QObject):
        pass

    class QButtonGroup(QtCore.QObject):
        pass

    class QLayout(QtCore.QObject):

        def setMargin(self, v):
            ProxyClassMember(self, 'setContentsMargins', 0)(v, v, v, v)

    class QGridLayout(QLayout):
        pass

    class QBoxLayout(QLayout):
        pass

    class QHBoxLayout(QBoxLayout):
        pass

    class QVBoxLayout(QBoxLayout):
        pass

    class QFormLayout(QLayout):
        pass

    class QWidget(QtCore.QObject):

        def font(self):
            return Literal('%s.font()' % self)

        def minimumSizeHint(self):
            return Literal('%s.minimumSizeHint()' % self)

        def sizePolicy(self):
            sp = LiteralProxyClass()
            sp._uic_name = '%s.sizePolicy()' % self
            return sp

    class QDialog(QWidget):
        pass

    class QWizard(QDialog):
        pass

    class QAbstractSlider(QWidget):
        pass

    class QDial(QAbstractSlider):
        pass

    class QScrollBar(QAbstractSlider):
        pass

    class QSlider(QAbstractSlider):
        pass

    class QMenu(QWidget):

        def menuAction(self):
            return Literal('%s.menuAction()' % self)

    class QTabWidget(QWidget):

        def addTab(self, *args):
            text = args[(-1)]
            if isinstance(text, i18n_string):
                i18n_print('%s.setTabText(%s.indexOf(%s), %s)' % (
                 self._uic_name, self._uic_name, args[0], text))
                args = args[:-1] + ('', )
            (ProxyClassMember(self, 'addTab', 0))(*args)

        def indexOf(self, page):
            return Literal('%s.indexOf(%s)' % (self, page))

    class QComboBox(QWidget):
        pass

    class QFontComboBox(QComboBox):
        pass

    class QAbstractSpinBox(QWidget):
        pass

    class QDoubleSpinBox(QAbstractSpinBox):
        pass

    class QSpinBox(QAbstractSpinBox):
        pass

    class QDateTimeEdit(QAbstractSpinBox):
        pass

    class QDateEdit(QDateTimeEdit):
        pass

    class QTimeEdit(QDateTimeEdit):
        pass

    class QFrame(QWidget):
        pass

    class QLabel(QFrame):
        pass

    class QLCDNumber(QFrame):
        pass

    class QSplitter(QFrame):
        pass

    class QStackedWidget(QFrame):
        pass

    class QToolBox(QFrame):

        def addItem(self, *args):
            text = args[(-1)]
            if isinstance(text, i18n_string):
                i18n_print('%s.setItemText(%s.indexOf(%s), %s)' % (
                 self._uic_name, self._uic_name, args[0], text))
                args = args[:-1] + ('', )
            (ProxyClassMember(self, 'addItem', 0))(*args)

        def indexOf(self, page):
            return Literal('%s.indexOf(%s)' % (self, page))

        def layout(self):
            return QtGui.QLayout(('%s.layout()' % self), False,
              (), noInstantiation=True)

    class QAbstractScrollArea(QFrame):
        pass

    class QGraphicsView(QAbstractScrollArea):
        pass

    class QMdiArea(QAbstractScrollArea):
        pass

    class QPlainTextEdit(QAbstractScrollArea):
        pass

    class QScrollArea(QAbstractScrollArea):
        pass

    class QTextEdit(QAbstractScrollArea):
        pass

    class QTextBrowser(QTextEdit):
        pass

    class QAbstractItemView(QAbstractScrollArea):
        pass

    class QColumnView(QAbstractItemView):
        pass

    class QHeaderView(QAbstractItemView):
        pass

    class QListView(QAbstractItemView):
        pass

    class QTableView(QAbstractItemView):

        def horizontalHeader(self):
            return QtGui.QHeaderView(('%s.horizontalHeader()' % self), False,
              (), noInstantiation=True)

        def verticalHeader(self):
            return QtGui.QHeaderView(('%s.verticalHeader()' % self), False,
              (), noInstantiation=True)

    class QTreeView(QAbstractItemView):

        def header(self):
            return QtGui.QHeaderView(('%s.header()' % self), False,
              (), noInstantiation=True)

    class QListWidgetItem(ProxyClass):
        pass

    class QListWidget(QListView):
        isSortingEnabled = i18n_func('isSortingEnabled')
        setSortingEnabled = i18n_void_func('setSortingEnabled')

        def item(self, row):
            return QtGui.QListWidgetItem(('%s.item(%i)' % (self, row)), False, (), noInstantiation=True)

    class QTableWidgetItem(ProxyClass):
        pass

    class QTableWidget(QTableView):
        isSortingEnabled = i18n_func('isSortingEnabled')
        setSortingEnabled = i18n_void_func('setSortingEnabled')

        def item(self, row, col):
            return QtGui.QTableWidgetItem(('%s.item(%i, %i)' % (self, row, col)), False,
              (), noInstantiation=True)

        def horizontalHeaderItem(self, col):
            return QtGui.QTableWidgetItem(('%s.horizontalHeaderItem(%i)' % (self, col)), False,
              (), noInstantiation=True)

        def verticalHeaderItem(self, row):
            return QtGui.QTableWidgetItem(('%s.verticalHeaderItem(%i)' % (self, row)), False,
              (), noInstantiation=True)

    class QTreeWidgetItem(ProxyClass):

        def child(self, index):
            return QtGui.QTreeWidgetItem(('%s.child(%i)' % (self, index)), False,
              (), noInstantiation=True)

    class QTreeWidget(QTreeView):
        isSortingEnabled = i18n_func('isSortingEnabled')
        setSortingEnabled = i18n_void_func('setSortingEnabled')

        def headerItem(self):
            return QtGui.QWidget(('%s.headerItem()' % self), False, (), noInstantiation=True)

        def topLevelItem(self, index):
            return QtGui.QTreeWidgetItem(('%s.topLevelItem(%i)' % (self, index)), False,
              (), noInstantiation=True)

    class QAbstractButton(QWidget):
        pass

    class QCheckBox(QAbstractButton):
        pass

    class QRadioButton(QAbstractButton):
        pass

    class QToolButton(QAbstractButton):
        pass

    class QPushButton(QAbstractButton):
        pass

    class QCommandLinkButton(QPushButton):
        pass

    for _class in _qwidgets:
        if _class not in locals():
            locals()[_class] = type(_class, (QWidget,), {})