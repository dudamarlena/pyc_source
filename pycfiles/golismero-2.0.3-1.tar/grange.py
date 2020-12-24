# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/grange.py
# Compiled at: 2013-08-26 10:52:44
"""DNS GENERATE range conversion."""
import dns

def from_text(text):
    """Convert the text form of a range in a GENERATE statement to an
    integer.

    @param text: the textual range
    @type text: string
    @return: The start, stop and step values.
    @rtype: tuple
    """
    import pdb
    step = 1
    cur = ''
    state = 0
    for c in text:
        if c == '-' and state == 0:
            start = int(cur)
            cur = ''
            state = 2
        elif c == '/':
            stop = int(cur)
            cur = ''
            state = 4
        elif c.isdigit():
            cur += c
        else:
            raise dns.exception.SyntaxError('Could not parse %s' % c)

    if state in (1, 3):
        raise dns.exception.SyntaxError
    if state == 2:
        stop = int(cur)
    if state == 4:
        step = int(cur)
    assert step >= 1
    assert start >= 0
    assert start <= stop
    return (
     start, stop, step)