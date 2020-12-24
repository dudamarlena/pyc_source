# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/DH/prosodic/lib/Parse.py
# Compiled at: 2019-06-07 00:03:27
from tools import *
from copy import copy
import string
from entity import entity
import logging
from functools import total_ordering

class Bounding:
    bounds = 0
    bounded = 1
    equal = 2
    unequal = 3


@total_ordering
class Parse(entity):
    str2int = {'w': '1', 's': '2'}

    def __init__(self, meter, totalSlots):
        self.positions = []
        self.meter = meter
        self.constraints = meter.constraints
        self.constraintScores = {}
        for constraint in self.constraints:
            self.constraintScores[constraint] = 0

        self.constraintNames = [ c.name for c in self.constraints ]
        self.numSlots = 0
        self.totalSlots = totalSlots
        self.isBounded = False
        self.boundedBy = None
        self.unmetrical = False
        self.comparisonNums = set()
        self.comparisonParses = []
        self.parseNum = 0
        self.totalScore = None
        self.pauseComparisons = False
        return

    def __copy__(self):
        other = Parse(self.meter, self.totalSlots)
        other.numSlots = self.numSlots
        for pos in self.positions:
            other.positions.append(copy(pos))

        other.comparisonNums = copy(self.comparisonNums)
        for k, v in list(self.constraintScores.items()):
            other.constraintScores[k] = copy(v)

        return other

    def slots(self, by_word=False):
        slots = []
        last_word_i = None
        for pos in self.positions:
            for slot in pos.slots:
                if not by_word:
                    slots.append(slot)
                else:
                    if last_word_i == None or last_word_i != slot.i_word:
                        slots.append([])
                    slots[(-1)].append(slot)
                    last_word_i = slot.i_word

        return slots

    def str_meter(self, word_sep=''):
        str_meter = ''
        wordTokNow = None
        for pos in self.positions:
            for slot in pos.slots:
                if word_sep and wordTokNow and slot.wordtoken != wordTokNow:
                    str_meter += word_sep
                wordTokNow = slot.wordtoken
                str_meter += pos.meterVal

        return str_meter

    def extend(self, slot):
        from MeterPosition import MeterPosition
        self.totalScore = None
        self.numSlots += 1
        extendedParses = [
         self]
        sPos = MeterPosition(self.meter, 's')
        sPos.append(slot)
        wPos = MeterPosition(self.meter, 'w')
        wPos.append(slot)
        if len(self.positions) == 0:
            wParse = copy(self)
            self.positions.append(sPos)
            wParse.positions.append(wPos)
            extendedParses.append(wParse)
        else:
            lastPos = self.positions[(-1)]
            if lastPos.meterVal == 's':
                if len(lastPos.slots) < self.meter.maxS() and not slot.issplit:
                    sParse = copy(self)
                    sParse.positions[(-1)].append(slot)
                    extendedParses.append(sParse)
                self.positions.append(wPos)
            else:
                if len(lastPos.slots) < self.meter.maxW() and not slot.issplit:
                    wParse = copy(self)
                    wParse.positions[(-1)].append(slot)
                    extendedParses.append(wParse)
                self.positions.append(sPos)
            pos_i = len(self.positions) - 2
            for constraint in self.constraints:
                vScore = constraint.violationScore(self.positions[(-2)], pos_i=pos_i, slot_i=self.numSlots - 1, num_slots=self.totalSlots, all_positions=self.positions, parse=self)
                if vScore == '*':
                    self.constraintScores[constraint] = '*'
                else:
                    self.constraintScores[constraint] += vScore

        if self.numSlots == self.totalSlots:
            for parse in extendedParses:
                for constraint in self.constraints:
                    vScore = constraint.violationScore(parse.positions[(-1)], pos_i=len(parse.positions) - 1, slot_i=self.numSlots - 1, num_slots=self.totalSlots, all_positions=parse.positions, parse=parse)
                    if vScore == '*':
                        parse.constraintScores[constraint] = '*'
                    else:
                        parse.constraintScores[constraint] += vScore

        return extendedParses

    def getErrorCount(self):
        return self.score()

    def getErrorCountN(self):
        return self.getErrorCount() / len(self.positions)

    def formatConstraints(self, normalize=True, getKeys=False):
        vals = []
        keys = []
        for k, v in sorted(self.constraintScores.items()):
            if normalize:
                if bool(v):
                    vals.append(1)
                else:
                    vals.append(0)
            else:
                vals.append(v)
            if getKeys:
                keys.append(k)

        if getKeys:
            return (vals, keys)
        else:
            return vals

    @property
    def totalCount(self):
        return sum(self.constraintCounts.values())

    @property
    def constraintCounts(self):
        cc = {}
        for constraint in self.constraints:
            cn = 0
            for pos in self.positions:
                if pos.constraintScores[constraint]:
                    cn += 1

            cc[constraint] = cn

        return cc

    @property
    def num_sylls(self):
        return sum(len(pos.slots) for pos in self.positions)

    def score(self):
        score = 0
        for constraint, value in list(self.constraintScores.items()):
            if value == '*':
                self.totalScore = '*'
                return self.totalScore
            score += value

        self.totalScore = score
        if int(self.totalScore) == self.totalScore:
            return int(self.totalScore)
        return self.totalScore

    def __lt__(self, other):
        return self.score() < other.score()

    def __eq__(self, other):
        return self.score() == other.score()

    def posString(self, viols=False):
        output = []
        for pos in self.positions:
            x = str(pos)
            if viols and pos.has_viol:
                x += '*'
            output.append(x)

        return ('|').join(output)

    def posString2(self, viols=False):
        last_word = None
        output = ''
        for pos in self.positions:
            for slot in pos.slots:
                slotstr = slot.token.upper() if pos.meterVal == 's' else slot.token.lower()
                if last_word != slot.wordtoken:
                    output += ' ' + slotstr
                    last_word = slot.wordtoken
                else:
                    output += '.' + slotstr

        return output.strip()

    def str_stress(self):
        output = []
        for pos in self.positions:
            slotx = []
            for slot in pos.slots:
                if not slot.feats['prom.stress']:
                    slotx.append('U')
                elif slot.feats['prom.stress'] == 1:
                    slotx.append('P')
                else:
                    slotx.append('S')

            output += [('').join(slotx)]

        return string.join(output, '|')

    def words(self):
        last_word = None
        words = []
        for slot in self.slots():
            slot_word = slot.word
            slot_wordtoken = slot.wordtoken
            if last_word != slot_wordtoken:
                words += [slot_word]
                last_word = slot_wordtoken

        return words

    def wordtokens(self):
        last_word = None
        words = []
        for slot in self.slots():
            slot_word = slot.wordtoken
            if last_word != slot_word:
                words += [slot_word]
                last_word = slot_word

        return words

    def set_wordtokens_to_best_word_options(self):
        for wordtok, wordobj in zip(self.wordtokens(), self.words()):
            wordtok.set_as_best_word_option(wordobj)

    def __repr__(self):
        return self.posString()

    def __repr2__(self):
        return str(self.getErrorCount())

    def str_ot(self):
        ot = []
        for c in self.constraints:
            v = self.constraintScores[c]
            ot += [str(v) if int(v) != float(v) else str(int(v))]

        return ('\t').join(ot)

    def __report__(self, proms=False):
        o = ''
        i = 0
        for pos in self.positions:
            unitlist = ''
            factlist = ''
            for unit in pos.slots:
                unitlist += self.u2s(unit.token) + ' '

            unitlist = unitlist[:-1]
            unitlist = makeminlength(unitlist, 10)
            if proms:
                feats = ''
                for unit in pos.slots:
                    for k, v in list(unit.feats.items()):
                        if 'prom.' not in k:
                            continue
                        if v:
                            feats += '[+' + str(k) + '] '
                        else:
                            feats += '[-' + str(k) + '] '

                    feats += '\t'

                feats = feats.strip()
            viols = ''
            for k, v in list(pos.constraintScores.items()):
                if v:
                    viols += str(k)

            viols = viols.strip()
            if proms:
                viols = makeminlength(viols, 60)
            if pos.meterVal == 's':
                unitlist = unitlist.upper()
            else:
                unitlist = unitlist.lower()
            i += 1
            o += str(i) + '\t' + pos.meterVal2 + '\t' + unitlist + '\t' + viols
            if proms:
                o += feats + '\n'
            else:
                o += '\n'

        return o[:-1]

    def isIambic(self):
        if len(self.positions) < 2:
            return
        else:
            return self.positions[0].meterVal == 'w' and self.positions[1].meterVal == 's'
            return

    def canCompare(self, parse):
        isTrue = self.numSlots == self.totalSlots or self.positions[(-1)].meterVal == parse.positions[(-1)].meterVal and len(self.positions[(-1)].slots) == len(parse.positions[(-1)].slots)
        if isTrue:
            pass
        return isTrue

    def violations(self, boolean=False):
        if not boolean:
            return self.constraintScores
        else:
            return [ (k, v > 0) for k, v in list(self.constraintScores.items()) ]

    @property
    def violated(self):
        viold = []
        for c, viol in list(self.constraintScores.items()):
            if viol:
                viold += [c]

        return viold

    def constraintScorez(self):
        toreturn = {}
        for c in self.constraints:
            toreturn[c] = 0
            for pos in self.positions:
                toreturn[c] += pos.constraintScores[c]

        return toreturn

    def boundingRelation(self, parse):
        containsGreaterViolation = False
        containsLesserViolation = False
        for constraint in self.constraints:
            mark = self.constraintScores[constraint]
            mark2 = parse.constraintScores[constraint]
            if mark > parse.constraintScores[constraint]:
                containsGreaterViolation = True
            if mark < parse.constraintScores[constraint]:
                containsLesserViolation = True

        if containsGreaterViolation:
            if containsLesserViolation:
                return Bounding.unequal
            else:
                return Bounding.bounded

        else:
            if containsLesserViolation:
                return Bounding.bounds
            else:
                return Bounding.equal