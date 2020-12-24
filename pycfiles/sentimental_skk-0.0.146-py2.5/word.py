# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/word.py
# Compiled at: 2014-03-11 11:41:30
import dictionary, kanadb
_SKK_WORD_NONE = 0
_SKK_WORD_MAIN = 1
_SKK_WORD_OKURI = 2
_SKK_MARK_COOK = '▽'
_SKK_MARK_OKURI = '*'

class WordBuffer:
    _main = ''
    _mode = _SKK_WORD_NONE
    _comp = None
    _comp_index = 0
    _wcswidth = None

    def __init__(self, termprop):
        """
        >>> from canossa import termprop
        >>> termprop = termprop.MockTermprop()
        >>> wordbuf = WordBuffer(termprop)
        >>> termprop.set_cjk()
        >>> wordbuf = WordBuffer(termprop)
        """
        self.reset()
        self._wcswidth = termprop.wcswidth
        if not termprop.is_cjk and termprop.is_vte():
            self._cookmark = _SKK_MARK_COOK + ' '
        else:
            self._cookmark = _SKK_MARK_COOK

    def reset(self):
        self._mode = _SKK_WORD_NONE
        self._main = ''
        self._comp = None
        self._comp_index = 0
        return

    def isempty(self):
        """
        >>> from canossa import termprop
        >>> termprop = termprop.MockTermprop()
        >>> wordbuf = WordBuffer(termprop)
        >>> wordbuf.isempty()
        True
        >>> wordbuf.startedit()
        >>> wordbuf.isempty()
        False
        """
        return self._mode == _SKK_WORD_NONE

    def complete(self):
        if self._comp:
            self._comp_index = (self._comp_index + 1) % len(self._comp)
        else:
            key = kanadb.to_hira(self._main)
            self._comp = dictionary.suggest(key, None)
        return

    def suggest(self, finals=None):
        if self._main or finals:
            key = kanadb.to_hira(self._main)
            completions = dictionary.suggest(key, finals)
            if completions:
                return map(lambda word: self._main + word, completions)
        return

    def get(self):
        r"""
        >>> from canossa import termprop
        >>> termprop = termprop.MockTermprop()
        >>> wordbuf = WordBuffer(termprop)
        >>> wordbuf.startedit()
        >>> wordbuf.append(u'\u3060\u3057\u3083\u3059')
        >>> wordbuf.get()
        u'\u3060\u3057\u3083\u3059'
        >>> wordbuf.startokuri()
        >>> wordbuf.append(u'\u3060')
        >>> wordbuf.get()
        u'\u3060\u3057\u3083\u3059\u3060'
        """
        if self._mode == _SKK_WORD_NONE:
            return ''
        elif self._mode == _SKK_WORD_MAIN:
            if self._comp:
                return self._main + self._comp[self._comp_index]
            return self._main
        else:
            assert self._mode == _SKK_WORD_OKURI
            return self._main

    def append(self, value):
        r"""
        >>> from canossa import termprop
        >>> termprop = termprop.MockTermprop()
        >>> wordbuf = WordBuffer(termprop)
        >>> wordbuf.append(u'\u3060')
        >>> wordbuf.get()
        u''
        """
        if self._mode == _SKK_WORD_NONE:
            self.startedit()
        elif self._mode == _SKK_WORD_MAIN:
            self._main += value
        else:
            assert self._mode == _SKK_WORD_OKURI
            self._main += value

    def back(self):
        if not self._main:
            self._mode = _SKK_WORD_NONE
        elif self._mode == _SKK_WORD_MAIN:
            self._main = self._main[:-1]
        else:
            assert self._mode == _SKK_WORD_OKURI
            self._mode = _SKK_WORD_MAIN

    def startedit(self):
        self._mode = _SKK_WORD_MAIN

    def startokuri(self):
        self._mode = _SKK_WORD_OKURI

    def has_okuri(self):
        return self._mode == _SKK_WORD_OKURI

    def length(self):
        r"""
        >>> from canossa import termprop
        >>> termprop = termprop.MockTermprop()
        >>> wordbuf = WordBuffer(termprop)
        >>> wordbuf.length()
        0
        >>> wordbuf.startedit()
        >>> wordbuf.length()
        0
        >>> wordbuf.append(u'\u3060')
        >>> wordbuf.length()
        2
        >>> wordbuf.startokuri()
        >>> wordbuf.length()
        2
        >>> wordbuf.append(u'\u3060')
        >>> wordbuf.length()
        4
        """
        if self._mode == _SKK_WORD_NONE:
            return 0
        elif self._mode == _SKK_WORD_MAIN:
            return self._wcswidth(self._main)
        else:
            assert self._mode == _SKK_WORD_OKURI
            return self._wcswidth(self._main)

    def getbuffer(self):
        r"""
        >>> from canossa import termprop
        >>> termprop = termprop.MockTermprop()
        >>> wordbuf = WordBuffer(termprop)
        >>> wordbuf.getbuffer()
        u''
        >>> wordbuf.startedit()
        >>> wordbuf.getbuffer()
        u'\u25bd'
        >>> wordbuf.append(u'\u3060')
        >>> wordbuf.getbuffer()
        u'\u25bd\u3060'
        >>> wordbuf.startokuri()
        >>> wordbuf.getbuffer()
        u'\u25bd\u3060*'
        """
        if self.isempty():
            return ''
        elif self.has_okuri():
            return self._cookmark + self.get() + _SKK_MARK_OKURI
        return self._cookmark + self.get()


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()