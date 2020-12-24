# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/biocyc/biocyc_chromosome_id_extractor.py
# Compiled at: 2016-02-16 15:21:39
import sys, os
try:
    from biocyc_parser import *
except ImportError:
    from sgs_utils.biocyc.biocyc_parser import *

CHROMOSOME = 'GENOME'
OUTPUT_HEADER = [
 'org_id', 'chromosome_id_list']

def get_chr(chr_species_map, species_file):
    species_map = load_flat_file(species_file)
    for organism in species_map:
        chr_list = []
        s = species_map[organism]
        if CHROMOSOME in s:
            chr_list = s[CHROMOSOME]
        else:
            sys.stderr.write('Warning: no chromosome in %s\n' % organism)
        chr_species_map[organism] = chr_list


def main(argv, prog=os.path.basename(sys.argv[0])):
    import argparse, textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('\t\tPrint in tabular format the chromosome list of an organism from its biocyc/metacyc flat files\n\n\t\texemple:\n\t\t%(prog)s species.dat > chromosome_list.txt\n\t\t'), prog=prog)
    parser.add_argument('specie_files', nargs='+', help='Biocyc flat species.dat file that contains the listing of chromosome id of the genome associated to an organism')
    parser.add_argument('-o', '--output', default=None, help='set an output file')
    parser.add_argument('-s', '--simple_output', default=False, action='store_true', help='Just display the list itself')
    args = parser.parse_args(argv)
    stream_out = sys.stdout
    if args.output:
        stream_out = open(args.output, 'w')
    if not args.simple_output:
        stream_out.write('%s\n' % ('\t').join(OUTPUT_HEADER))
    chr_species_map = {}
    for species_file in args.specie_files:
        get_chr(chr_species_map, species_file)

    for organism, chr_list in chr_species_map.items():
        if args.simple_output:
            stream_out.write('%s\n' % (' ').join(chr_list))
        else:
            stream_out.write('%s\t%s\n' % (organism, (' ').join(chr_list)))

    if args.output:
        stream_out.close()
    return


if __name__ == '__main__':
    main(sys.argv[1:])