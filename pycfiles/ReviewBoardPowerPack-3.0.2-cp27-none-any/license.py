# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/license.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import ConfigParser, binascii, io
from datetime import datetime, timedelta
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from django.utils import six
from django.utils.encoding import force_bytes
from django.utils.six.moves import cPickle as pickle, cStringIO as StringIO
from beanbag_licensing.errors import IncorrectSignatureError
from beanbag_licensing.immutable import immutable
from beanbag_licensing.keys import BEANBAG_PUBLIC_KEY, TEST_PUBLIC_KEY

@immutable
class License(object):
    """Represents a new or existing license for a product.

    This stores state on a license, allowing expiration and validity checks
    to be performed against it. It also has mechanisms for reading in
    encoded license data and writing it out.

    A License must be activated using activate() before any validity checks
    can be performed.
    """
    immutable_attrs = ('_verified', 'company', 'expiration', 'extra_data', 'grace_period',
                       'install_keys', 'num_perpetual_users', 'num_users', 'product',
                       'trial', 'unlicensed', 'version')
    mutable_attrs = ('_verify_grace_start_time', 'active_install_key')
    LATEST_LICENSE_VERSION = 2

    @classmethod
    def read(cls, license_data, public_key=BEANBAG_PUBLIC_KEY):
        """Constructs a License instance from license file data.

        This will parse the encoded license information and signature from
        a license file's contents and construct a License instance.

        Args:
            license_data (bytes):
                The contents of the license file.

            public_key (bytes, optional):
                The public key that the license data must be signed by.

        Returns:
            License:
            The resulting license.

        Raises:
            beanbag_licensing.errors.IncorrectSignatureError:
                The license data could not be verified against the license
                signature or public key, or the license file coudl not be
                parsed.
        """
        config = ConfigParser.SafeConfigParser()
        try:
            config.readfp(io.StringIO(unicode(license_data)))
        except Exception:
            raise IncorrectSignatureError

        encoded_license = force_bytes(config.get(b'License', b'license'))
        signature = force_bytes(config.get(b'License', b'signature'))
        return cls.decode(encoded_license, signature, public_key)

    @classmethod
    def decode(cls, encoded_license, signature, public_key=BEANBAG_PUBLIC_KEY):
        """Construct a License instance from encoded license data.

        This takes encoded license data and a matching signature, validates
        it, and constructs a License instance.

        This is meant to be used by :py:meth:`read`.

        Args:
            encoded_license (bytes):
                The Base64-encoded license data.

            signature (bytes):
                The signature for the license to verify the data against.

            public_key (bytes, optional):
                The public key that the license data must be signed by.

        Returns:
            License:
            The resulting license.

        Raises:
            beanbag_licensing.errors.IncorrectSignatureError:
                The license data could not be verified against the license
                signature or public key.
        """
        return cls(public_key=public_key, encoded_license=encoded_license, license_signature=signature, **pickle.loads(binascii.a2b_base64(encoded_license)))

    @classmethod
    def make_unlicensed(cls, product, perpetual_users=2):
        """Return an unlicensed License.

        This represents an unlicensed product, which has a pre-set user cap,
        and may have restricted features.

        This will behave like a typical license, but will have the
        :py:attr:`unlicensed` attribute set to ``True``, and will have
        certain limitations. In many ways, it behaves like an expired license.

        Args:
            product (unicode):
                The product name for the license.

            perpetual_users (int):
                The number of perpetual users who can use the product.

        Returns:
            License: The resulting license.
        """
        return cls(version=cls.LATEST_LICENSE_VERSION, product=product, perpetual_users=perpetual_users, trial=False, unlicensed=True)

    def __init__(self, license_version=None, product=None, company=None, users=None, perpetual_users=0, expiration=None, grace_period=0, trial=True, install_keys=None, unlicensed=False, encoded_license=None, license_signature=None, public_key=None, **kwargs):
        """Initialize the license.

        Once initialized, the license data cannot be changed.

        The license does need to be activated with an install key through
        :py:meth:`activate`, which can only be done once.

        In order for a license to be considered verified, the
        ``encoded_license``, ``license_signature``, and ``public_key``
        arguments are required, and the signature must be verifiable by the
        public key and must pertain to the encoded license data. Only
        verified licenses can be used in production. If these arguments are
        provided, but the signature or key are not correct,
        :py:class:`~beanbag_licensing.errors.IncorrectSignatureError` will be
        raised.

        To be verified, licenses also must be signed by the official private
        key.

        Args:
            license_version (int, optional):
                The version of the license. Certain capabilities may be
                enabled or disabled based on the version.

            product (unicode, optional):
                The product that the license is for.

            company (unicode, optional):
                The company that owns this license.

            users (int, optional):
                The maximum number of user seats permitted by this license. If
                0, the license does not have a user cap.

            perpetual_users (int, optional):
                The number of user seats available once the license has
                expired.

            expiration (datetime.datetime, optional):
                The expiration date/time of the license.

            grace_period (int, optional):
                The number of days the license will still work for after it
                expires.

            trial (bool, optional):
                Whether or not this is a trial license.

            install_keys (list of unicode, optional):
                The list of install keys that the license is valid for.

            unlicensed (bool, optional):
                Whether this actually represents an unlicensed state. This
                is set by :py:meth:`unlicensed`.

            encoded_license (bytes, optional):
                The pickled data for the license. This is required for licenses
                to be considered verified.

            license_signature (
                A valid signature for ``encoded_license``, verifiable by
                ``public_key``. This is required for licenses to be considered
                verified.

            public_key (bytes, optional):
                The public key that can verify the ``license_signature`` for
                ``encoded_license``. This is required for licenses
                to be considered verified.

            **kwargs (dict):
                Additional data from the license file. These will be set in
                :py:attr:`extra_data`.

        Raises:
            beanbag_licensing.errors.IncorrectSignatureError:
                The ``encoded_license``, ``license_signature``, and
                ``public_key`` arguments were not compatible.
        """
        if public_key is not None and license_signature is not None and encoded_license is not None:
            license_hash = SHA.new()
            license_hash.update(encoded_license)
            signer = PKCS1_v1_5.new(RSA.importKey(public_key))
            if not signer.verify(license_hash, binascii.a2b_base64(license_signature)):
                raise IncorrectSignatureError
            self._verified = public_key == BEANBAG_PUBLIC_KEY
        else:
            self._verified = False
        if not self._verified and public_key == TEST_PUBLIC_KEY:
            self._verify_grace_start_time = datetime.utcnow()
        else:
            self._verify_grace_start_time = None
        self.version = license_version
        self.product = product
        self.company = company
        self.num_users = users
        self.num_perpetual_users = perpetual_users or 0
        self.expiration = expiration
        self.grace_period = grace_period
        self.trial = trial
        self.install_keys = install_keys or []
        self.unlicensed = unlicensed
        self.extra_data = kwargs
        self.active_install_key = None
        return

    @property
    def has_user_cap(self):
        """Returns whether the license has a user cap."""
        if self.in_perpetual_user_mode:
            return True
        else:
            return self.num_users > 0

    @property
    def user_cap(self):
        """Return the user cap for the license.

        If the license is in perpetual user mode, the number of perpetual
        users will be returned. Otherwise, the license's standard user
        cap + the number of perpetual users will be returned, or 0 if
        there is no user cap.
        """
        if self.in_perpetual_user_mode:
            return self.num_perpetual_users
        else:
            if self.num_users > 0:
                return self.num_users + self.num_perpetual_users
            return 0

    @property
    def expired(self):
        """Returns whether the license is past the expiration date.

        Note that an expired license is not necessarily unusable if this
        returns True, as there may still be a grace period. To factor that
        in, use hard_expired().
        """
        if self.unlicensed:
            return False
        return datetime.utcnow() > self.expiration

    @property
    def time_left(self):
        """A timedelta of the time left before expiration."""
        if self.unlicensed:
            return None
        else:
            return self.expiration - datetime.utcnow()

    @property
    def hard_expiration_date(self):
        """The hard expiration date of the license.

        This factors in the grace period.
        """
        if self.unlicensed:
            return None
        else:
            return self.expiration + timedelta(days=self.grace_period)

    @property
    def hard_expired(self):
        """Returns whether the license is expired.

        This factors in the expiration date and grace period, determining
        if the license is in fact really expired.
        """
        return not self.unlicensed and datetime.utcnow() > self.hard_expiration_date

    @property
    def in_perpetual_user_mode(self):
        """Return whether the license is now in perpetual user mode.

        A license is in perpetual user mode if there are a number of
        perpetual users set, the license has hard-expired, and the license is
        a trial license.
        """
        return self.unlicensed or self.trial and self.num_perpetual_users > 0 and self.hard_expired

    @property
    def valid_install_key(self):
        """Returns whether the activated install key is valid.

        Note that activate() must be called first.
        """
        if self.unlicensed:
            return True
        assert self.active_install_key
        return not self.install_keys or self.active_install_key in self.install_keys

    @property
    def valid(self):
        """Returns whether the license is valid.

        A license is valid if it has not hard-expired, if the license
        key is valid, and if the license data came from a verified source.

        Note that activate() must be called first.
        """
        return self.unlicensed or self.valid_install_key and (not self.hard_expired or self.in_perpetual_user_mode) and (self._verified or self._verify_grace_start_time is not None and datetime.utcnow() < self._verify_grace_start_time + timedelta(minutes=60))

    def activate(self, install_key):
        """Activates the license for use with the given install key.

        This must be performed before any validation checks can pass.
        """
        self.active_install_key = install_key

    def encode(self, private_key):
        """Encode the license data using a private key.

        This will return encoded license data and a matching signature.

        Args:
            private_key (bytes):
                The private key used to encode the data.

        Returns:
            tuple:
            A tuple of the encoded license and the signature.
        """
        encoded_license = binascii.b2a_base64(pickle.dumps(self)).strip()
        h = SHA.new(encoded_license)
        signer = PKCS1_v1_5.new(RSA.importKey(private_key))
        signature = binascii.b2a_base64(signer.sign(h)).strip()
        return (
         encoded_license, signature)

    def write(self, f, private_key):
        """Write the license to a file pointer.

        This will write a distributable license file to th given file pointer.
        That license file can be directly used in an instance of the extension.

        Args:
            private_key (bytes):
                The private key used to encode the data.
        """
        encoded_license, signature = self.encode(private_key)
        config = ConfigParser.SafeConfigParser()
        config.add_section(b'License')
        config.set(b'License', b'license', encoded_license)
        config.set(b'License', b'signature', signature)
        config.write(f)

    def write_str(self, private_key):
        """Return the license file data as a string.

        Args:
            private_key (bytes):
                The private key used to encode the data.

        Returns:
            bytes:
            The license data.
        """
        s = StringIO()
        self.write(s, private_key)
        license_data = s.getvalue()
        s.close()
        return license_data

    def __setattr__(self, name, value):
        """Set an attribute on the license.

        This enforces what attributes can be set and how.

        ``active_install_key`` can only be set if it doesn't yet have a value.

        ``_verify_grace_start_time`` can only be set to ``None`` after the
        license is initialized.

        Otherwise, only mutable attributes can be modified. No license data
        can be set after initialization.

        Args:
            name (unicode):
                The name of the attribute to set.

            value (object):
                The value to set.
        """
        if name == b'active_install_key' and getattr(self, b'active_install_key', None):
            raise AttributeError(b'The active install key cannot be changed.')
        if name == b'_verify_grace_start_time' and not self._mutable and value is not None:
            raise AttributeError(b'Cannot set private variable "%s".' % name)
        super(License, self).__setattr__(name, value)
        return

    def __reduce__(self):
        """Construct a pickled representation of the license data.

        The will serialize the data as a dictionary with all license fields
        sorted (preventing unit test issues due to arbitrary ordering in
        dictionaries).

        Technically, this data is serialized differently in the Pickle protocol
        than if an actual dictionary is returned (it has to store
        ``__builtin__.dict`` as the type, instead of using an opcode for
        dictionaries), but this doesn't introduce any compatibility problems.

        Returns:
            tuple:
            A Pickle serialization tuple indicating how to serialize the data.
        """
        data = {b'license_version': self.LATEST_LICENSE_VERSION, 
           b'product': self.product, 
           b'company': self.company, 
           b'users': self.num_users, 
           b'perpetual_users': self.num_perpetual_users, 
           b'expiration': self.expiration, 
           b'grace_period': self.grace_period, 
           b'trial': self.trial, 
           b'install_keys': self.install_keys}
        data.update(self.extra_data)
        return (
         dict,
         (),
         None,
         None,
         iter(sorted(six.iteritems(data), key=lambda item: item[0])))

    def __eq__(self, other):
        """Return whether this license is equal to another.

        Args:
            other (License):
                The license to compare to.

        Returns:
            bool:
            ``True`` if the two licenses are equal. ``False`` if they are not.
        """
        return self.product == other.product and self.trial == other.trial and self.install_keys == other.install_keys and self.company == other.company and self.num_users == other.num_users and self.num_perpetual_users == other.num_perpetual_users and self.expiration == other.expiration and self.grace_period == other.grace_period and self.extra_data == other.extra_data