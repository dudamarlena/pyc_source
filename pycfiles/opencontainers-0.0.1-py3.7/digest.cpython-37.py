# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/digest/digest.py
# Compiled at: 2019-11-06 10:19:30
# Size of source mod 2**32: 3011 bytes
from opencontainers.struct import StrStruct
from opencontainers.logger import bot
from .algorithm import Algorithm
import re

class Digest(StrStruct):
    __doc__ = 'Digest allows simple protection of hex formatted digest strings, prefixed\n       by their algorithm. Strings of type Digest have some guarantee of being in\n       the correct format and it provides quick access to the components of a\n       digest string.\n\n       The following is an example of the contents of Digest types:\n       sha256:7173b809ca12ec5dee4506cd86be934c4596dd234ee82c0662eac04a8c2c71dc\n       This allows to abstract the digest behind this type and work only in those\n       terms.\n    '

    def __init__(self, value=None):
        super().__init__(value)

    def validate(self):
        """Validate checks that the contents of self (the digest) is valid
        """
        regexp = '^[a-z0-9]+(?:[+._-][a-z0-9]+)*:[a-zA-Z0-9=_-]+$'
        if not re.search(regexp, self):
            bot.exit('%s does not match %s' % (self, regexp))
        algorithm, encoded = self.split(':')
        match = re.search('[+._-]', algorithm)
        if match:
            algorithm = algorithm[:match.start()]
        algorithm = Algorithm(algorithm)
        return algorithm.validate(encoded)

    def sepIndex(self):
        """return the index of the : separator"""
        return self.index(':', 1)

    def algorithm(self):
        """Algorithm returns the algorithm portion of the digest. 
        """
        return Algorithm(self[:self.sepIndex()])

    def encoded(self):
        """Encoded returns the encoded portion of the digest.
        """
        return self[self.sepIndex() + 1:]

    def verifier(self):
        """Verifier returns a writer object that can be used to verify a stream of
           content against the digest. If the digest is invalid, the method will panic.
        """
        from .verifiers import hashVerifier
        return hashVerifier((self.algorithm.hash()), digest=self)


DigestRegexp = re.compile('[a-z0-9]+(?:[.+_-][a-z0-9]+)*:[a-zA-Z0-9=_-]+')
DigestRegexpAnchored = re.compile('^%s$' % DigestRegexp)

def NewDigestFromEncoded(algorithm, encoded):
    """NewDigestFromEncoded returns a Digest from alg and the encoded digest.
    """
    return Digest('%s:%s' % (algorithm, encoded))


def Parse(string):
    """Parse parses s and returns the validated digest object. An error will
       be returned if the format is invalid.
    """
    d = Digest(s)
    d.validate()
    return d