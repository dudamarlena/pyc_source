# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/bridgerequest.py
# Compiled at: 2016-05-30 19:29:39
__doc__ = 'API for creating classes which store information on the type of bridges\nrequested by a client.\n\n.. inheritance-diagram:: BridgeRequestBase\n    :parts: 1\n'
import ipaddr, logging
from zope.interface import implementer
from zope.interface import Attribute
from zope.interface import Interface
from bridgedb.crypto import getHMACFunc
from bridgedb.filters import byIPv
from bridgedb.filters import byNotBlockedIn
from bridgedb.filters import byTransport

class IRequestBridges(Interface):
    """Interface specification of client options for requested bridges."""
    filters = Attribute('A list of callables used to filter bridges from a hashring.')
    ipVersion = Attribute('The IP version of bridge addresses to distribute to the client.')
    transports = Attribute('A list of strings of Pluggable Transport types requested.')
    notBlockedIn = Attribute('A list of two-character country codes. The distributed bridges should not be blocked in these countries.')
    valid = Attribute("A boolean. Should be ``True`` if the client's request was valid.")
    client = Attribute('This should be some information unique to the client making the request for bridges, such that we are able to HMAC this unique data, via :meth:`getHashringPlacement()`, in order to place the client into a hashring (determining which bridge addresses they get in the request response).')

    def addFilter():
        """Add a filter to the list of ``filters``."""
        pass

    def clearFilters():
        """Clear the list of ``filters``."""
        pass

    def generateFilters():
        """Build the list of callables, ``filters``, according to the current
        contents of the lists of ``transports``, ``notBlockedIn``, and the
        ``ipVersion``.
        """
        pass

    def getHashringPlacement():
        """Use some unique parameters of the client making this request to
        obtain a value which we can use to place them into one of the hashrings
        with :class:`~bridgedb.bridges.Bridge`s in it, in order to give that
        client different bridges than other clients.
        """
        pass

    def isValid():
        """Determine if the request is ``valid`` according to some parameters."""
        pass

    def withIPv4():
        """Set the ``ipVersion`` to IPv4."""
        pass

    def withIPv6():
        """Set the ``ipVersion`` to IPv6."""
        pass

    def withPluggableTransportType(typeOfPT):
        """Add this **typeOfPT** to the list of requested ``transports``."""
        pass

    def withoutBlockInCountry(countryCode):
        """Add this **countryCode** to the list of countries which distributed
        bridges should not be blocked in (``notBlockedIn``).
        """
        pass


@implementer(IRequestBridges)
class BridgeRequestBase(object):
    """A generic base class for storing options of a client bridge request.

    :vartype filters: list
    :ivar filters: A list of callables used to filter bridges from a hashring.
    :vartype transports: list
    :ivar transports: A list of strings of Pluggable Transport types requested.
    :vartype notBlockedIn: list
    :ivar notBlockedIn: A list of two-character country codes. The distributed
        bridges should not be blocked in these countries.
    :vartype client: str
    :ivar client: This should be some information unique to the client making
        the request for bridges, such that we are able to HMAC this unique
        data in order to place the client into a hashring (determining which
        bridge addresses they get in the request response). It defaults to the
        string ``'default'``.
    :vartype valid: bool
    :ivar valid: Should be ``True`` if the client's request was valid.
    """

    def __init__(self, ipVersion=None):
        self.ipVersion = ipVersion
        self.filters = list()
        self.transports = list()
        self.notBlockedIn = list()
        self.client = 'default'
        self.valid = False

    @property
    def ipVersion(self):
        """The IP version of bridge addresses to distribute to the client.

        :rtype: int
        :returns: Either ``4`` or ``6``.
        """
        return self._ipVersion

    @ipVersion.setter
    def ipVersion(self, ipVersion):
        """The IP version of bridge addresses to distribute to the client.

        :param int ipVersion: The IP address version for the bridge lines we
            should distribute in response to this client request.
        """
        if ipVersion not in (4, 6):
            ipVersion = 4
        self._ipVersion = ipVersion

    def getHashringPlacement(self, key, client=None):
        """Create an HMAC of some **client** info using a **key**.

        :param str key: The key to use for HMACing.
        :param str client: Some (hopefully unique) information about the
            client who is requesting bridges, such as an IP or email address.
        :rtype: long
        :returns: A long specifying index of the first node in a hashring to
            be distributed to the client. This value should obviously be used
            mod the number of nodes in the hashring.
        """
        if not client:
            client = self.client
        digest = getHMACFunc(key)(client)
        position = long(digest[:8], 16)
        return position

    def isValid(self, valid=None):
        """Get or set the validity of this bridge request.

        If called without parameters, this method will return the current
        state, otherwise (if called with the **valid** parameter), it will set
        the current state of validity for this request.

        :param bool valid: If given, set the validity state of this
            request. Otherwise, get the current state.
        """
        if valid is not None:
            self.valid = bool(valid)
        return self.valid

    def withIPv4(self):
        """Set the ``ipVersion`` to IPv4."""
        self.ipVersion = 4

    def withIPv6(self):
        """Set the ``ipVersion`` to IPv6."""
        self.ipVersion = 6

    def withoutBlockInCountry(self, country):
        """Add this **countryCode** to the list of countries which distributed
        bridges should not be blocked in (``notBlockedIn``).
        """
        self.notBlockedIn.append(country.lower())

    def withPluggableTransportType(self, pt):
        """Add this **pt** to the list of requested ``transports``.

        :param str pt: A :class:`~bridgedb.bridges.PluggableTransport`.
            :data:`methodname <bridgedb.bridges.PluggableTransport.methodname>`.
        """
        self.transports.append(pt)

    def addFilter(self, filtre):
        """Add a **filtre** to the list of ``filters``.

        :type filter: callable
        :param filter: A filter function, e.g. one generated via
            :mod:`bridgedb.filters`.
        """
        self.filters.append(filtre)

    def clearFilters(self):
        """Clear the list of ``filters``."""
        self.filters = []

    def justOnePTType(self):
        """Get just one bridge type (e.g. a
        :data:`methodname <bridgedb.bridges.PluggableTransport.methodname>` of
        :class:`~bridgedb.bridges.PluggableTransport`) at a time!
        """
        ptType = None
        try:
            ptType = self.transports[(-1)]
        except IndexError:
            logging.debug('No pluggable transports were requested.')

        return ptType

    def generateFilters(self):
        """Build the list of callables, ``filters``, according to the current
        contents of the lists of ``transports``, ``notBlockedIn``, and the
        ``ipVersion``.
        """
        self.clearFilters()
        pt = self.justOnePTType()
        msg = 'Adding a filter to %s for %s for IPv%d' % (
         self.__class__.__name__, self.client, self.ipVersion)
        if self.notBlockedIn:
            for country in self.notBlockedIn:
                logging.info('%s %s bridges not blocked in %s...' % (
                 msg, pt or 'vanilla', country))
                self.addFilter(byNotBlockedIn(country, pt, self.ipVersion))

        elif pt:
            logging.info('%s %s bridges...' % (msg, pt))
            self.addFilter(byTransport(pt, self.ipVersion))
        else:
            logging.info('%s bridges...' % msg)
            self.addFilter(byIPv(self.ipVersion))