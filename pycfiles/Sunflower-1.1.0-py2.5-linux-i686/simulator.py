# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sunflower/simulator.py
# Compiled at: 2009-07-09 16:24:34
from __future__ import division, with_statement
__version__ = '$Revision: 446 $'
from collections import defaultdict
from itertools import count, izip
from math import log
import re, sys
from numpy import allclose, array, empty, empty_like, exp as aexp, isfinite, index_exp, intp, float64, ndarray, zeros
from textinput import open as _open
from ._fwd_bwd import fwd, bwd
from ._poly import chunk
from ._utils import FastaIterator, enum
from .driver import defline_identifier, load as driver_load
from .hmm import ALPHABET, ALPHABET_INT, LEN_ALPHABET, get_params, load as hmm_load
ALPHABET_ENUM = enum(ALPHABET)
LN_2 = log(2)

def accum_sum_relent_ref_mut(probs_ref, logprobs_ref, logprobs_mut, mask_nonzero_prob_cols):
    logprobs_ref_masked = logprobs_ref[mask_nonzero_prob_cols]
    logprobs_mut_masked = logprobs_mut[mask_nonzero_prob_cols]
    probs_ref_masked = probs_ref[mask_nonzero_prob_cols]
    ref_mut_bits = (logprobs_ref_masked - logprobs_mut_masked) / LN_2
    return (probs_ref_masked * ref_mut_bits).sum()


def seq2int(seq):
    res = [
     -1] + [ ALPHABET_ENUM[char] for char in seq.upper() ]
    return intp(res)


def match_names(pattern, names):
    """
    returns indexes_match, names_match
    """
    regex = re.compile(pattern)
    matchfunc = regex.search
    zipped = ((index, name) for (index, name) in enumerate(names) if matchfunc(name))
    return tuple((array(x) for x in zip(*zipped)))


def load_seqrecords(seq_filename, include, exclude):
    res = []
    if seq_filename is None:
        return res
    excluded_ids = set(exclude)
    included_ids = set(include)
    with _open(seq_filename) as (seq_file):
        for (defline, seq) in FastaIterator(seq_file):
            identifier = defline_identifier(defline)
            if not included_ids or identifier in included_ids:
                if identifier not in excluded_ids:
                    res.append((defline, seq))

    if not res:
        print >> sys.stderr, 'no matching sequences'
        sys.exit(2)
    return res


def _assert_fwd_bwd_results(f, b, logprob_tf, logprob_tb):
    assert allclose(logprob_tf, logprob_tb)
    arr = f[1:, 1:] + b[1:, 1:]
    arr -= logprob_tf
    aexp(arr, arr)
    assert allclose(arr.sum(-1), 1.0)


def fwd_bwd(f, b, x, (a, e, cf, cb), cells_keep=index_exp[:], start=0):
    """
    start allows you to avoid repeating all of the fwd and bwd calculations
    after a mutation
    """
    logprob_tf = fwd(f, x, a, e, cf, start)
    logprob_tb = bwd(b, x, a, e, cb, start)
    _assert_fwd_bwd_results(f, b, logprob_tf, logprob_tb)
    logprobs = f[cells_keep] + b[cells_keep] - logprob_tf
    return aexp(logprobs)


def fwd_bwd_log(f, b, x, (a, e, cf, cb), start=0):
    """
    returns log values instead of exp'd
    doesn't support cells_keep
    """
    logprob_tf = fwd(f, x, a, e, cf, start)
    logprob_tb = bwd(b, x, a, e, cb, start)
    _assert_fwd_bwd_results(f, b, logprob_tf, logprob_tb)
    return f + b - logprob_tf


def simulate_mutations(f, b, x, model_params, rows_keep, groupings):
    assert rows_keep.step is None
    if not rows_keep.start:
        rows_keep = slice(1, rows_keep.stop)
    x_keep_range = range(len(x))[rows_keep]
    x_keep = x[rows_keep]
    shape = (
     len(x_keep_range), LEN_ALPHABET)
    res = zeros(shape, dtype=float64)
    logprobs_ref = fwd_bwd_log(f, b, x, model_params)
    probs_ref = aexp(logprobs_ref)
    mask_nonzero_prob_cols = isfinite(logprobs_ref.sum(1))
    x_mut = x.copy()
    f_mut = empty_like(f)
    i_first_minus1 = x_keep_range[0] - 1
    f_mut[:i_first_minus1] = f[:i_first_minus1]
    for (res_index, i, x_i) in izip(count(), x_keep_range, x_keep):
        f_mut[i - 1] = f[(i - 1)]
        for x_i_mut in ALPHABET_INT:
            if x_i_mut == x_i:
                continue
            x_mut[i] = x_i_mut
            logprobs_mut = fwd_bwd_log(f_mut, b, x_mut, model_params, i)
            res[(res_index, x_i_mut)] = accum_sum_relent_ref_mut(probs_ref, logprobs_ref, logprobs_mut, mask_nonzero_prob_cols)

        x_mut[i] = x_i

    return res


