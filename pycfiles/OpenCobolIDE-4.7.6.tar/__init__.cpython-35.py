# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/qdarkstyle/qdarkstyle/__init__.py
# Compiled at: 2016-12-29 05:40:25
# Size of source mod 2**32: 3698 bytes
"""
Initialise the QDarkStyleSheet module when used with python.

This modules provides a function to transparently load the stylesheets
with the correct rc file.
"""
import logging, platform
__version__ = '2.3.0'

def _logger():
    return logging.getLogger('qdarkstyle')


def load_stylesheet(pyside=True):
    """
    Loads the stylesheet. Takes care of importing the rc module.

    :param pyside: True to load the pyside rc file, False to load the PyQt rc file

    :return the stylesheet string
    """
    if pyside:
        import qdarkstyle.pyside_style_rc
    else:
        import qdarkstyle.pyqt_style_rc
    if not pyside:
        from PyQt4.QtCore import QFile, QTextStream
    else:
        from PySide.QtCore import QFile, QTextStream
    f = QFile(':qdarkstyle/style.qss')
    if not f.exists():
        _logger().error('Unable to load stylesheet, file not found in resources')
        return ''
    else:
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()
        if platform.system().lower() == 'darwin':
            mac_fix = '\n            QDockWidget::title\n            {\n                background-color: #31363b;\n                text-align: center;\n                height: 12px;\n            }\n            '
            stylesheet += mac_fix
        return stylesheet


def load_stylesheet_pyqt5():
    """
    Loads the stylesheet for use in a pyqt5 application.

    :param pyside: True to load the pyside rc file, False to load the PyQt rc file

    :return the stylesheet string
    """
    import qdarkstyle.pyqt5_style_rc
    from PyQt5.QtCore import QFile, QTextStream
    f = QFile(':qdarkstyle/style.qss')
    if not f.exists():
        _logger().error('Unable to load stylesheet, file not found in resources')
        return ''
    else:
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()
        if platform.system().lower() == 'darwin':
            mac_fix = '\n            QDockWidget::title\n            {\n                background-color: #31363b;\n                text-align: center;\n                height: 12px;\n            }\n            '
            stylesheet += mac_fix
        return stylesheet