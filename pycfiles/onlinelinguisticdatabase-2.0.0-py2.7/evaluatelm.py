# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/lib/simplelm/evaluatelm.py
# Compiled at: 2016-09-19 13:27:02
import re, codecs, logging
log = logging.getLogger(__name__)

class LMTree:
    """A simple trie structure suitable for representing a standard
    statistical language model.

    Each node stores a variety of useful information:

        * ngram:     The word ID for this node
        * prob:      The (log_10) probability for this node
        * bow:       The backoff weight for this node - if any
        * parent:    A pointer to the parent node - if any
        * children:  A hash of child-nodes - if any
                      - This encodes higher-order Ngrams

    Two public methods are also implemented:

        * add_child(ngram, prob=0.0, bow=0.0)
            Create a new child node, an instance of LMTree, and
            add it to the hash of children for this node.

        * get_ngram_p(ngram, i=0)
            Recursive method for retrieving the probability
            or backoff weight for an input ngram. 

    """

    def __init__(self, ngram, prob=0.0, bow=0.0, parent=None, max_order=None):
        self.ngram = ngram
        self.prob = prob
        self.bow = bow
        self.parent = parent
        self.max_order = max_order
        self.children = {}

    def add_child(self, ngram, prob=0.0, bow=0.0):
        """Create a new child node, an instance of LMTree, and add it to the hash
        of children for this node.

        """
        if len(ngram) == 1:
            if ngram[0] in self.children:
                return
            self.children[ngram[0]] = LMTree(ngram[0], prob, bow, self)
        else:
            n0 = ngram.pop(0)
            if n0 in self.children:
                self.children[n0].add_child(ngram, prob, bow)
            else:
                self.children[n0] = LMTree(n0, 0.0, 0.0, self)
                self.children[n0].add_child(ngram, prob, bow)

    def get_ngram_p(self, ngram, i=0):
        """Recursive method for retrieving the probability or backoff weight for
        an input ngram. If the ngram exists, the probability is returned.
        If not, the backoff weight for the highest order ngram prefix of the
        input is returned. Also returns a boolean value indicating whether
        the first parameter is a prob or bow.

        """
        if i == len(ngram):
            return (self.prob, True)
        else:
            if ngram[i] in self.children:
                return self.children[ngram[i]].get_ngram_p(ngram, i + 1)
            return (self.bow, False)


def load_arpa(arpa_file, encoding=None):
    """Load an ARPA format LM into a simple trie structure."""
    arpalm = LMTree('<start>')
    order = max_order = 0
    for line in codecs.open(arpa_file, encoding=encoding):
        line = line.strip()
        if line.startswith('ngram'):
            max_order = int(re.sub('^ngram\\s+(\\d+)=.*$', '\\1', line))
        if order > 0 and not line.startswith('\\') and not line == '':
            parts = line.split('\t')
            words = parts[1].split(' ')
            if order < max_order:
                if len(parts) == 3:
                    arpalm.add_child(words, float(parts[0]), float(parts[(-1)]))
                else:
                    arpalm.add_child(words, float(parts[0]), 0.0)
            else:
                arpalm.add_child(words, float(parts[0]))
        if re.match('^\\\\\\d+', line):
            line = re.sub('^\\\\(\\d+).*$', '\\1', line)
            order = int(line)

    arpalm.max_order = max_order
    return arpalm


def compute_sentence_prob(arpalm, sentence):
    """Compute the probability of the input sentence.
    Should produce the same output as the SRILM ngram tool,

        $ ngram -lm test.arpa -ppl sent.txt

    or the NGramLibrary ngramapply tool, to within a delta of about 1e-7.
    Longer sentences may diverge further due to rounding.

    """
    total = 0.0
    ngram = [
     sentence.pop(0)]
    while len(sentence) > 0:
        ngram.append(sentence.pop(0))
        p, is_prob = arpalm.get_ngram_p(ngram)
        total += p
        while is_prob == False:
            ngram.pop(0)
            p, is_prob = arpalm.get_ngram_p(ngram)
            total += p

    return total


def retrieve_ngram_prob(arpalm, sentence):
    """Retrieve an individual ngram probability.
    """
    total = 0.0
    if len(sentence) == 1:
        p, is_prob = arpalm.get_ngram_p(sentence[0])
        return p
    ngram = []
    pr = 0.0
    while len(ngram) < arpalm.max_order and len(sentence) > 0:
        ngram.append(sentence.pop(0))
        pr, is_prob = arpalm.get_ngram_p(ngram)
        if is_prob == False:
            sentence.insert(0, ngram.pop(-1))
            break

    while len(sentence) > 0:
        ngram.append(sentence.pop(0))
        p, is_prob = arpalm.get_ngram_p(ngram)
        total += float(p)
        while is_prob == False:
            ngram.pop(0)
            p, is_prob = arpalm.get_ngram_p(ngram)
            total += float(p)

    if total == 0.0:
        total = pr
    return total


