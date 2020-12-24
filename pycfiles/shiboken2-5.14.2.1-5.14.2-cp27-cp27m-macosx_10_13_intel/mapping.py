# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_install/py2.7-qt5.14.2-64bit-release/lib/python2.7/site-packages/shiboken2/files.dir/shibokensupport/signature/mapping.py
# Compiled at: 2020-04-24 02:55:46
from __future__ import print_function, absolute_import
import sys, struct, os
from shibokensupport.signature import typing
from shibokensupport.signature.typing import TypeVar, Generic
from shibokensupport.signature.lib.tool import with_metaclass

class ellipsis(object):

    def __repr__(self):
        return '...'


ellipsis = ellipsis()
Point = typing.Tuple[(float, float)]
Variant = typing.Any
ModelIndexList = typing.List[int]
QImageCleanupFunction = typing.Callable
NoneType = type(None)
_S = TypeVar('_S')

class _CharMeta(type):

    def __repr__(self):
        return '%s.%s' % (self.__module__, self.__name__)


class Char(with_metaclass(_CharMeta)):
    """
    From http://doc.qt.io/qt-5/qchar.html :

    In Qt, Unicode characters are 16-bit entities without any markup or
    structure. This class represents such an entity. It is lightweight,
    so it can be used everywhere. Most compilers treat it like an
    unsigned short.

    Here, we provide a simple implementation just to avoid long aliases.
    """
    __module__ = 'typing'

    def __init__(self, code):
        if isinstance(code, int):
            self.code = code & 65535
        else:
            self.code = ord(code)

    def __add__(self, other):
        return chr(self.code) + other

    def __radd__(self, other):
        return other + chr(self.code)

    def __repr__(self):
        return ('typing.Char({})').format(self.code)


typing.Char = Char
MultiMap = typing.DefaultDict[(str, typing.List[str])]
ulong_max = 2 * sys.maxsize + 1 if len(struct.pack('L', 1)) != 4 else 4294967295
ushort_max = 65535
GL_COLOR_BUFFER_BIT = 16384
GL_NEAREST = 9728
WId = int
GL_TEXTURE_2D = 3553
GL_RGBA = 6408

class _NotCalled(str):
    """
    Wrap some text with semantics

    This class is wrapped around text in order to avoid calling it.
    There are three reasons for this:

      - some instances cannot be created since they are abstract,
      - some can only be created after qApp was created,
      - some have an ugly __repr__ with angle brackets in it.

    By using derived classes, good looking instances can be created
    which can be used to generate source code or .pyi files. When the
    real object is needed, the wrapper can simply be called.
    """

    def __repr__(self):
        return ('{}({})').format(type(self).__name__, self)

    def __call__(self):
        from shibokensupport.signature.mapping import __dict__ as namespace
        text = self if self.endswith(')') else self + '()'
        return eval(text, namespace)


USE_PEP563 = False

class Virtual(_NotCalled):
    pass


class Missing(_NotCalled):

    def __repr__(self):
        if USE_PEP563:
            return _NotCalled.__repr__(self)
        return ('{}("{}")').format(type(self).__name__, self)


class Invalid(_NotCalled):
    pass


class Default(_NotCalled):
    pass


class Instance(_NotCalled):
    pass


class _Parameterized(object):

    def __init__(self, type):
        self.type = type
        self.__name__ = self.__class__.__name__

    def __repr__(self):
        return ('{}({})').format(type(self).__name__, self.type.__name__)


class ResultVariable(_Parameterized):
    pass


class ArrayLikeVariable(_Parameterized):
    pass


StringList = ArrayLikeVariable(str)

