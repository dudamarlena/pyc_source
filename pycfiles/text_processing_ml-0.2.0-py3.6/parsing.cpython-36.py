# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/text_processing_ml/parsing/parsing.py
# Compiled at: 2019-05-06 07:24:42
# Size of source mod 2**32: 1305 bytes
import nltk, string, os
from ..normalization import NormalizeText
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

class ParseText:

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.normalizer = NormalizeText()

    def stem_tokens(self, tokens):
        stemmed = []
        for item in tokens:
            stemmed.append(self.stemmer.stem(item))

        return stemmed

    def tokenize(self, text):
        tokens = nltk.word_tokenize(text)
        stems = self.stem_tokens(tokens)
        return stems

    def process_text(self, text):
        text = text.lower()
        return ' '.join([self.normalizer.strip_punctuation(word) for word in text.split(' ')])

    def tfidf(self, documents):
        documents = [self.process_text(document) for document in documents]
        tfidf_vectorizer = TfidfVectorizer(tokenizer=(self.tokenize), stop_words='english')
        return tfidf_vectorizer.fit_transform(documents)