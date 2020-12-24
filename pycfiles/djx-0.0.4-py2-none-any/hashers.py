# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/auth/hashers.py
# Compiled at: 2019-02-14 00:35:15
from __future__ import unicode_literals
import base64, binascii, hashlib, importlib, warnings
from collections import OrderedDict
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils import lru_cache
from django.utils.crypto import constant_time_compare, get_random_string, pbkdf2
from django.utils.encoding import force_bytes, force_str, force_text
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_noop as _
UNUSABLE_PASSWORD_PREFIX = b'!'
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40

def is_password_usable(encoded):
    if encoded is None or encoded.startswith(UNUSABLE_PASSWORD_PREFIX):
        return False
    try:
        identify_hasher(encoded)
    except ValueError:
        return False

    return True


def check_password(password, encoded, setter=None, preferred=b'default'):
    """
    Returns a boolean of whether the raw password matches the three
    part encoded digest.

    If setter is specified, it'll be called when you need to
    regenerate the password.
    """
    if password is None or not is_password_usable(encoded):
        return False
    preferred = get_hasher(preferred)
    hasher = identify_hasher(encoded)
    hasher_changed = hasher.algorithm != preferred.algorithm
    must_update = hasher_changed or preferred.must_update(encoded)
    is_correct = hasher.verify(password, encoded)
    if not is_correct and not hasher_changed and must_update:
        hasher.harden_runtime(password, encoded)
    if setter and is_correct and must_update:
        setter(password)
    return is_correct


def make_password(password, salt=None, hasher=b'default'):
    """
    Turn a plain-text password into a hash for database storage

    Same as encode() but generates a new random salt.
    If password is None then a concatenation of
    UNUSABLE_PASSWORD_PREFIX and a random string will be returned
    which disallows logins. Additional random string reduces chances
    of gaining access to staff or superuser accounts.
    See ticket #20079 for more info.
    """
    if password is None:
        return UNUSABLE_PASSWORD_PREFIX + get_random_string(UNUSABLE_PASSWORD_SUFFIX_LENGTH)
    else:
        hasher = get_hasher(hasher)
        if not salt:
            salt = hasher.salt()
        return hasher.encode(password, salt)


@lru_cache.lru_cache()
def get_hashers():
    hashers = []
    for hasher_path in settings.PASSWORD_HASHERS:
        hasher_cls = import_string(hasher_path)
        hasher = hasher_cls()
        if not getattr(hasher, b'algorithm'):
            raise ImproperlyConfigured(b"hasher doesn't specify an algorithm name: %s" % hasher_path)
        hashers.append(hasher)

    return hashers


@lru_cache.lru_cache()
def get_hashers_by_algorithm():
    return {hasher.algorithm:hasher for hasher in get_hashers()}


@receiver(setting_changed)
def reset_hashers(**kwargs):
    if kwargs[b'setting'] == b'PASSWORD_HASHERS':
        get_hashers.cache_clear()
        get_hashers_by_algorithm.cache_clear()


def get_hasher(algorithm=b'default'):
    """
    Returns an instance of a loaded password hasher.

    If algorithm is 'default', the default hasher will be returned.
    This function will also lazy import hashers specified in your
    settings file if needed.
    """
    if hasattr(algorithm, b'algorithm'):
        return algorithm
    if algorithm == b'default':
        return get_hashers()[0]
    hashers = get_hashers_by_algorithm()
    try:
        return hashers[algorithm]
    except KeyError:
        raise ValueError(b"Unknown password hashing algorithm '%s'. Did you specify it in the PASSWORD_HASHERS setting?" % algorithm)


def identify_hasher(encoded):
    """
    Returns an instance of a loaded password hasher.

    Identifies hasher algorithm by examining encoded hash, and calls
    get_hasher() to return hasher. Raises ValueError if
    algorithm cannot be identified, or if hasher is not loaded.
    """
    if len(encoded) == 32 and b'$' not in encoded or len(encoded) == 37 and encoded.startswith(b'md5$$'):
        algorithm = b'unsalted_md5'
    elif len(encoded) == 46 and encoded.startswith(b'sha1$$'):
        algorithm = b'unsalted_sha1'
    else:
        algorithm = encoded.split(b'$', 1)[0]
    return get_hasher(algorithm)


def mask_hash(hash, show=6, char=b'*'):
    """
    Returns the given hash, with only the first ``show`` number shown. The
    rest are masked with ``char`` for security reasons.
    """
    masked = hash[:show]
    masked += char * len(hash[show:])
    return masked


