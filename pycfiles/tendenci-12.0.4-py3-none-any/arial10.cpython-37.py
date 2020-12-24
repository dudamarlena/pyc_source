# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/model_report/arial10.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 4582 bytes
"""
Character width dictionary and convenience functions for column sizing
with xlwt when Arial 10 is the standard font.  Widths were determined
experimentally using Excel 2000 on Windows XP.  I have no idea how well
these will work on other setups.  For example, I don't know if system
video settings will affect the results.  I do know for sure that this
module won't be applicable to other fonts in general.

//John Yeung  2009-09-02
"""
charwidths = {'0':262.637, 
 '1':262.637, 
 '2':262.637, 
 '3':262.637, 
 '4':262.637, 
 '5':262.637, 
 '6':262.637, 
 '7':262.637, 
 '8':262.637, 
 '9':262.637, 
 'a':262.637, 
 'b':262.637, 
 'c':262.637, 
 'd':262.637, 
 'e':262.637, 
 'f':146.015, 
 'g':262.637, 
 'h':262.637, 
 'i':117.096, 
 'j':88.178, 
 'k':233.244, 
 'l':88.178, 
 'm':379.259, 
 'n':262.637, 
 'o':262.637, 
 'p':262.637, 
 'q':262.637, 
 'r':175.407, 
 's':233.244, 
 't':117.096, 
 'u':262.637, 
 'v':203.852, 
 'w':321.422, 
 'x':203.852, 
 'y':262.637, 
 'z':233.244, 
 'A':321.422, 
 'B':321.422, 
 'C':350.341, 
 'D':350.341, 
 'E':321.422, 
 'F':291.556, 
 'G':350.341, 
 'H':321.422, 
 'I':146.015, 
 'J':262.637, 
 'K':321.422, 
 'L':262.637, 
 'M':379.259, 
 'N':321.422, 
 'O':350.341, 
 'P':321.422, 
 'Q':350.341, 
 'R':321.422, 
 'S':321.422, 
 'T':262.637, 
 'U':321.422, 
 'V':321.422, 
 'W':496.356, 
 'X':321.422, 
 'Y':321.422, 
 'Z':262.637, 
 ' ':146.015, 
 '!':146.015, 
 '"':175.407, 
 '#':262.637, 
 '$':262.637, 
 '%':438.044, 
 '&':321.422, 
 "'":88.178, 
 '(':175.407, 
 ')':175.407, 
 '*':203.852, 
 '+':291.556, 
 ',':146.015, 
 '-':175.407, 
 '.':146.015, 
 '/':146.015, 
 ':':146.015, 
 ';':146.015, 
 '<':291.556, 
 '=':291.556, 
 '>':291.556, 
 '?':262.637, 
 '@':496.356, 
 '[':146.015, 
 '\\':146.015, 
 ']':146.015, 
 '^':203.852, 
 '_':262.637, 
 '`':175.407, 
 '{':175.407, 
 '|':146.015, 
 '}':175.407, 
 '~':291.556}

def colwidth(n):
    """Translate human-readable units to BIFF column width units"""
    if n <= 0:
        return 0
    if n <= 1:
        return n * 456
    return 200 + n * 256


def fitwidth(data, bold=False):
    """Try to autofit Arial 10"""
    maxunits = 0
    for ndata in data.split('\n'):
        units = 220
        for char in ndata:
            if char in charwidths:
                units += charwidths[char]
            else:
                units += charwidths['0']

        if maxunits < units:
            maxunits = units

    if bold:
        maxunits *= 1.1
    return max(maxunits, 700)


def fitheight(data, bold=False):
    """Try to autofit Arial 10"""
    rowlen = len(data.split('\n'))
    if rowlen > 1:
        units = 230 * rowlen
    else:
        units = 290
    if bold:
        units *= 1.1
    return int(units)