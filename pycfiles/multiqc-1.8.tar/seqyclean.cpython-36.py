# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/seqyclean/seqyclean.py
# Compiled at: 2019-11-13 05:23:41
# Size of source mod 2**32: 5929 bytes
from __future__ import print_function
from collections import OrderedDict
import logging, re
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='SeqyClean',
          anchor='seqyclean',
          href='https://github.com/ibest/seqyclean',
          info='is a pre-processing tool for NGS data that filters adapters, vectors, and contaminants while quality trimming.')
        self.seqyclean_data = dict()
        for f in self.find_log_files('seqyclean'):
            rows = f['f'].splitlines()
            headers = rows[0].split('\t')
            cols = rows[1].split('\t')
            self.seqyclean_data[f['s_name']] = dict()
            for header, col in zip(headers, cols):
                try:
                    col = float(col)
                except (ValueError, TypeError):
                    pass

                self.seqyclean_data[f['s_name']].update({header: col})

        if len(self.seqyclean_data) == 0:
            raise UserWarning
        self.seqyclean_data = self.ignore_samples(self.seqyclean_data)
        log.info('Found {} logs'.format(len(self.seqyclean_data)))
        self.add_section(name='Summary',
          anchor='seqyclean-summary',
          description='This plot shows the number of reads that were kept and discarded.',
          plot=(self.seqyclean_summary()))
        self.add_section(name='Annotations',
          anchor='seqyclean-annotation',
          description='This plot shows how reads were annotated.',
          plot=(self.seqyclean_analysis()))
        self.add_section(name='Discarded',
          anchor='seqyclean-discarded',
          description='This plot shows the breakdown of reasons for why reads were discarded.',
          plot=(self.seqyclean_discarded()))
        self.write_data_file(self.seqyclean_data, 'multiqc_seqyclean')
        self.seqyclean_general_stats_table()

    def seqyclean_summary(self):
        config = {'id':'seqyclean-summary-plot', 
         'title':'SeqyClean: Summary', 
         'ylab':'Number of Reads'}
        keys = [
         'PairsKept',
         'PairsDiscarded',
         'PE1DiscardedTotal',
         'PE2DiscardedTotal',
         'SEReadsKept',
         'SEDiscardedTotal',
         'ReadsKept',
         'DiscardedTotal']
        return bargraph.plot(self.seqyclean_data, self._clean_keys(keys), config)

    def seqyclean_analysis(self):
        config = {'id':'seqyclean-read-annotation-plot', 
         'title':'SeqyClean: Read Annotations', 
         'ylab':'Number of Reads'}
        keys = [
         'PE1TruSeqAdap_found',
         'PE1ReadsWVector_found',
         'PE1ReadsWContam_found',
         'PE2TruSeqAdap_found',
         'PE2ReadsWVector_found',
         'PE2ReadsWContam_found',
         'SETruSeqAdap_found',
         'SEReadsWVector_found',
         'SEReadsWContam_found',
         'left_mid_tags_found',
         'right_mid_tags_found',
         'ReadsWithVector_found',
         'ReadsWithContam_found']
        return bargraph.plot(self.seqyclean_data, self._clean_keys(keys), config)

    def seqyclean_discarded(self):
        config = {'id':'seqyclean-discarded-reads-plot', 
         'title':'SeqyClean: Discarded Reads', 
         'ylab':'Number of Reads'}
        keys = [
         'SEDiscByContam',
         'SEDiscByLength',
         'PE1DiscByContam',
         'PE1DiscByLength',
         'PE2DiscByContam',
         'PE2DiscByLength',
         'DiscByContam',
         'DiscByLength']
        return bargraph.plot(self.seqyclean_data, self._clean_keys(keys), config)

    def seqyclean_general_stats_table(self):
        headers = OrderedDict()
        headers['Perc_Kept'] = {'title':'% Kept', 
         'description':'The percentage of reads remaining after cleaning', 
         'scale':'YlGn', 
         'suffix':'%', 
         'max':100, 
         'min':0}
        headers['PercentageKept'] = {'title':'% Kept', 
         'description':'The percentage of reads remaining after cleaning', 
         'scale':'YlGn', 
         'suffix':'%', 
         'max':100, 
         'min':0}
        self.general_stats_addcols(self.seqyclean_data, headers)

    def _clean_keys(self, keys):
        """ Given a list of keys, make them easier to read for plot labels
        """
        cats = OrderedDict()
        for k in keys:
            nice_name = re.sub('([a-z])([A-Z])', '\\g<1> \\g<2>', k)
            nice_name = re.sub('([PS]E\\d?)', '\\g<1> ', nice_name)
            nice_name = re.sub('W([A-Z])', 'W \\g<1>', nice_name)
            nice_name = nice_name.replace('_', ' ')
            nice_name = nice_name.title()
            nice_name = nice_name.replace('Pe', 'PE').replace('Se', 'SE')
            nice_name = nice_name.replace('Tru SEq', 'TruSeq')
            cats[k] = {'name': nice_name}

        return cats