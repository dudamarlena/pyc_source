# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caspredict/controller.py
# Compiled at: 2020-04-15 17:23:15
# Size of source mod 2**32: 5675 bytes
import os, logging, sys, shutil, pandas as pd
from Bio import SeqIO

class Controller(object):

    def __init__(self, args):
        self.fasta = args.input
        self.out = args.output
        self.threads = args.threads
        self.dist = args.dist
        self.prod = args.prodigal
        self.db = args.db
        self.circular = args.circular
        self.oev = args.overall_eval
        self.ocs = args.overall_cov_seq
        self.och = args.overall_cov_hmm
        self.check_inp = args.skip_check
        self.keep_tmp = args.keep_tmp
        self.lvl = args.log_lvl
        self.redo = args.redo_typing
        self.kmer = args.kmer
        self.crispr_cas_dist = args.ccd
        self.pred_prob = args.pred_prob
        self.noplot = args.no_plot
        self.scale = args.scale
        self.nogrid = args.no_grid
        self.expand = args.expand
        self.plotexpand = args.plot_expand
        self.simplelog = args.simplelog
        self.any_cas = False
        self.any_operon = False
        self.any_crispr = False
        if self.simplelog:
            logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=(self.lvl))
        else:
            logging.basicConfig(format='\x1b[36m[%(asctime)s] %(levelname)s:\x1b[0m %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=(self.lvl))
        logging.info('Running CasPredict version 0.5.4')
        self.out = os.path.join(self.out, '')
        if self.redo:
            self.check_inp = True
        self.prot_path = self.out + 'proteins.faa'
        self.check_db()
        self.check_input()
        self.check_out()
        if self.redo and not os.path.exists(self.out + 'cas_operons.tab'):
            if os.path.exists(self.out + 'cas_operons_putative.tab'):
                self.any_operon = True
            if os.path.exists(self.out + 'crisprs_all.tab'):
                self.any_crispr = True
            da = vars(args)
            f = open(self.out + 'arguments.tab', 'w')
            for k, v in da.items():
                f.write('{}:\t{}\n'.format(k, v))

            f.close()
            if self.circular:
                self.get_length()

    def check_out(self):
        if not self.redo:
            try:
                os.mkdir(self.out)
            except FileExistsError:
                logging.error('Directory ' + self.out + ' already exists')
                sys.exit()

    def check_input(self):
        if not self.check_inp:
            if os.path.isfile(self.fasta):
                if not self.is_fasta():
                    logging.error('Input file is not in fasta format')
                    sys.exit()
            else:
                logging.error('Could not find input file')
                sys.exit()

    def is_fasta--- This code section failed: ---

 L. 104         0  SETUP_FINALLY        78  'to 78'

 L. 105         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fasta
                8  LOAD_STR                 'r'
               10  CALL_FUNCTION_2       2  ''
               12  SETUP_WITH           68  'to 68'
               14  STORE_FAST               'handle'

 L. 106        16  LOAD_GLOBAL              SeqIO
               18  LOAD_METHOD              parse
               20  LOAD_FAST                'handle'
               22  LOAD_STR                 'fasta'
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'fa'

 L. 107        28  LOAD_LISTCOMP            '<code_object <listcomp>>'
               30  LOAD_STR                 'Controller.is_fasta.<locals>.<listcomp>'
               32  MAKE_FUNCTION_0          ''
               34  LOAD_FAST                'fa'
               36  GET_ITER         
               38  CALL_FUNCTION_1       1  ''
               40  POP_TOP          

 L. 108        42  LOAD_GLOBAL              logging
               44  LOAD_METHOD              error
               46  LOAD_STR                 'Numeric fasta headers not supported'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 109        52  POP_BLOCK        
               54  BEGIN_FINALLY    
               56  WITH_CLEANUP_START
               58  WITH_CLEANUP_FINISH
               60  POP_FINALLY           0  ''
               62  POP_BLOCK        
               64  LOAD_CONST               False
               66  RETURN_VALUE     
             68_0  COME_FROM_WITH       12  '12'
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      
               74  POP_BLOCK        
               76  JUMP_FORWARD        146  'to 146'
             78_0  COME_FROM_FINALLY     0  '0'

 L. 110        78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 111        84  LOAD_GLOBAL              open
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                fasta
               90  LOAD_STR                 'r'
               92  CALL_FUNCTION_2       2  ''
               94  SETUP_WITH          134  'to 134'
               96  STORE_FAST               'handle'

 L. 112        98  LOAD_GLOBAL              SeqIO
              100  LOAD_METHOD              parse
              102  LOAD_FAST                'handle'
              104  LOAD_STR                 'fasta'
              106  CALL_METHOD_2         2  ''
              108  STORE_FAST               'fa'

 L. 113       110  LOAD_GLOBAL              any
              112  LOAD_FAST                'fa'
              114  CALL_FUNCTION_1       1  ''
              116  POP_BLOCK        
              118  ROT_TWO          
              120  BEGIN_FINALLY    
              122  WITH_CLEANUP_START
              124  WITH_CLEANUP_FINISH
              126  POP_FINALLY           0  ''
              128  ROT_FOUR         
              130  POP_EXCEPT       
              132  RETURN_VALUE     
            134_0  COME_FROM_WITH       94  '94'
              134  WITH_CLEANUP_START
              136  WITH_CLEANUP_FINISH
              138  END_FINALLY      
              140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
              144  END_FINALLY      
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM            76  '76'

Parse error at or near `BEGIN_FINALLY' instruction at offset 54

    def clean(self):
        if not self.redo:
            if os.stat(self.out + 'hmmer.log').st_size == 0:
                os.remove(self.out + 'hmmer.log')
            if not self.keep_tmp:
                logging.info('Removing temporary files')
                shutil.rmtree(self.out + 'hmmer')
                os.remove(self.out + 'minced.out')
                os.remove(self.out + 'prodigal.log')
                os.remove(self.out + 'proteins.faa')

    def check_db--- This code section failed: ---

 L. 133         0  LOAD_FAST                'self'
                2  LOAD_ATTR                db
                4  LOAD_STR                 ''
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    58  'to 58'

 L. 134        10  SETUP_FINALLY        28  'to 28'

 L. 135        12  LOAD_GLOBAL              os
               14  LOAD_ATTR                environ
               16  LOAD_STR                 'CASPREDICT_DB'
               18  BINARY_SUBSCR    
               20  LOAD_FAST                'self'
               22  STORE_ATTR               db
               24  POP_BLOCK        
               26  JUMP_FORWARD         58  'to 58'
             28_0  COME_FROM_FINALLY    10  '10'

 L. 136        28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 137        34  LOAD_GLOBAL              logging
               36  LOAD_METHOD              error
               38  LOAD_STR                 'Could not find database directory'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 138        44  LOAD_GLOBAL              sys
               46  LOAD_METHOD              exit
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
               56  END_FINALLY      
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            26  '26'
             58_2  COME_FROM             8  '8'

 L. 140        58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_METHOD              join
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                db
               68  LOAD_STR                 'CasScoring.csv'
               70  CALL_METHOD_2         2  ''
               72  LOAD_FAST                'self'
               74  STORE_ATTR               scoring

 L. 141        76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              join
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                db
               86  LOAD_STR                 'Profiles'
               88  LOAD_STR                 ''
               90  CALL_METHOD_3         3  ''
               92  LOAD_FAST                'self'
               94  STORE_ATTR               pdir

 L. 142        96  LOAD_GLOBAL              os
               98  LOAD_ATTR                path
              100  LOAD_METHOD              join
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                db
              106  LOAD_STR                 'xgb_repeats.model'
              108  CALL_METHOD_2         2  ''
              110  LOAD_FAST                'self'
              112  STORE_ATTR               xgb

 L. 143       114  LOAD_GLOBAL              os
              116  LOAD_ATTR                path
              118  LOAD_METHOD              join
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                db
              124  LOAD_STR                 'type_dict.tab'
              126  CALL_METHOD_2         2  ''
              128  LOAD_FAST                'self'
              130  STORE_ATTR               typedict

 L. 144       132  LOAD_GLOBAL              os
              134  LOAD_ATTR                path
              136  LOAD_METHOD              join
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                db
              142  LOAD_STR                 'cutoffs.tab'
              144  CALL_METHOD_2         2  ''
              146  LOAD_FAST                'self'
              148  STORE_ATTR               cutoffdb

 L. 147       150  LOAD_GLOBAL              os
              152  LOAD_ATTR                path
              154  LOAD_METHOD              isfile
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                scoring
              160  CALL_METHOD_1         1  ''
              162  POP_JUMP_IF_FALSE   218  'to 218'

 L. 148       164  SETUP_FINALLY       186  'to 186'

 L. 149       166  LOAD_GLOBAL              pd
              168  LOAD_ATTR                read_csv
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                scoring
              174  LOAD_STR                 ','
              176  LOAD_CONST               ('sep',)
              178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              180  STORE_FAST               'dump'
              182  POP_BLOCK        
              184  JUMP_ABSOLUTE       236  'to 236'
            186_0  COME_FROM_FINALLY   164  '164'

 L. 150       186  POP_TOP          
              188  POP_TOP          
              190  POP_TOP          

 L. 151       192  LOAD_GLOBAL              logging
              194  LOAD_METHOD              error
              196  LOAD_STR                 'CasScoring table could not be loaded'
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L. 152       202  LOAD_GLOBAL              sys
              204  LOAD_METHOD              exit
              206  CALL_METHOD_0         0  ''
              208  POP_TOP          
              210  POP_EXCEPT       
              212  JUMP_ABSOLUTE       236  'to 236'
              214  END_FINALLY      
              216  JUMP_FORWARD        236  'to 236'
            218_0  COME_FROM           162  '162'

 L. 154       218  LOAD_GLOBAL              logging
              220  LOAD_METHOD              error
              222  LOAD_STR                 'CasScoring table could not be found'
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          

 L. 155       228  LOAD_GLOBAL              sys
              230  LOAD_METHOD              exit
              232  CALL_METHOD_0         0  ''
              234  POP_TOP          
            236_0  COME_FROM           216  '216'

 L. 158       236  LOAD_GLOBAL              os
              238  LOAD_ATTR                path
              240  LOAD_METHOD              isdir
              242  LOAD_FAST                'self'
              244  LOAD_ATTR                pdir
              246  CALL_METHOD_1         1  ''
          248_250  POP_JUMP_IF_FALSE   308  'to 308'

 L. 159       252  LOAD_GLOBAL              os
              254  LOAD_METHOD              listdir
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                pdir
              260  CALL_METHOD_1         1  ''
              262  GET_ITER         
            264_0  COME_FROM           280  '280'
              264  FOR_ITER            306  'to 306'
              266  STORE_FAST               'i'

 L. 160       268  LOAD_FAST                'i'
              270  LOAD_METHOD              lower
              272  CALL_METHOD_0         0  ''
              274  LOAD_METHOD              endswith
              276  LOAD_STR                 '.hmm'
              278  CALL_METHOD_1         1  ''
          280_282  POP_JUMP_IF_TRUE    264  'to 264'

 L. 161       284  LOAD_GLOBAL              logging
              286  LOAD_METHOD              error
              288  LOAD_STR                 'There are non-HMM profiles in the HMM profile directory'
              290  CALL_METHOD_1         1  ''
              292  POP_TOP          

 L. 162       294  LOAD_GLOBAL              sys
              296  LOAD_METHOD              exit
              298  CALL_METHOD_0         0  ''
              300  POP_TOP          
          302_304  JUMP_BACK           264  'to 264'
              306  JUMP_FORWARD        326  'to 326'
            308_0  COME_FROM           248  '248'

 L. 164       308  LOAD_GLOBAL              logging
              310  LOAD_METHOD              error
              312  LOAD_STR                 'Could not find HMM profile directory'
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          

 L. 165       318  LOAD_GLOBAL              sys
              320  LOAD_METHOD              exit
              322  CALL_METHOD_0         0  ''
              324  POP_TOP          
            326_0  COME_FROM           306  '306'

 L. 168       326  LOAD_GLOBAL              open
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                cutoffdb
              332  LOAD_STR                 'r'
              334  CALL_FUNCTION_2       2  ''
              336  SETUP_WITH          374  'to 374'
              338  STORE_FAST               'f'

 L. 169       340  LOAD_GENEXPR             '<code_object <genexpr>>'
              342  LOAD_STR                 'Controller.check_db.<locals>.<genexpr>'
              344  MAKE_FUNCTION_0          ''
              346  LOAD_FAST                'f'
              348  GET_ITER         
              350  CALL_FUNCTION_1       1  ''
              352  STORE_FAST               'rs'

 L. 170       354  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              356  LOAD_STR                 'Controller.check_db.<locals>.<dictcomp>'
              358  MAKE_FUNCTION_0          ''
              360  LOAD_FAST                'rs'
              362  GET_ITER         
              364  CALL_FUNCTION_1       1  ''
              366  LOAD_FAST                'self'
              368  STORE_ATTR               cutoffs
              370  POP_BLOCK        
              372  BEGIN_FINALLY    
            374_0  COME_FROM_WITH      336  '336'
              374  WITH_CLEANUP_START
              376  WITH_CLEANUP_FINISH
              378  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 372

    def get_length--- This code section failed: ---

 L. 173         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fasta
                6  LOAD_STR                 'r'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           60  'to 60'
               12  STORE_FAST               'handle'

 L. 174        14  BUILD_MAP_0           0 
               16  LOAD_FAST                'self'
               18  STORE_ATTR               len_dict

 L. 175        20  LOAD_GLOBAL              SeqIO
               22  LOAD_METHOD              parse
               24  LOAD_FAST                'handle'
               26  LOAD_STR                 'fasta'
               28  CALL_METHOD_2         2  ''
               30  GET_ITER         
               32  FOR_ITER             56  'to 56'
               34  STORE_FAST               'fa'

 L. 176        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'fa'
               40  LOAD_ATTR                seq
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                len_dict
               48  LOAD_FAST                'fa'
               50  LOAD_ATTR                id
               52  STORE_SUBSCR     
               54  JUMP_BACK            32  'to 32'
               56  POP_BLOCK        
               58  BEGIN_FINALLY    
             60_0  COME_FROM_WITH       10  '10'
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 58