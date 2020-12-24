# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/crypto.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 3933 bytes
import base64, string, errno, itsdangerous, logging, os.path, random, tempfile
from mediagoblin import mg_globals
_log = logging.getLogger(__name__)
ALPHABET = string.ascii_letters + '-_'
try:
    getrandbits = random.SystemRandom().getrandbits
except AttributeError:
    getrandbits = random.getrandbits

__itsda_secret = None

def load_key(filename):
    global __itsda_secret
    key_file = open(filename)
    try:
        __itsda_secret = key_file.read()
    finally:
        key_file.close()


def create_key(key_dir, key_filepath):
    global __itsda_secret
    old_umask = os.umask(63)
    key_file = None
    try:
        if not os.path.isdir(key_dir):
            os.makedirs(key_dir)
            _log.info('Created %s', key_dir)
        key = str(getrandbits(192))
        key_file = tempfile.NamedTemporaryFile(dir=key_dir, suffix='.bin', delete=False)
        key_file.write(key.encode('ascii'))
        key_file.flush()
        os.rename(key_file.name, key_filepath)
        key_file.close()
    finally:
        os.umask(old_umask)
        if key_file is not None:
            if not key_file.closed:
                key_file.close()
                os.unlink(key_file.name)

    __itsda_secret = key
    _log.info("Saved new key for It's Dangerous")


def setup_crypto(app_config):
    key_dir = app_config['crypto_path']
    key_filepath = os.path.join(key_dir, 'itsdangeroussecret.bin')
    try:
        load_key(key_filepath)
    except IOError as error:
        if error.errno != errno.ENOENT:
            raise
        create_key(key_dir, key_filepath)


def get_timed_signer_url(namespace):
    """
    This gives a basic signing/verifying object.

    The namespace makes sure signed tokens can't be used in
    a different area. Like using a forgot-password-token as
    a session cookie.

    Basic usage:

    .. code-block:: python

       _signer = None
       TOKEN_VALID_DAYS = 10
       def setup():
           global _signer
           _signer = get_timed_signer_url("session cookie")
       def create_token(obj):
           return _signer.dumps(obj)
       def parse_token(token):
           # This might raise an exception in case
           # of an invalid token, or an expired token.
           return _signer.loads(token, max_age=TOKEN_VALID_DAYS*24*3600)

    For more details see
    http://pythonhosted.org/itsdangerous/#itsdangerous.URLSafeTimedSerializer
    """
    assert __itsda_secret is not None
    return itsdangerous.URLSafeTimedSerializer(__itsda_secret, salt=namespace)


def random_string(length, alphabet=ALPHABET):
    """ Returns a URL safe base64 encoded crypographically strong string """
    base = len(alphabet)
    rstring = ''
    for i in range(length):
        n = getrandbits(6)
        n = divmod(n, base)[1]
        rstring += alphabet[n]

    return rstring