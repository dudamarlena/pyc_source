# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/shader.py
# Compiled at: 2020-05-02 23:38:23
# Size of source mod 2**32: 3539 bytes
"""
Module that contains functions and classes related with shaders
"""
from __future__ import print_function, division, absolute_import
import os
from Qt.QtWidgets import *
from Qt.QtGui import *
try:
    from shiboken import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

import tpDcc.dccs.maya as maya

def get_default_shaders():
    """
    Returns a list of default Maya shaders
    :return: list(str)
    """
    return [
     'particleCloud1', 'shaderGlow1', 'defaultColorMgtGlobals', 'lambert1']


def get_shading_group(geometry):
    """
    Get shading group assigned to the given geometry
    :param geometry: str, geometry to get shading group from
    :return: list<str>
    """
    sets = maya.cmds.listSets(extendToShape=True, type=1, object=geometry) or []
    return list(set(sets))


def set_shading_group(geometry, shading_group):
    """
    Sets shading group to the given geometry
    :param geometry: str, geometry to ste shading group to
    :param shading_group: str, shading group to set to geometry
    """
    maya.cmds.sets(geometry, edit=True, forceElement=shading_group)


def get_shading_node_type(shader_node):
    """
    Returns the type of shading node depending of the given shader node connections
    :param shader_node: str
    :return: str
    """
    connections = maya.cmds.listConnections(shader_node, source=False, destination=True) or list()
    if 'defaultTextureList1' in connections:
        return 'asTexture'
    if 'defaultShaderList1' in connections:
        return 'asShader'
    if 'defaultRenderUtilityList1' in connections:
        return 'asUtility'


def get_shader_swatch(shader_name, render_size=100, swatch_width=100, swatch_height=100):
    """
    Returns a Shader watch as QWidget
    :param shader_name: str
    :param render_size: int
    :param swatch_width: int
    :param swatch_height: int
    :return: QWidget
    """
    tempwin = maya.cmds.window()
    maya.cmds.columnLayout()
    swatch_port = maya.cmds.swatchDisplayPort(renderSize=render_size,
      widthHeight=(swatch_width, swatch_height),
      shadingNode=shader_name)
    if not swatch_port:
        return
    else:
        swatch_ptr = maya.OpenMayaUI.MQtUtil.findControl(swatch_port)
        swatch = wrapInstance(long(swatch_ptr), QWidget)
        return swatch


def export_shader_swatch_as_image(shader_name, export_path=None, render_size=100, swatch_width=100, swatch_height=100, format='png', get_pixmap=False):
    """
    Export shader swatch as image
    :param shader_name: str
    :param export_path: str
    :param render_size: int
    :param swatch_width: int
    :param swatch_height: int
    :param format: str
    :return: variant, None || str
    """
    swatch = get_shader_swatch(shader_name=shader_name,
      render_size=render_size,
      swatch_width=swatch_width,
      swatch_height=swatch_height)
    swatch_pixmap = QPixmap(swatch.size())
    swatch.render(swatch_pixmap)
    export_path = os.path.join(export_path, shader_name + '.' + format)
    swatch_pixmap.save(export_path)
    if get_pixmap:
        return swatch_pixmap
    if export_path is None:
        return
    else:
        if not os.path.exists(export_path):
            return
        export_path = os.path.join(export_path, shader_name + '.' + format)
        swatch_pixmap.save(export_path)
        return export_path