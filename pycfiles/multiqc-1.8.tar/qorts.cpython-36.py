# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/qorts/qorts.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 13857 bytes
""" MultiQC module to parse output from QoRTs """
from __future__ import print_function
from collections import OrderedDict
import re, os, logging
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='QoRTs', anchor='qorts', href='http://hartleys.github.io/QoRTs/',
          info='is toolkit for analysis, QC and data management of RNA-Seq datasets.')
        self.qorts_data = dict()
        for f in self.find_log_files('qorts', filehandles=True):
            self.parse_qorts(f)

        self.qorts_data = {s:v for s, v in self.qorts_data.items() if len(v) > 0 if len(v) > 0}
        self.qorts_data = self.ignore_samples(self.qorts_data)
        if len(self.qorts_data) == 0:
            raise UserWarning
        log.info('Found {} logs'.format(len(self.qorts_data)))
        self.write_data_file(self.qorts_data, 'multiqc_qorts')
        self.qorts_general_stats()
        self.qorts_alignment_barplot()
        self.qorts_splice_loci_barplot()
        self.qorts_splice_events_barplot()
        self.qorts_strandedness_plot()

    def parse_qorts(self, f):
        s_names = None
        for l in f['f']:
            s = l.split('\t')
            if s_names is None:
                s_names = [self.clean_s_name(s_name, f['root']) for s_name in s[1:]]
                if len(s_names) <= 2:
                    if s_names[0].endswith('COUNT'):
                        if f['fn'] == 'QC.summary.txt':
                            s_names = [
                             self.clean_s_name(os.path.basename(os.path.normpath(f['root'])), f['root'])]
                        else:
                            s_names = [
                             f['s_name']]
                for s_name in s_names:
                    if s_name in self.qorts_data:
                        log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
                    self.qorts_data[s_name] = dict()

            else:
                for i, s_name in enumerate(s_names):
                    self.qorts_data[s_name][s[0]] = float(s[(i + 1)])

        for i, s_name in enumerate(s_names):
            if 'Genes_Total' in self.qorts_data[s_name] and 'Genes_WithNonzeroCounts' in self.qorts_data[s_name]:
                self.qorts_data[s_name]['Genes_PercentWithNonzeroCounts'] = self.qorts_data[s_name]['Genes_WithNonzeroCounts'] / self.qorts_data[s_name]['Genes_Total'] * 100.0

    def qorts_general_stats(self):
        """ Add columns to the General Statistics table """
        headers = OrderedDict()
        headers['Genes_PercentWithNonzeroCounts'] = {'title':'% Genes with Counts', 
         'description':'Percent of Genes with Non-Zero Counts', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'YlGn'}
        headers['NumberOfChromosomesCovered'] = {'title':'Chrs Covered', 
         'description':'Number of Chromosomes Covered', 
         'format':'{:,.0f}'}
        self.general_stats_addcols(self.qorts_data, headers)

    def qorts_alignment_barplot(self):
        """ Alignment statistics bar plot """
        keys = [
         'ReadPairs_UniqueGene_CDS',
         'ReadPairs_UniqueGene_UTR',
         'ReadPairs_AmbigGene',
         'ReadPairs_NoGene_Intron',
         'ReadPairs_NoGene_OneKbFromGene',
         'ReadPairs_NoGene_TenKbFromGene',
         'ReadPairs_NoGene_MiddleOfNowhere']
        cats = OrderedDict()
        for k in keys:
            name = k.replace('ReadPairs_', '').replace('_', ': ')
            name = re.sub('([a-z])([A-Z])', '\\g<1> \\g<2>', name)
            cats[k] = {'name': name}

        pconfig = {'id':'qorts_alignments', 
         'title':'QoRTs: Alignment Locations', 
         'ylab':'# Read Pairs', 
         'cpswitch_counts_label':'Number of Read Pairs', 
         'hide_zero_cats':False}
        self.add_section(name='Alignments',
          description="This plot displays the rate for which the sample's read-pairs are assigned to the different categories.",
          helptext='\n            The [QoRTs vignette](http://hartleys.github.io/QoRTs/doc/QoRTs-vignette.pdf) describes the categories in this plot as follows:\n\n            * **Unique Gene**: The read-pair overlaps with the exonic segments of one and only one gene. For many\n              downstream analyses tools, such as DESeq, DESeq2 and EdgeR, only read-pairs in this category\n              are used.\n            * **Ambig Gene**: The read-pair overlaps with the exons of more than one gene.\n            * **No Gene: Intronic**: The read-pair does not overlap with the exons of any annotated gene, but appears\n              in a region that is bridged by an annotated splice junction.\n            * **No Gene: One kb From Gene**: The read-pair does not overlap with the exons of any annotated gene, but is\n              within 1 kilobase from the nearest annotated gene.\n            * **No Gene: Ten kb From Gene**: The read-pair does not overlap with the exons of any annotated gene, but\n              is within 10 kilobases from the nearest annotated gene.\n            * **No Gene: Middle Of Nowhere**: The read-pair does not overlap with the exons of any annotated gene,\n              and is more than 10 kilobases from the nearest annotated gene.\n\n            _What it means and what to look for:_\n\n            Outliers in these plots can indicate biological variations or the presence of large mapping problems.\n            They may also suggest the presence of large, highly-expressed, unannotated transcripts or genes.\n            ',
          plot=(bargraph.plot(self.qorts_data, cats, pconfig)))

    def qorts_splice_loci_barplot(self):
        """ Make the HighCharts HTML to plot the qorts splice loci """
        keys = [
         'SpliceLoci_Known_ManyReads',
         'SpliceLoci_Known_FewReads',
         'SpliceLoci_Known_NoReads',
         'SpliceLoci_Novel_ManyReads',
         'SpliceLoci_Novel_FewReads']
        cats = OrderedDict()
        for k in keys:
            name = k.replace('SpliceLoci_', '').replace('_', ': ')
            name = re.sub('([a-z])([A-Z])', '\\g<1> \\g<2>', name)
            cats[k] = {'name': name}

        pconfig = {'id':'qorts_splice_loci', 
         'title':'QoRTs: Splice Loci', 
         'ylab':'# Splice Loci', 
         'cpswitch_counts_label':'Number of Splice Loci', 
         'hide_zero_cats':False}
        self.add_section(name='Splice Loci',
          description="This plot shows the number of splice junction loci of each type that appear in the sample's reads.",
          helptext='\n            The [QoRTs vignette](http://hartleys.github.io/QoRTs/doc/QoRTs-vignette.pdf) describes the categories in this plot as follows:\n\n            * **Known**: The splice junction locus is found in the supplied transcript annotation gtf file.\n            * **Novel**: The splice junction locus is NOT found in the supplied transcript annotation gtf file.\n            * **Known: Few reads**: The locus is known, and is only covered by 1-3 read-pairs.\n            * **Known: Many reads**: The locus is known, and is covered by 4 or more read-pairs.\n            * **Novel: Few reads**: The locus is novel, and is only covered by 1-3 read-pairs.\n            * **Novel: Many reads**: The locus is novel, and is covered by 4 or more read-pairs\n\n            _What it means and what to look for:_\n\n            This plot can be used to detect a number of anomalies. For example:\n            whether mapping or sequencing artifacts caused a disproportionate discovery of novel splice junctions in\n            one sample or batch. It can also be used as an indicator of the comprehensiveness the genome annotation.\n            Replicates that are obvious outliers may have sequencing/technical issues causing false detection of splice\n            junctions.\n\n            Abnormalities in the splice junction rates are generally a symptom of larger issues which will generally be\n            picked up by other metrics. Numerous factors can reduce the efficacy by which aligners map across splice\n            junctions, and as such these plots become very important if the intended downstream analyses include\n            transcript assembly, transcript deconvolution, differential splicing, or any other form of analysis that in\n            some way involves the splice junctions themselves. These plots can be used to assess whether other minor\n            abnormalities observed in the other plots are of sufficient severity to impact splice junction mapping and\n            thus potentially compromise such analyses.\n            ',
          plot=(bargraph.plot(self.qorts_data, cats, pconfig)))

    def qorts_splice_events_barplot(self):
        """ Make the HighCharts HTML to plot the qorts splice events """
        keys = [
         'SpliceEvents_KnownLociWithManyReads',
         'SpliceEvents_KnownLociWithFewReads',
         'SpliceEvents_NovelLociWithManyReads',
         'SpliceEvents_NovelLociWithFewReads']
        cats = OrderedDict()
        for k in keys:
            name = k.replace('SpliceEvents_', '')
            name = re.sub('([a-z])([A-Z])', '\\g<1> \\g<2>', name)
            cats[k] = {'name': name}

        pconfig = {'id':'qorts_splice_events', 
         'title':'QoRTs: Splice Events', 
         'ylab':'# Splice Events', 
         'cpswitch_counts_label':'Number of Splice Events', 
         'hide_zero_cats':False}
        self.add_section(name='Splice Events',
          description='This plot shows the number of splice junction events falling into different junction categories.',
          helptext='\n            From the [QoRTs vignette](http://hartleys.github.io/QoRTs/doc/QoRTs-vignette.pdf):\n\n            A splice junction "event" is one instance of a read-pair bridging a splice junction.\n            Some reads may contain multiple splice junction events, some may contain none. If a splice junction appears\n            on both reads of a read-pair, this is still only counted as a single "event".\n\n            Note that because different samples/runs may have different total read counts and/or library sizes, this function\n            is generally not the best for comparing between samples. In general, the event rates per read-pair should be\n            used instead.\n            This plot is used to detect whether sample-specific or batch effects have a substantial or biased effect on splice\n            junction appearance, either due to differences in the original RNA, or due to artifacts that alter the rate at\n            which the aligner maps across splice junctions.\n\n            _What it means and what to look for:_\n\n            This plot is useful for identifying mapping and/or annotation issues,\n            and can indicate the comprehensiveness the genome annotation. Replicates that are obvious outliers may\n            have sequencing/technical issues causing false detection of splice junctions.\n            In general, abnormalities in the splice junction rates are generally a symptom of larger issues which will\n            often be picked up by other metrics.\n            ',
          plot=(bargraph.plot(self.qorts_data, cats, pconfig)))

    def qorts_strandedness_plot(self):
        """ Make a bar plot showing the reads assigned to each strand """
        keys = [
         'StrandTest_frFirstStrand',
         'StrandTest_frSecondStrand',
         'StrandTest_ambig_genesFountOnBothStrands',
         'StrandTest_ambig_noGenes',
         'StrandTest_ambig_other']
        cats = OrderedDict()
        for k in keys:
            name = k.replace('StrandTest_', '').replace('_', ' ').replace('ambig', 'ambig:')
            name = re.sub('([a-z])([A-Z])', '\\g<1> \\g<2>', name)
            cats[k] = {'name': name.title()}

        pconfig = {'id':'qorts_strand_test', 
         'title':'QoRTs: Strand Test', 
         'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads', 
         'cpswitch_c_active':False}
        self.add_section(name='Strandedness',
          description='This plot shows the rate at which reads appear to follow different library-type strandedness rules.',
          helptext='\n            From the [QoRTs vignette](http://hartleys.github.io/QoRTs/doc/QoRTs-vignette.pdf):\n\n            This plot is used to detect whether your data is indeed stranded, and whether you are using the correct\n            stranded data library type option. For unstranded libraries, one would expect close to 50-50\n            First Strand - Second Strand. For stranded libraries, all points should fall closer to 99% one or the other.\n            ',
          plot=(bargraph.plot(self.qorts_data, cats, pconfig)))