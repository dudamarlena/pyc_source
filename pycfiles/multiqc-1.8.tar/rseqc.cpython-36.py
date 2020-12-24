# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/rseqc/rseqc.py
# Compiled at: 2019-11-20 10:26:16
# Size of source mod 2**32: 2394 bytes
""" MultiQC module to parse output from RSeQC """
from collections import OrderedDict
import logging
from multiqc import config
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' RSeQC is a collection of scripts. This MultiQC module\n    supports some but not all. The code for each script is split\n    into its own file and adds a section to the module ooutput if\n    logs are found.'

    def __init__(self):
        super(MultiqcModule, self).__init__(name='RSeQC', anchor='rseqc', href='http://rseqc.sourceforge.net/',
          info='package provides a number of useful modules that can comprehensively evaluate high throughput RNA-seq data.')
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        n = dict()
        rseqc_sections = getattr(config, 'rseqc_sections', [])
        if len(rseqc_sections) == 0:
            rseqc_sections = ['read_distribution',
             'gene_body_coverage',
             'inner_distance',
             'read_gc',
             'read_duplication',
             'junction_annotation',
             'junction_saturation',
             'infer_experiment',
             'bam_stat']
        for sm in rseqc_sections:
            try:
                module = __import__(('multiqc.modules.rseqc.{}'.format(sm)), fromlist=[''])
                n[sm] = getattr(module, 'parse_reports')(self)
                if n[sm] > 0:
                    log.info('Found {} {} reports'.format(n[sm], sm))
            except (ImportError, AttributeError):
                log.warn("Could not find RSeQC Section '{}'".format(sm))

        if sum(n.values()) == 0:
            raise UserWarning
        self.general_stats_addcols(self.general_stats_data, self.general_stats_headers)