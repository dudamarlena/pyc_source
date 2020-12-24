# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-ppc/egg/oldowan/mitomotifs/biopython/pairwise2.py
# Compiled at: 2008-08-24 10:54:33
"""This package implements pairwise sequence alignment using a dynamic
programming algorithm.

This provides functions to get global and local alignments between two
sequences.  A global alignment finds the best concordance between all
characters in two sequences.  A local alignment finds just the
subsequences that align the best.

When doing alignments, you can specify the match score and gap
penalties.  The match score indicates the compatibility between an
alignment of two characters in the sequences.  Highly compatible
characters should be given positive scores, and incompatible ones
should be given negative scores or 0.  The gap penalties should be
negative.

The names of the alignment functions in this module follow the
convention
<alignment type>XX
where <alignment type> is either "global" or "local" and XX is a 2
character code indicating the parameters it takes.  The first
character indicates the parameters for matches (and mismatches), and
the second indicates the parameters for gap penalties.

The match parameters are
CODE  DESCRIPTION
x     No parameters.  Identical characters have score of 1, otherwise 0.
m     A match score is the score of identical chars, otherwise mismatch score.
d     A dictionary returns the score of any pair of characters.
c     A callback function returns scores.

The gap penalty parameters are
CODE  DESCRIPTION
x     No gap penalties.
s     Same open and extend gap penalties for both sequences.
d     The sequences have different open and extend gap penalties.
c     A callback function returns the gap penalties.

All the different alignment functions are contained in an object
"align".  For example:

    #>>> from Bio import pairwise2
    #>>> alignments = pairwise2.align.globalxx("ACCGT", "ACG")

will return a list of the alignments between the two strings.  The
parameters of the alignment function depends on the function called.
Some examples:

#>>> pairwise2.align.globalxx("ACCGT", "ACG")
    # Find the best global alignment between the two sequences.
    # Identical characters are given 1 point.  No points are deducted
    # for mismatches or gaps.
    
#>>> pairwise2.align.localxx("ACCGT", "ACG")
    # Same thing as before, but with a local alignment.
    
#>>> pairwise2.align.globalmx("ACCGT", "ACG", 2, -1)
    # Do a global alignment.  Identical characters are given 2 points,
    # 1 point is deducted for each non-identical character.

#>>> pairwise2.align.globalms("ACCGT", "ACG", 2, -1, -.5, -.1)
    # Same as above, except now 0.5 points are deducted when opening a
    # gap, and 0.1 points are deducted when extending it.

To see a description of the parameters for a function, please look at
the docstring for the function.

#>>> print newalign.align.localds.__doc__
localds(sequenceA, sequenceB, match_dict, open, extend) -> alignments

"""
from types import *
import listfns
MAX_ALIGNMENTS = 1000

