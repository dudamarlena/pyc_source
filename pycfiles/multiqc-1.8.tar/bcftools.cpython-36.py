# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/bcftools/bcftools.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 1611 bytes
""" MultiQC module to parse output from bcftools """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from .stats import StatsReportMixin
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule, StatsReportMixin):
    __doc__ = ' Bcftools has a number of different commands and outputs.\n    This MultiQC module supports some but not all. The code for\n    each script is split into its own file and adds a section to\n    the module output if logs are found. '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Bcftools',
          anchor='bcftools',
          target='Bcftools',
          href='https://samtools.github.io/bcftools/',
          info=' contains utilities for variant calling and manipulating VCFs and BCFs.')
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        n = dict()
        n['stats'] = self.parse_bcftools_stats()
        if n['stats'] > 0:
            log.info('Found {} stats reports'.format(n['stats']))
        if sum(n.values()) == 0:
            raise UserWarning
        self.general_stats_addcols(self.general_stats_data, self.general_stats_headers)