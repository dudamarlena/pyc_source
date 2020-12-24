# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/resource/email.py
# Compiled at: 2014-01-14 18:58:51
"""
Email address type.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'Email']
from . import Resource
from .domain import Domain
from .. import identity
from ...config import Config
from ...text.text_utils import to_utf8

class Email(Resource):
    """
    Email address.
    """
    resource_type = Resource.RESOURCE_EMAIL

    def __init__(self, address, name=None):
        """
        :param address: Email address.
        :type address: str

        :param name: Optional real life name associated with this email.
        :type name: str | None
        """
        address = to_utf8(address)
        name = to_utf8(name)
        if not isinstance(address, str):
            raise TypeError('Expected string, got %r instead', type(address))
        if name is not None and not isinstance(name, str):
            raise TypeError('Expected string, got %r instead', type(name))
        if '@' not in address or not address[0].isalnum() or not address[(-1)].isalnum():
            raise ValueError('Invalid email address: %s' % address)
        self.__address = address
        self.__name = name
        super(Email, self).__init__()
        return

    def __str__(self):
        return self.address

    def __repr__(self):
        return '<Email address=%r name=%r>' % (self.address, self.name)

    @property
    def display_name(self):
        return 'E-Mail Address'

    def is_in_scope(self, scope=None):
        if scope is None:
            scope = Config.audit_scope
        return self.hostname in scope

    @identity
    def address(self):
        """
        :return: Email address.
        :rtype: str
        """
        return self.__address

    @property
    def name(self):
        """
        :return: Real name.
        :rtype: str | None
        """
        return self.__name

    @property
    def url(self):
        """
        :return: mailto:// URL for this email address.
        :rtype: str
        """
        return 'mailto://' + self.__address

    @property
    def username(self):
        """
        :return: Username for this email address.
        :rtype: str
        """
        return self.__address.split('@', 1)[0].strip().lower()

    @property
    def hostname(self):
        """
        :return: Hostname for this email address.
        :rtype: str
        """
        return self.__address.split('@', 1)[1].strip().lower()

    @property
    def discovered(self):
        if self.is_in_scope():
            return [Domain(self.hostname)]
        return []