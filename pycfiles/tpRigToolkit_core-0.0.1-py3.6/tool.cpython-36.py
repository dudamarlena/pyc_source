# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpRigToolkit/core/tool.py
# Compiled at: 2020-02-05 21:34:07
# Size of source mod 2**32: 4263 bytes
"""
Module that contains core classes for tools
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import logging.config
from tpQtLib.core import base
import tpRigToolkit.register
LOGGER = logging.getLogger()

class ToolAttacher(object):
    Window = 0
    Dialog = 1


class Tool(base.BaseWidget, object):
    ATTACHER_TYPE = ToolAttacher.Window

    def __init__(self, config, parent=None):
        self._config = config
        self._attacher = None
        super(Tool, self).__init__(parent=parent)

    @property
    def config(self):
        return self._config

    def set_attacher(self, attacher):
        """
        Sets the attacher this tool will be linked to
        :param attacher:
        """
        self._attacher = attacher
        if attacher:
            self.post_attacher_set()

    def close_tool_attacher(self):
        """
        Closes tool attacher and the tool itself
        """
        if not self._attacher:
            self.close_tool()
        else:
            if self.ATTACHER_TYPE == ToolAttacher.Window:
                self._attacher.fade_close()
            else:
                if self.ATTACHER_TYPE == ToolAttacher.Dialog:
                    self._attacher.fade_close()
                else:
                    self.close_tool()

    def post_attacher_set(self):
        """
        Function that is called once an attacher has been set
        Override in child classes
        """
        pass

    def settings(self):
        """
        Returns settings of the attacher
        :return: QtSettings
        """
        if not self._attacher:
            return
        else:
            return self._attacher.settings()

    def save_settings(self):
        """
        Save settings of the attacher
        """
        if not self._attacher:
            return
        else:
            return self._attacher.save_settings()

    def register_callback(self, callback_type, fn):
        """
        Registers the given callback with the given function
        :param callback_type: tpDccLib.DccCallbacks
        :param fn: Python function to be called when callback is emitted
        """
        if not self._attacher or not hasattr(self._attacher, 'register_callback'):
            return
        else:
            return self._attacher.register_callback(callback_type, fn)

    def unregister_callbacks(self):
        """
        Unregisters all callbacks registered by this tool
        """
        if not self._attacher or not hasattr(self._attacher, 'unregister_callbacks'):
            return
        else:
            return self._attacher.unregister_callbacks()

    def show_ok_message(self, msg):
        """
        Shows an ok message in the attacher
        :param msg: str
        """
        if not self._attacher:
            return
        if not hasattr(self._attacher, 'show_ok_message'):
            LOGGER.warning('Tool Attacher for "{}" has no show_ok_message available!'.format(self.__class__.__name__))
        LOGGER.info(msg)
        self._attacher.show_ok_message(msg)

    def show_warning_message(self, msg):
        """
        Shows a warning message in the attacher
        :param msg: str
        """
        if not self._attacher:
            return
        if not hasattr(self._attacher, 'show_warning_message'):
            LOGGER.warning('Tool Attacher for "{}" has no show_warning_message available!'.format(self.__class__.__name__))
        LOGGER.warning(msg)
        self._attacher.show_warning_message(msg)

    def show_error_message(self, msg):
        """
        Shows an error message in the attacher
        :param msg: str
        """
        if not self._attacher:
            return
        if not hasattr(self._attacher, 'show_error_message'):
            LOGGER.warning('Tool Attacher f>or "{}" has no show_error_message available!'.format(self.__class__.__name__))
        LOGGER.error(msg)
        self._attacher.show_error_message(msg)

    def close_tool(self):
        """
        Close tool
        """
        self.unregister_callbacks()
        self.close()


tpRigToolkit.register.register_class('Tool', Tool)