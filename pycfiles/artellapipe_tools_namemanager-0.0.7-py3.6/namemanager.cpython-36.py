# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/namemanager/widgets/namemanager.py
# Compiled at: 2020-03-13 14:10:39
# Size of source mod 2**32: 1942 bytes
"""
Tool that allow to define the nomenclature of the pipeline files
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from tpDcc.tools.nameit.widgets import nameit
import artellapipe
from artellapipe.libs import naming
from artellapipe.libs.naming.core import naminglib

class NameWidget(nameit.NameIt, object):
    NAMING_LIB = naminglib.ArtellaNameLib

    def __init__(self, project, parent=None):
        self._project = project
        super(NameWidget, self).__init__(data_file=(naming.config.get_path()), parent=parent)

    def _on_open_renamer_tool(self):
        """
        Overrides nameit.NameIt _on_open_renamer_tool
        Internal function that is used by toolbar to open Renamer Tool
        """
        try:
            artellapipe.ToolsMgr().run_tool('artellapipe-tools-renamer', do_reload=False)
        except Exception:
            artellapipe.logger.warning('tpDcc-tools-renamer is not available!')
            return

    def _is_renamer_tool_available(self):
        """
        Overrides nameit.NameIt _is_renamer_tool_available
        Returns whether or not tpRenamer tool is available or not
        :return: bool
        """
        try:
            import artellapipe.tools.renamer
        except Exception:
            return False
        else:
            return True


class NameManager(artellapipe.ToolWidget, object):

    def __init__(self, project, config, settings, parent):
        super(NameManager, self).__init__(project=project, config=config, settings=settings, parent=parent)

    def ui(self):
        super(NameManager, self).ui()
        self._name_widget = NameWidget(project=(self._project))
        self.main_layout.addWidget(self._name_widget)

    @property
    def nameit(self):
        return self._name_widget