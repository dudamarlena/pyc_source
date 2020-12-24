# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zhemin/software/SPARSE_wrapper/SPARSE/modules/B1_query_metadata.py
# Compiled at: 2018-04-13 09:39:13
import sys, os, utils, pandas as pd, numpy as np

def query_metadata(params):
    params = utils.load_paramDict(params)
    fout = open(params['seqlist'], 'w') if params.get('seqlist', None) is not None else sys.stdout
    data = utils.load_database(**params)
    db_columns = params['db_columns'] + params['metadata_columns'] + params['taxa_columns']
    if params.get('default', None) is not None:
        tmp = {v['MapDB']:v for v in params['default_bowtie']}
        filter = tmp[params['default']]
    else:
        filter = {key:params[key] for key in db_columns + ['name', 'tag', 'min', 'max', 'group'] if params.get(key, None) is not None}
    for fld, value in filter.iteritems():
        if fld in db_columns:
            data = data[data[fld].isin(value.split(','))]
        elif fld == 'min':
            data = data[(data['size'].astype(int) >= int(value))]
        elif fld == 'max':
            data = data[(data['size'].astype(int) <= int(value))]
        elif fld == 'group':
            data = data[data['barcode'].str.contains(value)]
        elif fld == 'tag':
            data = data.reset_index(drop=True)
            barcodes = pd.DataFrame(data['barcode'].apply(lambda barcode: [ int(b[1:]) for b in barcode.split('.') ]).tolist(), columns=params['barcode_tag'])
            for f in value.split(';'):
                f = f.strip()
                g1, g2 = f[0], f[(-1)]
                if f.find('==') > 0:
                    barcodes = barcodes[(barcodes[g1] == barcodes[g2])]
                else:
                    barcodes = barcodes[(barcodes[g1] != barcodes[g2])]

            data = data.loc[barcodes.index].reset_index(drop=True)

    data.to_csv(fout, index=False, sep='\t')
    return


if __name__ == '__main__':
    query_metadata(dict([ [ k.strip() for k in arg.split('=', 1) ] for arg in sys.argv[1:] ]))