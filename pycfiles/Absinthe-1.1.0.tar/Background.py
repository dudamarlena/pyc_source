# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/seq/seq/Background.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = '\nThis program loads a Fasta file and generates a frequency file that\nlooks just like those that are used by MEME and the MarkovBackground\nclass in EM.py\n\nCopyright (2005) Whitehead Institute for Biomedical Research (except as noted below)\nAll Rights Reserved\n\nAuthor: David Benjamin Gordon\n'
import sys, re, os, math
from TAMO import MotifTools
from TAMO.seq import Fasta

def main():
    seqsD = Fasta.load(sys.argv[1])
    seqs = seqsD.values()
    for w in range(1, 7):
        allnmers = permute(w)
        nmersT = MotifTools.top_nmers(w, seqs, 'with counts', 'purge Ns')
        nmersD = {}
        total = 0
        for nmer in allnmers:
            nmersD[nmer] = 1
            total = total + 1

        for nmer, count in nmersT[:]:
            try:
                rc = MotifTools.revcomplement(nmer)
                nmersD[nmer] = nmersD[nmer] + count
                nmersD[rc] = nmersD[rc] + count
                total = total + 2 * count
            except KeyError:
                pass

        _t = nmersD.keys()
        _t.sort()
        print '# freq in %s (total %d with pseudocounts)' % (sys.argv[1], total)
        for nmer in _t:
            print '%-7s %20.17f' % (nmer, float(nmersD[nmer]) / total)

        sys.stdout.flush()


def permute(depth, letters=['A', 'C', 'G', 'T'], seqs=[''], curdepth=0):
    newseqs = []
    for seq in seqs:
        for letter in letters:
            newseqs.append(seq + letter)

    if depth > curdepth:
        return permute(depth, letters, newseqs, curdepth + 1)
    else:
        return seqs


if __name__ == '__main__':
    main()