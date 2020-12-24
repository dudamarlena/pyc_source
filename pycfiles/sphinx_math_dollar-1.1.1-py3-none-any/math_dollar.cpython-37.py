# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aaronmeurer/Documents/sphinx-math-dollar/build/lib/sphinx_math_dollar/math_dollar.py
# Compiled at: 2019-09-17 14:55:11
# Size of source mod 2**32: 2459 bytes
import re

def split_dollars(text):
    r"""
    Split text into text and math segments.

    Returns a list of tuples ``(type, text)``, where ``type`` is either
    ``"text"`` or ``"math"`` and ``text`` is the text.

    Example:

    >>> split_dollars(r"The functions $\sin(x)$ and $\cos(x)$.")
    [('text', 'The functions '), ('math', '\\sin(x)'), ('text', ' and '),
    ('math', '\\cos(x)'), ('text', '.')]

    More precisely, do a regular expression search.  To match as math, the
    first character after the first $ should not be a space. This is to avoid
    false positives with things like

    $ cd ~
    $ ls

    Escaped dollars (\$) are also not matched as math delimiters, however all
    escaped dollars are replaced with normal dollars in the final output.

    Math is allowed to be split across multiple lines, as its assumed the
    dollars will appear in places like docstrings where line wrapping is
    desired.

    This also doesn't replaces dollar signs enclosed in curly braces,
    to avoid nested math environments, such as ::

      $f(n) = 0 \text{ if $n$ is prime}$

    Thus the above line would get matched fully as math.

    """
    _data = {}

    def repl(matchobj):
        s = matchobj.group(0)
        t = '___XXX_REPL_%d___' % len(_data)
        _data[t] = s
        return t

    text = re.sub('({[^{}$]*\\$[^{}$]*\\$[^{}]*})', repl, text)
    dollars = re.compile('(?<!\\$)(?<!\\\\)\\$([^\\$ ](?:(?<=\\\\)\\$|[^\\$])*?)(?<!\\\\)\\$')
    res = []
    start = 0
    end = len(text)

    def _add_fragment(t, typ):
        t = t.replace('\\$', '$')
        for r in _data:
            t = t.replace(r, _data[r])

        if t:
            res.append((typ, t))

    for m in dollars.finditer(text):
        text_fragment = text[start:m.start()]
        math_fragment = m.group(1)
        start = m.end()
        _add_fragment(text_fragment, 'text')
        _add_fragment(math_fragment, 'math')

    _add_fragment(text[start:end], 'text')
    return res