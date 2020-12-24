# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/time_resolved_carbon_factors.py
# Compiled at: 2019-07-11 13:52:01
# Size of source mod 2**32: 3459 bytes
import os, csv
from pyehub.outputter import pretty_print
from pyehub.energy_hub.ehub_model import EHubModel
from pyehub.energy_hub.utils import constraint, constraint_list
from pprint import pprint as pp
with open('hourly_GHG_emission.csv') as (csvfile):
    readCSV = csv.reader(csvfile, delimiter=',')
    count = 0
    gen_list = []
    date_list = []
    carbon_factors = {}
    for row in readCSV:
        length = len(row)
        for column in range(length):
            if count == 0:
                if column != 0:
                    gen_list.append(row[column])
            elif column == 0:
                date_list.append(row[column])
                carbon_factors[row[column]] = {}
                for key in gen_list:
                    carbon_factors[row[column]][key] = {}

            else:
                carbon_factors[date_list[(count - 1)]][gen_list[(column - 1)]] = row[column]

        count += 1

carbon_factors.pop('kind')
pp(carbon_factors)

class TimeResolvedCarbon(EHubModel):
    """TimeResolvedCarbon"""

    @constraint()
    def calc_total_carbon(self):
        """A constraint for calculating the total carbon produced."""
        total_carbon_credits = 0
        for stream in self.export_streams:
            if self.CARBON_CREDITS[stream] in self.TIME_SERIES:
                for t in self.time:
                    carbon_credit = self.TIME_SERIES[self.CARBON_CREDITS[stream]][t]
                    energy_exported = self.energy_exported[t][stream]
                    total_carbon_credits += carbon_credit * energy_exported

            else:
                total_energy_exported = sum((self.energy_exported[t][stream] for t in self.time))
                carbon_credit = self.CARBON_CREDITS[stream]
                total_carbon_credits += carbon_credit * total_energy_exported

        total_carbon_emissions = 0
        for stream in self.import_streams:
            if self.CARBON_FACTORS[stream] in self.TIME_SERIES:
                for t in self.time:
                    carbon_factor = self.TIME_SERIES[self.CARBON_FACTORS[stream]][t]
                    energy_used = self.energy_imported[t][stream]
                    total_carbon_emissions += carbon_factor * energy_used

            else:
                total_energy_used = sum((self.energy_imported[t][stream] for t in self.time))
                carbon_factor = self.CARBON_FACTORS[stream]
                total_carbon_emissions += carbon_factor * total_energy_used

        return self.total_carbon == total_carbon_emissions - total_carbon_credits