class BasePasswordHasher(object):
    """
    Abstract base class for password hashers

    When creating your own hasher, you need to override algorithm,
    verify(), encode() and safe_summary().

    PasswordHasher objects are immutable.
    """
    algorithm = None
    library = None

    def _load_library(self):
        if self.library is not None:
            if isinstance(self.library, (tuple, list)):
                name, mod_path = self.library
            else:
                mod_path = self.library
            try:
                module = importlib.import_module(mod_path)
            except ImportError as e:
                raise ValueError(b"Couldn't load %r algorithm library: %s" % (
                 self.__class__.__name__, e))

            return module
        raise ValueError(b"Hasher %r doesn't specify a library attribute" % self.__class__.__name__)
        return

    def salt(self):
        """
        Generates a cryptographically secure nonce salt in ASCII
        """
        return get_random_string()

    def verify(self, password, encoded):
        """
        Checks if the given password is correct
        """
        raise NotImplementedError(b'subclasses of BasePasswordHasher must provide a verify() method')

    def encode(self, password, salt):
        """
        Creates an encoded database value

        The result is normally formatted as "algorithm$salt$hash" and
        must be fewer than 128 characters.
        """
        raise NotImplementedError(b'subclasses of BasePasswordHasher must provide an encode() method')

    def safe_summary(self, encoded):
        """
        Returns a summary of safe values

        The result is a dictionary and will be used where the password field
        must be displayed to construct a safe representation of the password.
        """
        raise NotImplementedError(b'subclasses of BasePasswordHasher must provide a safe_summary() method')

    def must_update(self, encoded):
        return False

    def harden_runtime(self, password, encoded):
        """
        Bridge the runtime gap between the work factor supplied in `encoded`
        and the work factor suggested by this hasher.

        Taking PBKDF2 as an example, if `encoded` contains 20000 iterations and
        `self.iterations` is 30000, this method should run password through
        another 10000 iterations of PBKDF2. Similar approaches should exist
        for any hasher that has a work factor. If not, this method should be
        defined as a no-op to silence the warning.
        """
        warnings.warn(b'subclasses of BasePasswordHasher should provide a harden_runtime() method')


class PBKDF2PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the PBKDF2 algorithm (recommended)

    Configured to use PBKDF2 + HMAC + SHA256.
    The result is a 64 byte binary string.  Iterations may be changed
    safely but you must rename the algorithm if you change SHA256.
    """
    algorithm = b'pbkdf2_sha256'
    iterations = 36000
    digest = hashlib.sha256

    def encode(self, password, salt, iterations=None):
        if not password is not None:
            raise AssertionError
            assert salt and b'$' not in salt
            iterations = iterations or self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode(b'ascii').strip()
        return b'%s$%d$%s$%s' % (self.algorithm, iterations, salt, hash)

    def verify(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split(b'$', 3)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt, int(iterations))
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, iterations, salt, hash = encoded.split(b'$', 3)
        assert algorithm == self.algorithm
        return OrderedDict([
         (
          _(b'algorithm'), algorithm),
         (
          _(b'iterations'), iterations),
         (
          _(b'salt'), mask_hash(salt)),
         (
          _(b'hash'), mask_hash(hash))])

    def must_update(self, encoded):
        algorithm, iterations, salt, hash = encoded.split(b'$', 3)
        return int(iterations) != self.iterations

    def harden_runtime(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split(b'$', 3)
        extra_iterations = self.iterations - int(iterations)
        if extra_iterations > 0:
            self.encode(password, salt, extra_iterations)


class PBKDF2SHA1PasswordHasher(PBKDF2PasswordHasher):
    """
    Alternate PBKDF2 hasher which uses SHA1, the default PRF
    recommended by PKCS #5. This is compatible with other
    implementations of PBKDF2, such as openssl's
    PKCS5_PBKDF2_HMAC_SHA1().
    """
    algorithm = b'pbkdf2_sha1'
    digest = hashlib.sha1


class Argon2PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the argon2 algorithm.

    This is the winner of the Password Hashing Competition 2013-2015
    (https://password-hashing.net). It requires the argon2-cffi library which
    depends on native C code and might cause portability issues.
    """
    algorithm = b'argon2'
    library = b'argon2'
    time_cost = 2
    memory_cost = 512
    parallelism = 2

    def encode(self, password, salt):
        argon2 = self._load_library()
        data = argon2.low_level.hash_secret(force_bytes(password), force_bytes(salt), time_cost=self.time_cost, memory_cost=self.memory_cost, parallelism=self.parallelism, hash_len=argon2.DEFAULT_HASH_LENGTH, type=argon2.low_level.Type.I)
        return self.algorithm + data.decode(b'ascii')

    def verify(self, password, encoded):
        argon2 = self._load_library()
        algorithm, rest = encoded.split(b'$', 1)
        assert algorithm == self.algorithm
        try:
            return argon2.low_level.verify_secret(force_bytes(b'$' + rest), force_bytes(password), type=argon2.low_level.Type.I)
        except argon2.exceptions.VerificationError:
            return False

    def safe_summary(self, encoded):
        algorithm, variety, version, time_cost, memory_cost, parallelism, salt, data = self._decode(encoded)
        assert algorithm == self.algorithm
        return OrderedDict([
         (
          _(b'algorithm'), algorithm),
         (
          _(b'variety'), variety),
         (
          _(b'version'), version),
         (
          _(b'memory cost'), memory_cost),
         (
          _(b'time cost'), time_cost),
         (
          _(b'parallelism'), parallelism),
         (
          _(b'salt'), mask_hash(salt)),
         (
          _(b'hash'), mask_hash(data))])

    def must_update(self, encoded):
        algorithm, variety, version, time_cost, memory_cost, parallelism, salt, data = self._decode(encoded)
        assert algorithm == self.algorithm
        argon2 = self._load_library()
        return argon2.low_level.ARGON2_VERSION != version or self.time_cost != time_cost or self.memory_cost != memory_cost or self.parallelism != parallelism

    def harden_runtime(self, password, encoded):
        pass

    def _decode(self, encoded):
        """
        Split an encoded hash and return: (
            algorithm, variety, version, time_cost, memory_cost,
            parallelism, salt, data,
        ).
        """
        bits = encoded.split(b'$')
        if len(bits) == 5:
            algorithm, variety, raw_params, salt, data = bits
            version = 16
        else:
            assert len(bits) == 6
            algorithm, variety, raw_version, raw_params, salt, data = bits
            assert raw_version.startswith(b'v=')
            version = int(raw_version[len(b'v='):])
        params = dict(bit.split(b'=', 1) for bit in raw_params.split(b','))
        assert len(params) == 3 and all(x in params for x in ('t', 'm', 'p'))
        time_cost = int(params[b't'])
        memory_cost = int(params[b'm'])
        parallelism = int(params[b'p'])
        return (
         algorithm, variety, version, time_cost, memory_cost, parallelism,
         salt, data)


