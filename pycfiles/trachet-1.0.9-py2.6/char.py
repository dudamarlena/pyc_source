# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/char.py
# Compiled at: 2014-07-01 10:29:06
import seqdb, template
_DB = seqdb.get()
_CHAR_MAP = {0: '<NUL>', 1: '<SOH>', 
   2: '<STX>', 
   3: '<ETX>', 
   4: '<EOT>', 
   5: '<ENQ>', 
   6: '<ACK>', 
   7: '<BEL>', 
   8: '<BS>', 
   9: '<HT>', 
   10: '<NL>', 
   11: '<VT>', 
   12: '<NP>', 
   13: '<CR>', 
   14: '<SO>', 
   15: '<SI>', 
   16: '<DLE>', 
   17: '<DC1>', 
   18: '<DC2>', 
   19: '<DC3>', 
   20: '<DC4>', 
   21: '<NAK>', 
   22: '<SYN>', 
   23: '<ETB>', 
   24: '<CAN>', 
   25: '<EM>', 
   26: '<SUB>', 
   27: '<ESC>', 
   28: '<FS>', 
   29: '<GS>', 
   30: '<RS>', 
   31: '<US>', 
   32: '<SP>', 
   127: '<DEL>'}

def get_mnemonic(key):
    """
      >>> _create_mock_db()
      >>> get_mnemonic('< <BEL>')
      'BEL / Ctrl-G'
      >>> get_mnemonic('< <DEL>')
      ''
    """
    global _DB
    if key in _DB:
        return _DB[key]
    return ''


def format_seq(c, is_input, tracer, controller):
    """
      >>> _create_mock_db()
      >>> template.enable_color()
      >>> str(format_seq(ord("a"), False, None, None)).replace("\x1b", "\\x1b")
      "(u'\\\\x1b[32ma\\\\x1b[m', False)"
      >>> str(format_seq(ord("\x1b"), False, None, None)).replace("\x1b", "\\x1b")
      "('\\\\x1b[32m<ESC>\\\\x1b[m', False)"
      >>> str(format_seq(ord("\x07"), False, None, None)).replace("\x1b", "\\x1b")
      "('\\\\x1b[31m<BEL>\\\\x1b[1;32m\\\\r\\\\x1b[30CBEL / bell\\\\x1b[m', True)"
    """
    if c in _CHAR_MAP:
        printable_char = _CHAR_MAP[c]
    elif c < 65536:
        printable_char = unichr(c)
    else:
        c -= 65536
        c1 = (c >> 10) + 55296
        c2 = (c & 1023) + 56320
        printable_char = unichr(c1) + unichr(c2)
    if is_input:
        direction = '<'
    else:
        direction = '>'
    key = '%s %s' % (direction, printable_char)
    mnemonic = get_mnemonic(key)
    if mnemonic:
        if mnemonic[0] == '!':
            return eval(mnemonic[1:])
        return (template.getprintablechar() % (printable_char, mnemonic), True)
    return (
     template.getchar() % printable_char, False)


def _create_mock_db():
    global _DB
    _DB = {'< <NUL>': 'NUL / Ctrl-@,Ctrl-SP,Ctrl-2', 
       '< <BEL>': 'BEL / Ctrl-G', 
       '> <NUL>': 'NUL / null character', 
       '> <BEL>': 'BEL / bell'}


if __name__ == '__main__':
    import doctest
    doctest.testmod()