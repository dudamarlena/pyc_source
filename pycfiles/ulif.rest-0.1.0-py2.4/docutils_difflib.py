# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ulif/rest/tests/docutils_difflib.py
# Compiled at: 2008-02-24 09:47:59
"""
Module difflib -- helpers for computing deltas between objects.

Function get_close_matches(word, possibilities, n=3, cutoff=0.6):
    Use SequenceMatcher to return list of the best "good enough" matches.

Function ndiff(a, b):
    Return a delta: the difference between `a` and `b` (lists of strings).

Function restore(delta, which):
    Return one of the two sequences that generated an ndiff delta.

Class SequenceMatcher:
    A flexible class for comparing pairs of sequences of any type.

Class Differ:
    For producing human-readable deltas from sequences of lines of text.
"""
__all__ = [
 'get_close_matches', 'ndiff', 'restore', 'SequenceMatcher', 'Differ']
TRACE = 0

class SequenceMatcher:
    """
    SequenceMatcher is a flexible class for comparing pairs of sequences of
    any type, so long as the sequence elements are hashable.  The basic
    algorithm predates, and is a little fancier than, an algorithm
    published in the late 1980's by Ratcliff and Obershelp under the
    hyperbolic name "gestalt pattern matching".  The basic idea is to find
    the longest contiguous matching subsequence that contains no "junk"
    elements (R-O doesn't address junk).  The same idea is then applied
    recursively to the pieces of the sequences to the left and to the right
    of the matching subsequence.  This does not yield minimal edit
    sequences, but does tend to yield matches that "look right" to people.

    SequenceMatcher tries to compute a "human-friendly diff" between two
    sequences.  Unlike e.g. UNIX(tm) diff, the fundamental notion is the
    longest *contiguous* & junk-free matching subsequence.  That's what
    catches peoples' eyes.  The Windows(tm) windiff has another interesting
    notion, pairing up elements that appear uniquely in each sequence.
    That, and the method here, appear to yield more intuitive difference
    reports than does diff.  This method appears to be the least vulnerable
    to synching up on blocks of "junk lines", though (like blank lines in
    ordinary text files, or maybe "<P>" lines in HTML files).  That may be
    because this is the only method of the 3 that has a *concept* of
    "junk" <wink>.

    Example, comparing two strings, and considering blanks to be "junk":

    >>> s = SequenceMatcher(lambda x: x == " ",
    ...                     "private Thread currentThread;",
    ...                     "private volatile Thread currentThread;")
    >>>

    .ratio() returns a float in [0, 1], measuring the "similarity" of the
    sequences.  As a rule of thumb, a .ratio() value over 0.6 means the
    sequences are close matches:

    >>> print round(s.ratio(), 3)
    0.866
    >>>

    If you're only interested in where the sequences match,
    .get_matching_blocks() is handy:

    >>> for block in s.get_matching_blocks():
    ...     print "a[%d] and b[%d] match for %d elements" % block
    a[0] and b[0] match for 8 elements
    a[8] and b[17] match for 6 elements
    a[14] and b[23] match for 15 elements
    a[29] and b[38] match for 0 elements

    Note that the last tuple returned by .get_matching_blocks() is always a
    dummy, (len(a), len(b), 0), and this is the only case in which the last
    tuple element (number of elements matched) is 0.

    If you want to know how to change the first sequence into the second,
    use .get_opcodes():

    >>> for opcode in s.get_opcodes():
    ...     print "%6s a[%d:%d] b[%d:%d]" % opcode
     equal a[0:8] b[0:8]
    insert a[8:8] b[8:17]
     equal a[8:14] b[17:23]
     equal a[14:29] b[23:38]

    See the Differ class for a fancy human-friendly file differencer, which
    uses SequenceMatcher both to compare sequences of lines, and to compare
    sequences of characters within similar (near-matching) lines.

    See also function get_close_matches() in this module, which shows how
    simple code building on SequenceMatcher can be used to do useful work.

    Timing:  Basic R-O is cubic time worst case and quadratic time expected
    case.  SequenceMatcher is quadratic time for the worst case and has
    expected-case behavior dependent in a complicated way on how many
    elements the sequences have in common; best case time is linear.

    Methods:

    __init__(isjunk=None, a='', b='')
        Construct a SequenceMatcher.

    set_seqs(a, b)
        Set the two sequences to be compared.

    set_seq1(a)
        Set the first sequence to be compared.

    set_seq2(b)
        Set the second sequence to be compared.

    find_longest_match(alo, ahi, blo, bhi)
        Find longest matching block in a[alo:ahi] and b[blo:bhi].

    get_matching_blocks()
        Return list of triples describing matching subsequences.

    get_opcodes()
        Return list of 5-tuples describing how to turn a into b.

    ratio()
        Return a measure of the sequences' similarity (float in [0,1]).

    quick_ratio()
        Return an upper bound on .ratio() relatively quickly.

    real_quick_ratio()
        Return an upper bound on ratio() very quickly.
    """
    __module__ = __name__

    def __init__(self, isjunk=None, a='', b=''):
        r"""Construct a SequenceMatcher.

        Optional arg isjunk is None (the default), or a one-argument
        function that takes a sequence element and returns true iff the
        element is junk.  None is equivalent to passing "lambda x: 0", i.e.
        no elements are considered to be junk.  For example, pass
            lambda x: x in " \t"
        if you're comparing lines as sequences of characters, and don't
        want to synch up on blanks or hard tabs.

        Optional arg a is the first of two sequences to be compared.  By
        default, an empty string.  The elements of a must be hashable.  See
        also .set_seqs() and .set_seq1().

        Optional arg b is the second of two sequences to be compared.  By
        default, an empty string.  The elements of b must be hashable. See
        also .set_seqs() and .set_seq2().
        """
        self.isjunk = isjunk
        self.a = self.b = None
        self.set_seqs(a, b)
        return

    def set_seqs(self, a, b):
        """Set the two sequences to be compared.

        >>> s = SequenceMatcher()
        >>> s.set_seqs("abcd", "bcde")
        >>> s.ratio()
        0.75
        """
        self.set_seq1(a)
        self.set_seq2(b)

    def set_seq1(self, a):
        """Set the first sequence to be compared.

        The second sequence to be compared is not changed.

        >>> s = SequenceMatcher(None, "abcd", "bcde")
        >>> s.ratio()
        0.75
        >>> s.set_seq1("bcde")
        >>> s.ratio()
        1.0
        >>>

        SequenceMatcher computes and caches detailed information about the
        second sequence, so if you want to compare one sequence S against
        many sequences, use .set_seq2(S) once and call .set_seq1(x)
        repeatedly for each of the other sequences.

        See also set_seqs() and set_seq2().
        """
        if a is self.a:
            return
        self.a = a
        self.matching_blocks = self.opcodes = None
        return

    def set_seq2(self, b):
        """Set the second sequence to be compared.

        The first sequence to be compared is not changed.

        >>> s = SequenceMatcher(None, "abcd", "bcde")
        >>> s.ratio()
        0.75
        >>> s.set_seq2("abcd")
        >>> s.ratio()
        1.0
        >>>

        SequenceMatcher computes and caches detailed information about the
        second sequence, so if you want to compare one sequence S against
        many sequences, use .set_seq2(S) once and call .set_seq1(x)
        repeatedly for each of the other sequences.

        See also set_seqs() and set_seq1().
        """
        if b is self.b:
            return
        self.b = b
        self.matching_blocks = self.opcodes = None
        self.fullbcount = None
        self.__chain_b()
        return

    def __chain_b(self):
        b = self.b
        self.b2j = b2j = {}
        self.b2jhas = b2jhas = b2j.has_key
        for i in xrange(len(b)):
            elt = b[i]
            if b2jhas(elt):
                b2j[elt].append(i)
            else:
                b2j[elt] = [
                 i]

        isjunk, junkdict = self.isjunk, {}
        if isjunk:
            for elt in b2j.keys():
                if isjunk(elt):
                    junkdict[elt] = 1
                    del b2j[elt]

        self.isbjunk = junkdict.has_key

    def find_longest_match(self, alo, ahi, blo, bhi):
        """Find longest matching block in a[alo:ahi] and b[blo:bhi].

        If isjunk is not defined:

        Return (i,j,k) such that a[i:i+k] is equal to b[j:j+k], where
            alo <= i <= i+k <= ahi
            blo <= j <= j+k <= bhi
        and for all (i',j',k') meeting those conditions,
            k >= k'
            i <= i'
            and if i == i', j <= j'

        In other words, of all maximal matching blocks, return one that
        starts earliest in a, and of all those maximal matching blocks that
        start earliest in a, return the one that starts earliest in b.

        >>> s = SequenceMatcher(None, " abcd", "abcd abcd")
        >>> s.find_longest_match(0, 5, 0, 9)
        (0, 4, 5)

        If isjunk is defined, first the longest matching block is
        determined as above, but with the additional restriction that no
        junk element appears in the block.  Then that block is extended as
        far as possible by matching (only) junk elements on both sides.  So
        the resulting block never matches on junk except as identical junk
        happens to be adjacent to an "interesting" match.

        Here's the same example as before, but considering blanks to be
        junk.  That prevents " abcd" from matching the " abcd" at the tail
        end of the second sequence directly.  Instead only the "abcd" can
        match, and matches the leftmost "abcd" in the second sequence:

        >>> s = SequenceMatcher(lambda x: x==" ", " abcd", "abcd abcd")
        >>> s.find_longest_match(0, 5, 0, 9)
        (1, 0, 4)

        If no blocks match, return (alo, blo, 0).

        >>> s = SequenceMatcher(None, "ab", "c")
        >>> s.find_longest_match(0, 2, 0, 1)
        (0, 0, 0)
        """
        (a, b, b2j, isbjunk) = (
         self.a, self.b, self.b2j, self.isbjunk)
        besti, bestj, bestsize = alo, blo, 0
        j2len = {}
        nothing = []
        for i in xrange(alo, ahi):
            j2lenget = j2len.get
            newj2len = {}
            for j in b2j.get(a[i], nothing):
                if j < blo:
                    continue
                if j >= bhi:
                    break
                k = newj2len[j] = j2lenget(j - 1, 0) + 1
                if k > bestsize:
                    besti, bestj, bestsize = i - k + 1, j - k + 1, k

            j2len = newj2len

        while besti > alo and bestj > blo and isbjunk(b[(bestj - 1)]) and a[(besti - 1)] == b[(bestj - 1)]:
            besti, bestj, bestsize = besti - 1, bestj - 1, bestsize + 1

        while besti + bestsize < ahi and bestj + bestsize < bhi and isbjunk(b[(bestj + bestsize)]) and a[(besti + bestsize)] == b[(bestj + bestsize)]:
            bestsize = bestsize + 1

        if TRACE:
            print 'get_matching_blocks', alo, ahi, blo, bhi
            print '    returns', besti, bestj, bestsize
        return (
         besti, bestj, bestsize)

    def get_matching_blocks(self):
        """Return list of triples describing matching subsequences.

        Each triple is of the form (i, j, n), and means that
        a[i:i+n] == b[j:j+n].  The triples are monotonically increasing in
        i and in j.

        The last triple is a dummy, (len(a), len(b), 0), and is the only
        triple with n==0.

        >>> s = SequenceMatcher(None, "abxcd", "abcd")
        >>> s.get_matching_blocks()
        [(0, 0, 2), (3, 2, 2), (5, 4, 0)]
        """
        if self.matching_blocks is not None:
            return self.matching_blocks
        self.matching_blocks = []
        la, lb = len(self.a), len(self.b)
        self.__helper(0, la, 0, lb, self.matching_blocks)
        self.matching_blocks.append((la, lb, 0))
        if TRACE:
            print '*** matching blocks', self.matching_blocks
        return self.matching_blocks

    def __helper(self, alo, ahi, blo, bhi, answer):
        (i, j, k) = x = self.find_longest_match(alo, ahi, blo, bhi)
        if k:
            if alo < i and blo < j:
                self.__helper(alo, i, blo, j, answer)
            answer.append(x)
            if i + k < ahi and j + k < bhi:
                self.__helper(i + k, ahi, j + k, bhi, answer)

    def get_opcodes(self):
        """Return list of 5-tuples describing how to turn a into b.

        Each tuple is of the form (tag, i1, i2, j1, j2).  The first tuple
        has i1 == j1 == 0, and remaining tuples have i1 == the i2 from the
        tuple preceding it, and likewise for j1 == the previous j2.

        The tags are strings, with these meanings:

        'replace':  a[i1:i2] should be replaced by b[j1:j2]
        'delete':   a[i1:i2] should be deleted.
                    Note that j1==j2 in this case.
        'insert':   b[j1:j2] should be inserted at a[i1:i1].
                    Note that i1==i2 in this case.
        'equal':    a[i1:i2] == b[j1:j2]

        >>> a = "qabxcd"
        >>> b = "abycdf"
        >>> s = SequenceMatcher(None, a, b)
        >>> for tag, i1, i2, j1, j2 in s.get_opcodes():
        ...    print ("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %
        ...           (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2]))
         delete a[0:1] (q) b[0:0] ()
          equal a[1:3] (ab) b[0:2] (ab)
        replace a[3:4] (x) b[2:3] (y)
          equal a[4:6] (cd) b[3:5] (cd)
         insert a[6:6] () b[5:6] (f)
        """
        if self.opcodes is not None:
            return self.opcodes
        i = j = 0
        self.opcodes = answer = []
        for (ai, bj, size) in self.get_matching_blocks():
            tag = ''
            if i < ai and j < bj:
                tag = 'replace'
            elif i < ai:
                tag = 'delete'
            elif j < bj:
                tag = 'insert'
            if tag:
                answer.append((tag, i, ai, j, bj))
            i, j = ai + size, bj + size
            if size:
                answer.append(('equal', ai, i, bj, j))

        return answer

    def ratio(self):
        """Return a measure of the sequences' similarity (float in [0,1]).

        Where T is the total number of elements in both sequences, and
        M is the number of matches, this is 2,0*M / T.
        Note that this is 1 if the sequences are identical, and 0 if
        they have nothing in common.

        .ratio() is expensive to compute if you haven't already computed
        .get_matching_blocks() or .get_opcodes(), in which case you may
        want to try .quick_ratio() or .real_quick_ratio() first to get an
        upper bound.

        >>> s = SequenceMatcher(None, "abcd", "bcde")
        >>> s.ratio()
        0.75
        >>> s.quick_ratio()
        0.75
        >>> s.real_quick_ratio()
        1.0
        """
        matches = reduce(lambda sum, triple: sum + triple[(-1)], self.get_matching_blocks(), 0)
        return 2.0 * matches / (len(self.a) + len(self.b))

    def quick_ratio(self):
        """Return an upper bound on ratio() relatively quickly.

        This isn't defined beyond that it is an upper bound on .ratio(), and
        is faster to compute.
        """
        if self.fullbcount is None:
            self.fullbcount = fullbcount = {}
            for elt in self.b:
                fullbcount[elt] = fullbcount.get(elt, 0) + 1

        fullbcount = self.fullbcount
        avail = {}
        availhas, matches = avail.has_key, 0
        for elt in self.a:
            if availhas(elt):
                numb = avail[elt]
            else:
                numb = fullbcount.get(elt, 0)
            avail[elt] = numb - 1
            if numb > 0:
                matches = matches + 1

        return 2.0 * matches / (len(self.a) + len(self.b))

    def real_quick_ratio(self):
        """Return an upper bound on ratio() very quickly.

        This isn't defined beyond that it is an upper bound on .ratio(), and
        is faster to compute than either .ratio() or .quick_ratio().
        """
        la, lb = len(self.a), len(self.b)
        return 2.0 * min(la, lb) / (la + lb)


