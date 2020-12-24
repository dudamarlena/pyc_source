# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cctyper/controller.py
# Compiled at: 2020-05-13 08:07:19
# Size of source mod 2**32: 5933 bytes
import os, logging, sys, shutil, json, pandas as pd
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
        self.simplelog = args.simplelog
        self.any_cas = False
        self.any_operon = False
        self.any_crispr = False
        if self.simplelog:
            logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=(self.lvl))
        else:
            logging.basicConfig(format='\x1b[36m[%(asctime)s] %(levelname)s:\x1b[0m %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=(self.lvl))
        logging.info('Running CRISPRCasTyper version 1.1.1')
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

 L. 103         0  SETUP_FINALLY        78  'to 78'

 L. 104         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fasta
                8  LOAD_STR                 'r'
               10  CALL_FUNCTION_2       2  ''
               12  SETUP_WITH           68  'to 68'
               14  STORE_FAST               'handle'

 L. 105        16  LOAD_GLOBAL              SeqIO
               18  LOAD_METHOD              parse
               20  LOAD_FAST                'handle'
               22  LOAD_STR                 'fasta'
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'fa'

 L. 106        28  LOAD_LISTCOMP            '<code_object <listcomp>>'
               30  LOAD_STR                 'Controller.is_fasta.<locals>.<listcomp>'
               32  MAKE_FUNCTION_0          ''
               34  LOAD_FAST                'fa'
               36  GET_ITER         
               38  CALL_FUNCTION_1       1  ''
               40  POP_TOP          

 L. 107        42  LOAD_GLOBAL              logging
               44  LOAD_METHOD              error
               46  LOAD_STR                 'Numeric fasta headers not supported'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 108        52  POP_BLOCK        
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

 L. 109        78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 110        84  LOAD_GLOBAL              open
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                fasta
               90  LOAD_STR                 'r'
               92  CALL_FUNCTION_2       2  ''
               94  SETUP_WITH          134  'to 134'
               96  STORE_FAST               'handle'

 L. 111        98  LOAD_GLOBAL              SeqIO
              100  LOAD_METHOD              parse
              102  LOAD_FAST                'handle'
              104  LOAD_STR                 'fasta'
              106  CALL_METHOD_2         2  ''
              108  STORE_FAST               'fa'

 L. 112       110  LOAD_GLOBAL              any
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

 L. 132         0  LOAD_FAST                'self'
                2  LOAD_ATTR                db
                4  LOAD_STR                 ''
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    58  'to 58'

 L. 133        10  SETUP_FINALLY        28  'to 28'

 L. 134        12  LOAD_GLOBAL              os
               14  LOAD_ATTR                environ
               16  LOAD_STR                 'CCTYPER_DB'
               18  BINARY_SUBSCR    
               20  LOAD_FAST                'self'
               22  STORE_ATTR               db
               24  POP_BLOCK        
               26  JUMP_FORWARD         58  'to 58'
             28_0  COME_FROM_FINALLY    10  '10'

 L. 135        28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 136        34  LOAD_GLOBAL              logging
               36  LOAD_METHOD              error
               38  LOAD_STR                 'Could not find database directory'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 137        44  LOAD_GLOBAL              sys
               46  LOAD_METHOD              exit
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
               56  END_FINALLY      
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            26  '26'
             58_2  COME_FROM             8  '8'

 L. 139        58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_METHOD              join
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                db
               68  LOAD_STR                 'CasScoring.csv'
               70  CALL_METHOD_2         2  ''
               72  LOAD_FAST                'self'
               74  STORE_ATTR               scoring

 L. 140        76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              join
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                db
               86  LOAD_STR                 'Profiles'
               88  LOAD_STR                 ''
               90  CALL_METHOD_3         3  ''
               92  LOAD_FAST                'self'
               94  STORE_ATTR               pdir

 L. 141        96  LOAD_GLOBAL              os
               98  LOAD_ATTR                path
              100  LOAD_METHOD              join
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                db
              106  LOAD_STR                 'xgb_repeats.model'
              108  CALL_METHOD_2         2  ''
              110  LOAD_FAST                'self'
              112  STORE_ATTR               xgb

 L. 142       114  LOAD_GLOBAL              os
              116  LOAD_ATTR                path
              118  LOAD_METHOD              join
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                db
              124  LOAD_STR                 'type_dict.tab'
              126  CALL_METHOD_2         2  ''
              128  LOAD_FAST                'self'
              130  STORE_ATTR               typedict

 L. 143       132  LOAD_GLOBAL              os
              134  LOAD_ATTR                path
              136  LOAD_METHOD              join
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                db
              142  LOAD_STR                 'cutoffs.tab'
              144  CALL_METHOD_2         2  ''
              146  LOAD_FAST                'self'
              148  STORE_ATTR               cutoffdb

 L. 144       150  LOAD_GLOBAL              os
              152  LOAD_ATTR                path
              154  LOAD_METHOD              join
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                db
              160  LOAD_STR                 'interference.json'
              162  CALL_METHOD_2         2  ''
              164  LOAD_FAST                'self'
              166  STORE_ATTR               ifdb

 L. 145       168  LOAD_GLOBAL              os
              170  LOAD_ATTR                path
              172  LOAD_METHOD              join
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                db
              178  LOAD_STR                 'adaptation.json'
              180  CALL_METHOD_2         2  ''
              182  LOAD_FAST                'self'
              184  STORE_ATTR               addb

 L. 148       186  LOAD_GLOBAL              os
              188  LOAD_ATTR                path
              190  LOAD_METHOD              isfile
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                scoring
              196  CALL_METHOD_1         1  ''
              198  POP_JUMP_IF_FALSE   254  'to 254'

 L. 149       200  SETUP_FINALLY       222  'to 222'

 L. 150       202  LOAD_GLOBAL              pd
              204  LOAD_ATTR                read_csv
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                scoring
              210  LOAD_STR                 ','
              212  LOAD_CONST               ('sep',)
              214  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              216  STORE_FAST               'dump'
              218  POP_BLOCK        
              220  JUMP_FORWARD        252  'to 252'
            222_0  COME_FROM_FINALLY   200  '200'

 L. 151       222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L. 152       228  LOAD_GLOBAL              logging
              230  LOAD_METHOD              error
              232  LOAD_STR                 'CasScoring table could not be loaded'
              234  CALL_METHOD_1         1  ''
              236  POP_TOP          

 L. 153       238  LOAD_GLOBAL              sys
              240  LOAD_METHOD              exit
              242  CALL_METHOD_0         0  ''
              244  POP_TOP          
              246  POP_EXCEPT       
              248  JUMP_FORWARD        252  'to 252'
              250  END_FINALLY      
            252_0  COME_FROM           248  '248'
            252_1  COME_FROM           220  '220'
              252  JUMP_FORWARD        272  'to 272'
            254_0  COME_FROM           198  '198'

 L. 155       254  LOAD_GLOBAL              logging
              256  LOAD_METHOD              error
              258  LOAD_STR                 'CasScoring table could not be found'
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          

 L. 156       264  LOAD_GLOBAL              sys
              266  LOAD_METHOD              exit
              268  CALL_METHOD_0         0  ''
              270  POP_TOP          
            272_0  COME_FROM           252  '252'

 L. 159       272  LOAD_GLOBAL              os
              274  LOAD_ATTR                path
              276  LOAD_METHOD              isdir
              278  LOAD_FAST                'self'
              280  LOAD_ATTR                pdir
              282  CALL_METHOD_1         1  ''
          284_286  POP_JUMP_IF_FALSE   344  'to 344'

 L. 160       288  LOAD_GLOBAL              os
              290  LOAD_METHOD              listdir
              292  LOAD_FAST                'self'
              294  LOAD_ATTR                pdir
              296  CALL_METHOD_1         1  ''
              298  GET_ITER         
            300_0  COME_FROM           316  '316'
              300  FOR_ITER            342  'to 342'
              302  STORE_FAST               'i'

 L. 161       304  LOAD_FAST                'i'
              306  LOAD_METHOD              lower
              308  CALL_METHOD_0         0  ''
              310  LOAD_METHOD              endswith
              312  LOAD_STR                 '.hmm'
              314  CALL_METHOD_1         1  ''
          316_318  POP_JUMP_IF_TRUE    300  'to 300'

 L. 162       320  LOAD_GLOBAL              logging
              322  LOAD_METHOD              error
              324  LOAD_STR                 'There are non-HMM profiles in the HMM profile directory'
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          

 L. 163       330  LOAD_GLOBAL              sys
              332  LOAD_METHOD              exit
              334  CALL_METHOD_0         0  ''
              336  POP_TOP          
          338_340  JUMP_BACK           300  'to 300'
              342  JUMP_FORWARD        362  'to 362'
            344_0  COME_FROM           284  '284'

 L. 165       344  LOAD_GLOBAL              logging
              346  LOAD_METHOD              error
              348  LOAD_STR                 'Could not find HMM profile directory'
              350  CALL_METHOD_1         1  ''
              352  POP_TOP          

 L. 166       354  LOAD_GLOBAL              sys
              356  LOAD_METHOD              exit
              358  CALL_METHOD_0         0  ''
              360  POP_TOP          
            362_0  COME_FROM           342  '342'

 L. 169       362  LOAD_GLOBAL              open
              364  LOAD_FAST                'self'
              366  LOAD_ATTR                cutoffdb
              368  LOAD_STR                 'r'
              370  CALL_FUNCTION_2       2  ''
              372  SETUP_WITH          410  'to 410'
              374  STORE_FAST               'f'

 L. 170       376  LOAD_GENEXPR             '<code_object <genexpr>>'
              378  LOAD_STR                 'Controller.check_db.<locals>.<genexpr>'
              380  MAKE_FUNCTION_0          ''
              382  LOAD_FAST                'f'
              384  GET_ITER         
              386  CALL_FUNCTION_1       1  ''
              388  STORE_FAST               'rs'

 L. 171       390  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              392  LOAD_STR                 'Controller.check_db.<locals>.<dictcomp>'
              394  MAKE_FUNCTION_0          ''
              396  LOAD_FAST                'rs'
              398  GET_ITER         
              400  CALL_FUNCTION_1       1  ''
              402  LOAD_FAST                'self'
              404  STORE_ATTR               cutoffs
              406  POP_BLOCK        
              408  BEGIN_FINALLY    
            410_0  COME_FROM_WITH      372  '372'
              410  WITH_CLEANUP_START
              412  WITH_CLEANUP_FINISH
              414  END_FINALLY      

 L. 174       416  LOAD_GLOBAL              open
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                ifdb
              422  LOAD_STR                 'r'
              424  CALL_FUNCTION_2       2  ''
              426  SETUP_WITH          446  'to 446'
              428  STORE_FAST               'f'

 L. 175       430  LOAD_GLOBAL              json
              432  LOAD_METHOD              load
              434  LOAD_FAST                'f'
              436  CALL_METHOD_1         1  ''
              438  LOAD_FAST                'self'
              440  STORE_ATTR               compl_interf
              442  POP_BLOCK        
              444  BEGIN_FINALLY    
            446_0  COME_FROM_WITH      426  '426'
              446  WITH_CLEANUP_START
              448  WITH_CLEANUP_FINISH
              450  END_FINALLY      

 L. 176       452  LOAD_GLOBAL              open
              454  LOAD_FAST                'self'
              456  LOAD_ATTR                addb
              458  LOAD_STR                 'r'
              460  CALL_FUNCTION_2       2  ''
              462  SETUP_WITH          482  'to 482'
              464  STORE_FAST               'f'

 L. 177       466  LOAD_GLOBAL              json
              468  LOAD_METHOD              load
              470  LOAD_FAST                'f'
              472  CALL_METHOD_1         1  ''
              474  LOAD_FAST                'self'
              476  STORE_ATTR               compl_adapt
              478  POP_BLOCK        
              480  BEGIN_FINALLY    
            482_0  COME_FROM_WITH      462  '462'
              482  WITH_CLEANUP_START
              484  WITH_CLEANUP_FINISH
              486  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 408

    def get_length--- This code section failed: ---

 L. 180         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fasta
                6  LOAD_STR                 'r'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           60  'to 60'
               12  STORE_FAST               'handle'

 L. 181        14  BUILD_MAP_0           0 
               16  LOAD_FAST                'self'
               18  STORE_ATTR               len_dict

 L. 182        20  LOAD_GLOBAL              SeqIO
               22  LOAD_METHOD              parse
               24  LOAD_FAST                'handle'
               26  LOAD_STR                 'fasta'
               28  CALL_METHOD_2         2  ''
               30  GET_ITER         
               32  FOR_ITER             56  'to 56'
               34  STORE_FAST               'fa'

 L. 183        36  LOAD_GLOBAL              len
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