def regroup_probs(probs, groupings):
    shape = (
     probs.shape[0], len(groupings))
    res = empty(shape, probs.dtype)
    for (grouping_index, grouping) in enumerate(groupings):
        res[:, grouping_index] = probs[:, grouping].sum(1)

    return res


def simulate_diff(f, b, x, model_params, rows_keep, groupings):
    (x, x_mut) = x
    assert rows_keep.start == 1 and rows_keep.stop is None and rows_keep.step is None
    logprobs_ref = fwd_bwd_log(f, b, x, model_params)
    probs_ref = aexp(logprobs_ref)
    logprobs_mut = fwd_bwd_log(f, b, x_mut, model_params)
    mask_nonzero_prob_cols = isfinite(logprobs_ref.sum(1))
    return accum_sum_relent_ref_mut(probs_ref, logprobs_ref, logprobs_mut, mask_nonzero_prob_cols)


def simulate_reference(f, b, x, model_params, cells_keep, groupings):
    probs = fwd_bwd(f, b, x, model_params, cells_keep)
    if groupings:
        return regroup_probs(probs, groupings)
    else:
        return probs


def simulate_seq(simulate_func, driver, model_params, num_states, seqrecord, cells_keep, groupings):
    (defline, seq) = seqrecord
    if isinstance(seq, ndarray):
        assert len(seq) == 2
        x = [ seq2int(seq_inner) for seq_inner in seq ]
        f_shape = (
         len(x[0]), num_states)
        assert f_shape[0] == len(x[1])
    else:
        x = seq2int(seq)
        f_shape = (len(x), num_states)
    f = empty(f_shape, dtype=float64)
    b = empty(f_shape, dtype=float64)
    outarray = simulate_func(f, b, x, model_params, cells_keep, groupings)
    driver(outarray, seqrecord)


def correct_limit_slice(limit_slice):
    limit_start = limit_slice.start
    limit_stop = limit_slice.stop
    if not limit_start:
        limit_start = 1
    elif limit_start > 0:
        limit_start += 1
    if limit_stop >= 0:
        limit_stop += 1
    return slice(limit_start, limit_stop, limit_slice.step)


def group_stems(names):
    """
    returns a defaultdict:

    keys: group stem names
    values: matching indexes
    """
    res = defaultdict(list)
    for (index, name) in enumerate(names):
        name = name.rpartition('.')[0] or name
        res[name].append(index)

    return res


def make_groupings(colnames):
    groups = group_stems(colnames)
    groupings = []
    colnames = []
    for (colname, col_indexes) in groups.iteritems():
        groupings.append(col_indexes)
        colnames.append(colname)

    return (groupings, array(colnames))


