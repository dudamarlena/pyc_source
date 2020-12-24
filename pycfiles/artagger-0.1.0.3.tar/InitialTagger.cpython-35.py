# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/app/tagger/InitialTagger/InitialTagger.py
# Compiled at: 2017-01-18 02:20:39
# Size of source mod 2**32: 2052 bytes
import re, copy

def initializeSentence(FREQDICT, sentence):
    words = sentence.strip().split()
    taggedSen = []
    for word in words:
        if word in ('“', '”', '"'):
            taggedSen.append("''/" + FREQDICT["''"])
            continue
            tag = ''
            decodedW = copy.copy(word)
            lowerW = word.lower()
            if word in FREQDICT:
                tag = FREQDICT[word]
            else:
                if lowerW in FREQDICT:
                    tag = FREQDICT[lowerW]
                else:
                    if re.search('[0-9]+', word) != None:
                        tag = FREQDICT['TAG4UNKN-NUM']
                    else:
                        suffixL2 = suffixL3 = suffixL4 = suffixL5 = None
                        wLength = len(decodedW)
                        if wLength >= 4:
                            suffixL3 = '.*' + decodedW[-3:]
                            suffixL2 = '.*' + decodedW[-2:]
                        if wLength >= 5:
                            suffixL4 = '.*' + decodedW[-4:]
                        if wLength >= 6:
                            suffixL5 = '.*' + decodedW[-5:]
                        if suffixL5 in FREQDICT:
                            tag = FREQDICT[suffixL5]
                        else:
                            if suffixL4 in FREQDICT:
                                tag = FREQDICT[suffixL4]
                            else:
                                if suffixL3 in FREQDICT:
                                    tag = FREQDICT[suffixL3]
                                else:
                                    if suffixL2 in FREQDICT:
                                        tag = FREQDICT[suffixL2]
                                    else:
                                        if decodedW[0].isupper():
                                            tag = FREQDICT['TAG4UNKN-CAPITAL']
                                        else:
                                            tag = FREQDICT['TAG4UNKN-WORD']
            taggedSen.append(word + '/' + tag)

    return ' '.join(taggedSen)


def initializeCorpus(FREQDICT, inputFile, outputFile):
    lines = open(inputFile, 'r').readlines()
    fileOut = open(outputFile, 'w')
    for line in lines:
        fileOut.write(initializeSentence(FREQDICT, line) + '\n')

    fileOut.close()