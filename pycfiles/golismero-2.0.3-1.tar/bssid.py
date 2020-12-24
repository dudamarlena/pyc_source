# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/resource/bssid.py
# Compiled at: 2014-01-14 18:58:51
"""
Wi-Fi BSSID.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'BSSID']
from . import Resource
from .mac import MAC
from .. import merge
from ...text.text_utils import to_utf8

class BSSID(MAC):
    """
    Wi-Fi BSSID (MAC address of a wireless router).
    """
    resource_type = Resource.RESOURCE_BSSID

    def __init__(self, bssid, essid=None):
        """
        :param bssid: BSSID.
        :type bssid: str

        :param essid: (Optional) ESSID.
        :type essid: str | None
        """
        super(BSSID, self).__init__(bssid)
        self.essid = essid
        self.depth = 0

    def __repr__(self):
        return '<BSSID %s>' % self.bssid

    @property
    def display_name(self):
        return 'Wi-Fi 802.11 BSSID'

    @property
    def bssid(self):
        """
        :return: BSSID.
        :rtype: str
        """
        return self.address

    @merge
    def essid(self):
        """
        :return: ESSID.
        :rtype: str | None
        """
        return self.__essid

    @essid.setter
    def essid(self, essid):
        """
        :param essid: ESSID.
        :type essid: str
        """
        essid = to_utf8(essid)
        if not isinstance(essid, basestring):
            raise TypeError('Expected string, got %r instead' % type(essid))
        self.__essid = essid

    @property
    def discovered(self):
        return [MAC(self.bssid)]