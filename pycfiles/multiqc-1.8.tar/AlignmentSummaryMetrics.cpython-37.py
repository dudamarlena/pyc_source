# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/picard/AlignmentSummaryMetrics.py
# Compiled at: 2018-02-21 12:08:13
# Size of source mod 2**32: 5284 bytes
""" MultiQC submodule to parse output from Picard AlignmentSummaryMetrics """
from collections import OrderedDict
import logging, os, re
from multiqc.plots import bargraph
log = logging.getLogger(__name__)

def parse_reports(self):
    """ Find Picard AlignmentSummaryMetrics reports and parse their data """
    self.picard_alignment_metrics = dict()
    for f in self.find_log_files('picard/alignment_metrics', filehandles=True):
        parsed_data = dict()
        s_name = None
        keys = None
        for l in f['f']:
            if 'AlignmentSummaryMetrics' in l:
                if 'INPUT' in l:
                    s_name = None
                    keys = None
                    fn_search = re.search('INPUT(?:=|\\s+)(\\[?[^\\s]+\\]?)', l, flags=(re.IGNORECASE))
                    if fn_search:
                        s_name = os.path.basename(fn_search.group(1).strip('[]'))
                        s_name = self.clean_s_name(s_name, f['root'])
                        parsed_data[s_name] = dict()
                elif s_name is not None:
                    if 'AlignmentSummaryMetrics' in l:
                        if '## METRICS CLASS' in l:
                            keys = f['f'].readline().strip('\n').split('\t')
                if keys:
                    vals = l.strip('\n').split('\t')
                    if len(vals) == len(keys):
                        if vals[0] == 'PAIR' or vals[0] == 'UNPAIRED':
                            for i, k in enumerate(keys):
                                try:
                                    parsed_data[s_name][k] = float(vals[i])
                                except ValueError:
                                    parsed_data[s_name][k] = vals[i]

            else:
                s_name = None
                keys = None

        for s_name in list(parsed_data.keys()):
            if len(parsed_data[s_name]) == 0:
                parsed_data.pop(s_name, None)

        for s_name in parsed_data.keys():
            if s_name in self.picard_alignment_metrics:
                log.debug('Duplicate sample name found in {}! Overwriting: {}'.format(f['fn'], s_name))
            self.add_data_source(f, s_name, section='AlignmentSummaryMetrics')
            self.picard_alignment_metrics[s_name] = parsed_data[s_name]

    self.picard_alignment_metrics = self.ignore_samples(self.picard_alignment_metrics)
    if len(self.picard_alignment_metrics) > 0:
        self.write_data_file(self.picard_alignment_metrics, 'multiqc_picard_AlignmentSummaryMetrics')
        self.general_stats_headers['PCT_PF_READS_ALIGNED'] = {'title':'% Aligned', 
         'description':'Percent of aligned reads', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'format':'{:,.0f}', 
         'scale':'RdYlGn', 
         'modify':lambda x: self.multiply_hundred(x)}
        for s_name in self.picard_alignment_metrics:
            if s_name not in self.general_stats_data:
                self.general_stats_data[s_name] = dict()
            self.general_stats_data[s_name].update(self.picard_alignment_metrics[s_name])

        pdata = dict()
        for s_name in self.picard_alignment_metrics.keys():
            pdata[s_name] = dict()
            if self.picard_alignment_metrics[s_name]['CATEGORY'] == 'PAIR':
                pdata[s_name]['total_reads'] = self.picard_alignment_metrics[s_name]['TOTAL_READS'] / 2
                pdata[s_name]['aligned_reads'] = self.picard_alignment_metrics[s_name]['PF_READS_ALIGNED'] / 2
            else:
                pdata[s_name]['total_reads'] = self.picard_alignment_metrics[s_name]['TOTAL_READS']
                pdata[s_name]['aligned_reads'] = self.picard_alignment_metrics[s_name]['PF_READS_ALIGNED']
            pdata[s_name]['unaligned_reads'] = pdata[s_name]['total_reads'] - pdata[s_name]['aligned_reads']

        keys = OrderedDict()
        keys['aligned_reads'] = {'name': 'Aligned Reads'}
        keys['unaligned_reads'] = {'name': 'Unaligned Reads'}
        pconfig = {'id':'picard_aligned_reads', 
         'title':'Picard: Aligned Reads', 
         'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads'}
        self.add_section(name='Alignment Summary',
          anchor='picard-alignmentsummary',
          description="Plase note that Picard's read counts are divided by two for paired-end data.",
          plot=(bargraph.plot(pdata, keys, pconfig)))
    return len(self.picard_alignment_metrics)