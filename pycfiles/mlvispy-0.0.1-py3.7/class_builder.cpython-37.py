# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/jupyter_vis/class_builder.py
# Compiled at: 2019-07-23 18:45:11
# Size of source mod 2**32: 783 bytes
import sys
from jupyter_react import Component
current_module = sys.modules[__name__]

def init(self, **kwargs):
    (Component.__init__)(self, target_name='react.jupyter_vis', **kwargs)
    self.on_msg(self._handle_msg)


def _handle_msg(self, msg):
    print(msg)


components = [
 'AreaChart',
 'StackedCalendar',
 'GraphBuilder',
 'FeatureListView',
 'MultiWayPlot']
for component in components:
    setattr(current_module, component, type(component, (
     Component,), {'module':component, 
     '__init__':init, 
     '_handle_msg':_handle_msg}))