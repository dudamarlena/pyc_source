# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/report/odt.py
# Compiled at: 2013-12-22 12:03:03
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'ODTReport']
from golismero.api.external import tempfile
from golismero.api.logger import Logger
from golismero.api.plugin import import_plugin
rstext = import_plugin('rst.py')
from warnings import catch_warnings

class ODTReport(rstext.RSTReport):
    """
    Creates reports in OpenOffice document format (.odt).
    """
    EXTENSION = '.odt'

    def generate_report(self, output_file):
        Logger.log_verbose('Writing OpenOffice report to file: %s' % output_file)
        with catch_warnings(record=True):
            from docutils.core import publish_file
            from docutils.writers.odf_odt import Writer, Reader
        with tempfile(suffix='.rst') as (filename):
            Logger.log_more_verbose('Writing temporary file in rST format...')
            with open(filename, 'w') as (source):
                self.write_report_to_open_file(source)
            Logger.log_more_verbose('Converting to OpenOffice format...')
            with open(filename, 'rU') as (source):
                writer = Writer()
                reader = Reader()
                with catch_warnings(record=True):
                    with open(output_file, 'wb') as (destination):
                        publish_file(source=source, destination=destination, destination_path=output_file, reader=reader, writer=writer)