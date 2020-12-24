# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/short_reads_pipeline/quantification/quantificationClass.py
# Compiled at: 2019-06-06 15:03:43
from tools.deepargClass import dsize
import sys, os

def merge(inputFile, bin_location, deeparg_path):
    try:
        x = os.popen('sort -k1,1 -k2,2n ' + inputFile + '  | bedtools merge -c 12,5 -o sum,distinct >' + inputFile + '.merged').read()
        genes = {}
        for i in open(inputFile + '.merged'):
            subtype, start, end, count, Type = i.split()
            start = int(start)
            end = int(end)
            count = int(count)
            try:
                genes[subtype]['count'] += count
                genes[subtype]['length'] += abs(end - start)
                genes[subtype]['type'].append(Type)
                genes[subtype]['type'] = list(set(genes[subtype]['type']))
            except:
                genes[subtype] = {'count': count, 
                   'length': abs(end - start), 
                   'type': [
                          Type]}

        fo = open(inputFile + '.merged.quant', 'w')
        gene_len = dsize(deeparg_path)
        for gene in genes:
            cov = genes[gene]['length'] / float(gene_len[gene][1])
            fo.write(('\t').join([
             gene,
             ('/').join(genes[gene]['type']),
             str(genes[gene]['count']),
             str(genes[gene]['length']),
             gene_len[gene][1],
             str(round(cov, 3))]) + '\n')

        fo.close()
        return True
    except Exception as inst:
        print str(inst)
        return False