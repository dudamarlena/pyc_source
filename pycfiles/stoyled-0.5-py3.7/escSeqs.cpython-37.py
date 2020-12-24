# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/stoyled/escSeqs.py
# Compiled at: 2020-04-22 18:36:09
# Size of source mod 2**32: 752 bytes


def genEscSeqs(stylSeq, preNum=''):
    count = 1
    out = ''
    if preNum:
        postStyl = ''
        if int(preNum) == 9:
            postStyl = '_l'
        for _ in stylSeq:
            _ += postStyl
            out += f"{_} = '\\x1b[{preNum}{count}m'\n"
            count += 1

    else:
        for _ in stylSeq:
            out += f"{_} = '\\x1b[{count}m'\n"
            count += 1

    return out


STYLS = ('bold', 'dim', 'italic', 'uline', 'blink', 'normal', 'invert', 'hidden', 'strike')
COLRS = ('red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white')
exec(genEscSeqs(STYLS))
exec(genEscSeqs(COLRS, 3))
exec(genEscSeqs(COLRS, 9))
rst = '\x1b[0m'