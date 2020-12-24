# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\A_MSU_Digital_Cell_Sorter\VS\DigitalCellSorter-master\scripts\generalForGeneLists.py
# Compiled at: 2018-10-17 19:38:57
# Size of source mod 2**32: 5221 bytes
import numpy as np, pandas as pd, shutil, os

def parse_Human_cell_markers():
    import copy
    indir = 'temp_for_gene_lists/'
    outdir = 'geneLists/'
    f2 = 'Human_cell_markers_.xlsx'
    typeBM = 'Bone marrow'
    typePBMC = 'Peripheral blood'
    tissueType = typePBMC
    df = pd.read_excel((indir + f2), sheet='Human_cell_markers')
    df = df[(df['tissueType2'] == tissueType)].drop(columns=['speciesType', 'tissueType2', 'cancerType', 'cellType', 'geneID', 'proteinName', 'proteinID', 'markerResource', 'PMID', 'Company'])
    cellType = 'cellName3'
    cellMarker = 'cellMarker'
    geneSymbol = 'geneSymbol'
    CellTypes = np.sort(np.unique(df[cellType]))
    numCellTypes = len(CellTypes)
    allEncounteredMarkers = []
    for i in range(len(df[cellMarker])):
        allEncounteredMarkers += map(str.strip, df[cellMarker].values[i].split(','))

    CellMarkers = np.sort(np.unique(allEncounteredMarkers))
    numCellMarkers = len(CellMarkers)
    _df = pd.DataFrame((np.zeros((numCellMarkers, numCellTypes))), index=CellMarkers, columns=CellTypes)
    for j in range(numCellTypes):
        match, _list = df[(df[cellType] == CellTypes[j])].values.T[1:][0], []
        for k in range(match.shape[0]):
            _list += map(str.strip, match[k].split(','))

        for i in range(numCellMarkers):
            _df.values[i][j] = 1 if _df.index[i] in _list else 0

    _df.index.name = 'Marker'
    _df.to_excel(outdir + 'Human_cell_markers_PBMC.xlsx')


parse_Human_cell_markers()
dir = 'temp_for_gene_lists/'
f1 = 'main_CellTypes_CD_from_bioLegend.csv'
f2 = '04-0027-02hu_mo_web.csv'
f3 = 'Guide-to-human-CD-antigens_CSV.xlsx'

def parse_short_from_BioLegend():
    with open(dir + f1, 'r') as (_temp_file):
        lines = _temp_file.readlines()
        MC = np.vstack([np.array(i.strip('\n').split(','))[:38] for i in lines]).T
        index = MC[0]
        MC = MC[1:].T
        CellTypes = index
        numCellTypes = len(CellTypes)
        for i in range(MC.shape[0]):
            for j in range(MC.shape[1]):
                res = MC[i][j].find(' (')
                if res > -1:
                    MC[i][j] = MC[i][j][:res]

        MC = pd.DataFrame(MC, index=index)
        _list = np.sort(np.unique(MC.values))
        if _list[0] == '':
            _list = np.delete(_list, 0)
        numMarkers = len(_list)
        MarkerCelltype = pd.DataFrame((np.zeros((numMarkers, numCellTypes))), index=_list)
        MarkerCelltype.columns = CellTypes
        for i in range(numCellTypes):
            for j in range(MC.shape[1]):
                marker = MC.loc[CellTypes[i]][j]
                if marker in MarkerCelltype.index:
                    MarkerCelltype.loc[marker][i] = 1

        MarkerCelltype.index.name = 'Marker'
    MarkerCelltype.to_excel('geneLists/' + f1[:-4] + '.xlsx')


def parse_poster_from_BioLegend():
    with open(dir + f2, 'r') as (_temp_file):
        lines = _temp_file.readlines()
        dummy = []
        for _ in range(50):
            dummy.append('')

        MC = np.vstack([np.array(i.strip('\n').split(',') + dummy)[:30] for i in lines[1:]])
        indexCD = MC.T[0]
        MC = MC.T[1:].T
        for i in range(MC.shape[0]):
            for j in range(MC.shape[1]):
                MC[i][j] = MC[i][j].strip('"').strip(' ').strip(' ').strip(' ')

        with open(dir + 'CellTypesListINPUT.txt') as (_t):
            lines = _t.readlines()
        CellTypes = np.sort(np.unique([i.strip('\n').strip(' ') for i in lines]))

        def get_CellType(CellTypes, _s):
            _s_copy = _s
            numCellTypes = len(CellTypes)
            result = ''
            for i in range(numCellTypes):
                if CellTypes[i] in _s_copy:
                    if not result == '':
                        print('Cell type overridden: _s is %s, %s, new %s. Ignoring this entry\n' % (_s_copy, result, CellTypes[i]))
                        _s_copy = ''
                        result = ''
                    else:
                        result = CellTypes[i]

            return result

        for i in range(MC.shape[0]):
            for j in range(MC.shape[1]):
                MC[i][j] = get_CellType(CellTypes, MC[i][j])

        numCellTypes = len(CellTypes)
        numMarkers = len(indexCD)
        MarkerCelltype = pd.DataFrame((np.zeros((numMarkers, numCellTypes))), index=indexCD)
        MarkerCelltype.columns = CellTypes
        for i in range(numMarkers):
            for j in range(numCellTypes):
                marker = MarkerCelltype.index[i]
                if CellTypes[j] in MC[i]:
                    MarkerCelltype.values[i][j] = 1

        MarkerCelltype.index.name = 'Marker'
    MarkerCelltype.to_excel('geneLists/' + f2[:-4] + '.xlsx')