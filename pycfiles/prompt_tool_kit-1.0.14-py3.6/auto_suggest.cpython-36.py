# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/auto_suggest.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 2844 bytes
"""
`Fish-style <http://fishshell.com/>`_  like auto-suggestion.

While a user types input in a certain buffer, suggestions are generated
(asynchronously.) Usually, they are displayed after the input. When the cursor
presses the right arrow and the cursor is at the end of the input, the
suggestion will be inserted.
"""
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from .filters import to_cli_filter
__all__ = ('Suggestion', 'AutoSuggest', 'AutoSuggestFromHistory', 'ConditionalAutoSuggest')

class Suggestion(object):
    __doc__ = '\n    Suggestion returned by an auto-suggest algorithm.\n\n    :param text: The suggestion text.\n    '

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Suggestion(%s)' % self.text


class AutoSuggest(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    Base class for auto suggestion implementations.\n    '

    @abstractmethod
    def get_suggestion(self, cli, buffer, document):
        """
        Return `None` or a :class:`.Suggestion` instance.

        We receive both ``buffer`` and ``document``. The reason is that auto
        suggestions are retrieved asynchronously. (Like completions.) The
        buffer text could be changed in the meantime, but ``document`` contains
        the buffer document like it was at the start of the auto suggestion
        call. So, from here, don't access ``buffer.text``, but use
        ``document.text`` instead.

        :param buffer: The :class:`~prompt_tool_kit.buffer.Buffer` instance.
        :param document: The :class:`~prompt_tool_kit.document.Document` instance.
        """
        pass


class AutoSuggestFromHistory(AutoSuggest):
    __doc__ = '\n    Give suggestions based on the lines in the history.\n    '

    def get_suggestion(self, cli, buffer, document):
        history = buffer.history
        text = document.text.rsplit('\n', 1)[(-1)]
        if text.strip():
            for string in reversed(list(history)):
                for line in reversed(string.splitlines()):
                    if line.startswith(text):
                        return Suggestion(line[len(text):])


class ConditionalAutoSuggest(AutoSuggest):
    __doc__ = '\n    Auto suggest that can be turned on and of according to a certain condition.\n    '

    def __init__(self, auto_suggest, filter):
        assert isinstance(auto_suggest, AutoSuggest)
        self.auto_suggest = auto_suggest
        self.filter = to_cli_filter(filter)

    def get_suggestion(self, cli, buffer, document):
        if self.filter(cli):
            return self.auto_suggest.get_suggestion(cli, buffer, document)