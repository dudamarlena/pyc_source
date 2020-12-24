# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/adapterRemoval/adapterRemoval.py
# Compiled at: 2019-11-20 10:26:16
# Size of source mod 2**32: 13379 bytes
""" MultiQC module to parse output from Adapter Removal """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc import config
from multiqc.plots import bargraph, linegraph
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Adapter Removal', anchor='adapterRemoval',
          target='Adapter Removal',
          href='https://github.com/MikkelSchubert/adapterremoval',
          info=' rapid adapter trimming, identification, and read merging ')
        self._MultiqcModule__read_type = None
        self._MultiqcModule__any_paired = False
        self._MultiqcModule__collapsed = None
        self._MultiqcModule__any_collapsed = False
        self.s_name = None
        self.adapter_removal_data = {}
        self.len_dist_plot_data = {'mate1':dict(), 
         'mate2':dict(), 
         'singleton':dict(), 
         'collapsed':dict(), 
         'collapsed_truncated':dict(), 
         'discarded':dict(), 
         'all':dict()}
        parsed_data = None
        for f in self.find_log_files('adapterRemoval', filehandles=True):
            self.s_name = f['s_name']
            try:
                parsed_data = self.parse_settings_file(f)
            except UserWarning:
                continue

            if parsed_data is not None:
                self.adapter_removal_data[self.s_name] = parsed_data

        self.adapter_removal_data = self.ignore_samples(self.adapter_removal_data)
        if len(self.adapter_removal_data) == 0:
            raise UserWarning
        log.info('Found {} reports'.format(len(self.adapter_removal_data)))
        self.write_data_file(self.adapter_removal_data, 'multiqc_adapter_removal')
        self.adapter_removal_stats_table()
        self.adapter_removal_retained_chart()
        self.adapter_removal_length_dist_plot()

    def parse_settings_file(self, f):
        self.result_data = {'total':None, 
         'unaligned':None, 
         'aligned':None, 
         'reads_total':None, 
         'retained':None, 
         'percent_aligned':None}
        settings_data = {'header': []}
        block_title = None
        for i, line in enumerate(f['f']):
            line = line.rstrip('\n')
            if line == '':
                continue
            if not block_title:
                block_title = 'header'
                settings_data[block_title].append(str(line))
            elif line.startswith('['):
                block_title = str(line.strip('[]'))
                settings_data[block_title] = []
            else:
                settings_data[block_title].append(str(line))

        self.set_result_data(settings_data)
        return self.result_data

    def set_result_data(self, settings_data):
        self.set_ar_type(settings_data['Length distribution'])
        self.set_trim_stat(settings_data['Trimming statistics'])
        self.set_len_dist(settings_data['Length distribution'])

    def set_ar_type(self, len_dist_data):
        head_line = len_dist_data[0].rstrip('\n').split('\t')
        self._MultiqcModule__read_type = 'paired' if head_line[2] == 'Mate2' else 'single'
        if not self._MultiqcModule__any_paired:
            self._MultiqcModule__any_paired = True if head_line[2] == 'Mate2' else False
        self._MultiqcModule__collapsed = True if head_line[(-3)] == 'CollapsedTruncated' else False
        if not self._MultiqcModule__any_collapsed:
            self._MultiqcModule__any_collapsed = True if head_line[(-3)] == 'CollapsedTruncated' else False
        if self._MultiqcModule__read_type == 'single':
            if self._MultiqcModule__collapsed:
                log.warning('Case single-end and collapse is not implemented -> File %s skipped' % self.s_name)
                raise UserWarning

    def set_trim_stat(self, trim_data):
        required = [
         'total', 'unaligned', 'aligned', 'discarded_m1', 'singleton_m1', 'retained', 'discarded_m2', 'singleton_m2',
         'full-length_cp', 'truncated_cp']
        data_pattern = {'total':0,  'unaligned':1, 
         'aligned':2, 
         'discarded_m1':3, 
         'singleton_m1':4, 
         'retained':6}
        if self._MultiqcModule__read_type == 'paired':
            data_pattern['discarded_m2'] = 5
            data_pattern['singleton_m2'] = 6
            if not self._MultiqcModule__collapsed:
                data_pattern['retained'] = 8
            else:
                data_pattern['full-length_cp'] = 8
                data_pattern['truncated_cp'] = 9
                data_pattern['retained'] = 10
        for field in required:
            if field in data_pattern:
                tmp = trim_data[data_pattern[field]]
                value = tmp.split(': ')[1]
                self.result_data[field] = int(value)
            else:
                self.result_data[field] = 0

        reads_total = self.result_data['total']
        aligned_total = self.result_data['aligned']
        unaligned_total = self.result_data['unaligned']
        if self._MultiqcModule__read_type == 'paired':
            reads_total = self.result_data['total'] * 2
            aligned_total = self.result_data['aligned'] * 2
            unaligned_total = self.result_data['unaligned'] * 2
        self.result_data['aligned_total'] = aligned_total
        self.result_data['unaligned_total'] = unaligned_total
        self.result_data['reads_total'] = reads_total
        self.result_data['discarded_total'] = reads_total - self.result_data['retained']
        self.result_data['retained_reads'] = self.result_data['retained'] - self.result_data['singleton_m1'] - self.result_data['singleton_m2']
        try:
            self.result_data['percent_aligned'] = float(self.result_data['aligned']) * 100.0 / float(self.result_data['total'])
        except ZeroDivisionError:
            self.result_data['percent_aligned'] = 0

    def set_len_dist--- This code section failed: ---

 L. 181         0  SETUP_LOOP          796  'to 796'
                4  LOAD_FAST                'len_dist_data'
                6  LOAD_CONST               1
                8  LOAD_CONST               None
               10  BUILD_SLICE_2         2 
               12  BINARY_SUBSCR    
               14  GET_ITER         
               16  FOR_ITER            794  'to 794'
               20  STORE_FAST               'line'

 L. 182        22  LOAD_FAST                'line'
               24  LOAD_ATTR                rstrip
               26  LOAD_STR                 '\n'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  LOAD_ATTR                split
               32  LOAD_STR                 '\t'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  STORE_FAST               'l_data'

 L. 183        38  LOAD_GLOBAL              list
               40  LOAD_GLOBAL              map
               42  LOAD_GLOBAL              int
               44  LOAD_FAST                'l_data'
               46  CALL_FUNCTION_2       2  '2 positional arguments'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  STORE_FAST               'l_data'

 L. 186        52  LOAD_FAST                'self'
               54  LOAD_ATTR                s_name
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                len_dist_plot_data
               60  LOAD_STR                 'mate1'
               62  BINARY_SUBSCR    
               64  COMPARE_OP               not-in
               66  POP_JUMP_IF_FALSE   194  'to 194'

 L. 187        68  LOAD_GLOBAL              dict
               70  CALL_FUNCTION_0       0  '0 positional arguments'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                len_dist_plot_data
               76  LOAD_STR                 'mate1'
               78  BINARY_SUBSCR    
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                s_name
               84  STORE_SUBSCR     

 L. 188        86  LOAD_GLOBAL              dict
               88  CALL_FUNCTION_0       0  '0 positional arguments'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                len_dist_plot_data
               94  LOAD_STR                 'mate2'
               96  BINARY_SUBSCR    
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                s_name
              102  STORE_SUBSCR     

 L. 189       104  LOAD_GLOBAL              dict
              106  CALL_FUNCTION_0       0  '0 positional arguments'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                len_dist_plot_data
              112  LOAD_STR                 'singleton'
              114  BINARY_SUBSCR    
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                s_name
              120  STORE_SUBSCR     

 L. 190       122  LOAD_GLOBAL              dict
              124  CALL_FUNCTION_0       0  '0 positional arguments'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                len_dist_plot_data
              130  LOAD_STR                 'collapsed'
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                s_name
              138  STORE_SUBSCR     

 L. 191       140  LOAD_GLOBAL              dict
              142  CALL_FUNCTION_0       0  '0 positional arguments'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                len_dist_plot_data
              148  LOAD_STR                 'collapsed_truncated'
              150  BINARY_SUBSCR    
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                s_name
              156  STORE_SUBSCR     

 L. 192       158  LOAD_GLOBAL              dict
              160  CALL_FUNCTION_0       0  '0 positional arguments'
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                len_dist_plot_data
              166  LOAD_STR                 'discarded'
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                s_name
              174  STORE_SUBSCR     

 L. 193       176  LOAD_GLOBAL              dict
              178  CALL_FUNCTION_0       0  '0 positional arguments'
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                len_dist_plot_data
              184  LOAD_STR                 'all'
              186  BINARY_SUBSCR    
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                s_name
              192  STORE_SUBSCR     
            194_0  COME_FROM            66  '66'

 L. 195       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _MultiqcModule__read_type
              198  LOAD_STR                 'single'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   398  'to 398'

 L. 196       206  LOAD_FAST                'self'
              208  LOAD_ATTR                _MultiqcModule__collapsed
              210  POP_JUMP_IF_TRUE    792  'to 792'

 L. 197       214  LOAD_FAST                'l_data'
              216  LOAD_CONST               1
              218  BINARY_SUBSCR    
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                len_dist_plot_data
              224  LOAD_STR                 'mate1'
              226  BINARY_SUBSCR    
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                s_name
              232  BINARY_SUBSCR    
              234  LOAD_FAST                'l_data'
              236  LOAD_CONST               0
              238  BINARY_SUBSCR    
              240  STORE_SUBSCR     

 L. 198       242  LOAD_CONST               None
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                len_dist_plot_data
              248  LOAD_STR                 'mate2'
              250  BINARY_SUBSCR    
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                s_name
              256  BINARY_SUBSCR    
              258  LOAD_FAST                'l_data'
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  STORE_SUBSCR     

 L. 199       266  LOAD_CONST               None
              268  LOAD_FAST                'self'
              270  LOAD_ATTR                len_dist_plot_data
              272  LOAD_STR                 'singleton'
              274  BINARY_SUBSCR    
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                s_name
              280  BINARY_SUBSCR    
              282  LOAD_FAST                'l_data'
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  STORE_SUBSCR     

 L. 200       290  LOAD_CONST               None
              292  LOAD_FAST                'self'
              294  LOAD_ATTR                len_dist_plot_data
              296  LOAD_STR                 'collapsed'
              298  BINARY_SUBSCR    
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                s_name
              304  BINARY_SUBSCR    
              306  LOAD_FAST                'l_data'
              308  LOAD_CONST               0
              310  BINARY_SUBSCR    
              312  STORE_SUBSCR     

 L. 201       314  LOAD_CONST               None
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                len_dist_plot_data
              320  LOAD_STR                 'collapsed_truncated'
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                s_name
              328  BINARY_SUBSCR    
              330  LOAD_FAST                'l_data'
              332  LOAD_CONST               0
              334  BINARY_SUBSCR    
              336  STORE_SUBSCR     

 L. 202       338  LOAD_FAST                'l_data'
              340  LOAD_CONST               2
              342  BINARY_SUBSCR    
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                len_dist_plot_data
              348  LOAD_STR                 'discarded'
              350  BINARY_SUBSCR    
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                s_name
              356  BINARY_SUBSCR    
              358  LOAD_FAST                'l_data'
              360  LOAD_CONST               0
              362  BINARY_SUBSCR    
              364  STORE_SUBSCR     

 L. 203       366  LOAD_FAST                'l_data'
              368  LOAD_CONST               3
              370  BINARY_SUBSCR    
              372  LOAD_FAST                'self'
              374  LOAD_ATTR                len_dist_plot_data
              376  LOAD_STR                 'all'
              378  BINARY_SUBSCR    
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                s_name
              384  BINARY_SUBSCR    
              386  LOAD_FAST                'l_data'
              388  LOAD_CONST               0
              390  BINARY_SUBSCR    
              392  STORE_SUBSCR     
              394  JUMP_FORWARD        396  'to 396'
            396_0  COME_FROM           394  '394'

 L. 206       396  CONTINUE             16  'to 16'

 L. 208       398  LOAD_FAST                'self'
              400  LOAD_ATTR                _MultiqcModule__collapsed
              402  POP_JUMP_IF_TRUE    596  'to 596'

 L. 209       406  LOAD_FAST                'l_data'
              408  LOAD_CONST               1
              410  BINARY_SUBSCR    
              412  LOAD_FAST                'self'
              414  LOAD_ATTR                len_dist_plot_data
              416  LOAD_STR                 'mate1'
              418  BINARY_SUBSCR    
              420  LOAD_FAST                'self'
              422  LOAD_ATTR                s_name
              424  BINARY_SUBSCR    
              426  LOAD_FAST                'l_data'
              428  LOAD_CONST               0
              430  BINARY_SUBSCR    
              432  STORE_SUBSCR     

 L. 210       434  LOAD_FAST                'l_data'
              436  LOAD_CONST               2
              438  BINARY_SUBSCR    
              440  LOAD_FAST                'self'
              442  LOAD_ATTR                len_dist_plot_data
              444  LOAD_STR                 'mate2'
              446  BINARY_SUBSCR    
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                s_name
              452  BINARY_SUBSCR    
              454  LOAD_FAST                'l_data'
              456  LOAD_CONST               0
              458  BINARY_SUBSCR    
              460  STORE_SUBSCR     

 L. 211       462  LOAD_FAST                'l_data'
              464  LOAD_CONST               3
              466  BINARY_SUBSCR    
              468  LOAD_FAST                'self'
              470  LOAD_ATTR                len_dist_plot_data
              472  LOAD_STR                 'singleton'
              474  BINARY_SUBSCR    
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                s_name
              480  BINARY_SUBSCR    
              482  LOAD_FAST                'l_data'
              484  LOAD_CONST               0
              486  BINARY_SUBSCR    
              488  STORE_SUBSCR     

 L. 212       490  LOAD_CONST               None
              492  LOAD_FAST                'self'
              494  LOAD_ATTR                len_dist_plot_data
              496  LOAD_STR                 'collapsed'
              498  BINARY_SUBSCR    
              500  LOAD_FAST                'self'
              502  LOAD_ATTR                s_name
              504  BINARY_SUBSCR    
              506  LOAD_FAST                'l_data'
              508  LOAD_CONST               0
              510  BINARY_SUBSCR    
              512  STORE_SUBSCR     

 L. 213       514  LOAD_CONST               None
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                len_dist_plot_data
              520  LOAD_STR                 'collapsed_truncated'
              522  BINARY_SUBSCR    
              524  LOAD_FAST                'self'
              526  LOAD_ATTR                s_name
              528  BINARY_SUBSCR    
              530  LOAD_FAST                'l_data'
              532  LOAD_CONST               0
              534  BINARY_SUBSCR    
              536  STORE_SUBSCR     

 L. 214       538  LOAD_FAST                'l_data'
              540  LOAD_CONST               4
              542  BINARY_SUBSCR    
              544  LOAD_FAST                'self'
              546  LOAD_ATTR                len_dist_plot_data
              548  LOAD_STR                 'discarded'
              550  BINARY_SUBSCR    
              552  LOAD_FAST                'self'
              554  LOAD_ATTR                s_name
              556  BINARY_SUBSCR    
              558  LOAD_FAST                'l_data'
              560  LOAD_CONST               0
              562  BINARY_SUBSCR    
              564  STORE_SUBSCR     

 L. 215       566  LOAD_FAST                'l_data'
              568  LOAD_CONST               5
              570  BINARY_SUBSCR    
              572  LOAD_FAST                'self'
              574  LOAD_ATTR                len_dist_plot_data
              576  LOAD_STR                 'all'
              578  BINARY_SUBSCR    
              580  LOAD_FAST                'self'
              582  LOAD_ATTR                s_name
              584  BINARY_SUBSCR    
              586  LOAD_FAST                'l_data'
              588  LOAD_CONST               0
              590  BINARY_SUBSCR    
              592  STORE_SUBSCR     
              594  JUMP_BACK            16  'to 16'
              596  ELSE                     '792'

 L. 217       596  LOAD_FAST                'l_data'
              598  LOAD_CONST               1
              600  BINARY_SUBSCR    
              602  LOAD_FAST                'self'
              604  LOAD_ATTR                len_dist_plot_data
              606  LOAD_STR                 'mate1'
              608  BINARY_SUBSCR    
              610  LOAD_FAST                'self'
              612  LOAD_ATTR                s_name
              614  BINARY_SUBSCR    
              616  LOAD_FAST                'l_data'
              618  LOAD_CONST               0
              620  BINARY_SUBSCR    
              622  STORE_SUBSCR     

 L. 218       624  LOAD_FAST                'l_data'
              626  LOAD_CONST               2
              628  BINARY_SUBSCR    
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                len_dist_plot_data
              634  LOAD_STR                 'mate2'
              636  BINARY_SUBSCR    
              638  LOAD_FAST                'self'
              640  LOAD_ATTR                s_name
              642  BINARY_SUBSCR    
              644  LOAD_FAST                'l_data'
              646  LOAD_CONST               0
              648  BINARY_SUBSCR    
              650  STORE_SUBSCR     

 L. 219       652  LOAD_FAST                'l_data'
              654  LOAD_CONST               3
              656  BINARY_SUBSCR    
              658  LOAD_FAST                'self'
              660  LOAD_ATTR                len_dist_plot_data
              662  LOAD_STR                 'singleton'
              664  BINARY_SUBSCR    
              666  LOAD_FAST                'self'
              668  LOAD_ATTR                s_name
              670  BINARY_SUBSCR    
              672  LOAD_FAST                'l_data'
              674  LOAD_CONST               0
              676  BINARY_SUBSCR    
              678  STORE_SUBSCR     

 L. 220       680  LOAD_FAST                'l_data'
              682  LOAD_CONST               4
              684  BINARY_SUBSCR    
              686  LOAD_FAST                'self'
              688  LOAD_ATTR                len_dist_plot_data
              690  LOAD_STR                 'collapsed'
              692  BINARY_SUBSCR    
              694  LOAD_FAST                'self'
              696  LOAD_ATTR                s_name
              698  BINARY_SUBSCR    
              700  LOAD_FAST                'l_data'
              702  LOAD_CONST               0
              704  BINARY_SUBSCR    
              706  STORE_SUBSCR     

 L. 221       708  LOAD_FAST                'l_data'
              710  LOAD_CONST               5
              712  BINARY_SUBSCR    
              714  LOAD_FAST                'self'
              716  LOAD_ATTR                len_dist_plot_data
              718  LOAD_STR                 'collapsed_truncated'
              720  BINARY_SUBSCR    
              722  LOAD_FAST                'self'
              724  LOAD_ATTR                s_name
              726  BINARY_SUBSCR    
              728  LOAD_FAST                'l_data'
              730  LOAD_CONST               0
              732  BINARY_SUBSCR    
              734  STORE_SUBSCR     

 L. 222       736  LOAD_FAST                'l_data'
              738  LOAD_CONST               6
              740  BINARY_SUBSCR    
              742  LOAD_FAST                'self'
              744  LOAD_ATTR                len_dist_plot_data
              746  LOAD_STR                 'discarded'
              748  BINARY_SUBSCR    
              750  LOAD_FAST                'self'
              752  LOAD_ATTR                s_name
              754  BINARY_SUBSCR    
              756  LOAD_FAST                'l_data'
              758  LOAD_CONST               0
              760  BINARY_SUBSCR    
              762  STORE_SUBSCR     

 L. 223       764  LOAD_FAST                'l_data'
              766  LOAD_CONST               7
              768  BINARY_SUBSCR    
              770  LOAD_FAST                'self'
              772  LOAD_ATTR                len_dist_plot_data
              774  LOAD_STR                 'all'
              776  BINARY_SUBSCR    
              778  LOAD_FAST                'self'
              780  LOAD_ATTR                s_name
              782  BINARY_SUBSCR    
              784  LOAD_FAST                'l_data'
              786  LOAD_CONST               0
              788  BINARY_SUBSCR    
              790  STORE_SUBSCR     
              792  JUMP_BACK            16  'to 16'
              794  POP_BLOCK        
            796_0  COME_FROM_LOOP        0  '0'

