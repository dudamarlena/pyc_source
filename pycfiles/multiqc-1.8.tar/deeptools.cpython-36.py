# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/deeptools/deeptools.py
# Compiled at: 2019-11-15 09:33:01
# Size of source mod 2**32: 4703 bytes
"""MultiQC module to parse the output from deepTools"""
from collections import OrderedDict
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from .bamPEFragmentSizeTable import bamPEFragmentSizeTableMixin
from .bamPEFragmentSizeDistribution import bamPEFragmentSizeDistributionMixin
from .estimateReadFiltering import estimateReadFilteringMixin
from .plotCoverage import plotCoverageMixin
from .plotEnrichment import plotEnrichmentMixin
from .plotFingerprint import plotFingerprintMixin
from .plotProfile import plotProfileMixin
from .plotPCA import plotPCAMixin
from .plotCorrelation import plotCorrelationMixin
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule, bamPEFragmentSizeTableMixin, bamPEFragmentSizeDistributionMixin, estimateReadFilteringMixin, plotCoverageMixin, plotEnrichmentMixin, plotFingerprintMixin, plotProfileMixin, plotPCAMixin, plotCorrelationMixin):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='deepTools',
          anchor='deepTools',
          target='deepTools',
          href='http://deeptools.readthedocs.io',
          info=' is a suite of tools to process and analyze deep sequencing data.')
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        n = dict()
        n['plotCorrelation'] = self.parse_plotCorrelation()
        if n['plotCorrelation'] > 0:
            log.debug('Found {} deepTools plotCorrelation samples'.format(n['plotCorrelation']))
        n['plotPCA'] = self.parse_plotPCA()
        if n['plotPCA'] > 0:
            log.debug('Found {} deepTools plotPCA samples'.format(n['plotPCA']))
        n['plotEnrichment'] = self.parse_plotEnrichment()
        if n['plotEnrichment'] > 0:
            log.debug('Found {} deepTools plotEnrichment samples'.format(n['plotEnrichment']))
        n['plotFingerprintOutQualityMetrics'], n['plotFingerprintOutRawCounts'] = self.parse_plotFingerprint()
        if n['plotFingerprintOutQualityMetrics'] + n['plotFingerprintOutRawCounts'] > 0:
            extra = ''
            if n['plotFingerprintOutRawCounts'] == 0:
                extra = ' (you may need to increase the maximum log file size to find plotFingerprint --outRawCounts files)'
            log.debug('Found {} and {} deepTools plotFingerprint --outQualityMetrics and --outRawCounts samples, respectively{}'.format(n['plotFingerprintOutQualityMetrics'], n['plotFingerprintOutRawCounts'], extra))
        n['bamPEFragmentSizeDistribution'] = self.parse_bamPEFragmentSizeDistribution()
        if n['bamPEFragmentSizeDistribution'] > 0:
            log.debug("Found {} deepTools 'bamPEFragmentSize --outRawFragmentLengths' samples".format(n['bamPEFragmentSizeDistribution']))
        n['bamPEFragmentSize'] = self.parse_bamPEFragmentSize()
        if n['bamPEFragmentSize'] > 0:
            log.debug("Found {} deepTools 'bamPEFragmentSize --table' samples".format(n['bamPEFragmentSize']))
        n['plotProfile'] = self.parse_plotProfile()
        if n['plotProfile'] > 0:
            log.debug('Found {} deepTools plotProfile samples'.format(n['plotProfile']))
        n['plotCoverageStdout'], n['plotCoverageOutRawCounts'] = self.parse_plotCoverage()
        if n['plotCoverageStdout'] + n['plotCoverageOutRawCounts'] > 0:
            extra = ''
            if n['plotCoverageOutRawCounts'] == 0:
                extra = ' (you may need to increase the maximum log file size to find plotCoverage --outRawCounts files)'
            log.debug('Found {} and {} deepTools plotCoverage standard output and --outRawCounts samples, respectively{}'.format(n['plotCoverageStdout'], n['plotCoverageOutRawCounts'], extra))
        else:
            n['estimateReadFiltering'] = self.parse_estimateReadFiltering()
            if n['estimateReadFiltering'] > 0:
                log.debug('Found {} deepTools estimateReadFiltering samples'.format(n['estimateReadFiltering']))
            tot = sum(n.values())
            if tot > 0:
                log.info('Found {} total deepTools samples'.format(tot))
            else:
                raise UserWarning

    def _int(self, val):
        """ Avoids Python3 error:
        ValueError: invalid literal for self._int() with base 10: '1.0'
        """
        return int(round(float(val)))