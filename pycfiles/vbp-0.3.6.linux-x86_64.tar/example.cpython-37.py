# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/vbp/example.py
# Compiled at: 2019-03-13 19:45:15
# Size of source mod 2**32: 1196 bytes
import vbp, enum, numpy, pandas, datetime, matplotlib

class ExampleDataSource(vbp.TimeSeriesDataSource):

    def initialize_parser(self, parser):
        super().initialize_parser(parser)
        parser.add_argument('--random-action', help='Create a random action', action='append', default=['Action1'])
        parser.add_argument('--years', help='Number of years to generate', type=int, default=100)

    def run_load(self):
        end_year = datetime.datetime.now().year
        dates = [pandas.to_datetime(i, format='%Y') for i in range(end_year - self.options.years + 1, end_year + 1) for j in range(1, len(self.options.random_action) + 1)]
        actions = [j for i in range(end_year - self.options.years + 1, end_year + 1) for j in self.options]
        values = numpy.random.random_sample(self.options.years * len(self.options.random_action)).tolist()
        df = pandas.DataFrame({self.get_action_column_name(): actions, 
         self.get_value_column_name(): values},
          index=dates)
        df.index.name = 'Date'
        return df

    def get_action_column_name(self):
        return 'Action'

    def get_value_column_name(self):
        return 'Value'