class BCryptSHA256PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the bcrypt algorithm (recommended)

    This is considered by many to be the most secure algorithm but you
    must first install the bcrypt library.  Please be warned that
    this library depends on native C code and might cause portability
    issues.
    """
    algorithm = b'bcrypt_sha256'
    digest = hashlib.sha256
    library = ('bcrypt', 'bcrypt')
    rounds = 12

    def salt(self):
        bcrypt = self._load_library()
        return bcrypt.gensalt(self.rounds)

    def encode(self, password, salt):
        bcrypt = self._load_library()
        if self.digest is not None:
            password = binascii.hexlify(self.digest(force_bytes(password)).digest())
        else:
            password = force_bytes(password)
        data = bcrypt.hashpw(password, salt)
        return b'%s$%s' % (self.algorithm, force_text(data))

    def verify(self, password, encoded):
        algorithm, data = encoded.split(b'$', 1)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, force_bytes(data))
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, empty, algostr, work_factor, data = encoded.split(b'$', 4)
        assert algorithm == self.algorithm
        salt, checksum = data[:22], data[22:]
        return OrderedDict([
         (
          _(b'algorithm'), algorithm),
         (
          _(b'work factor'), work_factor),
         (
          _(b'salt'), mask_hash(salt)),
         (
          _(b'checksum'), mask_hash(checksum))])

    def must_update(self, encoded):
        algorithm, empty, algostr, rounds, data = encoded.split(b'$', 4)
        return int(rounds) != self.rounds

    def harden_runtime(self, password, encoded):
        _, data = encoded.split(b'$', 1)
        salt = data[:29]
        rounds = data.split(b'$')[2]
        diff = 2 ** (self.rounds - int(rounds)) - 1
        while diff > 0:
            self.encode(password, force_bytes(salt))
            diff -= 1


class BCryptPasswordHasher(BCryptSHA256PasswordHasher):
    """
    Secure password hashing using the bcrypt algorithm

    This is considered by many to be the most secure algorithm but you
    must first install the bcrypt library.  Please be warned that
    this library depends on native C code and might cause portability
    issues.

    This hasher does not first hash the password which means it is subject to
    the 72 character bcrypt password truncation, most use cases should prefer
    the BCryptSHA256PasswordHasher.

    See: https://code.djangoproject.com/ticket/20138
    """
    algorithm = b'bcrypt'
    digest = None


class SHA1PasswordHasher(BasePasswordHasher):
    """
    The SHA1 password hashing algorithm (not recommended)
    """
    algorithm = b'sha1'

    def encode(self, password, salt):
        assert password is not None
        assert salt and b'$' not in salt
        hash = hashlib.sha1(force_bytes(salt + password)).hexdigest()
        return b'%s$%s$%s' % (self.algorithm, salt, hash)

    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split(b'$', 2)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt)
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, salt, hash = encoded.split(b'$', 2)
        assert algorithm == self.algorithm
        return OrderedDict([
         (
          _(b'algorithm'), algorithm),
         (
          _(b'salt'), mask_hash(salt, show=2)),
         (
          _(b'hash'), mask_hash(hash))])

    def harden_runtime(self, password, encoded):
        pass


class MD5PasswordHasher(BasePasswordHasher):
    """
    The Salted MD5 password hashing algorithm (not recommended)
    """
    algorithm = b'md5'

    def encode(self, password, salt):
        assert password is not None
        assert salt and b'$' not in salt
        hash = hashlib.md5(force_bytes(salt + password)).hexdigest()
        return b'%s$%s$%s' % (self.algorithm, salt, hash)

    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split(b'$', 2)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt)
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, salt, hash = encoded.split(b'$', 2)
        assert algorithm == self.algorithm
        return OrderedDict([
         (
          _(b'algorithm'), algorithm),
         (
          _(b'salt'), mask_hash(salt, show=2)),
         (
          _(b'hash'), mask_hash(hash))])

    def harden_runtime(self, password, encoded):
        pass


class UnsaltedSHA1PasswordHasher(BasePasswordHasher):
    """
    Very insecure algorithm that you should *never* use; stores SHA1 hashes
    with an empty salt.

    This class is implemented because Django used to accept such password
    hashes. Some older Django installs still have these values lingering
    around so we need to handle and upgrade them properly.
    """
    algorithm = b'unsalted_sha1'

    def salt(self):
        return b''

    def encode(self, password, salt):
        assert salt == b''
        hash = hashlib.sha1(force_bytes(password)).hexdigest()
        return b'sha1$$%s' % hash

    def verify(self, password, encoded):
        encoded_2 = self.encode(password, b'')
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        assert encoded.startswith(b'sha1$$')
        hash = encoded[6:]
        return OrderedDict([
         (
          _(b'algorithm'), self.algorithm),
         (
          _(b'hash'), mask_hash(hash))])

    def harden_runtime(self, password, encoded):
        pass


class UnsaltedMD5PasswordHasher(BasePasswordHasher):
    """
    Incredibly insecure algorithm that you should *never* use; stores unsalted
    MD5 hashes without the algorithm prefix, also accepts MD5 hashes with an
    empty salt.

    This class is implemented because Django used to store passwords this way
    and to accept such password hashes. Some older Django installs still have
    these values lingering around so we need to handle and upgrade them
    properly.
    """
    algorithm = b'unsalted_md5'

    def salt(self):
        return b''

    def encode(self, password, salt):
        assert salt == b''
        return hashlib.md5(force_bytes(password)).hexdigest()

    def verify(self, password, encoded):
        if len(encoded) == 37 and encoded.startswith(b'md5$$'):
            encoded = encoded[5:]
        encoded_2 = self.encode(password, b'')
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        return OrderedDict([
         (
          _(b'algorithm'), self.algorithm),
         (
          _(b'hash'), mask_hash(encoded, show=3))])

    def harden_runtime(self, password, encoded):
        pass


class CryptPasswordHasher(BasePasswordHasher):
    """
    Password hashing using UNIX crypt (not recommended)

    The crypt module is not supported on all platforms.
    """
    algorithm = b'crypt'
    library = b'crypt'

    def salt(self):
        return get_random_string(2)

    def encode(self, password, salt):
        crypt = self._load_library()
        assert len(salt) == 2
        data = crypt.crypt(force_str(password), salt)
        assert data is not None
        return b'%s$%s$%s' % (self.algorithm, b'', data)

    def verify(self, password, encoded):
        crypt = self._load_library()
        algorithm, salt, data = encoded.split(b'$', 2)
        assert algorithm == self.algorithm
        return constant_time_compare(data, crypt.crypt(force_str(password), data))

    def safe_summary(self, encoded):
        algorithm, salt, data = encoded.split(b'$', 2)
        assert algorithm == self.algorithm
        return OrderedDict([
         (
          _(b'algorithm'), algorithm),
         (
          _(b'salt'), salt),
         (
          _(b'hash'), mask_hash(data, show=3))])

    def harden_runtime(self, password, encoded):
        pass