class align:
    """This class provides functions that do alignments."""

    class alignment_function:
        """This class is callable impersonates an alignment function.
        The constructor takes the name of the function.  This class
        will decode the name of the function to figure out how to
        interpret the parameters.

        """
        match2args = {'x': ([], ''), 'm': (
               [
                'match', 'mismatch'],
               'match is the score to given to identical characters.  mismatch is\nthe score given to non-identical ones.'), 
           'd': (
               [
                'match_dict'],
               'match_dict is a dictionary where the keys are tuples of pairs of\ncharacters and the values are the scores, e.g. ("A", "C") : 2.5.'), 
           'c': (
               [
                'match_fn'],
               'match_fn is a callback function that takes two characters and\nreturns the score between them.')}
        penalty2args = {'x': ([], ''), 's': (
               [
                'open', 'extend'],
               'open and extend are the gap penalties when a gap is opened and\nextended.  They should be negative.'), 
           'd': (
               [
                'openA', 'extendA', 'openB', 'extendB'],
               'openA and extendA are the gap penalties for sequenceA, and openB\nand extendB for sequeneB.  The penalties should be negative.'), 
           'c': (
               [
                'gap_A_fn', 'gap_B_fn'],
               'gap_A_fn and gap_B_fn are callback functions that takes 1) the\nindex where the gap is opened, and 2) the length of the gap.  They\nshould return a gap penalty.')}

        def __init__(self, name):
            if name.startswith('global'):
                if len(name) != 8:
                    raise AttributeError, 'function should be globalXX'
            elif name.startswith('local'):
                if len(name) != 7:
                    raise AttributeError, 'function should be localXX'
            else:
                raise AttributeError, name
            align_type, match_type, penalty_type = name[:-2], name[(-2)], name[(-1)]
            try:
                (match_args, match_doc) = self.match2args[match_type]
            except KeyError, x:
                raise AttributeError, 'unknown match type %r' % match_type

            try:
                (penalty_args, penalty_doc) = self.penalty2args[penalty_type]
            except KeyError, x:
                raise AttributeError, 'unknown penalty type %r' % penalty_type

            param_names = [
             'sequenceA', 'sequenceB']
            param_names.extend(match_args)
            param_names.extend(penalty_args)
            self.function_name = name
            self.align_type = align_type
            self.param_names = param_names
            self.__name__ = self.function_name
            doc = '%s(%s) -> alignments\n' % (
             self.__name__, (', ').join(self.param_names))
            if match_doc:
                doc += '\n%s\n' % match_doc
            if penalty_doc:
                doc += '\n%s\n' % penalty_doc
            doc += '\nalignments is a list of tuples (seqA, seqB, score, begin, end).\nseqA and seqB are strings showing the alignment between the\nsequences.  score is the score of the alignment.  begin and end\nare indexes into seqA and seqB that indicate the where the\nalignment occurs.\n'
            self.__doc__ = doc

        def decode(self, *args, **keywds):
            keywds = keywds.copy()
            if len(args) != len(self.param_names):
                raise TypeError, '%s takes exactly %d argument (%d given)' % (
                 self.function_name, len(self.param_names), len(args))
            i = 0
            while i < len(self.param_names):
                if self.param_names[i] in ('sequenceA', 'sequenceB', 'gap_A_fn', 'gap_B_fn',
                                           'match_fn'):
                    keywds[self.param_names[i]] = args[i]
                    i += 1
                elif self.param_names[i] == 'match':
                    assert self.param_names[(i + 1)] == 'mismatch'
                    match, mismatch = args[i], args[(i + 1)]
                    keywds['match_fn'] = identity_match(match, mismatch)
                    i += 2
                elif self.param_names[i] == 'match_dict':
                    keywds['match_fn'] = dictionary_match(args[i])
                    i += 1
                elif self.param_names[i] == 'open':
                    assert self.param_names[(i + 1)] == 'extend'
                    open, extend = args[i], args[(i + 1)]
                    pe = keywds.get('penalize_extend_when_opening', 0)
                    keywds['gap_A_fn'] = affine_penalty(open, extend, pe)
                    keywds['gap_B_fn'] = affine_penalty(open, extend, pe)
                    i += 2
                elif self.param_names[i] == 'openA':
                    assert self.param_names[(i + 3)] == 'extendB'
                    (openA, extendA, openB, extendB) = args[i:i + 4]
                    pe = keywds.get('penalize_extend_when_opening', 0)
                    keywds['gap_A_fn'] = affine_penalty(openA, extendA, pe)
                    keywds['gap_B_fn'] = affine_penalty(openB, extendB, pe)
                    i += 4
                else:
                    raise ValueError, 'unknown parameter %r' % self.param_names[i]

            pe = keywds.get('penalize_extend_when_opening', 0)
            default_params = [
             (
              'match_fn', identity_match(1, 0)),
             (
              'gap_A_fn', affine_penalty(0, 0, pe)),
             (
              'gap_B_fn', affine_penalty(0, 0, pe)),
             ('penalize_extend_when_opening', 0),
             (
              'penalize_end_gaps', self.align_type == 'global'),
             (
              'align_globally', self.align_type == 'global'),
             ('gap_char', '-'),
             ('force_generic', 0),
             ('score_only', 0),
             ('one_alignment_only', 0)]
            for (name, default) in default_params:
                keywds[name] = keywds.get(name, default)

            return keywds

        def __call__(self, *args, **keywds):
            keywds = self.decode(*args, **keywds)
            return _align(**keywds)

    def __getattr__(self, attr):
        return self.alignment_function(attr)


