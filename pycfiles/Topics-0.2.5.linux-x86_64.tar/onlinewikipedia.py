# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Topics/onlineldavb/onlinewikipedia.py
# Compiled at: 2013-03-01 12:59:45
from sys import argv
import numpy
from Topics.onlineldavb import wikirandom
import onlineldavb

def main():
    """
    Downloads and analyzes a bunch of random Wikipedia articles using
    online VB for LDA.
    """
    batchsize = 64
    D = 3300000.0
    K = 100
    if len(argv) < 2:
        documentstoanalyze = int(D / batchsize)
    else:
        documentstoanalyze = int(argv[1])
    vocab = file('./dictnostops.txt').readlines()
    W = len(vocab)
    olda = onlineldavb.OnlineLDA(vocab, K, D, 1.0 / K, 1.0 / K, 1024.0, 0.7)
    for iteration in range(0, documentstoanalyze):
        docset, articlenames = wikirandom.get_random_wikipedia_articles(batchsize)
        gamma, bound = olda.update_lambda(docset)
        wordids, wordcts = onlineldavb.parse_doc_list(docset, olda._vocab)
        perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
        print '%d:  rho_t = %f,  held-out perplexity estimate = %f' % (
         iteration, olda._rhot, numpy.exp(-perwordbound))
        if iteration % 10 == 0:
            print 'Iteration: ', iteration
            numpy.savetxt('lambda.dat', olda._lambda)
            numpy.savetxt('gamma.dat', gamma)


if __name__ == '__main__':
    main()