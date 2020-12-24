# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/statistics_comparison.py
# Compiled at: 2019-04-23 22:11:57
# Size of source mod 2**32: 2425 bytes
from pocsuite3.lib.core.common import data_to_stdout
from pocsuite3.thirdparty.prettytable.prettytable import PrettyTable

class StatisticsComparison(object):

    def __init__(self):
        self.data = {}
        self.dork = {}

    def add_dork(self, source, dork):
        self.dork[source] = dork

    def add_ip(self, ip, source, honeypot=False):
        if ip not in self.data:
            self.data[ip] = {'source':[],  'honeypot':honeypot, 
             'success':False}
        self.data[ip]['source'].append(source)

    def getinfo(self, ip) -> tuple:
        if ip not in self.data:
            return ('Other', 'Unknown')
        sources = self.data[ip]['source']
        return (','.join(sources), str(self.data[ip]['honeypot']))

    def change_success(self, ip, success=False):
        if ip in self.data:
            self.data[ip]['success'] = success

    def _statistics(self) -> dict:
        static_data = {}
        for ip, item in self.data.items():
            engines = item['source']
            for engine in engines:
                if engine not in static_data:
                    static_data[engine] = {'total':0,  'success':0, 
                     'repetition':0}
                static_data[engine]['total'] += 1
                if item['success']:
                    static_data[engine]['success'] += 1
                if len(engines) > 1:
                    static_data[engine]['repetition'] += 1

        return static_data

    def output(self):
        results_table = PrettyTable(['Search-engine', 'Dork', 'Total-data', 'Success-rate', 'Repetition-rate'])
        results_table.align['Search-engine'] = 'c'
        results_table.padding_width = 1
        results = []
        for engine, item in self._statistics().items():
            dork = ''
            if engine in self.dork:
                dork = self.dork[engine]
            _result = [engine,
             dork,
             item['total'],
             '{0:.1f}%'.format(item['success'] / item['total'] * 100),
             '{0:.1f}%'.format(item['repetition'] / item['total'] * 100)]
            results.append(_result)

        for row in results:
            results_table.add_row(row)

        data_to_stdout('\n{0}\n'.format(results_table.get_string()))