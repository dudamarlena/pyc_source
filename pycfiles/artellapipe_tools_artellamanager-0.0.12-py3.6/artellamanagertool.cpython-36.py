# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/artellamanager/widgets/artellamanagertool.py
# Compiled at: 2020-05-13 18:51:46
# Size of source mod 2**32: 852 bytes
"""
Tool that allow artists to work with Artella local and server files
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import artellapipe
from artellapipe.tools.artellamanager.widgets import artellamanagerwidget

class ArtellaManager(artellapipe.ToolWidget, object):

    def __init__(self, project, config, settings, parent):
        super(ArtellaManager, self).__init__(project=project, config=config, settings=settings, parent=parent)

    def ui(self):
        super(ArtellaManager, self).ui()
        self._artellamanager_widget = artellamanagerwidget.ArtellaManagerWidget(project=(self._project))
        self.main_layout.addWidget(self._artellamanager_widget)