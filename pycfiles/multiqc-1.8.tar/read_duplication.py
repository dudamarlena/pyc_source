# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/rseqc/read_duplication.py
# Compiled at: 2018-04-20 04:18:28
""" MultiQC submodule to parse output from RSeQC read_duplication.py
http://rseqc.sourceforge.net/#read-duplication-py """
from collections import OrderedDict
import logging
from multiqc.plots import linegraph
log = logging.getLogger(__name__)

def parse_reports(self):
    """ Find RSeQC read_duplication reports and parse their data """
    self.read_dups = dict()
    for f in self.find_log_files('rseqc/read_duplication_pos'):
        if f['f'].startswith('Occurrence\tUniqReadNumber'):
            if f['s_name'] in self.read_dups:
                log.debug(('Duplicate sample name found! Overwriting: {}').format(f['s_name']))
            self.add_data_source(f, section='read_duplication')
            self.read_dups[f['s_name']] = OrderedDict()
            for l in f['f'].splitlines():
                s = l.split()
                try:
                    if int(s[0]) <= 500:
                        self.read_dups[f['s_name']][int(s[0])] = int(s[1])
                except:
                    pass

    self.read_dups = self.ignore_samples(self.read_dups)
    if len(self.read_dups) > 0:
        pconfig = {'smooth_points': 200, 
           'id': 'rseqc_read_dups_plot', 
           'title': 'RSeQC: Read Duplication', 
           'ylab': 'Number of Reads (log10)', 
           'xlab': 'Occurrence of read', 
           'yLog': True, 
           'tt_label': '<strong>{point.x} occurrences</strong>: {point.y} reads'}
        self.add_section(name='Read Duplication', anchor='rseqc-read_dups', description='<a href="http://rseqc.sourceforge.net/#read-duplication-py" target="_blank">read_duplication.py</a> calculates how many alignment positions have a certain number of exact duplicates. Note - plot truncated at 500 occurrences and binned.</p>', plot=linegraph.plot(self.read_dups, pconfig))
    return len(self.read_dups)