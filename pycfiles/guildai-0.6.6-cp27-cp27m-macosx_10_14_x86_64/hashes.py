# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_internal/utils/hashes.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import absolute_import
import hashlib
from pip._vendor.six import iteritems, iterkeys, itervalues
from pip._internal.exceptions import HashMismatch, HashMissing, InstallationError
from pip._internal.utils.misc import read_chunks
FAVORITE_HASH = 'sha256'
STRONG_HASHES = [
 'sha256', 'sha384', 'sha512']

class Hashes(object):
    """A wrapper that builds multiple hashes at once and checks them against
    known-good values

    """

    def __init__(self, hashes=None):
        """
        :param hashes: A dict of algorithm names pointing to lists of allowed
            hex digests
        """
        self._allowed = {} if hashes is None else hashes
        return

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
                raise InstallationError('Unknown hash name: %s' % hash_name)

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
    """A workalike for Hashes used when we're missing a hash for a requirement

    It computes the actual hash of the requirement and raises a HashMissing
    exception showing it to the user.

    """

    def __init__(self):
        """Don't offer the ``hashes`` kwarg."""
        super(MissingHashes, self).__init__(hashes={FAVORITE_HASH: []})

    def _raise(self, gots):
        raise HashMissing(gots[FAVORITE_HASH].hexdigest())