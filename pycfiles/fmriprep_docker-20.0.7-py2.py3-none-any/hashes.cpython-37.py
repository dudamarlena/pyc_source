# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/utils/hashes.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 3986 bytes
from __future__ import absolute_import
import hashlib
from pip._vendor.six import iteritems, iterkeys, itervalues
from pip._internal.exceptions import HashMismatch, HashMissing, InstallationError
from pip._internal.utils.misc import read_chunks
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Dict, List, BinaryIO, NoReturn, Iterator
    from pip._vendor.six import PY3
    if PY3:
        from hashlib import _Hash
    else:
        from hashlib import _hash as _Hash
FAVORITE_HASH = 'sha256'
STRONG_HASHES = [
 'sha256', 'sha384', 'sha512']

class Hashes(object):
    __doc__ = 'A wrapper that builds multiple hashes at once and checks them against\n    known-good values\n\n    '

    def __init__(self, hashes=None):
        """
        :param hashes: A dict of algorithm names pointing to lists of allowed
            hex digests
        """
        self._allowed = {} if hashes is None else hashes

    @property
    def digest_count(self):
        return sum((len(digests) for digests in self._allowed.values()))

    def is_hash_allowed(self, hash_name, hex_digest):
        """Return whether the given hex digest is allowed."""
        return hex_digest in self._allowed.get(hash_name, [])

    def check_against_chunks(self, chunks):
        """Check good hashes against ones built from iterable of chunks of
        data.

        Raise HashMismatch if none match.

        """
        gots = {}
        for hash_name in iterkeys(self._allowed):
            try:
                gots[hash_name] = hashlib.new(hash_name)
            except (ValueError, TypeError):
                raise InstallationError('Unknown hash name: {}'.format(hash_name))

        for chunk in chunks:
            for hash in itervalues(gots):
                hash.update(chunk)

        for hash_name, got in iteritems(gots):
            if got.hexdigest() in self._allowed[hash_name]:
                return

        self._raise(gots)

    def _raise(self, gots):
        raise HashMismatch(self._allowed, gots)

    def check_against_file(self, file):
        """Check good hashes against a file-like object

        Raise HashMismatch if none match.

        """
        return self.check_against_chunks(read_chunks(file))

    def check_against_path(self, path):
        with open(path, 'rb') as (file):
            return self.check_against_file(file)

    def __nonzero__(self):
        """Return whether I know any known-good hashes."""
        return bool(self._allowed)

    def __bool__(self):
        return self.__nonzero__()


class MissingHashes(Hashes):
    __doc__ = "A workalike for Hashes used when we're missing a hash for a requirement\n\n    It computes the actual hash of the requirement and raises a HashMissing\n    exception showing it to the user.\n\n    "

    def __init__(self):
        super(MissingHashes, self).__init__(hashes={FAVORITE_HASH: []})

    def _raise(self, gots):
        raise HashMissing(gots[FAVORITE_HASH].hexdigest())