# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/rsem/rsem.py
# Compiled at: 2019-11-20 10:26:16
# Size of source mod 2**32: 6996 bytes
""" MultiQC module to parse output from RSEM/rsem-calculate-expression """
from __future__ import print_function
import logging
from collections import OrderedDict
from multiqc import config
from multiqc.plots import bargraph, linegraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = '\n    RSEM module class, parses .cnt file .\n    '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Rsem', anchor='rsem', href='https://deweylab.github.io/RSEM/',
          info='RSEM (RNA-Seq by Expectation-Maximization) is a software package forestimating gene and isoform expression levels from RNA-Seq data.')
        self.rsem_mapped_data = dict()
        self.rsem_multimapping_data = dict()
        for f in self.find_log_files('rsem'):
            self.parse_rsem_report(f)

        self.rsem_mapped_data = self.ignore_samples(self.rsem_mapped_data)
        if len(self.rsem_mapped_data) == 0:
            raise UserWarning
        log.info('Found {} reports'.format(len(self.rsem_mapped_data)))
        self.write_data_file(self.rsem_mapped_data, 'multiqc_rsem')
        self.rsem_stats_table()
        self.rsem_mapped_reads_plot()
        self.rsem_multimapping_plot()

    def parse_rsem_report(self, f):
        """ Parse the rsem cnt stat file.
        Description of cnt file found : https://github.com/deweylab/RSEM/blob/master/cnt_file_description.txt
        """
        data = dict()
        multimapping_hist = dict()
        in_hist = False
        for l in f['f'].splitlines():
            s = l.split()
            if len(s) > 3:
                data['Unalignable'] = int(s[0])
                data['Alignable'] = int(s[1])
                data['Filtered'] = int(s[2])
                data['Total'] = int(s[3])
                data['alignable_percent'] = float(s[1]) / float(s[3]) * 100.0
            elif len(s) == 3:
                data['Unique'] = int(s[0])
                data['Multi'] = int(s[1])
                data['Uncertain'] = int(s[2])
            elif len(s) == 2:
                if in_hist or int(s[0]) == 0:
                    in_hist = True
                    try:
                        multimapping_hist[int(s[0])] = int(s[1])
                    except ValueError:
                        pass

            else:
                break

        try:
            assert data['Unique'] + data['Multi'] == data['Alignable']
        except AssertionError:
            log.warn("Unique + Multimapping read counts != alignable reads! '{}'".format(f['fn']))
            return
        except KeyError:
            log.warn("Error parsing RSEM counts file '{}'".format(f['fn']))
            return
        else:
            if len(data) > 0:
                if f['s_name'] in self.rsem_mapped_data:
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(f['s_name']))
                self.rsem_mapped_data[f['s_name']] = data
                self.add_data_source(f)
            if len(multimapping_hist) > 0:
                self.rsem_multimapping_data[f['s_name']] = multimapping_hist

    def rsem_stats_table(self):
        """ Take the parsed stats from the rsem report and add them to the
        basic stats table at the top of the report """
        headers = OrderedDict()
        headers['alignable_percent'] = {'title':'% Alignable'.format(config.read_count_prefix), 
         'description':'% Alignable reads'.format(config.read_count_desc), 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'YlGn'}
        self.general_stats_addcols(self.rsem_mapped_data, headers)

    def rsem_mapped_reads_plot(self):
        """ Make the rsem assignment rates plot """
        keys = OrderedDict()
        keys['Unique'] = {'color':'#437bb1',  'name':'Aligned uniquely to a gene'}
        keys['Multi'] = {'color':'#e63491',  'name':'Aligned to multiple genes'}
        keys['Filtered'] = {'color':'#b1084c',  'name':'Filtered due to too many alignments'}
        keys['Unalignable'] = {'color':'#7f0000',  'name':'Unalignable reads'}
        config = {'id':'rsem_assignment_plot', 
         'title':'RSEM: Mapped reads', 
         'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads', 
         'hide_zero_cats':False}
        self.add_section(name='Mapped Reads',
          anchor='rsem_mapped_reads',
          description='A breakdown of how all reads were aligned for each sample.',
          plot=(bargraph.plot(self.rsem_mapped_data, keys, config)))

    def rsem_multimapping_plot(self):
        """ Make a line plot showing the multimapping levels """
        pconfig = {'id':'rsem_multimapping_rates', 
         'title':'RSEM: Multimapping Rates', 
         'ylab':'Counts', 
         'xlab':'Number of alignments', 
         'xDecimals':False, 
         'ymin':0, 
         'tt_label':'<b>{point.x} alignments</b>: {point.y:.0f}'}
        self.add_section(name='Multimapping rates',
          anchor='rsem_multimapping',
          description='A frequency histogram showing how many reads were aligned to `n` reference regions.',
          helptext='In an ideal world, every sequence reads would align uniquely to a single location in the\n                reference. However, due to factors such as repeititve sequences, short reads and sequencing errors,\n                reads can be align to the reference 0, 1 or more times. This plot shows the frequency of each factor\n                of multimapping. Good samples should have the majority of reads aligning once.',
          plot=(linegraph.plot(self.rsem_multimapping_data, pconfig)))