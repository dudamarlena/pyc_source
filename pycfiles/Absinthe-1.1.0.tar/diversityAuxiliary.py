# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/IgRepAuxiliary/diversityAuxiliary.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = '\n    Short description: Quality Control Analysis of Immunoglobulin Repertoire NGS (Paired-End MiSeq)    \n    Author: Monther Alhamdoosh    \n    Python Version: 2.7\n    Changes log: check git commits. \n'
from collections import Counter, defaultdict
_REGIONS = [
 'fr1', 'cdr1', 'fr2', 'cdr2', 'fr3', 'cdr3', 'fr4']

def annotateSpectratypes(cloneAnnot, amino=True):
    denom = 3 if amino else 1
    spectraTypes = {}
    for region in _REGIONS:
        spectraType = ((cloneAnnot[(region + '.end')] - cloneAnnot[(region + '.start')] + 1) / denom).astype(int)
        spectraTypes[region] = Counter(spectraType)

    spectraType = ((cloneAnnot['fr4.end'] - cloneAnnot['fr1.start'] + 1) / denom).astype(int)
    spectraTypes['v'] = Counter(spectraType)
    return spectraTypes


def annotateClonotypes(cloneSeqs, segregate=False, removeNone=True):
    if segregate:
        clonoTypes = defaultdict(lambda : defaultdict(lambda : defaultdict(int)))
        for row in cloneSeqs.itertuples():
            geneName = row.germline.split('*')[0]
            variableAA = ''
            badAA = False
            for region in _REGIONS:
                regionAA = getattr(row, region)
                variableAA += regionAA
                if regionAA == 'None' or regionAA == '':
                    badAA = True
                if not (removeNone and (regionAA == 'None' or regionAA == '')):
                    clonoTypes[geneName][region][regionAA] += 1

            if not (badAA and removeNone):
                clonoTypes[geneName]['v'][variableAA] += 1

    else:
        clonoTypes = {}
        for region in _REGIONS:
            seqs = cloneSeqs[region].tolist()
            clonoTypes[region] = Counter(seqs)
            if removeNone:
                clonoTypes[region].pop('None', None)
                clonoTypes[region].pop('', None)

    def _join(frcdr):
        if removeNone and ('None' in frcdr or '' in frcdr):
            return 'None'
        return ('').join(frcdr)

    seqs = map(_join, zip(cloneSeqs['fr1'].tolist(), cloneSeqs['cdr1'].tolist(), cloneSeqs['fr2'].tolist(), cloneSeqs['cdr2'].tolist(), cloneSeqs['fr3'].tolist(), cloneSeqs['cdr3'].tolist(), cloneSeqs['fr4'].tolist()))
    clonoTypes['v'] = Counter(seqs)
    if removeNone:
        clonoTypes['v'].pop('None', None)
        clonoTypes['v'].pop('', None)
    return clonoTypes