# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/rseqc/bam_stat.py
# Compiled at: 2017-09-23 10:30:24
""" MultiQC submodule to parse output from RSeQC bam_stat.py
http://rseqc.sourceforge.net/#bam-stat-py """
from collections import OrderedDict
import logging, re
from multiqc.plots import beeswarm
log = logging.getLogger(__name__)

def parse_reports(self):
    """ Find RSeQC bam_stat reports and parse their data """
    self.bam_stat_data = dict()
    regexes = {'total_records': 'Total records:\\s*(\\d+)', 
       'qc_failed': 'QC failed:\\s*(\\d+)', 
       'optical_pcr_duplicate': 'Optical/PCR duplicate:\\s*(\\d+)', 
       'non_primary_hits': 'Non primary hits\\s*(\\d+)', 
       'unmapped_reads': 'Unmapped reads:\\s*(\\d+)', 
       'mapq_lt_mapq_cut_non-unique': 'mapq < mapq_cut \\(non-unique\\):\\s*(\\d+)', 
       'mapq_gte_mapq_cut_unique': 'mapq >= mapq_cut \\(unique\\):\\s*(\\d+)', 
       'read_1': 'Read-1:\\s*(\\d+)', 
       'read_2': 'Read-2:\\s*(\\d+)', 
       'reads_map_to_sense': "Reads map to '\\+':\\s*(\\d+)", 
       'reads_map_to_antisense': "Reads map to '-':\\s*(\\d+)", 
       'non-splice_reads': 'Non-splice reads:\\s*(\\d+)', 
       'splice_reads': 'Splice reads:\\s*(\\d+)', 
       'reads_mapped_in_proper_pairs': 'Reads mapped in proper pairs:\\s*(\\d+)', 
       'proper-paired_reads_map_to_different_chrom': 'Proper-paired reads map to different chrom:\\s*(\\d+)'}
    is_paired_end = False
    for f in self.find_log_files('rseqc/bam_stat'):
        d = dict()
        for k, r in regexes.items():
            r_search = re.search(r, f['f'], re.MULTILINE)
            if r_search:
                d[k] = int(r_search.group(1))

        if 'total_records' in d:
            t = float(d['total_records'])
            if 'mapq_gte_mapq_cut_unique' in d:
                d['unique_percent'] = float(d['mapq_gte_mapq_cut_unique']) / t * 100.0
            if 'reads_mapped_in_proper_pairs' in d:
                d['proper_pairs_percent'] = float(d['reads_mapped_in_proper_pairs']) / t * 100.0
        if len(d) > 0:
            if f['s_name'] in self.bam_stat_data:
                log.debug(('Duplicate sample name found! Overwriting: {}').format(f['s_name']))
            self.add_data_source(f, section='bam_stat')
            if d['read_2'] != 0:
                is_paired_end = True
            self.bam_stat_data[f['s_name']] = d

    self.bam_stat_data = self.ignore_samples(self.bam_stat_data)
    if len(self.bam_stat_data) > 0:
        self.write_data_file(self.bam_stat_data, 'multiqc_rseqc_bam_stat')
        self.general_stats_headers['proper_pairs_percent'] = {'title': '% Proper Pairs', 
           'description': '% Reads mapped in proper pairs', 
           'max': 100, 
           'min': 0, 
           'suffix': '%', 
           'scale': 'RdYlGn'}
        for s_name in self.bam_stat_data:
            if s_name not in self.general_stats_data:
                self.general_stats_data[s_name] = dict()
                if is_paired_end:
                    self.general_stats_data[s_name].update(self.bam_stat_data[s_name])

        pconfig = {'id': 'rseqc_bam_stat'}
        keys = OrderedDict()
        defaults = {'min': 0, 
           'shared_key': 'read_count', 
           'decimalPlaces': 2, 
           'modify': lambda x: float(x) / 1000000.0}
        keys['total_records'] = dict(defaults, **{'title': 'Total records'})
        keys['qc_failed'] = dict(defaults, **{'title': 'QC failed'})
        keys['optical_pcr_duplicate'] = dict(defaults, **{'title': 'Duplicates', 'description': 'Optical/PCR duplicate'})
        keys['non_primary_hits'] = dict(defaults, **{'title': 'Non primary hit'})
        keys['unmapped_reads'] = dict(defaults, **{'title': 'Unmapped', 'description': 'Unmapped reads'})
        keys['mapq_lt_mapq_cut_non'] = dict(defaults, **{'title': 'Non-unique', 'description': 'mapq < mapq_cut (non-unique)'})
        keys['mapq_gte_mapq_cut_unique'] = dict(defaults, **{'title': 'Unique', 'description': 'mapq >= mapq_cut (unique)'})
        if is_paired_end:
            keys['read_1'] = dict(defaults, **{'title': 'Read-1'})
            keys['read_2'] = dict(defaults, **{'title': 'Read-2'})
        keys['reads_map_to_sense'] = dict(defaults, **{'title': '+ve strand', 'description': "Reads map to '+'"})
        keys['reads_map_to_antisense'] = dict(defaults, **{'title': '-ve strand', 'description': "Reads map to '-'"})
        keys['non-splice_reads'] = dict(defaults, **{'title': 'Non-splice reads'})
        keys['splice_reads'] = dict(defaults, **{'title': 'Splice reads'})
        if is_paired_end:
            keys['reads_mapped_in_proper_pairs'] = dict(defaults, **{'title': 'Proper pairs', 
               'description': 'Reads mapped in proper pairs'})
            keys['proper-paired_reads_map_to_different_chrom'] = dict(defaults, **{'title': 'Different chrom', 
               'description': 'Proper-paired reads map to different chrom'})
        self.add_section(name='Bam Stat', anchor='rseqc-bam_stat', description='All numbers reported in millions.', plot=beeswarm.plot(self.bam_stat_data, keys, pconfig))
    return len(self.bam_stat_data)