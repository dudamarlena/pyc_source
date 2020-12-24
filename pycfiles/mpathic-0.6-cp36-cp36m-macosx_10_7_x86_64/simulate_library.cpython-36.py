# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/Desktop_Tests/MPathic3/mpathic/src/simulate_library.py
# Compiled at: 2018-06-21 14:48:50
# Size of source mod 2**32: 9050 bytes
"""
The simulate library class generates simulated data for a Sort Seq Experiment
with a given mutation rate and wild type sequence.
"""
import argparse, numpy as np, scipy as sp, pandas as pd, sys
from mpathic.src import utils
from mpathic.src import qc
from mpathic.src import io_local as io
from mpathic import SortSeqError
from mpathic.src.utils import check, handle_errors
import pdb
from numpy.random import choice

class SimulateLibrary:
    __doc__ = "\n\n    Parameters\n    ----------\n    wtseq : (string)\n            wildtype sequence. Must contain characteres 'A', 'C', 'G','T' for \n\n            dicttype = 'DNA', 'A', 'C', 'G','U' for  dicttype = 'RNA'\n\n    mutrate : (float)\n        mutation rate\n\n    numseq : (int)\n        number of sequences. Must be a positive integer.\n\n    dicttype : (string)\n        sequence dictionary: valid choices include 'dna', 'rna', 'pro'\n\n    probarr : (np.ndarray)\n        probability matrix used to generate bases\n\n    tags : (boolean)\n        If simulating tags, each generated seq gets a unique tag\n\n    tag_length : (int)\n        Length of tags. Should be >= 0\n\n\n    Attributes\n    ----------\n    output_df : (pandas dataframe)\n        Contains the output of simulate library in a pandas dataframe.\n\n\n    "

    @handle_errors
    def __init__(self, wtseq='ACGACGA', mutrate=0.1, numseq=10000, dicttype='dna', probarr=None, tags=False, tag_length=10):
        self.wtseq = wtseq
        self.mutrate = mutrate
        self.numseq = numseq
        self.dicttype = dicttype
        self.probarr = probarr
        self.tags = tags
        self.tag_length = tag_length
        self.output_df = None
        self._input_check()
        seq_dict, inv_dict = utils.choose_dict(dicttype)
        if isinstance(probarr, np.ndarray):
            L = probarr.shape[1]
            letarr = np.zeros([numseq, L])
            for z in range(L):
                letarr[:, z] = np.random.choice((range(len(seq_dict))),
                  numseq, p=(probarr[:, z]))

        else:
            parr = []
            wtseq = wtseq.upper()
            L = len(wtseq)
            letarr = np.zeros([numseq, L])
            wtarr = self.seq2arr(wtseq, seq_dict)
            mrate = mutrate / (len(seq_dict) - 1)
            parr = np.array([
             1 - (len(seq_dict) - 1) * mrate] + [mrate for i in range(len(seq_dict) - 1)])
            letarr = np.random.choice((range(len(seq_dict))),
              [numseq, len(wtseq)], p=parr)
            letarr = np.mod(letarr + wtarr, len(seq_dict))
        seqs = []
        for i in range(numseq):
            seqs.append(self.arr2seq(letarr[i, :], inv_dict))

        seq_col = qc.seqtype_to_seqcolname_dict[dicttype]
        seqs_df = pd.DataFrame(seqs, columns=[seq_col])
        if tags:
            tag_seq_dict, tag_inv_dict = utils.choose_dict('dna')
            tag_alphabet_list = tag_seq_dict.keys()
            check(len(tag_alphabet_list) ** tag_length > 2 * numseq, 'tag_length=%d is too short for num_tags_needed=%d' % (tag_length, numseq))
            tag_set = set([])
            while len(tag_set) < numseq:
                num_tags_left = numseq - len(tag_set)
                new_tags = [''.join(choice(tag_alphabet_list, size=tag_length)) for i in range(num_tags_left)]
                tag_set = tag_set.union(new_tags)

            df = seqs_df.copy()
            df.loc[:, 'ct'] = 1
            df.loc[:, 'tag'] = list(tag_set)
        else:
            seqs_counts = seqs_df[seq_col].value_counts()
            df = seqs_counts.reset_index()
            df.columns = [seq_col, 'ct']
        self.output_df = qc.validate_dataset(df, fix=True)

    def seq2arr(self, seq, seq_dict):
        """
        Change base pairs to numbers
        """
        return np.array([seq_dict[let] for let in seq])

    def arr2seq(self, arr, inv_dict):
        """
        Change numbers back into base pairs.
        """
        return ''.join([inv_dict[num] for num in arr])

    def _input_check(self):
        """
        Check all parameter values for correctness

        """
        check(isinstance(self.wtseq, str), 'type(wtseq) = %s; must be a string ' % type(self.wtseq))
        check(len(self.wtseq) > 0, 'wtseq length cannot be 0')
        unique_base_list = list(set(self.wtseq))
        if len(unique_base_list) > 4:
            if self.dicttype != 'protein':
                print(' Warning, more than 4 unique bases detected for dicttype %s did you mean to enter protein for dicttype? ' % self.dicttype)
        if 'U' in unique_base_list:
            if self.dicttype != 'rna':
                print(' Warning, U bases detected for dicttype %s did you mean to enter rna for dicttype? ' % self.dicttype)
        lin_seq_dict, lin_inv_dict = utils.choose_dict((self.dicttype), modeltype='MAT')
        check(set(self.wtseq).issubset(lin_seq_dict), 'wtseq can only contain bases in ' + str(lin_seq_dict.keys()))
        check(isinstance(self.mutrate, float), 'type(mutrate) = %s; must be a float ' % type(self.mutrate))
        check(self.mutrate > 0 and self.mutrate <= 1, 'mutrate = %d; must be %d <= mutrate <= %d.' % (
         self.mutrate, 0, 1))
        check(isinstance(self.numseq, int), 'type(numseq) = %s; must be a int ' % type(self.numseq))
        check(self.numseq > 0, 'numseq = %d must be a positive int ' % self.numseq)
        check(isinstance(self.dicttype, str), 'type(dicttype) = %s; must be a string ' % type(self.dicttype))
        check(len(self.dicttype) > 0, ' length of dicttype must be greater than 0, length(dicttype): %d' % len(self.dicttype))
        if self.probarr is not None:
            check(isinstance(self.probarr, np.ndarray), 'type(probarr) = %s; must be an np.ndarray ' % type(self.probarr))
        check(isinstance(self.tags, bool), 'type(tags) = %s; must be an boolean ' % type(self.tags))
        check(isinstance(self.tag_length, int), 'type(tag_length) = %s; must be an int ' % type(self.tag_length))
        check(self.tag_length > 0, 'tag_length = %d must be a positive int ' % self.tag_length)