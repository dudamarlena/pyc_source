# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/repeat_pattern_suffix.py
# Compiled at: 2010-10-16 07:02:00
"""
This module uses suffix array to find exact repeated patterns in a list.
The logic is pretty much identical to the Suffix Tree logic (in repeat_pattern2),
but the implementation is with suffix array.

The Algorithm:
1. Build a suffix array from the input-list - I use a slightly modified "tools"
        module from the pysuffix project.
2. Add to each item in the suffix-list the number of common elements with the
        previous item. The elements are from the input-list suffix.
3. Repeat for each value (i) from minimum-pattern-length to maximum-common-prefix:
3.1. Group the suffix-list by the condition: if common-elements >= i
3.2. Each True group is a possible pattern, the elements of the group are the
        indices of the pattern (add the last index of the last False group).
3.3. from these indices we need to filter overlaps (every index is a two-tuple
        (start, end), overlap is when the start of an index is before the previous
        index end).

This algorithm is faster then the Suffix Tree algorithm, and takes about half
the memory.

Erez Bibi
2010-05-08
"""
from collections import namedtuple
from itertools import izip_longest, izip, groupby
from pysuffix_tools import suffix_array
from repeat_pattern_base import RepeatPatternBase
MIN_LEN_LIMIT = 4
SuffixListItem = namedtuple('SuffixListItem', ['index', 'prefix'])

class RepeatPattern(RepeatPatternBase):
    """
        See module documentation.
        """

    def _print_suffix_array(self, start=0, stop=-1):
        """ Debugging method - Print the suffix list """
        max_len = len(self._suffix_lst)
        if stop == -1:
            stop = max_len
        for i in xrange(start, stop):
            a = self._suffix_lst[i].index
            if i < max_len - 1:
                d = max(self._suffix_lst[i].prefix, self._suffix_lst[(i + 1)].prefix)
            else:
                d = self._suffix_lst[i].prefix
            b = min(a + d + 1, max_len)
            print '> %s (%s):\t\t%s ...' % (
             self._suffix_lst[i].index, self._suffix_lst[i].prefix,
             (' ').join(repr(item) for item in self._input_lst[a:b]))

    def _print_final(self):
        """ Debug function to pass to gather_occurrences """
        if self.debug_level > 0:
            print 'Best %s (Repeats=%s, Factor=%s):' % (
             self.num_patterns, len(self.indices_lst), self.factor)
            print ('\n').join([ '\t' + str(item) for item in self.pattern ])
            if self.debug_level > 1:
                print 'Indices List:', self.indices_lst

    def _find_common_prefix2(self, x, y):
        """ Count how many common items in two sub lists. The sub list
                (suffixes) are starting in indices x and y.
                """
        if x < 0 or y < 0:
            return 0
        (a, b) = sorted((x, y))
        counter = 0
        while b < self.max_index:
            val = cmp(self._input_lst[a], self._input_lst[b])
            if val != 0:
                break
            counter += 1
            a += 1
            b += 1

        return counter

    def _filter_overlaps(self, indices):
        """ Filter overlapping indices from an indices list """
        new_indices = [
         indices[0]]
        for i in range(1, len(indices)):
            if indices[i][0] > new_indices[(-1)][1]:
                new_indices.append(indices[i])

        return new_indices

    def _build_suffix_array(self):
        """
                Build a suffix array from the input-list (class variable). Every item in
                the array (list) is a two-tuple (index, prefix).
                index is the index of this suffix in the input list.
                prefix is the number of common items with the previous suffix in the
                list.
                """
        tmp_lst = suffix_array(self._input_lst)
        self._suffix_lst = [ SuffixListItem(tmp_lst[i], self._find_common_prefix2(tmp_lst[(i - 1)], tmp_lst[i])) for i in xrange(len(tmp_lst))
                           ]
        self._max_prefix = max(self._suffix_lst, key=lambda x: x.prefix).prefix
        return self._suffix_lst

    def _find_repeat_pattern(self):
        """ Find all possible and acceptable repeat patterns """
        global MIN_LEN_LIMIT
        results = []
        if self.max_len:
            self._max_prefix = min(self._max_prefix, self.max_len)
        for pattern_len in range(self.min_len, self._max_prefix + 1):
            for (key, group) in groupby(self._suffix_lst, key=lambda x: x.prefix >= pattern_len):
                if not key:
                    for item in group:
                        last_index = item.index

                if key is True:
                    indices = [ item.index for item in group ]
                    pattern = self._input_lst[indices[0]:indices[0] + pattern_len]
                    if len(set(pattern)) < MIN_LEN_LIMIT:
                        continue
                    indices.append(last_index)
                    indices.sort()
                    indices = [ (index, index + pattern_len - 1) for index in indices ]
                    indices = self._filter_overlaps(indices)
                    factor = self.get_factor(pattern, indices)
                    if self.debug_level > 3:
                        print 'Factor: %s %s' % (factor, pattern)
                    if factor > 0:
                        if self.debug_level > 2:
                            print 'Possible: (%s, %s) %s' % (
                             len(indices), round(factor, 4), pattern)
                        results.append((pattern, indices, factor))

        return results

    def process(self, input_lst):
        """
                Find repeat patterns in an input-list.
                Returns the number of patterns found.
                """
        if MIN_LEN_LIMIT and self.min_len < MIN_LEN_LIMIT:
            self.min_len = MIN_LEN_LIMIT
        self.init(input_lst)
        self.max_index = len(input_lst)
        self._build_suffix_array()
        if self.debug_level > 4:
            self._print_suffix_array()
        results = self._find_repeat_pattern()
        if not results:
            return 0
        results.sort(key=lambda x: x[2], reverse=True)
        return self.gather_occurrences(results, self._print_final)

    @classmethod
    def test(cls, verbose=0):
        """ Tests for this class """
        global MIN_LEN_LIMIT
        rp = cls(debug_level=verbose)
        MIN_LEN_LIMIT = 0
        rp.min_repeat = 2
        list1 = list('XYZXYZABCkABClABCmABCXYZ')
        list2 = list('ABCAYBCAXBC')
        if verbose:
            print list1
        rp.max_patterns = 5
        rp.process(list1)
        assert rp.pattern == ['A', 'B', 'C'], rp.pattern
        assert rp.indices_lst == [(6, 8), (10, 12), (14, 16), (18, 20)], rp.indices_lst
        rp.pattern_num = 1
        assert rp.pattern == ['X', 'Y', 'Z'], rp.pattern
        rp.pattern_num = 0
        rp.sort(rp.INDICES)
        assert rp.pattern == ['X', 'Y', 'Z'], rp.pattern
        if verbose:
            print '----------------------------------------------'
        if verbose:
            print list2
        rp.process(list2)
        assert rp.pattern == ['B', 'C'], rp.pattern
        assert rp.indices_lst == [(1, 2), (5, 6), (9, 10)], rp.indices_lst
        rp.process_by_pattern(list('YBCA'))
        assert rp.repeats == 1, rp.repeats
        if verbose:
            print '----------------------------------------------'


if __name__ == '__main__':
    RepeatPattern.test(verbose=4)
    print 'Test Passed'
    text = 'make an iterator that aggregates elements from each of the\n\titerables if the iterables are of uneven length missing values are\n\tfilled-in with fillvalue iteration continues until the longest iterable is\n\texhausted\n\taaa aaa aaa aaa aaa aaa aaa'