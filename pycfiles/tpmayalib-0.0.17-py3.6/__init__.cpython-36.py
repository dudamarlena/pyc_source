# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/__init__.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 2310 bytes
"""
Initialization module for tpMayaLib
"""
from __future__ import print_function, division, absolute_import
try:
    import maya.cmds as cmds, maya.mel as mel, maya.utils as utils, maya.OpenMaya as OpenMaya, maya.OpenMayaUI as OpenMayaUI, maya.OpenMayaAnim as OpenMayaAnim, maya.OpenMayaRender as OpenMayaRender
except ImportError:
    pass

new_api = True
try:
    import maya.api.OpenMaya as OpenMayaV2, maya.api.OpenMayaUI as OpenMayaUIV2, maya.api.OpenMayaAnim as OpenMayaAnimV2, maya.api.OpenMayaRender as OpenMayaRenderV2
except Exception:
    new_api = False

try:
    api = {'OpenMaya':OpenMaya,  'OpenMayaUI':OpenMayaUI, 
     'OpenMayaAnim':OpenMayaAnim, 
     'OpenMayaRender':OpenMayaRender}
    if new_api:
        api2 = {'OpenMaya':OpenMayaV2,  'OpenMayaUI':OpenMayaUIV2, 
         'OpenMayaAnim':OpenMayaAnimV2, 
         'OpenMayaRender':OpenMayaRenderV2}
    else:
        api2 = api
    OpenMaya = OpenMaya
    OpenMayaUI = OpenMayaUI
    OpenMayaAnim = OpenMayaAnim
    OpenMayaRender = OpenMayaRender
except Exception:
    pass

def use_new_api(flag=False):
    """
    Enables new Maya API usage
    """
    global OpenMaya
    global OpenMayaAnim
    global OpenMayaUI
    if new_api:
        if flag:
            OpenMaya = api2['OpenMaya']
            OpenMayaUI = api2['OpenMayaUI']
            OpenMayaAnim = api2['OpenMayaAnim']
            OpenMayaRender = api2['OpenMayaRender']
        else:
            OpenMaya = api['OpenMaya']
            OpenMayaUI = api['OpenMayaUI']
            OpenMayaAnim = api['OpenMayaAnim']
            OpenMayaRender = api['OpenMayaRender']
    else:
        OpenMaya = api['OpenMaya']
        OpenMayaUI = api['OpenMayaUI']
        OpenMayaAnim = api['OpenMayaAnim']
        OpenMayaRender = api['OpenMayaRender']


def is_new_api():
    """
    Returns whether new Maya API is used or not
    :return: bool
    """
    return not OpenMaya == api['OpenMaya']