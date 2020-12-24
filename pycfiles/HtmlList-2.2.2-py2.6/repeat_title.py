# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/repeat_title.py
# Compiled at: 2010-10-16 07:02:00
"""
A trivial algorithm to find HTML titles. Some time that is what we need.
I inherit from the module repeat_pattern and not from the base, because there
are common methods here.
"""
from collections import defaultdict
from repeat_pattern import RepeatPattern as RepeatPatternBase
FACTOR_ADJUST = 5
TITLES = set(('h1', 'h2', 'h3', 'h4', 'h5', 'h6'))

class RepeatPattern(RepeatPatternBase):
    """
        See module documentation
        """

    def _find_titles(self):
        """ Here I do most of the work.
                1. Find the titles
                2. Get the indices and factors
                3. Break the indices to groups
                4. Populate with the best X titles type
                - There is no need to use "clean_indices" here
                I have to "cheat" with the indices list and the pattern so the factor
                will not be zero. The factor will be low anyway.
                """
        lst = []
        for (title, indices) in self._items_dict.iteritems():
            (title, index) = title
            if title.tag_name() not in TITLES:
                continue
            try:
                title.level = int(title.tag_name()[1])
            except ValueError:
                title.level = FACTOR_ADJUST

            if self.debug_level > 2:
                print 'Found', title
            indices_lst = zip(indices, indices)
            pattern = [title]
            if self.debug_level > 3:
                print 'Indices', indices_lst
            factor = self.get_factor(pattern, indices_lst)
            if factor > 0:
                lst.append((pattern, indices_lst, factor))

        return lst

    def _debug_print(self):
        if self.debug_level > 0:
            self._print_pattern('Best %s' % self.num_patterns)

    def process(self, input_lst):
        """ Find the titles """
        self.init(input_lst)
        self.LEN_ONE_MAGIC = None
        self.min_len = 1
        self._items_dict = defaultdict(list)
        self._group_items()
        results = self._find_titles()
        if not results:
            return 0
        else:
            if self.debug_level > 1:
                print 'Titles', results
            results.sort(key=lambda x: x[2], reverse=True)
            self.gather_occurrences(results, self._debug_print)
            return self.num_patterns


if __name__ == '__main__':
    pass