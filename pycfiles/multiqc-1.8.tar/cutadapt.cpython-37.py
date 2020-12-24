# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/cutadapt/cutadapt.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 8542 bytes
""" MultiQC module to parse output from Cutadapt """
from __future__ import print_function
import logging, re
from distutils.version import StrictVersion
from multiqc.plots import linegraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = '\n    Cutadapt module class, parses stderr logs.\n    Also understands logs saved by Trim Galore!\n    (which contain cutadapt logs)\n    '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Cutadapt', anchor='cutadapt', href='https://cutadapt.readthedocs.io/',
          info='is a tool to find and remove adapter sequences, primers, poly-Atails and other types of unwanted sequence from your high-throughput sequencing reads.')
        self.cutadapt_data = dict()
        self.cutadapt_length_counts = dict()
        self.cutadapt_length_exp = dict()
        self.cutadapt_length_obsexp = dict()
        for f in self.find_log_files('cutadapt', filehandles=True):
            self.parse_cutadapt_logs(f)

        self.cutadapt_data = self.ignore_samples(self.cutadapt_data)
        if len(self.cutadapt_data) == 0:
            raise UserWarning
        log.info('Found {} reports'.format(len(self.cutadapt_data)))
        self.write_data_file(self.cutadapt_data, 'multiqc_cutadapt')
        self.cutadapt_general_stats_table()
        self.cutadapt_length_trimmed_plot()

    def parse_cutadapt_logs(self, f):
        """ Go through log file looking for cutadapt output """
        fh = f['f']
        regexes = {'1.7':{'bp_processed':'Total basepairs processed:\\s*([\\d,]+) bp', 
          'bp_written':'Total written \\(filtered\\):\\s*([\\d,]+) bp', 
          'quality_trimmed':'Quality-trimmed:\\s*([\\d,]+) bp', 
          'r_processed':'Total reads processed:\\s*([\\d,]+)', 
          'r_with_adapters':'Reads with adapters:\\s*([\\d,]+)'}, 
         '1.6':{'r_processed':'Processed reads:\\s*([\\d,]+)', 
          'bp_processed':'Processed bases:\\s*([\\d,]+) bp', 
          'r_trimmed':'Trimmed reads:\\s*([\\d,]+)', 
          'quality_trimmed':'Quality-trimmed:\\s*([\\d,]+) bp', 
          'bp_trimmed':'Trimmed bases:\\s*([\\d,]+) bp', 
          'too_short':'Too short reads:\\s*([\\d,]+)', 
          'too_long':'Too long reads:\\s*([\\d,]+)'}}
        s_name = None
        cutadapt_version = '1.7'
        log_section = None
        for l in fh:
            if 'cutadapt' in l:
                s_name = None
                c_version = re.match('This is cutadapt ([\\d\\.]+)', l)
                if c_version:
                    try:
                        assert StrictVersion(c_version.group(1)) <= StrictVersion('1.6')
                        cutadapt_version = '1.6'
                    except:
                        cutadapt_version = '1.7'

                else:
                    c_version_old = re.match('cutadapt version ([\\d\\.]+)', l)
                    if c_version_old:
                        try:
                            assert StrictVersion(c_version.group(1)) <= StrictVersion('1.6')
                            cutadapt_version = '1.6'
                        except:
                            cutadapt_version = '1.6'

                        if l.startswith('Command line parameters'):
                            s_name = l.split()[(-1)]
                            if s_name == '-':
                                s_name = f['s_name']
                    else:
                        s_name = self.clean_s_name(s_name, f['root'])
                    if s_name in self.cutadapt_data:
                        log.debug('Duplicate sample name found! Overwriting: {}'.format(s_name))
                    self.cutadapt_data[s_name] = dict()
                if s_name is not None:
                    self.add_data_source(f, s_name)
                    for k, r in regexes[cutadapt_version].items():
                        match = re.search(r, l)
                        if match:
                            self.cutadapt_data[s_name][k] = int(match.group(1).replace(',', ''))

                    if '===' in l:
                        log_section = l.strip().strip('=').strip()
                    if 'length' in l:
                        if 'count' in l and 'expect' in l:
                            plot_sname = s_name
                            if log_section is not None:
                                plot_sname = '{} - {}'.format(s_name, log_section)
                        self.cutadapt_length_counts[plot_sname] = dict()
                        self.cutadapt_length_exp[plot_sname] = dict()
                        self.cutadapt_length_obsexp[plot_sname] = dict()
                        for l in fh:
                            r_seqs = re.search('^(\\d+)\\s+(\\d+)\\s+([\\d\\.]+)', l)
                            if r_seqs:
                                a_len = int(r_seqs.group(1))
                                self.cutadapt_length_counts[plot_sname][a_len] = int(r_seqs.group(2))
                                self.cutadapt_length_exp[plot_sname][a_len] = float(r_seqs.group(3))
                                if float(r_seqs.group(3)) > 0:
                                    self.cutadapt_length_obsexp[plot_sname][a_len] = float(r_seqs.group(2)) / float(r_seqs.group(3))
                                else:
                                    self.cutadapt_length_obsexp[plot_sname][a_len] = float(r_seqs.group(2))
                            else:
                                break

        for s_name, d in self.cutadapt_data.items():
            if 'bp_processed' in d:
                if 'bp_written' in d:
                    self.cutadapt_data[s_name]['percent_trimmed'] = float(d['bp_processed'] - d['bp_written']) / d['bp_processed'] * 100
            if 'bp_processed' in d and 'bp_trimmed' in d:
                self.cutadapt_data[s_name]['percent_trimmed'] = (float(d.get('bp_trimmed', 0)) + float(d.get('quality_trimmed', 0))) / d['bp_processed'] * 100

    def cutadapt_general_stats_table(self):
        """ Take the parsed stats from the Cutadapt report and add it to the
        basic stats table at the top of the report """
        headers = {}
        headers['percent_trimmed'] = {'title':'% Trimmed', 
         'description':'% Total Base Pairs trimmed', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'RdYlBu-rev'}
        self.general_stats_addcols(self.cutadapt_data, headers)

    def cutadapt_length_trimmed_plot(self):
        """ Generate the trimming length plot """
        description = 'This plot shows the number of reads with certain lengths of adapter trimmed. \n        Obs/Exp shows the raw counts divided by the number expected due to sequencing errors. A defined peak \n        may be related to adapter length. See the \n        <a href="http://cutadapt.readthedocs.org/en/latest/guide.html#how-to-read-the-report" target="_blank">cutadapt documentation</a> \n        for more information on how these numbers are generated.'
        pconfig = {'id':'cutadapt_plot', 
         'title':'Cutadapt: Lengths of Trimmed Sequences', 
         'ylab':'Counts', 
         'xlab':'Length Trimmed (bp)', 
         'xDecimals':False, 
         'ymin':0, 
         'tt_label':'<b>{point.x} bp trimmed</b>: {point.y:.0f}', 
         'data_labels':[
          {'name':'Counts', 
           'ylab':'Count'},
          {'name':'Obs/Exp', 
           'ylab':'Observed / Expected'}]}
        self.add_section(description=description,
          plot=(linegraph.plot([self.cutadapt_length_counts, self.cutadapt_length_obsexp], pconfig)))