# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/shogen2tab.py
# Compiled at: 2016-04-04 15:53:09
import sys, os, re
try:
    from utils import *
except ImportError:
    try:
        from .utils import *
    except ValueError:
        from sgs_utils.utils import *

def format(block_str, map_gene_to_position, mapping, length_limit, block_mode):
    block = block_str.split('\n')
    result = ''
    length = 0
    length_previous = 0
    gene_set = set()
    m = re.match('^[0-9]+ best gene units catalyzing pathway from reaction (\\S+) to (\\S+)', block[0])
    if m != None:
        r_start = m.group(1)
        r_end = m.group(2)
        for i in xrange(1, len(block)):
            if length <= length_limit:
                m = re.match('length: ([0-9]+)', block[i])
                if m != None:
                    length_previous = length
                    length = int(m.group(1))
                    if block_mode == 'rank' and length_previous != length and gene_set != set():
                        sg, density = genomic_density(gene_set, map_gene_to_position)
                        sg_start, sg_end = sg
                        gene_set = apply_mapping(gene_set, mapping)
                        result = result + '%s\n' % ('\t').join([r_start, r_end, str(sg_start), str(sg_end), str(length), str(density), (' ').join(gene_set)])
                        gene_set.clear()
                else:
                    m = re.match('[0-9]+: *(.+)  $', block[i])
                    if m != None:
                        gene_list = re.split(' +', m.group(1))
                        if block_mode == 'segment':
                            sg, density = genomic_density(gene_list, map_gene_to_position)
                            sg_start, sg_end = sg
                            gene_list = apply_mapping(gene_list, mapping)
                            gene_list.sort()
                            result += '%s\n' % ('\t').join([r_start, r_end, str(sg_start), str(sg_end), str(length), str(density), (' ').join(gene_list)])
                        else:
                            for g in gene_list:
                                gene_set.add(g)

    if gene_set != set():
        sg, density = genomic_density(gene_set, map_gene_to_position)
        sg_start, sg_end = sg
        gene_set = apply_mapping(gene_set, mapping)
        result = result + '%s\n' % ('\t').join([r_start, r_end, str(sg_start), str(sg_end), str(length), str(density), (' ').join(gene_set)])
    return result


def main(argv, prog=os.path.basename(sys.argv[0])):
    import argparse, textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('\t\tPrint in tabular format the SGS obtained by shogen\n\n\t\texemple:\n\t\t%(prog)s gene_seq.txt < sgs.txt > sgs.tsv\n\t\t'), prog=prog)
    parser.add_argument('gene_seq', help='Gene sequence file to compute additonal information')
    parser.add_argument('-o', '--output', default=None, help='set an output file')
    parser.add_argument('-l', '--length_limit', type=int, default=sys.maxint, help='Filter the length of SGS according to a limit')
    parser.add_argument('-t', '--translate', default=None, help='Translate SGS gene id with the given dictionnary', metavar='DICTIONNARY')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='quiet mode')
    args = parser.parse_args(argv)
    block_mode = 'segment'
    stream_out = sys.stdout
    if args.output:
        stream_out = open(args.output, 'w')
    if not args.quiet:
        sys.stderr.write('%s mode with a limit of %d\n' % (args.block_mode, args.length_limit))
    mapping = {}
    if args.mapping != None:
        mapping = load_map_id_to_list(args.mapping, sep='\t')
    genome = load_gene_sequence(args.gene_seq)
    map_gene_to_position = generate_map_gene_to_position(genome)
    lines = sys.stdin.readlines()
    stream_out.write('%s\n' % ('\t').join(['start_reaction', 'end_reaction', 'start_position', 'end_position', 'length', 'density', 'gene_set']))
    block = ''
    for l in lines:
        if l == '\n':
            stream_out.write(format(block, map_gene_to_position, mapping, args.length_limit, block_mode))
            block = ''
        else:
            block += l

    if block != '':
        stream_out.write(format(block, map_gene_to_position, mapping, args.length_limit, block_mode))
    if args.output:
        stream_out.close()
    return


if __name__ == '__main__':
    main(sys.argv[1:])