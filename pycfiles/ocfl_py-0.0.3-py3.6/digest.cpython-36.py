# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ocfl/digest.py
# Compiled at: 2020-03-31 11:51:35
# Size of source mod 2**32: 3427 bytes
"""Digest handling for OCFL."""
import hashlib

def _file_digest(filename, digester):
    """Generate a digest for filename using the supplied digester object.

    Like haslib.sha256 and hashlib.sha512, the digester object must
    support the .update() and .hexdigest() methods.
    """
    BUFSIZE = 65536
    with open(filename, 'rb', buffering=0) as (f):
        for b in iter(lambda : f.read(BUFSIZE), b''):
            digester.update(b)

    return digester.hexdigest()


def file_digest(filename, digest_type='sha512'):
    """Digest of digest_type for file filename.

    Supports digest_type values from OCFL spec:
        'md5', 'sha1', 'sha256', 'sha512', 'blake2b-512'
    and from OCFL extensions
        'blake2b-160', 'blake2b-256', 'blake2b-384'
    and a truncated sha512 and sha256 useful for examples
        'sha512-spec-ex',  'sha256-spec-ex'

    Raises an exception if the digest_type is not supported.
    """
    if digest_type == 'sha512':
        return _file_digest(filename, hashlib.sha512())
    else:
        if digest_type == 'sha256':
            return _file_digest(filename, hashlib.sha256())
        else:
            if digest_type == 'sha1':
                return _file_digest(filename, hashlib.sha1())
            else:
                if digest_type == 'md5':
                    return _file_digest(filename, hashlib.md5())
                else:
                    if digest_type == 'blake2b-512':
                        return _file_digest(filename, hashlib.blake2b())
                    if digest_type == 'blake2b-160':
                        return _file_digest(filename, hashlib.blake2b(digest_size=20))
                    if digest_type == 'blake2b-256':
                        return _file_digest(filename, hashlib.blake2b(digest_size=32))
                if digest_type == 'blake2b-384':
                    return _file_digest(filename, hashlib.blake2b(digest_size=48))
            if digest_type == 'sha512-spec-ex':
                d = _file_digest(filename, hashlib.sha512())
                return d[:15] + '...' + d[-3:]
        if digest_type == 'sha256-spec-ex':
            d = _file_digest(filename, hashlib.sha256())
            return d[:6] + '...' + d[-3:]
    raise ValueError('Unsupport digest type %s' % digest_type)


DIGEST_REGEXES = {'sha512':'^[0-9a-fA-F]{128}$', 
 'sha256':'^[0-9a-fA-F]{64}$', 
 'sha1':'^[0-9a-fA-F]{40}$', 
 'md5':'^[0-9a-fA-F]{32}$', 
 'blake2b-512':'^[0-9a-fA-F]{128}$', 
 'blake2b-384':'^[0-9a-fA-F]{96}$', 
 'blake2b-256':'^[0-9a-fA-F]{64}$', 
 'blake2b-160':'^[0-9a-fA-F]{40}$', 
 'sha512-spec-ex':'^[0-9a-f]{15}\\.\\.\\.[0-9a-f]{3}$', 
 'sha256-spec-ex':'^[0-9a-f]{6}\\.\\.\\.[0-9a-f]{3}$'}

def digest_regex(digest_type='sha512'):
    """Regex to be used to check the un-normalized form of a digest string."""
    try:
        return DIGEST_REGEXES[digest_type]
    except KeyError:
        raise ValueError('Unsupport digest type %s' % digest_type)


def normalized_digest(digest, digest_type='sha512'):
    """Normalized version of the digest that enables string comparison.

    All forms (except the spec example forms) are case insensitive. We
    use lowercase as the normalized form.
    """
    if digest_type != 'sha512-spec-ex':
        if digest_type != 'sha256-spec-ex':
            return digest.lower()
    return digest