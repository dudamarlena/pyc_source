# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/message_listener.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 3367 bytes
"""Defines a listener interface for observing certain
state transitions on Message objects.

Also defines a null implementation of this interface.
"""
__author__ = 'robinson@google.com (Will Robinson)'

class MessageListener(object):
    __doc__ = 'Listens for modifications made to a message.  Meant to be registered via\n  Message._SetListener().\n\n  Attributes:\n    dirty:  If True, then calling Modified() would be a no-op.  This can be\n            used to avoid these calls entirely in the common case.\n  '

    def Modified(self):
        """Called every time the message is modified in such a way that the parent
    message may need to be updated.  This currently means either:
    (a) The message was modified for the first time, so the parent message
        should henceforth mark the message as present.
    (b) The message's cached byte size became dirty -- i.e. the message was
        modified for the first time after a previous call to ByteSize().
        Therefore the parent should also mark its byte size as dirty.
    Note that (a) implies (b), since new objects start out with a client cached
    size (zero).  However, we document (a) explicitly because it is important.

    Modified() will *only* be called in response to one of these two events --
    not every time the sub-message is modified.

    Note that if the listener's |dirty| attribute is true, then calling
    Modified at the moment would be a no-op, so it can be skipped.  Performance-
    sensitive callers should check this attribute directly before calling since
    it will be true most of the time.
    """
        raise NotImplementedError


class NullMessageListener(object):
    __doc__ = 'No-op MessageListener implementation.'

    def Modified(self):
        pass