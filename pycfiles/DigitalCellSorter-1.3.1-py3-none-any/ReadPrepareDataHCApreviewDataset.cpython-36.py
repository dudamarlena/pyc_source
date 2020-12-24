# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/home/domansk6/Projects/clean_run_03 06 2019/BM1/scripts/ReadPrepareDataHCApreviewDataset.py
# Compiled at: 2019-03-06 11:19:32
# Size of source mod 2**32: 4038 bytes
import copy, h5py, os, numpy as np

def PrepareData(filename, saveFolderName, patient, useAllData=True, cellsLimitToUse=1000, RecordExpressionData=True, RecordBarcodesFile=False, RecordGenesFile=True):
    f = h5py.File(filename, 'r')
    barcodes = f['GRCh38/barcodes']
    gene_names = f['GRCh38/gene_names']
    data_set = f['GRCh38/data']
    genes = f['GRCh38/genes']
    indices = f['GRCh38/indices']
    indptr = f['GRCh38/indptr']
    shape = f['GRCh38/shape']
    print('\nReading all patients index')
    patientIndex = [[] for x in range(8)]
    loc_barcodes = copy.deepcopy(barcodes[0:barcodes.shape[0]])
    for i in range(barcodes.shape[0]):
        patientIndex[(int(str(loc_barcodes[i])[10]) - 1)].append(i)

    indicatorGeneNamesConverted = False
    dataName = 'HCA_BM%s_data' % patient
    saveFolderName = 'data'
    path = '/'.join([saveFolderName, dataName])
    if not os.path.exists(path):
        os.makedirs(path)
    if RecordGenesFile:
        if not indicatorGeneNamesConverted:
            print('\nDecoding genes names UTF-8')
            gene_names = list(map(lambda s: s.decode('UTF-8'), gene_names))
            indicatorGeneNamesConverted = True
        print('\nRecording genes.tsv' + '. Patient %s' % patient)
        with open('/'.join([path, 'genes.tsv']), 'w') as (fileGenes):
            for i in range(genes.shape[0]):
                fileGenes.write(str(genes[i])[2:17] + '\t' + str(gene_names[i]) + '\n')

    if RecordBarcodesFile:
        print('\nRecording barcodes.tsv' + '. Patient %s' % patient)
        with open('/'.join([path, 'barcodes.tsv']), 'w') as (fileBarcodes):
            for i in range(barcodes.shape[0]):
                fileBarcodes.write(str(barcodes[i]) + '\n')

    if RecordExpressionData:
        maxCellsPerPatient = 1 + patientIndex[(patient - 1)][(-1)] - patientIndex[(patient - 1)][0]
        print('Patient %s, total number of sequenced cells: %s' % (patient, maxCellsPerPatient))
        if useAllData:
            readOnlyNumberOfCells = -1
        else:
            readOnlyNumberOfCells = cellsLimitToUse
            print('\nLimiting data to %s cells' % readOnlyNumberOfCells)
        lines_count = 0
        with open('/'.join([path, 'matrix.mtx']), 'w') as (file_temp):
            print('\nCounting lines for matrix.mtx')
            file_temp.write('%%MatrixMarket matrix coordinate real general\n%\n')
            for i in range(patientIndex[(patient - 1)][0], patientIndex[(patient - 1)][readOnlyNumberOfCells]):
                for j in range(indptr[i], indptr[(i + 1)]):
                    lines_count += 1

            file_temp.write(str(shape[0]) + ' ' + str(patientIndex[(patient - 1)][readOnlyNumberOfCells] - patientIndex[(patient - 1)][0]) + ' ' + str(lines_count) + '\n')
            print('\nRecording matrix.mtx' + '. Patient %s' % patient)
            for i in range(patientIndex[(patient - 1)][0], patientIndex[(patient - 1)][readOnlyNumberOfCells]):
                s_index = indptr[i]
                f_index = indptr[(i + 1)]
                loc_data_set = copy.deepcopy(data_set[s_index:f_index])
                loc_indices = copy.deepcopy(indices[s_index:f_index])
                for j in range(f_index - s_index):
                    file_temp.write(str(loc_indices[j] + 1) + ' ' + str(1 + (i - patientIndex[(patient - 1)][0]) % maxCellsPerPatient) + ' ' + str(loc_data_set[j]) + '\n')

            print('\n')