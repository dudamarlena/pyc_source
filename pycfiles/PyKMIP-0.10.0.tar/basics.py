# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pykmer/basics.py
# Compiled at: 2017-01-23 23:55:36
__doc__ = '\nBasic functions for *k*-mer manipulations.\n\nThe elementary functions `kmer` converts string representations of DNA\nsequences (using ACG&T) in to a compact 2-bit/base integer representation,\nand `render` converts this representation back to a string.\n\nAn additional encoding for single bases is used by the function `fasta`\nwhere 4 indicator bits are used to represent a nucleotide in the extended\nform where the least significant bit indicates the presence of an A, the\nsecond least significant bit, a C, and so on, so that all 16 combinations\ncan be represented, and the function converts that representation in to\nthe standard FASTA form.\n\nThe functions `kmers` and `kmersWithPos` return the sequence of *k*-mers\nfrom sliding a window over the given sequence, optionally including\nreverse complement *k*-mers as well. The latter function also includes\nposition information. Positions are numbered from 1, not 0, and the\npositions of *k*-mers from the reverse complement strand are given\nnegative positions (from -1).\n\nThe basic manipulation and comparison functions included in this module are:\n\n`rc`\n    for computing the reverse complement of a *k*-mer\n`fnv`\n    for computing the Fowler-Noll-Vo (FNV) hash of a *k*-mer\n`can` \n    for computing the canonical choice between a *k*-mer and its reverse\n    complement.\n`ham`\n    for computing the Hamming distance (number of substitutions) between\n    two *k*-mers\n`lcp`\n    for computing longest common matchinng prefix betwen two *k*-mers\n'
__docformat__ = 'restructuredtext'
from pykmer.bits import ffs, rev, popcnt, m1
_nuc = {'A': 0, 'a': 0, 'C': 1, 'c': 1, 'G': 2, 'g': 2, 'T': 3, 't': 3, 'U': 3, 'u': 3}

def kmer(seq):
    """Turn a string `seq` into an integer k-mer"""
    r = 0
    for c in seq:
        if c not in _nuc:
            return
        r = r << 2 | _nuc[c]

    return r


def render(k, x):
    """Turn an integer k-mer `x` into a string"""
    r = []
    for i in xrange(k):
        r.append('ACGT'[(x & 3)])
        x >>= 2

    return ('').join(r[::-1])


_fas = [
 '*',
 'A',
 'C',
 'M',
 'G',
 'R',
 'S',
 'V',
 'T',
 'W',
 'Y',
 'H',
 'K',
 'D',
 'B',
 'N']

def fasta(x):
    """Convert a 4-bit indicator variable `x` representation
     of a base combination to the 16-letter FASTA alphabet.
     
     The indicator bit representation is the bitwise OR of:

     ====   ==============
     Base   Representation
     ====   ==============
     A      1
     C      2
     G      4
     T/U    8
     """
    return _fas[x]


def rc(k, x):
    """
    Compute the reverse complement of a *k*-mer `x`.

    Values of `k` > 30 are not guaranteed to work.
    """
    return rev(~x) >> 64 - 2 * k


def ham(x, y):
    """
    Compute the Hamming distance between two k-mers `x` and `y`.

    Although *k* is not a parameter, *k*-mers longer than 30bp are not
    guaranteed to produce correct results.
    """
    z = x ^ y
    v = (z | z >> 1) & m1
    return popcnt(v)


def lev(k, x, y):
    """
    Compute the minimal edit distance (Levenshtein distance)
    between the two *k*-mers `x` and `y`.
    """
    t0 = [ 0 ]
    t1 = [ 0 ]
    y0 = y
    for i in xrange(k):
        t1[0] = i + 1
        y = y0
        for j in xrange(k):
            c = 0 if x & 3 == y & 3 else 1
            a1 = t0[j] + c
            a2 = t1[j] + 1
            a3 = t0[(j + 1)] + 1
            t1[j + 1] = min(a1, a2, a3)
            y >>= 2

        x >>= 2
        t2 = t1
        t1 = t0
        t0 = t2

    return t0[k]


def lcp(k, x, y):
    """
    Find the length of the common matching prefix between 2 k-mers `x` and `y`.

    Values of `k` > 30 are not guaranteed to work.
    """
    z = x ^ y
    if z == 0:
        return k
    v = 1 + ffs(z) // 2
    return k - v


def fnv(x, s):
    """
    Compute a Fowler-Noll-Vo (FNV) hash of a *k*-mer `x` with the seed
    `s`, returning least significant 61 bits.

    Although *k* is not a parameter, *k*-mers longer than 30bp are not
    guaranteed to produce correct results.
    """
    h = 14695981039346656037
    for i in xrange(8):
        h ^= s & 255
        h = h * 1099511628211 & 2305843009213693951
        s >>= 8

    for i in xrange(8):
        h ^= x & 255
        h = h * 1099511628211 & 2305843009213693951
        x >>= 8

    return h & 2305843009213693951


