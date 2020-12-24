# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/messages/storage/session.py
# Compiled at: 2019-02-14 00:35:16
import json
from django.conf import settings
from django.contrib.messages.storage.base import BaseStorage
from django.contrib.messages.storage.cookie import MessageDecoder, MessageEncoder
from django.utils import six

class SessionStorage(BaseStorage):
    """
    Stores messages in the session (that is, django.contrib.sessions).
    """
    session_key = '_messages'

    def __init__(self, request, *args, **kwargs):
        assert hasattr(request, 'session'), 'The session-based temporary message storage requires session middleware to be installed, and come before the message middleware in the MIDDLEWARE%s list.' % ('_CLASSES' if settings.MIDDLEWARE is None else '')
        super(SessionStorage, self).__init__(request, *args, **kwargs)
        return

    def _get(self, *args, **kwargs):
        """
        Retrieves a list of messages from the request's session.  This storage
        always stores everything it is given, so return True for the
        all_retrieved flag.
        """
        return (
         self.deserialize_messages(self.request.session.get(self.session_key)), True)

    def _store(self, messages, response, *args, **kwargs):
        """
        Stores a list of messages to the request's session.
        """
        if messages:
            self.request.session[self.session_key] = self.serialize_messages(messages)
        else:
            self.request.session.pop(self.session_key, None)
        return []

    def serialize_messages(self, messages):
        encoder = MessageEncoder(separators=(',', ':'))
        return encoder.encode(messages)

    def deserialize_messages(self, data):
        if data and isinstance(data, six.string_types):
            return json.loads(data, cls=MessageDecoder)
        return data