# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/algo_dict.py
# Compiled at: 2010-10-16 07:02:00
"""
This is a data module that defines a global dictionary that carry the different
RepeatPattern algorithms meta and optional configuration data. The keys of this
dictionary are the implementation classes of the algorithms. The values are an
AlgoData class (defined below), this class is similar to a named-tuple.

There is a help function update_algo_dict to update this configuration
dictionary from a custom file. The file should define a Python dictionary of
dictionaries. The keys of the outer dictionary has to be the names of the
algorithms as they appear in the algo_dict below. The keys of the inner
dictionary has to be names in the FIELDS tuple you want to change.

This sample dictionary will change the "minimum coverage" of the Count Tags
algorithm and enable the Titles algorithm:

{
        "Count Tags": {
                "min_coverage": 0.5,
        },
        "Titles": {
                "enabled": True,
        },
}

This module is mainly for the htmllist_demo script, or for future modules that
will use HtmlList. Run as a script to see the algorithms meta-data.
"""
from repeat_pattern import RepeatPattern
from repeat_pattern2 import RepeatPattern as RepeatPatternTree
from repeat_pattern3 import RepeatPattern as RepeatGroupingTags
from repeat_pattern_suffix import RepeatPattern as RepeatPatternArray
from repeat_title import RepeatPattern as RepeatTitle
FIELDS = ('name', 'desc', 'enabled', 'order', 'min_quality', 'algo_factor', 'min_len',
          'max_len', 'min_repeat', 'max_repeat', 'max_stdv', 'min_weight', 'min_coverage',
          'min_comp', 'max_patterns')

class AlgoData(object):
    """ Like named-tuple but can handle optional arguments. It also has an
        "update" method. """
    __slots__ = FIELDS

    def __init__(self, **kw):
        self.update(kw)

    def __getattr__(self, name):
        if name in FIELDS:
            return
        else:
            raise AttributeError("AlgoData doesn't have %s" % name)
            return

    def update(self, dic):
        for (name, val) in dic.items():
            setattr(self, name, val)


def update_algo_dict(filename):
    """ A function to update the global algo_dict with partial dictionary of
        dictionaries. 'filename' is the name of the file that define this dictionary.
        """
    global algo_dict
    with open(filename) as (fl):
        new_dict = eval(fl.read())
        for (cls, dic) in algo_dict.items():
            if new_dict.has_key(dic.name):
                algo_dict[cls].update(new_dict[dic.name])

    return algo_dict


algo_dict = {RepeatPattern: AlgoData(name='Count Tags', desc='Counts the tags in (sub sections of) the HTML page and groups them to sequences. Then it tries to expand the best groups.', order=10, min_quality=0.6, algo_factor=1, enabled=True, max_patterns=3), 
   RepeatTitle: AlgoData(name='Titles', desc='Not much of an algorithm, simply look for Hx tags', order=22, algo_factor=0.5, min_quality=0.9, enabled=False), 
   RepeatGroupingTags: AlgoData(name='Grouping Tags', desc='Similar to Titles, looks for certain individual grouping tags', order=20, algo_factor=0.5, min_quality=0.9, enabled=True), 
   RepeatPatternTree: AlgoData(name='Tags Pattern Tree', desc='Finds repetitive patterns using suffix tree', order=32, algo_factor=0.3, min_quality=0.9, enabled=False), 
   RepeatPatternArray: AlgoData(name='Tags Pattern Array', desc='Finds repetitive patterns using suffix array', order=30, algo_factor=0.3, min_quality=0.9, enabled=True)}
if __name__ == '__main__':
    key_val = algo_dict.items()
    key_val.sort(key=lambda x: x[1].order)
    for (cls, data) in key_val:
        print 'Name:', data.name
        print 'Descriptiopn:', data.desc
        print 'Enabled:', data.enabled
        print 'Order:', data.order
        print 'Class:', cls
        print '----------------------------------'