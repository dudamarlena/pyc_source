# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/https/request.py
# Compiled at: 2015-11-05 10:40:17
"""
.. py:module:: bridgedb.https.request
    :synopsis: Classes for parsing and storing information about requests for
               bridges which are sent to the HTTPS distributor.

bridgedb.https.request
======================

Classes for parsing and storing information about requests for bridges
which are sent to the HTTPS distributor.

.. inheritance-diagram:: HTTPSBridgeRequest

::

  bridgedb.https.request
   |
   |_ HTTPSBridgeRequest - A request for bridges which was received through
                           the HTTPS distributor.

..
"""
from __future__ import print_function
from __future__ import unicode_literals
import ipaddr, logging, re
from bridgedb import bridgerequest
from bridgedb import geo
from bridgedb.parse import addr
TRANSPORT_REGEXP = b'[_a-zA-Z][_a-zA-Z0-9]*'
TRANSPORT_PATTERN = re.compile(TRANSPORT_REGEXP)
UNBLOCKED_REGEXP = b'[a-zA-Z]{2}'
UNBLOCKED_PATTERN = re.compile(UNBLOCKED_REGEXP)

class HTTPSBridgeRequest(bridgerequest.BridgeRequestBase):
    """We received a request for bridges through the HTTPS distributor."""

    def __init__(self, addClientCountryCode=True):
        """Process a new bridge request received through the
        :class:`~bridgedb.https.distributor.HTTPSDistributor`.

        :param bool addClientCountryCode: If ``True``, then calling
            :meth:`withoutBlockInCountry` will attempt to add the client's own
            country code, geolocated from her IP, to the ``notBlockedIn``
            countries list.
        """
        super(HTTPSBridgeRequest, self).__init__()
        self.addClientCountryCode = addClientCountryCode

    def withIPversion(self, parameters):
        """Determine if the request **parameters** were for bridges with IPv6
        addresses or not.

        .. note:: If there is an ``ipv6=`` parameter with anything non-zero
            after it, then we assume the client wanted IPv6 bridges.

        :param parameters: The :api:`twisted.web.http.Request.args`.
        """
        if parameters.get(b'ipv6', False):
            logging.info(b'HTTPS request for bridges with IPv6 addresses.')
            self.withIPv6()

    def withoutBlockInCountry(self, request):
        """Determine which countries the bridges for this **request** should
        not be blocked in.

        .. note:: Currently, a **request** for unblocked bridges is recognized
            if it contains an HTTP GET parameter ``unblocked=`` whose value is
            a comma-separater list of two-letter country codes.  Any
            two-letter country code found in the
            :api:`request <twisted.web.http.Request>` ``unblocked=`` HTTP GET
            parameter will be added to the :data:`notBlockedIn` list.

        If :data:`addClientCountryCode` is ``True``, the the client's own
        geolocated country code will be added to the to the
        :data`notBlockedIn` list.

        :type request: :api:`twisted.web.http.Request`
        :param request: A ``Request`` object containing the HTTP method, full
            URI, and any URL/POST arguments and headers present.
        """
        countryCodes = request.args.get(b'unblocked', list())
        for countryCode in countryCodes:
            try:
                country = UNBLOCKED_PATTERN.match(countryCode).group()
            except (TypeError, AttributeError):
                pass
            else:
                if country:
                    self.notBlockedIn.append(country.lower())
                    logging.info(b'HTTPS request for bridges not blocked in: %r' % country)

        if self.addClientCountryCode:
            if addr.isIPAddress(self.client):
                country = geo.getCountryCode(ipaddr.IPAddress(self.client))
                if country:
                    self.notBlockedIn.append(country.lower())
                    logging.info(b"HTTPS client's bridges also shouldn't be blocked in their GeoIP country code: %s" % country)

    def withPluggableTransportType(self, parameters):
        """This request included a specific Pluggable Transport identifier.

        Add any Pluggable Transport methodname found in the HTTP GET
        **parameters** to the list of ``transports``. Currently, a request for
        a transport is recognized if the request contains the
        ``'transport='`` parameter.

        :param parameters: The :api:`twisted.web.http.Request.args`.
        """
        for methodname in parameters.get(b'transport', list()):
            try:
                transport = TRANSPORT_PATTERN.match(methodname).group()
            except (TypeError, AttributeError):
                pass
            else:
                if transport:
                    self.transports.append(transport)
                    logging.info(b'HTTPS request for transport type: %r' % transport)