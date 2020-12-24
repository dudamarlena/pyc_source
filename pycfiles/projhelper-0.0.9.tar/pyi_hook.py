# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\xqt\pyi_hook.py
# Compiled at: 2013-11-18 18:23:08
__doc__ = ' Defines the hook required for the PyInstaller to use xqt with it. '
__authors__ = [
 'Eric Hulser']
__author__ = (',').join(__authors__)
__credits__ = []
__copyright__ = 'Copyright (c) 2011, Projex Software'
__license__ = 'LGPL'
__maintainer__ = 'Projex Software'
__email__ = 'team@projexsoftware.com'
__all__ = [
 'hiddenimports', 'datas']
import os, projex.pyi
hiddenimports, datas = projex.pyi.collect(os.path.dirname(__file__))
wrapper = os.environ.get('XQT_WRAPPER', 'PyQt4')
if wrapper == 'PySide':
    hiddenimports += ['PySide.QtUiTools', 'PySide.QtXml', 'PySide.QtWebKit']
    try:
        hiddenimports.remove('xqt.pyqt4_wrapper')
    except ValueError:
        pass

elif wrapper == 'PyQt4':
    hiddenimports += ['PyQt4.QtUiTools', 'PyQt4.QtXml', 'PyQt4.QtWebKit']
    try:
        hiddenimports.remove('xqt.pyside_wrapper')
    except ValueError:
        pass