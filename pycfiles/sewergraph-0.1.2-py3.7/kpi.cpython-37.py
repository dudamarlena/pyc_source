# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sewergraph\kpi.py
# Compiled at: 2018-06-26 13:49:43
# Size of source mod 2**32: 3895 bytes
"""
Key performance indicators for sewer sheds
"""
import pandas as pd
from .helpers import subset

class SewerShedKPI(object):

    def __init__(self, net):
        """
        calculate shed-wide KPIs given a SewerGraph object
        """
        nodes = net.nodes()
        self.shed_area_ac = nodes.local_area.sum() / 43560.0
        self.tc_min = nodes.tc.max()
        self.weighted_avg_c = [
         (nodes.runoff_coefficient * nodes.local_area).sum() / nodes.local_area.sum()]
        df = net.conduits()
        self.peakQ = df.peakQ.max()
        branches = df.loc[(df.PIPE_TYPE == 'BRANCH')]
        trunks = df.loc[(df.PIPE_TYPE == 'TRUNK')]
        other = df.loc[((df.PIPE_TYPE != 'BRANCH') & (df.PIPE_TYPE != 'TRUNK'))]
        hydr_dict = dict(all_sewers=dict(total_mi=(df.Shape_Leng.sum() / 5280),
          oversized_mi=(subset(df, 0, 0.5) / 5280),
          efficient_mi=(subset(df, 0.5, 1.0) / 5280),
          moderate_mi=(subset(df, 1.0, 2.0) / 5280),
          severe_mi=(subset(df, 2.0) / 5280),
          cap_frac_mean=(df.capacity_fraction.mean())),
          trunks=dict(total_mi=(trunks.Shape_Leng.sum() / 5280),
          oversized_mi=(subset(trunks, 0, 0.5) / 5280),
          efficient_mi=(subset(trunks, 0.5, 1.0) / 5280),
          moderate_mi=(subset(trunks, 1.0, 2.0) / 5280),
          severe_mi=(subset(trunks, 2.0) / 5280),
          cap_frac_mean=(trunks.capacity_fraction.mean())),
          branches=dict(total_mi=(branches.Shape_Leng.sum() / 5280),
          oversized_mi=(subset(branches, 0, 0.5) / 5280),
          efficient_mi=(subset(branches, 0.5, 1.0) / 5280),
          moderate_mi=(subset(branches, 1.0, 2.0) / 5280),
          severe_mi=(subset(branches, 2.0) / 5280),
          cap_frac_mean=(branches.capacity_fraction.mean())),
          other=dict(total_mi=(other.Shape_Leng.sum() / 5280),
          oversized_mi=(subset(other, 0, 0.5) / 5280),
          efficient_mi=(subset(other, 0.5, 1.0) / 5280),
          moderate_mi=(subset(other, 1.0, 2.0) / 5280),
          severe_mi=(subset(other, 2.0) / 5280),
          cap_frac_mean=(other.capacity_fraction.mean())))
        index = [
         'total_mi', 'oversized_mi', 'efficient_mi', 'moderate_mi',
         'severe_mi', 'cap_frac_mean']
        cols = ['all_sewers', 'branches', 'trunks', 'other']
        self.sewers = pd.DataFrame(hydr_dict, index=index, columns=cols)
        self.drainage_density = df.Shape_Leng.sum() / nodes.local_area.sum() * 5280
        self.capacity_deficit = net.estimate_sewer_replacement_costs()
        self.deficit_per_acre = self.capacity_deficit / self.shed_area_ac

    def __str__(self):
        s = []
        s.append('Total Shed Area: {} ac'.format(round(self.shed_area_ac, 1)))
        s.append('Time of Concentration: {} min'.format(round(self.tc_min, 1)))
        s.append('Peak Q: {} cfs'.format(round(self.peakQ, 1)))
        s.append('Total Sewer Miles: {}mi'.format(round(self.sewers.all_sewers.total_mi, 1)))
        s.append('Drainage Density: {} mi/sqmi'.format(round(self.drainage_density, 1)))
        s.append('Capacity Deficit: ${}M'.format(round(self.capacity_deficit, 1)))
        s.append('DPA: ${}M/ac'.format(round(self.deficit_per_acre, 3)))
        return '\n'.join(s)