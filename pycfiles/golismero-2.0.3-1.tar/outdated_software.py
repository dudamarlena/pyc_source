# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/vulnerability/infrastructure/outdated_software.py
# Compiled at: 2014-02-05 05:51:28
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'OutdatedSoftware']
from .. import Vulnerability
from ... import identity
from ...resource import Resource

class OutdatedSoftware(Vulnerability):
    """
    Outdated Software.

    Outdated, potentially vulnerable software was found.

    Apply all missing patches or upgrade to a newer version.
    """
    DEFAULTS = Vulnerability.DEFAULTS.copy()
    DEFAULTS['level'] = 'high'
    DEFAULTS['cvss_base'] = '8.5'
    DEFAULTS['references'] = ('https://www.owasp.org/index.php/Top_10_2013-A5-Security_Misconfiguration', )

    def __init__(self, resource, cpe, **kwargs):
        """
        :param resource: Vulnerable resource.
        :type resource: Resource

        :param cpe: CPE name of the outdated software.
        :type cpe: str

        """
        if not isinstance(resource, Resource):
            raise TypeError('Expected Resource, got %r instead' % type(resource))
        if type(cpe) is not str:
            raise TypeError('Expected str, got %r instead' % type(cpe))
        if not cpe.startswith('cpe:'):
            raise ValueError('Not a CPE name: %r' % cpe)
        if cpe.startswith('cpe:/'):
            cpe_parts = cpe[5:].split(':')
            if len(cpe_parts) < 11:
                cpe_parts.extend('*' * (11 - len(cpe_parts)))
            cpe = 'cpe:2.3:' + (':').join(cpe_parts)
        self.__resource_id = resource.identity
        self.__cpe = cpe
        super(OutdatedSoftware, self).__init__(**kwargs)
        self.add_resource(resource)

    __init__.__doc__ += Vulnerability.__init__.__doc__

    @identity
    def resource_id(self):
        """
        :returns: Identity hash of the vulnerable resource.
        :rtype: str
        """
        return self.__resource_id

    @property
    def resource(self):
        """
        :returns: Vulnerable resource.
        :rtype: Resource
        """
        return self.resolve(self.resource_id)

    @identity
    def cpe(self):
        """
        :returns: CPE 2.3 name of the outdated software.
        :rtype: str
        """
        return self.__cpe