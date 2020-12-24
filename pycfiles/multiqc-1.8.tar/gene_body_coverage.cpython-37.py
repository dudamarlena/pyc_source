# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/rseqc/gene_body_coverage.py
# Compiled at: 2017-09-23 10:30:24
# Size of source mod 2**32: 4376 bytes
""" MultiQC submodule to parse output from RSeQC geneBody_coverage.py
http://rseqc.sourceforge.net/#genebody-coverage-py """
from collections import OrderedDict
import logging
from multiqc.plots import linegraph
log = logging.getLogger(__name__)

def parse_reports(self):
    """ Find RSeQC gene_body_coverage reports and parse their data """
    self.gene_body_cov_hist_counts = dict()
    self.gene_body_cov_hist_percent = dict()
    for f in self.find_log_files('rseqc/gene_body_coverage'):
        if f['f'].startswith('Percentile'):
            keys = []
            nrows = 0
            for l in f['f'].splitlines():
                s = l.split()
                if len(keys) == 0:
                    keys = s[1:]
                else:
                    nrows += 1
                    s_name = self.clean_s_name(s[0], f['root'])
                    if s_name in self.gene_body_cov_hist_counts:
                        log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
                    self.add_data_source(f, s_name, section='gene_body_coverage')
                    self.gene_body_cov_hist_counts[s_name] = OrderedDict()
                    for k, var in enumerate(s[1:]):
                        self.gene_body_cov_hist_counts[s_name][int(keys[k])] = float(var)

            if nrows == 0:
                log.warning('Empty geneBodyCoverage file found: {}'.format(f['fn']))
            elif f['f'].startswith('Total reads'):
                if f['s_name'].endswith('.geneBodyCoverage'):
                    f['s_name'] = f['s_name'][:-17]
                if f['s_name'] in self.gene_body_cov_hist_counts:
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(f['s_name']))
                self.add_data_source(f, section='gene_body_coverage')
                self.gene_body_cov_hist_counts[f['s_name']] = OrderedDict()
                nrows = 0
                for l in f['f'].splitlines():
                    s = l.split()
                    try:
                        nrows += 1
                        self.gene_body_cov_hist_counts[f['s_name']][int(s[0])] = float(s[1])
                    except:
                        pass

                if nrows == 0:
                    del self.gene_body_cov_hist_counts[f['s_name']]
                    log.warning('Empty geneBodyCoverage file found: {}'.format(f['fn']))

    self.gene_body_cov_hist_counts = self.ignore_samples(self.gene_body_cov_hist_counts)
    if len(self.gene_body_cov_hist_counts) > 0:
        for s_name in self.gene_body_cov_hist_counts:
            self.gene_body_cov_hist_percent[s_name] = OrderedDict()
            total = sum(self.gene_body_cov_hist_counts[s_name].values())
            for k, v in self.gene_body_cov_hist_counts[s_name].items():
                self.gene_body_cov_hist_percent[s_name][k] = v / total * 100

        pconfig = {'id':'rseqc_gene_body_coverage_plot', 
         'title':'RSeQC: Gene Body Coverage', 
         'ylab':'% Coverage', 
         'xlab':"Gene Body Percentile (5' -> 3')", 
         'xmin':0, 
         'xmax':100, 
         'tt_label':"<strong>{point.x}% from 5'</strong>: {point.y:.2f}", 
         'data_labels':[
          {'name':'Percentages', 
           'ylab':'Percentage Coverage'},
          {'name':'Counts', 
           'ylab':'Coverage'}]}
        self.add_section(name='Gene Body Coverage',
          anchor='rseqc-gene_body_coverage',
          description='<a href="http://rseqc.sourceforge.net/#genebody-coverage-py" target="_blank">Gene Body Coverage</a> calculates read coverage over gene bodies. This is used to check if reads coverage is uniform and if there is any 5\' or 3\' bias.',
          plot=(linegraph.plot([self.gene_body_cov_hist_percent, self.gene_body_cov_hist_counts], pconfig)))
    return len(self.gene_body_cov_hist_counts)