align = align()

def _align(sequenceA, sequenceB, match_fn, gap_A_fn, gap_B_fn, penalize_extend_when_opening, penalize_end_gaps, align_globally, gap_char, force_generic, score_only, one_alignment_only):
    if not sequenceA or not sequenceB:
        return []
    if not force_generic and type(gap_A_fn) is InstanceType and gap_A_fn.__class__ is affine_penalty and type(gap_B_fn) is InstanceType and gap_B_fn.__class__ is affine_penalty:
        open_A, extend_A = gap_A_fn.open, gap_A_fn.extend
        open_B, extend_B = gap_B_fn.open, gap_B_fn.extend
        x = _make_score_matrix_fast(sequenceA, sequenceB, match_fn, open_A, extend_A, open_B, extend_B, penalize_extend_when_opening, penalize_end_gaps, align_globally, score_only)
    else:
        x = _make_score_matrix_generic(sequenceA, sequenceB, match_fn, gap_A_fn, gap_B_fn, penalize_extend_when_opening, penalize_end_gaps, align_globally, score_only)
    (score_matrix, trace_matrix) = x
    starts = _find_start(score_matrix, sequenceA, sequenceB, gap_A_fn, gap_B_fn, penalize_end_gaps, align_globally)
    best_score = max([ x[0] for x in starts ])
    if score_only:
        return best_score
    tolerance = 0
    i = 0
    while i < len(starts):
        (score, pos) = starts[i]
        if rint(abs(score - best_score)) > rint(tolerance):
            del starts[i]
        else:
            i += 1

    x = _recover_alignments(sequenceA, sequenceB, starts, score_matrix, trace_matrix, align_globally, penalize_end_gaps, gap_char, one_alignment_only)
    return x


def _make_score_matrix_generic(sequenceA, sequenceB, match_fn, gap_A_fn, gap_B_fn, penalize_extend_when_opening, penalize_end_gaps, align_globally, score_only):
    lenA, lenB = len(sequenceA), len(sequenceB)
    score_matrix, trace_matrix = [], []
    for i in range(lenA):
        score_matrix.append([None] * lenB)
        trace_matrix.append([[None]] * lenB)

    for i in range(lenA):
        score = match_fn(sequenceA[i], sequenceB[0])
        if penalize_end_gaps:
            score += gap_B_fn(0, i)
        score_matrix[i][0] = score

    for i in range(1, lenB):
        score = match_fn(sequenceA[0], sequenceB[i])
        if penalize_end_gaps:
            score += gap_A_fn(0, i)
        score_matrix[0][i] = score

    for row in range(1, lenA):
        for col in range(1, lenB):
            best_score = score_matrix[(row - 1)][(col - 1)]
            best_score_rint = rint(best_score)
            best_indexes = [(row - 1, col - 1)]
            for i in range(0, col - 1):
                score = score_matrix[(row - 1)][i] + gap_A_fn(i, col - 1 - i)
                score_rint = rint(score)
                if score_rint == best_score_rint:
                    best_score, best_score_rint = score, score_rint
                    best_indexes.append((row - 1, i))
                elif score_rint > best_score_rint:
                    best_score, best_score_rint = score, score_rint
                    best_indexes = [(row - 1, i)]

            for i in range(0, row - 1):
                score = score_matrix[i][(col - 1)] + gap_B_fn(i, row - 1 - i)
                score_rint = rint(score)
                if score_rint == best_score_rint:
                    best_score, best_score_rint = score, score_rint
                    best_indexes.append((i, col - 1))
                elif score_rint > best_score_rint:
                    best_score, best_score_rint = score, score_rint
                    best_indexes = [(i, col - 1)]

            score_matrix[row][col] = best_score + match_fn(sequenceA[row], sequenceB[col])
            if not align_globally and score_matrix[row][col] < 0:
                score_matrix[row][col] = 0
            trace_matrix[row][col] = best_indexes

    return (
     score_matrix, trace_matrix)


