# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Topics/visualization/printtopics.py
# Compiled at: 2013-03-04 12:43:10
import sys, numpy

def list_topics(vocab, testlambda):
    """

    :param vocab:
    :param testlambda:
    """
    for k in range(0, len(testlambda)):
        lambdak = list(testlambda[k, :])
        lambdak /= sum(lambdak)
        temp = zip(lambdak, range(0, len(lambdak)))
        temp = sorted(temp, key=lambda x: x[0], reverse=True)
        print ('topic {0:d}:').format(k)
        for i in xrange(0, 53):
            print ('{0:>20s}  \t---\t  {1:.4f}').format(vocab[temp[i][1]], temp[i][0])

        print


def main():
    """
    Displays topics fit by onlineldavb.py. The first column gives the
    (expected) most prominent words in the topics, the second column
    gives their (expected) relative prominence.
    """
    vocab = str.split(file(sys.argv[1]).read())
    testlambda = numpy.loadtxt(sys.argv[2])
    list_topics(vocab, testlambda)


if __name__ == '__main__':
    main()