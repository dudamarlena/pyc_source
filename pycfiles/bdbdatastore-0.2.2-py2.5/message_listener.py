# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/google/protobuf/internal/message_listener.py
# Compiled at: 2009-12-02 20:07:05
"""Defines a listener interface for observing certain
state transitions on Message objects.

Also defines a null implementation of this interface.
"""
__author__ = 'robinson@google.com (Will Robinson)'

class MessageListener(object):
    """Listens for transitions to nonempty and for invalidations of cached
  byte sizes.  Meant to be registered via Message._SetListener().
  """

    def TransitionToNonempty(self):
        """Called the *first* time that this message becomes nonempty.
    Implementations are free (but not required) to call this method multiple
    times after the message has become nonempty.
    """
        raise NotImplementedError

    def ByteSizeDirty(self):
        """Called *every* time the cached byte size value
    for this object is invalidated (transitions from being
    "clean" to "dirty").
    """
        raise NotImplementedError


class NullMessageListener(object):
    """No-op MessageListener implementation."""

    def TransitionToNonempty(self):
        pass

    def ByteSizeDirty(self):
        pass