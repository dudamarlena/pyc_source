# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Topics/visualization/compute_ngrams.py
# Compiled at: 2013-03-09 13:40:06
import turbotopics as tt, sys
from pprint import *

def main(corpus_file, pvalue, use_perm, out_filename, min_count=5, min_bigram_count=5, min_char_count=3):
    """recursively find collocations for a given corpus.  writes out
    the marginal counts to a specified file"""
    sys.stdout.write('computing n-grams from %s\n' % corpus_file)
    corpus = file(corpus_file).readlines()
    lr = tt.LikelihoodRatio(pvalue=pvalue, use_perm=use_perm)

    def iter_gen():
        return corpus

    char_filter = tt.make_char_filter(min_char_count)

    def my_filter(w):
        char_filter(w) and tt.stop_filter(w) and tt.digit_filter(w)

    def update_fun(count, doc):
        count.update_counts(doc, root_filter=tt.stop_filter)

    cnts = tt.nested_sig_bigrams(iter_gen, update_fun, lr, min_count)
    sys.stdout.write('writing to %s\n' % out_filename)
    f = file(out_filename, 'w')
    [ f.write('%s|%g\n' % (term, count)) for term, count in sorted(cnts.marg.items(), key=lambda x: -x[1])
    ]
    f.close()
    return cnts


if __name__ == '__main__':
    from optparse import *
    parser = OptionParser()
    parser.add_option('--corpus', type='string', dest='corpus')
    parser.add_option('--perm', action='store_true', dest='use_perm')
    parser.add_option('--pval', type='float', dest='p_value')
    parser.add_option('--out', type='string', dest='out_filename')
    parser.add_option('--min-count', type='float', dest='min_count')
    parser.set_defaults(min_count=5)
    opt, args = parser.parse_args()
    main(corpus=opt.corpus, p_value=opt.p_value, use_perm_test=opt.use_perm, out_filename=opt.out_filename, min_count=opt.min_count)