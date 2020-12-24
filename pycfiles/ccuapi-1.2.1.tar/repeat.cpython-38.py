# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cctyper/repeat.py
# Compiled at: 2020-04-20 04:27:22
# Size of source mod 2**32: 1312 bytes
import os, sys, re

class RepeatTyper(object):

    def __init__(self, args):
        self.input = args.input
        self.db = args.db
        self.threads = 1
        self.kmer = args.kmer
        self.check_db()
        self.read_input()

    def check_db(self):
        if self.db == '':
            try:
                DB_PATH = os.environ['CCTYPER_DB']
                self.xgb = os.path.join(DB_PATH, 'xgb_repeats.model')
                self.typedict = os.path.join(DB_PATH, 'type_dict.tab')
            except:
                print('Could not find database directory')
                sys.exit()

        else:
            self.xgb = os.path.join(self.db, 'xgb_repeats.model')
            self.typedict = os.path.join(self.db, 'type_dict.tab')

    def read_input--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                input
                6  LOAD_STR                 'r'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           34  'to 34'
               12  STORE_FAST               'f'

 L.  39        14  LOAD_LISTCOMP            '<code_object <listcomp>>'
               16  LOAD_STR                 'RepeatTyper.read_input.<locals>.<listcomp>'
               18  MAKE_FUNCTION_0          ''
               20  LOAD_FAST                'f'
               22  GET_ITER         
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'self'
               28  STORE_ATTR               repeats
               30  POP_BLOCK        
               32  BEGIN_FINALLY    
             34_0  COME_FROM_WITH       10  '10'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      

 L.  42        40  LOAD_CODE                <code_object is_dna>
               42  LOAD_STR                 'RepeatTyper.read_input.<locals>.is_dna'
               44  MAKE_FUNCTION_0          ''
               46  STORE_FAST               'is_dna'

 L.  46        48  LOAD_FAST                'self'
               50  LOAD_ATTR                repeats
               52  GET_ITER         
             54_0  COME_FROM            64  '64'
               54  FOR_ITER             92  'to 92'
               56  STORE_FAST               'rep'

 L.  47        58  LOAD_FAST                'is_dna'
               60  LOAD_FAST                'rep'
               62  CALL_FUNCTION_1       1  ''
               64  POP_JUMP_IF_TRUE     54  'to 54'

 L.  48        66  LOAD_GLOBAL              print
               68  LOAD_STR                 'Error - Non-DNA letters found in sequence:'
               70  CALL_FUNCTION_1       1  ''
               72  POP_TOP          

 L.  49        74  LOAD_GLOBAL              print
               76  LOAD_FAST                'rep'
               78  CALL_FUNCTION_1       1  ''
               80  POP_TOP          

 L.  50        82  LOAD_GLOBAL              sys
               84  LOAD_METHOD              exit
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          
               90  JUMP_BACK            54  'to 54'

Parse error at or near `BEGIN_FINALLY' instruction at offset 32