# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/djangoflash/storage/session.py
# Compiled at: 2011-01-28 16:01:34
"""This module provides a session-based flash storage backend.

Since this backend relies on the user's session, you need to include the
:class:`SessionMiddleware` class to the ``MIDDLEWARE_CLASSES`` section of your
project's ``settings.py`` file::

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'djangoflash.middleware.FlashMiddleware',
    )

.. seealso::
  :ref:`configuration`
"""

class FlashStorageClass(object):
    """Session-based flash storage backend.
    """

    def __init__(self):
        """Returns a new session-based flash storage backend.
        """
        self._key = '_djflash_session'

    def set(self, flash, request, response):
        """Stores the given :class:`FlashScope` object in the session.
        """
        if hasattr(request, 'session'):
            if flash:
                request.session[self._key] = flash
            elif self._key in request.session:
                del request.session[self._key]

    def get(self, request):
        """Returns :class:`FlashScope` object stored in the session.
        """
        if hasattr(request, 'session') and self._key in request.session:
            return request.session[self._key]