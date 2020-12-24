# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/mirtrace/mirtrace.py
# Compiled at: 2019-11-13 05:22:42
""" MultiQC module to parse output files from miRTrace """
from __future__ import print_function
from collections import OrderedDict
import logging, json
from multiqc.plots import bargraph, linegraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='miRTrace', anchor='mirtrace', href='https://github.com/friedlanderlab/mirtrace', info='is a quality control software for small RNA sequencing data developed by Friedländer lab (KTH, Sweden).')
        self.summary_data = dict()
        for f in self.find_log_files('mirtrace/summary'):
            self.parse_summary(f)

        self.length_data = dict()
        for f in self.find_log_files('mirtrace/length'):
            self.parse_length(f)

        self.contamination_data = dict()
        for f in self.find_log_files('mirtrace/contaminationbasic'):
            self.parse_contamination(f)

        self.complexity_data = dict()
        for f in self.find_log_files('mirtrace/mirnacomplexity'):
            self.parse_complexity(f)

        self.summary_data = self.ignore_samples(self.summary_data)
        self.length_data = self.ignore_samples(self.length_data)
        self.contamination_data = self.ignore_samples(self.contamination_data)
        self.complexity_data = self.ignore_samples(self.complexity_data)
        if max(len(self.summary_data), len(self.length_data), len(self.contamination_data), len(self.complexity_data)) == 0:
            raise UserWarning
        self.write_data_file(self.summary_data, 'multiqc_mirtrace_summary')
        self.write_data_file(self.length_data, 'multiqc_mirtrace_length')
        self.write_data_file(self.contamination_data, 'multiqc_mirtrace_contamination')
        self.write_data_file(self.complexity_data, 'multiqc_mirtrace_complexity')
        if len(self.summary_data) > 0:
            self.add_section(name='QC Plot', anchor='mirtrace_qc', plot=self.mirtrace_qc_plot())
            self.add_section(name='RNA Categories', anchor='mirtrace_rna_categories', plot=self.mirtrace_rna_categories())
        if len(self.length_data) > 0:
            self.add_section(name='Read Length Distribution', anchor='mirtrace_length', plot=self.mirtrace_length_plot())
        if len(self.contamination_data) > 0:
            self.add_section(name='Contamination Check', anchor='mirtrace_contamination_check', plot=self.mirtrace_contamination_check())
        if len(self.complexity_data) > 0:
            self.add_section(name='miRNA Complexity', anchor='mirtrace_complexity', plot=self.mirtrace_complexity_plot())

    def parse_summary(self, f):
        try:
            cdict = json.loads(f['f'])
        except ValueError as e:
            raise e

        if 'results' in cdict.keys():
            for record in cdict['results']:
                s_name = self.clean_s_name(record['verbosename'], f['root'])
                parsed_data = {}
                parsed_data['filename'] = record['filename']
                parsed_data['reads_total'] = record['stats']['allSeqsCount']
                parsed_data['adapter_removed_length_ok'] = record['stats']['statsQC'][4]
                parsed_data['adapter_not_detected'] = record['stats']['statsQC'][3]
                parsed_data['length_shorter_than_18'] = record['stats']['statsQC'][2]
                parsed_data['low_complexity'] = record['stats']['statsQC'][1]
                parsed_data['low_phred'] = record['stats']['statsQC'][0]
                parsed_data['reads_mirna'] = record['stats']['statsRNAType'][0]
                parsed_data['reads_rrna'] = record['stats']['statsRNAType'][1]
                parsed_data['reads_trna'] = record['stats']['statsRNAType'][2]
                parsed_data['reads_artifact'] = record['stats']['statsRNAType'][3]
                parsed_data['reads_unknown'] = record['stats']['statsRNAType'][4]
                if s_name in self.summary_data:
                    log.debug(('Duplicate sample name found! Overwriting: {}').format(s_name))
                self.add_data_source(f, s_name)
                self.summary_data[s_name] = parsed_data

        else:
            log.debug(('No valid data {} in miRTrace summary').format(f['fn']))
            return
        return

    def parse_length(self, f):
        header = []
        body = {}
        lines = f['f'].splitlines()
        for l in lines:
            s = l.split('\t')
            if len(header) == 0:
                if s[0] != 'LENGTH':
                    log.debug(('No valid data {} for read length distribution').format(f['fn']))
                    return
                header = s[1:]
            else:
                body[s[0]] = s[1:len(s)]

        for record in header[0:len(header)]:
            s_name = self.clean_s_name(record, f['root'])
            parsed_data = {}
            idx = header[0:len(header)].index(record)
            for length in body:
                parsed_data[length] = int(body[length][idx])

            if s_name in self.length_data:
                log.debug(('Duplicate sample name found! Overwriting: {}').format(s_name))
            self.add_data_source(f, s_name)
            self.length_data[s_name] = parsed_data

        return

    def parse_contamination(self, f):
        header = []
        body = {}
        lines = f['f'].splitlines()
        for l in lines:
            s = l.split('\t')
            if len(header) == 0:
                if s[0] != 'CLADE':
                    log.debug(('No valid data {} for contamination check').format(f['fn']))
                    return
                header = s[1:]
            else:
                body[s[0]] = s[1:len(s)]

        for record in header[0:len(header)]:
            s_name = self.clean_s_name(record, f['root'])
            parsed_data = {}
            idx = header[0:len(header)].index(record)
            for clade in body:
                parsed_data[clade] = int(body[clade][idx])

            if s_name in self.contamination_data:
                log.debug(('Duplicate sample name found! Overwriting: {}').format(s_name))
            self.add_data_source(f, s_name)
            self.contamination_data[s_name] = parsed_data

        return

    def parse_complexity(self, f):
        header = []
        body = {}
        lines = f['f'].splitlines()
        for l in lines:
            s = l.split('\t')
            if len(header) == 0:
                if s[0] != 'DISTINCT_MIRNA_HAIRPINS_ACCUMULATED_COUNT':
                    log.debug(('No valid data {} for miRNA complexity').format(f['fn']))
                    return
                header = s[1:]
            else:
                body[s[0]] = s[1:len(s)]

        for record in header[0:len(header)]:
            s_name = self.clean_s_name(record, f['root'])
            parsed_data = {}
            idx = header[0:len(header)].index(record)
            for depth in body:
                parsed_data[depth] = int(body[depth][idx]) if body[depth][idx] else 0

            if s_name in self.complexity_data:
                log.debug(('Duplicate sample name found! Overwriting: {}').format(s_name))
            self.add_data_source(f, s_name)
            self.complexity_data[s_name] = parsed_data

        return

    def mirtrace_qc_plot(self):
        """ Generate the miRTrace QC Plot"""
        keys = OrderedDict()
        keys['adapter_removed_length_ok'] = {'color': '#006837', 'name': 'Reads ≥ 18 nt after adapter removal'}
        keys['adapter_not_detected'] = {'color': '#66bd63', 'name': 'Reads without adapter'}
        keys['length_shorter_than_18'] = {'color': '#fdae61', 'name': 'Reads < 18 nt after adapter removal'}
        keys['low_complexity'] = {'color': '#d73027', 'name': 'Reads with low complexity'}
        keys['low_phred'] = {'color': '#a50026', 'name': 'Reads with low PHRED score'}
        config = {'id': 'mirtrace_qc_plot', 
           'title': 'miRTrace: QC Plot', 
           'ylab': '# Reads', 
           'cpswitch_counts_label': 'Number of Reads'}
        return bargraph.plot(self.summary_data, keys, config)

    def mirtrace_length_plot(self):
        """ Generate the miRTrace Read Length Distribution"""
        data = dict()
        for s_name in self.length_data:
            try:
                data[s_name] = {int(d):int(self.length_data[s_name][d]) for d in self.length_data[s_name]}
            except KeyError:
                pass

        if len(data) == 0:
            log.debug('No valid data for read length distribution')
            return None
        else:
            config = {'id': 'mirtrace_length_plot', 
               'title': 'miRTrace: Read Length Distribution', 
               'ylab': 'Read Count', 
               'xlab': 'Read Lenth (bp)', 
               'ymin': 0, 
               'xmin': 0, 
               'xDecimals': False, 
               'tt_label': '<b>Read Length (bp) {point.x}</b>: {point.y} Read Count', 
               'xPlotBands': [{'from': 40, 'to': 50, 'color': '#ffebd1'}, {'from': 26, 'to': 40, 'color': '#e2f5ff'}, {'from': 18, 'to': 26, 'color': '#e5fce0'}, {'from': 0, 'to': 18, 'color': '#ffffe2'}]}
            return linegraph.plot(data, config)

    def mirtrace_rna_categories(self):
        """ Generate the miRTrace RNA Categories"""
        keys = OrderedDict()
        keys['reads_mirna'] = {'color': '#33a02c', 'name': 'miRNA'}
        keys['reads_rrna'] = {'color': '#ff7f00', 'name': 'rRNA'}
        keys['reads_trna'] = {'color': '#1f78b4', 'name': 'tRNA'}
        keys['reads_artifact'] = {'color': '#fb9a99', 'name': 'Artifact'}
        keys['reads_unknown'] = {'color': '#d9d9d9', 'name': 'Unknown'}
        config = {'id': 'mirtrace_rna_categories_plot', 
           'title': 'miRTrace: RNA Categories', 
           'ylab': '# Reads', 
           'cpswitch_counts_label': 'Number of Reads'}
        return bargraph.plot(self.summary_data, keys, config)

    def mirtrace_contamination_check(self):
        """ Generate the miRTrace Contamination Check"""
        color_lib = [
         'rgb(166,206,227)', 'rgb(31,120,180)', 'rgb(178,223,138)', 'rgb(51,160,44)', 'rgb(251,154,153)', 'rgb(227,26,28)', 'rgb(253,191,111)', 'rgb(255,127,0)', 'rgb(202,178,214)', 'rgb(106,61,154)', 'rgb(255,255,153)', 'rgb(177,89,40)', 'rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)', 'rgb(253,180,98)', 'rgb(179,222,105)', 'rgb(252,205,229)', 'rgb(217,217,217)', 'rgb(188,128,189)', 'rgb(204,235,197)', 'rgb(255,237,111)']
        idx = 0
        keys = OrderedDict()
        for clade in self.contamination_data[list(self.contamination_data.keys())[0]]:
            keys[clade] = {'color': color_lib[idx], 'name': clade}
            if idx < 23:
                idx += 1
            else:
                idx = 0

        config = {'cpswitch_c_active': False, 
           'id': 'mirtrace_contamination_check_plot', 
           'title': 'miRTrace: Contamination Check', 
           'ylab': '# miRNA detected', 
           'cpswitch_counts_label': 'Number of detected miRNA'}
        return bargraph.plot(self.contamination_data, keys, config)

    def mirtrace_complexity_plot(self):
        """ Generate the miRTrace miRNA Complexity Plot"""
        data = dict()
        for s_name in self.complexity_data:
            try:
                data[s_name] = {int(self.complexity_data[s_name][d]):int(d) for d in self.complexity_data[s_name]}
            except KeyError:
                pass

        if len(data) == 0:
            log.debug('No valid data for miRNA complexity')
            return None
        else:
            config = {'id': 'mirtrace_complexity_plot', 
               'title': 'miRTrace: miRNA Complexity Plot', 
               'ylab': 'Distinct miRNA Count', 
               'xlab': 'Number of Sequencing Reads', 
               'ymin': 0, 
               'xmin': 1, 
               'xDecimals': False, 
               'tt_label': '<b>Number of Sequencing Reads {point.x}</b>: {point.y} Distinct miRNA Count'}
            return linegraph.plot(data, config)