def _make_score_matrix_fast(sequenceA, sequenceB, match_fn, open_A, extend_A, open_B, extend_B, penalize_extend_when_opening, penalize_end_gaps, align_globally, score_only):
    first_A_gap = calc_affine_penalty(1, open_A, extend_A, penalize_extend_when_opening)
    first_B_gap = calc_affine_penalty(1, open_B, extend_B, penalize_extend_when_opening)
    lenA, lenB = len(sequenceA), len(sequenceB)
    score_matrix, trace_matrix = [], []
    for i in range(lenA):
        score_matrix.append([None] * lenB)
        trace_matrix.append([[None]] * lenB)

    for i in range(lenA):
        score = match_fn(sequenceA[i], sequenceB[0])
        if penalize_end_gaps:
            score += calc_affine_penalty(i, open_B, extend_B, penalize_extend_when_opening)
        score_matrix[i][0] = score

    for i in range(1, lenB):
        score = match_fn(sequenceA[0], sequenceB[i])
        if penalize_end_gaps:
            score += calc_affine_penalty(i, open_A, extend_A, penalize_extend_when_opening)
        score_matrix[0][i] = score

    row_cache_score, row_cache_index = [
     None] * (lenA - 1), [None] * (lenA - 1)
    col_cache_score, col_cache_index = [
     None] * (lenB - 1), [None] * (lenB - 1)
    for i in range(lenA - 1):
        row_cache_score[i] = score_matrix[i][0] + first_A_gap
        row_cache_index[i] = [(i, 0)]

    for i in range(lenB - 1):
        col_cache_score[i] = score_matrix[0][i] + first_B_gap
        col_cache_index[i] = [(0, i)]

    for row in range(1, lenA):
        for col in range(1, lenB):
            nogap_score = score_matrix[(row - 1)][(col - 1)]
            if col > 1:
                row_score = row_cache_score[(row - 1)]
            else:
                row_score = nogap_score - 1
            if row > 1:
                col_score = col_cache_score[(col - 1)]
            else:
                col_score = nogap_score - 1
            best_score = max(nogap_score, row_score, col_score)
            best_score_rint = rint(best_score)
            best_index = []
            if best_score_rint == rint(nogap_score):
                best_index.append((row - 1, col - 1))
            if best_score_rint == rint(row_score):
                best_index.extend(row_cache_index[(row - 1)])
            if best_score_rint == rint(col_score):
                best_index.extend(col_cache_index[(col - 1)])
            score = best_score + match_fn(sequenceA[row], sequenceB[col])
            if not align_globally and score < 0:
                score_matrix[row][col] = 0
            else:
                score_matrix[row][col] = score
            trace_matrix[row][col] = best_index
            open_score = score_matrix[(row - 1)][(col - 1)] + first_B_gap
            extend_score = col_cache_score[(col - 1)] + extend_B
            open_score_rint, extend_score_rint = rint(open_score), rint(extend_score)
            if open_score_rint > extend_score_rint:
                col_cache_score[col - 1] = open_score
                col_cache_index[col - 1] = [(row - 1, col - 1)]
            elif extend_score_rint > open_score_rint:
                col_cache_score[col - 1] = extend_score
            else:
                col_cache_score[col - 1] = open_score
                if (row - 1, col - 1) not in col_cache_index[(col - 1)]:
                    col_cache_index[col - 1] = col_cache_index[(col - 1)] + [
                     (
                      row - 1, col - 1)]
            open_score = score_matrix[(row - 1)][(col - 1)] + first_A_gap
            extend_score = row_cache_score[(row - 1)] + extend_A
            open_score_rint, extend_score_rint = rint(open_score), rint(extend_score)
            if open_score_rint > extend_score_rint:
                row_cache_score[row - 1] = open_score
                row_cache_index[row - 1] = [(row - 1, col - 1)]
            elif extend_score_rint > open_score_rint:
                row_cache_score[row - 1] = extend_score
            else:
                row_cache_score[row - 1] = open_score
                if (row - 1, col - 1) not in row_cache_index[(row - 1)]:
                    row_cache_index[row - 1] = row_cache_index[(row - 1)] + [
                     (
                      row - 1, col - 1)]

    return (
     score_matrix, trace_matrix)


