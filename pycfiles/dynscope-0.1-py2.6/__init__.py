# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/dynscope/__init__.py
# Compiled at: 2010-12-16 12:19:12
"""
This module provides the basic interface to work with dynamically
scoped variables. It provides the following functions for that:

construct() returns a dynamic scope object and a function to introduce
local dynamic bindings.

fluid is the default dynamic scope set up ready to use.

flet(**kw) is the function to introduce local bindings on fluid. It
returns a context manager that is used in combination with the with
statement and will handle unwinding of dynamic namespaces.
"""
__version__ = '0.1'
from fluids import DynamicScope
__all__ = [
 'fluid', 'flet', 'construct']
construct = DynamicScope._construct
(fluid, flet) = construct()