# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ekas/dev/jedhy/jedhy/api.hy
# Compiled at: 2019-06-05 17:01:12
# Size of source mod 2**32: 1669 bytes
"""Expose jedhy's `API` for IDE and metaprogramming use-cases."""
import hy.macros
hy.macros.require('jedhy.macros', None, assignments='ALL', prefix='')
from jedhy.macros import *
from jedhy.inspection import Inspect
from jedhy.models import Candidate, Namespace, Prefix

class API(object):

    def __init__(self, globals_=None, locals_=None, macros_=None):
        self.set_namespace(globals_, locals_, macros_)
        self._cached_prefix = None
        return None

    def set_namespace(self, globals_=None, locals_=None, macros_=None):
        """Rebuild namespace for possibly given `globals-`, `locals-`, and `macros-`.

Typically, the values passed are:
  globals- -> (globals)
  locals-  -> (locals)
  macros-  -> --macros--"""
        self.namespace = Namespace(globals_, locals_, macros_)

    def complete(self, prefix_str):
        """Completions for a prefix string."""
        cached_prefix, prefix = [
         self._cached_prefix,
         Prefix(prefix_str, namespace=(self.namespace))]
        self._cached_prefix = prefix
        return prefix.complete(cached_prefix=cached_prefix)

    def annotate(self, candidate_str):
        """Annotate a candidate string."""
        return Candidate(candidate_str, namespace=(self.namespace)).annotate()

    def _inspect(self, candidate_str):
        """Inspect a candidate string."""
        return Inspect(Candidate(candidate_str, namespace=(self.namespace)).get_obj())

    def docs(self, candidate_str):
        """Docstring for a candidate string."""
        return self._inspect(candidate_str).docs()

    def full_docs(self, candidate_str):
        """Full documentation for a candidate string."""
        return self._inspect(candidate_str).full_docs()