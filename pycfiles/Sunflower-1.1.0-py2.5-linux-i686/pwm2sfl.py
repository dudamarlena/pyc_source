# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sunflower/pwm2sfl.py
# Compiled at: 2010-06-04 18:58:21
from __future__ import division, with_statement
__version__ = '$Revision: 457 $'
from math import log
import os, sys
from numpy import NINF, array, float64, log as alog
from path import path
from ._utils import DESC
from .hmm import ALPHABET, TF_START_SUFFIXES, LEN_ALPHABET, OFFSET_SILENT, OFFSET_UNBOUND, SPECIAL_STATE_NAMES, fill_array, optimize, save
GC_SET = set('GC')
PWM_LIST_FILENAME = 'matrix_list.txt'
PWM_EXT = 'pfm'
TF_START_FINAL_SUFFIXES = set(['0', 'r0'])
DEFAULT_GC_FRAC = 1.0 / LEN_ALPHABET * 2
PSEUDOCOUNT = 1.0
DEFAULT_PROB_SILENT2UNBOUND = 0.9
DEFAULT_COOP_DISTANCE = 22
DEFAULT_COOP_STRENGTH = 0.25
OUTPUT_FILENAME = 'jaspar.sfl'

class AppendableSet(set):

    def append(self, item):
        self.add(item)


class PwmInfo(object):

    def __init__(self, line):
        cols = line.rstrip().split('\t')
        (self.id, self.information_content, self.name, self.kind, other) = cols
        fields = other.lstrip('; ').split(' ; ')
        attribute_pairs = (field.split(' ') for field in fields)
        attribute_pairs_fmt = ((pair[0], self._fmt_attribute_value(pair[1:])) for pair in attribute_pairs)
        self.__dict__.update(dict(attribute_pairs_fmt))

    @staticmethod
    def _fmt_attribute_value(value):
        return (' ').join(value).strip('"')


def read_pwm(iterable):
    for line in iterable:
        yield map(float, line.rstrip().split())


def make_pwm_filename(dirpath, id):
    return os.extsep.join([dirpath / id, PWM_EXT])


def load_pwm(dirpath, id):
    filename = os.extsep.join([dirpath / id, PWM_EXT])
    with open(filename) as (infile):
        freq_pwm_list = list(read_pwm(infile))
    return array(freq_pwm_list)


def load_info(dirpath):
    filepath = dirpath / PWM_LIST_FILENAME
    with open(filepath) as (infofile):
        for line in infofile:
            yield PwmInfo(line)


def make_state_names(pwms, motif_infos):
    state_names = SPECIAL_STATE_NAMES[:]
    tf_start_offsets = []
    tf_end_offsets = []
    for (pwm, (name, dir_tag)) in zip(pwms, motif_infos):
        tf_length = pwm.shape[1]
        tf_start_offsets.append(len(state_names))
        state_names.extend((('.').join([name, '%s%d' % (dir_tag, index)]) for index in xrange(tf_length)))
        tf_end_offsets.append(len(state_names) - 1)

    return (state_names, tf_start_offsets, tf_end_offsets)


def attr_in_container(item, attr, container):
    """returns True if:
    * item does not have attr; or
    * attr is in container"""
    return not hasattr(item, attr) or getattr(item, attr) in container


def load_info_limited(dirpath, species_set, sysgroup_set):
    if not (species_set or sysgroup_set):
        for motif in load_info(dirpath):
            yield motif

    else:
        for motif in load_info(dirpath):
            if attr_in_container(motif, 'species', species_set) or attr_in_container(motif, 'sysgroup', sysgroup_set):
                yield motif


def load_pwms(dirname, species_set, sysgroup_set, revcom):
    pwms = []
    motif_infos = []
    dirpath = path(dirname)
    isatty = sys.stderr.isatty()
    for motif in load_info_limited(dirpath, species_set, sysgroup_set):
        row = [len(pwms), motif.id, motif.name, motif.kind]
        if isatty:
            print >> sys.stderr, ('\t').join(map(str, row))
        pwm = load_pwm(dirpath, motif.id)
        motif_name = motif.name
        pwms.append(pwm)
        if revcom:
            assert ALPHABET == 'ACGT'
            pwm_rev = pwm[::-1, ::-1]
            pwms.append(pwm_rev)
            motif_infos.append((motif_name, 'f'))
            motif_infos.append((motif_name, 'r'))
        else:
            motif_infos.append((motif_name, ''))

    (state_names, tf_start_offsets, tf_end_offsets) = make_state_names(pwms, motif_infos)
    return (
     pwms, state_names, tf_start_offsets, tf_end_offsets)


