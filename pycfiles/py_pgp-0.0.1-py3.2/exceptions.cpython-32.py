# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/exceptions.py
# Compiled at: 2015-08-31 08:17:33


class CannotParseCritical(RuntimeError):
    """This signature subpacket cannot be parsed by this implementation
    and is marked as critical. It must be discarded.
    """
    pass


class CannotParseCriticalNotation(CannotParseCritical):
    """This notation subpacket cannot be parsed by this implementation
    and is marked as critical. It must be discarded.
    """
    pass


class SensitiveSignature(ValueError):
    """This signature is marked as being a senstive revocation key. We
    should not have received it.
    """
    pass


class InvalidKey(ValueError):
    """This public key contains some invalid data."""
    pass


class InvalidKeyPacketOrder(InvalidKey):
    """The packets that make up this public key are ordered in an
    invalid way.
    """
    pass


class InvalidKeyPacketType(InvalidKey):
    """This packet is not valid for a transferable public key."""
    pass


class InvalidUserAttribute(InvalidKey):
    """This user attribute contains some invalid data."""
    pass


class InvalidUserAttributeImageFormat(InvalidUserAttribute):
    """The image format provided by this user attribute is not valid."""
    pass


class InvalidUserAttributeImage(InvalidUserAttribute):
    """The image data provided by this user attribute is not valid for
    the image format specified.
    """
    pass


class UnsupportedPacketType(InvalidKey):
    """This packet type is unsupported in public key data."""
    pass


class UnsupportedPacketVersion(UnsupportedPacketType):
    """The version of this packet is not supported by this
    implementation.
    """
    pass


class UnsupportedSignatureVersion(UnsupportedPacketVersion):
    """The version of this signature is not supported by this
    implementation.
    """
    pass


class ReservedSignatureSubpacket(InvalidKey):
    """This signature contains a subpacket type which is reserved."""
    pass


class InvalidSignatureSubpacket(InvalidKey):
    """This signature contains a subpacket type which is invalid."""
    pass


class LocalCertificationSignature(InvalidKey):
    """This signature is a local certification. We should not have
    received it and should discard it."""
    pass


class RegexValueError(InvalidSignatureSubpacket):
    """This regular expression signature subpacket contains an invalid
    expression.
    """

    def __init__(self, position, string, unterminated=False):
        if unterminated:
            position -= 1
        self.position = position
        self.string = string

    def __str__(self):
        return 'Invalid character at position {0}\n{1}\n{2}^'.format(self.position, self.string, ' ' * self.position)


class CannotValidateSignature(TypeError):
    """The implementation cannot validate this signature. It may or may
    not be valid.
    """
    pass


class UnexpectedSignatureType(CannotValidateSignature):
    """The implementation cannot validate this type of signature of
    this data.
    """
    pass


class UnsupportedPublicKeyAlgorithm(CannotValidateSignature):
    """The public key algorithm used by this signature is not supported
    by this implementation.
    """
    pass


class PublicKeyAlgorithmCannotSign(CannotValidateSignature):
    """The public key algorithm used by this signature cannot be used
    to sign data.
    """
    pass


class UnsupportedDigestAlgorithm(CannotValidateSignature):
    """The digest algorithm used by this signature is not supported by
    this implementation.
    """
    pass


class InvalidSignature(ValueError):
    """This signature is invalid."""
    pass


class SignatureDigestMismatch(InvalidSignature):
    """The signature check-bytes do not match the digest of the data it
    claims to sign.
    """
    pass


class SignatureVerificationFailed(InvalidSignature):
    """The signature does not match the data which it claims to sign.
    """
    pass


class InvalidSubkeyBindingSignature(InvalidSignature):
    """The signature binding this subkey to the primary key was not
    created by the primary key it claims to be bound to.
    """
    pass


class MissingBackSignature(InvalidSubkeyBindingSignature):
    """The subkey binding signature indicates that this subkey may be
    used to sign data. A backsignature is required for signing subkeys
    and one was not embedded in this binding signature.
    """
    pass


class InvalidBackSignature(InvalidSubkeyBindingSignature):
    """This subkey binding signature provided a backsignature, but did
    the backsignature is invalid.
    """
    pass


class SignatureTimeConflict(InvalidSignature):
    """Some kind of time conflict exists between the signature and the
    key that made it.
    """
    pass


class SigningKeyCreatedInTheFuture(SignatureTimeConflict):
    """The key used to create this signature claims to have been
    created in the future.
    """
    pass


class SignatureCreatedInTheFuture(SignatureTimeConflict):
    """This signature claims to have been created in the future."""
    pass


class SignatureCreatedBeforeContent(SignatureTimeConflict):
    """This signature was created before the content it signs purports
    to have been.
    """
    pass


class SignatureWarning(UserWarning):
    """Something is amiss with this signature, but it is not
    necessarily invalid.
    """
    pass


class SignatureHasExpired(SignatureWarning):
    """The signature has expired."""
    pass


class SigningKeyHasExpired(SignatureWarning):
    """The key used to make this signature has expired since the
    signature was created.
    """
    pass


class SignedByRevokedKey(SignatureWarning):
    """The key used to make this signature had already been revoked
    when the signature was created.
    """
    pass


class SigningKeyHasBeenRevoked(SignatureWarning):
    """The key used to make this signature has been revoked since the
    signature was created.
    """
    pass