class Reloader(object):
    """
    Reloder class

    This is a singleton class which provides the update function for the
    shiboken and PySide classes.
    """

    def __init__(self):
        self.sys_module_count = 0

    @staticmethod
    def module_valid(mod):
        if getattr(mod, '__file__', None) and not os.path.isdir(mod.__file__):
            ending = os.path.splitext(mod.__file__)[(-1)]
            return ending not in ('.py', '.pyc', '.pyo', '.pyi')
        else:
            return False

    def update(self):
        """
        'update' imports all binary modules which are already in sys.modules.
        The reason is to follow all user imports without introducing new ones.
        This function is called by pyside_type_init to adapt imports
        when the number of imported modules has changed.
        """
        if self.sys_module_count == len(sys.modules):
            return
        self.sys_module_count = len(sys.modules)
        g = globals()
        candidates = list(mod_name for mod_name in sys.modules.copy() if self.module_valid(sys.modules[mod_name]))
        for mod_name in candidates:
            top = __import__(mod_name)
            g[top.__name__] = top
            proc_name = 'init_' + mod_name.replace('.', '_')
            if proc_name in g:
                g.update(g.pop(proc_name)())


def check_module(mod):
    if not Reloader.module_valid(mod):
        mod_name = mod.__name__
        raise ImportError(("Module '{mod_name}' is not a binary module!").format(**locals()))


update_mapping = Reloader().update
type_map = {}
namespace = globals()
type_map.update({'...': ellipsis, 
   'bool': bool, 
   'char': Char, 
   'char*': str, 
   'char*const': str, 
   'double': float, 
   'float': float, 
   'int': int, 
   'List': ArrayLikeVariable, 
   'long': int, 
   'PyCallable': typing.Callable, 
   'PyObject': object, 
   'PySequence': typing.Iterable, 
   'PyTypeObject': type, 
   'QChar': Char, 
   'QHash': typing.Dict, 
   'qint16': int, 
   'qint32': int, 
   'qint64': int, 
   'qint8': int, 
   'qintptr': int, 
   'QList': ArrayLikeVariable, 
   'qlonglong': int, 
   'QMap': typing.Dict, 
   'QPair': typing.Tuple, 
   'qptrdiff': int, 
   'qreal': float, 
   'QSet': typing.Set, 
   'QString': str, 
   'QStringList': StringList, 
   'quint16': int, 
   'quint32': int, 
   'quint32': int, 
   'quint64': int, 
   'quint8': int, 
   'quintptr': int, 
   'qulonglong': int, 
   'QVariant': Variant, 
   'QVector': typing.List, 
   'real': float, 
   'short': int, 
   'signed char': Char, 
   'signed long': int, 
   'std.list': typing.List, 
   'std.map': typing.Dict, 
   'std.pair': typing.Tuple, 
   'std.vector': typing.List, 
   'str': str, 
   'true': True, 
   'Tuple': typing.Tuple, 
   'uchar': Char, 
   'uchar*': str, 
   'uint': int, 
   'ulong': int, 
   'ULONG_MAX': ulong_max, 
   'unsigned char': Char, 
   'unsigned char*': str, 
   'unsigned int': int, 
   'unsigned long int': int, 
   'unsigned long long': int, 
   'unsigned long': int, 
   'unsigned short int': int, 
   'unsigned short': int, 
   'Unspecified': None, 
   'ushort': int, 
   'void': int, 
   'WId': WId, 
   'zero(bytes)': '', 
   'zero(Char)': 0, 
   'zero(float)': 0, 
   'zero(int)': 0, 
   'zero(object)': None, 
   'zero(str)': '', 
   'zero(typing.Any)': None})
type_map.update({'array double*': ArrayLikeVariable(float), 
   'array float*': ArrayLikeVariable(float), 
   'array GLint*': ArrayLikeVariable(int), 
   'array GLuint*': ArrayLikeVariable(int), 
   'array int*': ArrayLikeVariable(int), 
   'array long long*': ArrayLikeVariable(int), 
   'array long*': ArrayLikeVariable(int), 
   'array short*': ArrayLikeVariable(int), 
   'array signed char*': bytes, 
   'array unsigned char*': bytes, 
   'array unsigned int*': ArrayLikeVariable(int), 
   'array unsigned short*': ArrayLikeVariable(int)})
