# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/dedup/dedup.py
# Compiled at: 2019-11-13 05:22:42
""" MultiQC module to parse output from DeDup """
from __future__ import print_function
from collections import OrderedDict
import logging, json
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    """ DeDup module """

    def __init__(self):
        super(MultiqcModule, self).__init__(name='DeDup', anchor='dedup', href='http://www.github.com/apeltzer/DeDup', info='is a tool for duplicate removal for merged/collapsed reads in ancient DNA analysis.')
        self.dedup_data = dict()
        for f in self.find_log_files('dedup', filehandles=True):
            self.parseJSON(f)

        self.dedup_data = self.ignore_samples(self.dedup_data)
        if len(self.dedup_data) == 0:
            raise UserWarning
        log.info(('Found {} reports').format(len(self.dedup_data)))
        self.write_data_file(self.dedup_data, 'multiqc_dedup')
        self.dedup_general_stats_table()
        self.add_section(description='This plot shows read categories that were either not removed (unique reads) or removed (duplicates).', plot=self.dedup_alignment_plot())

    def parseJSON(self, f):
        """ Parse the JSON output from DeDup and save the summary statistics """
        try:
            parsed_json = json.load(f['f'])
            if 'metrics' not in parsed_json or 'metadata' not in parsed_json:
                log.debug(("DeDup JSON missing essential keys - skipping sample: '{}'").format(f['fn']))
                return
        except JSONDecodeError as e:
            log.debug(("Could not parse DeDup JSON: '{}'").format(f['fn']))
            log.debug(e)
            return

        s_name = self.clean_s_name(parsed_json['metadata']['sample_name'], f['root'])
        self.add_data_source(f, s_name)
        metrics_dict = parsed_json['metrics']
        for k in metrics_dict:
            metrics_dict[k] = float(metrics_dict[k])

        metrics_dict['not_removed'] = metrics_dict['total_reads'] - metrics_dict['reverse_removed'] - metrics_dict['forward_removed'] - metrics_dict['merged_removed']
        self.dedup_data[s_name] = metrics_dict
        return

    def dedup_general_stats_table(self):
        """ Take the parsed stats from the DeDup report and add it to the
        basic stats table at the top of the report """
        headers = OrderedDict()
        headers['dup_rate'] = {'title': 'Duplication Rate', 
           'description': 'Percentage of reads categorised as a technical duplicate', 
           'min': 0, 
           'max': 100, 
           'suffix': '%', 
           'scale': 'OrRd', 
           'format': '{:,.0f}', 
           'modify': lambda x: x * 100.0}
        headers['clusterfactor'] = {'title': 'ClusterFactor', 
           'description': 'CF~1 means high library complexity. Large CF means not worth sequencing deeper.', 
           'min': 1, 
           'max': 100, 
           'scale': 'OrRd', 
           'format': '{:,.2f}'}
        self.general_stats_addcols(self.dedup_data, headers)

    def dedup_alignment_plot(self):
        """ Make the HighCharts HTML to plot the duplication rates """
        keys = OrderedDict()
        keys['not_removed'] = {'name': 'Not Removed'}
        keys['reverse_removed'] = {'name': 'Reverse Removed'}
        keys['forward_removed'] = {'name': 'Forward Removed'}
        keys['merged_removed'] = {'name': 'Merged Removed'}
        config = {'id': 'dedup_rates', 
           'title': 'DeDup: Deduplicated Reads', 
           'ylab': '# Reads', 
           'cpswitch_counts_label': 'Number of Reads', 
           'hide_zero_cats': False}
        return bargraph.plot(self.dedup_data, keys, config)