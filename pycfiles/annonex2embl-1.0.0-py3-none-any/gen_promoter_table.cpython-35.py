# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/gen_promoter_table.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 2280 bytes
from annogesiclib.gff3 import Gff3Parser

def gen_promoter_table(input_file, output_file, tss_file, type_):
    """generate the table of promoter based on MEME"""
    tsss = []
    gff_f = open(tss_file, 'r')
    for entry in Gff3Parser().entries(gff_f):
        tsss.append(entry)

    out = open(output_file, 'w')
    out.write('\t'.join(['Genome', 'TSS_position',
     'TSS_strand', 'Motif']) + '\n')
    detect = False
    num = 1
    with open(input_file) as (fh):
        for line in fh:
            line = line.strip()
            if type_ == 'meme':
                if line.startswith('MOTIF'):
                    motif = line.split('MEME')[0].strip()
                    datas = motif.split(' ')
                    motif = datas[0] + '_' + datas[(-1)]
                    detect = False
                else:
                    if line.startswith('Sequence name') and line.endswith('Site'):
                        detect = True
                    else:
                        if len(line) == 0:
                            detect = False
                        elif detect and not line.startswith('---'):
                            tag = line.split(' ')[0]
                            datas = tag.split('_')
                            for tss in tsss:
                                if '_'.join(datas[2:]) in tss.seq_id and datas[0] == str(tss.start) and datas[1] == tss.strand:
                                    out.write('\t'.join([tss.seq_id, datas[0],
                                     datas[1], motif]) + '\n')

            elif type_ == 'glam2':
                if line.startswith('*'):
                    detect = True
                    motif = 'MOTIF_' + str(num)
                    num += 1
                else:
                    if len(line) == 0:
                        detect = False
                    elif detect:
                        datas = line.split(' ')[0].split('_')
                        for tss in tsss:
                            if '_'.join(datas[2:]) in tss.seq_id and datas[0] == str(tss.start) and datas[1] == tss.strand:
                                out.write('\t'.join([tss.seq_id, datas[0],
                                 datas[1], motif]) + '\n')