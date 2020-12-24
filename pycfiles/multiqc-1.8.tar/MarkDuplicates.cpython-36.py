# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/picard/MarkDuplicates.py
# Compiled at: 2019-11-15 07:44:09
# Size of source mod 2**32: 5573 bytes
""" MultiQC submodule to parse output from Picard MarkDuplicates """
from collections import OrderedDict
import logging, os, re
from multiqc.plots import bargraph
log = logging.getLogger(__name__)

def parse_reports(self, log_key='picard/markdups', section_name='Mark Duplicates', section_anchor='picard-markduplicates', plot_title='Picard: Deduplication Stats', plot_id='picard_deduplication', data_filename='multiqc_picard_dups'):
    """ Find Picard MarkDuplicates reports and parse their dataself.
    This function is also used by the biobambam2 module, hence the parameters.
    """
    self.picard_dupMetrics_data = dict()
    for f in self.find_log_files(log_key, filehandles=True):
        s_name = f['s_name']
        for l in f['f']:
            if 'markduplicates' in l.lower() and 'input' in l.lower():
                s_name = None
                fn_search = re.search('INPUT(?:=|\\s+)(\\[?[^\\s]+\\]?)', l, flags=(re.IGNORECASE))
                if fn_search:
                    s_name = os.path.basename(fn_search.group(1).strip('[]'))
                    s_name = self.clean_s_name(s_name, f['root'])
                if s_name is not None:
                    if 'UNPAIRED_READ_DUPLICATES' in l:
                        if s_name in self.picard_dupMetrics_data:
                            log.debug('Duplicate sample name found in {}! Overwriting: {}'.format(f['fn'], s_name))
                        self.add_data_source(f, s_name, section='DuplicationMetrics')
                        self.picard_dupMetrics_data[s_name] = dict()
                        keys = l.rstrip('\n').split('\t')
                        vals = f['f'].readline().rstrip('\n').split('\t')
                        for i, k in enumerate(keys):
                            try:
                                self.picard_dupMetrics_data[s_name][k] = float(vals[i])
                            except ValueError:
                                self.picard_dupMetrics_data[s_name][k] = vals[i]

                        if self.picard_dupMetrics_data[s_name].get('READ_PAIRS_EXAMINED', 0) == 0:
                            if self.picard_dupMetrics_data[s_name].get('UNPAIRED_READS_EXAMINED', 0) == 0:
                                self.picard_dupMetrics_data.pop(s_name, None)
                                log.warn("Skipping MarkDuplicates sample '{}' as log contained no reads".format(s_name))
                    s_name = None

        for s_name in list(self.picard_dupMetrics_data.keys()):
            if len(self.picard_dupMetrics_data[s_name]) == 0:
                self.picard_dupMetrics_data.pop(s_name, None)
                log.debug('Removing {} as no data parsed'.format(s_name))

    self.picard_dupMetrics_data = self.ignore_samples(self.picard_dupMetrics_data)
    if len(self.picard_dupMetrics_data) > 0:
        self.write_data_file(self.picard_dupMetrics_data, data_filename)
        self.general_stats_headers['PERCENT_DUPLICATION'] = {'title':'% Dups', 
         'description':'{} - Percent Duplication'.format(section_name), 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'OrRd', 
         'modify':lambda x: self.multiply_hundred(x)}
        for s_name in self.picard_dupMetrics_data:
            if s_name not in self.general_stats_data:
                self.general_stats_data[s_name] = dict()
            self.general_stats_data[s_name].update(self.picard_dupMetrics_data[s_name])

        for sn in self.picard_dupMetrics_data.keys():
            self.picard_dupMetrics_data[sn]['UNPAIRED_READ_UNIQUE'] = self.picard_dupMetrics_data[sn]['UNPAIRED_READS_EXAMINED'] - self.picard_dupMetrics_data[sn]['UNPAIRED_READ_DUPLICATES']
            self.picard_dupMetrics_data[sn]['READ_PAIR_NOT_OPTICAL_DUPLICATES'] = self.picard_dupMetrics_data[sn]['READ_PAIR_DUPLICATES'] - self.picard_dupMetrics_data[sn]['READ_PAIR_OPTICAL_DUPLICATES']
            self.picard_dupMetrics_data[sn]['READ_PAIR_UNIQUE'] = self.picard_dupMetrics_data[sn]['READ_PAIRS_EXAMINED'] - self.picard_dupMetrics_data[sn]['READ_PAIR_DUPLICATES']

        keys = OrderedDict()
        keys_r = ['READ_PAIR_UNIQUE', 'UNPAIRED_READ_UNIQUE', 'READ_PAIR_NOT_OPTICAL_DUPLICATES',
         'READ_PAIR_OPTICAL_DUPLICATES', 'UNPAIRED_READ_DUPLICATES', 'UNMAPPED_READS']
        for k in keys_r:
            keys[k] = {'name': k.replace('_', ' ').title()}

        pconfig = {'id':plot_id, 
         'title':plot_title, 
         'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads', 
         'cpswitch_c_active':False}
        self.add_section(name=section_name,
          anchor=section_anchor,
          plot=(bargraph.plot(self.picard_dupMetrics_data, keys, pconfig)))
    return len(self.picard_dupMetrics_data)