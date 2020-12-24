# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/DH/prosodic/lib/Line.py
# Compiled at: 2019-06-07 00:03:27
from entity import being
from entity import entity
from tools import *

class Line(entity):

    def __init__(self):
        self.parent = False
        self.children = []
        self.feats = {}
        self.featpaths = {}
        self.finished = False
        self.__parses = {}
        self.__bestparse = {}
        self.__boundParses = {}

    def parse(self, meter=None, init=None):
        """
                words=self.ents(cls='Word',flattenList=False)
                #print words
                numSyll=0
                if not words: return None
                for word in words:
                        if type(word)==type([]):
                                for wrd in word:
                                        if wrd.isBroken():
                                                #print wrd
                                                return None
                                numSyll+=word[0].getNumSyll()
                        else:
                                if word.isBroken():
                                        return None
                                numSyll+=word.getNumSyll()

                ## PARSE
                self.__parses[meter.id],self.__boundParses[meter.id]=meter.parse(words,numSyll)
                ####
                """
        wordtoks = self.wordtokens(include_punct=False)
        numSyll = 0
        if not wordtoks:
            return
        else:
            for wordtok in wordtoks:
                wordtok_words = wordtok.children
                if not wordtok_words or True in [ word.isBroken() for word in wordtok_words ]:
                    return
                numSyll += wordtok_words[0].getNumSyll()

            self.__parses[meter.id], self.__boundParses[meter.id] = meter.parse(wordtoks, numSyll)
            self.__bestparse[meter.id] = None
            try:
                self.__bestparse[meter.id] = self.__parses[meter.id][0]
            except (KeyError, IndexError) as e:
                try:
                    self.__bestparse[meter.id] = self.__boundParses[meter.id][0]
                except (KeyError, IndexError) as e:
                    self.__bestparse[meter.id] = None

            bp = self.__bestparse[meter.id]
            if bp:
                bp.set_wordtokens_to_best_word_options()
            return

    def scansion(self, meter=None, conscious=False):
        bp = self.bestParse(meter)
        config = being.config
        lowestScore = ''
        str_ot = ''
        count = ''
        meterstr = ''
        if bp:
            meterstr = bp.str_meter()
            str_ot = bp.str_ot()
            lowestScore = bp.score()
            count = bp.totalCount
        from tools import makeminlength
        print makeminlength(str(bp), 60)
        data = [makeminlength(str(self), config['linelen']), makeminlength(str(bp) if bp else '', config['linelen']), meterstr, len(self.allParses(meter)), count, lowestScore, str_ot]
        data_unicode = [ str(x) for x in data ]
        self.om(('\t').join(data_unicode), conscious=conscious)

    def allParses(self, meter=None, one_per_meter=True):
        if not meter:
            itms = list(self.__parses.items())
            if not len(itms):
                return
            for mtr, parses in itms:
                return parses

        try:
            parses = self.__parses[meter.id]
            if one_per_meter:
                toreturn = []
                sofar = set()
                for _p in parses:
                    _pm = _p.str_meter()
                    if _pm not in sofar:
                        sofar |= {_pm}
                        if _p.isBounded and _p.boundedBy.str_meter() == _pm:
                            pass
                        else:
                            toreturn += [_p]

                parses = toreturn
            return parses
        except KeyError:
            return []

    def boundParses(self, meter=None):
        if not meter:
            itms = sorted(self.__boundParses.items())
            if not len(itms):
                return []
            for mtr, parses in itms:
                return parses

        try:
            return self.__boundParses[meter.id]
        except KeyError:
            return []

    def bestParse(self, meter=None):
        if not meter:
            itms = list(self.__bestparse.items())
            if not len(itms):
                return
            for mtr, parses in itms:
                return parses

        try:
            return self.__bestparse[meter.id]
        except KeyError:
            return

    def finish(self):
        if not hasattr(self, 'finished') or not self.finished:
            self.finished = True
            if not hasattr(self, 'broken'):
                self.broken = False
            if len(self.children) == 0:
                self.broken = True
            if not self.broken:
                for words in self.words(flattenList=False):
                    assert type(words) == list
                    for word in words:
                        if word.isBroken():
                            self.broken = True

    def __repr__(self):
        return self.txt

    @property
    def txt(self):
        x = ''
        for wordtok in self.wordtokens():
            if not wordtok.is_punct:
                x += ' ' + wordtok.token
            else:
                x += wordtok.token

        return x.strip()

    def str_wordbound(self):
        o = []
        for word in self.words():
            e = ''
            for x in word.children:
                e += 'X'

            o.append(e)

        return ('#').join(o)

    def str_weight(self, word_sep=''):
        o = []
        for word in self.words():
            o.append(('').join(x.str_weight() for x in word.children))

        return word_sep.join(o)

    def str_stress(self, word_sep=''):
        o = []
        for word in self.words():
            o.append(('').join(x.str_stress() for x in word.children))

        return word_sep.join(o)

    def str_sonority(self, word_sep=''):
        o = []
        for word in self.words():
            o.append(('').join(x.str_sonority() for x in word.children))

        return word_sep.join(o)