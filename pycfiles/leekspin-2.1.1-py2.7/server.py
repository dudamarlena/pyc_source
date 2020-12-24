# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/leekspin/server.py
# Compiled at: 2016-07-15 02:26:55
"""Functions for creating mock ``[bridge-]server-descriptors``."""
import math, random
from leekspin import crypto
from leekspin import torversions

def generateServerDescriptor(nick, fingerprint, timestamp, ipv4, ipv6, port, vers, protocols, uptime, bandwidth, extraInfoHexDigest, onionKeyLine, signingKeyLine, publicNTORKey, bridge=True):
    """Generate an ``@type [bridge-]server-descriptor``.

    :param str nick: The router's nickname.
    :param str fingerprint: The SHA-1 digest of the router's public identity
        key.
    :param str timestamp: An ISO 8601 timestamp, with a space as the separator.
    :param str ipv4: The IP address for router's main ``ORAddress``.
    :param str ipv6: Any IPv6 ``ORAddress`` es for this router.
    :param str port: The port for the router's main ``ORAddress``.
    :param str vers: One of :data:`~leekspin.torversions.SERVER_VERSIONS`.
    :param str protocols: The OR protocol versions supported by this router.
    :param str uptime: The current uptime for this router.
    :param str bandwidth: A bandwidth history line for this router.
    :param str extraInfoHexDigest: The SHA-1 digest of the router's
        ``@type [bridge-]extrainfo`` descriptor, before the extrainfo
        descriptor is signed.
    :param str onionKeyLine: An ``onion-key`` line.
    :param str signingKeyLine: A ``signing-key`` line.
    :param str publicNTORKey: An ``ntor-onion-key``.
    :param bool bridge: If ``True``, create a Bridge descriptor. If ``False``,
        create a Relay descriptor.
    """
    doc = []
    doc.append('router %s %s %s 0 0' % (nick, ipv4, port))
    doc.append('or-address [%s]:%s' % (ipv6, port - 1))
    doc.append('platform Tor %s on Linux' % vers)
    doc.append('%s' % protocols)
    doc.append('published %s' % timestamp)
    doc.append('%s' % makeFingerprintLine(fingerprint, vers))
    doc.append('uptime %s' % uptime)
    doc.append('%s' % bandwidth)
    doc.append('%s' % makeExtraInfoDigestLine(extraInfoHexDigest, vers))
    if onionKeyLine:
        doc.append('%s' % onionKeyLine)
    doc.append('%s' % signingKeyLine)
    if not bridge:
        doc.append('%s' % makeHSDirLine(vers))
    doc.append('contact Somebody <somebody@example.com>')
    if publicNTORKey is not None:
        doc.append('ntor-onion-key %s' % publicNTORKey)
    doc.append('reject *:*')
    doc.append('router-signature\n')
    unsignedDescriptor = ('\n').join(doc)
    return unsignedDescriptor


def makeProtocolsLine(version=None):
    """Generate an appropriate ``[bridge-]server-descriptor`` ``protocols``
    line.

    :param str version: One of :data:`~leekspin.torversions.SERVER_VERSIONS`.
    :rtype: str
    :returns: An ``@type [bridge-]server-descriptor`` ``protocols`` line.
    """
    line = ''
    if version is not None and torversions.shouldHaveOptPrefix(version):
        line += 'opt '
    line += 'protocols Link 1 2 Circuit 1'
    return line


def makeExtraInfoDigestLine(hexdigest, version):
    """Create a line to embed the hex SHA-1 digest of the extrainfo.

    :param str hexdigest: Should be the hex-encoded (uppercase) output of
        the SHA-1 digest of the generated extrainfo document (this is the
        extra-info descriptor, just without the signature at the end). This is
        the same exact digest which gets signed by the OR server identity key,
        and that signature is appended to the extrainfo document to create the
        extra-info descriptor.
    :param str version: One of :data:`~leekspin.torversions.SERVER_VERSIONS`.
    :rtype: str
    :returns: An ``@type [bridge-]server-descriptor`` ``extra-info-digest``
        line.
    """
    line = ''
    if version is not None and torversions.shouldHaveOptPrefix(version):
        line += 'opt '
    line += 'extra-info-digest %s' % hexdigest
    return line


