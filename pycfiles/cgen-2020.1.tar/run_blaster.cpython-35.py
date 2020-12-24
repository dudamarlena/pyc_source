# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgecore/blaster/run_blaster.py
# Compiled at: 2020-04-01 11:09:31
# Size of source mod 2**32: 6700 bytes
import sys, os, time, random, re, subprocess
from argparse import ArgumentParser
from blaster import Blaster
parser = ArgumentParser()
parser.add_argument('-i', '--input', help='Input file')
parser.add_argument('-l', '--input_list', help='File with list of files to analyse')
parser.add_argument('-d', '--databases', help='Comma seperated list of databases to blast against')
parser.add_argument('-o', '--out_path', help='output directory')
parser.add_argument('-b', '--blastPath', dest='blast_path', help='Path to blast', default='blastn')
parser.add_argument('-p', '--databasePath', dest='db_path', help='Path to the databases', default='')
parser.add_argument('-c', '--min_cov', dest='min_cov', help='Minimum coverage', type=float, default=0.6)
parser.add_argument('-t', '--threshold', dest='threshold', help='Blast threshold for identity', type=float, default=0.9)
parser.add_argument('--overlap', help='Allow hits/genes to overlap with this number of nucleotides. Default: 30.', type=int, default=30)
args = parser.parse_args()
min_cov = args.min_cov
threshold = args.threshold
input_list = []
if args.input is not None and args.input_list is not None:
    sys.exit('Input Error: Please only provide file list or single input file\n')
else:
    if args.input is None and args.input_list is None:
        sys.exit('Input Error: No Input were provided!\n')
    else:
        if args.input is not None and not os.path.exists(args.input):
            sys.exit('Input Error: Input file does not exist!\n')
        else:
            if args.input is not None:
                inputfile = args.input
                input_list.append(inputfile)
            else:
                if args.input_list is not None and not os.path.exists(args.input_list):
                    sys.exit('Input Error: No Input were provided!\n')
                elif args.input_list is not None:
                    inputfile = args.input_list
                    with open(inputfile, 'r') as (f):
                        for line in f:
                            line = line.rstrip()
                            input_list.append(line)

        if not os.path.exists(args.out_path):
            os.makedirs(args.out_path, exist_ok=True)
            out_path = args.out_path
        else:
            out_path = args.out_path
    if args.databases is None:
        sys.exit('Input Error: No databases sepcified!\n')
    else:
        databases = args.databases.split(',')
blast = args.blast_path
db_path = args.db_path
for inp_file in input_list:
    blast_run = Blaster(inputfile=inp_file, databases=databases, db_path=db_path, out_path=out_path, min_cov=min_cov, threshold=threshold, blast=blast, allowed_overlap=args.overlap)
    results = blast_run.results
    query_align = blast_run.gene_align_query
    homo_align = blast_run.gene_align_homo
    sbjct_align = blast_run.gene_align_sbjct
    file_name = inp_file.split('/')[(-1)].split('.')[0]
    out_name = '%s/%s_hit_alignments.txt' % (out_path, file_name)
    txt_file_seq_text = dict()
    pos_result = list()
    tab_file = '%s/%s_results.txt' % (out_path, file_name)
    tab = open(tab_file, 'w')
    for db in results:
        if results[db] == 'No hit found':
            tab.write('%s\n%s\n\n' % (db, results[db]))
        else:
            pos_result.append(db)
            tab.write('%s\n' % db)
            tab.write('Hit\tIdentity\tAlignment Length/Gene Length\tPosition in reference\tContig\tPosition in contig\n')
            txt_file_seq_text[db] = list()
            for hit in results[db]:
                header = results[db][hit]['sbjct_header']
                ID = results[db][hit]['perc_ident']
                sbjt_length = results[db][hit]['sbjct_length']
                HSP = results[db][hit]['HSP_length']
                positions_contig = '%s..%s' % (results[db][hit]['query_start'],
                 results[db][hit]['query_end'])
                positions_ref = '%s..%s' % (results[db][hit]['sbjct_start'],
                 results[db][hit]['sbjct_end'])
                contig_name = results[db][hit]['contig_name']
                tab.write('%s\t%.2f\t%s/%s\t%s\t%s\t%s\n' % (header, ID, HSP,
                 sbjt_length,
                 positions_ref,
                 contig_name,
                 positions_contig))
                ref_seq = sbjct_align[db][hit]
                hit_seq = query_align[db][hit]
                sbjct_start = results[db][hit]['sbjct_start']
                sbjct_end = results[db][hit]['sbjct_end']
                text = '%s, ID: %.2f %%, Alignment Length/Gene Length: %s/%s, Positions in reference: %s..%s, Contig name: %s, Position: %s' % (
                 header, ID, HSP, sbjt_length,
                 sbjct_start, sbjct_end, contig_name,
                 positions_contig)
                txt_file_seq_text[db].append((text, ref_seq, homo_align[db][hit],
                 hit_seq))

    tab.close()
    txt_file = open(out_name, 'w')
    for db in pos_result:
        txt_file.write('##################### %s #####################\n' % db)
        for text in txt_file_seq_text[db]:
            txt_file.write('%s\n\n' % text[0])
            for i in range(0, len(text[1]), 60):
                txt_file.write('%s\n' % text[1][i:i + 60])
                txt_file.write('%s\n' % text[2][i:i + 60])
                txt_file.write('%s\n\n' % text[3][i:i + 60])

            txt_file.write('\n')

    txt_file.close()