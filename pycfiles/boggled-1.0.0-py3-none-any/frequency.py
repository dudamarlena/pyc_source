# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/boggleboard/frequency.py
# Compiled at: 2010-10-08 12:36:00
__doc__ = "frequency.py\n\nFunctions to deal with frequency of symbols in lists of strings of said symbols.\nIn the context of the boggleboard library specifically, we use this to iterate\nover a list of words and find letter frequency (treating 'qu' as its own letter\nas is standard). Then this information can be used to construct random Boggle\nboards or a set of dice for Boggle boards."
import random
defaultSymbols = [ _a if _a != 'q' else 'qu' for _a in map(chr, range(ord('a'), ord('z') + 1)) ]

def estimateFrequencies(wordList, symbols=defaultSymbols):
    """estimateFrequencies(wordList, symbols=defaultSymbols)

    Given a list of words over the specified collection of symbols, calculate
    the frequency of each symbol in the word list. The results are returned
    as a dictionary with keys from symbols and values the relative frequency
    of the symbol (i.e. a value in the range [0,1]). Note that symbols must
    not contain duplicate entries.

    Note that this function does not take into account the fact that some
    symbols might be subsymbols of others and should thus be treated
    differently, e.g. in Boggle, the u in qu should not be taken to contribute
    to the overall frequency of u; this is why we call the function an
    estimation. In the case where no symbol is contained in any other, then it
    is a fully accurate calculation."""
    assert len(symbols) == len(set(symbols))
    f = [ (symbol, sum([ w.count(symbol) for w in wordList ])) for symbol in symbols ]
    numSymbols = sum([ i[1] for i in f ])
    return dict([ (i[0], float(i[1]) / float(numSymbols)) for i in f ])


def calculateFrequencies(wordList, symbols=defaultSymbols, subsymbol=lambda x, y: True if y.find(x) >= 0 else False):
    """calculateFrequencies(wordList, symbols=defaultSymbols,
                            subsymbol=lambda x,y: True is y.find(x) >= 0 else False)

    Given a list of words over the specified collection of symbols, calculate
    the frequency of each symbol in the word list. The results are returned
    as a dictionary with keys from symbols and values the relative frequency
    of the symbol (i.e. a value in the range [0,1]). Note that symbols must
    not contain duplicate entries.

    subsymbol is a function taking two arguments, x and y, which returns True if
    x is a subsymbol of y and False otherwise. (Since symbols is not permitted
    to contain duplicate entries, proper vs. nonproper subsymbols need not be a
    consideration.) The default implementation works for strings in the standard
    subsymbol as subset interpretation; other representations of symbols will
    require their own subsymbol implementation.

    If no symbol is contained in any other, then estimateFrequencies returns the
    same result as calculateFrequenices and is significantly more efficient."""
    assert len(symbols) == len(set(symbols))
    processingOrder = []
    deps = dict([ (key, set([ i for i in symbols if i != key if subsymbol(key, i) ])) for key in symbols ])
    while deps:
        processed = []
        for (symbol, depset) in deps.items():
            if depset:
                continue
            processingOrder.append(symbol)
            processed.append(symbol)
            for (psymbol, pdepset) in deps.items():
                pdepset.discard(symbol)

        for symbol in processed:
            deps.pop(symbol)

    f = dict.fromkeys(symbols, 0)
    for word in wordList:
        for symbol in processingOrder:
            if not word:
                break
            f[symbol] += word.count(symbol)
            word = word.replace(symbol, '')

    numSymbols = sum(f.values())
    return dict([ (symbol, float(count) / float(numSymbols)) for (symbol, count) in f.items() ])


def createDice(frequencies, diceSpecs=[
 6] * 16):
    """createDice(frequencies, diceSpecs=[6]*16)

    Given a relative frequency table (i.e. a table mapping symbols to their
    relative frequency in the word list that will be used), create a set of
    Boggle-like "dice" to try to capture the frequencies.

    diceSpecs is a list of specifications of the dice: diceSpecs[i] should
    be the number of faces to appear on the ith die. By default, we specify
    16 standard 6-sided dice."""
    totalNumberOfFacesRemaining = sum(diceSpecs)
    numberOfFacesPerSymbol = {}
    modifiedFrequencies = sorted(map(list, frequencies.items()), key=lambda x: x[1], reverse=True)
    while modifiedFrequencies:
        (symbol, frequency) = modifiedFrequencies.pop()
        numberOfFaces = max(1, int(round(frequency * totalNumberOfFacesRemaining)))
        numberOfFacesPerSymbol[symbol] = numberOfFaces
        totalNumberOfFacesRemaining -= numberOfFaces
        totalProportion = sum(map(lambda x: x[1], modifiedFrequencies))
        for frequencyPair in modifiedFrequencies:
            frequencyPair[1] /= totalProportion

    assert sum(numberOfFacesPerSymbol.values()) == sum(diceSpecs)
    faces = [ symbol for (symbol, numberOfFaces) in numberOfFacesPerSymbol.items() for i in range(numberOfFaces)
            ]
    random.shuffle(faces)
    dice = []
    for spec in diceSpecs:
        dice.append(faces[:spec])
        faces[:spec] = []

    assert not faces
    return dice


if __name__ == '__main__':
    import boggleboard.yawl
    f = calculateFrequencies(boggleboard.yawl.wordList)
    print createDice(f)