type_map.update({'char*': bytes, 
   'QChar*': bytes, 
   'quint32*': int, 
   'quint8*': bytearray, 
   'uchar*': bytes, 
   'unsigned char*': bytes})
type_map.update({'bool*': ResultVariable(bool), 
   'float*': ResultVariable(float), 
   'int*': ResultVariable(int), 
   'long long*': ResultVariable(int), 
   'long*': ResultVariable(int), 
   'PStr*': ResultVariable(str), 
   'qint32*': ResultVariable(int), 
   'qint64*': ResultVariable(int), 
   'qreal*': ResultVariable(float), 
   'QString*': ResultVariable(str), 
   'quint16*': ResultVariable(int), 
   'uint*': ResultVariable(int), 
   'unsigned int*': ResultVariable(int), 
   'QStringList*': ResultVariable(StringList)})

def init_Shiboken():
    type_map.update({'PyType': type, 
       'shiboken2.bool': bool, 
       'size_t': int})
    return locals()


def init_minimal():
    type_map.update({'MinBool': bool})
    return locals()


def init_sample():
    import datetime
    type_map.update({'char': Char, 
       'char**': typing.List[str], 
       'Complex': complex, 
       'double': float, 
       'Foo.HANDLE': int, 
       'HANDLE': int, 
       'Null': None, 
       'nullptr': None, 
       'ObjectType.Identifier': Missing('sample.ObjectType.Identifier'), 
       'OddBool': bool, 
       'PStr': str, 
       'PyDate': datetime.date, 
       'sample.bool': bool, 
       'sample.char': Char, 
       'sample.double': float, 
       'sample.int': int, 
       'sample.ObjectType': object, 
       'sample.OddBool': bool, 
       'sample.Photon.TemplateBase[Photon.DuplicatorType]': sample.Photon.ValueDuplicator, 
       'sample.Photon.TemplateBase[Photon.IdentityType]': sample.Photon.ValueIdentity, 
       'sample.Point': Point, 
       'sample.PStr': str, 
       'sample.unsigned char': Char, 
       'std.size_t': int, 
       'std.string': str, 
       'ZeroIn': 0, 
       'Str("<unk")': '<unk', 
       'Str("<unknown>")': '<unknown>', 
       'Str("nown>")': 'nown>'})
    return locals()


def init_other():
    import numbers
    type_map.update({'other.ExtendsNoImplicitConversion': Missing('other.ExtendsNoImplicitConversion'), 
       'other.Number': numbers.Number})
    return locals()


def init_smart():
    global SharedPtr

    class SharedPtr(Generic[_S]):
        __module__ = 'smart'

    smart.SharedPtr = SharedPtr
    type_map.update({'smart.Smart.Integer2': int})
    return locals()


