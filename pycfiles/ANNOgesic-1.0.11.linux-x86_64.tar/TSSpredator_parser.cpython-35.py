# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/TSSpredator_parser.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 1885 bytes
import csv

class TSSPredatorReader(object):

    def entries(self, input_fh):
        for row in csv.reader(input_fh, delimiter='\t'):
            if row[0].startswith('SuperPos'):
                pass
            else:
                yield TSSPredatorEntry(row)


class TSSPredatorEntry(object):

    def __init__(self, row):
        assert len(row) == 28
        self.super_pos = int(row[0])
        self.super_strand = row[1]
        self.map_count = int(row[2])
        self.det_count = int(row[3])
        self.genome = row[4]
        self.is_detected = True if row[5] == '1' else False
        self.is_enriched = True if row[6] == '1' else False
        self.step_heigth = row[7]
        self.step_factor = row[8]
        self.enrichment_factor = row[9]
        self.class_count = int(row[10])
        self.pos = int(row[11])
        self.strand = row[12]
        self.locus_tag = row[13]
        self.srna_asrna = row[14]
        self.product = row[15]
        self.utr_length = row[16]
        self.gene_length = row[17]
        self.is_primary = True if row[18] == '1' else False
        self.is_secondary = True if row[19] == '1' else False
        self.is_internal = True if row[20] == '1' else False
        self.is_antisense = True if row[21] == '1' else False
        self.is_automated = True if row[22] == '1' else False
        self.is_manual = True if row[23] == '1' else False
        self.is_putative_srna = True if row[24] == '1' else False
        self.is_putative_asrna = True if row[25] == '1' else False
        self.comment = row[26]
        self.seq = row[27]
        self.is_orphan = False
        if self.is_primary is False and self.is_secondary is False and self.is_internal is False and self.is_antisense is False:
            self.is_orphan = True

    def __str__(self):
        return '%s %s %s' % (self.super_pos, self.super_strand, self.genome)