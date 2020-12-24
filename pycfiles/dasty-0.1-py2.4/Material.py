# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/dasty/core/Material.py
# Compiled at: 2007-06-27 04:54:07
"""Define the Material class

Author: Jean-Christophe Hoelt <hoelt@irit.fr>
Copyright (c) 2007, IRIT-CNRS

This file is released under the CECILL-C licence.
"""

class Material(object):
    """Appearance of an entity"""
    __module__ = __name__

    def gl_bind(self):
        """Apply into the OpenGL context"""
        pass

    def gl_unbind(self):
        """Restore the OpenGL context to its previous state"""
        pass