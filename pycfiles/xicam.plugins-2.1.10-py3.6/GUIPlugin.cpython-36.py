# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\GUIPlugin.py
# Compiled at: 2018-05-17 15:54:05
# Size of source mod 2**32: 2261 bytes
from collections import OrderedDict
from enum import Enum
from typing import Dict, List
from xicam.core.data import NonDBHeader
from qtpy.QtGui import *
from yapsy.IPlugin import IPlugin

class GUIPlugin(IPlugin):
    __doc__ = '\n    GUIPlugins are left uninstanciated until all plugins are loaded so that all dependent widgets are loaded before\n    the UI is setup. They DO become singletons.\n    '
    isSingleton = False

    def __init__(self):
        super(GUIPlugin, self).__init__()
        self.stage = list(self.stages.values())[0]

    def appendHeader(self, header: NonDBHeader, **kwargs):
        pass

    def currentheader(self) -> Dict:
        raise NotImplementedError

    @property
    def headers(self) -> List[NonDBHeader]:
        return [self.headermodel.item(i) for i in range(self.headermodel.rowCount())]

    @property
    def stages(self) -> OrderedDict:
        return self._stages

    @stages.setter
    def stages(self, stages):
        self._stages = stages

    @property
    def exposedvars(self) -> Dict:
        raise NotImplementedError


class PanelState(Enum):
    Disabled = 1
    Defaulted = 2
    Customized = 3


class GUILayout(object):

    def __init__(self, center, left=PanelState.Defaulted, right=PanelState.Defaulted, bottom=PanelState.Defaulted, top=PanelState.Defaulted, lefttop=PanelState.Defaulted, righttop=PanelState.Defaulted, leftbottom=PanelState.Defaulted, rightbottom=PanelState.Defaulted):
        self.topwidget = top
        self.leftwidget = left
        self.rightwidget = right
        self.centerwidget = center
        self.bottomwidget = bottom
        self.lefttopwidget = lefttop
        self.righttopwidget = righttop
        self.leftbottomwidget = leftbottom
        self.rightbottomwidget = rightbottom

    def __getitem__(self, item: str):
        if not item.endswith('widget'):
            item += 'widget'
        return getattr(self, item, PanelState.Defaulted)