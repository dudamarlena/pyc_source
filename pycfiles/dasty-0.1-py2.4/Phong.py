# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/dasty/material/Phong.py
# Compiled at: 2007-06-27 04:54:07
"""Define the Phong material class.

Author: Jean-Christophe Hoelt <hoelt@irit.fr>
Copyright (c) 2007, IRIT-CNRS

This file is released under the CECILL-C licence.
"""
import dasty.core

class Phong(dasty.core.Material):
    """Phong material.

    Attributes are:
    diffuse_color -- list of 4 floats (red, green, blue, alpha)
    specular_color -- list of 4 floats (red, green, blue, alpha)
    specular_exponent -- 1 float
    """
    __module__ = __name__

    def __init__(self):
        dasty.core.Material.__init__(self)
        self.diffuse_color = (0.0, 0.0, 0.0, 1.0)
        self.specular_color = (0.0, 0.0, 0.0, 1.0)
        self.specular_exponent = 16.0