# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqa/tokenizers/spacy_tokenizer.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 2055 bytes
"""Tokenizer that is backed by spaCy (spacy.io).

Requires spaCy package and the spaCy english model.
"""
import spacy, copy
from .tokenizer import Tokens, Tokenizer

class SpacyTokenizer(Tokenizer):

    def __init__(self, **kwargs):
        """
        Args:
            annotators: set that can include pos, lemma, and ner.
            model: spaCy model to use (either path, or keyword like 'en').
        """
        model = kwargs.get('model', 'en')
        self.annotators = copy.deepcopy(kwargs.get('annotators', set()))
        nlp_kwargs = {'parser': False}
        if not {'lemma', 'pos', 'ner'} & self.annotators:
            nlp_kwargs['tagger'] = False
        if not {
         'ner'} & self.annotators:
            nlp_kwargs['entity'] = False
        self.nlp = (spacy.load)(model, **nlp_kwargs)

    def tokenize(self, text):
        clean_text = text.replace('\n', ' ')
        tokens = self.nlp.tokenizer(clean_text)
        if {'lemma', 'pos', 'ner'} & self.annotators:
            self.nlp.tagger(tokens)
        if {
         'ner'} & self.annotators:
            self.nlp.entity(tokens)
        data = []
        for i in range(len(tokens)):
            start_ws = tokens[i].idx
            if i + 1 < len(tokens):
                end_ws = tokens[(i + 1)].idx
            else:
                end_ws = tokens[i].idx + len(tokens[i].text)
            data.append((
             tokens[i].text,
             text[start_ws:end_ws],
             (
              tokens[i].idx, tokens[i].idx + len(tokens[i].text)),
             tokens[i].tag_,
             tokens[i].lemma_,
             tokens[i].ent_type_))

        return Tokens(data, (self.annotators), opts={'non_ent': ''})