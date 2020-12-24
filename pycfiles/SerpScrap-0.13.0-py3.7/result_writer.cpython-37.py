# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\scrapcore\result_writer.py
# Compiled at: 2017-08-18 10:54:52
# Size of source mod 2**32: 2637 bytes
"""Stores SERP results in the appropriate output format."""
import pprint, sys
from scrapcore.database import Link, SERP
from scrapcore.tools import CsvStreamWriter, JsonStreamWriter

class ResultWriter:
    output_format = 'stdout'
    outfile = sys.stdout

    def init_outfile(self, config, force_reload=False):
        if not self.outfile or force_reload:
            output_file = config.get('output_filename', '')
            if output_file is None:
                self.output_format = None
        elif output_file.endswith('.json'):
            self.output_format = 'json'
        else:
            if output_file.endswith('.csv'):
                self.output_format = 'csv'
            else:
                if output_file is 'stdout':
                    self.output_format = 'stdout'
                elif self.output_format == 'json':
                    self.outfile = JsonStreamWriter(output_file)
                else:
                    if self.output_format == 'csv':
                        csv_fieldnames = sorted(set(Link.__table__.columns._data.keys() + SERP.__table__.columns._data.keys()) - {'id', 'serp_id'})
                        self.outfile = CsvStreamWriter(output_file, csv_fieldnames)
                    else:
                        if self.output_format == 'stdout':
                            self.outfile = sys.stdout
                        else:
                            self.outfile = None

    def store_serp_result(self, serp, config):
        """Store the parsed SERP page.
        When called from SearchEngineScrape, then
        a parser object is passed.
        When called from caching, a list of serp object are given.
        """
        if self.outfile:
            data = self.row2dict(serp)
            data['results'] = []
            for link in serp.links:
                data['results'].append(self.row2dict(link))

            if self.output_format == 'json':
                self.outfile.write(data)
            else:
                if self.output_format == 'csv':
                    serp = self.row2dict(serp)
                    self.outfile.write(data, serp)
                else:
                    if self.output_format == 'stdout':
                        if config.get('print_results') == 'summarize':
                            print(serp)
                        else:
                            if config.get('print_results') == 'all':
                                pprint.pprint(data)

    def row2dict(self, obj):
        """Convert sql alchemy object to dictionary."""
        d = {}
        for column in obj.__table__.columns:
            d[column.name] = str(getattr(obj, column.name))

        return d

    def close_outfile(self):
        """Closes the outfile."""
        if self.output_format in ('json', 'csv'):
            self.outfile.end()