# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cornish/dev/envs/flextime/lib/python3.5/site-packages/flextime/utils.py
# Compiled at: 2017-11-10 13:08:03
# Size of source mod 2**32: 955 bytes
import yaml, os.path
from functools import reduce

def guess_path(tree, words):

    def build_path(acc, word):
        tree, path_parts = acc
        path_parts[(-1)].append(word)
        key = ' '.join(path_parts[(-1)])
        if key in tree:
            tree = tree[key]
            path_parts.append([])
        return (tree, path_parts)

    tree, path_lists = reduce(build_path, words, (tree, [[]]))
    return [' '.join(p) for p in path_lists if p]


def file_to_dict(filename):
    if os.path.isfile(filename):
        with open(filename) as (f):
            return yaml.safe_load(f)
    else:
        print('{} not found; skipping.'.format(filename))


def date_to_str(d):
    date_format = '%m-%d-%Y'
    return d.strftime(date_format)


def dump_dict(d):
    noalias_dumper = yaml.dumper.SafeDumper
    noalias_dumper.ignore_aliases = lambda self, date: True
    return yaml.dump(d, default_flow_style=False, Dumper=noalias_dumper)