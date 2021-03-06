# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/sexdeterrmine/sexdeterrmine.py
# Compiled at: 2019-10-28 10:24:54
# Size of source mod 2**32: 5016 bytes
""" MultiQC module to parse output from SexdetErrmine """
from __future__ import print_function
from collections import OrderedDict
import logging, json
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' SexDeterrmine module '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='SexDetErrmine', anchor='sexdeterrmine', href='https://github.com/TCLamnidis/Sex.DetERRmine',
          info='A python script to calculate the relative coverage of X and Y chromosomes,\n            and their associated error bars, from the depth of coverage at specified SNPs. ')
        self.sexdet_data = dict()
        for f in self.find_log_files('sexdeterrmine', filehandles=True):
            self.parse_data(f)

        self.sexdet_data = self.ignore_samples(self.sexdet_data)
        if len(self.sexdet_data) == 0:
            raise UserWarning
        self.write_data_file(self.sexdet_data, 'multiqc_sexdeter_metrics')
        self.addSummaryMetrics()
        self.read_count_barplot()
        self.snp_count_barplot()

    def parse_data(self, f):
        try:
            data = json.load(f['f'])
        except Exception as e:
            try:
                log.debug(e)
                log.warn("Could not parse SexDeterrmine JSON: '{}'".format(f['fn']))
                return
            finally:
                e = None
                del e

        for s_name in data:
            if s_name == 'Metadata':
                continue
            s_clean = self.clean_s_name(s_name, f['root'])
            if s_clean in self.sexdet_data:
                log.debug('Duplicate sample name found! Overwriting: {}'.format(s_clean))
            self.add_data_source(f, s_clean)
            self.sexdet_data[s_clean] = dict()
            for k, v in data[s_name].items():
                try:
                    self.sexdet_data[s_clean][k] = float(v)
                except ValueError:
                    self.sexdet_data[s_clean][k] = v

    def addSummaryMetrics(self):
        """ Take the parsed stats from SexDetErrmine and add it to the main plot """
        headers = OrderedDict()
        headers['RateErrX'] = {'title':'Err Rate X', 
         'description':'Rate of Error for Chr X', 
         'scale':'OrRd', 
         'hidden':True, 
         'shared_key':'snp_err_rate'}
        headers['RateErrY'] = {'title':'Err Rate Y', 
         'description':'Rate of Error for Chr Y', 
         'scale':'OrRd', 
         'hidden':True, 
         'shared_key':'snp_err_rate'}
        headers['RateX'] = {'title':'Rate X', 
         'description':'Number of positions on Chromosome X vs Autosomal positions.', 
         'scale':'PuBuGn', 
         'shared_key':'snp_count'}
        headers['RateY'] = {'title':'Rate Y', 
         'description':'Number of positions on Chromosome Y vs Autosomal positions.', 
         'scale':'BuPu', 
         'shared_key':'snp_count'}
        self.general_stats_addcols(self.sexdet_data, headers)

    def read_count_barplot(self):
        """ Make a bar plot showing read counts on Autosomal, X and Y chr
        """
        cats = OrderedDict()
        cats['NR Aut'] = {'name': 'Autosomal Reads'}
        cats['NrX'] = {'name': 'Reads on X'}
        cats['NrY'] = {'name': 'Reads on Y'}
        config = {'id':'sexdeterrmine-readcounts-plot', 
         'title':'SexDetErrmine: Read Counts', 
         'ylab':'# Reads'}
        self.add_section(name='Read Counts',
          anchor='sexdeterrmine-readcounts',
          description='The number of reads covering positions on the autosomes, X and Y chromosomes.',
          plot=(bargraph.plot(self.sexdet_data, cats, config)))

    def snp_count_barplot(self):
        """ Make a bar plot showing read counts on Autosomal, X and Y chr
        """
        cats = OrderedDict()
        cats['Snps Autosomal'] = {'name': 'Autosomal SNPs'}
        cats['XSnps'] = {'name': 'SNPs on X'}
        cats['YSnps'] = {'name': 'SNPs on Y'}
        config = {'id':'sexdeterrmine-snps-plot', 
         'title':'SexDetErrmine: SNP Counts', 
         'ylab':'# Reads'}
        self.add_section(name='SNP Counts',
          anchor='sexdeterrmine-snps',
          description='Total number of SNP positions. When supplied with a BED file, this includes only positions specified there.',
          plot=(bargraph.plot(self.sexdet_data, cats, config)))