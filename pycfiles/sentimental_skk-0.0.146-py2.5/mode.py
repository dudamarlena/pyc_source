# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/mode.py
# Compiled at: 2014-03-11 11:41:30
import title
from canossa import IModeListenerImpl
import settings
_SKK_MODE_HANKAKU = 0
_SKK_MODE_ZENKAKU = 1
_SKK_MODE_HIRAGANA = 2
_SKK_MODE_KATAKANA = 3
_SKK_SUBMODE_ABBREV = 4
_SKK_MODE_MARK_MAP = {_SKK_MODE_HANKAKU: 'SKK', _SKK_MODE_ZENKAKU: '全英', 
   _SKK_MODE_HIRAGANA: 'かな', 
   _SKK_MODE_KATAKANA: 'カナ', 
   _SKK_SUBMODE_ABBREV: 'Aあ'}
import eisuudb

class InputMode(IModeListenerImpl):
    """
    モードの管理をします。
    """
    _value = -1

    def __init__(self, session):
        self._session = session
        self._setmode(_SKK_MODE_HANKAKU)

    def _setmode(self, mode):
        if self._value != mode:
            self._value = mode
            if self.hasevent():
                process = self._session.getactiveprocess()
                if self.isabbrev():
                    process.write('\x1b[8854~')
                else:
                    process.write('\x1b[%d~' % (8850 + self._value))
        title.setmode(_SKK_MODE_MARK_MAP[min(mode, 4)])

    def handle_char(self, context, c):
        if c == settings.get('skk-j-mode'):
            self.endabbrev()
            if self.ishan():
                self.starthira()
                return True
            elif self.iszen():
                self.starthira()
                return True
        elif self.ishan():
            context.write(c)
            return True
        elif self.iszen():
            context.write(eisuudb.to_zenkaku_cp(c))
            return True
        return False

    def isdirect(self):
        value = self._value
        return value == _SKK_MODE_HANKAKU or value == _SKK_MODE_ZENKAKU

    def reset(self):
        self._setmode(_SKK_MODE_HANKAKU)

    def startabbrev(self):
        u""" 英数サブモードを開始 """
        if self.getenabled():
            self._setmode(self._value | _SKK_SUBMODE_ABBREV)

    def endabbrev(self):
        u""" 英数サブモードを終了 """
        self._setmode(self._value & ~_SKK_SUBMODE_ABBREV)

    def startzen(self):
        u""" 全角英数モードを開始 """
        if self.getenabled():
            self._setmode(_SKK_MODE_ZENKAKU)

    def starthira(self):
        u""" ひらがなモードを開始 """
        if self.getenabled():
            self._setmode(_SKK_MODE_HIRAGANA)

    def startkata(self):
        u""" カタカナモードを開始 """
        if self.getenabled():
            self._setmode(_SKK_MODE_KATAKANA)

    def ishira(self):
        u""" ひらがなモードかどうか """
        return self._value == _SKK_MODE_HIRAGANA

    def iskata(self):
        u""" カタカナモードかどうか """
        return self._value == _SKK_MODE_KATAKANA

    def isabbrev(self):
        return self._value & _SKK_SUBMODE_ABBREV != 0

    def iszen(self):
        return self._value == _SKK_MODE_ZENKAKU

    def ishan(self):
        return self._value == _SKK_MODE_HANKAKU


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()