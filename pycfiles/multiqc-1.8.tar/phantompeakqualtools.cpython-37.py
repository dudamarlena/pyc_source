# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/phantompeakqualtools/phantompeakqualtools.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 3207 bytes
""" MultiQC module to parse output from phantompeakqualtools """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='phantompeakqualtools', anchor='phantompeakqualtools', href='https://www.encodeproject.org/software/phantompeakqualtools',
          info='computes informative enrichment and quality measures for ChIP-seq/DNase-seq/FAIRE-seq/MNase-seq data.')
        self.phantompeakqualtools_data = dict()
        for f in self.find_log_files('phantompeakqualtools/out', filehandles=False):
            self.parse_phantompeakqualtools(f)

        self.phantompeakqualtools_data = self.ignore_samples(self.phantompeakqualtools_data)
        if len(self.phantompeakqualtools_data) == 0:
            raise UserWarning
        log.info('Found {} logs'.format(len(self.phantompeakqualtools_data)))
        self.write_data_file(self.phantompeakqualtools_data, 'multiqc_phantompeakqualtools')
        self.phantompeakqualtools_general_stats()

    def parse_phantompeakqualtools(self, f):
        s_name = self.clean_s_name(f['s_name'], f['root'])
        parsed_data = {}
        lines = f['f'].splitlines()
        for l in lines:
            s = l.split('\t')
            parsed_data['Estimated_Fragment_Length_bp'] = int(s[2].split(',')[0])
            parsed_data['NSC'] = float(s[8])
            parsed_data['RSC'] = float(s[9])

        if len(parsed_data) > 0:
            if s_name in self.phantompeakqualtools_data:
                log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
            self.add_data_source(f, s_name)
            self.phantompeakqualtools_data[s_name] = parsed_data

    def phantompeakqualtools_general_stats(self):
        """ Add columns to General Statistics table """
        headers = OrderedDict()
        headers['Estimated_Fragment_Length_bp'] = {'title':'Frag Length', 
         'description':'Estimated fragment length (bp)', 
         'min':0, 
         'format':'{:,.0f}'}
        headers['NSC'] = {'title':'NSC', 
         'description':'Normalized strand cross-correlation', 
         'max':10, 
         'min':0, 
         'format':'{:,.2f}', 
         'scale':'RdYlGn-rev'}
        headers['RSC'] = {'title':'RSC', 
         'description':'Relative strand cross-correlation', 
         'max':10, 
         'min':0, 
         'format':'{:,.2f}', 
         'scale':'RdYlBu-rev'}
        self.general_stats_addcols(self.phantompeakqualtools_data, headers)