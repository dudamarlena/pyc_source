# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/qualimap/qualimap.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 2083 bytes
""" MultiQC module to parse output from QualiMap """
from __future__ import print_function
from collections import defaultdict, OrderedDict
import logging, os
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' Qualimap is really a collection of separate programs:\n    BamQC, RNASeq and Counts.. This module is split into separate\n    files to reflect this and help with code organisation. '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='QualiMap', anchor='qualimap', href='http://qualimap.bioinfo.cipf.es/',
          info='is a platform-independent application to facilitate the quality control of alignment sequencing data and its derivatives like feature counts.')
        from . import QM_BamQC
        from . import QM_RNASeq
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = defaultdict(lambda : dict())
        n = dict()
        n['BamQC'] = QM_BamQC.parse_reports(self)
        if n['BamQC'] > 0:
            log.info('Found {} BamQC reports'.format(n['BamQC']))
        n['RNASeq'] = QM_RNASeq.parse_reports(self)
        if n['RNASeq'] > 0:
            log.info('Found {} RNASeq reports'.format(n['RNASeq']))
        if sum(n.values()) == 0:
            raise UserWarning
        self.general_stats_addcols(self.general_stats_data, self.general_stats_headers)

    def get_s_name(self, f):
        s_name = os.path.basename(os.path.dirname(f['root']))
        s_name = self.clean_s_name(s_name, f['root'])
        if s_name.endswith('.qc'):
            s_name = s_name[:-3]
        return s_name