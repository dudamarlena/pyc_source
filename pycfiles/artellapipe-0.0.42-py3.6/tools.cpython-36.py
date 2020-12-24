# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/managers/tools.py
# Compiled at: 2020-04-17 19:05:38
# Size of source mod 2**32: 1238 bytes
"""
Module that contains manager that handles Artella Tools
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import tpDcc
from tpDcc.libs.python import decorators
import artellapipe, artellapipe.register

class ArtellaToolsManager(object):

    def __init__(self):
        super(ArtellaToolsManager, self).__init__()

    def run_tool(self, tool_id, do_reload=False, debug=False, project=None, *args, **kwargs):
        """
        Launches artellapipe tool
        :param tool_id: str
        :param do_reload: bool
        :param debug: bool
        :param project: ArtellaProject or None
        """
        if not project:
            project = artellapipe.project
        return (tpDcc.ToolsMgr().launch_tool_by_id)(
 tool_id, *args, do_reload=do_reload, debug=debug, project=project, **kwargs)


@decorators.Singleton
class ArtellaToolsManagerSingleton(ArtellaToolsManager, object):

    def __init__(self):
        ArtellaToolsManager.__init__(self)


artellapipe.register.register_class('ToolsMgr', ArtellaToolsManagerSingleton)