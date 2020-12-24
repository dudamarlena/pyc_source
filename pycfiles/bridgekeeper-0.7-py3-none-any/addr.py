# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/parse/addr.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = b'Utilities for parsing IP and email addresses.\n\n.. py:module:: bridgedb.parse.addr\n    :synopsis: Parsers for finding and validating IP addresses, email\n        addresses, and port ranges.\n\n\nbridgedb.parse.addr\n===================\n\n::\n\n  parse.addr\n   | |_ extractEmailAddress() - Validate a :rfc:2822 email address.\n   | |_ isIPAddress() - Check if an arbitrary string is an IP address.\n   | |_ isIPv4() - Check if an arbitrary string is an IPv4 address.\n   | |_ isIPv6() - Check if an arbitrary string is an IPv6 address.\n   | \\_ isValidIP() - Check that an IP address is valid.\n   |\n   |_ PortList - A container class for validated port ranges.\n\n..\n\n\nHow address validity is determined\n----------------------------------\n\nThe following terms define addresses which are **not** valid. All other\naddresses are taken to be valid.\n\n\nPrivate IP Address Ranges\n^^^^^^^^^^^^^^^^^^^^^^^^^\n.. glossary::\n\n   Private Address\n     These address ranges are reserved by IANA for private intranets, and not\n     routable to the Internet::\n         10.0.0.0    - 10.255.255.255  (10.0.0.0/8)\n         172.16.0.0  - 172.31.255.255  (172.16.0.0/12)\n         192.168.0.0 - 192.168.255.255 (192.168.0.0/16)\n     For additional information, see :rfc:`1918`.\n\n\nReserved and Special Use Addresses\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n.. glossary::\n\n   Unspecified Address\n   Default Route\n     Current network (only valid as source address). See :rfc:`1122`. An\n     **Unspecified Address** in the context of firewalls means "all addresses\n     of the local machine". In a routing context, it is usually termed the\n     **Default Route**, and it means the default route (to "the rest of" the\n     internet). See :rfc:`1700`.\n     For example::\n         0.0.0.0/8\n         ::/128\n\n   Loopback Address\n     Reserved for loopback and IPC on the localhost. See :rfc:`1122`.\n     Example::\n         127.0.0.0\n\n   Localhost Address\n     Loopback IP addresses (refers to self). See :rfc:`5735`.\n     Examples include::\n         127.0.0.1 - 127.255.255.254   (127.0.0.0/8)\n         ::1\n\n   Link-Local Address\n     These are the link-local blocks, used for communication between hosts on\n     a single link. See :rfc:`3927`.\n     Examples::\n         169.254.0.0/16\n         fe80::/64\n\n   Multicast Address\n     Reserved for multicast addresses. See :rfc:`3171`.\n     For example::\n         224.0.0.0 - 239.255.255.255 (224.0.0.0/4)\n\n   Private Address\n     Reserved for private networks. See :rfc:`1918`.\n     Some examples include::\n         10.0.0.0/8\n         172.16.0.0/12\n         192.168.0.0/16\n\n   Reserved Address\n     Reserved (former Class E network). See :rfc:`1700`, :rfc:`3232`, and\n     :rfc:`5735`. The one exception to this rule is the :term:`Limited\n     Broadcast Address`, ``255.255.255.255`` for which packets at the IP\n     layer are not forwarded to the public internet. For example::\n         240.0.0.0 - 255.255.255.255 (240.0.0.0/4)\n\n   Limited Broadcast Address\n     Limited broadcast address (limited to all other nodes on the LAN). See\n     :rfc:`919`. For IPv4, ``255`` in any part of the IP is reserved for\n     broadcast addressing to the local LAN, e.g.::\n         255.255.255.255\n\n\n.. warning:: The :mod:`ipaddr` module (as of version 2.1.10) does not\n             understand the following reserved_ addresses:\n.. _reserved: https://tools.ietf.org/html/rfc5735#page-4\n\n.. glossary::\n\n   Reserved Address (Protocol Assignments)\n     Reserved for IETF protocol assignments. See :rfc:`5735`.\n     Example::\n         192.0.0.0/24\n\n   Reserved Address (6to4 Relay Anycast)\n     IPv6 to IPv4 relay. See :rfc:`3068`.\n     Example::\n         192.88.99.0/24\n\n   Reserved Address (Network Benchmark)\n     Network benchmark tests. See :rfc:`2544`.\n     Example::\n         198.18.0.0/15\n\n   Reserved Address (TEST-NET-1)\n     Reserved for use in documentation and example code. It is often used in\n     conjunction with domain names ``example.com`` or ``example.net`` in\n     vendor and protocol documentation. See :rfc:`1166`.\n     For example::\n         192.0.2.0/24\n\n   Reserved Address (TEST-NET-2)\n     TEST-NET-2. See :rfc:`5737`.\n     Example::\n         198.51.100.0/24\n\n   Reserved Address (TEST-NET-3)\n     TEST-NET-3. See :rfc:`5737`.\n     Example::\n         203.0.113.0/24\n\n   Shared Address Space\n     See :rfc:`6598`.\n     Example::\n         100.64.0.0/10\n\n   Site-Local Address\n   Unique Local Address\n     Similar uses to :term:`Limited Broadcast Address`. For IPv6, everything\n     becomes convoluted_ and complicated_, and then redefined_. See\n     :rfc:`4193`, :rfc:`3879`, and :rfc:`3513`. The\n     :meth:`ipaddr.IPAddress.is_site_local` method *only* checks to see if\n     the address is a **Unique Local Address** vis-á-vis :rfc:`3513` §2.5.6,\n     e.g.::\n         ff00::0/8\n         fec0::/10\n\n..\n\n.. _convoluted: https://en.wikipedia.org/wiki/IPv6_address#Multicast_addresses\n.. _complicated: https://en.wikipedia.org/wiki/IPv6_address#IPv6_address_scopes\n.. _redefined: https://en.wikipedia.org/wiki/Unique_local_address\n'
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import logging, re, ipaddr
ASPECIAL = b'-_+/=_~'
ACHAR = b'[\\w%s]' % (b'').join(b'\\%s' % c for c in ASPECIAL)
DOTATOM = b'%s+(?:\\.%s+)*' % (ACHAR, ACHAR)
DOMAIN = b'\\w+(?:\\.\\w+)*'
ADDRSPEC = b'(%s)\\@(%s)' % (DOTATOM, DOMAIN)
SPACE_PAT = re.compile(b'\\s+')
ADDRSPEC_PAT = re.compile(ADDRSPEC)

