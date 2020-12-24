# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\elements.py
# Compiled at: 2009-02-06 04:21:29
"""
    This file lists all of the basic grammar element classes.

    It is this file which is usually imported by end-user code which
    needs to use dragonfly grammar elements.
"""
import dragonfly.grammar.elements_basic as basic_, dragonfly.grammar.elements_compound as compound_
ElementBase = basic_.ElementBase
Sequence = basic_.Sequence
Alternative = basic_.Alternative
Optional = basic_.Optional
Repetition = basic_.Repetition
Literal = basic_.Literal
RuleRef = basic_.RuleRef
Rule = basic_.RuleRef
ListRef = basic_.ListRef
List = basic_.ListRef
DictListRef = basic_.DictListRef
DictList = basic_.DictListRef
Empty = basic_.Empty
Dictation = basic_.Dictation
Impossible = basic_.Impossible
Compound = compound_.Compound
Choice = compound_.Choice