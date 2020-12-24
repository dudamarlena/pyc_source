# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sweaver/Programming/BioExt/BioExt/align/__init__.py
# Compiled at: 2016-09-22 13:18:58
# Size of source mod 2**32: 12482 bytes
from __future__ import division, print_function
import sys
from collections import defaultdict
from os import getpid
import numpy as np
from Bio.Seq import Seq, translate as _translate
from Bio.SeqRecord import SeqRecord
from BioExt.align._align import _align, _compute_codon_matrices
from BioExt.misc import gapless
from BioExt.scorematrices import ProteinScoreMatrix as _ProteinScoreMatrix
__all__ = [
 'Aligner']

def _protein_to_codon(protein_matrix, non_identity_penalty=None):
    from BioExt.scorematrices._scorematrix import dletters
    codon_matrix = np.ones((64, 64), dtype=float) * -10000.0
    pletters = protein_matrix.letters
    mapping = defaultdict(list)
    stops = set()
    for i in range(4):
        for j in range(4):
            for k in range(4):
                cdn = ''.join(dletters[l] for l in (i, j, k))
                aa = _translate(cdn)
                idx = pletters.index(aa)
                if aa == '*':
                    stops.add(idx)
                mapping[idx].append(16 * i + 4 * j + k)

    protein_matrix_ = protein_matrix.tondarray()
    M, N = protein_matrix_.shape
    for i in range(M):
        for k in mapping[i]:
            for j in range(N):
                for l in mapping[j]:
                    if i != j:
                        if not i in stops:
                            if j in stops:
                                pass
                    else:
                        codon_matrix[(k, l)] = protein_matrix_[(i, j)]
                        if k != l and non_identity_penalty:
                            codon_matrix[(k, l)] -= non_identity_penalty
                            continue

    return (
     dletters, codon_matrix)