class BadEmail(Exception):
    """Exception raised when we get a bad email address."""

    def __init__(self, msg, email):
        Exception.__init__(self, msg)
        self.email = email


class InvalidPort(ValueError):
    """Raised when a given port number is invalid."""


class UnsupportedDomain(ValueError):
    """Raised when we get an email address from an unsupported domain."""


def canonicalizeEmailDomain(domain, domainmap):
    """Decide if an email was sent from a permitted domain.

    :param str domain: The domain portion of an email address to validate. It
        will be checked that it is one of the domains allowed to email
        requests for bridges to the
        :class:`~bridgedb.email.distributor.EmailDistributor`.
    :param dict domainmap: A map of permitted alternate domains (in lowercase)
        to their canonical domain names (in lowercase). This can be configured
        with the ``EMAIL_DOMAIN_MAP`` option in ``bridgedb.conf``, for
        example::
            EMAIL_DOMAIN_MAP = {'mail.google.com': 'gmail.com',
                                'googlemail.com': 'gmail.com'}

    :raises UnsupportedDomain: if the domain portion of the email address is
        not within the map of alternate to canonical allowed domain names.
    :rtype: str
    :returns: The canonical domain name for the email address.
    """
    permitted = None
    try:
        permitted = domainmap.get(domain)
    except AttributeError:
        logging.debug(b"Got non-dict for 'domainmap' parameter: %r" % domainmap)

    if not permitted:
        raise UnsupportedDomain(b'Domain not permitted: %s' % domain)
    return permitted


def extractEmailAddress(emailaddr):
    """Given an email address, obtained for example, via a ``From:`` or
    ``Sender:`` email header, try to extract and parse (according to
    :rfc:`2822`) the local and domain portions.

    We only allow the following form::

        LOCAL_PART := DOTATOM
        DOMAIN := DOTATOM
        ADDRSPEC := LOCAL_PART "@" DOMAIN

    In particular, we are disallowing: obs-local-part, obs-domain, comment,
    and obs-FWS. Other forms exist, but none of the incoming services we
    recognize support them.

    :param emailaddr: An email address to validate.
    :raises BadEmail: if the **emailaddr** couldn't be validated or parsed.
    :returns: A tuple of the validated email address, containing the mail
        local part and the domain::
            (LOCAL_PART, DOMAIN)
    """
    orig = emailaddr
    try:
        addr = SPACE_PAT.sub(b' ', emailaddr).strip()
    except TypeError as error:
        logging.debug(error)
        raise BadEmail(b"Can't extract address from object type %r!" % type(orig), orig)

    if b'<' in addr:
        idx = addr.rindex(b'<')
        addr = addr[idx:]
        m = re.search(b'<([^>]*)>', addr)
        if m is None:
            raise BadEmail(b"Couldn't extract address spec", orig)
        addr = m.group(1)
    addr = addr.replace(b' ', b'')
    m = ADDRSPEC_PAT.match(addr)
    if not m:
        raise BadEmail(b'Bad address spec format', orig)
    localpart, domain = m.groups()
    return (
     localpart, domain)