def simulator(hmm_filename, seq_filename, args, driver_class=None, simulate_func=simulate_reference, keep_pattern=None, include=[], exclude=[], resource=False, start_default=None, write_seq=True, limit_slice=None, total_stems=False, seq2_filename=None):
    model = hmm_load(hmm_filename, resource)
    num_states = model['num_states']
    alphabet = model['alphabet']
    emitting_states = model['emitting_states']
    assert alphabet == ALPHABET
    assert emitting_states == range(1, num_states)
    state_names = model['state_names']
    model_params = get_params(model)
    seqrecords = load_seqrecords(seq_filename, include, exclude)
    assert seqrecords
    seqrecords2 = load_seqrecords(seq2_filename, include, exclude)
    seqrecords2_dict = dict(((defline_identifier(defline), seq) for (defline, seq) in seqrecords2))
    assert not simulate_func == simulate_diff or seqrecords2_dict
    limit_slice_adj = correct_limit_slice(limit_slice)
    groupings = None
    if simulate_func == simulate_reference:
        measurement = 'prob'
        (cols_keep, colnames) = match_names(keep_pattern, state_names)
        if total_stems:
            (groupings, colnames) = make_groupings(colnames)
        cells_keep = (limit_slice_adj, cols_keep)
    else:
        measurement = 'sum_relent_ref_mut'
        cells_keep = limit_slice_adj
        colnames = array(ALPHABET)
    driver = driver_class(args, colnames, measurement, write_seq, start_default, limit_slice)
    with driver as (driver):
        for seqrecord in chunk(seqrecords):
            (defline, seq) = seqrecord
            if seqrecords2_dict:
                seq2 = seqrecords2_dict[defline_identifier(defline)]
                seqrecord = (
                 defline, array([seq, seq2]))
            try:
                simulate_seq(simulate_func, driver, model_params, num_states, seqrecord, cells_keep, groupings)
            except KeyError:
                msg = '%s contains illegal characters; skipping' % defline
                print >> sys.stderr, msg

    return


def parse_options(args):
    from ._optparse import OptionGroup, OptionParser
    usage = '%prog [OPTION...] MODEL SEQFILE OUTFILE\n       %prog [OPTION...] --driver=DRIVER MODEL SEQFILE [DRIVEROPTIONS...]'
    version = '%%prog %s' % __version__
    parser = OptionParser(usage=usage, version=version)
    parser.disable_interspersed_args()
    with OptionGroup(parser, 'Model') as (group):
        group.add_option('-R', '--resource', action='store_true', help='get MODEL from a resource that comes with the sunflower distribution instead of a file')
    with OptionGroup(parser, 'Sequence') as (group):
        group.add_option('-i', '--include', action='append', default=[], metavar='IDENTIFIER', help='run only on IDENTIFIER')
        group.add_option('', '--include-from', action='load', dest='include', metavar='FILE', help='run only on specified identifiers from FILE')
        group.add_option('-x', '--exclude', action='append', default=[], metavar='IDENTIFIER', help="don't run on IDENTIFIER")
        group.add_option('', '--exclude-from', action='load', dest='exclude', metavar='FILE', help="don't run on specified identifiers from FILE")
    with OptionGroup(parser, 'Comparison mode') as (group):
        group.add_option('-m', '--mutate', action='store_const', dest='simulator', const=simulate_mutations, default=simulate_reference, help='iteratively mutate input sequences')
        group.add_option('-2', '--diff', metavar='SEQFILE2', help='compute difference between sequences in SEQFILE and SEQFILE2')
    with OptionGroup(parser, 'Output options') as (group):
        group.add_option('-s', '--start', type=int, metavar='POS', help='call the first position POS')
        group.add_option('-S', '--states', metavar='REGEX', default='^(?!silent$)', help='only write states matching REGEX')
        group.add_option('--separate-state-groups', action='store_true', help="don't add together .f0, .f1, .r0, etc.")
        group.add_option('-r', '--range', type=slice, metavar='SLICE', default=slice(None), help='only write positions in SLICE (ignores start values)')
        group.add_option('--no-sequence', action='store_true', help="don't write seq attribute of output (saves space)")
    with OptionGroup(parser, 'Output driver') as (group):
        group.add_option('-d', '--driver', default='DEFAULT', help='set output format')
        group.add_option('--driver-help', action='store_true', help='get driver-specific help')
    (options, args) = parser.parse_args(args)
    if options.driver_help:
        driver_class = driver_load(options.driver)
        driver_class.print_help()
        sys.exit(0)
    if not len(args) >= 2:
        parser.print_usage()
        sys.exit(1)
    return (options, args)


def main(args=sys.argv[1:]):
    (options, args) = parse_options(args)
    driver_class = driver_load(options.driver)
    hmm_filename = args[0]
    seq_filename = args[1]
    if options.diff:
        assert options.simulator == simulate_reference
        options.simulator = simulate_diff
    return simulator(hmm_filename, seq_filename, args[2:], simulate_func=options.simulator, driver_class=driver_class, keep_pattern=options.states, include=options.include, exclude=options.exclude, resource=options.resource, start_default=options.start, limit_slice=options.range, write_seq=not options.no_sequence, total_stems=not options.separate_state_groups, seq2_filename=options.diff)


if __name__ == '__main__':
    sys.exit(main())