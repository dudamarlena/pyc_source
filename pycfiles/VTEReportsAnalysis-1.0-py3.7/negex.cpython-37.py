# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\VTEReportsAnalysis\negex.py
# Compiled at: 2020-05-05 05:08:30
# Size of source mod 2**32: 8984 bytes
import re

def sortRules(ruleList):
    """Return sorted list of rules.
    
    Rules should be in a tab-delimited format: 'rule            [four letter negation tag]'
    Sorts list of rules descending based on length of the rule, 
    splits each rule into components, converts pattern to regular expression,
    and appends it to the end of the rule. """
    ruleList.sort(key=len, reverse=True)
    sortedList = []
    for rule in ruleList:
        s = rule.strip().split('\t')
        splitTrig = s[0].split()
        trig = '\\s+'.join(splitTrig)
        pattern = '\\b(' + trig + ')\\b'
        s.append(re.compile(pattern, re.IGNORECASE))
        sortedList.append(s)

    return sortedList


class negTagger(object):
    __doc__ = "Take a sentence and tag negation terms and negated phrases.\n    \n    Keyword arguments:\n    sentence -- string to be tagged\n    phrases  -- list of phrases to check for negation\n    rules    -- list of negation trigger terms from the sortRules function\n    negP     -- tag 'possible' terms as well (default = True)    "

    def __init__(self, sentence='', phrases=None, rules=None, negP=True):
        self._negTagger__sentence = sentence
        self._negTagger__phrases = phrases
        self._negTagger__rules = rules
        self._negTagger__negTaggedSentence = ''
        self._negTagger__scopesToReturn = []
        self._negTagger__negationFlag = None
        filler = '_'
        for rule in self._negTagger__rules:
            reformatRule = re.sub('\\s+', filler, rule[0].strip())
            self._negTagger__sentence = rule[3].sub(' ' + rule[2].strip() + reformatRule + rule[2].strip() + ' ', self._negTagger__sentence)

        for phrase in self._negTagger__phrases:
            phrase = re.sub('([.^$*+?{\\\\|()[\\]])', '\\\\\\1', phrase)
            splitPhrase = phrase.split()
            joiner = '\\W+'
            joinedPattern = '\\b' + joiner.join(splitPhrase) + '\\b'
            reP = re.compile(joinedPattern, re.IGNORECASE)
            m = reP.search(self._negTagger__sentence)
            if m:
                self._negTagger__sentence = self._negTagger__sentence.replace(m.group(0), '[PHRASE]' + re.sub('\\s+', filler, m.group(0).strip()) + '[PHRASE]')

        overlapFlag = 0
        prenFlag = 0
        postFlag = 0
        prePossibleFlag = 0
        postPossibleFlag = 0
        sentenceTokens = self._negTagger__sentence.split()
        sentencePortion = ''
        aScopes = []
        sb = []
        for i in range(len(sentenceTokens)):
            if sentenceTokens[i][:6] == '[PREN]':
                prenFlag = 1
                overlapFlag = 0
            else:
                if sentenceTokens[i][:6] in ('[CONJ]', '[PSEU]', '[POST]', '[PREP]',
                                             '[POSP]'):
                    overlapFlag = 1
                elif i + 1 < len(sentenceTokens) and sentenceTokens[(i + 1)][:6] == '[PREN]':
                    overlapFlag = 1
                    if sentencePortion.strip():
                        aScopes.append(sentencePortion.strip())
                    sentencePortion = ''
                if prenFlag == 1 and overlapFlag == 0:
                    sentenceTokens[i] = sentenceTokens[i].replace('[PHRASE]', '[NEGATED]')
                    sentencePortion = sentencePortion + ' ' + sentenceTokens[i]
            sb.append(sentenceTokens[i])

        if sentencePortion.strip():
            aScopes.append(sentencePortion.strip())
        else:
            sentencePortion = ''
            sb.reverse()
            sentenceTokens = sb
            sb2 = []
            for i in range(len(sentenceTokens)):
                if sentenceTokens[i][:6] == '[POST]':
                    postFlag = 1
                    overlapFlag = 0
                else:
                    if sentenceTokens[i][:6] in ('[CONJ]', '[PSEU]', '[PREN]', '[PREP]',
                                                 '[POSP]'):
                        overlapFlag = 1
                    elif i + 1 < len(sentenceTokens) and sentenceTokens[(i + 1)][:6] == '[POST]':
                        overlapFlag = 1
                        if sentencePortion.strip():
                            aScopes.append(sentencePortion.strip())
                        sentencePortion = ''
                    if postFlag == 1 and overlapFlag == 0:
                        sentenceTokens[i] = sentenceTokens[i].replace('[PHRASE]', '[NEGATED]')
                        sentencePortion = sentenceTokens[i] + ' ' + sentencePortion
                sb2.insert(0, sentenceTokens[i])

            if sentencePortion.strip():
                aScopes.append(sentencePortion.strip())
            else:
                sentencePortion = ''
                self._negTagger__negTaggedSentence = ' '.join(sb2)
                if negP:
                    sentenceTokens = sb2
                    sb3 = []
                    for i in range(len(sentenceTokens)):
                        if sentenceTokens[i][:6] == '[PREP]':
                            prePossibleFlag = 1
                            overlapFlag = 0
                        else:
                            if sentenceTokens[i][:6] in ('[CONJ]', '[PSEU]', '[POST]',
                                                         '[PREN]', '[POSP]'):
                                overlapFlag = 1
                            elif i + 1 < len(sentenceTokens) and sentenceTokens[(i + 1)][:6] == '[PREP]':
                                overlapFlag = 1
                                if sentencePortion.strip():
                                    aScopes.append(sentencePortion.strip())
                                sentencePortion = ''
                            if prePossibleFlag == 1 and overlapFlag == 0:
                                sentenceTokens[i] = sentenceTokens[i].replace('[PHRASE]', '[POSSIBLE]')
                                sentencePortion = sentencePortion + ' ' + sentenceTokens[i]
                        sb3 = sb3 + ' ' + sentenceTokens[i]

                    if sentencePortion.strip():
                        aScopes.append(sentencePortion.strip())
                    sentencePortion = ''
                    sb3.reverse()
                    sentenceTokens = sb3
                    sb4 = []
                    for i in range(len(sentenceTokens)):
                        if sentenceTokens[i][:6] == '[POSP]':
                            postPossibleFlag = 1
                            overlapFlag = 0
                        else:
                            if sentenceTokens[i][:6] in ('[CONJ]', '[PSEU]', '[PREN]',
                                                         '[PREP]', '[POST]'):
                                overlapFlag = 1
                            elif i + 1 < len(sentenceTokens) and sentenceTokens[(i + 1)][:6] == '[POSP]':
                                overlapFlag = 1
                                if sentencePortion.strip():
                                    aScopes.append(sentencePortion.strip())
                                sentencePortion = ''
                            if postPossibleFlag == 1 and overlapFlag == 0:
                                sentenceTokens[i] = sentenceTokens[i].replace('[PHRASE]', '[POSSIBLE]')
                                sentencePortion = sentenceTokens[i] + ' ' + sentencePortion
                        sb4.insert(0, sentenceTokens[i])

                    if sentencePortion.strip():
                        aScopes.append(sentencePortion.strip())
                    self._negTagger__negTaggedSentence = ' '.join(sb4)
                if '[NEGATED]' in self._negTagger__negTaggedSentence:
                    self._negTagger__negationFlag = 'negated'
                else:
                    if '[POSSIBLE]' in self._negTagger__negTaggedSentence:
                        self._negTagger__negationFlag = 'possible'
                    else:
                        self._negTagger__negationFlag = 'affirmed'
        self._negTagger__negTaggedSentence = self._negTagger__negTaggedSentence.replace(filler, ' ')
        for line in aScopes:
            tokensToReturn = []
            thisLineTokens = line.split()
            for token in thisLineTokens:
                if token[:6] not in ('[PREN]', '[PREP]', '[POST]', '[POSP]'):
                    tokensToReturn.append(token)

            self._negTagger__scopesToReturn.append(' '.join(tokensToReturn))

    def getNegTaggedSentence(self):
        return self._negTagger__negTaggedSentence

    def getNegationFlag(self):
        return self._negTagger__negationFlag

    def getScopes(self):
        return self._negTagger__scopesToReturn

    def __str__(self):
        text = self._negTagger__negTaggedSentence
        text += '\t' + self._negTagger__negationFlag
        text += '\t' + '\t'.join(self._negTagger__scopesToReturn)