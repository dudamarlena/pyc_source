# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/componentized/components/joiner.py
# Compiled at: 2011-07-12 09:15:48
from pyf.componentized.components.base import Component

class DataJoiner(Component):
    strip_bypass = True

    def __init__(self, config_node):
        self.config_node = config_node

    @property
    def component(self):
        return self.launch