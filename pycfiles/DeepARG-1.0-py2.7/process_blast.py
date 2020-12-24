# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/predict/bin/process_blast.py
# Compiled at: 2018-12-06 14:23:01
import json
from tqdm import tqdm

def make_alignments_json(fname, iden=50, eval=1e-05, coverage=0.8, BitScore=True, Features={}, glen={}, pipeline='reads'):
    alignments = {}
    BHit = {}
    SF = {i:True for i in Features}
    print 'traversing input file ...'
    if BitScore == True:
        measure = 11
    else:
        measure = 2
    for i in tqdm(open(fname), unit='reads'):
        i = i.strip().split('\t')
        l1 = [float(i[7]) - float(i[6])]
        l2 = [float(i[9]) - float(i[8])]
        if float(i[2]) < iden:
            continue
        if float(i[10]) > eval:
            continue
        if pipeline == 'genes':
            if float(int(i[3])) / glen[i[1]] < coverage:
                continue
        if pipeline == 'reads':
            if float(int(i[3])) <= coverage:
                continue
        try:
            if SF[i[1]]:
                alignments[i[0]].update({i[1]: float(i[measure])})
        except:
            try:
                if SF[i[1]]:
                    alignments[i[0]] = {i[1]: float(i[measure])}
            except:
                pass

        try:
            if SF[i[1]]:
                try:
                    if BHit[i[0]][1] < float(i[measure]):
                        BHit[i[0]] = [
                         i[1], float(i[measure]), i]
                except Exception as e:
                    BHit[i[0]] = [
                     i[1], float(i[measure]), i]

        except:
            pass

    print (
     len(alignments), ' reads passed the filters and ready for prediction')
    return [alignments, BHit]