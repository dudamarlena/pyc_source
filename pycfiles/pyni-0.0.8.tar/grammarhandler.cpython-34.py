# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/grammarhandler.py
# Compiled at: 2015-07-19 00:50:38
# Size of source mod 2**32: 4983 bytes
import os, re, inspect, sys
from pynhost import grammarbase, utilities, commands
from pynhost.platforms import platformhandler
try:
    from pynhost.grammars import _locals
except:
    _locals = None

class GrammarHandler:

    def __init__(self):
        self.global_grammars = []
        self.active_global_grammars = []
        self.local_grammars = {}
        self.active_local_grammars = {}
        self.all_grammars = []
        self.triggered = {'word': {'before': [],  'after': []},  'match': {'before': [],  'after': []},  'command': {'before': [],  'after': []}}
        try:
            self.process_contexts = _locals.GLOBAL_CONTEXTS
        except AttributeError:
            self.process_contexts = {}

    def load_grammars(self):
        grammar_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'grammars')
        for module in utilities.get_modules_in_dir(grammar_dir):
            self.load_grammars_from_module(module)

        self.set_active_grammars()
        for context in self.local_grammars:
            self.local_grammars[context].sort()

    def load_grammars_from_module(self, module):
        clsmembers = inspect.getmembers(sys.modules[module.__name__], inspect.isclass)
        for member in clsmembers:
            class_hierarchy = inspect.getmro(member[1])
            if len(class_hierarchy) > 2 and class_hierarchy[(-2)] == grammarbase.GrammarBase:
                grammar = self.initialize_grammar(member[1])
                app_pattern = grammar.app_context
                if grammar.app_context != '':
                    app_pattern = re.compile(grammar.app_context)
                    try:
                        self.local_grammars[app_pattern].append(grammar)
                    except KeyError:
                        self.local_grammars[app_pattern] = [
                         grammar]

                else:
                    self.global_grammars.append(grammar)
                    continue

    def set_active_grammars(self):
        try:
            self.active_global_grammars = utilities.filter_grammar_list(self.global_grammars, self.process_contexts)
        except KeyError:
            self.active_global_grammars = []

        self.active_local_grammars = {}
        for app_pattern, grammar_list in self.local_grammars.items():
            active_list = utilities.filter_grammar_list(grammar_list, self.process_contexts)
            self.active_local_grammars[app_pattern] = active_list + self.active_global_grammars
            self.active_local_grammars[app_pattern].sort()
            self.active_local_grammars[app_pattern].reverse()

    def get_matching_grammars(self):
        active_window_name = platformhandler.get_active_window_name().lower()
        grammars = []
        for app_pattern in self.active_local_grammars:
            if app_pattern.search(active_window_name):
                grammars.extend(self.active_local_grammars[app_pattern])
                continue

        grammars.sort()
        grammars.reverse()
        if grammars:
            return grammars
        return self.global_grammars

    def add_actions_to_recording_macros(self, action_list):
        contexts = self.get_contexts(action_list)
        for context in (c for c in contexts if c in self.local_grammars):
            for grammar in self.local_grammars[context]:
                self.add_actions_to_grammar_recording_macros(grammar, action_list)

    def add_actions_to_grammar_recording_macros(self, grammar, action_list):
        for name in grammar._recording_macros:
            for action in action_list.actions:
                if isinstance(action, str):
                    grammar._recording_macros[name].append(action)
                elif callable(action):
                    grammar._recording_macros[name].append(commands.CallableWrapper(action, action_list.matched_words))
                else:
                    grammar._recording_macros[name].append(action)

    def get_contexts(self, action_list):
        contexts = [
         '']
        if action_list.rule_match is None:
            context = platformhandler.get_active_window_name().lower()
            if context:
                contexts.append(context)
        elif action_list.rule_match.rule.grammar.app_context:
            contexts.append(action_list.rule_match.rule.grammar.app_context)
        return contexts

    def initialize_grammar(self, grammar_class):
        grammar = grammar_class()
        grammar._handler = self
        grammar.app_context = grammar.app_context.lower()
        grammar._set_rules()
        return grammar