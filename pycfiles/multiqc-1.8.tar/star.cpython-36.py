# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/star/star.py
# Compiled at: 2019-11-20 10:26:16
# Size of source mod 2**32: 12498 bytes
""" MultiQC module to parse output from STAR """
from __future__ import print_function
from collections import OrderedDict
import logging, os, re
from multiqc import config
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='STAR', anchor='star', href='https://github.com/alexdobin/STAR',
          info='is an ultrafast universal RNA-seq aligner.')
        self.star_data = dict()
        for f in self.find_log_files('star'):
            parsed_data = self.parse_star_report(f['f'])
            if parsed_data is not None:
                s_name = f['s_name']
                if s_name == '' or s_name == 'Log.final.out':
                    s_name = self.clean_s_name(os.path.basename(f['root']), os.path.dirname(f['root']))
                if s_name in self.star_data:
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
                self.add_data_source(f, section='SummaryLog')
                self.star_data[s_name] = parsed_data

        self.star_genecounts_unstranded = dict()
        self.star_genecounts_first_strand = dict()
        self.star_genecounts_second_strand = dict()
        for f in self.find_log_files('star/genecounts', filehandles=True):
            parsed_data = self.parse_star_genecount_report(f)
            if parsed_data is not None:
                s_name = f['s_name']
                if s_name == '' or s_name == 'ReadsPerGene.out.tab':
                    s_name = self.clean_s_name(os.path.basename(f['root']), os.path.dirname(f['root']))
                if s_name in self.star_data:
                    log.debug('Duplicate ReadsPerGene sample name found! Overwriting: {}'.format(s_name))
                self.add_data_source(f, section='ReadsPerGene')
                self.star_genecounts_unstranded[s_name] = parsed_data['unstranded']
                self.star_genecounts_first_strand[s_name] = parsed_data['first_strand']
                self.star_genecounts_second_strand[s_name] = parsed_data['second_strand']

        self.star_data = self.ignore_samples(self.star_data)
        self.star_genecounts_unstranded = self.ignore_samples(self.star_genecounts_unstranded)
        self.star_genecounts_first_strand = self.ignore_samples(self.star_genecounts_first_strand)
        self.star_genecounts_second_strand = self.ignore_samples(self.star_genecounts_second_strand)
        if len(self.star_data) == 0:
            if len(self.star_genecounts_unstranded) == 0:
                raise UserWarning
        else:
            if len(self.star_data) > 0:
                if len(self.star_genecounts_unstranded) > 0:
                    log.info('Found {} reports and {} gene count files'.format(len(self.star_data), len(self.star_genecounts_unstranded)))
                else:
                    log.info('Found {} reports'.format(len(self.star_data)))
            else:
                log.info('Found {} gene count files'.format(len(self.star_genecounts_unstranded)))
        if len(self.star_data) > 0:
            self.write_data_file(self.star_data, 'multiqc_star')
            self.star_stats_table()
            self.add_section(name='Alignment Scores',
              anchor='star_alignments',
              plot=(self.star_alignment_chart()))
        if len(self.star_genecounts_unstranded) > 0:
            self.add_section(name='Gene Counts',
              anchor='star_geneCounts',
              description=('Statistics from results generated using <code>--quantMode GeneCounts</code>. ' + 'The three tabs show counts for unstranded RNA-seq, counts for the 1st read strand ' + 'aligned with RNA and counts for the 2nd read strand aligned with RNA.'),
              plot=(self.star_genecount_chart()))

    def parse_star_report(self, raw_data):
        """ Parse the final STAR log file. """
        regexes = {'total_reads':'Number of input reads \\|\\s+(\\d+)', 
         'avg_input_read_length':'Average input read length \\|\\s+([\\d\\.]+)', 
         'uniquely_mapped':'Uniquely mapped reads number \\|\\s+(\\d+)', 
         'uniquely_mapped_percent':'Uniquely mapped reads % \\|\\s+([\\d\\.]+)', 
         'avg_mapped_read_length':'Average mapped length \\|\\s+([\\d\\.]+)', 
         'num_splices':'Number of splices: Total \\|\\s+(\\d+)', 
         'num_annotated_splices':'Number of splices: Annotated \\(sjdb\\) \\|\\s+(\\d+)', 
         'num_GTAG_splices':'Number of splices: GT/AG \\|\\s+(\\d+)', 
         'num_GCAG_splices':'Number of splices: GC/AG \\|\\s+(\\d+)', 
         'num_ATAC_splices':'Number of splices: AT/AC \\|\\s+(\\d+)', 
         'num_noncanonical_splices':'Number of splices: Non-canonical \\|\\s+(\\d+)', 
         'mismatch_rate':'Mismatch rate per base, % \\|\\s+([\\d\\.]+)', 
         'deletion_rate':'Deletion rate per base \\|\\s+([\\d\\.]+)', 
         'deletion_length':'Deletion average length \\|\\s+([\\d\\.]+)', 
         'insertion_rate':'Insertion rate per base \\|\\s+([\\d\\.]+)', 
         'insertion_length':'Insertion average length \\|\\s+([\\d\\.]+)', 
         'multimapped':'Number of reads mapped to multiple loci \\|\\s+(\\d+)', 
         'multimapped_percent':'% of reads mapped to multiple loci \\|\\s+([\\d\\.]+)', 
         'multimapped_toomany':'Number of reads mapped to too many loci \\|\\s+(\\d+)', 
         'multimapped_toomany_percent':'% of reads mapped to too many loci \\|\\s+([\\d\\.]+)', 
         'unmapped_mismatches_percent':'% of reads unmapped: too many mismatches \\|\\s+([\\d\\.]+)', 
         'unmapped_tooshort_percent':'% of reads unmapped: too short \\|\\s+([\\d\\.]+)', 
         'unmapped_other_percent':'% of reads unmapped: other \\|\\s+([\\d\\.]+)'}
        parsed_data = {}
        for k, r in regexes.items():
            r_search = re.search(r, raw_data, re.MULTILINE)
            if r_search:
                parsed_data[k] = float(r_search.group(1))

        try:
            total_mapped = parsed_data['uniquely_mapped'] + parsed_data['multimapped'] + parsed_data['multimapped_toomany']
            unmapped_count = parsed_data['total_reads'] - total_mapped
            total_unmapped_percent = parsed_data['unmapped_mismatches_percent'] + parsed_data['unmapped_tooshort_percent'] + parsed_data['unmapped_other_percent']
            try:
                parsed_data['unmapped_mismatches'] = int(round(unmapped_count * (parsed_data['unmapped_mismatches_percent'] / total_unmapped_percent), 0))
                parsed_data['unmapped_tooshort'] = int(round(unmapped_count * (parsed_data['unmapped_tooshort_percent'] / total_unmapped_percent), 0))
                parsed_data['unmapped_other'] = int(round(unmapped_count * (parsed_data['unmapped_other_percent'] / total_unmapped_percent), 0))
            except ZeroDivisionError:
                parsed_data['unmapped_mismatches'] = 0
                parsed_data['unmapped_tooshort'] = 0
                parsed_data['unmapped_other'] = 0

        except KeyError:
            pass

        if len(parsed_data) == 0:
            return
        else:
            return parsed_data

    def parse_star_genecount_report(self, f):
        """ Parse a STAR gene counts output file """
        keys = [
         'N_unmapped', 'N_multimapping', 'N_noFeature', 'N_ambiguous']
        unstranded = {'N_genes': 0}
        first_strand = {'N_genes': 0}
        second_strand = {'N_genes': 0}
        num_errors = 0
        num_genes = 0
        for l in f['f']:
            s = l.split('\t')
            try:
                for i in (1, 2, 3):
                    s[i] = float(s[i])

                if s[0] in keys:
                    unstranded[s[0]] = s[1]
                    first_strand[s[0]] = s[2]
                    second_strand[s[0]] = s[3]
                else:
                    unstranded['N_genes'] += s[1]
                    first_strand['N_genes'] += s[2]
                    second_strand['N_genes'] += s[3]
                    num_genes += 1
            except IndexError:
                num_errors += 1
                if num_errors > 10:
                    if num_genes == 0:
                        log.warning('Error parsing {}'.format(f['fn']))
                        return

        if num_genes > 0:
            return {'unstranded':unstranded,  'first_strand':first_strand,  'second_strand':second_strand}
        else:
            return

    def star_stats_table(self):
        """ Take the parsed stats from the STAR report and add them to the
        basic stats table at the top of the report """
        headers = OrderedDict()
        headers['uniquely_mapped_percent'] = {'title':'% Aligned', 
         'description':'% Uniquely mapped reads', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'YlGn'}
        headers['uniquely_mapped'] = {'title':'{} Aligned'.format(config.read_count_prefix), 
         'description':'Uniquely mapped reads ({})'.format(config.read_count_desc), 
         'min':0, 
         'scale':'PuRd', 
         'modify':lambda x: x * config.read_count_multiplier, 
         'shared_key':'read_count'}
        self.general_stats_addcols(self.star_data, headers)

    def star_alignment_chart(self):
        """ Make the plot showing alignment rates """
        keys = OrderedDict()
        keys['uniquely_mapped'] = {'color':'#437bb1',  'name':'Uniquely mapped'}
        keys['multimapped'] = {'color':'#7cb5ec',  'name':'Mapped to multiple loci'}
        keys['multimapped_toomany'] = {'color':'#f7a35c',  'name':'Mapped to too many loci'}
        keys['unmapped_mismatches'] = {'color':'#e63491',  'name':'Unmapped: too many mismatches'}
        keys['unmapped_tooshort'] = {'color':'#b1084c',  'name':'Unmapped: too short'}
        keys['unmapped_other'] = {'color':'#7f0000',  'name':'Unmapped: other'}
        pconfig = {'id':'star_alignment_plot', 
         'title':'STAR: Alignment Scores', 
         'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads'}
        return bargraph.plot(self.star_data, keys, pconfig)

    def star_genecount_chart(self):
        """ Make a plot for the ReadsPerGene output """
        keys = OrderedDict()
        keys['N_genes'] = {'color':'#2f7ed8',  'name':'Overlapping Genes'}
        keys['N_noFeature'] = {'color':'#0d233a',  'name':'No Feature'}
        keys['N_ambiguous'] = {'color':'#492970',  'name':'Ambiguous Features'}
        keys['N_multimapping'] = {'color':'#f28f43',  'name':'Multimapping'}
        keys['N_unmapped'] = {'color':'#7f0000',  'name':'Unmapped'}
        pconfig = {'id':'star_gene_counts', 
         'title':'STAR: Gene Counts', 
         'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads', 
         'data_labels':[
          'Unstranded', 'Same Stranded', 'Reverse Stranded']}
        datasets = [
         self.star_genecounts_unstranded,
         self.star_genecounts_first_strand,
         self.star_genecounts_second_strand]
        return bargraph.plot(datasets, [keys, keys, keys, keys], pconfig)