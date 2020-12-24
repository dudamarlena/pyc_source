# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/biocyc/biocyc_genome_extractor.py
# Compiled at: 2016-02-16 12:14:58
import sys, os
try:
    from biocyc_parser import *
except ImportError:
    from sgs_utils.biocyc.biocyc_parser import *

try:
    from biocyc_chromosome_id_extractor import get_chr
except ImportError:
    from sgs_utils.biocyc.biocyc_chromosome_id_extractor import get_chr

TRANSCRIPTION_DIRECTION = 'TRANSCRIPTION-DIRECTION'
LEFT = 'LEFT-END-POSITION'
RIGHT = 'RIGHT-END-POSITION'
COMPONENT_OF = 'COMPONENT-OF'
COMMON_NAME = 'COMMON-NAME'

def generate_gene_listing(genes_map, chr_list, metacyc_new, supplementary_fields):
    result = []
    for gene_id, attributes in genes_map.items():
        try:
            chr_id = attributes[COMPONENT_OF]
            if metacyc_new:
                chr_id_corr = set()
                for c in chr_id:
                    chr_id_corr.add(c.rsplit('-', 1)[0])

                chr_id = chr_id_corr
            for c in chr_id:
                if c in chr_list:
                    try:
                        left = int(attributes[LEFT][0])
                        right = int(attributes[RIGHT][0])
                        direction = attributes[TRANSCRIPTION_DIRECTION]
                        line = [c, gene_id, left, right, (' ').join(direction)]
                        for field in supplementary_fields:
                            f = ''
                            if field in attributes:
                                f = attributes[field]
                            line.append((' ').join(f))

                        result.append(line)
                    except KeyError:
                        sys.stderr.write('Warning: %s has no left or right end position registred\n' % gene_id)

        except KeyError:
            sys.stderr.write('Warning: %s is not attached to a chromosome\n' % gene_id)

    return result


def compare_gene_list(a, b):
    return cmp(a[0], b[0]) or cmp(a[2], b[2]) or cmp(a[3], b[3])


OUTPUT_HEADER = [
 'chromosome_id', 'gene_id', 'left_end_position', 'right_end_position', 'transcription_direction']

def main(argv, prefix=[]):
    import argparse, textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('\t\tPrint in tabular format the gene list of an organism from its biocyc/metacyc flat files\n\n\t\texemple:\n\t\tpython %(prog)s genes.dat species.dat ECOLI > genome.txt\n\t\t'))
    parser.add_argument('genes_file', help='Biocyc flat genes.dat file')
    parser.add_argument('species_file', help='Biocyc flat species.dat file that contains the listing of chromosome id of the genome associated to an organism')
    parser.add_argument('-o', '--output', default=None, help='set an output file')
    parser.add_argument('-org', '--organism', nargs='+', help='Selected organism ids')
    parser.add_argument('-sf', '--supplementary_fields', nargs='+', default=[], help='Add custom supplementary fields in the tabular files')
    parser.add_argument('-sc', '--selected_chromosomes', nargs='+', default=None, help='list of selected chromosomes id')
    biocyc_version = parser.add_mutually_exclusive_group()
    biocyc_version.add_argument('-new', '--metacyc_new', action='store_true', help='Manage metacyc 18.5+ flatfiles format')
    biocyc_version.add_argument('-old', '--metacyc_old', action='store_false', help='Manage metacyc 18.0- flatfiles format')
    args = parser.parse_args(argv)
    chr_list = []
    chr_species_map = {}
    get_chr(chr_species_map, args.species_file)
    v185 = True
    if not args.metacyc_old:
        v185 = False
    stream_out = sys.stdout
    if args.output:
        stream_out = open(args.output, 'w')
    if not args.organism:
        args.organism = chr_species_map.keys()
    for organism in args.organism:
        if organism in chr_species_map:
            chr_list = chr_species_map[organism]
        else:
            sys.stderr.write('Error: no specie %s in %s\n' % (organism, args.species_file))
            sys.exit()

    if args.selected_chromosomes:
        chr_list = list(set(chr_list).intersection(args.selected_chromosomes))
    genes_map = load_flat_file(args.genes_file)
    gene_list = generate_gene_listing(genes_map, chr_list, v185, args.supplementary_fields)
    gene_list.sort(compare_gene_list)
    head = OUTPUT_HEADER + args.supplementary_fields
    stream_out.write('%s\n' % ('\t').join(head))
    for elem in gene_list:
        line = [ str(i) for i in elem ]
        stream_out.write('%s\n' % ('\t').join(line))

    if args.output:
        stream_out.close()
    return


if __name__ == '__main__':
    main(sys.argv[1:])