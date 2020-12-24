# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flap\substitutions\comments.py
# Compiled at: 2016-09-27 12:05:26
# Size of source mod 2**32: 1229 bytes
from re import sub
from flap.substitutions.commons import ProcessorDecorator

class CommentsRemover(ProcessorDecorator):
    __doc__ = '\n    Remove the comments from the LaTeX source (i.e., replace them by nothing)\n    '

    def __init__(self, delegate):
        super().__init__(delegate)

    def fragments(self):
        for each_fragment in self._delegate.fragments():
            without_comments = sub('(?: *)(?<!\\\\|\\|)%(?:[^\\n]*)\\n', '', each_fragment.text())
            each_fragment._text = without_comments
            yield each_fragment