# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sunflower/recompose.py
# Compiled at: 2009-04-08 21:11:50
from __future__ import division
__version__ = '$Revision: 425 $'
from collections import defaultdict
import sys
from numpy import array, float64, log as alog
from ._utils import DESC
from .hmm import ALPHABET, adjust, load, save
PSEUDOCOUNT = 1

def add_pseudocount(n=0):
    return n + PSEUDOCOUNT


def cols2counts(cols):
    labels = cols[::2]
    count_generator = (add_pseudocount(int(col)) for col in cols[1::2])
    counts = defaultdict(add_pseudocount, zip(labels, count_generator))
    return array([ counts[letter] for letter in ALPHABET ])


def load_fastacomposition(filename):
    line = iter(open(filename)).next()
    return line.rstrip().split()[1:]


def calc_logprobs_emission(counts):
    counts_float = array(counts, dtype=float64)
    return alog(counts_float / counts.sum())


def cols2logprobs_emission(cols):
    return calc_logprobs_emission(cols2counts(cols))


def recompose(composition_filename, infilename, outfilename, resource=False):
    cols = load_fastacomposition(composition_filename)
    logprobs_emission = cols2logprobs_emission(cols)
    model = load(infilename, resource)
    adjust(model, logprobs_emission)
    model['desc'] = ('; ').join([model['desc'], DESC])
    save(outfilename, model)


def parse_options(args):
    from optparse import OptionParser
    usage = '%prog [OPTION]... FASTACOMPOSITION IN-SFL OUT-SFL'
    version = '%%prog %s' % __version__
    parser = OptionParser(usage=usage, version=version)
    parser.add_option('-R', '--resource', action='store_true', help='get IN-SFL from a resource that comes with the Sunflower distribution instead of a file')
    (options, args) = parser.parse_args(args)
    if not len(args) == 3:
        parser.print_usage()
        sys.exit(1)
    return (options, args)


def main(args=sys.argv[1:]):
    (options, args) = parse_options(args)
    return recompose(resource=options.resource, *args)


if __name__ == '__main__':
    sys.exit(main())