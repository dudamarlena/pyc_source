# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simplebayes/__init__.py
# Compiled at: 2015-04-21 21:09:52
"""
The MIT License (MIT)

Copyright (c) 2015 Ryan Vennell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from simplebayes.categories import BayesCategories
import pickle, os

class SimpleBayes(object):
    """A memory-based, optional-persistence naïve bayesian text classifier."""
    cache_file = '_simplebayes.pickle'

    def __init__(self, tokenizer=None, cache_path='/tmp/'):
        """
        :param tokenizer: A tokenizer override
        :type tokenizer: function (optional)
        :param cache_path: path to data storage
        :type cache_path: str
        """
        self.categories = BayesCategories()
        self.tokenizer = tokenizer or SimpleBayes.tokenize_text
        self.cache_path = cache_path
        self.probabilities = {}

    @classmethod
    def tokenize_text(cls, text):
        """
        Default tokenize method; can be overridden

        :param text: the text we want to tokenize
        :type text: str
        :return: list of tokenized text
        :rtype: list
        """
        return [ w for w in text.split() if len(w) > 2 ]

    @classmethod
    def count_token_occurrences(cls, words):
        """
        Creates a key/value set of word/count for a given sample of text

        :param words: full list of all tokens, non-unique
        :type words: list
        :return: key/value pairs of words and their counts in the list
        :rtype: dict
        """
        counts = {}
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        return counts

    def flush(self):
        """
        Deletes all tokens & categories
        """
        self.categories = BayesCategories()

    def calculate_category_probability(self):
        """
        Caches the individual probabilities for each category
        """
        total_tally = 0.0
        probs = {}
        for category, bayes_category in self.categories.get_categories().items():
            count = bayes_category.get_tally()
            total_tally += count
            probs[category] = count

        for category, count in probs.items():
            if total_tally > 0:
                probs[category] = float(count) / float(total_tally)
            else:
                probs[category] = 0.0

        for category, probability in probs.items():
            self.probabilities[category] = {'prc': probability, 'prnc': sum(probs.values()) - probability}

    def train(self, category, text):
        """
        Trains a category with a sample of text

        :param category: the name of the category we want to train
        :type category: str
        :param text: the text we want to train the category with
        :type text: str
        """
        try:
            bayes_category = self.categories.get_category(category)
        except KeyError:
            bayes_category = self.categories.add_category(category)

        tokens = self.tokenizer(str(text))
        occurrence_counts = self.count_token_occurrences(tokens)
        for word, count in occurrence_counts.items():
            bayes_category.train_token(word, count)

        self.calculate_category_probability()

    def untrain(self, category, text):
        """
        Untrains a category with a sample of text

        :param category: the name of the category we want to train
        :type category: str
        :param text: the text we want to untrain the category with
        :type text: str
        """
        try:
            bayes_category = self.categories.get_category(category)
        except KeyError:
            return

        tokens = self.tokenizer(str(text))
        occurance_counts = self.count_token_occurrences(tokens)
        for word, count in occurance_counts.items():
            bayes_category.untrain_token(word, count)

        self.calculate_category_probability()

    def classify(self, text):
        """
        Chooses the highest scoring category for a sample of text

        :param text: sample text to classify
        :type text: str
        :return: the "winning" category
        :rtype: str
        """
        score = self.score(text)
        if not score:
            return None
        else:
            return sorted(score.items(), key=lambda v: v[1])[(-1)][0]

    def score(self, text):
        """
        Scores a sample of text

        :param text: sample text to score
        :type text: str
        :return: dict of scores per category
        :rtype: dict
        """
        occurs = self.count_token_occurrences(self.tokenizer(text))
        scores = {}
        for category in self.categories.get_categories().keys():
            scores[category] = 0

        categories = self.categories.get_categories().items()
        for word, count in occurs.items():
            token_scores = {}
            for category, bayes_category in categories:
                token_scores[category] = float(bayes_category.get_token_count(word))

            token_tally = sum(token_scores.values())
            if token_tally == 0.0:
                continue
            for category, token_score in token_scores.items():
                scores[category] += count * self.calculate_bayesian_probability(category, token_score, token_tally)

        final_scores = {}
        for category, score in scores.items():
            if score > 0:
                final_scores[category] = score

        return final_scores

    def calculate_bayesian_probability(self, cat, token_score, token_tally):
        """
        Calculates the bayesian probability for a given token/category

        :param cat: The category we're scoring for this token
        :type cat: str
        :param token_score: The tally of this token for this category
        :type token_score: float
        :param token_tally: The tally total for this token from all categories
        :type token_tally: float
        :return: bayesian probability
        :rtype: float
        """
        prc = self.probabilities[cat]['prc']
        prnc = self.probabilities[cat]['prnc']
        prtnc = (token_tally - token_score) / token_tally
        prtc = token_score / token_tally
        numerator = prtc * prc
        denominator = numerator + prtnc * prnc
        if denominator != 0.0:
            return numerator / denominator
        return 0.0

    def tally(self, category):
        """
        Gets the tally for a requested category

        :param category: The category we want a tally for
        :type category: str
        :return: tally for a given category
        :rtype: int
        """
        try:
            bayes_category = self.categories.get_category(category)
        except KeyError:
            return 0

        return bayes_category.get_tally()

    def get_cache_location(self):
        """
        Gets the location of the cache file

        :return: the location of the cache file
        :rtype: string
        """
        filename = self.cache_path if self.cache_path[-1:] == '/' else self.cache_path + '/'
        filename += self.cache_file
        return filename

    def cache_persist(self):
        """
        Saves the current trained data to the cache.
        This is initiated by the program using this module
        """
        filename = self.get_cache_location()
        pickle.dump(self.categories, open(filename, 'wb'))

    def cache_train(self):
        """
        Loads the data for this classifier from a cache file

        :return: whether or not we were successful
        :rtype: bool
        """
        filename = self.get_cache_location()
        if not os.path.exists(filename):
            return False
        categories = pickle.load(open(filename, 'rb'))
        assert isinstance(categories, BayesCategories), 'Cache data is either corrupt or invalid'
        self.categories = categories
        self.calculate_category_probability()
        return True