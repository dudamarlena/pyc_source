# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/vulnerability/suspicious/header.py
# Compiled at: 2014-02-05 05:49:22
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'SuspiciousHeader']
from .. import Vulnerability
from ... import identity
from ...information.http import HTTP_Response

class SuspiciousHeader(Vulnerability):
    """
    Suspicious HTTP Header.

    An HTTP header was found that may contain sensitive information.
    User attention could be required.
    """
    DEFAULTS = Vulnerability.DEFAULTS.copy()
    DEFAULTS['level'] = 'informational'
    DEFAULTS['cvss_base'] = '2.9'

    def __init__(self, response, name, value, **kwargs):
        """
        :param response: HTTP response where the suspicious header was found.
        :type response: HTTP_Response

        :param name: Name of the suspicious header.
        :type name: str

        :param value: Header value.
        :type value: str
        """
        if not isinstance(response, HTTP_Response):
            raise TypeError('Expected HTTP_Response, got %r instead' % type(response))
        if type(name) is not str:
            raise TypeError('Expected str, got %r instead' % type(name))
        if type(value) is not str:
            raise TypeError('Expected str, got %r instead' % type(value))
        self.__response_id = response.identity
        self.__name = name
        self.__value = value
        super(SuspiciousHeader, self).__init__(**kwargs)
        self.add_information(response)

    __init__.__doc__ += Vulnerability.__init__.__doc__

    @identity
    def response_id(self):
        """
        :returns: Identity hash of the HTTPResponse
            where the vulnerable cookie was found.
        :rtype: str
        """
        return self.__response_id

    @property
    def response(self):
        """
        :returns: HTTP response where the vulnerable cookie was found.
        :rtype: HTTP_Response
        """
        return self.resolve(self.response_id)

    @property
    def name(self):
        """
        :returns: Header name.
        :rtype: str
        """
        return self.__name

    @property
    def value(self):
        """
        :returns: Header value.
        :rtype: str
        """
        return self.__value