def murmer(x, s):
    """
    Compute the Murmer hash of the *k*-mer `x` with the seed `s`,
    returning least significant 61 bits.

    Although *k* is not a parameter, *k*-mers longer than 30bp are
    not guaranteed to produce correct results.
    """

    def _rot64(a, b):
        return a << b | a >> 64 - b

    def _fmix64(k):
        k ^= k >> 33
        k = k * 18397679294719823053 & 18446744073709551615
        k ^= k >> 33
        k = k * 14181476777654086739 & 18446744073709551615
        k ^= k >> 33
        return k

    c1 = 9782798678568883157
    c2 = 5545529020109919103
    h = s
    k = x
    k = k * c1 & 18446744073709551615
    k = (k << 31 | k >> 33) & 18446744073709551615
    k = k * c2 & 18446744073709551615
    h ^= k
    h = (h << 27 | h >> 37) & 18446744073709551615
    h = h * 5 + 1390208809 & 18446744073709551615
    h ^= h >> 33
    h = h * 18397679294719823053 & 18446744073709551615
    h ^= h >> 33
    h = h * 14181476777654086739 & 18446744073709551615
    h ^= h >> 33
    return h


def can(k, x):
    """
    Return a canonical choice between `x` and its reverse complement.

    Some implementations just choose the lexicographically less of
    the two. For reasons of robustness, this method returns the
    *k*-mer with the smaller Murmer (see `murmer`) hash. This results
    in an approximately uniform distribution of canonical *k*-mers,
    rather than the highly skewed distribution that results from a
    lexicographically determined choice.

    Values of `k` > 30 are not guaranteed to work.
    """
    xh = murmer(x, 17)
    xb = rc(k, x)
    xbh = murmer(xb, 17)
    if xh <= xbh:
        return x
    else:
        return xb


def sub(s, p, x):
    """
    Return true iff `x` is in the deterministically defined subspace
    of *k*-mers defined by determining those who's normalized hash
    value (with seed `s`) is less than `p`.
    """
    u = float(murmer(x, s)) / float(2305843009213693951)
    return u < p


def kmers(k, seq, bothStrands=False):
    """
    A generator for extracting *k*-mers from a string nucleotide
    sequence `seq`.  The parameter `bothStrands` determines whether
    the sequence of result *k*-mers should include the reverse
    complement of each *k*-mer extracted from the string.

    The *k*-mers are extracted using a *sliding* window, not a *tiling*
    window.  This means that the results include the *k*-mer starting
    at each position in the string: 0, 1, 2, ...., len(str) - k + 1.

    Any *k*-mers overlaying characters *other* than AaCcGgTtUu are skipped.

    Values of `k` > 30 are not guaranteed to work.
    """
    z = len(seq)
    msk = (1 << 2 * k) - 1
    s = 2 * (k - 1)
    i = 0
    j = 0
    x = 0
    xb = 0
    while i + k <= z:
        while i + j < z and j < k:
            b = _nuc.get(seq[(i + j)], 4)
            if b == 4:
                i += j + 1
                j = 0
                x = 0
                xb = 0
            else:
                x = x << 2 | b
                xb = xb >> 2 | 3 - b << s
                j += 1

        if j == k:
            x &= msk
            yield x
            if bothStrands:
                yield xb
            j -= 1
        i += 1


def kmersList(k, seq, bothStrands=False):
    """
    Extract *k*-mers from a string nucleotide sequence `seq` and
    return them as a list.  The parameter `bothStrands` determines
    whether the sequence of result *k*-mers should include the
    reverse complement of each *k*-mer extracted from the string.

    The *k*-mers are extracted using a *sliding* window, not a
    *tiling* window.  This means that the results include the *k*-mer
    starting at each position in the string:
        0, 1, 2, ...., len(str) - k + 1.

    Any *k*-mers overlaying characters *other* than AaCcGgTtUu are
    skipped.

    Values of `k` > 30 are not guaranteed to work.
    """
    z = len(seq)
    msk = (1 << 2 * k) - 1
    s = 2 * (k - 1)
    i = 0
    j = 0
    x = 0
    xb = 0
    res = []
    while i + k <= z:
        while i + j < z and j < k:
            b = _nuc.get(seq[(i + j)], 4)
            if b == 4:
                i += j + 1
                j = 0
                x = 0
                xb = 0
            else:
                x = x << 2 | b
                xb = xb >> 2 | 3 - b << s
                j += 1

        if j == k:
            x &= msk
            res.append(x)
            if bothStrands:
                res.append(xb)
            j -= 1
        i += 1

    return res


def kmersWithPos(k, seq, bothStrands=False):
    """
    Extract *k*-mers from a string nucleotide sequence `seq`.
    The parameter `bothStrands` determines whether the sequence of
    result *k*-mers should include the reverse complement of each *k*-mer
    extracted from the string.

    The *k*-mers are returned in a tuple with the position in the sequence
    of the left-most base (i.e. most significant bits). Positions on
    the forward strand are numbered from 1. Positions on the reverse
    complement strand are numbered from -1.

    The *k*-mers are extracted using a *sliding* window, not a *tiling*
    window.  This means that the results include the *k*-mer starting
    at each position in the string: 0, 1, 2, ...., len(str) - k + 1.

    Any *k*-mers overlaying characters *other* than AaCcGgTtUu are skipped.

    Values of `k` > 30 are not guaranteed to work.
    """
    z = len(seq)
    msk = (1 << 2 * k) - 1
    i = 0
    j = 0
    x = 0
    while i + k <= z:
        while i + j < z and j < k:
            b = _nuc.get(seq[(i + j)], 4)
            if b == 4:
                i += j + 1
                j = 0
                x = 0
            else:
                x = x << 2 | b
                j += 1

        if j == k:
            x &= msk
            yield (x, i + 1)
            if bothStrands:
                yield (
                 rc(k, x), -(i + 1))
            j -= 1
        i += 1