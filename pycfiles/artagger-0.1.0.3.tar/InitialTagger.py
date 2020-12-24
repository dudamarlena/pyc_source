# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/app/RDRPOSTagger-master/InitialTagger/InitialTagger.py
# Compiled at: 2016-10-16 09:54:12
import re

def initializeSentence(FREQDICT, sentence):
    words = sentence.strip().split()
    taggedSen = []
    for word in words:
        if word in ('“', '”', '"'):
            taggedSen.append("''/" + FREQDICT["''"])
            continue
        tag = ''
        decodedW = word.decode('utf-8')
        lowerW = decodedW.lower().encode('utf-8')
        if word in FREQDICT:
            tag = FREQDICT[word]
        elif lowerW in FREQDICT:
            tag = FREQDICT[lowerW]
        elif re.search('[0-9]+', word) != None:
            tag = FREQDICT['TAG4UNKN-NUM']
        else:
            suffixL2 = suffixL3 = suffixL4 = suffixL5 = None
            wLength = len(decodedW)
            if wLength >= 4:
                suffixL3 = '.*' + decodedW[-3:].encode('utf-8')
                suffixL2 = '.*' + decodedW[-2:].encode('utf-8')
            if wLength >= 5:
                suffixL4 = '.*' + decodedW[-4:].encode('utf-8')
            if wLength >= 6:
                suffixL5 = '.*' + decodedW[-5:].encode('utf-8')
            if suffixL5 in FREQDICT:
                tag = FREQDICT[suffixL5]
            elif suffixL4 in FREQDICT:
                tag = FREQDICT[suffixL4]
            elif suffixL3 in FREQDICT:
                tag = FREQDICT[suffixL3]
            elif suffixL2 in FREQDICT:
                tag = FREQDICT[suffixL2]
            elif decodedW[0].isupper():
                tag = FREQDICT['TAG4UNKN-CAPITAL']
            else:
                tag = FREQDICT['TAG4UNKN-WORD']
        taggedSen.append(word + '/' + tag)

    return (' ').join(taggedSen)


def initializeCorpus(FREQDICT, inputFile, outputFile):
    lines = open(inputFile, 'r').readlines()
    fileOut = open(outputFile, 'w')
    for line in lines:
        fileOut.write(initializeSentence(FREQDICT, line) + '\n')

    fileOut.close()