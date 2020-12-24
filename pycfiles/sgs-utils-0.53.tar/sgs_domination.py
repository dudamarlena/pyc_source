# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/sgs_domination.py
# Compiled at: 2016-04-04 15:59:15
import csv, os, sys

def load(file):
    result = {}
    head = ''
    headers = {}
    with open(file, 'rb') as (input_file):
        line_reader = csv.reader(input_file, delimiter='\t', quotechar='#')
        head = line_reader.next()
        for i in range(0, len(head)):
            headers[head[i]] = i

        chr = ''
        org = ''
        for row in line_reader:
            if 'chr_id' in headers:
                chr = row[headers['chr_id']]
                if 'org_id' in headers:
                    chr = row[headers['org_id']]
            density = float(row[headers['density']])
            s = (
             org, chr, frozenset(row[headers['gene_set']].split(' ')))
            if s not in result:
                result[s] = (
                 density, list())
            result[s][1].append(row)

    return (
     headers, head, result)


def main(argv, prog=os.path.basename(sys.argv[0])):
    import argparse, textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('\t\tGenerate the dominant SGS list from a SGS list\n\n\t\texemple:\n\t\t%(prog)s sgs_list.tsv > dominant_sgs_list.tsv\n\t\t'), prog=prog)
    parser.add_argument('sgs_file', help='SGS list in .tsv file format')
    parser.add_argument('-o', '--output', default=None, help='set an output file')
    args = parser.parse_args(argv)
    stream_out = sys.stdout
    if args.output:
        stream_out = open(args.output, 'w')
    to_remove = set()
    map_overset_of = {}
    headers, head, sgs_list = load(args.sgs_file)
    gene_set_to_reaction_set = {}
    if 'reaction_set' in headers:
        for fset, values in sgs_list.items():
            density, rows = values
            gene_set_to_reaction_set[fset] = set(rows[0][headers['reaction_set']].split())

    for fset1, values1 in sgs_list.items():
        density1, rows1 = values1
        org1, chr1, gene_set1 = fset1
        for fset2, values2 in sgs_list.items():
            density2, rows2 = values2
            org2, chr2, gene_set2 = fset2
            if org1 == org2 and chr1 == chr2 and gene_set1 < gene_set2 and density1 <= density2:
                to_remove.add(fset1)
                if fset2 not in map_overset_of:
                    map_overset_of[fset2] = set()
                map_overset_of[fset2].add(fset1)
            if 'reaction_set' in headers and fset1 == fset2:
                s = gene_set_to_reaction_set[fset1] | gene_set_to_reaction_set[fset2]
                gene_set_to_reaction_set[fset1] = s
                gene_set_to_reaction_set[fset2] = s

    remove_from_headers = []
    if 'start_reaction' in headers:
        remove_from_headers.append(headers['start_reaction'])
    if 'end_reaction' in headers:
        remove_from_headers.append(headers['end_reaction'])
    remove_from_headers.sort()
    remove_from_headers.reverse()
    for i in remove_from_headers:
        head.pop(i)

    stream_out.write('%s\n' % ('\t').join(head))
    for fset, values in sgs_list.items():
        if fset not in to_remove:
            density, rows = values
            row = rows[0]
            if 'reaction_set' in headers:
                row[headers['reaction_set']] = (' ').join(gene_set_to_reaction_set[fset])
            for i in remove_from_headers:
                row.pop(i)

            stream_out.write('%s\n' % ('\t').join(row))

    if args.output:
        stream_out.close()
    return


if __name__ == '__main__':
    main(sys.argv[1:])