# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\engines\recobs_natlink.py
# Compiled at: 2009-04-06 11:18:28
"""
Recognition observer class for the Natlink engine
============================================================================

"""
from .recobs_base import RecObsManagerBase
from ..grammar.grammar import Grammar
from ..grammar.rule_base import Rule
from ..grammar.elements import Impossible

class NatlinkRecObsManager(RecObsManagerBase):

    def __init__(self, engine):
        RecObsManagerBase.__init__(self, engine)
        self._grammar = None
        return

    def _activate(self):
        if not self._grammar:
            self._grammar = NatlinkRecObsGrammar(self)
        self._grammar.load()

    def _deactivate(self):
        if self._grammar:
            self._grammar.unload()
        self._grammar = None
        return


class NatlinkRecObsGrammar(Grammar):

    def __init__(self, manager):
        self._manager = manager
        name = '_recobs_grammar'
        Grammar.__init__(self, name, description=None, context=None)
        rule = Rule(element=Impossible(), exported=True)
        self.add_rule(rule)
        return

    def load(self):
        """ Load this grammar into its SR engine. """
        if self._loaded:
            return
        self._log_load.debug('Grammar %s: loading.' % self._name)
        self._engine.load_natlink_grammar(self, all_results=True)
        self._loaded = True
        self._in_context = False
        for rule in self._rules:
            if rule.active != False:
                rule.activate()

        for lst in self._lists:
            lst._update()

    def process_begin(self, executable, title, handle):
        self._manager.notify_begin()

    def process_results(self, words, result):
        if words == 'other':
            words = result.getWords(0)
            self._manager.notify_recognition(result, words)
        else:
            self._manager.notify_failure(result)
        return False