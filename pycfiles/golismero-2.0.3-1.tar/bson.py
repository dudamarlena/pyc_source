# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/report/bson.py
# Compiled at: 2013-12-21 23:37:50
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'BSONOutput']
from golismero.api.logger import Logger
from golismero.api.plugin import import_plugin
json = import_plugin('json.py')
BSON = None

class BSONOutput(json.JSONOutput):
    """
    Dumps the output in BSON (Binary JSON) format.
    """
    EXTENSION = '.bson'

    def is_supported(self, output_file):
        if super(BSONOutput, self).is_supported(output_file):
            try:
                self.load_bson()
            except ImportError:
                Logger.log_error('BSON encoder not found!\nGet it from:\n    https://github.com/mongodb/mongo-python-driver\nOr alternatively from:\n    https://github.com/martinkou/bson')
                return False

            return True
        return False

    @staticmethod
    def load_bson():
        global BSON
        if BSON is None:
            try:
                from pymongo.bson import BSON
            except ImportError:
                from bson import dumps

                class BSON(object):

                    @staticmethod
                    def encode(obj, *args, **kwargs):
                        return dumps(obj)

        return

    def serialize_report(self, output_file, report_data):
        self.load_bson()
        bson_data = BSON.encode(report_data, check_keys=True)
        with open(output_file, 'wb') as (fp):
            fp.write(bson_data)

    def test_data_serialization(self, data):
        self.load_bson()
        BSON.encode(data, check_keys=True)