# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joe/devel/covviz/covviz/ped.py
# Compiled at: 2020-01-24 15:00:31
# Size of source mod 2**32: 3938 bytes
import csv
from collections import defaultdict
from .utils import gzopen

def check_ped_header(header, cols):
    """
    header (list) - current ped header columns
    cols (list) - typical columns we'll see from indexcov
    """
    header = set(header)
    cols = set(cols)
    is_indexcov = True
    if len(cols - header) > 0:
        is_indexcov = False
    return is_indexcov


def parse_ped(path, traces, sample_col, sex_chroms, sex_vals='1,2'):
    table_data = list()
    ped_data = dict(inferred=(defaultdict(list)),
      bins=(defaultdict(list)),
      pca=(defaultdict(list)))
    sex_chroms = [i.strip() for i in sex_chroms.split(',')]
    male = None
    female = None
    for i, v in enumerate(sex_vals.split(',')):
        if i == 0:
            male = v
        elif i == 1:
            female = v
        else:
            break

    required_vals = [
     sample_col,
     'bins.in',
     'bins.out',
     'bins.lo']
    float_vals = [
     'slope', 'p.out', 'PC1', 'PC2', 'PC3', 'PC4', 'PC5']
    int_vals = ['bins.out', 'bins.lo', 'bins.hi', 'bins.in']
    via_indexcov = False
    with gzopen(path) as (fh):
        header = fh.readline().strip().split('\t')
        datatable_cols = [dict(title=i, data=(i.replace('.', '\\.'))) for i in header]
        table_data.append(datatable_cols)
        fh.seek(0)
        reader = csv.DictReader(fh, delimiter='\t')
        via_indexcov = check_ped_header(header, required_vals)
        for row in reader:
            if via_indexcov:
                for k, v in row.items():
                    if k in int_vals:
                        row[k] = int(v)
                    else:
                        if k in float_vals:
                            row[k] = float(v)

            table_data.append(row)
            if via_indexcov:
                ped_data['inferred']['x'].append(row[('CN%s' % sex_chroms[0])])
                try:
                    ped_data['inferred']['y'].append(row[('CN%s' % sex_chroms[1])])
                except IndexError:
                    ped_data['inferred']['y'].append(0)

                if row['sex'] == male:
                    ped_data['inferred']['color'].append('rgba(144,237,125,0.5)')
                    ped_data['inferred']['hover'].append('Sample: %s<br>Inferred X CN: 1' % (row[sample_col],))
                else:
                    if row['sex'] == female:
                        ped_data['inferred']['color'].append('rgba(247,163,92,0.5)')
                        ped_data['inferred']['hover'].append('Sample: %s<br>Inferred X CN: 2' % (row[sample_col],))
                    else:
                        ped_data['inferred']['color'].append('rgba(105,105,105,0.5)')
                        ped_data['inferred']['hover'].append('Sample: %s<br>Unknown' % (row[sample_col],))
                total = row['bins.in'] + row['bins.out']
                ped_data['bins']['samples'].append(row[sample_col])
                ped_data['bins']['x'].append(row['bins.lo'] / total)
                ped_data['bins']['y'].append(row['bins.out'] / total)
                try:
                    ped_data['pca']['pca_1'].append(row['PC1'])
                    ped_data['pca']['pca_2'].append(row['PC2'])
                    ped_data['pca']['pca_3'].append(row['PC3'])
                except KeyError:
                    pass

    traces['ped'] = table_data
    traces['sample_column'] = sample_col
    if via_indexcov:
        traces['depth'] = ped_data
    return traces