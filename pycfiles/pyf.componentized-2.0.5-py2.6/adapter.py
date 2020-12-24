# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/componentized/components/adapter.py
# Compiled at: 2011-02-05 06:39:28
from pyf.componentized.components.base import Component

class BaseAdapter(Component):

    def __init__(self, config_node, name):
        self.node_name = name
        self.config_node = config_node