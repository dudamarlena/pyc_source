# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpRigToolkit/widgets/dialog.py
# Compiled at: 2020-02-05 21:34:07
# Size of source mod 2**32: 2212 bytes
"""
Base wrapper classes to create DCC dialogs
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import tpQtLib, tpRigToolkit
from tpRigToolkit.core import resource

class MainDialog(tpQtLib.Dialog, object):

    def __init__(self, tool=None, name='MainDialog', title='MainDialog', show_dragger=True, size=(200, 125), fixed_size=False, parent=None):
        self._tool = tool
        super(MainDialog, self).__init__(name=name,
          title=title,
          parent=parent,
          show_dragger=show_dragger,
          size=size,
          fixed_size=fixed_size)

    def ui(self):
        super(MainDialog, self).ui()
        dialog_icon = self._get_icon()
        self.setWindowIcon(dialog_icon)
        if self._tool:
            self.main_layout.addWidget(self._tool)

    def setWindowTitle(self, title):
        super(MainDialog, self).setWindowTitle(title)

    def _get_icon(self):
        """
        Internal function that returns the icon used for the window
        :return: QIcon
        """
        if self._project:
            window_icon = self._project.icon
            if not window_icon.isNull():
                return window_icon
            self._project.logger.warning('{} Project Icon not found: {}!'.format(self._project.name.title(), self._project.icon_name + '.png'))
        return resource.ResourceManager().icon('artella')


tpRigToolkit.register.register_class('Dialog', MainDialog)