def init_PySide2_QtCore():
    from PySide2.QtCore import Qt, QUrl, QDir
    from PySide2.QtCore import QRect, QSize, QPoint, QLocale, QByteArray
    from PySide2.QtCore import QMarginsF
    try:
        from PySide2.QtCore import Connection
    except ImportError:
        pass

    type_map.update({"' '": ' ', 
       "'%'": '%', 
       "'g'": 'g', 
       '4294967295UL': 4294967295, 
       'CheckIndexOption.NoOption': Instance('PySide2.QtCore.QAbstractItemModel.CheckIndexOptions.NoOption'), 
       'false': False, 
       'list of QAbstractAnimation': typing.List[PySide2.QtCore.QAbstractAnimation], 
       'list of QAbstractState': typing.List[PySide2.QtCore.QAbstractState], 
       'long long': int, 
       'NULL': None, 
       'nullptr': None, 
       'PyByteArray': bytearray, 
       'PyBytes': bytes, 
       'PySide2.QtCore.QCborStreamReader.StringResult[PySide2.QtCore.QByteArray]': PySide2.QtCore.QCborStringResultByteArray, 
       'PySide2.QtCore.QCborStreamReader.StringResult[QString]': PySide2.QtCore.QCborStringResultString, 
       'PySide2.QtCore.QCborStreamReader.QCborStringResultByteArray': PySide2.QtCore.QCborStringResultByteArray, 
       'PySide2.QtCore.QCborStreamReader.QCborStringResultString': PySide2.QtCore.QCborStringResultString, 
       'PySide2.QtCore.QUrl.ComponentFormattingOptions': PySide2.QtCore.QUrl.ComponentFormattingOption, 
       'PyUnicode': typing.Text, 
       'Q_NULLPTR': None, 
       'QDir.Filters(AllEntries | NoDotAndDotDot)': Instance('QDir.Filters(QDir.AllEntries | QDir.NoDotAndDotDot)'), 
       'QDir.SortFlags(Name | IgnoreCase)': Instance('QDir.SortFlags(QDir.Name | QDir.IgnoreCase)'), 
       'QGenericArgument((0))': ellipsis, 
       'QGenericArgument()': ellipsis, 
       'QGenericArgument(0)': ellipsis, 
       'QGenericArgument(NULL)': ellipsis, 
       'QGenericArgument(nullptr)': ellipsis, 
       'QGenericArgument(Q_NULLPTR)': ellipsis, 
       'QJsonObject': typing.Dict[(str, PySide2.QtCore.QJsonValue)], 
       'QModelIndex()': Invalid('PySide2.QtCore.QModelIndex'), 
       'QModelIndexList': ModelIndexList, 
       'QModelIndexList': ModelIndexList, 
       'QString()': '', 
       'QStringList()': [], 'QStringRef': str, 
       'QStringRef': str, 
       'Qt.HANDLE': int, 
       'QUrl.FormattingOptions(PrettyDecoded)': Instance('QUrl.FormattingOptions(QUrl.PrettyDecoded)'), 
       'QVariant()': Invalid(Variant), 
       'QVariant.Type': type, 
       'QVariantMap': typing.Dict[(str, Variant)], 
       'QVariantMap': typing.Dict[(str, Variant)]})
    try:
        type_map.update({'PySide2.QtCore.QMetaObject.Connection': PySide2.QtCore.Connection})
    except AttributeError:
        pass

    return locals()


def init_PySide2_QtGui():
    from PySide2.QtGui import QPageLayout, QPageSize
    type_map.update({'0.0f': 0.0, 
       '1.0f': 1.0, 
       'GL_COLOR_BUFFER_BIT': GL_COLOR_BUFFER_BIT, 
       'GL_NEAREST': GL_NEAREST, 
       'int32_t': int, 
       'QPixmap()': Default('PySide2.QtGui.QPixmap'), 
       'QPlatformSurface*': int, 
       'QVector< QTextLayout.FormatRange >()': [], 'uint32_t': int, 
       'uint8_t': int, 
       'USHRT_MAX': ushort_max})
    return locals()


def init_PySide2_QtWidgets():
    from PySide2.QtWidgets import QWidget, QMessageBox, QStyleOption, QStyleHintReturn, QStyleOptionComplex
    from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem
    type_map.update({'QMessageBox.StandardButtons(Yes | No)': Instance('QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No)'), 
       'QWidget.RenderFlags(DrawWindowBackground | DrawChildren)': Instance('QWidget.RenderFlags(QWidget.DrawWindowBackground | QWidget.DrawChildren)'), 
       'SH_Default': QStyleHintReturn.SH_Default, 
       'SO_Complex': QStyleOptionComplex.SO_Complex, 
       'SO_Default': QStyleOption.SO_Default, 
       'static_cast<Qt.MatchFlags>(Qt.MatchExactly|Qt.MatchCaseSensitive)': Instance('Qt.MatchFlags(Qt.MatchExactly | Qt.MatchCaseSensitive)'), 
       'Type': PySide2.QtWidgets.QListWidgetItem.Type})
    return locals()


