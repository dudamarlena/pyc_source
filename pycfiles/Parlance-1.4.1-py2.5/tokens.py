# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/parlance/tokens.py
# Compiled at: 2009-08-22 22:50:09
"""Parlance core language tokens
    Copyright (C) 2004-2008  Eric Wald
    
    This module is designed to be used as "from tokens import *".
    It includes all of the token from the core protocol, with upper-case
    names, including BRA ('(') and KET (')'), but not including provinces
    or powers from the standard map.
    
    Parlance may be used, modified, and/or redistributed under the terms of
    the Artistic License 2.0, as published by the Perl Foundation.
"""
from sys import modules
from language import protocol
__all__ = protocol.base_rep.keys()
module = modules[__name__]
for name in __all__:
    setattr(module, name, protocol.base_rep[name])