class Aligner:
    __slots__ = ('__nchars', '__char_map', '__score_matrix', '__score_matrix_', '__open_insertion',
                 '__extend_insertion', '__open_deletion', '__extend_deletion', '__miscall_cost',
                 '__expected_score', '__do_local', '__do_affine', '__do_codon', '__codon3x5',
                 '__codon3x4', '__codon3x2', '__codon3x1', '__cached_pid', '__cached_score_matrix',
                 '__cached_deletion_matrix', '__cached_insertion_matrix')

    def __init__(self, score_matrix, open_insertion=None, extend_insertion=None, open_deletion=None, extend_deletion=None, miscall_cost=None, expected_identity=None, do_local=True, do_affine=True, do_codon=True):
        if do_codon:
            if not isinstance(score_matrix, _ProteinScoreMatrix):
                raise ValueError('codon alignment requires a protein score matrix')
        if do_codon:
            letters, score_matrix_ = _protein_to_codon(score_matrix, 0.5)
        else:
            letters = score_matrix.letters
            score_matrix_ = score_matrix.tondarray()
        magic = 13.333333333333334
        min_score = -score_matrix.min()
        max_score = score_matrix.max()
        score_weight = max(min_score, max_score)
        ext_cost = (max_score + min_score) / magic
        if open_insertion is None:
            open_insertion = 2 * score_weight
        if extend_insertion is None:
            extend_insertion = ext_cost
        if open_deletion is None:
            open_deletion = 2 * score_weight
        if extend_deletion is None:
            extend_deletion = ext_cost
        if miscall_cost is None:
            miscall_cost = 3 * score_weight
        expected_score = Aligner._expected_score(score_matrix, expected_identity)
        char_map = np.zeros((256, ), dtype=int)
        char_map[:] = -256
        for i, l in enumerate(letters):
            char_map[ord(l)] = i

        if do_codon:
            codon3x5, codon3x4, codon3x2, codon3x1 = _compute_codon_matrices(score_matrix_)
        else:
            codon3x5 = codon3x4 = codon3x2 = codon3x1 = np.zeros((0, 0), dtype=float)
        self._Aligner__nchars = len(letters)
        self._Aligner__char_map = char_map
        self._Aligner__score_matrix = score_matrix
        self._Aligner__score_matrix_ = score_matrix_
        self._Aligner__open_insertion = open_insertion
        self._Aligner__extend_insertion = extend_insertion
        self._Aligner__open_deletion = open_deletion
        self._Aligner__extend_deletion = extend_deletion
        self._Aligner__miscall_cost = miscall_cost
        self._Aligner__expected_score = expected_score
        self._Aligner__do_local = do_local
        self._Aligner__do_affine = do_affine
        self._Aligner__do_codon = do_codon
        self._Aligner__codon3x5 = codon3x5
        self._Aligner__codon3x4 = codon3x4
        self._Aligner__codon3x2 = codon3x2
        self._Aligner__codon3x1 = codon3x1
        self._Aligner__cached_pid = getpid()
        self._Aligner__cached_score_matrix = np.empty((1, ), dtype=float)
        self._Aligner__cached_deletion_matrix = np.empty((1, ), dtype=float)
        self._Aligner__cached_insertion_matrix = np.empty((1, ), dtype=float)

    @staticmethod
    def _expected_score(score_matrix, expected_identity):
        if expected_identity is None:
            expected_score = None
        else:
            N = len(score_matrix.letters)
            freqs = list(score_matrix.freqs().values())
            expected_score = 0.0
            pair_norm = 1.0 / (1.0 - sum(v ** 2 for v in freqs))
            for i in range(N):
                for j in range(N):
                    if i != j:
                        expected_score += (1 - expected_identity) * score_matrix[(i, j)] * freqs[i] * freqs[j] * pair_norm
                    else:
                        expected_score += expected_identity * score_matrix[(i, j)] * freqs[i]

        return expected_score

    def __call__(self, ref, query, open_insertion=None, extend_insertion=None, open_deletion=None, extend_deletion=None, miscall_cost=None, do_local=None, do_affine=None):
        if open_insertion is None:
            open_insertion = self._Aligner__open_insertion
        if extend_insertion is None:
            extend_insertion = self._Aligner__extend_insertion
        if open_deletion is None:
            open_deletion = self._Aligner__open_deletion
        if extend_deletion is None:
            extend_deletion = self._Aligner__extend_deletion
        if miscall_cost is None:
            miscall_cost = self._Aligner__miscall_cost
        if do_local is None:
            do_local = self._Aligner__do_local
        if do_affine is None:
            do_affine = self._Aligner__do_affine
        ref = gapless(ref)
        query = gapless(query)
        if len(ref) and ref == str(query.seq):
            if self._Aligner__do_codon:
                score = sum(self._Aligner__score_matrix[(char, char)] for char in _translate(ref))
            else:
                score = sum(self._Aligner__score_matrix[(char, char)] for char in ref)
            return (score / len(ref), ref, query)
        if isinstance(ref, SeqRecord):
            ref_ = str(ref.seq)
        else:
            if isinstance(ref, Seq):
                ref_ = str(ref)
            else:
                ref_ = ref
        if isinstance(query, SeqRecord):
            query_ = str(query.seq)
        else:
            if isinstance(query, Seq):
                query_ = str(query)
            else:
                query_ = query
            ref_ = ref_.upper()
            query_ = query_.upper()
            if self._Aligner__do_codon:
                if len(ref_) % 3 != 0:
                    raise ValueError('when do_codon = True, len(ref) must be a multiple of 3')
            current_pid = getpid()
            if self._Aligner__cached_pid != current_pid:
                self._Aligner__cached_pid = current_pid
                self._Aligner__cached_score_matrix = np.empty((1, ), dtype=float)
                self._Aligner__cached_deletion_matrix = np.empty((1, ), dtype=float)
                self._Aligner__cached_insertion_matrix = np.empty((1, ), dtype=float)
            if self._Aligner__do_codon:
                cache_size = (len(ref_) // 3 + 1) * (len(query_) + 1)
            else:
                cache_size = (len(ref_) + 1) * (len(query_) + 1)
            if self._Aligner__cached_score_matrix.shape[0] < cache_size:
                self._Aligner__cached_score_matrix.resize((cache_size,))
            if do_affine:
                if self._Aligner__cached_deletion_matrix.shape[0] < cache_size:
                    self._Aligner__cached_deletion_matrix.resize((cache_size,))
                if self._Aligner__cached_insertion_matrix.shape[0] < cache_size:
                    self._Aligner__cached_insertion_matrix.resize((cache_size,))
        if len(query) == 0:
            score, ref_aligned, query_aligned = float('-Inf'), ref_, '-' * len(ref_)
        else:
            score, ref_aligned, query_aligned = _align(ref_.encode('utf-8'), query_.encode('utf-8'), self._Aligner__nchars, self._Aligner__char_map, self._Aligner__score_matrix_, self._Aligner__score_matrix_.shape[0], open_insertion, extend_insertion, open_deletion, extend_deletion, miscall_cost, do_local, do_affine, self._Aligner__do_codon, self._Aligner__codon3x5, self._Aligner__codon3x4, self._Aligner__codon3x2, self._Aligner__codon3x1, self._Aligner__cached_score_matrix, self._Aligner__cached_deletion_matrix, self._Aligner__cached_insertion_matrix)
            if sys.version_info >= (3, 0):
                ref_aligned = ref_aligned.decode('utf-8')
                query_aligned = query_aligned.decode('utf-8')
            if isinstance(ref, SeqRecord):
                ref_aligned_ = SeqRecord(Seq(ref_aligned, ref.seq.alphabet), id=ref.id, name=ref.name, description=ref.description, dbxrefs=ref.dbxrefs, annotations=ref.annotations)
            else:
                if isinstance(ref, Seq):
                    ref_aligned_ = Seq(ref_aligned, ref.seq.alphabet)
                else:
                    ref_aligned_ = ref_aligned
                if isinstance(query, SeqRecord):
                    query_aligned_ = SeqRecord(Seq(query_aligned, query.seq.alphabet), id=query.id, name=query.name, description=query.description, dbxrefs=query.dbxrefs, annotations=query.annotations)
                else:
                    if isinstance(query, Seq):
                        query_aligned_ = Seq(query_aligned, query.seq.alphabet)
                    else:
                        query_aligned_ = query_aligned
        if len(query_):
            score /= len(query_) / 3 if self._Aligner__do_codon else len(query_)
        return (score, ref_aligned_, query_aligned_)

    def expected(self, score, expected_identity=None):
        if expected_identity is None:
            expected_score = self._Aligner__expected_score
        else:
            expected_score = Aligner._expected_score(self._Aligner__score_matrix, expected_identity)
        if expected_score is None:
            return True
        else:
            return score >= expected_score