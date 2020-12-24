# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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

    def read_input(self):
        with open(self.input, 'r') as (f):
            self.repeats = [ll.rstrip() for ll in f]

        def is_dna(s):
            match = re.match('^[ACTGactg]*$', s)
            return match is not None

        for rep in self.repeats:
            if not is_dna(rep):
                print('Error - Non-DNA letters found in sequence:')
                print(rep)
                sys.exit()