# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/sdk/VaiInterface.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 314 bytes
from ..EditorApp import EditorApp
from vai.lexer import token as lexertoken
from vaitk import gui

def application():
    """
    Returns the Vai application.
    """
    return EditorApp.vApp


def statusBar():
    """
    Returns the application's status bar.
    """
    return application().editor.status_bar