def _recover_alignments(sequenceA, sequenceB, starts, score_matrix, trace_matrix, align_globally, penalize_end_gaps, gap_char, one_alignment_only):
    lenA, lenB = len(sequenceA), len(sequenceB)
    tracebacks = []
    in_process = []
    for (score, (row, col)) in starts:
        if align_globally:
            (begin, end) = (None, None)
        else:
            begin, end = None, -max(lenA - row, lenB - col) + 1
            if not end:
                end = None
        in_process.append((
         sequenceA[0:0], sequenceB[0:0], score, begin, end,
         (
          lenA, lenB), (row, col)))
        if one_alignment_only:
            break

    while in_process and len(tracebacks) < MAX_ALIGNMENTS:
        (seqA, seqB, score, begin, end, prev_pos, next_pos) = in_process.pop()
        (prevA, prevB) = prev_pos
        if next_pos is None:
            prevlen = len(seqA)
            seqA = sequenceA[:prevA] + seqA
            seqB = sequenceB[:prevB] + seqB
            (seqA, seqB) = _lpad_until_equal(seqA, seqB, gap_char)
            if begin is None:
                if align_globally:
                    begin = 0
                else:
                    begin = len(seqA) - prevlen
            tracebacks.append((seqA, seqB, score, begin, end))
        else:
            (nextA, nextB) = next_pos
            nseqA, nseqB = prevA - nextA, prevB - nextB
            maxseq = max(nseqA, nseqB)
            ngapA, ngapB = maxseq - nseqA, maxseq - nseqB
            seqA = sequenceA[nextA:nextA + nseqA] + gap_char * ngapA + seqA
            seqB = sequenceB[nextB:nextB + nseqB] + gap_char * ngapB + seqB
            prev_pos = next_pos
            if not align_globally and score_matrix[nextA][nextB] <= 0:
                begin = max(prevA, prevB)
                in_process.append((
                 seqA, seqB, score, begin, end, prev_pos, None))
            else:
                for next_pos in trace_matrix[nextA][nextB]:
                    in_process.append((
                     seqA, seqB, score, begin, end, prev_pos, next_pos))
                    if one_alignment_only:
                        break

    return _clean_alignments(tracebacks)


def _find_start(score_matrix, sequenceA, sequenceB, gap_A_fn, gap_B_fn, penalize_end_gaps, align_globally):
    if align_globally:
        if penalize_end_gaps:
            starts = _find_global_start(sequenceA, sequenceB, score_matrix, gap_A_fn, gap_B_fn, 1)
        else:
            starts = _find_global_start(sequenceA, sequenceB, score_matrix, None, None, 0)
    else:
        starts = _find_local_start(score_matrix)
    return starts


def _find_global_start(sequenceA, sequenceB, score_matrix, gap_A_fn, gap_B_fn, penalize_end_gaps):
    nrows, ncols = len(score_matrix), len(score_matrix[0])
    positions = []
    for row in range(nrows):
        score = score_matrix[row][(ncols - 1)]
        if penalize_end_gaps:
            score += gap_B_fn(ncols, nrows - row - 1)
        positions.append((score, (row, ncols - 1)))

    for col in range(ncols - 1):
        score = score_matrix[(nrows - 1)][col]
        if penalize_end_gaps:
            score += gap_A_fn(nrows, ncols - col - 1)
        positions.append((score, (nrows - 1, col)))

    return positions


def _find_local_start(score_matrix):
    positions = []
    nrows, ncols = len(score_matrix), len(score_matrix[0])
    for row in range(nrows):
        for col in range(ncols):
            score = score_matrix[row][col]
            positions.append((score, (row, col)))

    return positions


