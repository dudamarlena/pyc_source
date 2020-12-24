# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/qtutils.py
# Compiled at: 2020-04-24 23:10:50
# Size of source mod 2**32: 1953 bytes
"""
Module that contains utils functions to work with Qt in Maya
"""
import sys
from Qt.QtCore import *
from Qt.QtWidgets import *
import tpDcc.dccs.maya as maya
from tpDcc.libs.qt.core import qtutils as qt
from tpDcc.dccs.maya.core import gui
if sys.version_info > (3, ):
    long = int

def add_widget_to_maya_layout(widget):
    """
    Adds given QWidget to maya layout
    :param widget: QWidget
    """
    parent = maya.OpenMayaUI.MQtUtil.getCurrentParent()
    mixin_ptr = maya.OpenMayaUI.MQtUtil.findControl(widget.objectName())
    maya.OpenMayaUI.MQtUtil.addWidgetToMayaLayout(long(mixin_ptr), long(parent))
    return True


def dock_widget(widget, label, retain=False, show=True):
    """
    Creates an instance of the class and dock into Maya UI
    :param widget_class:
    """
    workspace_control = widget.objectName() + '_workspace_control'
    initial_width = maya.cmds.optionVar(query='workspacesWidePanelInitialWidth') * 0.75
    try:
        maya.cmds.deleteUI(workspace_control)
        maya.cmds.workspaceControlState(workspace_control, remove=True)
        maya.debug('Removing workspace {0}'.format(workspace_control))
    except Exception:
        pass

    if gui.get_maya_api_version() >= 201700:
        main_control = maya.cmds.workspaceControl(workspace_control,
          ttc=['AttributeEditor', -1], iw=25, mw=False, wp='free',
          label=label,
          retain=retain)
        control_widget = maya.OpenMayaUI.MQtUtil.findControl(workspace_control)
        control_wrap = qt.wrapinstance(long(control_widget), QWidget)
        control_wrap.setAttribute(Qt.WA_DeleteOnClose)
        widget.setParent(control_wrap)
        control_wrap.layout().addWidget(widget)
        if show:
            maya.cmds.evalDeferred(lambda *args: maya.cmds.workspaceControl(main_control, e=True, rs=True, fl=True))
    else:
        control_wrap = None
    return control_wrap