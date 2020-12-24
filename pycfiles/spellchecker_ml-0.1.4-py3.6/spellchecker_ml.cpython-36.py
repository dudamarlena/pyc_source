# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spellchecker_ml/spellchecker_ml/spellchecker_ml.py
# Compiled at: 2019-05-05 21:39:59
# Size of source mod 2**32: 1478 bytes
from spellchecker import SpellChecker
import autocomplete, random

class SpellCheckerML:

    def __init__(self):
        self.spell_checker = SpellChecker()
        self.autocomplete = autocomplete
        self.autocomplete.load()

    def train(self, text, model_name=''):
        if model_name == '':
            self.autocomplete.models.train_models(text, model_name=False)
        else:
            self.autocomplete.models.train_models(text, model_name=model_name)
        self.autocomplete.load()

    def correction(self, previous_word, word):
        if self.spell_checker.known([word]):
            return word
        else:
            spell_checker_candidates = self.spell_checker.candidates(word)
            autocomplete_predictions = self.autocomplete.predict(previous_word, word[0])
            autocomplete_candidates = [elem[0] for elem in autocomplete_predictions]
            best_choices = []
            for candidate in spell_checker_candidates:
                try:
                    candidate_index = autocomplete_candidates.index(candidate)
                    best_choices.append(autocomplete_predictions[candidate_index])
                except:
                    continue

            if best_choices:
                best_choices = sorted(best_choices, key=(lambda t: t[1]))
                return list(best_choices[(-1)])[0]
            return random.choice(list(spell_checker_candidates))