def get_close_matches(word, possibilities, n=3, cutoff=0.6):
    """Use SequenceMatcher to return list of the best "good enough" matches.

    word is a sequence for which close matches are desired (typically a
    string).

    possibilities is a list of sequences against which to match word
    (typically a list of strings).

    Optional arg n (default 3) is the maximum number of close matches to
    return.  n must be > 0.

    Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
    that don't score at least that similar to word are ignored.

    The best (no more than n) matches among the possibilities are returned
    in a list, sorted by similarity score, most similar first.

    >>> get_close_matches("appel", ["ape", "apple", "peach", "puppy"])
    ['apple', 'ape']
    >>> import keyword as _keyword
    >>> get_close_matches("wheel", _keyword.kwlist)
    ['while']
    >>> get_close_matches("apple", _keyword.kwlist)
    []
    >>> get_close_matches("accept", _keyword.kwlist)
    ['except']
    """
    if not n > 0:
        raise ValueError('n must be > 0: ' + `n`)
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError('cutoff must be in [0.0, 1.0]: ' + `cutoff`)
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for x in possibilities:
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and s.quick_ratio() >= cutoff and s.ratio() >= cutoff:
            result.append((s.ratio(), x))

    result.sort()
    result = result[-n:]
    result.reverse()
    return [ x for (score, x) in result ]


