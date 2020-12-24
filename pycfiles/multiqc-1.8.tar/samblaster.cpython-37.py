# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/samblaster/samblaster.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 4000 bytes
""" MultiQC module to parse output from Samblaster """
from __future__ import print_function
import os
from collections import OrderedDict
import logging, re
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' Samblaster '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Samblaster', anchor='samblaster', href='https://github.com/GregoryFaust/samblaster',
          info='is a tool to mark duplicates and extract discordant and split reads from sam files.')
        self.samblaster_data = dict()
        for f in self.find_log_files('samblaster', filehandles=True):
            self.parse_samblaster(f)

        self.samblaster_data = self.ignore_samples(self.samblaster_data)
        if len(self.samblaster_data) == 0:
            raise UserWarning
        headers = OrderedDict()
        headers['pct_dups'] = {'title':'% Dups', 
         'description':'Percent Duplication', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'OrRd'}
        self.general_stats_addcols(self.samblaster_data, headers)
        self.write_data_file(self.samblaster_data, 'multiqc_samblaster')
        log.info('Found {} reports'.format(len(self.samblaster_data)))
        self.add_barplot()

    def add_barplot(self):
        """ Generate the Samblaster bar plot. """
        cats = OrderedDict()
        cats['n_nondups'] = {'name': 'Non-duplicates'}
        cats['n_dups'] = {'name': 'Duplicates'}
        pconfig = {'id':'samblaster_duplicates', 
         'title':'Samblaster: Number of duplicate reads', 
         'ylab':'Number of reads'}
        self.add_section(plot=(bargraph.plot(self.samblaster_data, cats, pconfig)))

    def parse_samblaster(self, f):
        """ Go through log file looking for samblaster output.
        If the
        Grab the name from the RG tag of the preceding bwa command """
        dups_regex = 'samblaster: (Removed|Marked) (\\d+) of (\\d+) \\((\\d+.\\d+)%\\) read ids as duplicates'
        input_file_regex = 'samblaster: Opening (\\S+) for read.'
        rgtag_name_regex = '\\\\tID:(\\S*?)\\\\t'
        data = {}
        s_name = None
        fh = f['f']
        for l in fh:
            match = re.search(rgtag_name_regex, l)
            if match:
                s_name = self.clean_s_name(match.group(1), f['root'])
            match = re.search(input_file_regex, l)
            if match:
                basefn = os.path.basename(match.group(1))
                fname, ext = os.path.splitext(basefn)
                if fname != 'stdin':
                    s_name = self.clean_s_name(fname, f['root'])
            match = re.search(dups_regex, l)
            if match:
                data['n_dups'] = int(match.group(2))
                data['n_tot'] = int(match.group(3))
                data['n_nondups'] = data['n_tot'] - data['n_dups']
                data['pct_dups'] = float(match.group(4))

        if s_name is None:
            s_name = f['s_name']
        if len(data) > 0:
            if s_name in self.samblaster_data:
                log.debug('Duplicate sample name found in {}! Overwriting: {}'.format(f['fn'], s_name))
            self.add_data_source(f, s_name)
            self.samblaster_data[s_name] = data