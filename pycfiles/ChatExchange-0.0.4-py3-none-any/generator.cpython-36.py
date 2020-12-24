# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\generator.py
# Compiled at: 2019-04-01 22:07:20
# Size of source mod 2**32: 2902 bytes
from chatette_qiu.utils import print_DBG, remove_duplicates

class Generator(object):
    """Generator"""
    DEFAULT_MAX_NB_INTENT_EXAMPLES = 1000000000

    def __init__(self, parser):
        self.parser = parser
        self.max_nb_single_intent_examples = Generator.DEFAULT_MAX_NB_INTENT_EXAMPLES

    def set_max_nb_single_intent_examples(self, new_max):
        self.max_nb_single_intent_examples = new_max

    def generate_train(self):
        print_DBG('Generating training examples...')
        for intent_name in self.parser.intent_definitions:
            intent = self.parser.intent_definitions[intent_name]
            examples = intent.generate(self.max_nb_single_intent_examples)
            for example in examples:
                yield example

    def generate_test(self, training_examples=None):
        should_generate_test_set = False
        for intent_name in self.parser.intent_definitions:
            if self.parser.intent_definitions[intent_name].nb_testing_examples_asked is not None:
                should_generate_test_set = True
                break

        if should_generate_test_set:
            print_DBG('Generating testing examples...')
            for intent_name in self.parser.intent_definitions:
                intent = self.parser.intent_definitions[intent_name]
                examples = intent.generate(self.max_nb_single_intent_examples, training_examples)
                for example in examples:
                    yield example

    def get_entities_synonyms(self):
        """
        Makes a dict of all the synonyms of entities
        based on the slot value they are assigned.
        """
        synonyms = dict()
        for slot_definition in self.parser.slot_definitions:
            current_synonyms_dict = self.parser.slot_definitions[slot_definition].get_synonyms_dict()
            for slot_value in current_synonyms_dict:
                if slot_value not in synonyms:
                    synonyms[slot_value] = current_synonyms_dict[slot_value]
                else:
                    synonyms[slot_value].extend(current_synonyms_dict[slot_value])

        return remove_duplicates(synonyms)


if __name__ == '__main__':
    import warnings
    warnings.warn("You are running the wrong file ('generator.py')." + "The file that should be run is '__main__.py'.")