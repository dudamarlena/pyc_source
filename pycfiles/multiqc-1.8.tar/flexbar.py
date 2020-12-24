# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/flexbar/flexbar.py
# Compiled at: 2019-11-13 05:22:42
""" MultiQC module to parse output from Flexbar """
from __future__ import print_function
from collections import OrderedDict
import logging, re
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Flexbar', anchor='flexbar', href='https://github.com/seqan/flexbar', info='is a barcode and adapter removal tool.')
        self.flexbar_data = dict()
        for f in self.find_log_files('flexbar', filehandles=True):
            self.parse_flexbar(f)

        self.flexbar_data = self.ignore_samples(self.flexbar_data)
        if len(self.flexbar_data) == 0:
            raise UserWarning
        log.info(('Found {} logs').format(len(self.flexbar_data)))
        self.write_data_file(self.flexbar_data, 'multiqc_flexbar')
        headers = {}
        headers['removed_bases_pct'] = {'title': '% bp Trimmed', 
           'description': '% Total Base Pairs removed', 
           'max': 100, 
           'min': 0, 
           'suffix': '%', 
           'scale': 'YlOrRd'}
        self.general_stats_addcols(self.flexbar_data, headers)
        self.flexbar_barplot()

    def parse_flexbar(self, f):

        def _save_data(parsed_data):
            if len(parsed_data) > 0:
                if 'processed_bases' in parsed_data and 'remaining_bases' in parsed_data:
                    parsed_data['removed_bases'] = parsed_data['processed_bases'] - parsed_data['remaining_bases']
                    parsed_data['removed_bases_pct'] = float(parsed_data['removed_bases']) / float(parsed_data['processed_bases']) * 100.0
                if s_name in self.flexbar_data:
                    log.debug(('Duplicate sample name found! Overwriting: {}').format(s_name))
                self.flexbar_data[s_name] = parsed_data

        regexes = {'output_filename': 'Read file:\\s+(.+)$', 
           'processed_reads': 'Processed reads\\s+(\\d+)', 
           'skipped_due_to_uncalled_bases': 'skipped due to uncalled bases\\s+(\\d+)', 
           'short_prior_to_adapter_removal': 'short prior to adapter removal\\s+(\\d+)', 
           'finally_skipped_short_reads': 'finally skipped short reads\\s+(\\d+)', 
           'discarded_reads_overall': 'Discarded reads overall\\s+(\\d+)', 
           'remaining_reads': 'Remaining reads\\s+(\\d+)', 
           'processed_bases': 'Processed bases:?\\s+(\\d+)', 
           'remaining_bases': 'Remaining bases:?\\s+(\\d+)'}
        s_name = f['s_name']
        parsed_data = dict()
        for l in f['f']:
            for k, r in regexes.items():
                match = re.search(r, l)
                if match:
                    if k == 'output_filename':
                        s_name = self.clean_s_name(match.group(1), f['root'])
                    else:
                        parsed_data[k] = int(match.group(1))

            if 'Flexbar completed' in l:
                _save_data(parsed_data)
                s_name = f['s_name']
                parsed_data = dict()

        _save_data(parsed_data)

    def flexbar_barplot(self):
        """ Make the HighCharts HTML to plot the flexbar rates """
        keys = OrderedDict()
        keys['remaining_reads'] = {'color': '#437bb1', 'name': 'Remaining reads'}
        keys['skipped_due_to_uncalled_bases'] = {'color': '#e63491', 'name': 'Skipped due to uncalled bases'}
        keys['short_prior_to_adapter_removal'] = {'color': '#b1084c', 'name': 'Short prior to adapter removal'}
        keys['finally_skipped_short_reads'] = {'color': '#7f0000', 'name': 'Finally skipped short reads'}
        pconfig = {'id': 'flexbar_plot', 
           'title': 'Flexbar: Processed Reads', 
           'ylab': '# Reads', 
           'cpswitch_counts_label': 'Number of Reads', 
           'hide_zero_cats': False}
        self.add_section(plot=bargraph.plot(self.flexbar_data, keys, pconfig))