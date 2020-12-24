# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/samtools/samtools.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 2263 bytes
""" MultiQC module to parse output from Samtools """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from .stats import StatsReportMixin
from .flagstat import FlagstatReportMixin
from .idxstats import IdxstatsReportMixin
from .rmdup import RmdupReportMixin
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule, StatsReportMixin, FlagstatReportMixin, IdxstatsReportMixin, RmdupReportMixin):
    __doc__ = ' Samtools has a number of different commands and outputs.\n    This MultiQC module supports some but not all. The code for\n    each script is split into its own file and adds a section to\n    the module output if logs are found. '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Samtools',
          anchor='Samtools',
          target='Samtools',
          href='http://www.htslib.org',
          info=' is a suite of programs for interacting with high-throughput sequencing data.')
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        n = dict()
        n['stats'] = self.parse_samtools_stats()
        if n['stats'] > 0:
            log.info('Found {} stats reports'.format(n['stats']))
        n['flagstat'] = self.parse_samtools_flagstats()
        if n['flagstat'] > 0:
            log.info('Found {} flagstat reports'.format(n['flagstat']))
        n['idxstats'] = self.parse_samtools_idxstats()
        if n['idxstats'] > 0:
            log.info('Found {} idxstats reports'.format(n['idxstats']))
        n['rmdup'] = self.parse_samtools_rmdup()
        if n['rmdup'] > 0:
            log.info('Found {} rmdup reports'.format(n['rmdup']))
        if sum(n.values()) == 0:
            raise UserWarning
        self.general_stats_addcols(self.general_stats_data, self.general_stats_headers)