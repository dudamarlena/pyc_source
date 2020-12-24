# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/conpair/conpair.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 4322 bytes
""" MultiQC module to parse output from Conpair """
from __future__ import print_function
import logging, re
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = '\n    Conpair module class.\n    '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Conpair', anchor='conpair', href='https://github.com/nygenome/Conpair',
          info='is a fast and robust method dedicated for human tumor-normal studies to perform concordance verification, as well as cross-individual contamination level estimation in whole-genome and whole-exome sequencing experiments.')
        self.conpair_data = dict()
        for f in self.find_log_files('conpair/concordance'):
            self.parse_conpair_logs(f)

        for f in self.find_log_files('conpair/contamination'):
            self.parse_conpair_logs(f)

        self.conpair_concordance_data = self.ignore_samples(self.conpair_data)
        if len(self.conpair_data) == 0:
            raise UserWarning
        log.info('Found {} reports'.format(len(self.conpair_data)))
        self.write_data_file(self.conpair_data, 'multiqc_conpair')
        self.conpair_general_stats_table()

    def parse_conpair_logs(self, f):
        """ Go through log file looking for conpair concordance or contamination output
        One parser to rule them all. """
        conpair_regexes = {'concordance_concordance':'Concordance: ([\\d\\.]+)%', 
         'concordance_used_markers':'Based on (\\d+)/\\d+ markers', 
         'concordance_total_markers':'Based on \\d+/(\\d+) markers', 
         'concordance_marker_threshold':'\\(coverage per marker threshold : (\\d+) reads\\)', 
         'concordance_min_mapping_quality':'Minimum mappinq quality: (\\d+)', 
         'concordance_min_base_quality':'Minimum base quality: (\\d+)', 
         'contamination_normal':'Normal sample contamination level: ([\\d\\.]+)%', 
         'contamination_tumor':'Tumor sample contamination level: ([\\d\\.]+)%'}
        parsed_data = {}
        for k, r in conpair_regexes.items():
            match = re.search(r, f['f'])
            if match:
                parsed_data[k] = float(match.group(1))

        def _cp_type(data):
            if 'concordance_concordance' in parsed_data:
                return 'concordance'
            if 'contamination_normal' in parsed_data:
                return 'contamination'

        if len(parsed_data) > 0:
            if f['s_name'] in self.conpair_data:
                if _cp_type(self.conpair_data[f['s_name']]) == _cp_type(parsed_data):
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(f['s_name']))
            else:
                self.conpair_data[f['s_name']] = dict()
            self.add_data_source(f, section=(_cp_type(parsed_data)))
            self.conpair_data[f['s_name']].update(parsed_data)

    def conpair_general_stats_table(self):
        """ Take the parsed stats from the Conpair report and add it to the
        basic stats table at the top of the report """
        headers = {}
        headers['concordance_concordance'] = {'title':'Concordance', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'format':'{:,.2f}', 
         'scale':'RdYlGn'}
        headers['contamination_normal'] = {'title':'N Contamination', 
         'description':'Normal sample contamination level', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'format':'{:,.3f}', 
         'scale':'RdYlBu-rev'}
        headers['contamination_tumor'] = {'title':'T Contamination', 
         'description':'Tumor sample contamination level', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'format':'{:,.3f}', 
         'scale':'RdYlBu-rev'}
        self.general_stats_addcols(self.conpair_data, headers)