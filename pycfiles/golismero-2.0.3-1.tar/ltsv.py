# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/report/ltsv.py
# Compiled at: 2013-12-21 23:37:50
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'LTSVLogger']
from golismero.api.audit import get_audit_log_lines
from golismero.api.logger import Logger
from golismero.api.plugin import ReportPlugin
from collections import namedtuple
from time import asctime, gmtime
LogLine = namedtuple('LogLine', [
 'plugin_id', 'identity', 'text', 'level', 'is_err', 'time'])

class LTSVLogger(ReportPlugin):
    """
    Extracts only the logs, in labeled tab-separated values format.
    """
    EXTENSION = '.ltsv'

    def generate_report(self, output_file):
        Logger.log_verbose('Writing audit logs to file: %s' % output_file)
        with open(output_file, 'w') as (f):
            page_num = 0
            while True:
                lines = get_audit_log_lines(page_num=page_num, per_page=20)
                if not lines:
                    break
                page_num += 1
                for line in lines:
                    n = LogLine(*line)
                    d = n._asdict()
                    k = list(n._fields)
                    d['level'] = {0: 'INFO', 
                       1: 'LOW', 
                       2: 'MED', 
                       3: 'HIGH'}.get(d['level'], 'HIGH')
                    if d['is_err']:
                        d['level'] = 'ERR_' + d['level']
                    del d['is_err']
                    k.remove('is_err')
                    d['time'] = asctime(gmtime(d['time']))
                    d['text'] = d['text'].replace('\t', '        ')
                    if '\n' not in d['text']:
                        sub_lines = [
                         d]
                    else:
                        sub_lines = []
                        for x in d['text'].split('\n'):
                            x = x.rstrip()
                            d['text'] = x
                            sub_lines.append(d.copy())

                        for d in sub_lines:
                            l = ('\t').join('%s:%s' % (x, d[x]) for x in k) + '\n'
                            f.write(l.encode('utf-8'))

        self.launch_command(output_file)