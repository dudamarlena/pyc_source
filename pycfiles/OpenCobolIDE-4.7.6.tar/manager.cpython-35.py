# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/api/manager.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 1206 bytes
"""
This module contains the Manager API.

"""
import weakref

class Manager(object):
    __doc__ = '\n    A manager manages a specific aspect of a CodeEdit instance:\n        - backend management (start/stop server, request work,...)\n        - modes management\n        - panels management and drawing\n        - file manager\n\n    Managers are typically created internally when you create a CodeEdit.\n    You interact with them later, e.g. when you want to start the backend\n    process or when you want to install/retrieve a mode or a panel.\n\n    ::\n        editor = CodeEdit()\n\n        # use the backend manager to start the backend server\n        editor.backend.start(...)\n        editor.backend.send_request(...)\n\n        # use the panels controller to install a panel\n        editor.panels.install(MyPanel(), MyPanel.Position.Right)\n        my_panel = editor.panels.get(MyPanel)\n\n        # and so on\n\n    '

    @property
    def editor(self):
        """
        Return a reference to the parent code edit widget.
        """
        return self._editor()

    def __init__(self, editor):
        """
        :param editor: CodeEdit instance to control
        """
        self._editor = weakref.ref(editor)