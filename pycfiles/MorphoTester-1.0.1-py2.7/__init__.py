# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/MorphoTester/__init__.py
# Compiled at: 2015-10-02 14:49:11
"""
Created on Oct 2, 2015

A scientific computing application for measuring topographic shape in 3D data.
To run MorphoTester, execute Morpho.py as a script. 

MorphoTester is licensed under the GPL license. See LICENSE.txt for further details. 

@author: Julia M. Winchester
"""
__version__ = '1.0'
__requires__ = [
 'Image', 'matplotlib', 'mayavi', 'numpy', 'PyQt4', 'scipy', 'sip', 'traits', 'traitsui', 'tvtk']
__all__ = [
 'Morpho', 'DNE', 'OPCR', 'RFI', 'implicitfair', 'normcore', 'plython', 'render']