def add_cooperativity(model, coop_distance, coop_strength, probs_prior, logprobs_e_background, tf_start_offsets, tf_end_offsets):
    state_names = model['state_names']
    coop_offsets = []
    tf_coop_offsets = []
    for state_name in state_names[:]:
        state_name_partition = state_name.rpartition('.')
        suffix = state_name_partition[2]
        if suffix in TF_START_SUFFIXES:
            num_states = len(state_names)
            tf_coop_offsets.append(num_states)
            if suffix in TF_START_FINAL_SUFFIXES:
                coop_offsets.append(num_states)
                state_names.append('%s.c' % state_name_partition[0])

    num_states = len(state_names)
    logprobs_a_old = model['logprobs_transition']
    logprobs_e_old = model['logprobs_emission']
    logprobs_a = fill_array(NINF, (num_states, num_states))
    logprobs_e = fill_array(NINF, (num_states, LEN_ALPHABET))
    logprobs_a_old_shape = logprobs_a_old.shape
    logprobs_e_old_shape = logprobs_e_old.shape
    logprobs_a[:logprobs_a_old_shape[0], :logprobs_a_old_shape[1]] = logprobs_a_old
    logprobs_e[:logprobs_e_old_shape[0], :logprobs_e_old_shape[1]] = logprobs_e_old
    prob_coop2notcoop = 1.0 / coop_distance
    prob_coop2coop = 1.0 - prob_coop2notcoop
    prob_prior_unbound = probs_prior['unbound']
    silent_strength = 1.0 - coop_strength
    prob_coop2silent = prob_coop2notcoop * prob_prior_unbound * silent_strength
    prob_coop2alltfs = 1 - prob_coop2coop - prob_coop2silent
    prob_silent2alltfs = 1 - prob_prior_unbound
    logprob_coop2coop = log(prob_coop2coop)
    logprob_coop2silent = log(prob_coop2silent)
    for (coop_offset, tf_end_offset) in zip(tf_coop_offsets, tf_end_offsets):
        logprobs_a[(tf_end_offset, OFFSET_SILENT)] = NINF
        logprobs_a[(tf_end_offset, coop_offset)] = 0

    for coop_offset in coop_offsets:
        logprobs_a[(coop_offset, coop_offset)] = logprob_coop2coop
        logprobs_a[(coop_offset, OFFSET_SILENT)] = logprob_coop2silent
        for tf_start_offset in tf_start_offsets:
            prob_prior_tf = probs_prior[state_names[tf_start_offset]]
            prob_prior_tf_scaled = prob_prior_tf * prob_coop2alltfs
            prob_coop2tf = prob_prior_tf_scaled / prob_silent2alltfs
            logprobs_a[(coop_offset, tf_start_offset)] = log(prob_coop2tf)

    logprobs_e[coop_offsets] = logprobs_e_background
    model.update(state_names=state_names, logprobs_transition=logprobs_a, logprobs_emission=logprobs_e)


def get_priors(prob_silent2unbound, state_names, tf_start_offsets, num_tfs, filename, revcom):
    probs_prior = {}
    if filename:
        prior_init = {}
        with open(filename) as (infile):
            for line in infile:
                tokens = line.split()
                if len(tokens) == 2:
                    prior_init[tokens[0]] = float(tokens[1])

        total = sum(prior_init.values())
        if total != 1.0:
            for key in prior_init.keys():
                prior_init[key] = prior_init[key] / total

        probs_prior['unbound'] = prior_init['unbound']
        for tf_start_offset in tf_start_offsets:
            tf_initial_state_name = state_names[tf_start_offset]
            if revcom:
                prior_init_all = prior_init[tf_initial_state_name[:-3]]
                probs_prior[tf_initial_state_name] = prior_init_all / 2
            else:
                prior_init_all = prior_init[tf_initial_state_name[:-2]]
                probs_prior[tf_initial_state_name] = prior_init_all

    probs_prior['unbound'] = prob_silent2unbound
    for tf_start_offset in tf_start_offsets:
        tf_state_name = state_names[tf_start_offset]
        probs_prior[tf_state_name] = (1 - prob_silent2unbound) / num_tfs

    return probs_prior


