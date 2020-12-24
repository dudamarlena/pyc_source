# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyazure\locations.py
# Compiled at: 2012-01-28 13:15:13
__doc__ = '\nPython wrapper around Windows Azure storage and management APIs\n\nAuthors:\n    Blair Bethwaite <blair.bethwaite@gmail.com>\n\nLicense:\n    GNU General Public Licence (GPL)\n    \n    This file is part of pyazure.\n    Copyright (c) 2011 Blair Bethwaite <blair.bethwaite@gmail.com>\n    \n    pyazure is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    pyazure is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with pyazure. If not, see <http://www.gnu.org/licenses/>.\n'
import httplib
try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree

from util import *

class Locations(ServiceManagementEndpoint):

    def __init__(self, *args, **kwargs):
        log.debug('init locations')
        self.wasm_ops = []
        super(Locations, self).__init__(*args, **kwargs)

    @property
    def base_url(self):
        return super(Locations, self).base_url + '/locations'

    def get_wasm_ops(self):
        return [
         self.list_locations]

    def list_locations(self, just_names=True):
        """The List Locations operation lists all of the data center locations
        that are valid for your subscription."""
        log.debug('Getting locations list')
        req = RequestWithMethod('GET', self.base_url)
        res = self.urlopen(req)
        log.debug('HTTP Response: %s %s', res.code, res.msg)
        if res.code != httplib.OK:
            self._raise_wa_error(res)
        ET = etree.parse(res)
        locations = ET.findall('.//{%s}Location' % NAMESPACE_MANAGEMENT)
        for location in locations:
            name = location.findtext('{%s}Name' % NAMESPACE_MANAGEMENT)
            if just_names:
                yield name
            else:
                display_name = location.findtext('{%s}DisplayName' % NAMESPACE_MANAGEMENT)
                yield {'Name': name, 'DisplayName': display_name}