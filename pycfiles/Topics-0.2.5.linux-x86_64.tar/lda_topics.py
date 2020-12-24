# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Topics/visualization/lda_topics.py
# Compiled at: 2013-03-10 05:54:10
import turbotopics as tt, re
from sys import stdout
from itertools import izip

def read_vocab(vocab_fname):
    """reads a vocabulary and returns a map of words to indices
    :param vocab_fname: file name for vocabulary list
    """
    stdout.write('reading vocabulary from %s\n' % vocab_fname)
    with open(vocab_fname) as (f):
        terms = f.read().split('\n')
    return terms


def parse_word_assignments(assigns_fname, vocab):
    """
    Given a word assignments file and a list of words,
    returns a list of dictionaries mapping words to topics
    :param assigns_fname: Filename of file with assignment of terms to topics
    :param vocab: list with vocabulary
    """
    results = []
    with open(assigns_fname) as (f):
        for assign in f:
            wordmap = {}
            for term, topic in [ x.split(':') for x in assign.split(' ')[1:] ]:
                wordmap[vocab[int(term)]] = int(topic)

            results.append(wordmap)

    return results


def update_counts_from_topic(doc, topicmap, topic, counts_obj):
    """
    updates the counts of a counts object from a
    :param doc: line of text
    :param topicmap: mapping of words to topics
    :param topic: integer of the topic to focus on
    :param counts_obj: counts object to update
    """
    if topic not in topicmap.values():
        return
    root_filter = lambda w: topicmap.get(w.split()[0], -1) == topic
    counts_obj.update_counts(doc, root_filter=root_filter)


def turbo_topic(corpus, assigns, topic, use_perm=False, pvalue=0.1, min=25):

    def iter_gen():
        return izip(corpus, assigns)

    def update_fun(counts, doc):
        update_counts_from_topic(doc[0], doc[1], topic, counts)

    test = tt.LikelihoodRatio(pvalue, use_perm=use_perm)
    cnts = tt.nested_sig_bigrams(iter_gen, update_fun, test, min)
    return cnts


if __name__ == '__main__':
    from optparse import *
    parser = OptionParser()
    parser.add_option('--corpus', type='string', dest='corpus')
    parser.add_option('--assign', type='string', dest='assignments')
    parser.add_option('--vocab', type='string', dest='vocab')
    parser.add_option('--perm', action='store_true', dest='use_perm')
    parser.add_option('--pval', type='float', dest='pvalue')
    parser.add_option('--out', type='string', dest='out')
    parser.add_option('--min-count', type='float', dest='min_count')
    parser.add_option('--ntopics', type='int', dest='ntopics')
    parser.set_defaults(min_count=25, use_perm=False, pval=0.001)
    opt, args = parser.parse_args()
    vocab = read_vocab(opt.vocab)
    assigns = parse_word_assignments(opt.assignments, vocab)
    corpus = file(opt.corpus).readlines()
    for topic in range(opt.ntopics):
        stdout.write('writing topic %d\n' % topic)
        sig_bigrams = turbo_topic(corpus, assigns, topic, use_perm=opt.use_perm, min=opt.min_count, pvalue=opt.pvalue)
        tt.write_vocab(sig_bigrams.marg, '%stopic%03d.txt' % (opt.out, topic))