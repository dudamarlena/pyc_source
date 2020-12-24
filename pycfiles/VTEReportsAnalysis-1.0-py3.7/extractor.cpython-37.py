# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\VTEReportsAnalysis\extractor.py
# Compiled at: 2020-05-05 06:15:54
# Size of source mod 2**32: 2002 bytes
import nltk, nltk.data
from .findMatch import horspool_match
from .negex import *
import pkg_resources
resource_package = 'VTEReportsAnalysis'
resource_path = '/'.join(('config', 'negex_triggers.txt'))
path = pkg_resources.resource_filename(resource_package, resource_path)
rfile = open(path)
irules = sortRules(rfile.readlines())

def splitSentence(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    return sentences


class reExtractor:

    def __init__(self, target, skip, absolute_negative, absolute_positive, start):
        self.target = target
        self.skip = skip
        self.absolute_positive = absolute_positive
        self.absolute_negative = absolute_negative
        self.start = start

    def test(self):
        print(self.target)

    def processing(self, text):
        for phrase in self.start:
            temp = horspool_match(phrase, text)
            if temp != -1:
                text = text[temp:]

        text = text.lower()
        for phrase in self.absolute_negative:
            temp = horspool_match(phrase, text)
            if temp != -1:
                print(phrase, text)
                return (-99, -99)

        sentences = splitSentence(text)
        presentCount = 0
        absentCount = 0
        for sentence in sentences:
            present = 0
            mark = 0
            for phrase in self.skip:
                temp = horspool_match(phrase, sentence)
                if temp != -1:
                    mark = 1

            if mark == 1:
                continue
            mark = 0
            for phrase in self.target:
                temp = horspool_match(phrase, sentence)
                if temp != -1:
                    mark = 1

            if mark == 1:
                tagger = negTagger(sentence, phrases='', rules=irules, negP=False)
                negexResult = tagger.getNegationFlag()
                if negexResult == 'affirmed':
                    present = 1
                else:
                    if negexResult == 'negated':
                        present = 0
                if present == 1:
                    presentCount += 1
            else:
                absentCount += 1

        return (
         presentCount, absentCount)