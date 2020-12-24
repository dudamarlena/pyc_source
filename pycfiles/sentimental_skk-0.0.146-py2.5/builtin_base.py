# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/rule/builtin_base.py
# Compiled at: 2014-06-12 02:32:28
_rule = {'\x00': '@skk-cancel-pass', 
   '\x01': '@skk-cancel-pass', 
   '\x02': '@skk-move-prev-clause', 
   '\x03': '@skk-cancel-pass', 
   '\x04': '@skk-cancel-pass', 
   '\x05': '@skk-cancel-pass', 
   '\x06': '@skk-move-next-clause', 
   '\x07': '@skk-cancel', 
   '\x08': '@skk-back', 
   '\t': '@skkmenu-next', 
   '\n': '@skk-kakutei-key-pass', 
   '\x0b': '@skk-cancel-pass', 
   '\x0c': '@skk-cancel-pass', 
   '\r': '@skk-kakutei-key', 
   '\x0e': '@skkmenu-next', 
   '\x0f': '@skk-cancel-pass', 
   '\x10': '@skkmenu-prev', 
   '\x11': '@skk-set-henkan-point-subr', 
   '\x12': '@skk-cancel-pass', 
   '\x13': '@skk-cancel-pass', 
   '\x14': '@skk-cancel-pass', 
   '\x15': '@skk-cancel-pass', 
   '\x16': '@skk-cancel-pass', 
   '\x17': '@skkapp-wikipedia', 
   '\x18': '@skk-delete-candidate', 
   '\x19': '@skk-cancel-pass', 
   '\x1a': '@skk-cancel-pass', 
   '\x1b': '@skk-j-mode-off', 
   '\x1c': '@skk-cancel-pass', 
   '\x1d': '@skk-cancel-pass', 
   '\x1e': '@skk-cancel-pass', 
   '\x1f': '@skk-cancel-pass', 
   ' ': '@skk-henkan', 
   '\x7f': '@skk-back', 
   '/': '@skk-abbrev-mode', 
   'l': '@skk-j-mode-off', 
   'q': '@skk-toggle-kana', 
   'L': '@skk-start-eisuu', 
   'wws': '@skkwm-switch', 
   'wwn': '@skkwm-next', 
   'wwp': '@skkwm-prev', 
   'wwd': '@skkwm-blur', 
   'wwh': '@skkwm-left', 
   'wwj': '@skkwm-down', 
   'wwk': '@skkwm-up', 
   'wwl': '@skkwm-right', 
   'w4': '@skksh-start', 
   '$': '@skksh-start', 
   '@': '@skkconf-start'}

def get():
    """
    >>> name, rule = get()
    """
    return (
     'base', _rule)


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()