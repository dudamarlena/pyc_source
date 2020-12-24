# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/catalog/indexes/text_lexicon.py
# Compiled at: 2016-03-05 15:57:06
from BTrees.Length import Length
from zope.index.text.lexicon import Lexicon as _Lexicon
from zerodb import trees
from zerodb.storage import parallel_traversal

def _text2list(text):
    try:
        text + ''
    except UnicodeDecodeError:
        try:
            return [
             text.decode('utf-8')]
        except UnicodeDecodeError:
            return [
             text]

    except TypeError:
        return text
    else:
        return [
         text]


class Lexicon(_Lexicon):
    family = trees.family32

    def __init__(self, *pipeline):
        self._wids = self.family.OI.BTree()
        self._words = self.family.IO.BTree()
        self.wordCount = Length()
        self._pipeline = pipeline

    def sourceToWordIds(self, text):
        if text is None:
            text = ''
        last = _text2list(text)
        for element in self._pipeline:
            last = element.process(last)

        if not isinstance(self.wordCount, Length):
            self.wordCount = Length(self.wordCount())
        self.wordCount._p_deactivate()
        parallel_traversal(self._wids, last)
        return list(map(self._getWordIdCreate, last))

    def termToWordIds(self, text):
        last = _text2list(text)
        for element in self._pipeline:
            last = element.process(last)

        wids = []
        if len(last) > 1:
            parallel_traversal(self._wids, last)
        for word in last:
            wids.append(self._wids.get(word, 0))

        return wids