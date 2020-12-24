# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/max/core/viewport.py
# Compiled at: 2020-04-11 22:25:56
# Size of source mod 2**32: 629 bytes
from __future__ import print_function, division, absolute_import
import MaxPlus

def disable_redraw():
    """
    Disables redraw of 3ds Max viewports
    """
    MaxPlus.ViewportManager.DisableSceneRedraw()


def enable_redraw():
    """
    Enables redraw of 3ds Max viewports
    """
    MaxPlus.ViewportManager.EnableSceneRedraw()


def force_redraw():
    """
    Forces the redrawing of the viewports
    """
    MaxPlus.ViewportManager.RedrawViews(0)