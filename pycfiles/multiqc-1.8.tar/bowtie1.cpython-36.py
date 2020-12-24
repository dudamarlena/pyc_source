# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/bowtie1/bowtie1.py
# Compiled at: 2019-11-20 10:26:16
# Size of source mod 2**32: 5664 bytes
""" MultiQC module to parse output from Bowtie 1 """
from __future__ import print_function
from collections import OrderedDict
import logging, re
from multiqc import config
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' Bowtie 1 module, parses stderr logs. '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Bowtie 1', anchor='bowtie1', target='Bowtie 1',
          href='http://bowtie-bio.sourceforge.net/',
          info='is an ultrafast, memory-efficient short read aligner.')
        self.bowtie_data = dict()
        for f in self.find_log_files('bowtie1'):
            self.parse_bowtie_logs(f)

        self.bowtie_data = self.ignore_samples(self.bowtie_data)
        if len(self.bowtie_data) == 0:
            raise UserWarning
        log.info('Found {} reports'.format(len(self.bowtie_data)))
        self.write_data_file(self.bowtie_data, 'multiqc_bowtie1')
        self.bowtie_general_stats_table()
        self.bowtie_alignment_plot()

    def parse_bowtie_logs(self, f):
        s_name = f['s_name']
        parsed_data = {}
        regexes = {'reads_processed':'# reads processed:\\s+(\\d+)', 
         'reads_aligned':'# reads with at least one reported alignment:\\s+(\\d+)', 
         'reads_aligned_percentage':'# reads with at least one reported alignment:\\s+\\d+\\s+\\(([\\d\\.]+)%\\)', 
         'not_aligned':'# reads that failed to align:\\s+(\\d+)', 
         'not_aligned_percentage':'# reads that failed to align:\\s+\\d+\\s+\\(([\\d\\.]+)%\\)', 
         'multimapped':'# reads with alignments suppressed due to -m:\\s+(\\d+)', 
         'multimapped_percentage':'# reads with alignments suppressed due to -m:\\s+\\d+\\s+\\(([\\d\\.]+)%\\)'}
        for l in f['f'].splitlines():
            if 'bowtie' in l:
                if 'q.gz' in l:
                    fqmatch = re.search('([^\\s,]+\\.f(ast)?q.gz)', l)
                    if fqmatch:
                        s_name = self.clean_s_name(fqmatch.group(1), f['root'])
                        log.debug("Found a bowtie command, updating sample name to '{}'".format(s_name))
            if 'Overall time:' in l:
                if len(parsed_data) > 0:
                    if s_name in self.bowtie_data:
                        log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
                    self.add_data_source(f, s_name)
                    self.bowtie_data[s_name] = parsed_data
                s_name = f['s_name']
                parsed_data = {}
            for k, r in regexes.items():
                match = re.search(r, l)
                if match:
                    parsed_data[k] = float(match.group(1).replace(',', ''))

        if len(parsed_data) > 0:
            if s_name in self.bowtie_data:
                log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
            self.add_data_source(f, s_name)
            self.bowtie_data[s_name] = parsed_data

    def bowtie_general_stats_table(self):
        """ Take the parsed stats from the Bowtie report and add it to the
        basic stats table at the top of the report """
        headers = OrderedDict()
        headers['reads_aligned_percentage'] = {'title':'% Aligned', 
         'description':'% reads with at least one reported alignment', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'YlGn'}
        headers['reads_aligned'] = {'title':'{} Aligned'.format(config.read_count_prefix), 
         'description':'reads with at least one reported alignment ({})'.format(config.read_count_desc), 
         'min':0, 
         'scale':'PuRd', 
         'modify':lambda x: x * config.read_count_multiplier, 
         'shared_key':'read_count'}
        self.general_stats_addcols(self.bowtie_data, headers)

    def bowtie_alignment_plot(self):
        """ Make the HighCharts HTML to plot the alignment rates """
        keys = OrderedDict()
        keys['reads_aligned'] = {'color':'#8bbc21',  'name':'Aligned'}
        keys['multimapped'] = {'color':'#2f7ed8',  'name':'Multimapped'}
        keys['not_aligned'] = {'color':'#0d233a',  'name':'Not aligned'}
        config = {'id':'bowtie1_alignment', 
         'title':'Bowtie 1: Alignment Scores', 
         'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads'}
        self.add_section(description='This plot shows the number of reads aligning to the reference in different ways.',
          helptext='\n            There are 3 possible types of alignment:\n            * **Aligned**: Read has only one occurence in the reference genome.\n            * **Multimapped**: Read has multiple occurence.\n            * **Not aligned**: Read has no occurence.\n            ',
          plot=(bargraph.plot(self.bowtie_data, keys, config)))