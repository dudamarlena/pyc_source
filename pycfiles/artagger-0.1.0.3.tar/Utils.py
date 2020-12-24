# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/app/RDRPOSTagger-master/Utility/Utils.py
# Compiled at: 2016-10-16 09:54:12


def getWordTag(wordTag):
    if wordTag == '///':
        return ('/', '/')
    index = wordTag.rfind('/')
    word = wordTag[:index].strip()
    tag = wordTag[index + 1:].strip()
    return (word, tag)


def getRawText(inputFile, outFile):
    out = open(outFile, 'w')
    sents = open(inputFile, 'r').readlines()
    for sent in sents:
        wordTags = sent.strip().split()
        for wordTag in wordTags:
            word, tag = getWordTag(wordTag)
            out.write(word + ' ')

        out.write('\n')

    out.close()


def readDictionary(inputFile):
    dictionary = {}
    lines = open(inputFile, 'r').readlines()
    for line in lines:
        wordtag = line.strip().split()
        dictionary[wordtag[0]] = wordtag[1]

    return dictionary