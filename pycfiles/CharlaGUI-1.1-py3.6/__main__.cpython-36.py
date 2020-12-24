# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/charlagui/__main__.py
# Compiled at: 2019-09-11 13:45:07
# Size of source mod 2**32: 154 bytes
from charlagui.gui import GUI

def start():
    gui = GUI()
    gui.load_menu()


if __name__ == '__main__':
    gui = GUI()
    gui.load_menu()
    exit()