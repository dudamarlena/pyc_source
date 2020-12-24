# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/constant2-project/constant2/pkg/superjson/comments.py
# Compiled at: 2018-12-19 11:16:54
__doc__ = '\nThis module can remove these two style ``// comment``, ``# comment`` comments\nfrom code.\n\n---------- Revised BSD License ----------\n\nCopyright (c) 2017, Mark V.\nAll rights reserved.\n\nRedistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions are met:\n    * Redistributions of source code must retain the above copyright\n      notice, this list of conditions and the following disclaimer.\n    * Redistributions in binary form must reproduce the above copyright\n      notice, this list of conditions and the following disclaimer in the\n      documentation and/or other materials provided with the distribution.\n    * Neither the name of the organization nor the\n      names of its contributors may be used to endorse or promote products\n      derived from this software without specific prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\nANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\nWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\nDISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY\nDIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\nLOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND\nON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\nSOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n\nhttps://github.com/mverleg/pyjson_tricks\n'
from re import findall

def strip_comment_line_with_symbol(line, start):
    """Strip comments from line string.
    """
    parts = line.split(start)
    counts = [ len(findall('(?:^|[^"\\\\]|(?:\\\\\\\\|\\\\")+)(")', part)) for part in parts
             ]
    total = 0
    for nr, count in enumerate(counts):
        total += count
        if total % 2 == 0:
            return start.join(parts[:nr + 1]).rstrip()
    else:
        return line.rstrip()


def strip_comments(string, comment_symbols=frozenset(('#', '//'))):
    """Strip comments from json string.

    :param string: A string containing json with comments started by comment_symbols.
    :param comment_symbols: Iterable of symbols that start a line comment (default # or //).
    :return: The string with the comments removed.
    """
    lines = string.splitlines()
    for k in range(len(lines)):
        for symbol in comment_symbols:
            lines[k] = strip_comment_line_with_symbol(lines[k], start=symbol)

    return ('\n').join(lines)