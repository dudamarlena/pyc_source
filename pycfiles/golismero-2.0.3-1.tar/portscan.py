# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/information/portscan.py
# Compiled at: 2014-01-14 18:58:51
"""
Portscan results.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'Portscan']
from . import Fingerprint
from .. import identity
from ..resource.ip import IP
from time import time

class Portscan(Fingerprint):
    """
    Portscan results.
    """
    information_type = Fingerprint.INFORMATION_PORTSCAN

    def __init__(self, ip, ports, timestamp=None):
        """
        :param ip: Scanned host's IP address.
        :type ip: IP

        :param ports: Portscan results.
            A set of tuples, each tuple containing the following data for
            each scanned port: state, protocol, port. The state is a string
            with one of the following values: "OPEN, "CLOSED" or "FILTERED".
            The protocol is a string with one of the following values: "TCP"
            or "UDP". The port is an integer from 0 to 65536, not included.
        :type ports: set( tuple(str, str, int), ... )

        :param timestamp: Timestamp for these portscan results.
            Defaults to the current time.
        :type timestamp: float
        """
        try:
            assert isinstance(ip, IP), type(ip)
            self.__address = ip.address
            self.__timestamp = float(timestamp) if timestamp else time()
            sane = set()
            visited = set()
            for state, protocol, port in ports:
                state = str(state.upper())
                protocol = str(protocol.upper())
                port = int(port)
                assert state in ('OPEN', 'CLOSED', 'FILTERED'), state
                assert protocol in ('TCP', 'UDP'), state
                assert 0 < port < 65536, port
                key = (protocol, port)
                assert key not in visited, key
                visited.add(key)
                sane.add((state, protocol, port))

            self.__ports = frozenset(sane)
        except Exception:
            raise ValueError('Malformed portscan results!')

        super(Portscan, self).__init__()
        self.add_resource(ip)

    @identity
    def address(self):
        """
        :returns: Scanned host's IP address.
        :rtype: str
        """
        return self.__address

    @identity
    def ports(self):
        """
        :returns: Portscan results.
            A set of tuples, each tuple containing the following data for
            each scanned port: state, protocol, port. The state is a string
            with one of the following values: "OPEN, "CLOSED" or "FILTERED".
            The protocol is a string with one of the following values: "TCP"
            or "UDP". The port is an integer from 0 to 65536, not included.
        :rtype: frozenset( tuple(str, str, int), ... )
        """
        return self.__ports

    @identity
    def timestamp(self):
        """
        :returns: Timestamp for these portscan results.
        :rtype: float
        """
        return self.__timestamp

    def __str__(self):
        return ('\n').join('%-8s %-3s %d' % p for p in sorted(self.ports))

    @property
    def display_name(self):
        return 'Port Scan Results'

    @property
    def open_tcp_ports(self):
        """
        :returns: Open TCP ports.
        :rtype: list(int)
        """
        ports = [ port for state, protocol, port in self.ports if state == 'OPEN' and protocol == 'TCP'
                ]
        ports.sort()
        return ports

    @property
    def closed_tcp_ports(self):
        """
        :returns: Closed TCP ports.
        :rtype: list(int)
        """
        ports = [ port for state, protocol, port in self.ports if state == 'CLOSED' and protocol == 'TCP'
                ]
        ports.sort()
        return ports

    @property
    def filtered_tcp_ports(self):
        """
        :returns: Filtered TCP ports.
        :rtype: list(int)
        """
        ports = [ port for state, protocol, port in self.ports if state == 'FILTERED' and protocol == 'TCP'
                ]
        ports.sort()
        return ports

    @property
    def open_udp_ports(self):
        """
        :returns: Open UDP ports.
        :rtype: list(int)
        """
        ports = [ port for state, protocol, port in self.ports if state == 'OPEN' and protocol == 'UDP'
                ]
        ports.sort()
        return ports

    @property
    def closed_udp_ports(self):
        """
        :returns: Closed UDP ports.
        :rtype: list(int)
        """
        ports = [ port for state, protocol, port in self.ports if state == 'CLOSED' and protocol == 'UDP'
                ]
        ports.sort()
        return ports

    @property
    def filtered_udp_ports(self):
        """
        :returns: Filtered UDP ports.
        :rtype: list(int)
        """
        ports = [ port for state, protocol, port in self.ports if state == 'FILTERED' and protocol == 'UDP'
                ]
        ports.sort()
        return ports