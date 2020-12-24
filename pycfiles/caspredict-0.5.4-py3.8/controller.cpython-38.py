# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
        else:
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
                self.is_fasta() or logging.error('Input file is not in fasta format')
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
               32  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
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

Parse error at or near `WITH_CLEANUP_START' instruction at offset 56

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

    def check_db(self):
        if self.db == '':
            try:
                self.db = os.environ['CASPREDICT_DB']
            except:
                logging.error('Could not find database directory')
                sys.exit()

        else:
            self.scoring = os.path.join(self.db, 'CasScoring.csv')
            self.pdir = os.path.join(self.db, 'Profiles', '')
            self.xgb = os.path.join(self.db, 'xgb_repeats.model')
            self.typedict = os.path.join(self.db, 'type_dict.tab')
            self.cutoffdb = os.path.join(self.db, 'cutoffs.tab')
            if os.path.isfile(self.scoring):
                try:
                    dump = pd.read_csv((self.scoring), sep=',')
                except:
                    logging.error('CasScoring table could not be loaded')
                    sys.exit()

            else:
                logging.error('CasScoring table could not be found')
                sys.exit()
            if os.path.isdir(self.pdir):
                for i in os.listdir(self.pdir):
                    if not i.lower().endswith('.hmm'):
                        logging.error('There are non-HMM profiles in the HMM profile directory')
                        sys.exit()

            else:
                logging.error('Could not find HMM profile directory')
            sys.exit()
        with open(self.cutoffdb, 'r') as (f):
            rs = (ll.rstrip().split(':') for ll in f)
            self.cutoffs = {r[1].split(','):r[0].lower() for r in rs}

    def get_length(self):
        with open(self.fasta, 'r') as (handle):
            self.len_dict = {}
            for fa in SeqIO.parse(handle, 'fasta'):
                self.len_dict[fa.id] = len(fa.seq)