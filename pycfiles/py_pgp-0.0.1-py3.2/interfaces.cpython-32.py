# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/interfaces.py
# Compiled at: 2015-08-31 08:17:33
from zope.interface import Attribute
from zope.interface import Interface

class IRevocationKeyInfo(Interface):
    public_key_algorithm = Attribute('')
    fingerprint = Attribute('')
    sensitive = Attribute('')


class INotation(Interface):
    namespace = Attribute('')
    name = Attribute('')
    value = Attribute('')

    def is_human_readable(self):
        pass


class ISignature(Interface):
    target = Attribute('ISignable')
    version = Attribute('int')
    signature_type = Attribute('int')
    public_key_algorithm = Attribute('int')
    hash_algorithm = Attribute('int')
    hash2 = Attribute('bytes')
    signature_values = Attribute('tuple of ints')

    def is_self_signature(self):
        pass

    def is_expired(self):
        pass

    def is_revoked(self):
        pass

    def issuer_key_is_expired(self):
        pass

    def issuer_key_is_revoked(self):
        pass

    def signature_target(self):
        pass

    creation_time = Attribute('datetime')
    issuer_key_ids = Attribute('List of hex strings')
    expiration_time = Attribute('A datetime or None')
    exportable = Attribute('bool')
    trust_depth = Attribute('int (0 <= i < 256) or None')
    trust_amount = Attribute('int (0 <= i < 256) or None')
    regular_expressions = Attribute('List of re.RegexObject')
    revocable = Attribute('bool')
    notations = Attribute('List of INotation')
    issuer_user_id = Attribute('RFC 2822 address unicode string or None')
    issuer_user_name = Attribute('Unicode string or None')
    issuer_user_email = Attribute('Unicode string or None')
    issuer_user_comment = Attribute('Unicode string or None')
    revocation_reason = Attribute('Unicode string or None')
    revocation_code = Attribute('int or None')
    embedded_signatures = Attribute('List of ISignature')
    key_expiration_time = Attribute('datetime or None')
    preferred_compression_algorithms = Attribute('List of int')
    preferred_hash_algorithms = Attribute('List of int')
    preferred_symmetric_algorithms = Attribute('List of int')
    revocation_keys = Attribute('List of IRevocationKeyInfo')
    key_server_should_not_modify = Attribute('bool')
    preferred_key_server = Attribute('Unicode URI or None')
    primary_user_id = Attribute('bool')
    policy_uri = Attribute('Unicode URI or None')
    may_certify_others = Attribute('bool')
    may_sign_data = Attribute('bool')
    may_encrypt_comms = Attribute('bool')
    may_encrypt_storage = Attribute('bool')
    may_be_used_for_auth = Attribute('bool')
    may_have_been_split = Attribute('bool')
    may_have_multiple_owners = Attribute('bool')
    supports_modification_detection = Attribute('bool')


class IUnlockable(Interface):

    def unlock(self, passphrase):
        pass

    def lock(self, passphrase):
        pass

    def is_locked(self):
        pass


class ISignable(Interface):
    signatures = Attribute('List of ISignature')


class IPublicKey(ISignable):

    def verify(self, signature):
        pass

    def encrypt(self, data):
        pass

    def is_expired(self):
        pass

    def is_revoked(self):
        pass

    version = Attribute('')
    public_key_algorithm = Attribute('')
    bit_length = Attribute('')
    key_id = Attribute('')
    fingerprint = Attribute('')
    modulus_n = Attribute('')
    exponent_e = Attribute('')
    prime_p = Attribute('')
    group_generator_g = Attribute('')
    group_order_q = Attribute('')
    key_value_y = Attribute('')
    creation_time = Attribute('A datetime of when the key was created')
    expiration_time = Attribute('A datetime of when the key will expire, or None')
    preferred_compression_algorithms = Attribute('List of int')
    preferred_hash_algorithms = Attribute('List of int')
    preferred_symmetric_algorithms = Attribute('List of int')
    revocation_keys = Attribute('List of IRevocationKeyInfo')
    key_server_should_not_modify = Attribute('bool')
    preferred_key_server = Attribute('Unicode URI or None')
    primary_user_id = Attribute('bool')
    policy_uri = Attribute('Unicode URI or None')
    may_certify_others = Attribute('bool')
    may_sign_data = Attribute('bool')
    may_encrypt_comms = Attribute('bool')
    may_encrypt_storage = Attribute('bool')
    may_be_used_for_auth = Attribute('bool')
    may_have_been_split = Attribute('bool')
    may_have_multiple_owners = Attribute('bool')
    supports_modification_detection = Attribute('bool')
    keygrip = Attribute('The SHA1 hash of the S-expression representing the public key. Used by agents.')


class ISecretKey(IPublicKey, IUnlockable):
    s2k_specification = Attribute('IS2KSpecification')
    symmetric_algorithm = Attribute('int')
    iv = Attribute('bytes')
    encrypted_portion = Attribute('bytes')
    checksum = Attribute('int')
    hash = Attribute('bytes')
    exponent_d = Attribute('int')
    prime_p = Attribute('int')
    prime_q = Attribute('int')
    multiplicative_inverse_u = Attribute('int')
    exponent_x = Attribute('int')


class IUserID(ISignable):
    primary_public_key = Attribute('')
    user_id = Attribute('')
    user_name = Attribute('')
    user_email = Attribute('')
    user_comment = Attribute('')


class IUserAttributeContentItem(Interface):
    data = Attribute('')
    mime_type = Attribute('')


class IUserAttribute(ISignable):
    primary_public_key = Attribute('')
    content_items = Attribute('A list of IUserAttributeContentItem')


class ITransferablePublicKeyFactory(Interface):

    def from_packets(self, packets):
        """"""
        pass


class ITransferableSecretKeyFactory(ITransferablePublicKeyFactory):
    pass


class ITransferablePublicKey(IPublicKey):

    def to_packets(self):
        """"""
        pass

    primary_user_id = Attribute('')
    user_ids = Attribute('')
    primary_user_attribute = Attribute('')
    user_attributes = Attribute('')
    subkeys = Attribute('')


class ITransferableSecretKey(ITransferablePublicKey, ISecretKey):
    pass


class ISubkey(Interface):
    primary_public_key = Attribute('')


class IPublicSubkey(IPublicKey, ISubkey):
    pass


class ISecretSubkey(ISecretKey, ISubkey):
    pass