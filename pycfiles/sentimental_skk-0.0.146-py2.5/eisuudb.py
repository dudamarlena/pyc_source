# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/eisuudb.py
# Compiled at: 2014-03-11 11:35:14
_eisuudb = (
 ('0', '０'), ('1', '１'), ('2', '２'),
 ('3', '３'), ('4', '４'), ('5', '５'),
 ('6', '６'), ('7', '７'), ('8', '８'),
 ('9', '９'), ('^', '＾'), ('@', '＠'),
 ('[', '［'), (']', '］'), (':', '：'),
 (';', '；'), (',', '，'), ('.', '．'),
 ('/', '／'), ('_', '＿'), ('*', '＊'),
 ('!', '！'), ('#', '＃'), ('$', '＄'),
 ('%', '％'), ('&', '＆'), ('(', '（'),
 (')', '）'), ('=', '＝'), ('~', '〜'),
 ('|', '｜'), ('{', '｛'), ('}', '｝'),
 ('+', '＋'), ('*', '＊'), ('<', '＜'),
 ('>', '＞'), ('?', '？'), ('A', 'Ａ'),
 ('B', 'Ｂ'), ('C', 'Ｃ'), ('D', 'Ｄ'),
 ('E', 'Ｅ'), ('F', 'Ｆ'), ('G', 'Ｇ'),
 ('H', 'Ｈ'), ('I', 'Ｉ'), ('J', 'Ｊ'),
 ('K', 'Ｋ'), ('L', 'Ｌ'), ('M', 'Ｍ'),
 ('N', 'Ｎ'), ('O', 'Ｏ'), ('P', 'Ｐ'),
 ('Q', 'Ｑ'), ('R', 'Ｒ'), ('S', 'Ｓ'),
 ('T', 'Ｔ'), ('U', 'Ｕ'), ('V', 'Ｖ'),
 ('W', 'Ｗ'), ('X', 'Ｘ'), ('Y', 'Ｙ'),
 ('Z', 'Ｚ'), ('a', 'ａ'), ('b', 'ｂ'),
 ('c', 'ｃ'), ('d', 'ｄ'), ('e', 'ｅ'),
 ('f', 'ｆ'), ('g', 'ｇ'), ('h', 'ｈ'),
 ('i', 'ｉ'), ('j', 'ｊ'), ('k', 'ｋ'),
 ('l', 'ｌ'), ('m', 'ｍ'), ('n', 'ｎ'),
 ('o', 'ｏ'), ('p', 'ｐ'), ('q', 'ｑ'),
 ('r', 'ｒ'), ('s', 'ｓ'), ('t', 'ｔ'),
 ('u', 'ｕ'), ('v', 'ｖ'), ('w', 'ｗ'),
 ('x', 'ｘ'), ('y', 'ｙ'), ('z', 'ｚ'),
 (' ', '\u3000'))
_han_to_zen = {}
_han_to_zen_cp = {}

def _loaddb():
    for (han, zen) in _eisuudb:
        _han_to_zen[han] = zen
        _han_to_zen_cp[ord(han)] = ord(zen)


def to_zenkaku(s):
    r"""
    convert ascii string to Japanese Zenkaku string

    >>> _loaddb()
    >>> to_zenkaku("0")
    u'\uff10'
    >>> to_zenkaku("a")
    u'\uff41'
    >>> to_zenkaku("ABC")
    u'\uff21\uff22\uff23'
    """

    def conv(c):
        if c in _han_to_zen:
            return _han_to_zen[c]
        return c

    return ('').join([ conv(c) for c in s ])


def to_zenkaku_cp(code):
    """
    convert some ascii code points to Japanese Zenkaku code points

    >>> _loaddb()
    >>> hex(to_zenkaku_cp(40))
    '0xff08'
    >>> hex(to_zenkaku_cp(84))
    '0xff34'
    """
    if code in _han_to_zen_cp:
        return _han_to_zen_cp[code]
    return code


try:
    import thread
    thread.start_new_thread(_loaddb, ())
except Exception, e:
    _loaddb()

def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()