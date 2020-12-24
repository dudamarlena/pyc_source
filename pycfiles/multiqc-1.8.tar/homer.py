# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/homer/homer.py
# Compiled at: 2019-11-13 05:22:42
""" MultiQC module to parse output from HOMER """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from .findpeaks import FindPeaksReportMixin
from .tagdirectory import TagDirReportMixin
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule, FindPeaksReportMixin, TagDirReportMixin):
    """ HOMER has a number of different commands and outputs.
    This MultiQC module supports some but not all. The code for
    each script is split into its own file and adds a section to
    the module output if logs are found. """

    def __init__(self):
        super(MultiqcModule, self).__init__(name='HOMER', anchor='homer', href='http://homer.ucsd.edu/homer/', info='is a suite of tools for Motif Discovery and next-gen sequencing analysis.')
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        n = dict()
        self.tagdir_data = {'GCcontent': {}, 'restriction': {}, 'restriction_norm': {}, 'length': {}, 'taginfo_total': {}, 'taginfo_total_norm': {}, 'taginfo_uniq': {}, 'taginfo_uniq_norm': {}, 'FreqDistribution': {}, 'header': {}, 'interChr': {}}
        n['findpeaks'] = self.parse_homer_findpeaks()
        if n['findpeaks'] > 0:
            log.info(('Found {} findPeaks reports').format(n['findpeaks']))
        n['Homer_tagDir'] = self.homer_tagdirectory()
        if n['Homer_tagDir'] > 0:
            log.info(('Found {} reports').format(n['Homer_tagDir']))
        if sum(n.values()) == 0:
            raise UserWarning
        self.general_stats_addcols(self.general_stats_data, self.general_stats_headers)