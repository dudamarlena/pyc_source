# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/mtnucratio/mtnucratio.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 3970 bytes
""" MultiQC module to parse output from mtnucratio """
from __future__ import print_function
from collections import OrderedDict
import logging, json
from multiqc import config
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' mtnucratio module '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='mtnucratio', anchor='mtnucratio', href='http://www.github.com/apeltzer/MTNucRatioCalculator',
          info='is a tool to compute mt/nuc ratios for NGS datasets.')
        self.mtnuc_data = dict()
        for f in self.find_log_files('mtnucratio', filehandles=True):
            self.parseJSON(f)

        self.mtnuc_data = self.ignore_samples(self.mtnuc_data)
        if len(self.mtnuc_data) == 0:
            raise UserWarning
        log.info('Found {} reports'.format(len(self.mtnuc_data)))
        self.write_data_file(self.mtnuc_data, 'multiqc_mtnucratio')
        self.mtnucratio_general_stats_table()

    def parseJSON(self, f):
        """ Parse the JSON output from mtnucratio and save the summary statistics """
        try:
            parsed_json = json.load(f['f'])
            if 'metrics' not in parsed_json:
                if 'metadata' not in parsed_json:
                    log.warn("No MTNUCRATIO JSON: '{}'".format(f['fn']))
                    return
        except JSONDecodeError as e:
            try:
                log.warn("Could not parse mtnucratio JSON: '{}'".format(f['fn']))
                log.debug(e)
                return
            finally:
                e = None
                del e

        s_name = self.clean_s_name(parsed_json['metadata']['sample_name'], '')
        self.add_data_source(f, s_name)
        metrics_dict = parsed_json['metrics']
        self.mtnuc_data[s_name] = metrics_dict

    def mtnucratio_general_stats_table(self):
        """ Take the parsed stats from the mtnucratio report and add it to the
        basic stats table at the top of the report """
        headers = OrderedDict()
        headers['mt_cov_avg'] = {'title':'MT genome coverage', 
         'description':'Average coverage (X) on mitochondrial genome.', 
         'min':0, 
         'scale':'OrRd', 
         'suffix':' X', 
         'hidden':True}
        headers['nuc_cov_avg'] = {'title':'Genome coverage', 
         'description':'Average coverage (X) on nuclear genome.', 
         'min':0, 
         'scale':'GnBu', 
         'suffix':' X', 
         'hidden':True}
        headers['mt_nuc_ratio'] = {'title':'% MTNUC', 
         'description':'Mitochondrial to nuclear reads ratio (MTNUC)', 
         'min':0, 
         'max':100, 
         'suffix':'%', 
         'scale':'RdYlGrn-rev'}
        headers['nucreads'] = {'title':'{} Genome reads'.format(config.read_count_prefix), 
         'description':'Reads on the nuclear genome ({})'.format(config.read_count_desc), 
         'modify':lambda x: x * config.read_count_multiplier, 
         'shared_key':'read_count', 
         'scale':'BuPu', 
         'hidden':True}
        headers['mtreads'] = {'title':'{} MT genome reads'.format(config.read_count_prefix), 
         'description':'Reads on the mitochondrial genome ({})'.format(config.read_count_desc), 
         'modify':lambda x: x * config.read_count_multiplier, 
         'shared_key':'read_count', 
         'scale':'OrRd', 
         'hidden':True}
        self.general_stats_addcols(self.mtnuc_data, headers)