def isIPAddress(ip, compressed=True):
    """Check if an arbitrary string is an IP address, and that it's valid.

    :type ip: basestring or int
    :param ip: The IP address to check.
    :param boolean compressed: If True, return a string representing the
        compressed form of the address. Otherwise, return an
        :class:`ipaddr.IPAddress` instance.
    :rtype: A :class:`ipaddr.IPAddress`, or a string, or False
    :returns: The IP, as a string or a class, if it passed the
        checks. Otherwise, returns False.
    """
    try:
        ip = ipaddr.IPAddress(ip)
    except ValueError:
        return False

    if isValidIP(ip):
        if compressed:
            return ip.compressed
        else:
            return ip

    return False


def isIPv(version, ip):
    """Check if **ip** is a certain **version** (IPv4 or IPv6).

    .. warning: Do *not* put any calls to the logging module in this function,
        or else an infinite recursion will occur when the call is made, due
        the the log :class:`~logging.Filter`s in :mod:`~bridgedb.safelog`
        using this function to validate matches from the regular expression
        for IP addresses.

    :param integer version: The IPv[4|6] version to check; must be either
        ``4`` or ``6``. Any other value will be silently changed to ``4``.
    :param ip: The IP address to check. May be an any type which
        :class:`ipaddr.IPAddress` will accept.
    :rtype: boolean
    :returns: ``True``, if the address is an IPv4 address.
    """
    try:
        ipaddr.IPAddress(ip, version=version)
    except (ipaddr.AddressValueError, Exception):
        return False

    return True
    return False


def isIPv4(ip):
    """Check if an address is IPv4.

    .. attention:: This does *not* check validity. See :func:`isValidIP`.

    :type ip: basestring or int
    :param ip: The IP address to check.
    :rtype: boolean
    :returns: True if the address is an IPv4 address.
    """
    return isIPv(4, ip)


def isIPv6(ip):
    """Check if an address is IPv6.

    .. attention:: This does *not* check validity. See :func:`isValidIP`.

    :type ip: basestring or int
    :param ip: The IP address to check.
    :rtype: boolean
    :returns: True if the address is an IPv6 address.
    """
    return isIPv(6, ip)


def isValidIP(ip):
    """Check that an IP (v4 or v6) is valid.

    The IP address, **ip**, must not be any of the following:

      * A :term:`Link-Local Address`,
      * A :term:`Loopback Address` or :term:`Localhost Address`,
      * A :term:`Multicast Address`,
      * An :term:`Unspecified Address` or :term:`Default Route`,
      * Any other :term:`Private Address`, or address within a privately
        allocated space, such as the IANA-reserved
        :term:`Shared Address Space`.

    If it is an IPv6 address, it also must not be:

      * A :term:`Site-Local Address` or an :term:`Unique Local Address`.

    >>> from bridgedb.parse.addr import isValidIP
    >>> isValidIP('1.2.3.4')
    True
    >>> isValidIP('1.2.3.255')
    True
    >>> isValidIP('1.2.3.256')
    False
    >>> isValidIP('1')
    False
    >>> isValidIP('1.2.3')
    False
    >>> isValidIP('xyzzy')
    False

    :type ip: An :class:`ipaddr.IPAddress`, :class:`ipaddr.IPv4Address`,
        :class:`ipaddr.IPv6Address`, or str
    :param ip: An IP address. If it is a string, it will be converted to a
        :class:`ipaddr.IPAddress`.
    :rtype: boolean
    :returns: ``True``, if **ip** passes the checks; False otherwise.
    """
    reasons = []
    try:
        if isinstance(ip, basestring):
            ip = ipaddr.IPAddress(ip)
        if ip.is_link_local:
            reasons.append(b'link local')
        if ip.is_loopback:
            reasons.append(b'loopback')
        if ip.is_multicast:
            reasons.append(b'multicast')
        if ip.is_private:
            reasons.append(b'private')
        if ip.is_unspecified:
            reasons.append(b'unspecified')
        if ip.version == 6 and ip.is_site_local:
            reasons.append(b'site local')
        elif ip.version == 4 and ip.is_reserved:
            reasons.append(b'reserved')
    except ValueError:
        reasons.append(b'cannot convert to ip')

    if reasons:
        explain = (b', ').join([ r for r in reasons ])
        logging.debug(b'IP address %r is invalid! Reason(s): %s' % (
         ip, explain))
        return False
    return True


