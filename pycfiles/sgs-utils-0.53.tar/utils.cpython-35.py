# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filou/git/work/sgs-utils/sgs_utils/utils.py
# Compiled at: 2015-03-18 21:08:53
# Size of source mod 2**32: 4885 bytes
import sys, os, csv

def load_gene_sequence(genome_file):
    with open(genome_file, 'r') as (in_gene_seq):
        genes_seq = in_gene_seq.read().replace('\r\n', '\n').splitlines()
    in_gene_seq.close()
    return genes_seq


def genomic_density(genes, map_gene_to_position):
    positions = list()
    for g in genes:
        positions.append(map_gene_to_position[g])

    positions.sort()
    interval = (0, 0)
    max_size = -2
    size = -2
    for i in xrange(0, len(positions)):
        deb = positions[i]
        fin = positions[((i + 1) % len(positions))]
        if fin < deb:
            size = len(map_gene_to_position) - (deb - fin + 1)
        else:
            size = fin - deb - 1
        if size > max_size:
            max_size = size
            interval = (fin, deb)

    if max_size < 0:
        max_size = len(map_gene_to_position) + max_size
    return (
     interval, len(genes) / float(len(map_gene_to_position) - max_size))


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


def load_map_id_to_set(file_map, keep_empty=False, sep=None, silent_warning=False):
    result = {}
    with open(file_map, 'r') as (in_map):
        lines = in_map.read().replace('\r\n', '\n').splitlines()
        for row in lines:
            l = row.split(sep)
            if keep_empty or not keep_empty and len(l) > 1:
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
            if keep_empty or not keep_empty and len(l) > 1:
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