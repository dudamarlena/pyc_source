# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/rseqc/read_gc.py
# Compiled at: 2018-02-06 09:14:27
# Size of source mod 2**32: 2608 bytes
""" MultiQC submodule to parse output from RSeQC read_GC.py
http://rseqc.sourceforge.net/#read-gc-py """
from collections import OrderedDict
import logging
from multiqc.plots import linegraph
log = logging.getLogger(__name__)

def parse_reports(self):
    """ Find RSeQC read_GC reports and parse their data """
    self.read_gc = dict()
    self.read_gc_pct = dict()
    for f in self.find_log_files('rseqc/read_gc'):
        if f['f'].startswith('GC%\tread_count'):
            gc = list()
            counts = list()
            for l in f['f'].splitlines():
                s = l.split()
                try:
                    gc.append(float(s[0]))
                    counts.append(float(s[1]))
                except:
                    pass

            if len(gc) > 0:
                sorted_gc_keys = sorted((range(len(gc))), key=(lambda k: gc[k]))
                total = sum(counts)
                if f['s_name'] in self.read_gc:
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(f['s_name']))
                self.add_data_source(f, section='read_GC')
                self.read_gc[f['s_name']] = OrderedDict()
                self.read_gc_pct[f['s_name']] = OrderedDict()
                for i in sorted_gc_keys:
                    self.read_gc[f['s_name']][gc[i]] = counts[i]
                    self.read_gc_pct[f['s_name']][gc[i]] = counts[i] / total * 100

    self.read_gc = self.ignore_samples(self.read_gc)
    if len(self.read_gc) > 0:
        pconfig = {'id':'rseqc_read_gc_plot', 
         'title':'RSeQC: Read GC Content', 
         'ylab':'Number of Reads', 
         'xlab':'GC content (%)', 
         'xmin':0, 
         'xmax':100, 
         'tt_label':'<strong>{point.x}% GC</strong>: {point.y:.2f}', 
         'data_labels':[
          {'name':'Counts', 
           'ylab':'Number of Reads'},
          {'name':'Percentages', 
           'ylab':'Percentage of Reads'}]}
        self.add_section(name='Read GC Content',
          anchor='rseqc-read_gc',
          description='<a href="http://rseqc.sourceforge.net/#read-gc-py" target="_blank">read_GC</a> calculates a histogram of read GC content.</p>',
          plot=(linegraph.plot([self.read_gc, self.read_gc_pct], pconfig)))
    return len(self.read_gc)