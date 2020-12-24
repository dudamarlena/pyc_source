# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/repeat_pattern3.py
# Compiled at: 2010-10-16 07:02:00
"""
This simple RepeatPattern class is similar to the one in the repeat_title module.
It inherit from RepeatPattern from the repeat_pattern module (Count Tags algo).
The class looks at some container (grouping) tags from the list, and expands them
using the _expand_bucket method of the Count Tags algorithm. It then takes the
patterns with the best factor.

It works surprisingly well but tend to yield patterns that overlaps (different
patterns not different occurrences of one pattern). So it is better to get only
the first pattern from this class.

The constructor of this class takes an optional argument "tags" that has to be a
tag_tools.TagSet object. These are the tags to look at. If this argument is
missing, the class will look at a default list of tags.
"""
from collections import defaultdict
from repeat_pattern import RepeatPattern as RepeatPatternBase
from tag_tools import CONTAINER_TAGS

class RepeatPattern(RepeatPatternBase):
    """
        See module documentation
        """

    def __init__(self, tags=None, *args, **kw):
        RepeatPatternBase.__init__(self, *args, **kw)
        if tags:
            self._group_tags = tags
        else:
            self._group_tags = CONTAINER_TAGS

    def _find_group_tags(self):
        """ Here I do most of the work.
                1. Find all grouping tags.
                2. Expand around the tag.
                3. Add to list if factor is not zero.
                """
        lst = []
        for (tag, indices) in self._items_dict.iteritems():
            (tag, index) = tag
            if tag not in self._group_tags:
                continue
            if self.debug_level > 2:
                print 'Found:', tag
            indices_lst = zip(indices, indices)
            pattern = [tag]
            if len(indices_lst) > 1:
                indices_lst = self._expand_bucket(pattern, indices_lst, after_only=True)
            if self.debug_level > 3:
                self._print_list('Indices', indices_lst)
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
        results = self._find_group_tags()
        if not results:
            return 0
        else:
            if self.debug_level > 1:
                self._print_list('Grouping Tags', results)
            results.sort(key=lambda x: x[2], reverse=True)
            self.gather_occurrences(results, self._debug_print)
            return self.num_patterns


if __name__ == '__main__':
    pass