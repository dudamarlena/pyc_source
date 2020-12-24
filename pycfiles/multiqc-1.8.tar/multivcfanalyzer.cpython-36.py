# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/multivcfanalyzer/multivcfanalyzer.py
# Compiled at: 2019-11-20 09:48:56
# Size of source mod 2**32: 9525 bytes
""" MultiQC module to parse output from MultiVCFAnalyzer """
from __future__ import print_function
from collections import OrderedDict
import logging, json
from multiqc.plots import table
from multiqc.plots import bargraph
from collections import OrderedDict
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' MultiVCFAnalyzer module '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='MultiVCFAnalyzer', anchor='multivcfanalyzer', href='https://github.com/alexherbig/MultiVCFAnalyzer',
          info='combines multiple VCF files in a coherent way, can produce summary statistics and downstream analysis formats for phylogeny reconstruction.')
        self.mvcf_data = dict()
        for f in self.find_log_files('multivcfanalyzer', filehandles=True):
            self.parse_data(f)

        self.mvcf_data = self.ignore_samples(self.mvcf_data)
        if len(self.mvcf_data) == 0:
            raise UserWarning
        self.compute_perc_hets()
        self.write_data_file(self.mvcf_data, 'multiqc_multivcfanalyzer')
        self.addSummaryMetrics()
        self.add_section(name='Summary metrics',
          anchor='mvcf_table',
          plot=(self.addTable()))
        self.add_section(name='Call statistics barplot',
          anchor='mvcf-barplot',
          helptext='\n        MultiVCFAnalyzer has a filtering step during the merge, where SNPs of low quality are discarded.\n        This plot shows the number of SNPs that fell in to the different MultiVCFAnalyzer categories:\n\n        * _SNP Calls (all):_ Total number of non-reference homzygous and heterozygous calls made\n        * _Filtered SNP call:_ Number of non-reference positions excluded by user-supplied list.\n        * _Number of Reference Calls:_ Number of reference calls made\n        * _Discarded Reference Calls:_ Number of reference positions not reaching genotyping or coverage thresholds\n        * _Discarded SNP Call:_ Number of non-reference positions not reaching enough coverage.\n        * _No Call:_ Number of positions with no call made as reported by GATK\n        * _Unhandled Genotypes:_ Number of positions where more than two possible alleles occured and were discarded\n        ',
          plot=(self.addBarplot()))

    def parse_data(self, f):
        try:
            data = json.load(f['f'])
        except Exception as e:
            log.debug(e)
            log.warn("Could not parse MultiVCFAnalyzer JSON: '{}'".format(f['fn']))
            return

        for s_name, metrics in data.get('metrics', {}).items():
            s_clean = self.clean_s_name(s_name, f['root'])
            if s_clean in self.mvcf_data:
                log.debug('Duplicate sample name found! Overwriting: {}'.format(s_clean))
            self.add_data_source(f, s_clean)
            self.mvcf_data[s_clean] = dict()
            for snp_prop, value in metrics.items():
                self.mvcf_data[s_clean][snp_prop] = value

    def compute_perc_hets(self):
        """Take the parsed stats from MultiVCFAnalyzer and add one column per sample """
        for sample in self.mvcf_data:
            try:
                self.mvcf_data[sample]['Heterozygous SNP alleles (percent)'] = self.mvcf_data[sample]['SNP Calls (het)'] / self.mvcf_data[sample]['SNP Calls (all)'] * 100
            except ZeroDivisionError:
                self.mvcf_data[sample]['Heterozygous SNP alleles (percent)'] = 'NA'

    def addSummaryMetrics(self):
        """ Take the parsed stats from MultiVCFAnalyzer and add it to the main plot """
        headers = OrderedDict()
        headers['SNP Calls (all)'] = {'title':'SNPs', 
         'description':'Total number of non-reference calls made', 
         'scale':'OrRd', 
         'shared_key':'snp_call'}
        headers['SNP Calls (het)'] = {'title':'Het SNPs', 
         'description':'Total number of non-reference calls not passing homozygosity thresholds', 
         'scale':'OrRd', 
         'hidden':True, 
         'shared_key':'snp_call'}
        headers['Heterozygous SNP alleles (percent)'] = {'title':'% Hets', 
         'description':'Percentage of heterozygous SNP alleles', 
         'scale':'OrRd', 
         'shared_key':'snp_call'}
        self.general_stats_addcols(self.mvcf_data, headers)

    def addTable(self):
        """ Take the parsed stats from MultiVCFAnalyzer and add it to the MVCF Table"""
        headers = OrderedDict()
        headers['allPos'] = {'title':'Bases in SNP Alignment', 
         'description':'Length of FASTA file in base pairs (bp)', 
         'scale':'BuPu', 
         'shared_key':'calls', 
         'format':'{:,.0f}'}
        headers['discardedVarCall'] = {'title':'Discarded SNP Call', 
         'description':'Number of non-reference positions not reaching genotyping or coverage thresholds', 
         'scale':'BuPu', 
         'hidden':True, 
         'shared_key':'calls'}
        headers['filteredVarCall'] = {'title':'Filtered SNP Call', 
         'description':'Number of positions ignored defined in user-supplied filter list', 
         'scale':'BuPu', 
         'hidden':True, 
         'shared_key':'calls'}
        headers['refCall'] = {'title':'Reference Calls', 
         'description':'Number of reference calls made', 
         'scale':'BuPu', 
         'hidden':True, 
         'shared_key':'calls'}
        headers['discardedRefCall'] = {'title':'Discarded Reference Call', 
         'description':'Number of reference positions not reaching genotyping or coverage thresholds', 
         'scale':'BuPu', 
         'hidden':True, 
         'shared_key':'calls'}
        headers['noCall'] = {'title':'Positions with No Call', 
         'description':'Number of positions with no call made as reported by GATK', 
         'scale':'BuPu', 
         'shared_key':'calls'}
        headers['coverage (fold)'] = {'title':'SNP Coverage', 
         'description':'Average number of reads covering final calls', 
         'scale':'OrRd', 
         'shared_key':'coverage', 
         'suffix':'X'}
        headers['coverage (percent)'] = {'title':'% SNPs Covered', 
         'description':'Percent coverage of all positions with final calls', 
         'scale':'PuBuGn', 
         'shared_key':'coverage', 
         'suffix':'%'}
        headers['unhandledGenotype'] = {'title':'Unhandled Genotypes', 
         'description':'Number of positions discarded due to presence of more than one alternate allele', 
         'scale':'BuPu', 
         'hidden':True, 
         'shared_key':'snp_count'}
        table_config = {'namespace':'MultiVCFAnalyzer', 
         'id':'mvcf-table', 
         'table_title':'MultiVCFAnalyzer Results'}
        tab = table.plot(self.mvcf_data, headers, table_config)
        return tab

    def addBarplot(self):
        """ Take the parsed stats from MultiVCFAnalyzer and add it to the MVCF Table"""
        cats = OrderedDict()
        cats['SNP Calls (all)'] = {'name':'SNP Calls', 
         'color':'#8bbc21'}
        cats['discardedVarCall'] = {'name':'Discarded SNP Call', 
         'color':'#f7a35c'}
        cats['filteredVarCall'] = {'name': 'Filtered SNP Call'}
        cats['refCall'] = {'name': 'Reference Calls'}
        cats['discardedRefCall'] = {'name': 'Discarded Reference Call'}
        cats['noCall'] = {'name': 'Positions with No Call'}
        config = {'id':'mvcf_barplot', 
         'hide_zero_cats':True, 
         'title':'MultiVCFAnalyzer: Call Categories', 
         'ylab':'Total # Positions', 
         'xlab':None, 
         'stacking':'normal', 
         'use_legend':True}
        return bargraph.plot(self.mvcf_data, cats, config)