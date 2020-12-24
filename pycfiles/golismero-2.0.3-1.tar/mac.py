# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/resource/mac.py
# Compiled at: 2014-01-14 18:58:51
"""
MAC address.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'MAC']
from . import Resource
from .. import identity
from ...text.text_utils import to_utf8
import re

class MAC(Resource):
    """
    MAC address.
    """
    resource_type = Resource.RESOURCE_MAC
    __re_mac = re.compile('[0-9A-Fa-f][0-9A-Fa-f][ \\:\\-\\.]?[0-9A-Fa-f][0-9A-Fa-f][ \\:\\-\\.]?[0-9A-Fa-f][0-9A-Fa-f][ \\:\\-\\.]?[0-9A-Fa-f][0-9A-Fa-f][ \\:\\-\\.]?[0-9A-Fa-f][0-9A-Fa-f][ \\:\\-\\.]?[0-9A-Fa-f][0-9A-Fa-f]')

    def __init__(self, address):
        """
        :param address: MAC address.
        :type address: str
        """
        address = to_utf8(address)
        if not isinstance(address, str):
            raise TypeError('Expected str, got %r instead' % type(address))
        if not self.__re_mac.match(address):
            raise ValueError('Invalid %s: %r' % (self.display_name, address))
        address = re.sub('[^0-9A-Fa-f]', '', address)
        if not len(address) == 12:
            raise ValueError('Invalid %s: %r' % (self.display_name, address))
        address = (':').join(address[i:i + 2] for i in xrange(0, len(address) - 2, 2))
        self.__address = address
        super(MAC, self).__init__()
        self.depth = 0

    @classmethod
    def search(cls, text):
        """
        Extract MAC addresses from text input.
        You can pass each one of them to the constructor of this class.

        :param text: Text to scan.
        :type text: str

        :returns: MAC addresses found.
        :rtype: list(str)
        """
        return cls.__re_mac.findall(text)

    def __str__(self):
        return self.address

    def __repr__(self):
        return '<MAC address=%r>' % self.address

    @property
    def display_name(self):
        return 'MAC Address'

    @identity
    def address(self):
        """
        :return: MAC address.
        :rtype: str
        """
        return self.__address