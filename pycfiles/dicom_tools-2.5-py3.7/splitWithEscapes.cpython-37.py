# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/splitWithEscapes.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 705 bytes


def splitWithEscapes(theString, splittingChar=' ', escapeChar='\\', verbose=False):
    words = theString.split(splittingChar)
    iword = 0
    while iword < len(words) - 1:
        if verbose:
            print('splitWithEscapes', iword, words[iword])
        if len(words[iword]) > 2:
            if words[iword][(-1)] == escapeChar:
                words[iword] = words[iword][:-1] + splittingChar + words[(iword + 1)]
                words.remove(words[(iword + 1)])
                iword -= 2
        iword += 1

    for word in words:
        if word == '':
            words.remove(word)
        if word == '\n':
            words.remove(word)

    if verbose:
        print('splitWithEscapes', words)
    return words