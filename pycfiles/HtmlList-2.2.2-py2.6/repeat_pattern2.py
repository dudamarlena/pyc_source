# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/repeat_pattern2.py
# Compiled at: 2010-10-16 07:02:00
"""
* This is the "old" repeat-pattern algorithm.

This module defines a class to find a repetitive patterns in a list. It uses
a suffix tree as the base of it's algorithm. In every node of the tree I keep an
indices list of the occurrence of the sequence on the input list. This allows me
to check for overlapping, and find all the occurrences of the chosen pattern
efficiently.

Erez Bibi
"""
from collections import namedtuple
from repeat_pattern_base import RepeatPatternBase
MIN_LEN_LIMIT = 4
TreeItem = namedtuple('TreeItem', ['tags', 'childes', 'indices'])

class RepeatPattern(RepeatPatternBase):
    """ (See module documentation) """

    def _build_tree(self, lst, tree, lst_index):
        """ This is the inner recursive method to build suffix tree from a list.
                Each node in the tree is a named-tuple TreeItem (tags, childes, indices).
                        tags - A list of items from the input list.
                        childes - A list of sub trees under this node.
                        indices - A list of the indices (from the original input list) of
                        the items that are represented by this node.
                """
        if not lst:
            return tree
        for j in range(len(tree.childes)):
            (sub_lst, childs, indices) = tree.childes[j]
            if sub_lst[0] != lst[0]:
                continue
            else:
                index = 1
                while index < min(len(sub_lst), len(lst)):
                    if sub_lst[index] != lst[index]:
                        break
                    index += 1

                if index < len(sub_lst):
                    sub2 = TreeItem(sub_lst[index:], childs, map(lambda x: x + index, indices))
                    indices.append(lst_index)
                    tree.childes[j] = TreeItem(sub_lst[:index], [sub2], indices)
                else:
                    indices.append(lst_index)
                tree.childes[j] = self._build_tree(lst[index:], tree.childes[j], lst_index + index)
                return tree

        tree.childes.append(TreeItem(lst, [], [lst_index]))
        return tree

    def _build_tree_main(self):
        """ This method builds the suffix tree, you must call it before calling
                find_repeat_pattern. it creates the top most (empty) tree, and inserts
                all the lists suffixes.
                """
        self._tree = TreeItem([], [], [])
        for i in xrange(len(self._input_lst)):
            self._tree = self._build_tree(self._input_lst[i:], self._tree, i)

        if self.debug_level > 4:
            self.traverse_tree()

    def _find_repeat_pattern(self, tree=None, cur_lst=None, results=None):
        """ This method finds the "best" repetitive patterns in the tree.
                In other words it finds a sequence of items, that it's length multiply
                by the number of repeats and by some factor of STDV, is the biggest.
                In addition, it will not return a pattens that are overlapping.

                This is also a recursive function. It return the best matched sequence.
                """
        global MIN_LEN_LIMIT
        if not self._tree:
            return
        else:
            if tree is None:
                tree = self._tree
            if cur_lst is None:
                cur_lst = []
            if results is None:
                results = []
            (lst, childs, indices) = tree
            cur_lst = cur_lst + list(lst)
            if len(set(cur_lst)) >= MIN_LEN_LIMIT:
                up = len(lst)
                down = len(cur_lst) - up
                indices_lst = [ (i - down, i + up - 1) for i in indices ]
                factor = self.get_factor(cur_lst, indices_lst)
                if factor > 0:
                    if self.debug_level > 3:
                        print 'First criteria: Occurrences', len(indices), cur_lst
                    if min(self._derivative(indices)) >= len(cur_lst):
                        if self.debug_level > 2:
                            print 'Second Criteria: Factor', factor
                        results.append((cur_lst, indices_lst, factor))
            for sub_tree in childs:
                self._find_repeat_pattern(sub_tree, cur_lst, results)

            return results

    @property
    def relevant_items(self):
        """ For compatibility with other algorithms. """
        return

    def traverse_tree(self, tree=None, level=0, index_filter=None):
        """ This is only for debugging - Prints the tree.
                """
        if not self._tree:
            return
        else:
            if tree is None:
                tree = self._tree
            (lst, childs, indices) = tree
            if not index_filter or indices and indices[0] in index_filter:
                print '>', '  ' * level, lst, '-', indices
            for sub_tree in childs:
                self.traverse_tree(sub_tree, level + 1, index_filter)

            return

    def process(self, input_lst):
        """ Find the best pattern in a list of items (see module documentation
                for more details).
                Returns a list of tow-tuple indices (start, end) of the indices of the
                best pattern, or None if there is no "best" pattern.
                """
        if self.min_len < MIN_LEN_LIMIT:
            self.min_len = MIN_LEN_LIMIT
        self.init(input_lst)
        self._build_tree_main()
        results = self._find_repeat_pattern()
        if not results:
            return 0
        results.sort(key=lambda x: x[2], reverse=True)
        self.num_patterns = 0
        index = 0
        while self.num_patterns < self.max_patterns and index < len(results):
            (pattern, indices, factor) = results[index]
            old_len = len(indices)
            new_len = self.clean_indices(indices)
            if new_len >= self.min_repeat:
                if new_len < old_len:
                    factor = self.get_factor(pattern, indices)
                if factor > 0:
                    self.num_patterns += 1
                    self.pattern = pattern
                    self.indices_lst = indices
                    self.factor = factor
                    if self.debug_level > 0:
                        print 'Best %s (Repeats=%s, Factor=%s):' % (
                         self.num_patterns, len(self.indices_lst), self.factor)
                        print ('\n').join([ '\t' + str(item) for item in self.pattern ])
                        if self.debug_level > 1:
                            print 'Indices List:', self.indices_lst
            index += 1

        self.sort()
        self.pattern_num = 0
        return self.num_patterns

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