# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/recon/directory_listing.py
# Compiled at: 2014-02-02 08:23:44
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2014\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
import os, re
try:
    import cPickle as pickle
except ImportError:
    import pickle

from golismero.api.logger import Logger
from golismero.api.data.vulnerability.information_disclosure.directory_listing import DirectoryListing
from golismero.api.data.information.http import HTTP_Response
from golismero.api.plugin import TestingPlugin
base_dir = os.path.split(os.path.abspath(__file__))[0]
plugin_dir = os.path.join(base_dir, 'directory_listing_plugin')
plugin_data = os.path.join(plugin_dir, 'signatures.dat')
del base_dir

class DirectoryListingPlugin(TestingPlugin):
    """
    This plugin detect and try to discover directory listing in folders and Urls.
    """

    def get_accepted_info(self):
        return [
         HTTP_Response]

    def recv_info(self, info):
        if not isinstance(info, HTTP_Response):
            return
        response = info.data
        url = list(info.associated_resources)[0]
        try:
            signatures = pickle.load(open(plugin_data, 'rb'))
        except pickle.PickleError:
            signatures = {}

        total = float(len(signatures))
        for step, (server_name, regex) in enumerate(signatures.iteritems()):
            progress = step / total * 100
            self.update_status(progress=progress)
            if re.search(regex, response):
                vulnerability = DirectoryListing(url, server_name, title="Directory listing for server '%s'" % server_name)
                return vulnerability