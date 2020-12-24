# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/sRNA_antisense.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 3383 bytes
import os, csv, shutil
from annogesiclib.gff3 import Gff3Parser

def compare_srna_gff(gffs, strain, strand, start, end, srna_types, file_type):
    for gff in gffs:
        if strain == gff.seq_id and strand != gff.strand and (start <= gff.start and end >= gff.end or start >= gff.start and end <= gff.end or start <= gff.start and end <= gff.end and end >= gff.start or start >= gff.start and start <= gff.end and end >= gff.end):
            if file_type == 'gff':
                if 'antisense' not in srna_types:
                    srna_types = srna_types + ',' + 'antisense'
            elif 'Antisense' not in srna_types:
                srna_types = srna_types + ',' + 'Antisense'

    return srna_types


def srna_antisense(srna_gff, srna_table, gff_file):
    tmp_srna_gff = srna_gff + 'tmp'
    tmp_srna_table = srna_table + 'tmp'
    out = open(tmp_srna_gff, 'w')
    out.write('##gff-version 3\n')
    out_t = open(tmp_srna_table, 'w')
    out_t.write('\t'.join(['Rank', 'Genome', 'Name', 'Start', 'End', 'Strand',
     'Start_with_TSS/Cleavage_site', 'End_with_cleavage',
     'Candidates', 'Lib_type', 'Best_avg_coverage',
     'Best_highest_coverage', 'Best_lower_coverage',
     'Track/Coverage',
     'Normalized_secondary_energy_change(by_length)',
     'sRNA_types', 'Confliction_of_sORF',
     'nr_hit_number', 'sRNA_hit_number',
     'nr_hit_top3|ID|e-value', 'sRNA_hit|e-value',
     'Overlap_CDS', 'Overlap_percent',
     'End_with_terminator']) + '\n')
    srnas = []
    sf = open(srna_gff, 'r')
    for entry in Gff3Parser().entries(sf):
        srnas.append(entry)

    tabs = []
    fh = open(srna_table, 'r')
    for row in csv.reader(fh, delimiter='\t'):
        if row[0] != 'rank':
            tabs.append({'info': row, 'strain': row[1], 'strand': row[5], 
             'start': int(row[3]), 'end': int(row[4]), 
             'srna_type': row[15]})
        else:
            out_t.write('\t'.join(row) + '\n')

    gffs = []
    gf = open(gff_file, 'r')
    for entry in Gff3Parser().entries(gf):
        gffs.append(entry)

    for srna in srnas:
        compare_srna_gff(gffs, srna.seq_id, srna.strand, srna.start, srna.end, srna.attributes['sRNA_type'], 'gff')
        attribute_string = ';'.join(['='.join(items) for items in srna.attributes.items()])
        out.write('\t'.join([srna.info_without_attributes,
         attribute_string]) + '\n')

    for tab in tabs:
        compare_srna_gff(gffs, tab['strain'], tab['strand'], tab['start'], tab['end'], tab['srna_type'], 'table')
        tab['info'][15] = tab['srna_type']
        out_t.write('\t'.join(tab['info']) + '\n')

    os.remove(srna_gff)
    shutil.move(tmp_srna_gff, srna_gff)
    os.remove(srna_table)
    shutil.move(tmp_srna_table, srna_table)