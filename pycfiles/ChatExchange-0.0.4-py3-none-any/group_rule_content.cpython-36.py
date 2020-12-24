# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\units\word\group_rule_content.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 4836 bytes
from random import randint
from chatette_qiu.units import Example, RuleContent, may_change_leading_case, may_get_leading_space, randomly_change_case, with_leading_lower, with_leading_upper
from chatette_qiu.parsing.parser_utils import add_escapement_back_in_group

class GroupWordRuleContent(RuleContent):
    """GroupWordRuleContent"""

    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None, casegen=False, randgen=None, percentage_gen=50, parser=None):
        if variation_name is not None:
            raise SyntaxError("Word groups cannot have variations, yet '" + name + "' does (unescaped '#'?)")
        else:
            if arg_value is not None:
                raise SyntaxError("Word groups cannot have an argument, yet '" + name + "' does (unescaped '$'?)")
            if parser is not None:
                raise RuntimeError('Internal error: tried to create a word ' + 'group with a pointer to the parser')
            casegen = may_change_leading_case(name) or False
        super(GroupWordRuleContent, self).__init__(name, leading_space=leading_space,
          variation_name=None,
          arg_value=None,
          casegen=casegen,
          randgen=randgen,
          percentage_gen=percentage_gen,
          parser=None)
        self.words = name

    def can_have_casegen(self):
        return may_change_leading_case(self.words)

    def generate_random(self, generated_randgens=None):
        if generated_randgens is None:
            generated_randgens = dict()
        elif self.randgen is not None:
            if self.randgen in generated_randgens:
                if generated_randgens[self.randgen]:
                    pass
                else:
                    return Example()
            elif self.randgen is not None:
                if randint(0, 99) >= self.percentgen:
                    generated_randgens[self.randgen] = False
                    return Example()
                generated_randgens[self.randgen] = True
        else:
            generated_str = self.words
            if self.casegen:
                generated_str = randomly_change_case(generated_str)
            if self.leading_space:
                if may_get_leading_space(generated_str):
                    generated_str = ' ' + generated_str
        return Example(generated_str)

    def generate_all(self):
        generated_examples = []
        if self.randgen is not None:
            generated_examples.append('')
        else:
            if self.casegen:
                generated_examples.append(with_leading_lower(self.words))
                generated_examples.append(with_leading_upper(self.words))
            else:
                generated_examples.append(self.words)
        if self.leading_space:
            for i, ex in enumerate(generated_examples):
                if may_get_leading_space(ex):
                    generated_examples[i] = ' ' + ex

        result = [Example(ex) for ex in generated_examples]
        return result

    def get_max_nb_generated_examples(self):
        nb_possible_ex = 1
        if self.casegen:
            nb_possible_ex *= 2
        if self.randgen is not None:
            nb_possible_ex += 1
        return nb_possible_ex

    def as_string(self):
        """
        Returns the representation of the rule
        as it would be written in a template file.
        """
        result = add_escapement_back_in_group(self.name)
        if self.casegen:
            result = '&' + result
        if self.variation_name is not None:
            result += '#' + self.variation_name
        if self.randgen is not None:
            result += '?' + str(self.randgen)
            if self.percentgen != 50:
                result += '/' + str(self.percentgen)
        if self.arg_value is not None:
            result += '$' + self.arg_value
        result = '[' + result + ']'
        if self.leading_space:
            result = ' ' + result
        return result