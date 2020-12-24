# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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