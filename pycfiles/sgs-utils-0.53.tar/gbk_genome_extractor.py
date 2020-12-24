# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/gbk/gbk_genome_extractor.py
# Compiled at: 2016-04-05 18:25:50
import sys, os, re, Bio
from Bio import SeqIO
DEFAULT_FIELD_OF_GENE_ID = 'locus_tag'
DB_XREF = 'db_xref'
GENE_SYNONYM = 'gene_synonym'
FIELD_LIST = ['locus_tag', 'gene', DB_XREF, GENE_SYNONYM, 'EC_number', 'protein_id', 'product', 'old_locus_tag', 'note']

def read_gbk(gbk_file, feature_type):
    seq_result = {}
    for gene_seq in SeqIO.parse(gbk_file, 'genbank'):
        result = {}
        for f in gene_seq.features:
            if f.type == 'source':
                chr_start = f.location.start
                chr_end = f.location.end
            if f.type in feature_type:
                gene_name = ''
                start = len(gene_seq)
                end = -1
                direction = ''
                if float(Bio.__version__) <= 1.62:
                    start = f.location.start
                    end = f.location.end
                    if f.strand < 0:
                        direction = direction + '-'
                    elif f.strand > 0:
                        direction = direction + '+'
                    else:
                        direction = direction + '?'
                else:
                    for pos in f.location.parts:
                        start = min(start, int(pos.start))
                        end = max(end, int(pos.end))
                        if pos.strand < 0:
                            direction = direction + '-'
                        elif pos.strand > 0:
                            direction = direction + '+'
                        else:
                            direction = direction + '?'

                if start == chr_start and end == chr_end:
                    start = f.location.parts[0].start
                    end = f.location.parts[(-1)].end
                    if start < end:
                        start = f.location.parts[(-1)].start
                        end = f.location.parts[0].end
                start = start + 1
                gene_id = ('G_{}_{}').format(start, end)
                if gene_id not in result:
                    result[gene_id] = {'start': start, 'end': end, 'dir': direction}
                else:
                    if result[gene_id]['start'] != start or result[gene_id]['end'] != end:
                        sys.stderr.write('Error: non consistent position between %s at [%d..%d] vs [%d..%d]\n' % ('(' + (' ').join(feature_type) + ')', result[gene_id]['start'], result[gene_id]['end'], start, end))
                        sys.exit(1)
                    for key, value in f.qualifiers.items():
                        if key not in result[gene_id]:
                            result[gene_id][key] = set()
                        result[gene_id][key].update(value)

        seq_result[gene_seq.id] = (
         len(gene_seq), result)

    return seq_result


def extract_info(genome_map, supp_field_list, alt_id=None):
    result = []
    db_xref_set = set()
    db_xref_gene_map = {}
    field_list = list(FIELD_LIST)
    if alt_id and alt_id not in field_list and alt_id not in supp_field_list:
        field_list = [
         alt_id] + field_list
    for f in supp_field_list:
        if f not in field_list:
            field_list.append(f)

    for chr_id, gene_listing in genome_map.items():
        alt_id_set = set()
        for gene_id, field_map in gene_listing.items():
            if alt_id == None:
                line = [
                 chr_id, gene_id, field_map['start'], field_map['end'], field_map['dir']]
            else:
                if alt_id in field_map:
                    g = field_map[alt_id].pop()
                    field_map[alt_id].add(g)
                    if g not in alt_id_set:
                        alt_id_set.add(g)
                        line = [chr_id, g, field_map['start'], field_map['end'], field_map['dir']]
                    else:
                        sys.stderr.write("Error: alternative id '%s' is duplicated (%s) and cannot be used as an id\n" % (alt_id, g))
                        sys.exit(1)
                else:
                    sys.stderr.write("Error: alternative id '%s' is missing for feature [%d..%d]\n" % (alt_id, field_map['start'], field_map['end']))
                    sys.exit(1)
                for field in field_list:
                    if field in field_map:
                        values = field_map[field]
                        if field == DB_XREF:
                            db_xref_gene_map[(chr_id, gene_id)] = {}
                            for v in values:
                                db, id_v = v.split(':')
                                db_xref_set.add(db)
                                db_xref_gene_map[(chr_id, gene_id)][db] = id_v

                        if field == GENE_SYNONYM:
                            values = [ re.sub(';', '', v) for v in values ]
                        else:
                            line.append((' ').join(values))
                    else:
                        line.append('')

            result.append(line)

    return result


def compare_gene_list(a, b):
    return cmp(a[0], b[0]) or cmp(a[2], b[2]) or cmp(a[3], b[3])


OUTPUT_HEADER = [
 'chromosome_id', 'gene_id', 'left_end_position', 'right_end_position', 'transcription_direction'] + FIELD_LIST

def main(argv, prog=os.path.basename(sys.argv[0])):
    import argparse, textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('\t\tExtract, from a list of GenBank files (.gbk), the list of genes with their respective chromosome id, left end position, right end position and transcription direction and write it to the standard output in tabular file format (.tsv)\n\n\t\texemple:\n\t\t%(prog)s chr1.gbk chr2.gbk... > gene_list.txt\n\t\t'), prog=prog)
    chrp = parser.add_argument_group(title='chromosome files')
    chrp.add_argument('chr_files', type=argparse.FileType('r'), nargs='+', help='a list of GenBank (.gbk) files')
    parser.add_argument('-o', '--output', default=None, help='set an output file')
    parser.add_argument('-chr', '--chromosome_length', type=argparse.FileType('w'), help='produce the list of chromosomes and their respective length in the CHROMOSOME_LIST_OUTPUT file', metavar='CHROMOSOME_LIST_OUTPUT')
    filedp = parser.add_argument_group(title='optional switches')
    filedp.add_argument('-alt_id', '--alternate_id', type=str, default=None, help='select the specified field (like locus_tag) as the id of the gene if possible')
    filedp.add_argument('-f', '--add_field', type=str, nargs='+', default=[], metavar='FIELD', help='add columns listing the values in the selected fields')
    filedp.add_argument('-feat', '--features', type=str, nargs='+', default=['CDS'], metavar='FEAT', help='Which feature(s) to take in account. When many are given, (1) check the consitensy of position and ids and (2) fuse the annotations (default: %(default)s)')
    parser.add_argument('-q', '--quiet', help='quiet mode', action='store_true')
    args = parser.parse_args(argv)
    stream_out = sys.stdout
    if args.output:
        stream_out = open(args.output, 'w')
    if args.quiet:
        sys.stderr.write('quiet option not implemented now\n')
    supp_field_list = args.add_field
    genome_map = {}
    length_map = {}
    for gbk_file in args.chr_files:
        for chr_id, c in read_gbk(gbk_file, args.features).items():
            chr_length, gene_listing = c
            genome_map[chr_id] = gene_listing
            length_map[chr_id] = chr_length

    gene_list = extract_info(genome_map, supp_field_list, args.alternate_id)
    gene_list.sort(compare_gene_list)
    head = OUTPUT_HEADER + supp_field_list
    stream_out.write('%s\n' % ('\t').join(head))
    for elem in gene_list:
        line = [ str(i) for i in elem ]
        stream_out.write('%s\n' % ('\t').join(line))

    if args.output:
        stream_out.close()
    if args.chromosome_length:
        args.chromosome_length.write('chromosome_id\tlength\n')
        for k, v in length_map.items():
            args.chromosome_length.write(('{}\t{}\n').format(k, v))

    return


if __name__ == '__main__':
    main(sys.argv[1:])