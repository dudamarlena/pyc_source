# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/psycoptima.py
# Compiled at: 2009-06-08 07:12:47
"""Bindings to Psyco optimizer."""
import types
from pkg_resources import Requirement, working_set
working_set.resolve([Requirement.parse('psyco>=1.5')])
try:
    import psyco
except:
    raise

import core, varios, globs, basic, logic
for class_ in (
 core.Node,
 core.Synaps,
 varios.VariositiedSynaps,
 globs.Glob,
 basic.GeneralizedNeuron,
 basic.InputMemory,
 basic.OutputMemory,
 basic.AssociativeMemory,
 logic.ComparisionSelect,
 logic.ComparisionBoolean,
 logic.BooleanOperation):
    class_.__metaclass__ = psyco.compacttype