# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/bowtie2/bowtie2.py
# Compiled at: 2019-11-20 06:36:41
# Size of source mod 2**32: 12584 bytes
""" MultiQC module to parse output from Bowtie 2 """
from __future__ import print_function
from collections import OrderedDict
import logging, re
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' Bowtie 2 module, parses stderr logs. '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Bowtie 2 / HiSAT2', anchor='bowtie2', target='',
          info='<a href="http://bowtie-bio.sourceforge.net/bowtie2/">Bowtie 2</a>\n                and <a href="https://ccb.jhu.edu/software/hisat2/">HISAT2</a> are fast\n                and memory-efficient tools for aligning sequencing reads against a reference genome.\n                Unfortunately both tools have identical log output by default, so it is impossible\n                to distiguish which tool was used.\n                ')
        self.bowtie2_data = dict()
        self.num_se = 0
        self.num_pe = 0
        for f in self.find_log_files('bowtie2', filehandles=True):
            self.parse_bowtie2_logs(f)

        self.bowtie2_data = self.ignore_samples(self.bowtie2_data)
        if len(self.bowtie2_data) == 0:
            raise UserWarning
        log.info('Found {} reports'.format(len(self.bowtie2_data)))
        self.write_data_file(self.bowtie2_data, 'multiqc_bowtie2')
        self.bowtie2_general_stats_table()
        self.bowtie2_alignment_plot()

    def parse_bowtie2_logs(self, f):
        """
        Warning: This function may make you want to stab yourself.

        Parse logs from bowtie2. These miss several key bits of information
        such as input files, so we try to look for logs from other wrapper tools
        that may have logged this info. If not found, we default to using the filename.
        Note that concatenated logs only parse if we have the command printed in there.

        The bowtie log uses the same strings mulitple times in different contexts to mean
        different things, making parsing very messy. Handle with care.

        Example single-end output from bowtie2:
            Time loading reference: 00:00:08
            Time loading forward index: 00:00:16
            Time loading mirror index: 00:00:09
            [samopen] SAM header is present: 25 sequences.
            Multiseed full-index search: 00:58:04
            38377305 reads; of these:
              38377305 (100.00%) were unpaired; of these:
                2525577 (6.58%) aligned 0 times
                27593593 (71.90%) aligned exactly 1 time
                8258135 (21.52%) aligned >1 times
            93.42% overall alignment rate
            Time searching: 00:58:37
            Overall time: 00:58:37

        Example paired-end output from bowtie2:
            Time loading reference: 00:01:07
            Time loading forward index: 00:00:26
            Time loading mirror index: 00:00:09
            Multiseed full-index search: 01:32:55
            15066949 reads; of these:
              15066949 (100.00%) were paired; of these:
                516325 (3.43%) aligned concordantly 0 times
                11294617 (74.96%) aligned concordantly exactly 1 time
                3256007 (21.61%) aligned concordantly >1 times
                ----
                516325 pairs aligned concordantly 0 times; of these:
                  26692 (5.17%) aligned discordantly 1 time
                ----
                489633 pairs aligned 0 times concordantly or discordantly; of these:
                  979266 mates make up the pairs; of these:
                    592900 (60.55%) aligned 0 times
                    209206 (21.36%) aligned exactly 1 time
                    177160 (18.09%) aligned >1 times
            98.03% overall alignment rate
            Time searching: 01:34:37
            Overall time: 01:34:37
        """
        regexes = {'unpaired':{'unpaired_aligned_none':'(\\d+) \\([\\d\\.]+%\\) aligned 0 times', 
          'unpaired_aligned_one':'(\\d+) \\([\\d\\.]+%\\) aligned exactly 1 time', 
          'unpaired_aligned_multi':'(\\d+) \\([\\d\\.]+%\\) aligned >1 times'}, 
         'paired':{'paired_aligned_none':'(\\d+) \\([\\d\\.]+%\\) aligned concordantly 0 times', 
          'paired_aligned_one':'(\\d+) \\([\\d\\.]+%\\) aligned concordantly exactly 1 time', 
          'paired_aligned_multi':'(\\d+) \\([\\d\\.]+%\\) aligned concordantly >1 times', 
          'paired_aligned_discord_one':'(\\d+) \\([\\d\\.]+%\\) aligned discordantly 1 time', 
          'paired_aligned_discord_multi':'(\\d+) \\([\\d\\.]+%\\) aligned discordantly >1 times', 
          'paired_aligned_mate_one':'(\\d+) \\([\\d\\.]+%\\) aligned exactly 1 time', 
          'paired_aligned_mate_multi':'(\\d+) \\([\\d\\.]+%\\) aligned >1 times', 
          'paired_aligned_mate_none':'(\\d+) \\([\\d\\.]+%\\) aligned 0 times'}}
        s_name = f['s_name']
        parsed_data = {}
        for l in f['f']:
            btcmd = re.search('bowtie2 .+ -[1U] ([^\\s,]+)', l)
            if btcmd:
                s_name = self.clean_s_name(btcmd.group(1), f['root'])
                log.debug("Found a bowtie2 command, updating sample name to '{}'".format(s_name))
            total = re.search('(\\d+) reads; of these:', l)
            if total:
                parsed_data['total_reads'] = int(total.group(1))
            unpaired = re.search('(\\d+) \\([\\d\\.]+%\\) were unpaired; of these:', l)
            if unpaired:
                parsed_data['unpaired_total'] = int(unpaired.group(1))
                self.num_se += 1
                l = f['f'].readline()
                while l.startswith('    '):
                    for k, r in regexes['unpaired'].items():
                        match = re.search(r, l)
                        if match:
                            parsed_data[k] = int(match.group(1))

                    l = f['f'].readline()

            paired = re.search('(\\d+) \\([\\d\\.]+%\\) were paired; of these:', l)
            if paired:
                parsed_data['paired_total'] = int(paired.group(1))
                self.num_pe += 1
                l = f['f'].readline()
                while l.startswith('    '):
                    for k, r in regexes['paired'].items():
                        match = re.search(r, l)
                        if match:
                            parsed_data[k] = int(match.group(1))

                    l = f['f'].readline()

            overall = re.search('([\\d\\.]+)% overall alignment rate', l)
            if overall:
                parsed_data['overall_alignment_rate'] = float(overall.group(1))
                m_keys = [
                 'paired_aligned_mate_multi', 'paired_aligned_mate_none', 'paired_aligned_mate_one']
                for k in m_keys:
                    if k in parsed_data:
                        parsed_data['{}_halved'.format(k)] = float(parsed_data[k]) / 2.0

                if s_name in self.bowtie2_data:
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
                self.add_data_source(f, s_name)
                self.bowtie2_data[s_name] = parsed_data
                s_name = f['s_name']
                parsed_data = {}

    def bowtie2_general_stats_table(self):
        """ Take the parsed stats from the Bowtie 2 report and add it to the
        basic stats table at the top of the report """
        headers = OrderedDict()
        headers['overall_alignment_rate'] = {'title':'% Aligned', 
         'description':'overall alignment rate', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'YlGn'}
        self.general_stats_addcols(self.bowtie2_data, headers)

    def bowtie2_alignment_plot(self):
        """ Make the HighCharts HTML to plot the alignment rates """
        half_warning = ''
        for s_name in self.bowtie2_data:
            if 'paired_aligned_mate_one_halved' in self.bowtie2_data[s_name] or 'paired_aligned_mate_multi_halved' in self.bowtie2_data[s_name] or 'paired_aligned_mate_none_halved' in self.bowtie2_data[s_name]:
                half_warning = '\n                <div class="alert alert-warning">Please note that single mate alignment counts are halved to tally with pair counts properly.</div>\n                '

        description_text = 'This plot shows the number of reads aligning to the reference in different ways.'
        config = {'ylab':'# Reads', 
         'cpswitch_counts_label':'Number of Reads'}
        if self.num_se > 0:
            sekeys = OrderedDict()
            sekeys['unpaired_aligned_one'] = {'color':'#20568f',  'name':'SE mapped uniquely'}
            sekeys['unpaired_aligned_multi'] = {'color':'#f7a35c',  'name':'SE multimapped'}
            sekeys['unpaired_aligned_none'] = {'color':'#981919',  'name':'SE not aligned'}
            config['id'] = 'bowtie2_se_plot'
            config['title'] = 'Bowtie 2: SE Alignment Scores'
            self.add_section(name='Single-end alignments',
              anchor='bowtie2-align-se',
              description=description_text,
              helptext='\n                There are 3 possible types of alignment:\n\n                * **SE mapped uniquely**: Read has only one occurence in the reference genome.\n                * **SE multimapped**: Read has multiple occurence.\n                * **SE not aligned**: Read has no occurence.\n                ',
              plot=(bargraph.plot(self.bowtie2_data, sekeys, config)))
        if self.num_pe > 0:
            pekeys = OrderedDict()
            pekeys['paired_aligned_one'] = {'color':'#20568f',  'name':'PE mapped uniquely'}
            pekeys['paired_aligned_discord_one'] = {'color':'#5c94ca',  'name':'PE mapped discordantly uniquely'}
            pekeys['paired_aligned_mate_one_halved'] = {'color':'#95ceff',  'name':'PE one mate mapped uniquely'}
            pekeys['paired_aligned_multi'] = {'color':'#f7a35c',  'name':'PE multimapped'}
            pekeys['paired_aligned_discord_multi'] = {'color':'#dce333',  'name':'PE discordantly multimapped'}
            pekeys['paired_aligned_mate_multi_halved'] = {'color':'#ffeb75',  'name':'PE one mate multimapped'}
            pekeys['paired_aligned_mate_none_halved'] = {'color':'#981919',  'name':'PE neither mate aligned'}
            config['id'] = 'bowtie2_pe_plot'
            config['title'] = 'Bowtie 2: PE Alignment Scores'
            self.add_section(name='Paired-end alignments',
              anchor='bowtie2-align-pe',
              description=(description_text + half_warning),
              helptext='\n                There are 6 possible types of alignment:\n\n                * **PE mapped uniquely**: Pair has only one occurence in the reference genome.\n                * **PE mapped discordantly uniquely**: Pair has only one occurence but not in proper pair.\n                * **PE one mate mapped uniquely**: One read of a pair has one occurence.\n                * **PE multimapped**: Pair has multiple occurence.\n                * **PE one mate multimapped**: One read of a pair has multiple occurence.\n                * **PE neither mate aligned**: Pair has no occurence.\n                ',
              plot=(bargraph.plot(self.bowtie2_data, pekeys, config)))