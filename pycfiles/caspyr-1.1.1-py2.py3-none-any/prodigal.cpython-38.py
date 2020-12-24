# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caspredict/prodigal.py
# Compiled at: 2020-04-15 17:23:15
# Size of source mod 2**32: 1977 bytes
import os, subprocess, logging, sys, re, pandas as pd

class Prodigal(object):

    def __init__(self, obj):
        self.master = obj
        for key, val in vars(obj).items():
            setattr(self, key, val)

    def run_prod--- This code section failed: ---

 L.  18         0  LOAD_FAST                'self'
                2  LOAD_ATTR                redo
                4  POP_JUMP_IF_TRUE    102  'to 102'

 L.  19         6  LOAD_GLOBAL              logging
                8  LOAD_METHOD              info
               10  LOAD_STR                 'Predicting ORFs with prodigal'
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          

 L.  22        16  LOAD_GLOBAL              open
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                out
               22  LOAD_STR                 'prodigal.log'
               24  BINARY_ADD       
               26  LOAD_STR                 'w'
               28  CALL_FUNCTION_2       2  ''
               30  SETUP_WITH           80  'to 80'
               32  STORE_FAST               'prodigal_log'

 L.  23        34  LOAD_GLOBAL              subprocess
               36  LOAD_ATTR                run
               38  LOAD_STR                 'prodigal'

 L.  24        40  LOAD_STR                 '-i'

 L.  24        42  LOAD_FAST                'self'
               44  LOAD_ATTR                fasta

 L.  25        46  LOAD_STR                 '-a'

 L.  25        48  LOAD_FAST                'self'
               50  LOAD_ATTR                out
               52  LOAD_STR                 'proteins.faa'
               54  BINARY_ADD       

 L.  26        56  LOAD_STR                 '-p'

 L.  26        58  LOAD_FAST                'self'
               60  LOAD_ATTR                prod

 L.  23        62  BUILD_LIST_7          7 

 L.  27        64  LOAD_GLOBAL              subprocess
               66  LOAD_ATTR                DEVNULL

 L.  28        68  LOAD_FAST                'prodigal_log'

 L.  23        70  LOAD_CONST               ('stdout', 'stderr')
               72  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               74  POP_TOP          
               76  POP_BLOCK        
               78  BEGIN_FINALLY    
             80_0  COME_FROM_WITH       30  '30'
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  END_FINALLY      

 L.  31        86  LOAD_FAST                'self'
               88  LOAD_METHOD              check_rerun
               90  CALL_METHOD_0         0  ''
               92  POP_TOP          

 L.  34        94  LOAD_FAST                'self'
               96  LOAD_METHOD              get_genes
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          
            102_0  COME_FROM             4  '4'

Parse error at or near `BEGIN_FINALLY' instruction at offset 78

    def check_rerun(self):
        if os.statself.prot_path.st_size == 0:
            if self.prod == 'single':
                logging.warning'Prodigal failed. Trying in meta mode'
                self.prod = 'meta'
                self.run_prod()
            else:
                logging.critical'Prodigal failed! Check the log'
                sys.exit()

    def get_genes--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                out
                6  LOAD_STR                 'genes.tab'
                8  BINARY_ADD       
               10  LOAD_STR                 'w'
               12  CALL_FUNCTION_2       2  ''
               14  SETUP_WITH           48  'to 48'
               16  STORE_FAST               'gene_tab'

 L.  50        18  LOAD_GLOBAL              subprocess
               20  LOAD_ATTR                run
               22  LOAD_STR                 'grep'
               24  LOAD_STR                 '^>'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                out
               30  LOAD_STR                 'proteins.faa'
               32  BINARY_ADD       
               34  BUILD_LIST_3          3 
               36  LOAD_FAST                'gene_tab'
               38  LOAD_CONST               ('stdout',)
               40  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               42  POP_TOP          
               44  POP_BLOCK        
               46  BEGIN_FINALLY    
             48_0  COME_FROM_WITH       14  '14'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      

 L.  52        54  LOAD_GLOBAL              pd
               56  LOAD_ATTR                read_csv
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                out
               62  LOAD_STR                 'genes.tab'
               64  BINARY_ADD       
               66  LOAD_STR                 '\\s+'
               68  LOAD_CONST               None

 L.  53        70  LOAD_CONST               (0, 2, 4, 6)

 L.  53        72  LOAD_CONST               ('Contig', 'Start', 'End', 'Strand')

 L.  52        74  LOAD_CONST               ('sep', 'header', 'usecols', 'names')
               76  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               78  STORE_FAST               'genes'

 L.  55        80  LOAD_LISTCOMP            '<code_object <listcomp>>'
               82  LOAD_STR                 'Prodigal.get_genes.<locals>.<listcomp>'
               84  MAKE_FUNCTION_0          ''
               86  LOAD_FAST                'genes'
               88  LOAD_STR                 'Contig'
               90  BINARY_SUBSCR    
               92  GET_ITER         
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_FAST                'genes'
               98  LOAD_STR                 'Contig'
              100  STORE_SUBSCR     

 L.  56       102  LOAD_LISTCOMP            '<code_object <listcomp>>'
              104  LOAD_STR                 'Prodigal.get_genes.<locals>.<listcomp>'
              106  MAKE_FUNCTION_0          ''
              108  LOAD_FAST                'genes'
              110  LOAD_STR                 'Contig'
              112  BINARY_SUBSCR    
              114  GET_ITER         
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_FAST                'genes'
              120  LOAD_STR                 'Pos'
              122  STORE_SUBSCR     

 L.  57       124  LOAD_LISTCOMP            '<code_object <listcomp>>'
              126  LOAD_STR                 'Prodigal.get_genes.<locals>.<listcomp>'
              128  MAKE_FUNCTION_0          ''
              130  LOAD_FAST                'genes'
              132  LOAD_STR                 'Contig'
              134  BINARY_SUBSCR    
              136  GET_ITER         
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_FAST                'genes'
              142  LOAD_STR                 'Contig'
              144  STORE_SUBSCR     

 L.  59       146  LOAD_FAST                'genes'
              148  LOAD_FAST                'self'
              150  STORE_ATTR               genes

 L.  61       152  LOAD_FAST                'genes'
              154  LOAD_ATTR                to_csv
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                out
              160  LOAD_STR                 'genes.tab'
              162  BINARY_ADD       
              164  LOAD_CONST               False
              166  LOAD_STR                 '\t'
              168  LOAD_CONST               ('index', 'sep')
              170  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              172  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 46