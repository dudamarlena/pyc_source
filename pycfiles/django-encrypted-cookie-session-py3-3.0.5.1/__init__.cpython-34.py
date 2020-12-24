# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\GitHub\django-encrypted-cookie-session-py3\encrypted_cookies\__init__.py
# Compiled at: 2015-10-17 16:29:21
# Size of source mod 2**32: 3805 bytes
import logging, zlib, django.contrib.sessions.backends.signed_cookies
from django.conf import settings
try:
    from django.contrib.sessions.serializers import PickleSerializer
except ImportError:
    from django.contrib.sessions.backends.signed_cookies import PickleSerializer

from django.core import signing
try:
    from django.utils.six.moves import cPickle as pickle
except ImportError:
    import pickle

from cryptography.fernet import InvalidToken
from encrypted_cookies import crypto
__version__ = '3.0.4'
log = logging.getLogger(__name__)

class EncryptingPickleSerializer(PickleSerializer):
    __doc__ = '\n    Serialize/unserialize data with AES encryption using a secret key.\n    '

    def dumps(self, obj):
        raw_data = super(EncryptingPickleSerializer, self).dumps(obj)
        if getattr(settings, 'COMPRESS_ENCRYPTED_COOKIE', False):
            level = getattr(settings, 'ENCRYPTED_COOKIE_COMPRESSION_LEVEL', 6)
            raw_data = zlib.compress(raw_data, level)
        return bytes(crypto.encrypt(raw_data))

    def loads(self, data):
        decrypted_data = crypto.decrypt(data)
        if getattr(settings, 'COMPRESS_ENCRYPTED_COOKIE', False):
            try:
                decrypted_data = zlib.decompress(decrypted_data)
            except zlib.error as exc:
                log.warning('Could not decompress cookie value: %s: %s' % (
                 exc.__class__.__name__, exc))

        return super(EncryptingPickleSerializer, self).loads(decrypted_data)


class SessionStore(django.contrib.sessions.backends.signed_cookies.SessionStore):

    def load(self):
        """
        We load the data from the key itself instead of fetching from
        some external data store. Opposite of _get_session_key(),
        raises BadSignature if signature fails.
        """
        try:
            return signing.loads(self.session_key, serializer=EncryptingPickleSerializer, max_age=settings.SESSION_COOKIE_AGE, salt='encrypted_cookies')
        except (signing.BadSignature, pickle.UnpicklingError, InvalidToken, ValueError) as exc:
            log.debug('recreating session because of exception: %s: %s' % (
             exc.__class__.__name__, exc))
            self.create()

        return {}

    def _get_session_key(self):
        """
        Most session backends don't need to override this method, but we do,
        because instead of generating a random string, we want to actually
        generate a secure url-safe Base64-encoded string of data as our
        session key.
        """
        session_cache = getattr(self, '_session_cache', {})
        data = signing.dumps(session_cache, compress=True, salt='encrypted_cookies', serializer=EncryptingPickleSerializer)
        cookie_size = len(data)
        log.debug('encrypted session cookie is %s bytes' % cookie_size)
        if cookie_size > 4093:
            log.error('encrypted session cookie is too large for most browsers; size: %s' % cookie_size)
        return data.encode('utf-8')