# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/samtools/rmdup.py
# Compiled at: 2017-12-07 11:43:17
# Size of source mod 2**32: 3061 bytes
""" MultiQC module to parse output from Samtools rmdup """
import logging, re
from collections import OrderedDict
from multiqc.plots import bargraph
log = logging.getLogger(__name__)

class RmdupReportMixin:

    def parse_samtools_rmdup(self):
        """ Find Samtools rmdup logs and parse their data """
        self.samtools_rmdup = dict()
        for f in self.find_log_files('samtools/rmdup', filehandles=True):
            dups_regex = "\\[bam_rmdups?e?_core\\] (\\d+) / (\\d+) = (\\d+\\.\\d+) in library '(.*)'"
            s_name = f['s_name']
            for l in f['f']:
                match = re.search(dups_regex, l)
                if match:
                    library_name = match.group(4).strip()
                    if library_name != '':
                        s_name = library_name
                    if s_name in self.samtools_rmdup:
                        log.debug('Duplicate sample name found in {}! Overwriting: {}'.format(f['fn'], s_name))
                    self.add_data_source(f, s_name)
                    self.samtools_rmdup[s_name] = dict()
                    self.samtools_rmdup[s_name]['n_dups'] = int(match.group(1))
                    self.samtools_rmdup[s_name]['n_tot'] = int(match.group(2))
                    self.samtools_rmdup[s_name]['n_unique'] = int(match.group(2)) - int(match.group(1))
                    self.samtools_rmdup[s_name]['pct_dups'] = float(match.group(3)) * 100

        self.samtools_rmdup = self.ignore_samples(self.samtools_rmdup)
        if len(self.samtools_rmdup) > 0:
            self.write_data_file(self.samtools_rmdup, 'multiqc_samtools_rmdup')
            keys = OrderedDict()
            keys['n_unique'] = {'name': 'Non-duplicated reads'}
            keys['n_dups'] = {'name': 'Duplicated reads'}
            pconfig = {'id':'samtools_rmdup_plot', 
             'title':'Samtools rmdup: Duplicate alignments', 
             'ylab':'Number of reads', 
             'yDecimals':False}
            self.add_section(name='Duplicates removed',
              anchor='samtools-rmdup',
              plot=(bargraph.plot(self.samtools_rmdup, keys, pconfig)))
            stats_headers = OrderedDict()
            stats_headers['pct_dups'] = {'title':'% Dups', 
             'description':'Percent of duplicate alignments', 
             'min':0, 
             'max':100, 
             'suffix':'%', 
             'scale':'OrRd'}
            self.general_stats_addcols(self.samtools_rmdup, stats_headers, 'Samtools rmdup')
        return len(self.samtools_rmdup)