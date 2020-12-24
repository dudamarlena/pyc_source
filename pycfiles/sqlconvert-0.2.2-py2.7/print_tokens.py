# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.7/sqlconvert/print_tokens.py
# Compiled at: 2016-09-26 17:50:29
import sys

def print_tokens(token_list, outfile=sys.stdout, encoding=None):
    if encoding:
        buffer = getattr(outfile, 'buffer', outfile)
    else:
        buffer = outfile
    for token in token_list.flatten():
        normalized = token.normalized
        if encoding:
            normalized = normalized.encode(encoding)
        buffer.write(normalized)

    if buffer is not outfile:
        buffer.flush()
    outfile.flush()


def tlist2str(token_list):
    return ('').join(token.normalized for token in token_list.flatten())