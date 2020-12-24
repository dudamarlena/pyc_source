# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\compiler.py
# Compiled at: 2008-11-19 12:15:14
"""
    This file implements Dragonfly's grammar compiler which turns
    dragonfly rules and elements into NaturallySpeaking's
    binary grammar format.
"""
import struct

class GrammarError(Exception):
    pass


class Compiler(object):
    _start_type = 1
    _end_type = 2
    _word_type = 3
    _rule_type = 4
    _list_type = 6
    _seq_value = 1
    _alt_value = 2
    _rep_value = 3
    _opt_value = 4

    def __init__(self):
        self._words = []
        self._lists = []
        self._rules = []
        self._import_rules = []
        self._export_rules = []
        self._rule_definitions = {}
        self._current_rule_name = None
        self._current_rule_export = None
        self._current_rule_definition = None
        return

    def start_rule_definition(self, name, exported=False):
        """start defining a rule."""
        if self._current_rule_name:
            raise GrammarError('Cannot start defining a rule whilea different rule is already being defined.')
        assert isinstance(name, str), 'The rule name must be a string.'
        self._current_rule_name = name
        self._current_rule_export = exported
        self._current_rule_definition = []

    def end_rule_definition(self):
        """End defining a rule."""
        if not self._current_rule_name:
            raise GrammarError('Cannot end defining a rule when no rule is being defined.')
        if self._current_rule_name in self._rule_definitions:
            raise GrammarError("Rule '%s' defined more than once." % self._current_rule_name)
        if self._current_rule_name not in self._rules:
            self._rules.append(self._current_rule_name)
        if self._current_rule_export:
            self._export_rules.append(self._current_rule_name)
        self._rule_definitions[self._current_rule_name] = self._current_rule_definition
        self._current_rule_name = None
        self._current_rule_export = None
        self._current_rule_definition = None
        return

    def start_sequence(self):
        """start a sequence structure in the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError('Cannot start a sequence because no rule is currently being defined.')
        self._current_rule_definition.append((
         self._start_type, self._seq_value))

    def end_sequence(self):
        """End a sequence structure in the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError('Cannot end a sequence because no rule is currently being defined.')
        self._current_rule_definition.append((
         self._end_type, self._seq_value))

    def start_alternative(self):
        """start an alternative structure in the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError('Cannot start an alternative because no rule is currently being defined.')
        self._current_rule_definition.append((
         self._start_type, self._alt_value))

    def end_alternative(self):
        """End an alternative structure in the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError('Cannot end an alternative because no rule is currently being defined.')
        self._current_rule_definition.append((
         self._end_type, self._alt_value))

    def start_repetition(self):
        """start a repetition structure in the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError('Cannot start a repetition because no rule is currently being defined.')
        self._current_rule_definition.append((
         self._start_type, self._rep_value))

    def end_repetition(self):
        """End a repetition structure in the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError('Cannot end a repetition because no rule is currently being defined.')
        self._current_rule_definition.append((
         self._end_type, self._rep_value))

    def start_optional(self):
        """start a optional structure in the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError('Cannot start a optional because no rule is currently being defined.')
        self._current_rule_definition.append((
         self._start_type, self._opt_value))

    def end_optional(self):
        """End a optional structure in the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError('Cannot end a optional because no rule is currently being defined.')
        self._current_rule_definition.append((
         self._end_type, self._opt_value))

    def add_word(self, word):
        """Append a literal word to the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError("Cannot add word '%s' because no rule is currently being defined." % word)
        if word not in self._words:
            self._words.append(word)
            id = len(self._words)
        else:
            id = self._words.index(word) + 1
        self._current_rule_definition.append((self._word_type, id))

    def add_list(self, list):
        """Append a list to the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError("Cannot add list '%s' because no rule is currently being defined." % list)
        if list not in self._lists:
            self._lists.append(list)
            id = len(self._lists)
        else:
            id = self._lists.index(list) + 1
        self._current_rule_definition.append((self._list_type, id))

    def add_rule(self, rule, imported=False):
        """Append a rule reference to the rule currently being defined."""
        if not self._current_rule_name:
            raise GrammarError("Cannot add rule '%s' because no rule is currently being defined." % rule)
        if rule not in self._rules:
            self._rules.append(rule)
            if imported:
                self._import_rules.append(rule)
            id = len(self._rules)
        elif imported != (rule in self._import_rules):
            raise GrammarError("Rule '%s' cannot be referenced as both imported and not imported within a grammar." % rule)
        else:
            id = self._rules.index(rule) + 1
        self._current_rule_definition.append((self._rule_type, id))

    def compile(self):
        """Compile a binary grammar of this compiler's current state."""
        if self._current_rule_name:
            raise GrammarError('Cannot compile grammar while a rule is being defined.')
        output = [
         struct.pack('LL', 0, 0)]
        output.append(self._compile_id_chunk(4, self._export_rules, self._rules))
        output.append(self._compile_id_chunk(5, self._import_rules, self._rules))
        output.append(self._compile_id_chunk(6, self._lists, self._lists))
        output.append(self._compile_id_chunk(2, self._words, self._words))
        output.append(self._compile_rule_chunk(3))
        return ('').join(output)

    def _compile_id_chunk(self, chunk_id, subset, ordered_superset):
        elements = []
        for (name, id) in zip(ordered_superset, xrange(1, len(ordered_superset) + 1)):
            if name not in subset:
                continue
            padded_len = len(name) + 4 & -4
            element = struct.pack('LL%ds' % padded_len, padded_len + 8, id, name)
            elements.append(element)

        element_data = ('').join(elements)
        header = struct.pack('LL', chunk_id, len(element_data))
        return header + element_data

    def _compile_rule_chunk(self, chunk_id):
        definitions = []
        for (name, id) in zip(self._rules, xrange(1, len(self._rules) + 1)):
            if name in self._import_rules:
                if name in self._rule_definitions:
                    raise GrammarError("Rule '%s' cannot be both imported and defined in a grammar" % name)
                continue
            if name not in self._rule_definitions:
                raise GrammarError("Rule '%s' is neither imported nor defined" % name)
            elements = []
            for (t, v) in self._rule_definitions[name]:
                element = struct.pack('HHL', t, 0, v)
                elements.append(element)

            definition_size = 8 + sum([ len(s) for s in elements ])
            definition = struct.pack('LL', definition_size, id)
            definition += ('').join(elements)
            definitions.append(definition)

        definition_data = ('').join(definitions)
        header = struct.pack('LL', chunk_id, len(definition_data))
        return header + definition_data

    def _get_rule_names(self):
        return tuple([None] + self._rules)

    rule_names = property(_get_rule_names, doc='Read-only access to the list of rule names.')

    def debug_state_string(self):
        """Debug."""
        import textwrap
        wrapper = textwrap.TextWrapper(subsequent_indent='   ')
        output = []
        wrapper.initial_indent = 'exported rules: '
        output.append(wrapper.wrap((', ').join(self._export_rules)))
        wrapper.initial_indent = 'imported rules: '
        output.append(wrapper.wrap((', ').join(self._import_rules)))
        wrapper.initial_indent = 'lists: '
        output.append(wrapper.wrap((', ').join(self._lists)))
        wrapper.initial_indent = 'words: '
        output.append(wrapper.wrap((', ').join(self._words)))
        wrapper.initial_indent = 'rule definitions: '
        output.append(wrapper.wrap(str(self._rule_definitions)))
        return ('\n').join([ ('\n').join(lines) for lines in output if lines ])