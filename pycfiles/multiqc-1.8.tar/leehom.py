# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/leehom/leehom.py
# Compiled at: 2019-11-20 10:26:16
""" MultiQC module to parse output from leeHom """
from __future__ import print_function
import logging, re
from multiqc import config
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    """
    leeHom module class, parses stderr logs.
    """

    def __init__(self):
        super(MultiqcModule, self).__init__(name='leeHom', anchor='leehom', href='https://github.com/grenaud/leeHom', info='is a program for the Bayesian reconstruction of ancient DNA')
        self.leehom_data = dict()
        for f in self.find_log_files('leehom', filehandles=True):
            parsed_data = self.parse_leehom_logs(f)
            if parsed_data is not None and len(parsed_data) > 0:
                self.leehom_data[f['s_name']] = parsed_data
                self.add_data_source(f, f['s_name'])

        self.leehom_data = self.ignore_samples(self.leehom_data)
        if len(self.leehom_data) == 0:
            raise UserWarning
        log.info(('Found {} reports').format(len(self.leehom_data)))
        self.write_data_file(self.leehom_data, 'multiqc_leehom')
        self.leehom_general_stats_table()
        return

    def parse_leehom_logs(self, f):
        """ Go through log file looking for leehom output """
        regexes = {'total': 'Total reads[\\s\\:]+(\\d+)', 
           'merged_trimming': 'Merged \\(trimming\\)\\s+(\\d+)', 
           'merged_overlap': 'Merged \\(overlap\\)\\s+(\\d+)', 
           'kept': 'Kept PE/SR\\s+(\\d+)', 
           'trimmed': 'Trimmed SR\\s+(\\d+)', 
           'adapter_dimers_chimeras': 'Adapter dimers/chimeras\\s+(\\d+)', 
           'failed_key': 'Failed Key\\s+(\\d+)'}
        parsed_data = dict()
        for l in f['f']:
            for k, r in regexes.items():
                match = re.search(r, l)
                if match:
                    parsed_data[k] = int(match.group(1))

        return parsed_data

    def leehom_general_stats_table(self):
        """ Take the parsed stats from the leeHom report and add it to the
        basic stats table at the top of the report """
        headers = {}
        headers['merged_trimming'] = {'title': ('{} Merged (Trimming)').format(config.read_count_prefix), 
           'description': ('Merged clusters from trimming ({})').format(config.read_count_desc), 
           'min': 0, 
           'scale': 'PuRd', 
           'modify': lambda x: x * config.read_count_multiplier, 
           'shared_key': 'read_count'}
        headers['merged_overlap'] = {'title': ('{} Merged (Overlap)').format(config.read_count_prefix), 
           'description': ('Merged clusters from overlapping reads ({})').format(config.read_count_desc), 
           'min': 0, 
           'scale': 'PuRd', 
           'modify': lambda x: x * config.read_count_multiplier, 
           'shared_key': 'read_count'}
        self.general_stats_addcols(self.leehom_data, headers)