def pwm2sfl(dirname, prob_silent2unbound, priors, coop, coop_distance, coop_strength, revcom, species_set, sysgroup_set, gc_frac, output_filename=None):
    (pwms, state_names, tf_start_offsets, tf_end_offsets) = load_pwms(dirname, species_set, sysgroup_set, revcom)
    num_states = len(state_names)
    num_tfs = len(tf_start_offsets)
    probs_prior = get_priors(prob_silent2unbound, state_names, tf_start_offsets, num_tfs, priors, revcom)
    logprobs_a = fill_array(NINF, (num_states, num_states))
    logprobs_e = fill_array(NINF, (num_states, LEN_ALPHABET))
    logprobs_a_silent = logprobs_a[OFFSET_SILENT]
    logprobs_a_silent[OFFSET_SILENT] = NINF
    logprobs_a_silent[OFFSET_UNBOUND] = log(probs_prior['unbound'])
    for tf_start_offset in tf_start_offsets:
        tf_state_name = state_names[tf_start_offset]
        logprobs_a_silent[tf_start_offset] = log(probs_prior[tf_state_name])

    assert ALPHABET == 'ACGT'
    logprobs_e_background = [
     0.0] * LEN_ALPHABET
    for i in xrange(LEN_ALPHABET):
        base = ALPHABET[i]
        if base in GC_SET:
            logprobs_e_background[i] = log(gc_frac / 2.0)
        else:
            logprobs_e_background[i] = log((1 - gc_frac) / 2.0)

    logprobs_a[(OFFSET_UNBOUND, OFFSET_SILENT)] = 0
    logprobs_e[OFFSET_UNBOUND] = logprobs_e_background
    for offset in xrange(tf_start_offsets[0], num_states):
        if offset in tf_end_offsets:
            logprobs_a[(offset, OFFSET_SILENT)] = 0
        else:
            logprobs_a[(offset, offset + 1)] = 0

    for (pwm, offset) in zip(pwms, tf_start_offsets):
        for (index, col) in enumerate(pwm.transpose()):
            pseudocol = array(col + PSEUDOCOUNT, dtype=float64)
            total_counts = pseudocol.sum()
            logprobs_e[offset + index] = alog(pseudocol / total_counts)

    model = dict(alphabet=ALPHABET, desc=DESC, state_names=state_names, logprobs_transition=logprobs_a, logprobs_emission=logprobs_e)
    if coop:
        add_cooperativity(model, coop_distance, coop_strength, probs_prior, logprobs_e_background, tf_start_offsets, tf_end_offsets)
    optimize(model)
    save(output_filename, model)


def add_optgroup_input_limiters(parser):
    from ._optparse import OptionGroup
    with OptionGroup(parser, 'Input limiters') as (group):
        group.add_option('-s', '--species', action='append', default=AppendableSet(), metavar='SPECIES', help='include matrices marked from SPECIES')
        group.add_option('-S', '--sysgroup', action='append', default=AppendableSet(), metavar='SYSGROUP', help='include matrices marked from SYSGROUP')


def parse_options(args):
    from ._optparse import OptionGroup, OptionParser
    usage = '%prog [OPTION...] MATRIXDIR'
    version = '%%prog %s' % __version__
    parser = OptionParser(usage=usage, version=version)
    add_optgroup_input_limiters(parser)
    with OptionGroup(parser, 'Model parameters') as (group):
        group.add_option('-r', '--revcom', action='store_true', help='add reverse complement of all PWMs to model')
        group.add_option('-u', '--unbound', type=float, default=DEFAULT_PROB_SILENT2UNBOUND, metavar='PROB', help='prior probability of unbound state (default %s)' % DEFAULT_PROB_SILENT2UNBOUND)
        group.add_option('-p', '--priors', metavar='FILE', help='file containing prior probabilities of unbound state and for bound states for different transcription factors (supersedes --unbound)')
        group.add_option('-g', '--gc', type=float, default=DEFAULT_GC_FRAC, metavar='GC', help='G+C content between 0 and 1 (default %s)' % DEFAULT_GC_FRAC)
    with OptionGroup(parser, 'Cooperativity parameters') as (group):
        group.add_option('-c', '--coop', action='store_true', help='build model with cooperativity states')
        group.add_option('-d', '--coop-distance', type=float, default=DEFAULT_COOP_DISTANCE, help='Mean distance at which co-operativity is effective; used to calculate P(coop->coop) (default %s)' % DEFAULT_COOP_DISTANCE)
        group.add_option('-t', '--coop-strength', type=float, default=DEFAULT_COOP_STRENGTH, help='percentage increase in prior probability of transitioning from an unbound cooperative state to a bound state, compared to prior probability of transitioning from unbound, non-cooperative state to a bound state (range (0-1), default %s)' % DEFAULT_COOP_STRENGTH)
    with OptionGroup(parser, 'Output') as (group):
        group.add_option('-o', '--output', default=OUTPUT_FILENAME, metavar='FILE', help='output model to FILE (default %s)' % OUTPUT_FILENAME)
    (options, args) = parser.parse_args(args)
    if len(args) != 1:
        parser.print_usage()
        sys.exit(1)
    if not 0 < options.coop_strength < 1:
        print '--coop-strength must be between 0 and 1 exclusive'
        parser.print_usage()
        sys.exit(1)
    if not 0 < options.gc < 1:
        print '--gc must be between 0 and 1 exclusive'
        parser.print_usage()
        sys.exit(1)
    return (options, args)


def main(args=sys.argv[1:]):
    (options, args) = parse_options(args)
    return pwm2sfl(output_filename=options.output, prob_silent2unbound=options.unbound, priors=options.priors, coop=options.coop, coop_distance=options.coop_distance, coop_strength=options.coop_strength, revcom=options.revcom, species_set=options.species, gc_frac=options.gc, sysgroup_set=options.sysgroup, *args)


if __name__ == '__main__':
    sys.exit(main())