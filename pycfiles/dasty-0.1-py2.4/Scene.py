# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/dasty/core/Scene.py
# Compiled at: 2007-06-27 04:54:07
"""Define the Primitive class

Author: Jean-Christophe Hoelt <hoelt@irit.fr>
Copyright (c) 2007, IRIT-CNRS

This file is released under the CECILL-C licence.
"""
from dasty.core.MMM import MMM

class Scene(MMM):
    """Objects and materials of the scene"""
    __module__ = __name__

    def __init__(self):
        MMM.__init__(self)

    def add_entity(self, entity):
        self.add_to_decomposition(entity)