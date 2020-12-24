# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/fgbio/groupreadsbyumi.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 2344 bytes
""" MultiQC module to parse output from fgbio GroupReadsByUmi
"""
from __future__ import print_function
import logging
from multiqc.plots import linegraph
log = logging.getLogger(__name__)

class GroupReadsByUmiMixin:

    def parse_groupreadsbyumi(self):
        self.parse_groupreadsbyumi_log()
        if len(self.fgbio_umi_data) > 0:
            self.parse_groupreadsbyumi_plot()
        return len(self.fgbio_umi_data)

    def parse_groupreadsbyumi_log(self):
        umi_data = dict()
        for f in self.find_log_files('fgbio/groupreadsbyumi'):
            self.add_data_source(f)
            family_size = []
            for line in f['f'].splitlines():
                if not line.startswith('family_size'):
                    family_size.append(tuple(line.split('\t')))

            umi_data[f['s_name']] = {int(s):int(d[1]) for s, d in enumerate(family_size, 1)}

        self.fgbio_umi_data = self.ignore_samples(umi_data)

    def parse_groupreadsbyumi_plot(self):
        config = {'id':'fgbio-groupreadsbyumi-plot', 
         'title':'fgbio: Family size count', 
         'ylab':'# UMIs', 
         'xlab':'Reads supporting UMI', 
         'xmax':15, 
         'xDecimals':False}
        self.add_section(name='GroupReadsByUmi statistics',
          anchor='fgbio-groupreadsbyumi',
          description='During GroupReadsByUmi processing family size count data is generated,\n                             showing number of UMIs represented by a certain number of reads.',
          helptext="\n            This tool groups reads together that appear to have come from the same original molecule.\n            Reads are grouped by template, and then templates are sorted by the 5' mapping positions\n            of the reads from the template, used from earliest mapping position to latest.\n            Reads that have the same end positions are then sub-grouped by UMI sequence.\n\n            The histogram shows tag family size counts.\n            ",
          plot=(linegraph.plot(self.fgbio_umi_data, config)))