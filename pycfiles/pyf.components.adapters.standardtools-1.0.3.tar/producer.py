# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/componentized/components/producer.py
# Compiled at: 2011-02-05 06:39:28
from pyf.componentized.components.base import Component

class Producer(Component):

    def __init__(self, config_node, name):
        self.name = name
        self.config_node = config_node