def makeFingerprintLine(fingerprint, version=None):
    """Generate an appropriate ``[bridge-]server-descriptor`` ``fingerprint``
    line.

    For example, for tor-0.2.3.25 and prior versions, this would look like:
      |
      | opt fingerprint D4BB C339 2560 1B7F 226E 133B A85F 72AF E734 0B29
      |

    :param str fingerprint: A public key fingerprint in groups of four,
         separated by spaces.
    :param str version: One of :data:`~leekspin.torversions.SERVER_VERSIONS`.
    :rtype: str
    :returns: An ``@type [bridge-]server-descriptor`` ``fingerprint`` line.
    """
    line = ''
    if version is not None and torversions.shouldHaveOptPrefix(version):
        line += 'opt '
    line += 'fingerprint %s' % fingerprint
    return line


def makeBandwidthLine(variance=30):
    u"""Create a random ``bandwidth`` line with some plausible bandwidth burst
    variance.

    From `dir-spec.txt`_ §2.1 "Router descriptors"::

        "bandwidth" bandwidth-avg bandwidth-burst bandwidth-observed NL

        [Exactly once]

          Estimated bandwidth for this router, in bytes per second.  The
          "average" bandwidth is the volume per second that the OR is willing
          to sustain over long periods; the "burst" bandwidth is the volume
          that the OR is willing to sustain in very short intervals.  The
          "observed" value is an estimate of the capacity this relay can
          handle.  The relay remembers the max bandwidth sustained output over
          any ten second period in the past day, and another sustained input.
          The "observed" value is the lesser of these two numbers.

    .. _dir-spec.txt: https://gitweb.torproject.org/torspec.git/tree/dir-spec.txt

    The ``observed`` bandwidth, in this function, is taken as some random value,
    bounded between 20KB/s and 2MB/s. For example, say:

    >>> import math
    >>> variance = 25
    >>> observed = 180376
    >>> percentage = float(variance) / 100.
    >>> percentage
    0.25

    The ``variance`` in this context is the percentage of the ``observed``
    bandwidth, which will be added to the ``observed`` bandwidth, and becomes
    the value for the ``burst`` bandwidth:

    >>> burst = observed + math.ceil(observed * percentage)
    >>> assert burst > observed

    This doesn't do much, since the ``burst`` bandwidth in a real
    ``@type [bridge-]server-descriptor`` is reported by the OR; this function
    mostly serves to avoid generating completely-crazy, totally-implausible
    bandwidth values. The ``average`` bandwidth value is then just the mean
    value of the other two.

    :param int variance: The percent of the fake ``observed`` bandwidth to
        increase the ``burst`` bandwidth by.
    :rtype: str
    :returns: A ``bandwidth`` line for an ``@type [bridge-]server-descriptor``.
    """
    observed = random.randint(20 * 1024, 2 * 1073741824)
    percentage = float(variance) / 100.0
    burst = int(observed + math.ceil(observed * percentage))
    bandwidths = [burst, observed]
    nitems = len(bandwidths) if len(bandwidths) > 0 else float('nan')
    avg = int(math.ceil(float(sum(bandwidths)) / nitems))
    line = 'bandwidth %s %s %s' % (avg, burst, observed)
    return line


def makeHSDirLine(version):
    u"""This line doesn't do much… all the cool kids are ``HSDir`` s these days.

    :param str version: One of :data:`~leekspin.torversions.SERVER_VERSIONS`.
    :rtype: str
    :returns: An ``@type [bridge-]server-descriptor`` ``hidden-service-dir``
        line.
    """
    line = ''
    if version is not None and torversions.shouldHaveOptPrefix(version):
        line += 'opt '
    line += 'hidden-service-dir'
    return line