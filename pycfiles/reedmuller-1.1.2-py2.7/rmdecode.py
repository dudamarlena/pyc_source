# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/reedmuller/rmdecode.py
# Compiled at: 2018-05-19 10:59:18
"""rmdecode.py

By Sebastian Raaphorst, 2012.

Simple command-line application for Reed-Muller decoding of one or more 0-1 strings."""
import sys, reedmuller
if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.stderr.write('Usage: %s r m codeword [codeword [...]]\n' % (sys.argv[0],))
        sys.exit(1)
    r, m = map(int, sys.argv[1:3])
    if m <= r:
        sys.stderr.write('We require r < m.\n')
        sys.exit(2)
    rm = reedmuller.ReedMuller(r, m)
    n = rm.block_length()
    for codeword in sys.argv[3:]:
        try:
            listword = list(map(int, codeword))
            if not set(listword).issubset([0, 1]) or len(listword) != n:
                sys.stderr.write('FAIL: word %s is not a 0-1 string of length %d\n' % (codeword, n))
            else:
                decodeword = rm.decode(listword)
                if not decodeword:
                    print 'Could not unambiguously decode word %s' % codeword
                else:
                    print ('').join(map(str, decodeword))
        except:
            print (
             'Unexpected error:', sys.exc_info()[0])