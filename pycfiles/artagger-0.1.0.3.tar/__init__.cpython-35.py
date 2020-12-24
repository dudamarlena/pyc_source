# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/app/tagger/artagger/__init__.py
# Compiled at: 2017-01-18 05:25:08
# Size of source mod 2**32: 2142 bytes
from .Utility.Utils import getWordTag, readDictionary
from .InitialTagger.InitialTagger import initializeSentence
from .SCRDRlearner.SCRDRTree import SCRDRTree
from .SCRDRlearner.Object import FWObject
import os, copy, pickle

class Word:

    def __init__(self, **kwargs):
        self.word = kwargs.get('word', None)
        self.tag = kwargs.get('tag', None)


class RDRPOSTagger(SCRDRTree):
    __doc__ = '\n    RDRPOSTagger for a particular language\n    '

    def __init__(self):
        self.root = None

    def tagRawSentence(self, dictionary, rawLine):
        line = initializeSentence(dictionary, rawLine)
        sen = []
        wordTags = line.split()
        for i in range(len(wordTags)):
            fwObject = FWObject.getFWObject(wordTags, i)
            word, tag = getWordTag(wordTags[i])
            node = self.findFiredNode(fwObject)
            if node.depth > 0:
                sen.append(Word(word=word, tag=node.conclusion))
            else:
                sen.append(Word(word=word, tag=tag))
                sen.append(word + '/' + tag)

        return sen


class Tagger:

    def __init__(self, **kwargs):
        self.language = kwargs.get('language', 'th')
        self.text = kwargs.get('text', None)
        self.model = {}
        self.load_model()

    def load_model(self):
        self.model.update({'th': {'rdr': open(os.path.join(os.path.dirname(__file__), 'Models', 'POS', 'Thai.RDR'), 'r'), 
                'dict': open(os.path.join(os.path.dirname(__file__), 'Models', 'POS', 'Thai.DICT'), 'r')}})

    def tag(self, text):
        self.text = copy.copy(text)
        tagger = RDRPOSTagger()
        rdr_file = self.model[self.language]['rdr']
        dict_file = self.model[self.language]['dict']
        tagger.constructSCRDRtreeFromRDRfile(rdr_file.readlines())
        dictionary = readDictionary(dict_file.readlines())
        return tagger.tagRawSentence(dictionary, self.text)