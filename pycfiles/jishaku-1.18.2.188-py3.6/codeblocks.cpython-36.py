# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/codeblocks.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 1895 bytes
"""
jishaku.codeblocks
~~~~~~~~~~~~~~~~~~

Converters for detecting and obtaining codeblock content

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import collections
__all__ = ('Codeblock', 'codeblock_converter')
Codeblock = collections.namedtuple('Codeblock', 'language content')

def codeblock_converter(argument):
    """
    A converter that strips codeblock markdown if it exists.

    Returns a namedtuple of (language, content).

    :attr:`Codeblock.language` is an empty string if no language was given with this codeblock.
    It is ``None`` if the input was not a complete codeblock.
    """
    if not argument.startswith('`'):
        return Codeblock(None, argument)
    else:
        last = collections.deque(maxlen=3)
        backticks = 0
        in_language = False
        in_code = False
        language = []
        code = []
        for char in argument:
            if char == '`':
                if not in_code:
                    if not in_language:
                        backticks += 1
            else:
                if last and last[(-1)] == '`' and char != '`' or in_code and ''.join(last) != '`' * backticks:
                    in_code = True
                    code.append(char)
                if char == '\n':
                    in_language = False
                    in_code = True
                else:
                    if ''.join(last) == '```' and char != '`':
                        in_language = True
                        language.append(char)
            if in_language:
                if char != '\n':
                    language.append(char)
            last.append(char)

        if not code:
            if not language:
                code[:] = last
        return Codeblock(''.join(language), ''.join(code[len(language):-backticks]))