def _clean_alignments(alignments):
    alignments = listfns.items(alignments)
    i = 0
    while i < len(alignments):
        (seqA, seqB, score, begin, end) = alignments[i]
        if end is None:
            end = len(seqA)
        elif end < 0:
            end = end + len(seqA)
        if begin >= end:
            del alignments[i]
            continue
        alignments[i] = (
         seqA, seqB, score, begin, end)
        i += 1

    return alignments


def _pad_until_equal(s1, s2, char):
    ls1, ls2 = len(s1), len(s2)
    if ls1 < ls2:
        s1 = _pad(s1, char, ls2 - ls1)
    elif ls2 < ls1:
        s2 = _pad(s2, char, ls1 - ls2)
    return (
     s1, s2)


def _lpad_until_equal(s1, s2, char):
    ls1, ls2 = len(s1), len(s2)
    if ls1 < ls2:
        s1 = _lpad(s1, char, ls2 - ls1)
    elif ls2 < ls1:
        s2 = _lpad(s2, char, ls1 - ls2)
    return (
     s1, s2)


def _pad(s, char, n):
    return s + char * n


def _lpad(s, char, n):
    return char * n + s


_PRECISION = 1000

def rint(x, precision=_PRECISION):
    return int(x * precision + 0.5)


class identity_match:
    """identity_match([match][, mismatch]) -> match_fn

    Create a match function for use in an alignment.  match and
    mismatch are the scores to give when two residues are equal or
    unequal.  By default, match is 1 and mismatch is 0.

    """

    def __init__(self, match=1, mismatch=0):
        self.match = match
        self.mismatch = mismatch

    def __call__(self, charA, charB):
        if charA == charB:
            return self.match
        return self.mismatch


class dictionary_match:
    """dictionary_match(score_dict[, symmetric]) -> match_fn

    Create a match function for use in an alignment.  score_dict is a
    dictionary where the keys are tuples (residue 1, residue 2) and
    the values are the match scores between those residues.  symmetric
    is a flag that indicates whether the scores are symmetric.  If
    true, then if (res 1, res 2) doesn't exist, I will use the score
    at (res 2, res 1).

    """

    def __init__(self, score_dict, symmetric=1):
        self.score_dict = score_dict
        self.symmetric = symmetric

    def __call__(self, charA, charB):
        if self.symmetric and not self.score_dict.has_key((charA, charB)):
            charB, charA = charA, charB
        return self.score_dict[(charA, charB)]


class affine_penalty:
    """affine_penalty(open, extend[, penalize_extend_when_opening]) -> gap_fn

    Create a gap function for use in an alignment.

    """

    def __init__(self, open, extend, penalize_extend_when_opening=0):
        if open > 0 or extend > 0:
            raise ValueError, 'Gap penalties should be non-positive.'
        self.open, self.extend = open, extend
        self.penalize_extend_when_opening = penalize_extend_when_opening

    def __call__(self, index, length):
        return calc_affine_penalty(length, self.open, self.extend, self.penalize_extend_when_opening)


def calc_affine_penalty(length, open, extend, penalize_extend_when_opening):
    if length <= 0:
        return 0
    penalty = open + extend * length
    if not penalize_extend_when_opening:
        penalty -= extend
    return penalty


def print_matrix(matrix):
    """print_matrix(matrix)

    Print out a matrix.  For debugging purposes.

    """
    matrixT = [ [] for x in range(len(matrix[0])) ]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrixT[j].append(len(str(matrix[i][j])))

    ndigits = map(max, matrixT)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            n = ndigits[j]
            print '%*s ' % (n, matrix[i][j]),

        print


def format_alignment(align1, align2, score, begin, end):
    """format_alignment(align1, align2, score, begin, end) -> string

    Format the alignment prettily into a string.

    """
    s = []
    s.append('%s\n' % align1)
    s.append('%s%s\n' % (' ' * begin, '|' * (end - begin)))
    s.append('%s\n' % align2)
    s.append('  Score=%g\n' % score)
    return ('').join(s)