# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michal/workspace/code/newtbase/blastplus/settings.py
# Compiled at: 2018-02-19 04:38:08
# Size of source mod 2**32: 4014 bytes
"""
user defined blastplus app settings file
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SAMPLE_DIR = os.path.join(BASE_DIR, 'blastplus/sampledata/')
BLAST_DB_NUCL_LIST = [
 {'name':'sample1', 
  'path':'blastplus/sampledata/sample_db1/sample_db', 
  'desc':'Sample database 1', 
  'annotated':False},
 {'name':'sample2', 
  'path':'blastplus/sampledata/sample_db2/sample_db2', 
  'desc':'Sample database 2', 
  'annotated':False}]
BLAST_DB_PROT_LIST = [
 {'name':'sample3', 
  'path':'blastplus/sampledata/sample_db3_prot/sample_db3_prot', 
  'desc':'Sample database 3 - proteins', 
  'annotated':False},
 {'name':'sample4', 
  'path':'blastplus/sampledata/sample_db4_prot/sample_db4_prot', 
  'desc':'Sample database 4 - proteins', 
  'annotated':False}]
BLAST_DB_NUCL_CHOICE = [(os.path.join(BASE_DIR, db['path']), db['desc']) for db in BLAST_DB_NUCL_LIST]
BLAST_DB_PROT_CHOICE = [(os.path.join(BASE_DIR, db['path']), db['desc']) for db in BLAST_DB_PROT_LIST]
EXAMPLE_FASTA_NUCL_FILE_PATH = os.path.join(BASE_DIR, 'blastplus/sampledata/sample_nucl.fasta')
EXAMPLE_FASTA_PROT_FILE_PATH = os.path.join(BASE_DIR, 'blastplus/sampledata/sample_prot.fasta')
BLAST_MAX_NUMBER_SEQ_IN_INPUT = 10
BLAST_FORM_ATTRS = {'class': 'blastplus_input_seq_form'}
BLAST_FORM_INPUTTEXT_ATTRS = {'class': 'blastplus_input_textfield_form'}
MATRIX_LIST = [
 'BLOSUM45', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM30', 'PAM70']
MATRIX_CHOICE_LIST = list((x, x) for x in MATRIX_LIST)
MATRIX_DEFAULT = 'BLOSUM62'
EVALUE_LIST = [
 1, 0.001, 1e-05, 1e-06, 1e-10, 1e-30, 1e-50, 1e-100]
EVALUE_CHOICE_LIST = list((x, str(x)) for x in list(EVALUE_LIST))
EVALUE_BLAST_DEFAULT = 0.001
NUCLEOTIDE_SEARCH_SENSITIVE_CHOICE = (("{'gapopen': 5, 'gapextend': 2, 'penalty': -3, 'reward': 2}", 'NORMAL'),
                                      ("{'penalty': -3, 'word_size': 15,'gapopen': 5, 'gapextend': 2,  'reward': 1, }", 'NEAR MATCH'),
                                      ("{'penalty': -1, 'word_size': 9,'gapopen': 2, 'gapextend': 1,  'reward': 1, }", 'DISTANT'))
PROTEIN_SEARCH_SENSITIVE_CHOICE = (("{'gapopen': 11, 'gapextend': 1, 'matrix': 'BLOSUM62'}", 'NORMAL'),
                                   ("{'gapopen': 10, 'gapextend': 1, 'matrix': 'BLOSUM90'}", 'NEAR MATCH'),
                                   ("{'gapopen': 14, 'gapextend': 2, 'matrix': 'BLOSUM45'}", 'DISTANT'))

class BlastLimitSet(object):

    def __init__(self, default_word_size, min_word_size, max_word_size):
        self.default_word_size = default_word_size
        self.min_word_size = min_word_size
        self.max_word_size = max_word_size

    def get_word_size_error(self):
        return 'word size should be between {} and {}'.format(self.min_word_size, self.max_word_size - 1)


BLASTN_SETS = BlastLimitSet(default_word_size=11, min_word_size=7, max_word_size=50)
TBLASTN_SETS = BlastLimitSet(default_word_size=3, min_word_size=3, max_word_size=8)
BLASTP_SETS = BlastLimitSet(default_word_size=3, min_word_size=2, max_word_size=7)
BLASTX_SETS = BlastLimitSet(default_word_size=3, min_word_size=2, max_word_size=7)
BLAST_CORRECT_SEQ_ERROR_MSG = 'Please put correct sequence!'
BLAST_CORRECT_SEQ_MAX_SEQ_NUMB_ERROR_MSG = 'Too many sequences, maximum is {}'.format(BLAST_MAX_NUMBER_SEQ_IN_INPUT)
BLAST_CORRECT_SEQ_TOO_SHORT_ERROR_MSG = 'Too short sequence!'
BLAST_CORRECT_PARAMS = 'Sorry, incorrect parameter combination'