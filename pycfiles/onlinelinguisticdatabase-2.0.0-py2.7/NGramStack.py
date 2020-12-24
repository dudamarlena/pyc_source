# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/lib/simplelm/NGramStack.py
# Compiled at: 2016-09-19 13:27:02


class NGramStack:
    """
      A stack object designed to pop and push word 
      tokens onto an N-gram stack of fixed max-length.
    """

    def __init__(self, order=3):
        self.o = order
        self.s = []

    def push(self, word):
        """ 
           Push a word onto the stack.
           Pop off the bottom word if the
           stack size becomes too large.
        """
        self.s.append(word)
        if len(self.s) > self.o:
            self.s.pop(0)
        return self.s[:]

    def pop(self):
        self.s.pop(0)
        return self.s[:]

    def clear(self):
        """
           Empty all the words from the stack.
        """
        self.s = []