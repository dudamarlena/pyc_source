# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/kanadb.py
# Compiled at: 2014-03-11 11:41:30
_kanadb = (
 ('あ', 'ア', 'ｱ'),
 ('い', 'イ', 'ｲ'),
 ('う', 'ウ', 'ｳ'),
 ('え', 'エ', 'ｴ'),
 ('お', 'オ', 'ｵ'),
 ('ぁ', 'ァ', 'ｧ'),
 ('ぃ', 'ィ', 'ｨ'),
 ('ぅ', 'ゥ', 'ｩ'),
 ('ぇ', 'ェ', 'ｪ'),
 ('ぉ', 'ォ', 'ｫ'),
 ('か', 'カ', 'ｶ'),
 ('き', 'キ', 'ｷ'),
 ('く', 'ク', 'ｸ'),
 ('け', 'ケ', 'ｹ'),
 ('こ', 'コ', 'ｺ'),
 ('が', 'ガ', 'ｶﾞ'),
 ('ぎ', 'ギ', 'ｷﾞ'),
 ('ぐ', 'グ', 'ｸﾞ'),
 ('げ', 'ゲ', 'ｹﾞ'),
 ('ご', 'ゴ', 'ｺﾞ'),
 ('さ', 'サ', 'ｻ'),
 ('し', 'シ', 'ｼ'),
 ('す', 'ス', 'ｽ'),
 ('せ', 'セ', 'ｾ'),
 ('そ', 'ソ', 'ｿ'),
 ('ざ', 'ザ', 'ｻﾞ'),
 ('じ', 'ジ', 'ｼﾞ'),
 ('ず', 'ズ', 'ｽﾞ'),
 ('ぜ', 'ゼ', 'ｾﾞ'),
 ('ぞ', 'ゾ', 'ｿﾞ'),
 ('た', 'タ', 'ﾀ'),
 ('ち', 'チ', 'ﾁ'),
 ('つ', 'ツ', 'ﾂ'),
 ('て', 'テ', 'ﾃ'),
 ('と', 'ト', 'ﾄ'),
 ('だ', 'ダ', 'ﾀﾞ'),
 ('ぢ', 'ヂ', 'ﾁﾞ'),
 ('づ', 'ヅ', 'ﾂﾞ'),
 ('で', 'デ', 'ﾃﾞ'),
 ('ど', 'ド', 'ﾄﾞ'),
 ('な', 'ナ', 'ﾅ'),
 ('に', 'ニ', 'ﾆ'),
 ('ぬ', 'ヌ', 'ﾇ'),
 ('ね', 'ネ', 'ﾈ'),
 ('の', 'ノ', 'ﾉ'),
 ('は', 'ハ', 'ﾊ'),
 ('ひ', 'ヒ', 'ﾋ'),
 ('ふ', 'フ', 'ﾌ'),
 ('へ', 'ヘ', 'ﾍ'),
 ('ほ', 'ホ', 'ﾎ'),
 ('ぱ', 'パ', 'ﾊﾟ'),
 ('ぴ', 'ピ', 'ﾋﾟ'),
 ('ぷ', 'プ', 'ﾌﾟ'),
 ('ぺ', 'ペ', 'ﾍﾟ'),
 ('ぽ', 'ポ', 'ﾎﾟ'),
 ('ば', 'バ', 'ﾊﾞ'),
 ('び', 'ビ', 'ﾋﾞ'),
 ('ぶ', 'ブ', 'ﾌﾞ'),
 ('べ', 'ベ', 'ﾍﾞ'),
 ('ぼ', 'ボ', 'ﾎﾞ'),
 ('ま', 'マ', 'ﾏ'),
 ('み', 'ミ', 'ﾐ'),
 ('む', 'ム', 'ﾑ'),
 ('め', 'メ', 'ﾒ'),
 ('も', 'モ', 'ﾓ'),
 ('や', 'ヤ', 'ﾔ'),
 ('ゆ', 'ユ', 'ﾕ'),
 ('よ', 'ヨ', 'ﾖ'),
 ('ら', 'ラ', 'ﾗ'),
 ('り', 'リ', 'ﾘ'),
 ('る', 'ル', 'ﾙ'),
 ('れ', 'レ', 'ﾚ'),
 ('ろ', 'ロ', 'ﾛ'),
 ('わ', 'ワ', 'ﾜ'),
 ('を', 'ヲ', 'ｦ'),
 ('っ', 'ッ', 'ｯ'),
 ('ゃ', 'ャ', 'ｬ'),
 ('ゅ', 'ュ', 'ｭ'),
 ('ょ', 'ョ', 'ｮ'),
 ('ん', 'ン', 'ﾝ'))
_to_kata = {}
_to_hira = {}
_to_hankata = {}

def compile():
    for (hira, kata, hankata) in _kanadb:
        _to_kata[hira] = kata
        _to_hira[kata] = hira
        _to_hankata[hira] = hankata
        _to_hankata[kata] = hankata


def to_kata(s):
    r"""
    convert Japanese Hiragana String to Katakana

    >>> to_kata(u"\u3042\u3044\u3046\u3048\u304a") == u'\u30a2\u30a4\u30a6\u30a8\u30aa'
    True
    >>> to_kata(u"\u30a2\u30a4\u30a6\u30a8\u30aa") == u'\u30a2\u30a4\u30a6\u30a8\u30aa'
    True
    """

    def conv(c):
        if c in _to_kata:
            return _to_kata[c]
        return c

    return ('').join([ conv(c) for c in s ])


def to_hira(s):
    r"""
    convert Japanese Katakana String to Hiragana

    >>> to_hira(u'\u3042\u3044\u3046\u3048\u304a') == u'\u3042\u3044\u3046\u3048\u304a'
    True
    >>> to_hira(u'\u30a2\u30a4\u30a6\u30a8\u30aa') == u'\u3042\u3044\u3046\u3048\u304a'
    True
    """

    def conv(c):
        if c in _to_hira:
            return _to_hira[c]
        return c

    return ('').join([ conv(c) for c in s ])


def to_hankata(s):
    r"""
    convert Japanese Kana String to Half-Width-Katakana

    >>> to_hankata(u'\u3042\u3044\u3046\u3048\u304a') == u'\uff71\uff72\uff73\uff74\uff75'
    True
    >>> to_hankata(u'\u30a2\u30a4\u30a6\u30a8\u30aa') == u'\uff71\uff72\uff73\uff74\uff75'
    True
    """

    def conv(c):
        if c in _to_hankata:
            return _to_hankata[c]
        return c

    return ('').join([ conv(c) for c in s ])


compile()

def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()