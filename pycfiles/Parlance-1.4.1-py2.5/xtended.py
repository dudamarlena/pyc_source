# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/parlance/xtended.py
# Compiled at: 2009-08-22 22:50:09
"""Parlance standard map environment
    Copyright (C) 2004-2008  Eric Wald
    
    This module includes the standard map, default map tokens, and starting
    position messages. It can take a few seconds to load, and might not work
    properly, but offers a convenient way to import all those names.
    
    Parlance may be used, modified, and/or redistributed under the terms of
    the Artistic License 2.0, as published by the Perl Foundation.
"""
from sys import modules
from gameboard import Map, Variant
from language import protocol
standard = Variant('standard', filename='parlance://data/standard.cfg')
__all__ = [
 'standard', 'standard_map', 'standard_sco', 'standard_now',
 'default_rep', 'base_rep']
standard_map = Map(standard)
standard_sco = standard.sco()
standard_now = standard.now()
default_rep = protocol.default_rep
base_rep = protocol.base_rep
module = modules[__name__]
for (name, token) in default_rep.items():
    setattr(module, name, token)

__all__.extend(default_rep.keys())