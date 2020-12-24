# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/grammarbase.py
# Compiled at: 2015-07-19 00:43:49
# Size of source mod 2**32: 1382 bytes
from pynhost import ruleparser, dynamic

class GrammarBase:

    def __init__(self):
        self.mapping = {}
        self.app_context = ''
        self.settings = {'filtered words': [],  'priority': 0}
        self.context_filters = {}
        self._rules = []

    def __lt__(self, other):
        return self.settings['priority'] < other.settings['priority']

    def _change_global_context(self, context, value):
        self._handler.process_contexts[context] = value
        self._handler.set_active_grammars()

    def _begin_recording_macro(self, rule_name):
        self._recording_macros[rule_name] = []

    def _finish_recording_macros(self):
        new_rules = []
        for rule_name, macro in self._recording_macros.items():
            rule_name = '{} [<num>]'.format(rule_name)
            new_rules.append(ruleparser.Rule(rule_name, macro[:-1] + [dynamic.Num(-1).add(-1)], self))

        for rule in self._rules:
            if rule.raw_text not in [r.raw_text for r in new_rules]:
                new_rules.append(rule)
                continue

        self._rules = new_rules
        self._recording_macros = {}

    def _set_rules(self):
        for rule_text, actions in self.mapping.items():
            rule = ruleparser.Rule(rule_text, actions, self)
            self._rules.append(rule)