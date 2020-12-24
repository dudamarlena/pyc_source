# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/qdarkstyle/qdarkstyle/compile_qrc.py
# Compiled at: 2016-12-29 05:40:25
# Size of source mod 2**32: 2060 bytes
"""
Utility scripts to compile the qrc file. The script will
attempt to compile the qrc file using the following tools:
    - rcc
    - pyside-rcc
    - pyrcc4

Delete the compiled files that you don't want to use 
manually after running this script.
"""
import os

def compile_all():
    """
    Compile style.qrc using rcc, pyside-rcc and pyrcc4
    """
    print('Compiling for PyQt4: style.qrc -> pyqt_style_rc.py')
    os.system('pyrcc4 -py3 style.qrc -o pyqt_style_rc.py')
    print('Compiling for PyQt5: style.qrc -> pyqt5_style_rc.py')
    os.system('pyrcc5 style.qrc -o pyqt5_style_rc.py')
    print('Compiling for PySide: style.qrc -> pyside_style_rc.py')
    os.system('pyside-rcc -py3 style.qrc -o pyside_style_rc.py')


if __name__ == '__main__':
    compile_all()