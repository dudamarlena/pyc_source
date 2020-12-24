# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/autocomp/simplecomp.py
# Compiled at: 2012-07-28 13:46:44
"""
Simple Generic autocompleter for completing words found in the current buffer.

"""
__author__ = 'Giuseppe "Cowo" Corbelli'
__cvsid__ = '$Id: simplecomp.py 72222 2012-07-28 15:43:38Z CJP $'
__revision__ = '$Revision: 72222 $'
import string, wx.stc as stc, completer

class Completer(completer.BaseCompleter):
    """Generic word completer provider"""
    wordCharacters = ('').join(['_', string.letters])

    def __init__(self, stc_buffer):
        super(Completer, self).__init__(stc_buffer)
        self.SetAutoCompKeys([])
        self.SetAutoCompStops(' \'"\\`):')
        self.SetAutoCompFillups('.,:;([]){}<>%^&+-=*/|$@')
        self.SetCallTipKeys([])
        self.SetCallTipCancel([])
        self.SetCaseSensitive(False)

    def _GetCompletionInfo(self, command, calltip=False):
        """Get Completion list or Calltip
        @return: list or string

        """
        bf = self.GetBuffer()
        kwlst = map(lambda kw: completer.Symbol(kw, completer.TYPE_UNKNOWN), bf.GetKeywords())
        if command in (None, ''):
            return kwlst
        else:
            fillups = self.GetAutoCompFillups()
            if command[0].isdigit() or command[(-1)] in fillups:
                return list()
            currentPos = bf.GetCurrentPos()
            tmp = command
            for ch in fillups:
                tmp = command.strip(ch)

            ls = list(tmp)
            ls.reverse()
            idx = 0
            for c in ls:
                if c in fillups:
                    break
                idx += 1

            ls2 = ls[:idx]
            ls2.reverse()
            command = ('').join(ls2)
            wordsNear = []
            maxWordLength = 0
            nWords = 0
            minPos = 0
            maxPos = bf.GetLength()
            flags = stc.STC_FIND_WORDSTART
            if self.GetCaseSensitive():
                flags |= stc.STC_FIND_MATCHCASE
            posFind = bf.FindText(minPos, maxPos, command, flags)
            while posFind >= 0 and posFind < maxPos:
                wordEnd = posFind + len(command)
                if posFind != currentPos:
                    while -1 != Completer.wordCharacters.find(chr(bf.GetCharAt(wordEnd))):
                        wordEnd += 1

                    wordLength = wordEnd - posFind
                    if wordLength > len(command):
                        word = bf.GetTextRange(posFind, wordEnd)
                        sym = completer.Symbol(word, completer.TYPE_UNKNOWN)
                        if not wordsNear.count(sym):
                            wordsNear.append(sym)
                            maxWordLength = max(maxWordLength, wordLength)
                            nWords += 1
                minPos = wordEnd
                posFind = bf.FindText(minPos, maxPos, command, flags)

            if len(wordsNear) > 0 and maxWordLength > len(command):
                return wordsNear
            return kwlst

    def GetAutoCompList(self, command):
        """Returns the list of possible completions for a command string.
        @param command: command lookup is done on

        """
        rlist = self._GetCompletionInfo(command)
        return sorted(list(set(rlist)))