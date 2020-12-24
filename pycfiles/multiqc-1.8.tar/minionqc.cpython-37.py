# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/minionqc/minionqc.py
# Compiled at: 2019-03-08 06:04:03
# Size of source mod 2**32: 9455 bytes
""" MultiQC submodule to parse output from MinIONQC summary stats """
from collections import OrderedDict
import copy, yaml, os, re, logging
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.plots import linegraph, table
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='MinIONQC',
          anchor='minionqc',
          href='https://github.com/roblanf/minion_qc',
          info=' is a QC tool for Oxford Nanopore sequencing data')
        self.minionqc_raw_data = dict()
        self.minionqc_data = dict()
        self.qfilt_data = dict()
        self.q_threshold_list = set()
        for f in self.find_log_files('minionqc', filehandles=True):
            s_name = self.clean_s_name(os.path.basename(f['root']), os.path.dirname(f['root']))
            parsed_dict = self.parse_minionqc_report(s_name, f['f'])
            if parsed_dict is not None:
                if s_name in self.minionqc_data:
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(f['s_name']))
                self.add_data_source(f, s_name)

        self.minionqc_data = self.ignore_samples(self.minionqc_data)
        if len(self.minionqc_data) == 0:
            raise UserWarning
        log.info('Found {} reports'.format(len(self.minionqc_data)))
        headers = self.headers_to_use()
        self.general_stats_addcols(self.minionqc_data, {'total.reads': headers['total.reads']})
        self.write_data_file(self.minionqc_data, 'multiqc_minionqc')
        self.table_qALL()
        self.table_qfiltered()
        self.plot_readlengths()

    def parse_minionqc_report(self, s_name, f):
        """
        Parses minionqc's 'summary.yaml' report file for results.
        Uses only the "All reads" stats. Ignores "Q>=x" part.
        """
        try:

            def dict_constructor(loader, node):
                return OrderedDict(loader.construct_pairs(node))

            yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)
            summary_dict = yaml.safe_load(f)
        except Exception as e:
            try:
                log.error('Error parsing MinIONQC input file: {}'.format(f))
                return
            finally:
                e = None
                del e

        self.minionqc_raw_data[s_name] = copy.deepcopy(summary_dict)
        q_threshold = None
        for k in summary_dict.keys():
            if k.startswith('Q>='):
                q_threshold = k

        data_dict = {}
        data_dict['all'] = summary_dict['All reads']
        data_dict['q_filt'] = summary_dict[q_threshold]
        for q_key in ('all', 'q_filt'):
            for key_1 in ('reads', 'gigabases'):
                for key_2 in data_dict[q_key][key_1]:
                    new_key = '{} {}'.format(key_1, key_2)
                    data_dict[q_key][new_key] = data_dict[q_key][key_1][key_2]

                data_dict[q_key].pop(key_1)

        self.minionqc_data[s_name] = data_dict['all']
        self.qfilt_data[s_name] = data_dict['q_filt']
        self.q_threshold_list.add(q_threshold)

    def headers_to_use(self):
        """
        Defines features of columns to be used in multiqc table
        """
        headers = OrderedDict()
        headers['total.reads'] = {'title':'Total reads', 
         'description':'Total number of reads', 
         'format':'{:,.0f}', 
         'scale':'Greys'}
        headers['total.gigabases'] = {'title':'Total bases (GB)', 
         'description':'Total bases', 
         'format':'{:,.2f}', 
         'scale':'Blues'}
        headers['N50.length'] = {'title':'Reads N50', 
         'description':'Minimum read length needed to cover 50% of all reads', 
         'format':'{:,.0f}', 
         'scale':'Purples'}
        headers['mean.q'] = {'title':'Mean Q score', 
         'description':'Mean quality of reads', 
         'min':0, 
         'max':15, 
         'format':'{:,.1f}', 
         'hidden':True, 
         'scale':'Greens'}
        headers['median.q'] = {'title':'Median Q score', 
         'description':'Median quality of reads', 
         'min':0, 
         'max':15, 
         'format':'{:,.1f}', 
         'scale':'Greens'}
        headers['mean.length'] = {'title':'Mean length (bp)', 
         'description':'Mean read length', 
         'format':'{:,.0f}', 
         'hidden':True, 
         'scale':'Blues'}
        headers['median.length'] = {'title':'Median length (bp)', 
         'description':'Median read length', 
         'format':'{:,.0f}', 
         'scale':'Blues'}
        for k in headers:
            h_id = re.sub('[^0-9a-zA-Z]+', '_', headers[k]['title'])
            headers[k]['rid'] = 'rid_{}'.format(h_id)

        return headers

    def table_qALL(self):
        """ Table showing stats for all reads """
        self.add_section(name='Stats: All reads',
          anchor='minionqc-stats-qAll',
          description='MinIONQC statistics for all reads',
          plot=(table.plot(self.minionqc_data, self.headers_to_use(), {'namespace':'MinIONQC', 
         'id':'minionqc-stats-qAll-table', 
         'table_title':'MinIONQC Stats: All reads'})))

    def table_qfiltered(self):
        """ Table showing stats for q-filtered reads """
        description = 'MinIONQC statistics for quality filtered reads. ' + 'Quailty threshold used: {}.'.format(', '.join(list(self.q_threshold_list)))
        if len(self.q_threshold_list) > 1:
            description += '\n            <div class="alert alert-warning">\n              <span class="glyphicon glyphicon-warning-sign"></span>\n              <strong>Warning!</strong> More than one quality thresholds were present.\n            </div>\n            '
            log.warning('More than one quality thresholds were present. Thresholds: {}.'.format(', '.join(list(self.q_threshold_list))))
        self.add_section(name='Stats: Quality filtered reads',
          anchor='minionqc-stats-qFilt',
          description=description,
          plot=(table.plot(self.qfilt_data, self.headers_to_use(), {'namespace':'MinIONQC', 
         'id':'minionqc-stats-qFilt-table', 
         'table_title':'MinIONQC Stats: Quality filtered reads'})))

    def plot_readlengths(self):
        pdata = [{s_name:d['All reads']['reads'] for s_name, d in self.minionqc_raw_data.items()}, {s_name:d['All reads']['gigabases'] for s_name, d in self.minionqc_raw_data.items()}]
        pconfig = {'id':'minionqc_read_lengths', 
         'title':'MinIONQC: Output versus read length', 
         'categories':True, 
         'data_labels':[
          {'name':'All reads: Num reads', 
           'ylab':'# reads'},
          {'name':'All reads: Num gigabases', 
           'ylab':'# gigabases'}]}
        for qfilt in list(self.q_threshold_list):
            try:
                pdata.extend([{s_name:d[qfilt]['reads'] for s_name, d in self.minionqc_raw_data.items()}, {s_name:d[qfilt]['gigabases'] for s_name, d in self.minionqc_raw_data.items()}])
                pconfig['data_labels'].extend([
                 {'name':'{}: Num reads'.format(qfilt), 
                  'ylab':'# reads'},
                 {'name':'{}: Num gigabases'.format(qfilt), 
                  'ylab':'# gigabases'}])
            except KeyError:
                pass

        self.add_section(name='Read length output',
          anchor='minionqc-read-length-output',
          description='Number of reads / bp sequenced at given read length thresholds.',
          plot=linegraph.plot(pdata, pconfig=pconfig))