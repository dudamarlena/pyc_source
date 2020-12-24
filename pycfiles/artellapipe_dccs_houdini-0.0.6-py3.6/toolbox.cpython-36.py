# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/dccs/houdini/core/toolbox.py
# Compiled at: 2019-12-20 20:47:38
# Size of source mod 2**32: 422 bytes
import tpDccLib as tp, artellapipe.register
from artellapipe.core import toolbox

class HoudiniToolBox(toolbox.ToolBox, object):

    def __init__(self, project, parent=None):
        if parent is None:
            parent = tp.Dcc.get_main_window()
        super(HoudiniToolBox, self).__init__(project=project, parent=parent)


if tp.is_houdini():
    artellapipe.register.register_class('ToolBox', HoudiniToolBox)