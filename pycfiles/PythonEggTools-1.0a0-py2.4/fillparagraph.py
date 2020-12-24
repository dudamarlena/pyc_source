# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pet/fillparagraph.py
# Compiled at: 2006-12-21 09:20:10
"""Contains a function to do word-wrapping on text paragraphs."""
__version__ = '0.1'
__author__ = 'Christopher Arndt <chris.arndt@web.de'
import re, random

def justify_line(line, width):
    """Stretch a line to width by filling in spaces at word gaps.

    The gaps are picked randomly one-after-another, before it starts
    over again.

    """
    i = []
    while 1:
        if len((' ').join(line)) < width:
            if not i:
                i = range(max(1, len(line) - 1))
                random.shuffle(i)
            line[i.pop(0)] += ' '
        else:
            return (' ').join(line)


def fill_paragraphs(text, width=80, justify=0):
    """Split a text into paragraphs and wrap them to width linelength.

    Optionally justify the paragraphs (i.e. stretch lines to fill width).

    Inter-word space is reduced to one space character and paragraphs are
    always separated by two newlines. Indention is currently also lost.

    """
    paragraphs = re.split('\\n[ \\t]*\\n+', text)
    for i in range(len(paragraphs)):
        words = paragraphs[i].strip().split()
        line = []
        new_par = []
        while 1:
            if words:
                if len((' ').join(line + [words[0]])) > width and line:
                    if justify:
                        new_par.append(justify_line(line, width))
                    else:
                        new_par.append((' ').join(line))
                    line = []
                else:
                    line.append(words.pop(0))
            else:
                new_par.append((' ').join(line))
                line = []
                break

        paragraphs[i] = ('\n').join(new_par)

    return ('\n\n').join(paragraphs)


def _test(width=78, justify=1):
    """Module test case."""
    s = '\nThis is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. \nThis is some text. This is some text. This is some text. \n\nThis is some text. This is some text. This is some text. \nThis is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. \nThis is some text. This is some text. \nThis is some text.\n\nThis is some text. \nThis is some text. \nThis is some text. This is some text. \nThis is some text. This is some text. This is some text. \n'
    print fill_paragraphs(s, width, justify)


if __name__ == '__main__':
    _test()