def _count_leading(line, ch):
    """
    Return number of `ch` characters at the start of `line`.

    Example:

    >>> _count_leading('   abc', ' ')
    3
    """
    i, n = 0, len(line)
    while i < n and line[i] == ch:
        i += 1

    return i


class Differ:
    r"""
    Differ is a class for comparing sequences of lines of text, and
    producing human-readable differences or deltas.  Differ uses
    SequenceMatcher both to compare sequences of lines, and to compare
    sequences of characters within similar (near-matching) lines.

    Each line of a Differ delta begins with a two-letter code:

        '- '    line unique to sequence 1
        '+ '    line unique to sequence 2
        '  '    line common to both sequences
        '? '    line not present in either input sequence

    Lines beginning with '? ' attempt to guide the eye to intraline
    differences, and were not present in either input sequence.  These lines
    can be confusing if the sequences contain tab characters.

    Note that Differ makes no claim to produce a *minimal* diff.  To the
    contrary, minimal diffs are often counter-intuitive, because they synch
    up anywhere possible, sometimes accidental matches 100 pages apart.
    Restricting synch points to contiguous matches preserves some notion of
    locality, at the occasional cost of producing a longer diff.

    Example: Comparing two texts.

    First we set up the texts, sequences of individual single-line strings
    ending with newlines (such sequences can also be obtained from the
    `readlines()` method of file-like objects):

    >>> text1 = '''  1. Beautiful is better than ugly.
    ...   2. Explicit is better than implicit.
    ...   3. Simple is better than complex.
    ...   4. Complex is better than complicated.
    ... '''.splitlines(1)
    >>> len(text1)
    4
    >>> text1[0][-1]
    '\n'
    >>> text2 = '''  1. Beautiful is better than ugly.
    ...   3.   Simple is better than complex.
    ...   4. Complicated is better than complex.
    ...   5. Flat is better than nested.
    ... '''.splitlines(1)

    Next we instantiate a Differ object:

    >>> d = Differ()

    Note that when instantiating a Differ object we may pass functions to
    filter out line and character 'junk'.  See Differ.__init__ for details.

    Finally, we compare the two:

    >>> result = d.compare(text1, text2)

    'result' is a list of strings, so let's pretty-print it:

    >>> from pprint import pprint as _pprint
    >>> _pprint(result)
    ['    1. Beautiful is better than ugly.\n',
     '-   2. Explicit is better than implicit.\n',
     '-   3. Simple is better than complex.\n',
     '+   3.   Simple is better than complex.\n',
     '?     ++\n',
     '-   4. Complex is better than complicated.\n',
     '?            ^                     ---- ^\n',
     '+   4. Complicated is better than complex.\n',
     '?           ++++ ^                      ^\n',
     '+   5. Flat is better than nested.\n']

    As a single multi-line string it looks like this:

    >>> print ''.join(result),
        1. Beautiful is better than ugly.
    -   2. Explicit is better than implicit.
    -   3. Simple is better than complex.
    +   3.   Simple is better than complex.
    ?     ++
    -   4. Complex is better than complicated.
    ?            ^                     ---- ^
    +   4. Complicated is better than complex.
    ?           ++++ ^                      ^
    +   5. Flat is better than nested.

    Methods:

    __init__(linejunk=None, charjunk=None)
        Construct a text differencer, with optional filters.

    compare(a, b)
        Compare two sequences of lines; return the resulting delta (list).
    """
    __module__ = __name__

    def __init__(self, linejunk=None, charjunk=None):
        """
        Construct a text differencer, with optional filters.

        The two optional keyword parameters are for filter functions:

        - `linejunk`: A function that should accept a single string argument,
          and return true iff the string is junk. The module-level function
          `IS_LINE_JUNK` may be used to filter out lines without visible
          characters, except for at most one splat ('#').

        - `charjunk`: A function that should accept a string of length 1. The
          module-level function `IS_CHARACTER_JUNK` may be used to filter out
          whitespace characters (a blank or tab; **note**: bad idea to include
          newline in this!).
        """
        self.linejunk = linejunk
        self.charjunk = charjunk
        self.results = []

    def compare(self, a, b):
        r"""
        Compare two sequences of lines; return the resulting delta (list).

        Each sequence must contain individual single-line strings ending with
        newlines. Such sequences can be obtained from the `readlines()` method
        of file-like objects. The list returned is also made up of
        newline-terminated strings, ready to be used with the `writelines()`
        method of a file-like object.

        Example:

        >>> print ''.join(Differ().compare('one\ntwo\nthree\n'.splitlines(1),
        ...                                'ore\ntree\nemu\n'.splitlines(1))),
        - one
        ?  ^
        + ore
        ?  ^
        - two
        - three
        ?  -
        + tree
        + emu
        """
        cruncher = SequenceMatcher(self.linejunk, a, b)
        for (tag, alo, ahi, blo, bhi) in cruncher.get_opcodes():
            if tag == 'replace':
                self._fancy_replace(a, alo, ahi, b, blo, bhi)
            elif tag == 'delete':
                self._dump('-', a, alo, ahi)
            elif tag == 'insert':
                self._dump('+', b, blo, bhi)
            elif tag == 'equal':
                self._dump(' ', a, alo, ahi)
            else:
                raise ValueError, 'unknown tag ' + `tag`

        results = self.results
        self.results = []
        return results

    def _dump(self, tag, x, lo, hi):
        """Store comparison results for a same-tagged range."""
        for i in xrange(lo, hi):
            self.results.append('%s %s' % (tag, x[i]))

    def _plain_replace(self, a, alo, ahi, b, blo, bhi):
        assert alo < ahi and blo < bhi
        if bhi - blo < ahi - alo:
            self._dump('+', b, blo, bhi)
            self._dump('-', a, alo, ahi)
        else:
            self._dump('-', a, alo, ahi)
            self._dump('+', b, blo, bhi)

    def _fancy_replace(self, a, alo, ahi, b, blo, bhi):
        r"""
        When replacing one block of lines with another, search the blocks
        for *similar* lines; the best-matching pair (if any) is used as a
        synch point, and intraline difference marking is done on the
        similar pair. Lots of work, but often worth it.

        Example:

        >>> d = Differ()
        >>> d._fancy_replace(['abcDefghiJkl\n'], 0, 1, ['abcdefGhijkl\n'], 0, 1)
        >>> print ''.join(d.results),
        - abcDefghiJkl
        ?    ^  ^  ^
        + abcdefGhijkl
        ?    ^  ^  ^
        """
        if TRACE:
            self.results.append('*** _fancy_replace %s %s %s %s\n' % (alo, ahi, blo, bhi))
            self._dump('>', a, alo, ahi)
            self._dump('<', b, blo, bhi)
        (best_ratio, cutoff) = (0.74, 0.75)
        cruncher = SequenceMatcher(self.charjunk)
        (eqi, eqj) = (None, None)
        for j in xrange(blo, bhi):
            bj = b[j]
            cruncher.set_seq2(bj)
            for i in xrange(alo, ahi):
                ai = a[i]
                if ai == bj:
                    if eqi is None:
                        eqi, eqj = i, j
                    continue
                cruncher.set_seq1(ai)
                if cruncher.real_quick_ratio() > best_ratio and cruncher.quick_ratio() > best_ratio and cruncher.ratio() > best_ratio:
                    best_ratio, best_i, best_j = cruncher.ratio(), i, j

        if best_ratio < cutoff:
            if eqi is None:
                self._plain_replace(a, alo, ahi, b, blo, bhi)
                return
            best_i, best_j, best_ratio = eqi, eqj, 1.0
        else:
            eqi = None
        if TRACE:
            self.results.append('*** best_ratio %s %s %s %s\n' % (best_ratio, best_i, best_j))
            self._dump('>', a, best_i, best_i + 1)
            self._dump('<', b, best_j, best_j + 1)
        self._fancy_helper(a, alo, best_i, b, blo, best_j)
        aelt, belt = a[best_i], b[best_j]
        if eqi is None:
            atags = btags = ''
            cruncher.set_seqs(aelt, belt)
            for (tag, ai1, ai2, bj1, bj2) in cruncher.get_opcodes():
                la, lb = ai2 - ai1, bj2 - bj1
                if tag == 'replace':
                    atags += '^' * la
                    btags += '^' * lb
                elif tag == 'delete':
                    atags += '-' * la
                elif tag == 'insert':
                    btags += '+' * lb
                elif tag == 'equal':
                    atags += ' ' * la
                    btags += ' ' * lb
                else:
                    raise ValueError, 'unknown tag ' + `tag`

            self._qformat(aelt, belt, atags, btags)
        else:
            self.results.append('  ' + aelt)
        self._fancy_helper(a, best_i + 1, ahi, b, best_j + 1, bhi)
        return

    def _fancy_helper(self, a, alo, ahi, b, blo, bhi):
        if alo < ahi:
            if blo < bhi:
                self._fancy_replace(a, alo, ahi, b, blo, bhi)
            else:
                self._dump('-', a, alo, ahi)
        elif blo < bhi:
            self._dump('+', b, blo, bhi)

    def _qformat(self, aline, bline, atags, btags):
        r"""
        Format "?" output and deal with leading tabs.

        Example:

        >>> d = Differ()
        >>> d._qformat('\tabcDefghiJkl\n', '\t\tabcdefGhijkl\n',
        ...            '  ^ ^  ^      ', '+  ^ ^  ^      ')
        >>> for line in d.results: print repr(line)
        ...
        '- \tabcDefghiJkl\n'
        '? \t ^ ^  ^\n'
        '+ \t\tabcdefGhijkl\n'
        '? \t  ^ ^  ^\n'
        """
        common = min(_count_leading(aline, '\t'), _count_leading(bline, '\t'))
        common = min(common, _count_leading(atags[:common], ' '))
        atags = atags[common:].rstrip()
        btags = btags[common:].rstrip()
        self.results.append('- ' + aline)
        if atags:
            self.results.append('? %s%s\n' % ('\t' * common, atags))
        self.results.append('+ ' + bline)
        if btags:
            self.results.append('? %s%s\n' % ('\t' * common, btags))