def normalizeEmail(emailaddr, domainmap, domainrules, ignorePlus=True):
    """Normalise an email address according to the processing rules for its
    canonical originating domain.

    The email address, **emailaddr**, will be parsed and validated, and then
    checked that it originated from one of the domains allowed to email
    requests for bridges to the
    :class:`~bridgedb.email.distributor.EmailDistributor` via the
    :func:`canonicaliseEmailDomain` function.

    :param str emailaddr: An email address to normalise.
    :param dict domainmap: A map of permitted alternate domains (in lowercase)
        to their canonical domain names (in lowercase). This can be configured
        with the ``EMAIL_DOMAIN_MAP`` option in ``bridgedb.conf``, for
        example::

            EMAIL_DOMAIN_MAP = {'mail.google.com': 'gmail.com',
                                'googlemail.com': 'gmail.com'}

    :param dict domainrules: A mapping of canonical permitted domain names to
        a list of rules which should be applied to processing them, for
        example::

            EMAIL_DOMAIN_RULES = {'gmail.com': ["ignore_dots", "dkim"]

        Currently, ``"ignore_dots"`` means that all ``"."`` characters will be
        removed from the local part of the validated email address.

    :param bool ignorePlus: If ``True``, assume that
        ``blackhole+kerr@torproject.org`` is an alias for
        ``blackhole@torproject.org``, and remove everything after the first
        ``'+'`` character.

    :raises UnsupportedDomain: if the email address originated from a domain
        that we do not explicitly support.
    :raises BadEmail: if the email address could not be parsed or validated.
    :rtype: str
    :returns: The validated, normalised email address, if it was from a
        permitted domain. Otherwise, returns an empty string.
    """
    emailaddr = emailaddr.lower()
    localpart, domain = extractEmailAddress(emailaddr)
    canonical = canonicalizeEmailDomain(domain, domainmap)
    if ignorePlus:
        idx = localpart.find(b'+')
        if idx >= 0:
            localpart = localpart[:idx]
    rules = domainrules.get(canonical, [])
    if b'ignore_dots' in rules:
        localpart = localpart.replace(b'.', b'')
    normalized = b'%s@%s' % (localpart, domain)
    return normalized


class PortList(object):
    u"""A container class for validated port ranges.

    From torspec.git/dir-spec.txt §2.3:
      |
      | portspec ::= "*" | port | port "-" port
      | port ::= an integer between 1 and 65535, inclusive.
      |
      |    [Some implementations incorrectly generate ports with value 0.
      |     Implementations SHOULD accept this, and SHOULD NOT generate it.
      |     Connections to port 0 are never permitted.]
      |

    :ivar set ports: All ports which have been added to this ``PortList``.
    """
    PORTSPEC_LEN = 16

    def __init__(self, *args, **kwargs):
        """Create a :class:`~bridgedb.parse.addr.PortList`.

        :param args: Should match the ``portspec`` defined above.
        :raises: InvalidPort, if one of ``args`` doesn't match ``port`` as
            defined above.
        """
        self.ports = set()
        self.add(*args)

    def _sanitycheck(self, port):
        """Check that ``port`` is in the range [1, 65535] inclusive.

        :raises: InvalidPort, if ``port`` doesn't match ``port`` as defined
            in the excert from torspec above.
        :rtype: int
        :returns: The **port**, if no exceptions were raised.
        """
        if not isinstance(port, int) or not 0 < port <= 65535:
            raise InvalidPort(b'%s is not a valid port number!' % port)
        return port

    def __contains__(self, port):
        """Determine whether ``port`` is already in this ``PortList``.

        :returns: True if ``port`` is in this ``PortList``; False otherwise.
        """
        return port in self.ports

    def add(self, *args):
        """Add a port (or ports) to this ``PortList``.

        :param args: Should match the ``portspec`` defined above.
        :raises: InvalidPort, if one of ``args`` doesn't match ``port`` as
            defined above.
        """
        for arg in args:
            portlist = []
            try:
                if isinstance(arg, basestring):
                    ports = set([ int(p) for p in arg.split(b',')
                                ][:self.PORTSPEC_LEN])
                    portlist.extend([ self._sanitycheck(p) for p in ports ])
                if isinstance(arg, int):
                    portlist.append(self._sanitycheck(arg))
                if isinstance(arg, PortList):
                    self.add(list(arg.ports))
            except ValueError:
                raise InvalidPort(b'%s is not a valid port number!' % arg)

            self.ports.update(set(portlist))

    def __iter__(self):
        """Iterate through all ports in this PortList."""
        return self.ports.__iter__()

    def __str__(self):
        """Returns a pretty string representation of this PortList."""
        return (b',').join([ b'%s' % port for port in self.ports ])

    def __repr__(self):
        """Returns a raw depiction of this PortList."""
        return b"PortList('%s')" % self.__str__()

    def __len__(self):
        """Returns the total number of ports in this PortList."""
        return len(self.ports)

    def __getitem__(self, port):
        """Get the value of ``port`` if it is in this PortList.

        :raises: ValueError, if ``port`` isn't in this PortList.
        :rtype: integer
        :returns: The ``port``, if it is in this PortList.
        """
        return list(self.ports)[port]