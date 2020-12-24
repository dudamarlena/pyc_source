# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mpathic/src/scan_model.py
# Compiled at: 2018-06-22 14:35:02
"""A script which accepts an model of binding energy and a wild type sequence.
    The script scans the model across the sequence, and generates an energy
    prediction for each starting position. It then sorts by best binding and
    displays all posibilities."""
from __future__ import division
import argparse, numpy as np, scipy as sp, sys, pandas as pd
from Bio import SeqIO
from mpathic.src import utils
from mpathic.src import Models
from mpathic.src import io_local as io
from mpathic.src import qc
from mpathic.src import fast
import re, pdb
from mpathic import SortSeqError

class ScanModel:

    def __init__(self, model_df, contig_list, numsites=10, verbose=False):
        self.sitelist_df = None
        qc.validate_model(model_df)
        seqtype, modeltype = qc.get_model_type(model_df)
        seq_dict, inv_dict = utils.choose_dict(seqtype, modeltype=modeltype)
        alphabet = qc.seqtype_to_alphabet_dict[seqtype]
        search_string = '[^%s]' % alphabet
        for contig_str, contig_name, pos_offset in contig_list:
            if re.search(search_string, contig_str):
                raise SortSeqError('Invalid character for seqtype %s found in %s.' % (
                 seqtype, contig_name))

        if modeltype == 'MAT':
            model_obj = Models.LinearModel(model_df)
        else:
            if modeltype == 'NBR':
                model_obj = Models.NeighborModel(model_df)
            seq_col = qc.seqtype_to_seqcolname_dict[seqtype]
            L = model_obj.length
            sitelist_df = pd.DataFrame(columns=[
             'val', seq_col, 'left', 'right', 'ori', 'contig'])
            for contig_str, contig_name, pos_offset in contig_list:
                if len(contig_str) < L:
                    continue
                this_df = pd.DataFrame(columns=[
                 'val', seq_col, 'left', 'right', 'ori', 'contig'])
                num_sites = len(contig_str) - L + 1
                poss = np.arange(num_sites).astype(int)
                this_df['left'] = poss + pos_offset
                this_df['right'] = poss + pos_offset + L - 1
                contig_str = str(contig_str).encode('UTF-8')
                this_df[seq_col] = fast.seq2sitelist(contig_str, L)
                this_df['ori'] = '+'
                this_df['contig'] = contig_name
                this_df['val'] = model_obj.evaluate(this_df[seq_col])
                sitelist_df = pd.concat([sitelist_df, this_df], ignore_index=True)
                if seqtype == 'dna':
                    this_df[seq_col] = fast.seq2sitelist(contig_str, L, rc=True)
                    this_df['ori'] = '-'
                    this_df['val'] = model_obj.evaluate(this_df[seq_col])
                    sitelist_df = pd.concat([sitelist_df, this_df], ignore_index=True)
                sitelist_df.sort_values(by='val', ascending=False, inplace=True)
                sitelist_df.reset_index(drop=True, inplace=True)
                if sitelist_df.shape[0] > numsites:
                    sitelist_df.drop(sitelist_df.index[numsites:], inplace=True)
                if verbose:
                    print (
                     '.',
                     sys.stdout.flush())

        if verbose:
            print ''
            sys.stdout.flush()
        if sitelist_df.shape[0] == 0:
            raise SortSeqError('No full-length sites found within provided contigs.')
        sitelist_df = qc.validate_sitelist(sitelist_df, fix=True)
        self.sitelist_df = sitelist_df
        return