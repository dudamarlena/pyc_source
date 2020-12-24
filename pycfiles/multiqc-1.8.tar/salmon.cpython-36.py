# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/salmon/salmon.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 3559 bytes
""" MultiQC module to parse output from Salmon """
from __future__ import print_function
from collections import OrderedDict
import json, logging, os
from multiqc.plots import linegraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Salmon', anchor='salmon', href='http://combine-lab.github.io/salmon/',
          info='is a tool for quantifying the expression of transcripts using RNA-seq data.')
        self.salmon_meta = dict()
        for f in self.find_log_files('salmon/meta'):
            s_name = os.path.basename(os.path.dirname(f['root']))
            s_name = self.clean_s_name(s_name, f['root'])
            self.salmon_meta[s_name] = json.loads(f['f'])

        self.salmon_fld = dict()
        for f in self.find_log_files('salmon/fld'):
            if os.path.basename(f['root']) == 'libParams':
                s_name = os.path.basename(os.path.dirname(f['root']))
                s_name = self.clean_s_name(s_name, f['root'])
                parsed = OrderedDict()
                for i, v in enumerate(f['f'].split()):
                    parsed[i] = float(v)

                if len(parsed) > 0:
                    if s_name in self.salmon_fld:
                        log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
                    self.add_data_source(f, s_name)
                    self.salmon_fld[s_name] = parsed

        self.salmon_meta = self.ignore_samples(self.salmon_meta)
        self.salmon_fld = self.ignore_samples(self.salmon_fld)
        if len(self.salmon_meta) == 0:
            if len(self.salmon_fld) == 0:
                raise UserWarning
        if len(self.salmon_meta) > 0:
            log.info('Found {} meta reports'.format(len(self.salmon_meta)))
            self.write_data_file(self.salmon_meta, 'multiqc_salmon')
        if len(self.salmon_fld) > 0:
            log.info('Found {} fragment length distributions'.format(len(self.salmon_fld)))
        headers = OrderedDict()
        headers['percent_mapped'] = {'title':'% Aligned', 
         'description':'% Mapped reads', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'YlGn'}
        headers['num_mapped'] = {'title':'M Aligned', 
         'description':'Mapped reads (millions)', 
         'min':0, 
         'scale':'PuRd', 
         'modify':lambda x: float(x) / 1000000, 
         'shared_key':'read_count'}
        self.general_stats_addcols(self.salmon_meta, headers)
        pconfig = {'smooth_points':500, 
         'id':'salmon_plot', 
         'title':'Salmon: Fragment Length Distribution', 
         'ylab':'Fraction', 
         'xlab':'Fragment Length (bp)', 
         'ymin':0, 
         'xmin':0, 
         'tt_label':'<b>{point.x:,.0f} bp</b>: {point.y:,.0f}'}
        self.add_section(plot=(linegraph.plot(self.salmon_fld, pconfig)))