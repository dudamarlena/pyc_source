# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/add_gene_name.py
# Compiled at: 2016-02-16 15:26:58
import sys, os, re
try:
    import utils
except ImportError:
    import sgs_utils.utils as utils

def compare_gene_list(a, b):
    return cmp(a[1], b[1]) or cmp(a[2], b[2])


def main(argv, prog=os.path.basename(sys.argv[0])):
    import argparse, textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent("\t\tChange the list of active genes in a SGS into a list of 'active','non active' and 'non catalytic' genes in the SGS with tags\n\n\t\texemple:\n\t\tpython %(prog)s sgs_list.tsv gene_list.tsv [-na reaction_list.txt]> sgs_list_with_gene_name.tsv\n\t\t"), prog=prog)
    parser.add_argument('sgs_file', help='SGS list file')
    parser.add_argument('gene_list', nargs='+', help='Gene listing')
    parser.add_argument('-o', '--output', default=None, help='set an output file')
    parser.add_argument('-t', '--tag', action='store_true', default=False, help='add catalytic/non-catalityc gene tag')
    parser.add_argument('-na', '--non_active', nargs='+', default=[], help='differenciate non-active from non-catalytic reaction list')
    parser.add_argument('-i', '--ignore_duplicates', action='store_true', default=False, help='Ignore duplicated error')
    args = parser.parse_args(argv)
    stream_out = sys.stdout
    if args.output:
        stream_out = open(args.output, 'w')
    map_gene_to_name = {}
    positions_map = {}
    for gene_file in args.gene_list:
        gene_header, gene_list = utils.load_csv_list(gene_file)
        for l in gene_list:
            chromosome_id = l[gene_header['chromosome_id']]
            gene_id = l[gene_header['gene_id']]
            left = int(l[gene_header['left_end_position']])
            right = int(l[gene_header['right_end_position']])
            gene_name = ''
            if 'gene_name' in gene_header:
                gene_name = l[gene_header['gene_name']]
            if gene_id not in map_gene_to_name:
                map_gene_to_name[(chromosome_id, gene_id)] = gene_name
            elif not arg.ignore_duplicates:
                sys.stderr.write(('Error: duplicated chromosome_id and gene_id {}, {}').format(chromosome_id, gene_id))
                exit(1)
            if gene_id not in map_gene_to_name:
                map_gene_to_name[('', gene_id)] = gene_name
            elif not arg.ignore_duplicates:
                sys.stderr.write(('Error: duplicated gene_id {}').format(gene_id))
                exit(1)
            if chromosome_id not in positions_map:
                positions_map[chromosome_id] = []
            positions_map[chromosome_id].append((gene_id, left, right))

    for positions in positions_map.values():
        positions.sort(compare_gene_list)

    sgs_header, sgs_list = utils.load_csv_list(args.sgs_file)
    catalytic_set = set()
    if args.tag or args.non_active:
        for reaction_file in args.non_active:
            reaction_header, reaction_list = utils.load_csv_list(reaction_file)
            for l in reaction_list:
                if 'association' in reaction_header:
                    catalytic_set.update(l[reaction_header['association']].split(' '))

    stream_out.write(('{}\t{}\n').format(utils.header_to_str(sgs_header), 'gene_name_set'))
    for l in sgs_list:
        gene_set = l[sgs_header['gene_set']].split(' ')
        chromosome_id = ''
        if 'chromosome_id' in sgs_header:
            chromosome_id = l[sgs_header['chromosome_id']]
        gene_name_list = []
        if not args.tag:
            for g in gene_set:
                gene_name_list.append(map_gene_to_name[(chromosome_id, g)])

        else:
            start = int(l[sgs_header['start_position']])
            end = int(l[sgs_header['end_position']])
            new_gene_list = []
            if start <= end:
                for i in range(start, end + 1):
                    g = positions_map[chromosome_id][i][0]
                    if g in gene_set:
                        new_gene_list.append('ac:' + g)
                        gene_name_list.append(('ac:', map_gene_to_name[(chromosome_id, g)]))
                    elif g in catalytic_set:
                        new_gene_list.append('na:' + g)
                        gene_name_list.append(('na:', map_gene_to_name[(chromosome_id, g)]))
                    else:
                        new_gene_list.append('nc:' + g)
                        gene_name_list.append(('nc:', map_gene_to_name[(chromosome_id, g)]))

            else:
                for i in range(end, len(positions_map[chromosome_id])):
                    g = positions_map[chromosome_id][i][0]
                    if g in gene_set:
                        new_gene_list.append('ac:' + g)
                        gene_name_list.append(('ac:', map_gene_to_name[(chromosome_id, g)]))
                    elif g in catalytic_set:
                        new_gene_list.append('na:' + g)
                        gene_name_list.append(('na:', map_gene_to_name[(chromosome_id, g)]))
                    else:
                        new_gene_list.append('nc:' + g)
                        gene_name_list.append(('nc:', map_gene_to_name[(chromosome_id, g)]))

                for i in range(0, start + 1):
                    g = positions_map[chromosome_id][i][0]
                    if g in gene_set:
                        new_gene_list.append('ac:' + g)
                        gene_name_list.append(('ac:', map_gene_to_name[(chromosome_id, g)]))
                    elif g in catalytic_set:
                        new_gene_list.append('na:' + g)
                        gene_name_list.append(('na:', map_gene_to_name[(chromosome_id, g)]))
                    else:
                        new_gene_list.append('nc:' + g)
                        gene_name_list.append(('nc:', map_gene_to_name[(chromosome_id, g)]))

            l[sgs_header['gene_set']] = (' ').join(new_gene_list)
        stream_out.write(('{}\t{}\n').format(('\t').join(l), (' ').join([ g[0] + '"' + g[1] + '"' for g in gene_name_list ])))

    if args.output:
        stream_out.close()
    return


if __name__ == '__main__':
    main(sys.argv[1:])