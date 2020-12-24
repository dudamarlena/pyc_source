# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/api/mode.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 3662 bytes
"""
This module contains the editor extension API.
"""
import logging

def _logger():
    return logging.getLogger(__name__)


class Mode(object):
    __doc__ = '\n    Base class for editor extensions. An extension is a "thing" that can be\n    installed on an editor to add new behaviours or to modify its appearance.\n\n    A mode is added to an editor by using the ModesManager/PanelsManager:\n\n        - :meth:`pyqode.core.api.CodeEdit.modes.append` or\n        - :meth:`pyqode.core.api.CodeEdit.panels.append`\n\n    Subclasses may/should override the following methods:\n\n        - :meth:`pyqode.core.api.Mode.on_install`\n        - :meth:`pyqode.core.api.Mode.on_uninstall`\n        - :meth:`pyqode.core.api.Mode.on_state_changed`\n\n    ..warning: The mode will be identified by its class name, this means that\n    **there cannot be two modes of the same type on the same editor instance!**\n    '

    @property
    def editor(self):
        """
        Returns a reference to the parent editor widget.

        **READ ONLY**

        :rtype: pyqode.core.api.code_edit.CodeEdit
        """
        if self._editor is not None:
            return self._editor
        else:
            return

    @property
    def enabled(self):
        """
        Tells if the mode is enabled,
        :meth:`pyqode.core.api.Mode.on_state_changed` will be called as soon
        as the mode state changed.

        :type: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        if enabled != self._enabled:
            self._enabled = enabled
            self.on_state_changed(enabled)

    def __init__(self):
        self.name = self.__class__.__name__
        self.description = self.__doc__
        self._enabled = False
        self._editor = None
        self._on_close = False

    def __del__(self):
        _logger().log(5, '%s.__del__', type(self))

    def on_install(self, editor):
        """
        Installs the extension on the editor.

        :param editor: editor widget instance
        :type editor: pyqode.core.api.code_edit.CodeEdit

        .. note:: This method is called by editor when you install a Mode.
                  You should never call it yourself, even in a subclasss.

        .. warning:: Don't forget to call **super** when subclassing
        """
        self._editor = editor
        self.enabled = True

    def on_uninstall(self):
        """
        Uninstalls the mode from the editor.
        """
        self._on_close = True
        self.enabled = False
        self._editor = None

    def on_state_changed(self, state):
        """
        Called when the enable state has changed.

        This method does not do anything, you may override it if you need
        to connect/disconnect to the editor's signals (connect when state is
        true and disconnect when it is false).

        :param state: True = enabled, False = disabled
        :type state: bool
        """
        pass

    def clone_settings(self, original):
        """
        Clone the settings from another mode (same class).

        This method is called when splitting an editor widget.

        :param original: other mode (must be the same class).

        .. note:: The base method does not do anything, you must implement
            this method for every new mode/panel (if you plan on using the
            split feature). You should also make sure any properties will be
            propagated to the clones.
        """
        pass