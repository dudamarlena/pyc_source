# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\engines\compiler_base.py
# Compiled at: 2009-02-06 04:21:01
"""
    This file implements the compiler base class.
"""
import dragonfly.log as log_, dragonfly.grammar.elements as elements_

class CompilerError(Exception):
    pass


class CompilerBase(object):
    _log = log_.get_log('engine.compiler')
    element_compilers = [
     (
      elements_.Sequence, lambda s, e, *a, **k: s._compile_sequence(e, *a, **k)),
     (
      elements_.Alternative, lambda s, e, *a, **k: s._compile_alternative(e, *a, **k)),
     (
      elements_.Optional, lambda s, e, *a, **k: s._compile_optional(e, *a, **k)),
     (
      elements_.Literal, lambda s, e, *a, **k: s._compile_literal(e, *a, **k)),
     (
      elements_.RuleRef, lambda s, e, *a, **k: s._compile_rule_ref(e, *a, **k)),
     (
      elements_.ListRef, lambda s, e, *a, **k: s._compile_list_ref(e, *a, **k)),
     (
      elements_.Dictation, lambda s, e, *a, **k: s._compile_dictation(e, *a, **k)),
     (
      elements_.Impossible, lambda s, e, *a, **k: s._compile_impossible(e, *a, **k))]

    def __str__(self):
        return '%s()' % self.__class__.__name__

    def compile_grammar(self, grammar, *args, **kwargs):
        raise NotImplementedError('Compiler %s not implemented.' % self)

    def compile_element(self, element, *args, **kwargs):
        for (element_type, compiler) in self.element_compilers:
            if isinstance(element, element_type):
                compiler(self, element, *args, **kwargs)
                return

        raise NotImplementedError('Compiler %s not implemented for element type %s.' % (
         self, element))

    def _compile_unknown_element(self, element, *args, **kwargs):
        raise NotImplementedError('Compiler %s not implemented for element type %s.' % (
         self, element))

    _compile_sequence = _compile_unknown_element
    _compile_alternative = _compile_unknown_element
    _compile_optional = _compile_unknown_element
    _compile_literal = _compile_unknown_element
    _compile_rule_ref = _compile_unknown_element
    _compile_list_ref = _compile_unknown_element
    _compile_dictation = _compile_unknown_element
    _compile_impossible = _compile_unknown_element