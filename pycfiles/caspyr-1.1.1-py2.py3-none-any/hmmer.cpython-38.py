# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caspredict/hmmer.py
# Compiled at: 2020-04-13 09:16:17
# Size of source mod 2**32: 4469 bytes
import os, subprocess, sys, logging, re, glob, tqdm, multiprocess as mp, pandas as pd

class HMMER(object):

    def __init__(self, obj):
        self.master = obj
        for key, val in vars(obj).items():
            setattr(self, key, val)

    def main_hmm(self):
        if self.redo:
            self.read_hmm()
        else:
            self.run_hmm()
            self.load_hmm()
            self.write_hmm()
        self.check_hmm()
        self.parse_hmm()

    def hmmsearch--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              re
                2  LOAD_METHOD              sub
                4  LOAD_STR                 '\\.hmm'
                6  LOAD_STR                 ''
                8  LOAD_FAST                'hmm'
               10  CALL_METHOD_3         3  ''
               12  STORE_FAST               'hmm_name'

 L.  40        14  LOAD_GLOBAL              logging
               16  LOAD_METHOD              debug
               18  LOAD_STR                 'Running HMMER against '
               20  LOAD_FAST                'hmm_name'
               22  BINARY_ADD       
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L.  42        28  LOAD_GLOBAL              open
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                out
               34  LOAD_STR                 'hmmer.log'
               36  BINARY_ADD       
               38  LOAD_STR                 'a'
               40  CALL_FUNCTION_2       2  ''
               42  SETUP_WITH          112  'to 112'
               44  STORE_FAST               'hmmer_log'

 L.  43        46  LOAD_GLOBAL              subprocess
               48  LOAD_ATTR                run
               50  LOAD_STR                 'hmmsearch'

 L.  44        52  LOAD_STR                 '--domtblout'

 L.  44        54  LOAD_GLOBAL              os
               56  LOAD_ATTR                path
               58  LOAD_METHOD              join
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                out
               64  LOAD_STR                 'hmmer'
               66  BINARY_ADD       
               68  LOAD_FAST                'hmm_name'
               70  LOAD_STR                 '.tab'
               72  BINARY_ADD       
               74  CALL_METHOD_2         2  ''

 L.  45        76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              join
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                pdir
               86  LOAD_FAST                'hmm'
               88  CALL_METHOD_2         2  ''

 L.  46        90  LOAD_FAST                'self'
               92  LOAD_ATTR                prot_path

 L.  43        94  BUILD_LIST_5          5 

 L.  47        96  LOAD_GLOBAL              subprocess
               98  LOAD_ATTR                DEVNULL

 L.  48       100  LOAD_FAST                'hmmer_log'

 L.  43       102  LOAD_CONST               ('stdout', 'stderr')
              104  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              106  POP_TOP          
              108  POP_BLOCK        
              110  BEGIN_FINALLY    
            112_0  COME_FROM_WITH       42  '42'
              112  WITH_CLEANUP_START
              114  WITH_CLEANUP_FINISH
              116  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 110

    def run_hmm(self):
        logging.info'Running HMMER against Cas profiles'
        os.mkdir(self.out + 'hmmer')
        pool = mp.Poolself.threads
        if self.lvl == 'DEBUG' or self.simplelog:
            list(pool.imapself.hmmsearchos.listdirself.pdir)
        else:
            list(tqdm.tqdm((pool.imapself.hmmsearchos.listdirself.pdir), total=(len(os.listdirself.pdir))))
        pool.close()

    def load_hmm--- This code section failed: ---

 L.  70         0  LOAD_GLOBAL              logging
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'Loading HMMER output'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.  73        10  LOAD_GLOBAL              glob
               12  LOAD_METHOD              glob
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                path
               18  LOAD_METHOD              join
               20  LOAD_DEREF               'self'
               22  LOAD_ATTR                out
               24  LOAD_STR                 'hmmer'
               26  BINARY_ADD       
               28  LOAD_STR                 '*.tab'
               30  CALL_METHOD_2         2  ''
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'hmm_files'

 L.  76        36  LOAD_GLOBAL              open
               38  LOAD_DEREF               'self'
               40  LOAD_ATTR                out
               42  LOAD_STR                 'hmmer.tab'
               44  BINARY_ADD       
               46  LOAD_STR                 'w'
               48  CALL_FUNCTION_2       2  ''
               50  SETUP_WITH          106  'to 106'
               52  STORE_FAST               'hmmer_tab'

 L.  77        54  LOAD_GLOBAL              subprocess
               56  LOAD_ATTR                run
               58  LOAD_STR                 'grep'
               60  LOAD_STR                 '-v'
               62  LOAD_STR                 '^#'
               64  BUILD_LIST_3          3 
               66  LOAD_FAST                'hmm_files'
               68  BINARY_ADD       
               70  LOAD_FAST                'hmmer_tab'
               72  LOAD_CONST               ('stdout',)
               74  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               76  POP_TOP          

 L.  78        78  LOAD_GLOBAL              subprocess
               80  LOAD_METHOD              run
               82  LOAD_STR                 'sed'
               84  LOAD_STR                 '-i'
               86  LOAD_STR                 's/:/ /'
               88  LOAD_DEREF               'self'
               90  LOAD_ATTR                out
               92  LOAD_STR                 'hmmer.tab'
               94  BINARY_ADD       
               96  BUILD_LIST_4          4 
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  POP_BLOCK        
              104  BEGIN_FINALLY    
            106_0  COME_FROM_WITH       50  '50'
              106  WITH_CLEANUP_START
              108  WITH_CLEANUP_FINISH
              110  END_FINALLY      

 L.  81       112  LOAD_GLOBAL              pd
              114  LOAD_ATTR                read_csv
              116  LOAD_DEREF               'self'
              118  LOAD_ATTR                out
              120  LOAD_STR                 'hmmer.tab'
              122  BINARY_ADD       
              124  LOAD_STR                 '\\s+'
              126  LOAD_CONST               None

 L.  82       128  LOAD_CONST               (0, 1, 3, 6, 7, 8, 16, 17, 18, 19, 20, 21, 22, 24, 26, 28)

 L.  85       130  LOAD_CONST               ('Hmm', 'ORF', 'tlen', 'qlen', 'Eval', 'score', 'hmm_from', 'hmm_to', 'ali_from', 'ali_to', 'env_from', 'env_to', 'pprop', 'start', 'end', 'strand')

 L.  81       132  LOAD_CONST               ('sep', 'header', 'usecols', 'names')
              134  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              136  STORE_FAST               'hmm_df'

 L.  90       138  LOAD_CLOSURE             'self'
              140  BUILD_TUPLE_1         1 
              142  LOAD_LISTCOMP            '<code_object <listcomp>>'
              144  LOAD_STR                 'HMMER.load_hmm.<locals>.<listcomp>'
              146  MAKE_FUNCTION_8          'closure'

 L.  92       148  LOAD_FAST                'hmm_df'
              150  LOAD_STR                 'Hmm'
              152  BINARY_SUBSCR    

 L.  90       154  GET_ITER         
              156  CALL_FUNCTION_1       1  ''
              158  LOAD_FAST                'hmm_df'
              160  LOAD_STR                 'Hmm'
              162  STORE_SUBSCR     

 L.  95       164  LOAD_LISTCOMP            '<code_object <listcomp>>'
              166  LOAD_STR                 'HMMER.load_hmm.<locals>.<listcomp>'
              168  MAKE_FUNCTION_0          ''
              170  LOAD_FAST                'hmm_df'
              172  LOAD_STR                 'ORF'
              174  BINARY_SUBSCR    
              176  GET_ITER         
              178  CALL_FUNCTION_1       1  ''
              180  LOAD_FAST                'hmm_df'
              182  LOAD_STR                 'Acc'
              184  STORE_SUBSCR     

 L.  96       186  LOAD_LISTCOMP            '<code_object <listcomp>>'
              188  LOAD_STR                 'HMMER.load_hmm.<locals>.<listcomp>'
              190  MAKE_FUNCTION_0          ''
              192  LOAD_FAST                'hmm_df'
              194  LOAD_STR                 'ORF'
              196  BINARY_SUBSCR    
              198  GET_ITER         
              200  CALL_FUNCTION_1       1  ''
              202  LOAD_FAST                'hmm_df'
              204  LOAD_STR                 'Pos'
              206  STORE_SUBSCR     

 L.  99       208  LOAD_CODE                <code_object covs>
              210  LOAD_STR                 'HMMER.load_hmm.<locals>.covs'
              212  MAKE_FUNCTION_0          ''
              214  STORE_FAST               'covs'

 L. 110       216  LOAD_FAST                'hmm_df'
              218  LOAD_METHOD              groupby
              220  LOAD_STR                 'Hmm'
              222  LOAD_STR                 'ORF'
              224  BUILD_LIST_2          2 
              226  CALL_METHOD_1         1  ''
              228  LOAD_METHOD              apply
              230  LOAD_FAST                'covs'
              232  CALL_METHOD_1         1  ''
              234  STORE_FAST               'hmm_df'

 L. 111       236  LOAD_FAST                'hmm_df'
              238  LOAD_METHOD              drop_duplicates
              240  CALL_METHOD_0         0  ''
              242  LOAD_DEREF               'self'
              244  STORE_ATTR               hmm_df

Parse error at or near `BEGIN_FINALLY' instruction at offset 104

    def write_hmm(self):
        self.hmm_df.to_csv((self.out + 'hmmer.tab'), sep='\t', index=False)

    def read_hmm(self):
        self.hmm_df = pd.read_csv((self.out + 'hmmer.tab'), sep='\t')

    def check_hmm(self):
        if len(self.hmm_df) == 0:
            logging.info'No Cas proteins found.'
        else:
            self.any_cas = True

    def parse_hmm(self):
        if self.any_cas:
            logging.info'Parsing HMMER output'
            self.hmm_df.sort_values('score', ascending=False, inplace=True)
            self.hmm_df.drop_duplicates('ORF', inplace=True)