Parse error at or near `JUMP_BACK' instruction at offset 792

    def adapter_removal_stats_table(self):
        headers = OrderedDict()
        headers['percent_aligned'] = {'title':'% Trimmed', 
         'description':'% trimmed reads', 
         'max':100, 
         'min':0, 
         'suffix':'%', 
         'scale':'RdYlGn-rev', 
         'shared_key':'percent_aligned'}
        headers['aligned_total'] = {'title':'{} Reads Trimmed'.format(config.read_count_prefix), 
         'description':'Total trimmed reads ({})'.format(config.read_count_desc), 
         'modify':lambda x: x * config.read_count_multiplier, 
         'min':0, 
         'scale':'PuBu', 
         'shared_key':'read_count'}
        self.general_stats_addcols(self.adapter_removal_data, headers)

    def adapter_removal_retained_chart(self):
        pconfig = {'title':'Adapter Removal: Discarded Reads', 
         'id':'ar_retained_plot', 
         'ylab':'# Reads', 
         'hide_zero_cats':False, 
         'cpswitch_counts_label':'Number of Reads'}
        cats_pec = OrderedDict()
        if self._MultiqcModule__any_paired:
            cats_pec['retained_reads'] = {'name': 'Retained Read Pairs'}
        cats_pec['singleton_m1'] = {'name': 'Singleton R1'}
        if self._MultiqcModule__any_paired:
            cats_pec['singleton_m2'] = {'name': 'Singleton R2'}
            if self._MultiqcModule__any_collapsed:
                cats_pec['full-length_cp'] = {'name': 'Full-length Collapsed Pairs'}
                cats_pec['truncated_cp'] = {'name': 'Truncated Collapsed Pairs'}
        cats_pec['discarded_m1'] = {'name': 'Discarded R1'}
        if self._MultiqcModule__any_paired:
            cats_pec['discarded_m2'] = {'name': 'Discarded R2'}
        self.add_section(name='Retained and Discarded Paired-End Collapsed',
          anchor='adapter_removal_retained_plot',
          description='The number of retained and discarded reads.',
          plot=(bargraph.plot(self.adapter_removal_data, cats_pec, pconfig)))

    def adapter_removal_length_dist_plot(self):
        pconfig = {'title':'Adapter Removal: Length Distribution', 
         'id':'ar_length_count_plot', 
         'ylab':'Counts', 
         'xlab':'read length', 
         'xDecimals':False, 
         'ymin':0, 
         'tt_label':'<b>{point.x} bp trimmed</b>: {point.y:.0f}', 
         'data_labels':None}
        lineplot_data = [
         self.len_dist_plot_data['all'],
         self.len_dist_plot_data['mate1']]
        data_labels = [
         {'name':'All', 
          'ylab':'Count'},
         {'name':'Mate1', 
          'ylab':'Count'}]
        if self._MultiqcModule__any_paired:
            lineplot_data.extend([
             self.len_dist_plot_data['mate2'],
             self.len_dist_plot_data['singleton']])
            data_labels.extend([
             {'name':'Mate2', 
              'ylab':'Count'},
             {'name':'Singleton', 
              'ylab':'Count'}])
            if self._MultiqcModule__any_collapsed:
                lineplot_data.extend([
                 self.len_dist_plot_data['collapsed'],
                 self.len_dist_plot_data['collapsed_truncated']])
                data_labels.extend([
                 {'name':'Collapsed', 
                  'ylab':'Count'},
                 {'name':'Collapsed Truncated', 
                  'ylab':'Count'}])
        lineplot_data.append(self.len_dist_plot_data['discarded'])
        data_labels.append({'name':'Discarded',  'ylab':'Count'})
        pconfig['data_labels'] = data_labels
        self.add_section(name='Length Distribution Paired End Collapsed',
          anchor='ar_length_count',
          description='The length distribution of reads after processing adapter alignment.',
          plot=(linegraph.plot(lineplot_data, pconfig)))