def init_PySide2_QtSql():
    from PySide2.QtSql import QSqlDatabase
    type_map.update({'QLatin1String(defaultConnection)': QSqlDatabase.defaultConnection, 
       'QVariant.Invalid': Invalid('Variant')})
    return locals()


def init_PySide2_QtNetwork():
    best_structure = typing.OrderedDict if getattr(typing, 'OrderedDict', None) else typing.Dict
    type_map.update({'QMultiMap[PySide2.QtNetwork.QSsl.AlternativeNameEntryType, QString]': best_structure[(PySide2.QtNetwork.QSsl.AlternativeNameEntryType, typing.List[str])]})
    del best_structure
    return locals()


def init_PySide2_QtXmlPatterns():
    from PySide2.QtXmlPatterns import QXmlName
    type_map.update({'QXmlName.NamespaceCode': Missing('PySide2.QtXmlPatterns.QXmlName.NamespaceCode'), 
       'QXmlName.PrefixCode': Missing('PySide2.QtXmlPatterns.QXmlName.PrefixCode')})
    return locals()


def init_PySide2_QtMultimedia():
    import PySide2.QtMultimediaWidgets
    check_module(PySide2.QtMultimediaWidgets)
    type_map.update({'QGraphicsVideoItem': PySide2.QtMultimediaWidgets.QGraphicsVideoItem, 
       'qint64': int, 
       'QVideoWidget': PySide2.QtMultimediaWidgets.QVideoWidget})
    return locals()


def init_PySide2_QtOpenGL():
    type_map.update({'GLbitfield': int, 
       'GLenum': int, 
       'GLfloat': float, 
       'GLint': int, 
       'GLuint': int})
    return locals()


def init_PySide2_QtQml():
    type_map.update({'QJSValueList()': [], 'QVariantHash()': typing.Dict[(str, Variant)]})
    return locals()


def init_PySide2_QtQuick():
    type_map.update({'PySide2.QtQuick.QSharedPointer[PySide2.QtQuick.QQuickItemGrabResult]': PySide2.QtQuick.QQuickItemGrabResult, 
       'UnsignedShortType': int})
    return locals()


def init_PySide2_QtScript():
    type_map.update({'QScriptValueList()': []})
    return locals()


def init_PySide2_QtTest():
    type_map.update({'PySide2.QtTest.QTest.PySideQTouchEventSequence': PySide2.QtTest.QTest.QTouchEventSequence, 
       'PySide2.QtTest.QTouchEventSequence': PySide2.QtTest.QTest.QTouchEventSequence})
    return locals()


def init_PySide2_QtWinExtras():
    type_map.update({'QList< QWinJumpListItem* >()': []})
    return locals()


def init_PySide2_QtDataVisualization():
    from PySide2.QtDataVisualization import QtDataVisualization
    QtDataVisualization.QBarDataRow = typing.List[QtDataVisualization.QBarDataItem]
    QtDataVisualization.QBarDataArray = typing.List[QtDataVisualization.QBarDataRow]
    QtDataVisualization.QSurfaceDataRow = typing.List[QtDataVisualization.QSurfaceDataItem]
    QtDataVisualization.QSurfaceDataArray = typing.List[QtDataVisualization.QSurfaceDataRow]
    type_map.update({'100.0f': 100.0, 
       'QtDataVisualization.QBarDataArray': QtDataVisualization.QBarDataArray, 
       'QtDataVisualization.QBarDataArray*': QtDataVisualization.QBarDataArray, 
       'QtDataVisualization.QSurfaceDataArray': QtDataVisualization.QSurfaceDataArray, 
       'QtDataVisualization.QSurfaceDataArray*': QtDataVisualization.QSurfaceDataArray})
    return locals()


def init_testbinding():
    type_map.update({'testbinding.PySideCPP2.TestObjectWithoutNamespace': testbinding.TestObjectWithoutNamespace})
    return locals()