# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/ensembl/process_hsa37_gtf.py
# Compiled at: 2019-11-14 14:47:06
# Size of source mod 2**32: 1036 bytes
import sys, gzip
input_file = 'Homo_sapiens.GRCh37.87.gtf.gz'
out_fh = gzip.open('hgnc_to_ens_gids.txt.gz', 'w')
hgnc_to_ens_ids = dict()
cnt = 0
with gzip.open(input_file) as (fh):
    for line in fh:
        line = line.decode('utf-8').rstrip()
        if line.startswith('#'):
            pass
        else:
            vals = line.split('\t')
            annot = vals[8]
            dd = dict(s.strip().replace('"', '').split(' ') for s in annot.split(';') if s != '')
            gene_id = dd['gene_id']
            gene_name = dd['gene_name']
            if gene_name in hgnc_to_ens_ids:
                hgnc_to_ens_ids[gene_name].append(gene_id)
                hgnc_to_ens_ids[gene_name] = list(set(hgnc_to_ens_ids[gene_name]))
            else:
                hgnc_to_ens_ids[gene_name] = [
                 gene_id]

print(len(hgnc_to_ens_ids))
for k, v in hgnc_to_ens_ids.items():
    out_fh.write(str.encode(k + '\t' + ''.join(v) + '\n'))

out_fh.close()