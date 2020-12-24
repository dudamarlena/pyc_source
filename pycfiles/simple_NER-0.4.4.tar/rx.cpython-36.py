# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/rules/rx.py
# Compiled at: 2020-04-12 15:14:53
# Size of source mod 2**32: 2124 bytes
import re
from simple_NER import Entity
from simple_NER.rules import Rule, RuleNER

class RegexNER(RuleNER):

    def __init__(self):
        super().__init__()
        self._rules = {}

    def _create_regex(self, rule):
        """ Create regex and return. If error occurs returns None. """
        return re.compile(rule, re.IGNORECASE)

    def extract_entities(self, query, as_json=False):
        for r in self._rules:
            for rule in self._rules[r]:
                for rul in rule.rules:
                    regex = self._create_regex(rul)
                    match = regex.findall(query)
                    for ent in match:
                        if not isinstance(ent, str):
                            ent = ent[0]
                        if as_json:
                            yield Entity(ent, (rule.name), source_text=query, rules=(self._rules[r])).as_json()
                        else:
                            yield Entity(ent, (rule.name), source_text=query, rules=(self._rules[r]))

    def add_entity_examples(self, name, examples):
        if isinstance(examples, str):
            examples = [
             examples]
        if name not in self._examples:
            self._examples[name] = []
        for e in examples:
            rules = '\\b' + e.lower() + '\\b'
            self._examples[name].append(Entity(e, name, rules=(Rule(name, rules))))

    def add_rule(self, name, rules):
        if isinstance(rules, str):
            rules = [
             rules]
        if name not in self._rules:
            self._rules[name] = []
        self._rules[name].append(Rule(name, rules))


if __name__ == '__main__':
    from pprint import pprint
    n = RegexNER()
    text = 'hello there'
    word = 'hello'
    rules = '(\\W*hello\\W*\\!?\\W*)'
    n.add_rule('greeting', rules)
    for e in n.extract_entities(text):
        pprint(e.as_json())

    n.add_entity_examples('person', ['bob', 'joe', 'amy'])
    text = 'hello amy'
    for e in n.entity_lookup(text):
        pprint(e.as_json())