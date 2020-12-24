# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/trimmomatic/trimmomatic.py
# Compiled at: 2019-11-20 10:26:16
# Size of source mod 2**32: 6212 bytes
""" MultiQC module to parse output from Trimmomatic """
from __future__ import print_function
from collections import OrderedDict
import logging, re
from multiqc import config
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Trimmomatic',
          anchor='trimmomatic',
          href='http://www.usadellab.org/cms/?page=trimmomatic',
          info='is a flexible read trimming tool for Illumina NGS data.')
        self.trimmomatic = dict()
        for f in self.find_log_files('trimmomatic', filehandles=True):
            self.parse_trimmomatic(f)

        self.trimmomatic = self.ignore_samples(self.trimmomatic)
        if len(self.trimmomatic) == 0:
            raise UserWarning
        log.info('Found {} logs'.format(len(self.trimmomatic)))
        self.write_data_file(self.trimmomatic, 'multiqc_trimmomatic')
        headers = OrderedDict()
        headers['dropped_pct'] = {'title':'% Dropped', 
         'description':'% Dropped reads', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'OrRd'}
        self.general_stats_addcols(self.trimmomatic, headers)
        self.trimmomatic_barplot()

    def parse_trimmomatic(self, f):
        s_name = None
        if getattr(config, 'trimmomatic', {}).get('s_name_filenames', False):
            s_name = f['s_name']
        for l in f['f']:
            if s_name is None:
                if 'Trimmomatic' in l:
                    if 'Started with arguments:' in l:
                        match = re.search('Trimmomatic[SP]E: Started with arguments:.+?(?=\\.fastq|\\.fq)', l)
                        if match:
                            s_name = match.group().split()[(-1)]
                            s_name = self.clean_s_name(s_name, f['root'])
                            if s_name in self.trimmomatic:
                                log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
                        else:
                            l = next(f['f'])
                            match = re.search('.+?(?=\\.fastq|\\.fq)', l)
                            if match:
                                s_name = match.group().split()[(-1)]
                                s_name = self.clean_s_name(s_name, f['root'])
                                if s_name in self.trimmomatic:
                                    log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
                if 'Input Reads' in l and s_name is not None:
                    match = re.search('Input Reads: (\\d+) Surviving: (\\d+) \\(([\\d\\.,]+)%\\) Dropped: (\\d+) \\(([\\d\\.,]+)%\\)', l)
                    if match:
                        self.trimmomatic[s_name] = dict()
                        self.trimmomatic[s_name]['input_reads'] = float(match.group(1))
                        self.trimmomatic[s_name]['surviving'] = float(match.group(2))
                        self.trimmomatic[s_name]['surviving_pct'] = float(match.group(3).replace(',', '.'))
                        self.trimmomatic[s_name]['dropped'] = float(match.group(4))
                        self.trimmomatic[s_name]['dropped_pct'] = float(match.group(5).replace(',', '.'))
                        s_name = None
                if 'Input Read Pairs' in l and s_name is not None:
                    match = re.search('Input Read Pairs: (\\d+) Both Surviving: (\\d+) \\(([\\d\\.,]+)%\\) Forward Only Surviving: (\\d+) \\(([\\d\\.,]+)%\\) Reverse Only Surviving: (\\d+) \\(([\\d\\.,]+)%\\) Dropped: (\\d+) \\(([\\d\\.,]+)%\\)', l)
                    if match:
                        self.trimmomatic[s_name] = dict()
                        self.trimmomatic[s_name]['input_read_pairs'] = float(match.group(1))
                        self.trimmomatic[s_name]['surviving'] = float(match.group(2))
                        self.trimmomatic[s_name]['surviving_pct'] = float(match.group(3).replace(',', '.'))
                        self.trimmomatic[s_name]['forward_only_surviving'] = float(match.group(4))
                        self.trimmomatic[s_name]['forward_only_surviving_pct'] = float(match.group(5).replace(',', '.'))
                        self.trimmomatic[s_name]['reverse_only_surviving'] = float(match.group(6))
                        self.trimmomatic[s_name]['reverse_only_surviving_pct'] = float(match.group(7).replace(',', '.'))
                        self.trimmomatic[s_name]['dropped'] = float(match.group(8))
                        self.trimmomatic[s_name]['dropped_pct'] = float(match.group(9).replace(',', '.'))
                        s_name = None

    def trimmomatic_barplot(self):
        """ Make the HighCharts HTML to plot the trimmomatic rates """
        keys = OrderedDict()
        keys['surviving'] = {'color':'#437bb1',  'name':'Surviving Reads'}
        keys['both_surviving'] = {'color':'#f7a35c',  'name':'Both Surviving'}
        keys['forward_only_surviving'] = {'color':'#e63491',  'name':'Forward Only Surviving'}
        keys['reverse_only_surviving'] = {'color':'#b1084c',  'name':'Reverse Only Surviving'}
        keys['dropped'] = {'color':'#7f0000',  'name':'Dropped'}
        pconfig = {'id':'trimmomatic_plot', 
         'title':'Trimmomatic: Surviving Reads', 
         'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads'}
        self.add_section(plot=(bargraph.plot(self.trimmomatic, keys, pconfig)))