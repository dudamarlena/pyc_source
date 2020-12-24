# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\xqt\__init__.py
# Compiled at: 2013-11-21 14:58:08
__doc__ = '\nThe xqt library is a simple wrapper system on top of the various bindings\nthat Qt has for Python.  This provides a way to consolidate the differences\nbetween things like PyQt4, PyQt5, and PySide in a way that will allow Python\ndevelopers to build tools and libraries that are able to work with any of the\nwrapper systems.\n'
__authors__ = [
 'Eric Hulser']
__author__ = (',').join(__authors__)
__credits__ = []
__copyright__ = 'Copyright (c) 2012, Projex Software'
__license__ = 'LGPL'
__maintainer__ = 'Projex Software'
__email__ = 'team@projexsoftware.com'
__major__ = 1
__minor__ = 1
try:
    from __revision__ import __revision__
except:
    __revision__ = 0

__version_info__ = (__major__, __minor__, __revision__)
__version__ = '%s.%s' % (__major__, __minor__)
__all__ = [
 'uic',
 'wrapVariant',
 'unwrapVariant',
 'PyObject',
 'QtCore',
 'QtGui',
 'QtXml',
 'Qsci',
 'QtWebKit',
 'QtDesigner',
 'QtNetwork',
 'Signal',
 'Slot',
 'Property',
 'QStringList']
import logging, os, sys
logger = logging.getLogger(__name__)
QT_WRAPPER = os.environ.get('XQT_WRAPPER', 'PyQt4')
package = 'xqt.%s_wrapper' % QT_WRAPPER.lower()
__import__(package)
glbls = globals()
for name in __all__:
    glbls[name] = None

def wrapVariant(variant):
    if hasattr(QtCore, 'QVariant'):
        return QtCore.QVariant(variant)
    return variant


def unwrapVariant(variant, default=None):
    if type(variant).__name__ == 'QVariant':
        if not variant.isNull():
            return variant.toPyObject()
        return default
    if variant is None:
        return default
    else:
        return variant


def wrapNone(value):
    """
    Handles any custom wrapping that needs to happen for Qt to process
    None values properly (PySide issue)
    
    :param      value | <variant>
    
    :return     <variant>
    """
    return value


def unwrapNone(value):
    """
    Handles any custom wrapping that needs to happen for Qt to process
    None values properly (PySide issue)
    
    :param      value | <variant>
    
    :return     <variant>
    """
    return value


if package:
    sys.modules[package].createMap(globals())
    sys.modules['xqt.QtCore'] = QtCore
    sys.modules['xqt.QtDesigner'] = QtDesigner
    sys.modules['xqt.QtGui'] = QtGui
    sys.modules['xqt.Qsci'] = Qsci
    sys.modules['xqt.QtWebKit'] = QtWebKit
    sys.modules['xqt.QtNetwork'] = QtNetwork
    sys.modules['xqt.QtXml'] = QtXml