import re

def IS_LINE_JUNK(line, pat=re.compile('\\s*#?\\s*$').match):
    r"""
    Return 1 for ignorable line: iff `line` is blank or contains a single '#'.

    Examples:

    >>> IS_LINE_JUNK('\n')
    1
    >>> IS_LINE_JUNK('  #   \n')
    1
    >>> IS_LINE_JUNK('hello\n')
    0
    """
    return pat(line) is not None


def IS_CHARACTER_JUNK(ch, ws=' \t'):
    r"""
    Return 1 for ignorable character: iff `ch` is a space or tab.

    Examples:

    >>> IS_CHARACTER_JUNK(' ')
    1
    >>> IS_CHARACTER_JUNK('\t')
    1
    >>> IS_CHARACTER_JUNK('\n')
    0
    >>> IS_CHARACTER_JUNK('x')
    0
    """
    return ch in ws


del re

def ndiff(a, b, linejunk=IS_LINE_JUNK, charjunk=IS_CHARACTER_JUNK):
    r"""
    Compare `a` and `b` (lists of strings); return a `Differ`-style delta.

    Optional keyword parameters `linejunk` and `charjunk` are for filter
    functions (or None):

    - linejunk: A function that should accept a single string argument, and
      return true iff the string is junk. The default is module-level function
      IS_LINE_JUNK, which filters out lines without visible characters, except
      for at most one splat ('#').

    - charjunk: A function that should accept a string of length 1. The
      default is module-level function IS_CHARACTER_JUNK, which filters out
      whitespace characters (a blank or tab; note: bad idea to include newline
      in this!).

    Tools/scripts/ndiff.py is a command-line front-end to this function.

    Example:

    >>> diff = ndiff('one\ntwo\nthree\n'.splitlines(1),
    ...              'ore\ntree\nemu\n'.splitlines(1))
    >>> print ''.join(diff),
    - one
    ?  ^
    + ore
    ?  ^
    - two
    - three
    ?  -
    + tree
    + emu
    """
    return Differ(linejunk, charjunk).compare(a, b)


def restore(delta, which):
    r"""
    Return one of the two sequences that generated a delta.

    Given a `delta` produced by `Differ.compare()` or `ndiff()`, extract
    lines originating from file 1 or 2 (parameter `which`), stripping off line
    prefixes.

    Examples:

    >>> diff = ndiff('one\ntwo\nthree\n'.splitlines(1),
    ...              'ore\ntree\nemu\n'.splitlines(1))
    >>> print ''.join(restore(diff, 1)),
    one
    two
    three
    >>> print ''.join(restore(diff, 2)),
    ore
    tree
    emu
    """
    try:
        tag = {1: '- ', 2: '+ '}[int(which)]
    except KeyError:
        raise ValueError, 'unknown delta choice (must be 1 or 2): %r' % which

    prefixes = ('  ', tag)
    results = []
    for line in delta:
        if line[:2] in prefixes:
            results.append(line[2:])

    return results


def _test():
    import doctest, difflib
    return doctest.testmod(difflib)


if __name__ == '__main__':
    _test()