# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rake/rake.py
# Compiled at: 2013-12-24 22:37:01
import re, operator, math, os
debug = False
test = True

def isnum(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def loadStopWords(stopWordFile):
    stopWords = []
    for line in open(stopWordFile):
        if line.strip()[0:1] != '#':
            for word in line.split():
                stopWords.append(word)

    return stopWords


def separatewords(text, minWordReturnSize):
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for singleWord in splitter.split(text):
        currWord = singleWord.strip().lower()
        if len(currWord) > minWordReturnSize and currWord != '' and not isnum(currWord):
            words.append(currWord)

    return words


def splitSentences(text):
    sentenceDelimiters = re.compile('[.!?,;:\t\\-\\"\\(\\)\\\'’–]')
    sentenceList = sentenceDelimiters.split(text)
    return sentenceList


def buildStopwordRegExPattern(pathtostopwordsfile):
    stopwordlist = loadStopWords(pathtostopwordsfile)
    stopwordregexlist = []
    for wrd in stopwordlist:
        wrdregex = '\\b' + wrd + '\\b'
        stopwordregexlist.append(wrdregex)

    stopwordpattern = re.compile(('|').join(stopwordregexlist), re.IGNORECASE)
    return stopwordpattern


def generateCandidateKeywords(sentenceList, stopwordpattern):
    phraseList = []
    for s in sentenceList:
        tmp = re.sub(stopwordpattern, '|', s.strip())
        phrases = tmp.split('|')
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != '':
                phraseList.append(phrase)

    return phraseList


def calculateWordScores(phraseList):
    wordfreq = {}
    worddegree = {}
    for phrase in phraseList:
        wordlist = separatewords(phrase, 0)
        wordlistlength = len(wordlist)
        wordlistdegree = wordlistlength - 1
        for word in wordlist:
            wordfreq.setdefault(word, 0)
            wordfreq[word] += 1
            worddegree.setdefault(word, 0)
            worddegree[word] += wordlistdegree

    for item in wordfreq:
        worddegree[item] = worddegree[item] + wordfreq[item]

    wordscore = {}
    for item in wordfreq:
        wordscore.setdefault(item, 0)
        wordscore[item] = worddegree[item] / (wordfreq[item] * 1.0)

    return wordscore


def generateCandidateKeywordScores(phraseList, wordscore):
    keywordcandidates = {}
    for phrase in phraseList:
        keywordcandidates.setdefault(phrase, 0)
        wordlist = separatewords(phrase, 0)
        candidatescore = 0
        for word in wordlist:
            candidatescore += wordscore[word]

        keywordcandidates[phrase] = candidatescore

    return keywordcandidates


def rake(text):
    sentenceList = splitSentences(text)
    stoppath = os.path.join(os.path.dirname(__file__), 'SmartStoplist.txt')
    stopwordpattern = buildStopwordRegExPattern(stoppath)
    phraseList = generateCandidateKeywords(sentenceList, stopwordpattern)
    wordscores = calculateWordScores(phraseList)
    keywordcandidates = generateCandidateKeywordScores(phraseList, wordscores)
    if debug:
        print keywordcandidates
    sortedKeywords = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
    if debug:
        print sortedKeywords
    totalKeywords = len(sortedKeywords)
    if debug:
        print totalKeywords
    print sortedKeywords[0:totalKeywords / 3]
    return sortedKeywords


if test:
    text = 'Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types.'
    rake(text)