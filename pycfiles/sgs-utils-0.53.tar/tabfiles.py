# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/libs/tabfiles.py
# Compiled at: 2016-01-21 15:18:58
import sys, os, csv

def str_to_bool(s):
    if s.lower() == 'true':
        return True
    if s.lower() == 'false':
        return False
    raise ValueError


def load_list_file(infile):
    with open(infile, 'r') as (reader):
        result = reader.read().replace('\r\n', '\n').splitlines()
    reader.close()
    return result


def apply_mapping(gene_list, mapping):
    if mapping == {}:
        return gene_list
    result = []
    for g in gene_list:
        if g in mapping:
            result.append(mapping[g])
        else:
            sys.stderr.write('%s has no mapped value\n' % g)
            result.append(g)

    return result


def generate_map_gene_to_position(genes_seq):
    result = {}
    i = 0
    for g in genes_seq:
        result[g] = i
        i = i + 1

    return result


def header_to_str(header_map, sep='\t'):
    tab = list()
    tmp = {}
    for key, value in header_map.items():
        tmp[value] = key

    order = tmp.keys()
    order.sort()
    for key in order:
        tab.append(tmp[key])

    return sep.join(tab)


def load_tab_file(file_name):
    headers = {}
    lines = []
    with open(file_name, 'r') as (in_file):
        rows = in_file.read().replace('\r\n', '\n').replace('"', '').splitlines()
        i = 0
        for e in rows[0].split('\t'):
            headers[e] = i
            i = i + 1

        for l in rows[1:]:
            if not l.startwith('#'):
                lines.append(l.split('\t'))

    in_file.close()
    return (headers, lines)


def load_csv_list(csv_file):
    lines = []
    headers = {}
    with open(csv_file, 'rb') as (in_csv):
        node_reader = csv.reader(in_csv, delimiter='\t', quotechar='#')
        i = 0
        for elem in node_reader.next():
            headers[elem] = i
            i = i + 1

        for row in node_reader:
            lines.append(row)

    in_csv.close()
    return (headers, lines)


def load_map_id_to_set(file_map, keep_empty=False, sep=None, silent_warning=False):
    result = {}
    with open(file_map, 'r') as (in_map):
        lines = in_map.read().replace('\r\n', '\n').splitlines()
        for row in lines:
            l = row.split(sep)
            if not row.startswith('#') and (keep_empty or not keep_empty and len(l) > 1):
                if l[0] not in result:
                    result[l[0]] = set()
                else:
                    if not silent_warning:
                        sys.stderr.write('Warning: %s has multiple lines. Value sets will be fused\n' % l[0])
                    value = result[l[0]]
                    for v in l[1:]:
                        value.add(v)

    in_map.close()
    return result


def reverse_map_id_to_set(mapping):
    result = {}
    for key, values in mapping.items():
        for v in values:
            if v not in result:
                result[v] = set()
            result[v].add(key)

    return result


def load_map_id_to_list(file_map, keep_empty=False, sep=None, silent_warning=False):
    result = {}
    with open(file_map, 'r') as (in_map):
        lines = in_map.read().replace('\r\n', '\n').splitlines()
        for row in lines:
            l = row.split(sep)
            if not row.startswith('#') and (keep_empty or not keep_empty and len(l) > 1):
                if l[0] not in result:
                    result[l[0]] = list()
                else:
                    if not silent_warning:
                        sys.stderr.write('Warning: %s has multiple lines. Value list will be concatenated\n' % l[0])
                    value = result[l[0]]
                    for v in l[1:]:
                        value.append(v)

    in_map.close()
    return result