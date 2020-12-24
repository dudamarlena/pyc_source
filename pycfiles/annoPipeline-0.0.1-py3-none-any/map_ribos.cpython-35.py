# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/map_ribos.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 1602 bytes
import os, csv, shutil

def mapping_ribos(table_folder, id_file, feature):
    ids = []
    ih = open(id_file, 'r')
    for row in csv.reader(ih, delimiter='\t'):
        if not row[0].startswith('#'):
            ids.append({'id': row[0].strip(), 
             'name': row[1].strip(), 
             'info': row[2].strip()})

    for table_file in os.listdir(table_folder):
        if table_file.endswith('_' + feature + '.csv'):
            tmp_table = os.path.join(table_folder, 'tmp' + table_file)
            table_file = os.path.join(table_folder, table_file)
            out = open(tmp_table, 'w')
            tables = []
            fh = open(table_file, 'r')
            out.write('#ID\tGenome\tStrand\tAssociated_CDS\tStart_genome\tEnd_genome\tRfam\tE_value\tStart_align\tEnd_align\n')
            for row in csv.reader(fh, delimiter='\t'):
                if not row[0].startswith('#'):
                    tables.append({'input': row[0:6], 'Rfam': row[6], 
                     'e': row[7], 'start': row[8], 
                     'end': row[9]})

            for table in tables:
                for id_ in ids:
                    if table['Rfam'] == id_['id']:
                        name = id_['name']

                out.write('\t'.join(table['input'] + [table['Rfam'], name,
                 table['e'], table['start'],
                 table['end']]) + '\n')

            out.close()
            os.remove(table_file)
            shutil.move(tmp_table, table_file)