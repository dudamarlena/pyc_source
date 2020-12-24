# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/sRNA_filter_frag.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 2051 bytes
import os, csv, shutil
from annogesiclib.gff3 import Gff3Parser

def filter_frag(srna_table, srna_gff):
    out = open('tmp_srna.gff', 'w')
    out_ta = open('tmp_srna.csv', 'w')
    out.write('##gff-version 3\n')
    gffs = []
    tables = []
    gff_parser = Gff3Parser()
    g_f = open(srna_gff, 'r')
    for entry in gff_parser.entries(g_f):
        gffs.append(entry)

    fh = open(srna_table, 'r')
    for row in csv.reader(fh, delimiter='\t'):
        tables.append(row)

    new_gffs = []
    for gff in gffs:
        if 'UTR_type' in gff.attributes.keys():
            if '5utr' in gff.attributes['UTR_type'] or 'interCDS' in gff.attributes['UTR_type']:
                for table in tables:
                    if gff.seq_id == table[0] and gff.start == int(table[2]) and gff.end == int(table[3]) and gff.strand == table[4] and 'frag' in table[5]:
                        new_gffs.append(gff)

            elif '3utr' in gff.attributes['UTR_type']:
                new_gffs.append(gff)
        else:
            new_gffs.append(gff)

    new_tables = []
    for table in tables:
        for gff in new_gffs:
            if gff.seq_id == table[0] and gff.start == int(table[2]) and gff.end == int(table[3]) and gff.strand == table[4]:
                new_tables.append(table)
                out_ta.write('\t'.join(table) + '\n')

    for gff in new_gffs:
        for table in new_tables:
            if gff.seq_id == table[0] and gff.start == int(table[2]) and gff.end == int(table[3]) and gff.strand == table[4]:
                out.write(gff.info + '\n')

    g_f.close()
    fh.close()
    out.close()
    out_ta.close()
    os.remove(srna_gff)
    os.remove(srna_table)
    shutil.move('tmp_srna.gff', srna_gff)
    shutil.move('tmp_srna.csv', srna_table)