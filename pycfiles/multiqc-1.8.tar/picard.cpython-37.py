# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/picard/picard.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 4487 bytes
""" MultiQC module to parse output from Picard """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from . import AlignmentSummaryMetrics
from . import BaseDistributionByCycleMetrics
from . import GcBiasMetrics
from . import HsMetrics
from . import InsertSizeMetrics
from . import MarkDuplicates
from . import OxoGMetrics
from . import RnaSeqMetrics
from . import RrbsSummaryMetrics
from . import TargetedPcrMetrics
from . import VariantCallingMetrics
from . import ValidateSamFile
from . import WgsMetrics
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' Picard is a collection of scripts. This MultiQC module\n    supports some but not all. The code for each script is split\n    into its own file and adds a section to the module output if\n    logs are found.'

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Picard', anchor='picard', href='http://broadinstitute.github.io/picard/',
          info='is a set of Java command line tools for manipulating high-throughput sequencing data.')
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        n = dict()
        n['AlignmentMetrics'] = AlignmentSummaryMetrics.parse_reports(self)
        if n['AlignmentMetrics'] > 0:
            log.info('Found {} AlignmentSummaryMetrics reports'.format(n['AlignmentMetrics']))
        n['BaseDistributionByCycleMetrics'] = BaseDistributionByCycleMetrics.parse_reports(self)
        if n['BaseDistributionByCycleMetrics'] > 0:
            log.info('Found {} BaseDistributionByCycleMetrics reports'.format(n['BaseDistributionByCycleMetrics']))
        n['GcBiasMetrics'] = GcBiasMetrics.parse_reports(self)
        if n['GcBiasMetrics'] > 0:
            log.info('Found {} GcBiasMetrics reports'.format(n['GcBiasMetrics']))
        n['HsMetrics'] = HsMetrics.parse_reports(self)
        if n['HsMetrics'] > 0:
            log.info('Found {} HsMetrics reports'.format(n['HsMetrics']))
        n['InsertSizeMetrics'] = InsertSizeMetrics.parse_reports(self)
        if n['InsertSizeMetrics'] > 0:
            log.info('Found {} InsertSizeMetrics reports'.format(n['InsertSizeMetrics']))
        n['MarkDuplicates'] = MarkDuplicates.parse_reports(self)
        if n['MarkDuplicates'] > 0:
            log.info('Found {} MarkDuplicates reports'.format(n['MarkDuplicates']))
        n['OxoGMetrics'] = OxoGMetrics.parse_reports(self)
        if n['OxoGMetrics'] > 0:
            log.info('Found {} OxoGMetrics reports'.format(n['OxoGMetrics']))
        n['RnaSeqMetrics'] = RnaSeqMetrics.parse_reports(self)
        if n['RnaSeqMetrics'] > 0:
            log.info('Found {} RnaSeqMetrics reports'.format(n['RnaSeqMetrics']))
        n['RrbsSummaryMetrics'] = RrbsSummaryMetrics.parse_reports(self)
        if n['RrbsSummaryMetrics'] > 0:
            log.info('Found {} RrbsSummaryMetrics reports'.format(n['RrbsSummaryMetrics']))
        n['TargetedPcrMetrics'] = TargetedPcrMetrics.parse_reports(self)
        if n['TargetedPcrMetrics'] > 0:
            log.info('Found {} TargetedPcrMetrics reports'.format(n['TargetedPcrMetrics']))
        n['VariantCallingMetrics'] = VariantCallingMetrics.parse_reports(self)
        if n['VariantCallingMetrics'] > 0:
            log.info('Found {} VariantCallingMetrics reports'.format(n['VariantCallingMetrics']))
        n['ValidateSamFile'] = ValidateSamFile.parse_reports(self)
        if n['ValidateSamFile'] > 0:
            log.info('Found {} ValidateSamFile reports'.format(n['ValidateSamFile']))
        n['WgsMetrics'] = WgsMetrics.parse_reports(self)
        if n['WgsMetrics'] > 0:
            log.info('Found {} WgsMetrics reports'.format(n['WgsMetrics']))
        if sum(n.values()) == 0:
            raise UserWarning
        self.general_stats_addcols(self.general_stats_data, self.general_stats_headers)

    def multiply_hundred(self, val):
        try:
            val = float(val) * 100
        except ValueError:
            pass

        return val