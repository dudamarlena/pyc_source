# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqa/tokenizers/tokenizer.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 4260 bytes
"""Base tokenizer/tokens classes and utilities."""
import copy

class Tokens(object):
    __doc__ = 'A class to represent a list of tokenized text.'
    TEXT = 0
    TEXT_WS = 1
    SPAN = 2
    POS = 3
    LEMMA = 4
    NER = 5

    def __init__(self, data, annotators, opts=None):
        self.data = data
        self.annotators = annotators
        self.opts = opts or {}

    def __len__(self):
        """The number of tokens."""
        return len(self.data)

    def slice(self, i=None, j=None):
        """Return a view of the list of tokens from [i, j)."""
        new_tokens = copy.copy(self)
        new_tokens.data = self.data[i:j]
        return new_tokens

    def untokenize(self):
        """Returns the original text (with whitespace reinserted)."""
        return ''.join([t[self.TEXT_WS] for t in self.data]).strip()

    def words(self, uncased=False):
        """Returns a list of the text of each token

        Args:
            uncased: lower cases text
        """
        if uncased:
            return [t[self.TEXT].lower() for t in self.data]
        else:
            return [t[self.TEXT] for t in self.data]

    def offsets(self):
        """Returns a list of [start, end) character offsets of each token."""
        return [t[self.SPAN] for t in self.data]

    def pos(self):
        """Returns a list of part-of-speech tags of each token.
        Returns None if this annotation was not included.
        """
        if 'pos' not in self.annotators:
            return
        else:
            return [t[self.POS] for t in self.data]

    def lemmas(self):
        """Returns a list of the lemmatized text of each token.
        Returns None if this annotation was not included.
        """
        if 'lemma' not in self.annotators:
            return
        else:
            return [t[self.LEMMA] for t in self.data]

    def entities(self):
        """Returns a list of named-entity-recognition tags of each token.
        Returns None if this annotation was not included.
        """
        if 'ner' not in self.annotators:
            return
        else:
            return [t[self.NER] for t in self.data]

    def ngrams(self, n=1, uncased=False, filter_fn=None, as_strings=True):
        """Returns a list of all ngrams from length 1 to n.

        Args:
            n: upper limit of ngram length
            uncased: lower cases text
            filter_fn: user function that takes in an ngram list and returns
              True or False to keep or not keep the ngram
            as_string: return the ngram as a string vs list
        """

        def _skip(gram):
            if not filter_fn:
                return False
            else:
                return filter_fn(gram)

        words = self.words(uncased)
        ngrams = [(s, e + 1) for s in range(len(words)) if not _skip(words[s:e + 1]) for e in range(s, min(s + n, len(words)))]
        if as_strings:
            ngrams = ['{}'.format(' '.join(words[s:e])) for s, e in ngrams]
        return ngrams

    def entity_groups(self):
        """Group consecutive entity tokens with the same NER tag."""
        entities = self.entities()
        if not entities:
            return
        else:
            non_ent = self.opts.get('non_ent', 'O')
            groups = []
            idx = 0
            while idx < len(entities):
                ner_tag = entities[idx]
                if ner_tag != non_ent:
                    start = idx
                    while idx < len(entities) and entities[idx] == ner_tag:
                        idx += 1

                    groups.append((self.slice(start, idx).untokenize(), ner_tag))
                else:
                    idx += 1

            return groups


class Tokenizer(object):
    __doc__ = 'Base tokenizer class.\n    Tokenizers implement tokenize, which should return a Tokens class.\n    '

    def tokenize(self, text):
        raise NotImplementedError

    def shutdown(self):
        pass

    def __del__(self):
        self.shutdown()