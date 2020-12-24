# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/completion.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 5724 bytes
"""
"""
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
__all__ = ('Completion', 'Completer', 'CompleteEvent', 'get_common_complete_suffix')

class Completion(object):
    __doc__ = "\n    :param text: The new string that will be inserted into the document.\n    :param start_position: Position relative to the cursor_position where the\n        new text will start. The text will be inserted between the\n        start_position and the original cursor position.\n    :param display: (optional string) If the completion has to be displayed\n        differently in the completion menu.\n    :param display_meta: (Optional string) Meta information about the\n        completion, e.g. the path or source where it's coming from.\n    :param get_display_meta: Lazy `display_meta`. Retrieve meta information\n        only when meta is displayed.\n    "

    def __init__(self, text, start_position=0, display=None, display_meta=None, get_display_meta=None):
        self.text = text
        self.start_position = start_position
        self._display_meta = display_meta
        self._get_display_meta = get_display_meta
        if display is None:
            self.display = text
        else:
            self.display = display
        assert self.start_position <= 0

    def __repr__(self):
        if self.display == self.text:
            return '%s(text=%r, start_position=%r)' % (
             self.__class__.__name__, self.text, self.start_position)
        else:
            return '%s(text=%r, start_position=%r, display=%r)' % (
             self.__class__.__name__, self.text, self.start_position,
             self.display)

    def __eq__(self, other):
        return self.text == other.text and self.start_position == other.start_position and self.display == other.display and self.display_meta == other.display_meta

    def __hash__(self):
        return hash((self.text, self.start_position, self.display, self.display_meta))

    @property
    def display_meta(self):
        if self._display_meta is not None:
            return self._display_meta
        else:
            if self._get_display_meta:
                self._display_meta = self._get_display_meta()
                return self._display_meta
            return ''

    def new_completion_from_position(self, position):
        """
        (Only for internal use!)
        Get a new completion by splitting this one. Used by
        `CommandLineInterface` when it needs to have a list of new completions
        after inserting the common prefix.
        """
        assert isinstance(position, int) and position - self.start_position >= 0
        return Completion(text=(self.text[position - self.start_position:]),
          display=(self.display),
          display_meta=(self._display_meta),
          get_display_meta=(self._get_display_meta))


class CompleteEvent(object):
    __doc__ = '\n    Event that called the completer.\n\n    :param text_inserted: When True, it means that completions are requested\n        because of a text insert. (`Buffer.complete_while_typing`.)\n    :param completion_requested: When True, it means that the user explicitely\n        pressed the `Tab` key in order to view the completions.\n\n    These two flags can be used for instance to implemented a completer that\n    shows some completions when ``Tab`` has been pressed, but not\n    automatically when the user presses a space. (Because of\n    `complete_while_typing`.)\n    '

    def __init__(self, text_inserted=False, completion_requested=False):
        assert not (text_inserted and completion_requested)
        self.text_inserted = text_inserted
        self.completion_requested = completion_requested

    def __repr__(self):
        return '%s(text_inserted=%r, completion_requested=%r)' % (
         self.__class__.__name__, self.text_inserted, self.completion_requested)


class Completer(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    Base class for completer implementations.\n    '

    @abstractmethod
    def get_completions(self, document, complete_event):
        """
        Yield :class:`.Completion` instances.

        :param document: :class:`~prompt_tool_kit.document.Document` instance.
        :param complete_event: :class:`.CompleteEvent` instance.
        """
        pass
        if False:
            yield None


def get_common_complete_suffix(document, completions):
    """
    Return the common prefix for all completions.
    """

    def doesnt_change_before_cursor(completion):
        end = completion.text[:-completion.start_position]
        return document.text_before_cursor.endswith(end)

    completions2 = [c for c in completions if doesnt_change_before_cursor(c)]
    if len(completions2) != len(completions):
        return ''
    else:

        def get_suffix(completion):
            return completion.text[-completion.start_position:]

        return _commonprefix([get_suffix(c) for c in completions2])


def _commonprefix(strings):
    if not strings:
        return ''
    else:
        s1 = min(strings)
        s2 = max(strings)
        for i, c in enumerate(s1):
            if c != s2[i]:
                return s1[:i]

        return s1