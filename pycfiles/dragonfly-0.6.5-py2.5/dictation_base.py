# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\engines\dictation_base.py
# Compiled at: 2009-04-06 11:18:28
"""
Dictation container base class
============================================================================

This class is used to store the recognized results of dictation elements 
within voice-commands.  It offers access to both the raw spoken-form words 
and be formatted written-form text.

The formatted text can be retrieved using :meth:`.format` or simply by 
calling ``str(...)`` on a dictation container object. A tuple of the raw 
spoken words can be retrieved using :meth:`.words`.

"""

class DictationContainerBase(object):
    """
        Container class for dictated words as recognized by the
        :class:`Dictation` element.

        This base class implements the general functionality of dictation 
        container classes.  Each supported engine should have a derived 
        dictation container class which performs the actual engine-
        specific formatting of dictated text.

    """

    def __init__(self, words):
        self._words = tuple(words)
        self._formatted = None
        return

    def __str__(self):
        if self._formatted is None:
            self._formatted = self.format()
        return self._formatted

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, (', ').join(self._words))

    @property
    def words(self):
        """ Sequence of the words forming this dictation. """
        return self._words

    def format(self):
        """ Format and return this dictation. """
        return (' ').join(self._words)