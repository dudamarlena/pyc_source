# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/csi.py
# Compiled at: 2014-07-01 10:29:06
import seqdb, template
_DB = seqdb.get()

def get_mnemonic(direction, prefix, p, i, f):
    """
      >>> _create_mock_db()
      >>> get_mnemonic('<', '?', '1;2', '', 'c')
      'DA1 Response'
      >>> get_mnemonic('<', '', '32;41;42', '', 'M')
      'urxvt (1015) mouse reporting (code=(32-32),row=41,col=42)'
    """
    global _DB
    params = p.split(';')
    if len(p) == 0 or len(p) == len(prefix):
        length = 0
    else:
        key = '%s CSI %s%s%s' % (direction, p, i, f)
        if key in _DB:
            return _DB[key]
        length = len(params)
    key = '%s CSI %s[%s]%s%s' % (direction, prefix, length, i, f)
    if key in _DB:
        if length > 0:
            return _DB[key] % tuple(params)
        else:
            return _DB[key]
    if length > 1:
        for x in xrange(0, length):
            pbytes = (';').join(params[:x])
            key = '%s CSI %s;[%s]%s%s' % (direction, pbytes, length - x, i, f)
            if key in _DB:
                return _DB[key] % tuple(params[x:])

    key = '%s CSI %s%s%s' % (direction, prefix, i, f)
    if key in _DB:
        return _DB[key]
    return '<Unknown>'


def format_seq(parameter, intermediate, final, is_input, tracer, controller):
    """
      >>> _create_mock_db()
      >>> template.disable_color()
      >>> format_seq([0x3f, 0x31, 0x3b, 0x32], [], 0x63, True, None, None)
      ' CSI ?1;2c    DA1 Response'
    """
    p = ('').join([ chr(c) for c in parameter ])
    i = ('').join([ chr(c) for c in intermediate ]).replace(' ', '<SP>')
    f = chr(final)
    if is_input:
        direction = '<'
    else:
        direction = '>'
    if p and p[0] > ';':
        prefix = p[0]
    else:
        prefix = ''
    mnemonic = get_mnemonic(direction, prefix, p, i, f)
    if mnemonic[0] == '!':
        return eval(mnemonic[1:])
    return template.getcsi() % (p, i, f, mnemonic)


def _create_mock_db():
    global _DB
    _DB = {'< CSI A': 'Cursor key(normal keypad): up arrow', 
       '< CSI 1;5A': 'Cursor key (xterm): Ctrl + up arrow', 
       '< CSI [0]M': 'xterm normal mouse reporting, following 3 bytes mean (code, row, col)', 
       '< CSI [3]M': 'urxvt (1015) mouse reporting (code=(%s-32),row=%s,col=%s)', 
       '< CSI ?c': 'DA1 Response', 
       '< CSI >0;95;c': 'DA2 Response: xterm patch#95 (could be iTerm/iTerm2)', 
       '> CSI @': 'ICH / insert blank characters', 
       '> CSI [2]H': 'CUP / move cursor to (row=%s, col=%s)', 
       '> CSI >2T': 'Title Mode - Reset (xterm) 2: Do not set window/icon labels using UTF-8'}


if __name__ == '__main__':
    import doctest
    doctest.testmod()