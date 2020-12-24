# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/auto_suggest.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 2844 bytes
__doc__ = '\n`Fish-style <http://fishshell.com/>`_  like auto-suggestion.\n\nWhile a user types input in a certain buffer, suggestions are generated\n(asynchronously.) Usually, they are displayed after the input. When the cursor\npresses the right arrow and the cursor is at the end of the input, the\nsuggestion will be inserted.\n'
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from .filters import to_cli_filter
__all__ = ('Suggestion', 'AutoSuggest', 'AutoSuggestFromHistory', 'ConditionalAutoSuggest')

class Suggestion(object):
    """Suggestion"""

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Suggestion(%s)' % self.text


class AutoSuggest(with_metaclass(ABCMeta, object)):
    """AutoSuggest"""

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
    """AutoSuggestFromHistory"""

    def get_suggestion(self, cli, buffer, document):
        history = buffer.history
        text = document.text.rsplit('\n', 1)[(-1)]
        if text.strip():
            for string in reversed(list(history)):
                for line in reversed(string.splitlines()):
                    if line.startswith(text):
                        return Suggestion(line[len(text):])


class ConditionalAutoSuggest(AutoSuggest):
    """ConditionalAutoSuggest"""

    def __init__(self, auto_suggest, filter):
        assert isinstance(auto_suggest, AutoSuggest)
        self.auto_suggest = auto_suggest
        self.filter = to_cli_filter(filter)

    def get_suggestion(self, cli, buffer, document):
        if self.filter(cli):
            return self.auto_suggest.get_suggestion(cli, buffer, document)