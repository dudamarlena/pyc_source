# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/clipandmerge/clipandmerge.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 4410 bytes
""" MultiQC module to parse output from ClipAndMerge """
from __future__ import print_function
from collections import OrderedDict
import logging, os, re
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' ClipAndMerge module '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='ClipAndMerge', anchor='clipandmerge', href='http://www.github.com/apeltzer/ClipAndMerge',
          info='is a tool for adapter clipping and read merging for ancient DNA data.')
        self.clipandmerge_data = dict()
        for f in self.find_log_files('clipandmerge'):
            self.parse_clipandmerge_log(f)

        self.clipandmerge_data = self.ignore_samples(self.clipandmerge_data)
        if len(self.clipandmerge_data) == 0:
            raise UserWarning
        log.info('Found {} reports'.format(len(self.clipandmerge_data)))
        self.write_data_file(self.clipandmerge_data, 'multiqc_clipandmerge')
        self.clipandmerge_general_stats_table()
        self.add_section(plot=(self.clipandmerge_alignment_plot()))

    def parse_clipandmerge_log(self, f):
        regexes = {'usable_reads':'Number of usable reads in the output file\\(s\\):\\s+(\\d+)', 
         'merged_reads':'Number of usable merged reads:\\s+(\\d+)', 
         'percentage':'Percentage of usable merged reads:\\s+(\\d+\\.\\d+)', 
         'usable_not_merged_forward':'Number of usable not merged forward reads:\\s+(\\d+)', 
         'usable_not_merged_reverse':'Number of usable not merged reverse reads:\\s+(\\d+)', 
         'usable_forward_no_pairing_reverse':'Number of usable forward reads with no pairing reverse read:\\s+(\\d+)', 
         'usable_reverse_no_pairing_forward':'Number of usable reverse reads with no pairing forward read:\\s+(\\d+)', 
         'identifier':'SampleID:\\s+(\\S+)'}
        parsed_data = dict()
        for k, r in regexes.items():
            r_search = re.search(r, f['f'], re.MULTILINE)
            if r_search:
                try:
                    parsed_data[k] = float(r_search.group(1))
                except ValueError:
                    parsed_data[k] = r_search.group(1)

        if len(parsed_data) > 0:
            s_name = self.clean_s_name(os.path.basename(f['root']), f['root'])
            if 'identifier' in parsed_data:
                s_name = self.clean_s_name(parsed_data['identifier'], f['root'])
            self.clipandmerge_data[s_name] = parsed_data

    def clipandmerge_general_stats_table(self):
        """ Take the parsed stats from the ClipAndMerge report and add it to the
        basic stats table at the top of the report """
        headers = OrderedDict()
        headers['percentage'] = {'title':'% Merged', 
         'description':'Percentage of reads merged', 
         'min':0, 
         'max':100, 
         'suffix':'%', 
         'scale':'Greens', 
         'format':'{:,.2f}'}
        self.general_stats_addcols(self.clipandmerge_data, headers)

    def clipandmerge_alignment_plot(self):
        """ Make the HighCharts HTML to plot the duplication rates """
        keys = OrderedDict()
        keys['merged_reads'] = {'name': 'Merged Reads'}
        keys['usable_not_merged_forward'] = {'name': 'Usable, not merged (forward)'}
        keys['usable_not_merged_reverse'] = {'name': 'Usable, not merged (reverse)'}
        keys['usable_forward_no_pairing_reverse'] = {'name': 'Usable forward-only'}
        keys['usable_reverse_no_pairing_forward'] = {'name': 'Usable reverse-only'}
        config = {'id':'clipandmerge_rates', 
         'title':'ClipAndMerge: Read merging results', 
         'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads', 
         'hide_zero_cats':False}
        return bargraph.plot(self.clipandmerge_data, keys, config)