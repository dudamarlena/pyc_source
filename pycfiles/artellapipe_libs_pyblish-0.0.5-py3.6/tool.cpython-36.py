# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/core/tool.py
# Compiled at: 2020-05-13 18:50:22
# Size of source mod 2**32: 4644 bytes
"""
Module that contains custom tool definition for Pyblish based tools
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import logging, pyblish.api, pyblish_lite, tpDcc as tp, artellapipe.register
LOGGER = logging.getLogger()

class ArtellaPyblishTool(artellapipe.ToolWidget, object):

    def __init__(self, project, config, settings, parent):
        self._pyblish_window = None
        self._registered_plugins = list()
        super(ArtellaPyblishTool, self).__init__(project=project, config=config, settings=settings, parent=parent)
        self._setup_host()
        pyblish_win = pyblish_lite.show()
        self.set_pyblish_window(pyblish_win)
        pyblish_win.setStyleSheet(pyblish_win.styleSheet() + '\n\n              #Header {\n              background: "#555";\n              border: 1px solid "#444";\n          }\n\n          #Header QRadioButton {\n              border-right: 1px solid #333;\n              left: 2px;\n          }\n\n          #Header QRadioButton::indicator {\n              width: 65px;\n              height: 40px;\n              border: 0px solid "transparent";\n              border-bottom: 3px solid "transparent";\n              background-repeat: no-repeat;\n              background-position: center center;\n          }\n\n          #Header QRadioButton::indicator:checked {\n              width: 65px;\n              height: 40px;\n              border: 0px solid "transparent";\n              border-bottom: 3px solid "transparent";\n              background-repeat: no-repeat;\n              background-position: center center;\n              image: none;\n          }\n\n          #Header QRadioButton:checked {\n              background-color: rgba(255, 255, 255, 20);\n              border-bottom: 3px solid "lightblue";\n          }\n\n          #Header QRadioButton::indicator:unchecked {\n              image: none;\n          }\n          ')
        self._register_plugins()

    def close_tool(self):
        self._deregister_plugins()
        super(ArtellaPyblishTool, self).close_tool()

    def set_pyblish_window(self, pyblish_window):
        """
        Sets the Pyblish window wrapped by this window
        :param pyblish_window:
        """
        if self._pyblish_window:
            return
        pyblish_window.controller.was_reset.connect(self._on_controller_reset)
        self.main_layout.addWidget(pyblish_window)
        self._pyblish_window = pyblish_window

    def register_plugin(self, plugin_class):
        """
        Registers given plugin path
        :param plugin_path: str
        """
        if not plugin_class or plugin_class in self._registered_plugins:
            return
        LOGGER.info('Registering Pyblish Plugin: {}'.format(plugin_class))
        pyblish.api.register_plugin(plugin_class)
        self._registered_plugins.append(plugin_class)

    def _setup_host(self):
        """
        Internal function that sets the host of the tool
        :return:
        """
        if tp.is_maya():
            pyblish.api.register_host('maya')
        elif tp.is_houdini():
            pyblish.api.register_host('houdini')

    def _register_plugins(self):
        """
        Internal function that registers current available plugins in project
        """
        plugins_to_register = self.config.get('pyblish_plugins', dict())
        if not plugins_to_register:
            LOGGER.warning('No Pyblish Plugins defined to load')
            return
        for plugin_name, plugin_attrs in plugins_to_register.items():
            plugin_class = artellapipe.PyblishMgr().get_plugin(plugin_name)
            if not plugin_class:
                LOGGER.warning('Impossible to load Pyblish Plugin: {}!'.format(plugin_name))
            else:
                if plugin_attrs:
                    for attr, value in plugin_attrs.items():
                        setattr(plugin_class, attr, value)

                self.register_plugin(plugin_class)

    def _deregister_plugins(self):
        """
        Internal function that deregister current registered plugin paths
        """
        for p in self._registered_plugins:
            pyblish.api.deregister_plugin(p)

    def _on_controller_reset(self):
        self._pyblish_window.controller.context.data['project'] = self._project


artellapipe.register.register_class('PyblishTool', ArtellaPyblishTool)