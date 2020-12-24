# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/samtools/flagstat.py
# Compiled at: 2019-11-20 10:26:16
# Size of source mod 2**32: 6555 bytes
""" MultiQC submodule to parse output from Samtools flagstat """
import logging, re
from collections import OrderedDict
from multiqc import config
from multiqc.plots import beeswarm
log = logging.getLogger(__name__)

class FlagstatReportMixin:

    def parse_samtools_flagstats(self):
        """ Find Samtools flagstat logs and parse their data """
        self.samtools_flagstat = dict()
        for f in self.find_log_files('samtools/flagstat'):
            parsed_data = parse_single_report(f['f'])
            if len(parsed_data) > 0:
                if f['s_name'] in self.samtools_flagstat:
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(f['s_name']))
                self.add_data_source(f, section='flagstat')
                self.samtools_flagstat[f['s_name']] = parsed_data

        self.samtools_flagstat = self.ignore_samples(self.samtools_flagstat)
        if len(self.samtools_flagstat) > 0:
            self.write_data_file(self.samtools_flagstat, 'multiqc_samtools_flagstat')
            flagstats_headers = dict()
            flagstats_headers['mapped_passed'] = {'title':'{} Reads Mapped'.format(config.read_count_prefix), 
             'description':'Reads Mapped in the bam file ({})'.format(config.read_count_desc), 
             'min':0, 
             'modify':lambda x: x * config.read_count_multiplier, 
             'shared_key':'read_count', 
             'placement':100.0}
            self.general_stats_addcols(self.samtools_flagstat, flagstats_headers, 'Samtools Flagstat')
            keys = OrderedDict()
            reads = {'min':0, 
             'modify':lambda x: float(x) * config.read_count_multiplier, 
             'suffix':'{} reads'.format(config.read_count_prefix), 
             'decimalPlaces':2, 
             'shared_key':'read_count'}
            keys['flagstat_total'] = dict(reads, title='Total Reads')
            keys['total_passed'] = dict(reads, title='Total Passed QC')
            keys['mapped_passed'] = dict(reads, title='Mapped')
            if any(v.get('secondary_passed') for v in self.samtools_flagstat.values()):
                keys['secondary_passed'] = dict(reads, title='Secondary Alignments')
            if any(v.get('supplementary_passed') for v in self.samtools_flagstat.values()):
                keys['supplementary_passed'] = dict(reads, title='Supplementary Alignments')
            keys['duplicates_passed'] = dict(reads, title='Duplicates')
            keys['paired in sequencing_passed'] = dict(reads, title='Paired in Sequencing')
            keys['properly paired_passed'] = dict(reads, title='Properly Paired')
            keys['with itself and mate mapped_passed'] = dict(reads, title='Self and mate mapped', description='Reads with itself and mate mapped')
            keys['singletons_passed'] = dict(reads, title='Singletons')
            keys['with mate mapped to a different chr_passed'] = dict(reads, title='Mate mapped to diff chr', description='Mate mapped to different chromosome')
            keys['with mate mapped to a different chr (mapQ >= 5)_passed'] = dict(reads, title='Diff chr (mapQ >= 5)', description='Mate mapped to different chromosome (mapQ >= 5)')
            self.add_section(name='Samtools Flagstat',
              anchor='samtools-flagstat',
              description='This module parses the output from <code>samtools flagstat</code>. All numbers in millions.',
              plot=(beeswarm.plot(self.samtools_flagstat, keys, {'id': 'samtools-flagstat-dp'})))
        return len(self.samtools_flagstat)


flagstat_regexes = {'total':'(\\d+) \\+ (\\d+) in total \\(QC-passed reads \\+ QC-failed reads\\)', 
 'secondary':'(\\d+) \\+ (\\d+) secondary', 
 'supplementary':'(\\d+) \\+ (\\d+) supplementary', 
 'duplicates':'(\\d+) \\+ (\\d+) duplicates', 
 'mapped':'(\\d+) \\+ (\\d+) mapped \\((.+):(.+)\\)', 
 'paired in sequencing':'(\\d+) \\+ (\\d+) paired in sequencing', 
 'read1':'(\\d+) \\+ (\\d+) read1', 
 'read2':'(\\d+) \\+ (\\d+) read2', 
 'properly paired':'(\\d+) \\+ (\\d+) properly paired \\((.+):(.+)\\)', 
 'with itself and mate mapped':'(\\d+) \\+ (\\d+) with itself and mate mapped', 
 'singletons':'(\\d+) \\+ (\\d+) singletons \\((.+):(.+)\\)', 
 'with mate mapped to a different chr':'(\\d+) \\+ (\\d+) with mate mapped to a different chr', 
 'with mate mapped to a different chr (mapQ >= 5)':'(\\d+) \\+ (\\d+) with mate mapped to a different chr \\(mapQ>=5\\)'}

def parse_single_report(file_obj):
    """
    Take a filename, parse the data assuming it's a flagstat file
    Returns a dictionary {'lineName_pass' : value, 'lineName_fail' : value}
    """
    parsed_data = {}
    re_groups = [
     'passed', 'failed', 'passed_pct', 'failed_pct']
    for k, r in flagstat_regexes.items():
        r_search = re.search(r, file_obj, re.MULTILINE)
        if r_search:
            for i, j in enumerate(re_groups):
                try:
                    key = '{}_{}'.format(k, j)
                    val = r_search.group(i + 1).strip('% ')
                    parsed_data[key] = float(val) if '.' in val else int(val)
                except IndexError:
                    pass
                except ValueError:
                    parsed_data[key] = float('nan')

    try:
        parsed_data['flagstat_total'] = parsed_data['total_passed'] + parsed_data['total_failed']
    except KeyError:
        pass

    return parsed_data