# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/picard/TargetedPcrMetrics.py
# Compiled at: 2018-02-21 12:08:13
""" MultiQC submodule to parse output from Picard TargetedPcrMetrics """
from collections import OrderedDict
import logging, os, re
from multiqc.plots import bargraph
log = logging.getLogger(__name__)

def parse_reports(self):
    """ Find Picard TargetedPcrMetrics reports and parse their data """
    self.picard_pcrmetrics_data = dict()
    self.picard_pcrmetrics_samplestats = dict()
    for f in self.find_log_files('picard/pcr_metrics', filehandles=True):
        s_name = None
        for l in f['f']:
            if 'TargetedPcrMetrics' in l and 'INPUT' in l:
                s_name = None
                fn_search = re.search('INPUT(?:=|\\s+)(\\[?[^\\s]+\\]?)', l, flags=re.IGNORECASE)
                if fn_search:
                    s_name = os.path.basename(fn_search.group(1).strip('[]'))
                    s_name = self.clean_s_name(s_name, f['root'])
            if s_name is not None:
                if 'TargetedPcrMetrics' in l and '## METRICS CLASS' in l:
                    keys = f['f'].readline().strip('\n').split('\t')
                    vals = f['f'].readline().strip('\n').split('\t')
                    if len(vals) == len(keys):
                        if s_name in self.picard_pcrmetrics_data:
                            log.debug(('Duplicate sample name found in {}! Overwriting: {}').format(f['fn'], s_name))
                        self.add_data_source(f, s_name, section='TargetedPcrMetrics')
                        self.picard_pcrmetrics_data[s_name] = dict()
                        for i, k in enumerate(keys):
                            try:
                                if k.startswith('PCT_'):
                                    vals[i] = float(vals[i]) * 100.0
                                self.picard_pcrmetrics_data[s_name][k] = float(vals[i])
                            except ValueError:
                                self.picard_pcrmetrics_data[s_name][k] = vals[i]

    self.picard_pcrmetrics_data = self.ignore_samples(self.picard_pcrmetrics_data)
    if len(self.picard_pcrmetrics_data) > 0:
        self.write_data_file(self.picard_pcrmetrics_data, 'multiqc_picard_pcrmetrics')
        self.general_stats_headers['PCT_AMPLIFIED_BASES'] = {'title': '% Amplified Bases', 
           'description': 'The fraction of aligned bases that mapped to or near an amplicon.', 
           'min': 0, 
           'max': 100, 
           'suffix': '%', 
           'scale': 'BrBG'}
        self.general_stats_headers['MEDIAN_TARGET_COVERAGE'] = {'title': 'Median Target Coverage', 
           'description': 'The median coverage of reads that mapped to target regions of an experiment.', 
           'min': 0, 
           'suffix': 'X', 
           'scale': 'GnBu'}
        for s_name in self.picard_pcrmetrics_data:
            if s_name not in self.general_stats_data:
                self.general_stats_data[s_name] = dict()
            self.general_stats_data[s_name].update(self.picard_pcrmetrics_data[s_name])

        keys = OrderedDict()
        keys['ON_AMPLICON_BASES'] = {'name': 'On-amplicon bases'}
        keys['NEAR_AMPLICON_BASES'] = {'name': 'Near-amplicon bases'}
        keys['OFF_AMPLICON_BASES'] = {'name': 'Off-amplicon bases', 'color': '#f28f43'}
        pconfig = {'id': 'picard_pcr_metrics_bases', 
           'title': 'Picard: PCR Amplicon Bases', 
           'ylab': '# Bases', 
           'cpswitch_counts_label': '# Bases', 
           'hide_zero_cats': False}
        self.add_section(name='PCR Amplicon Bases', anchor='picard-pcrmetrics-bases', description='Metrics about reads obtained from targeted PCR experiments.', helptext='\n            This plot shows the number of bases aligned on or near to amplified regions of the genome.\n\n            * `ON_AMPLICON_BASES`: The number of `PF_BASES_ALIGNED` that mapped to an amplified region of the genome.\n            * `NEAR_AMPLICON_BASES`: The number of `PF_BASES_ALIGNED` that mapped to within a fixed interval of an amplified region, but not on a baited region.\n            * `OFF_AMPLICON_BASES`: The number of `PF_BASES_ALIGNED` that mapped neither on or near an amplicon.\n\n            For more information see the [Picard documentation](https://broadinstitute.github.io/picard/picard-metric-definitions.html#TargetedPcrMetrics).', plot=bargraph.plot(self.picard_pcrmetrics_data, keys, pconfig))
    return len(self.picard_pcrmetrics_data)