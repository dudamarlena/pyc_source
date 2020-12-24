# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/biobambam2/biobambam2.py
# Compiled at: 2019-02-06 06:32:56
""" MultiQC module to parse output from biobambam2 """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.modules.picard import MarkDuplicates
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    """ This module is super weird. The output from this tools is essentially
    identical to Picard MarkDuplicates, so we just hijack that module instead"""

    def __init__(self):
        super(MultiqcModule, self).__init__(name='biobambam2', anchor='biobambam2', href='https://github.com/gt1/biobambam2', info='provides tools for early stage alignment file processing')
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        n = dict()
        n['bamsormadup'] = MarkDuplicates.parse_reports(self, log_key='biobambam2/bamsormadup', section_name='bamsormadup', section_anchor='biobambam2-bamsormadup', plot_title='biobambam2: bamsormadup deduplication stats', plot_id='biobambam2_bamsormadup_plot', data_filename='bamsormadup_bamsormadup')
        if n['bamsormadup'] > 0:
            log.info(('Found {} bamsormadup reports').format(n['bamsormadup']))
        if sum(n.values()) == 0:
            raise UserWarning
        self.general_stats_addcols(self.general_stats_data, self.general_stats_headers)

    def multiply_hundred(self, val):
        try:
            val = float(val) * 100
        except ValueError:
            pass

        return val