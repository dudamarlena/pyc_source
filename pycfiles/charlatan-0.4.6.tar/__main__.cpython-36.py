# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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