# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/core/term_parsers.py
# Compiled at: 2019-09-30 13:55:18
# Size of source mod 2**32: 2412 bytes
from collections import defaultdict, Counter
import itertools, gzip

def read_termlist(terms):
    termlist = []
    with open(terms) as (nl):
        for line in nl:
            parts = line.strip().split()
            termlist.append(parts[0])

    return termlist


def parse_gaf_file(gaf_mappings, whole_list_counts=False):
    uniGO = defaultdict(set)
    if whole_list_counts:
        whole_list = []
    elif '.gz' in gaf_mappings:
        with gzip.open(gaf_mappings, 'rb') as (im):
            for line in im:
                line = line.decode('utf-8')
                parts = line.strip().split('\t')
                try:
                    if parts[4] != '':
                        uniGO[parts[1]].add(parts[4])
                    if whole_list_counts:
                        whole_list.append(parts[4])
                except Exception as es:
                    try:
                        print(es)
                    finally:
                        es = None
                        del es

    else:
        with open(gaf_mappings, 'r') as (im):
            for line in im:
                parts = line.strip().split('\t')
                try:
                    if parts[4] != '':
                        uniGO[parts[1]].add(parts[4])
                    if whole_list_counts:
                        whole_list.append(parts[4])
                except Exception as es:
                    try:
                        pass
                    finally:
                        es = None
                        del es

    if whole_list_counts:
        return (uniGO, whole_list)
    return uniGO


def read_topology_mappings(mapping):
    if isinstance(mapping, dict):
        return mapping
    components = defaultdict(set)
    with open(mapping) as (cf):
        for line in cf:
            node, module = line.strip().split()
            components[module].add(node)

    return components


def read_uniprot_GO(filename, verbose=True):
    unigo_counts, whole_termlist = parse_gaf_file(filename, whole_list_counts=True)
    term_counts = Counter(whole_termlist)
    all_terms = sum(list(term_counts.values()))
    if verbose:
        print('All annotations {}'.format(all_terms))
    return (unigo_counts, term_counts, all_terms)