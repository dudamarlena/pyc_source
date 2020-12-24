# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uta/utils/alignment.py
# Compiled at: 2014-08-29 17:40:42
import itertools, Bio.AlignIO, Bio.Emboss.Applications as bea, cStringIO

def align2(seqa, seqb, gapopen=10, gapextend=0.5):
    """Globally align two sequences.
    This function currently uses EMBOSS' needle command, which ideally
    would be replaced by a forkless version in Python.

    >>> seq1 = 'acacagccattaatcttgtagcttcatattaactggtttgctttcatgacgctgctgaggaat'
    >>> seq2 = 'acagacccattaatcttgtagcttcatcaacattaactggtttgctttcatgacaggaat'

    # TODO: Work out conditional test based on whether emboss is available
    # >>> a1,a2 = align2(seq1,seq2)
    # >>> a1
    # 'acacagccattaatcttgtagcttcat----attaactggtttgctttcatgacgctgctgaggaat'
    # >>> a2
    # 'acagacccattaatcttgtagcttcatcaacattaactggtttgctttcatgac-------aggaat'

    """
    if seqa == seqb:
        return (seqa, seqb)
    cline = bea.NeedleCommandline(asequence='asis:' + seqa, bsequence='asis:' + seqb, gapopen=gapopen, gapextend=gapextend, auto=True, filter=True, stdout=True)
    o, e = cline()
    aln = Bio.AlignIO.read(cStringIO.StringIO(o), 'emboss')
    return (aln[0].seq.tostring(), aln[1].seq.tostring())


def alignment_match_string(aseq1, aseq2):
    """for aligned sequences aseq1 and aseq2, both of length n, return an
    exploded CIGAR string of length n with characters denoting M)atch,
    I)nsertion, D)eletion, X)mismatch of aseq2 relative to aseq1.  In our
    case, M always means identity match; in general, M may mean
    match/mismatch under some substitution matrix.  See
    http://goo.gl/fek4t for a short summary.

    >>> aseq1 = 'acacagccattaatcttgtagcttcat----attaactggtttgctttcatgacgctgctgaggaat'
    >>> aseq2 = 'acagacccattaatcttgtagcttcatcaacattaactggtttgctttcatgac-------aggaat'
    >>> alignment_match_string( aseq1,aseq2 )
    'MMMXMXMMMMMMMMMMMMMMMMMMMMMIIIIMMMMMMMMMMMMMMMMMMMMMMMDDDDDDDMMMMMM'

    """
    assert len(aseq1) == len(aseq2)

    def _cigar_char(c1, c2):
        if c1 == c2:
            return 'M'
        if c1 == '-':
            return 'I'
        if c2 == '-':
            return 'D'
        if c1 != c2:
            return 'X'
        raise Exception('In the words of David Byrne, how did I get here?')

    match_string = [ _cigar_char(c1, c2) for c1, c2 in zip(aseq1, aseq2) ]
    return ('').join(match_string)


def alignment_cigar_list(aseq1, aseq2):
    """Return a list of cigar operations for the aligned sequences aseq1
    and aseq2.  Each tuple is (pos, operation, count).
    
    >>> aseq1 = 'acacagccattaatcttgtagcttcat----attaactggtttgctttcatgacgctgctgaggaat'
    >>> aseq2 = 'acagacccattaatcttgtagcttcatcaacattaactggtttgctttcatgac-------aggaat'
    >>> for a in alignment_cigar_list( aseq1,aseq2 ):
    ...   print a
    (0, 'M', 3)
    (3, 'X', 1)
    (4, 'M', 1)
    (5, 'X', 1)
    (6, 'M', 21)
    (27, 'I', 4)
    (31, 'M', 23)
    (54, 'D', 7)
    (61, 'M', 6)

    """
    cv = [ (c, len(list(group))) for c, group in itertools.groupby(alignment_match_string(aseq1, aseq2))
         ]
    pcv = []
    s = 0
    for e in cv:
        pcv += [(s, e[0], e[1])]
        s += e[1]

    return pcv


def alignment_cigar_string(aseq1, aseq2):
    """return a CIGAR string for aligned sequences aseq1 and aseq2,
    which must be of equal length.

    >>> aseq1 = 'acacagccattaatcttgtagcttcat----attaactggtttgctttcatgacgctgctgaggaat'
    >>> aseq2 = 'acagacccattaatcttgtagcttcatcaacattaactggtttgctttcatgac-------aggaat'
    >>> alignment_cigar_string( aseq1,aseq2 )
    '3M1X1M1X21M4I23M7D6M'

    """
    return ('').join([ str(l) + c for _, c, l in alignment_cigar_list(aseq1, aseq2)
                     ])


def explode_cigar(cigar):
    """return a vector of column matches for a given cigar string

    >>> explode_cigar('5M2I4X1D')
    'MMMMMIIXXXXD'

    """
    import re
    u = re.compile('(?P<n>\\d+)(?P<op>[MXID])')
    return ('').join([ md['op'] * int(md['n']) for md in [ m.groupdict() for m in u.finditer(cigar) ] ])


if __name__ == '__main__':
    import doctest
    doctest.testmod()