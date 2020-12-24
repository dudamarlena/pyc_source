# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/enlp/pipeline.py
# Compiled at: 2019-11-27 15:57:30
# Size of source mod 2**32: 1896 bytes
"""
Class for piping functions for natural language processing
"""
from enlp.processing.stdtools import *
from enlp.understanding.linguistic import pos_tag

class NLPPipeline(object):
    __doc__ = 'Pipeline class for combining functions from nlp_tools\n\n    Attributes\n    ----------\n    model : :obj:`spacy.lang`\n        SpaCy language model\n    text : :obj:`str`\n        text string on which to perform processing\n    pos : :obj:`list`\n        list of Parts-of-Speech tags\n    tokens : :obj:`list`\n        list of tokens\n\n    '

    def __init__(self, model, text):
        """__init__ method of nlp_pipeline class

        Parameters
        ----------
        model : :obj:`spacy.lang`
            SpaCy language model
        text : :obj:`str`
            text string on which to perform processing

        """
        self.model = model
        self.text = text

    def rm_punctuation(self, **kwargs):
        """remove punctuation from text
        """
        self.text = rm_punctuation(self.model, self.text)
        return self

    def rm_stopwords(self, **kwargs):
        """remove stopwords from text

        Notes
        -----
        List of stopwords can be obtained from stdtools.get_stopwords()

        """
        self.text = rm_stopwords((self.model), (self.text), stopwords=(kwargs['stopwords']))
        return self

    def spacy_lemmatize(self):
        """lemmatise text
        """
        self.text = spacy_lemmatize(self.model, self.text)
        return self

    def nltk_stem_no(self):
        """stem text
        """
        self.text = nltk_stem_no(self.model, self.text)
        return self

    def pos_tag(self):
        """get part-of-speech tags
        """
        self.pos = pos_tag(self.model, self.text)
        return self

    def tokenise(self):
        """tokenise text
        """
        self.tokens = tokenise(self.model, self.text)
        return self