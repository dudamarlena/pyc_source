# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/resource/ip.py
# Compiled at: 2014-01-14 18:58:51
"""
IP address.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'IP']
from . import Resource
from .. import identity
from .. import Config
from ...text.text_utils import to_utf8
from netaddr import IPAddress

class IP(Resource):
    """
    IP address.
    """
    resource_type = Resource.RESOURCE_IP

    def __init__(self, address):
        """
        :param address: IP address.
        :type address: str
        """
        address = to_utf8(address)
        if not isinstance(address, str):
            raise TypeError('Expected str, got %r instead' % type(address))
        try:
            if address.startswith('[') and address.endswith(']'):
                parsed = IPAddress(address[1:-1], version=6)
                address = address[1:-1]
            else:
                parsed = IPAddress(address)
            version = int(parsed.version)
        except Exception:
            raise ValueError('Invalid IP address: %s' % address)

        self.__address = address
        self.__version = version
        super(IP, self).__init__()
        self.depth = 0

    def __str__(self):
        return self.address

    def __repr__(self):
        return '<IPv%s address=%r>' % (self.version, self.address)

    @property
    def display_name(self):
        return 'IP Address'

    @identity
    def address(self):
        """
        :return: IP address.
        :rtype: str
        """
        return self.__address

    @property
    def version(self):
        """
        :return: version of IP protocol: 4 or 6.
        :rtype: int(4|6)
        """
        return self.__version

    def is_in_scope(self, scope=None):
        if scope is None:
            scope = Config.audit_scope
        return self.address in scope