# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/prokka/prokka.py
# Compiled at: 2019-11-20 10:26:16
# Size of source mod 2**32: 7997 bytes
""" MultiQC module to parse output from Prokka """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc import config
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.plots import table, bargraph
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Prokka', anchor='prokka', href='http://www.vicbioinformatics.com/software.prokka.shtml',
          info='is a software tool for the rapid annotation of prokaryotic genomes.')
        self.prokka = dict()
        for f in self.find_log_files('prokka', filehandles=True):
            self.parse_prokka(f)

        self.prokka = self.ignore_samples(self.prokka)
        if len(self.prokka) == 0:
            raise UserWarning
        log.info('Found {} logs'.format(len(self.prokka)))
        self.write_data_file(self.prokka, 'multiqc_prokka')
        headers = OrderedDict()
        headers['organism'] = {'title':'Organism', 
         'description':'Organism'}
        headers['contigs'] = {'title':'Contigs', 
         'description':'Number of contigs', 
         'min':0}
        headers['bases'] = {'title':'Bases', 
         'description':'Number of bases', 
         'min':0, 
         'format':'{:i}%', 
         'hidden':True}
        headers['CDS'] = {'title':'CDS', 
         'description':'Number of CDS', 
         'min':0, 
         'format':'{:i}%'}
        self.general_stats_addcols(self.prokka, headers)
        if getattr(config, 'prokka_table', False):
            self.add_section(plot=(self.prokka_table()))
        if getattr(config, 'prokka_barplot', True):
            descr_plot = 'This barplot shows the distribution of different types of features found in each contig.'
            helptext = '\n            `Prokka` can detect different features:\n\n            - CDS\n            - rRNA\n            - tmRNA\n            - tRNA\n            - miscRNA\n            - signal peptides\n            - CRISPR arrays\n\n            This barplot shows you the distribution of these different types of features found in each contig.\n            '
            self.add_section(plot=(self.prokka_barplot()), helptext=helptext,
              description=descr_plot)

    def parse_prokka(self, f):
        """ Parse prokka txt summary files.

        Prokka summary files are difficult to identify as there are practically
        no distinct prokka identifiers in the filenames or file contents. This
        parser makes an attempt using the first three lines, expected to contain
        organism, contigs, and bases statistics.
        """
        s_name = None
        first_line = f['f'].readline()
        contigs_line = f['f'].readline()
        bases_line = f['f'].readline()
        if not all((first_line.startswith('organism:'),
         contigs_line.startswith('contigs:'),
         bases_line.startswith('bases:'))):
            return
        try:
            organism = ' '.join(first_line.strip().split(':', 1)[1].split()[:2])
            s_name = self.clean_s_name(' '.join(first_line.split()[3:]), f['root'])
        except KeyError:
            organism = first_line.strip().split(':', 1)[1]
            s_name = f['s_name']

        if getattr(config, 'prokka_fn_snames', False):
            s_name = f['s_name']
        if s_name in self.prokka:
            log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
        self.prokka[s_name] = dict()
        self.prokka[s_name]['organism'] = organism
        self.prokka[s_name]['contigs'] = int(contigs_line.split(':')[1])
        self.prokka[s_name]['bases'] = int(bases_line.split(':')[1])
        for line in f['f']:
            description, value = line.split(':')
            try:
                self.prokka[s_name][description] = int(value)
            except ValueError:
                log.warning("Unable to parse line: '%s'", line)

        self.add_data_source(f, s_name)

    def prokka_table(self):
        """ Make basic table of the annotation stats """
        headers = OrderedDict()
        headers['organism'] = {'title':'Organism', 
         'description':'Organism name'}
        headers['contigs'] = {'title':'# contigs', 
         'description':'Number of contigs in assembly', 
         'format':'{:i}'}
        headers['bases'] = {'title':'# bases', 
         'description':'Number of nucleotide bases in assembly', 
         'format':'{:i}'}
        headers['CDS'] = {'title':'# CDS', 
         'description':'Number of annotated CDS', 
         'format':'{:i}'}
        headers['rRNA'] = {'title':'# rRNA', 
         'description':'Number of annotated rRNA', 
         'format':'{:i}'}
        headers['tRNA'] = {'title':'# tRNA', 
         'description':'Number of annotated tRNA', 
         'format':'{:i}'}
        headers['tmRNA'] = {'title':'# tmRNA', 
         'description':'Number of annotated tmRNA', 
         'format':'{:i}'}
        headers['misc_RNA'] = {'title':'# misc RNA', 
         'description':'Number of annotated misc. RNA', 
         'format':'{:i}'}
        headers['sig_peptide'] = {'title':'# sig_peptide', 
         'description':'Number of annotated sig_peptide', 
         'format':'{:i}'}
        headers['repeat_region'] = {'title':'# CRISPR arrays', 
         'description':'Number of annotated CRSIPR arrays', 
         'format':'{:i}'}
        table_config = {'namespace':'prokka', 
         'min':0}
        return table.plot(self.prokka, headers, table_config)

    def prokka_barplot(self):
        """ Make a basic plot of the annotation stats """
        keys = OrderedDict()
        keys['CDS'] = {'name': 'CDS'}
        keys['rRNA'] = {'name': 'rRNA'}
        keys['tRNA'] = {'name': 'tRNA'}
        keys['tmRNA'] = {'name': 'tmRNA'}
        keys['misc_RNA'] = {'name': 'misc RNA'}
        keys['sig_peptide'] = {'name': 'Signal peptides'}
        keys['repeat_region'] = {'name': 'CRISPR array'}
        plot_config = {'id':'prokka_plot', 
         'title':'Prokka: Feature Types', 
         'ylab':'# Counts', 
         'cpswitch_counts_label':'Features'}
        return bargraph.plot(self.prokka, keys, plot_config)