def history_sum(arpalm, ngram_hist):
    """Compute the sum for a given history.

    This will perform a sum over all n+1 grams starting with ngram_hist,
    as well as any backoff probs for items in the vocabulary that do NOT
    occur as an extension of ngram_hist.

    The result should always be 1.0~ unless the NGram ends in </s>.

    """
    from math import pow
    vocab = set(arpalm.children.keys())
    total = 0.0
    for word in vocab:
        ngram = [ w for w in ngram_hist ]
        ngram.append(word)
        total += pow(10, retrieve_ngram_prob(arpalm, ngram))

    return total


def lm_is_normalized(arpalm_file, delta=1e-06, encoding=None):
    """Determine whether the model is fully normalized.

    First, for the zero-th order, compute the unigram sum.
    Next, for each ngram order o < max_order, compute the history_sum.

    If the absolute value,  abs(1-hist_sum) < delta, then count
    the history as normalized.  Otherwise throw a ValueError and quit.

    """
    from math import pow
    order = 0
    arpalm = load_arpa(arpalm_file, encoding)
    total = 0.0
    for word in arpalm.children.keys():
        total += pow(10.0, float(arpalm.children[word].prob))

    if abs(1.0 - total) > delta:
        print total, delta, 1.0 - total
        raise ValueError, 'The unigram model is not fully normalized!'
    total = 0.0
    for line in codecs.open(arpalm_file, encoding):
        line = line.strip()
        if order > 0 and not line.startswith('\\') and not line == '':
            parts = line.split('\t')
            ngram = parts[1].split(' ')
            total += pow(10.0, history_sum(arpalm, ngram))
        if re.match('^\\\\\\d+', line):
            if order > 0 and 1 - total > delta:
                raise ValueError, 'The %d-order model is not fully normalized!' % order
            order = int(re.sub('^\\\\(\\d+).*$', '\\1', line))
            if order == arpalm.max_order:
                return True
            total = 0.0


if __name__ == '__main__':
    import sys, argparse
    example = '%s --arpalm lm.arpa --sent "some sentence to evaluate" ' % sys.argv[0]
    parser = argparse.ArgumentParser(description=example)
    parser.add_argument('--arpalm', '-m', help='The ARPA format language model to be used.', required=True)
    parser.add_argument('--sent', '-s', help='The input sentence/sequence to be evaluated.', required=False, default='')
    parser.add_argument('--sb', '-b', help='The sentence begin token. (<s>)', default='<s>', required=False)
    parser.add_argument('--se', '-e', help='The sentence end token. (</s>)', default='</s>', required=False)
    parser.add_argument('--nosbse', '-n', help="Don't add sentence-begin/sentence-end tokens to the input.", default=False, action='store_true')
    parser.add_argument('--hist_sum', '-i', help='Compute the sum for a given history.  History must be in the model.', default=False, action='store_true')
    parser.add_argument('--get_ngram', '-g', help='Retrieve an individual NGram probability. Length of the NGrm  must be <= the max order of the input LM.', default=False, action='store_true')
    parser.add_argument('--delta', '-d', help='Delta for determining normalization success/failure.', type=float, default=1e-06, required=False)
    parser.add_argument('--verbose', '-v', help='Verbose mode.', action='store_true', default=False)
    args = parser.parse_args()
    if args.verbose:
        for attr, value in args.__dict__.iteritems():
            print attr, '=', value

    if args.sent == '':
        print lm_is_normalized(args.arpalm, delta=args.delta)
    else:
        arpalm = load_arpa(args.arpalm)
        tokens = args.sent.split(' ')
        for token in tokens:
            if token not in arpalm.children:
                raise ValueError, 'Unigram token: %s not found in LM vocabulary!' % token

        if args.get_ngram:
            if len(tokens) > arpalm.max_order:
                print 'Sequence:', tokens, 'is longer than the max order of the input model!'
                sys.exit(1)
            print 'NGram:', tokens
            print 'NGram prob:', retrieve_ngram_prob(arpalm, tokens)
        elif args.hist_sum:
            print history_sum(arpalm, args.sent.split(' '))
        else:
            if args.nosbse:
                print 'Not adding sentence-begin/sentence-end tokens.'
            else:
                if not tokens[0] == args.sb:
                    tokens.insert(0, args.sb)
                if not tokens[(-1)] == args.se:
                    tokens.append(args.se)
            print 'Evaluating sequence:', (' ').join(tokens)
            print 'Log_10 prob:', compute_sentence_prob(arpalm, tokens)