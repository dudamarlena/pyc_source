# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyazure\locations.py
# Compiled at: 2012-01-28 13:15:13
"""
Python wrapper around Windows Azure storage and management APIs

Authors:
    Blair Bethwaite <blair.bethwaite@gmail.com>

License:
    GNU General Public Licence (GPL)
    
    This file is part of pyazure.
    Copyright (c) 2011 Blair Bethwaite <blair.bethwaite@gmail.com>
    
    pyazure is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyazure is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pyazure. If not, see <http://www.gnu.org/licenses/>.
"""
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