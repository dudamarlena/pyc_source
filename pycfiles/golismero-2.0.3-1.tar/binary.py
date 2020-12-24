# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/information/binary.py
# Compiled at: 2014-01-07 11:03:17
"""
Binary data.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'Binary']
from . import File
from .. import identity

class Binary(File):
    """
    Binary data.
    """
    information_type = File.INFORMATION_BINARY

    def __init__(self, data, content_type='application/octet-stream'):
        """
        :param data: Raw bytes.
        :type data: str

        :param content_type: MIME type.
        :type content_type: str
        """
        if type(data) is not str:
            raise TypeError('Expected string, got %r instead' % type(data))
        if type(content_type) is not str:
            raise TypeError('Expected string, got %r instead' % type(content_type))
        if '/' not in content_type:
            raise ValueError('Invalid MIME type: %r' % content_type)
        if ';' in content_type and content_type.find(';') < content_type.find('/'):
            raise ValueError('Invalid MIME type: %r' % content_type)
        self.__raw_data = data
        self.__content_type = content_type
        super(Binary, self).__init__()

    @property
    def display_name(self):
        return 'Binary Data'

    @identity
    def raw_data(self):
        """
        :returns: Raw bytes.
        :rtype: str
        """
        return self.__raw_data

    @identity
    def content_type(self):
        """
        :returns: MIME type.
        :rtype: str
        """
        return self.__content_type

    @property
    def mime_type(self):
        """
        :returns: First component of the MIME type.
        :rtype: str
        """
        content_type = self.content_type
        content_type = content_type[:content_type.find('/')]
        content_type = content_type.lower()
        return content_type

    @property
    def mime_subtype(self):
        """
        :returns: Second component of the MIME type.
        :rtype: str
        """
        content_type = self.content_type
        content_type = content_type[content_type.find('/') + 1:]
        if ';' in content_type:
            content_type = content_type[:content_type.find(';')]
        content_type = content_type.lower()
        return content_type