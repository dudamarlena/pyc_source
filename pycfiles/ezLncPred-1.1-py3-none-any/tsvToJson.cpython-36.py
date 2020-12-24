# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/Ezlncpred_LS_test/Ezlncpred/tsvToJson.py
# Compiled at: 2019-11-24 10:24:03
# Size of source mod 2**32: 7941 bytes
import pandas as pd, json

def tsvToJson(resultFile):
    values = []
    model = resultFile.split('/')[1].split('_')[0]
    tsvfile = '%s_outfile' % resultFile
    if model == 'CPAT':
        col = 'coding_prob'
        data = pd.read_csv(tsvfile, sep='\t')
        nr = data.shape[0]
        sequenceId = data.index.tolist()
        jsonContent = []
        for i in range(0, nr):
            sequenceDict = {'Sequence Id':'',  'Coding Potential':'',  'Coding Label':''}
            if data[col][i] > 0.5:
                sequenceDict['Coding Label'] = 'coding'
            else:
                sequenceDict['Coding Label'] = 'noncoding'
            sequenceDict['Sequence Id'] = sequenceId[i][2:-1]
            sequenceDict['Coding Potential'] = data[col][i]
            jsonContent.append(json.dumps(sequenceDict))

        jsonContent = ','.join(jsonContent)
    else:
        if model == 'CNCI':
            tsvfile = 'results/CNCI.index'
            data = pd.read_csv(tsvfile, sep='\t')
            nr = data.shape[0]
            codingPotential = data['score'].tolist()
            cnciClass = data['index'].tolist()
            sequenceId = [data['Transcript ID'][i].split(' ')[0] for i in range(0, nr)]
            jsonContent = []
            for i in range(0, nr):
                sequenceDict = {'Sequence Id':'', 
                 'Coding score':'',  'Coding Label':''}
                sequenceDict['Coding Label'] = cnciClass[i]
                sequenceDict['Sequence Id'] = sequenceId[i]
                sequenceDict['Coding score'] = codingPotential[i]
                jsonContent.append(json.dumps(sequenceDict))

            jsonContent = ','.join(jsonContent)
        else:
            if model == 'CPC2':
                tsvfile = 'results/CPC2_outfile'
                data = pd.read_csv(tsvfile, sep='\t')
                nr = data.shape[0]
                cpc2Class = data['label'].tolist()
                sequenceId = data['#ID'].tolist()
                codingPotential = data['coding_probability'].tolist()
                jsonContent = []
                for i in range(0, nr):
                    sequenceDict = {'Sequence Id':'', 
                     'Coding Potential':'',  'Coding Label':''}
                    sequenceDict['Coding Label'] = cpc2Class[i]
                    sequenceDict['Sequence Id'] = sequenceId[i]
                    sequenceDict['Coding Potential'] = codingPotential[i]
                    jsonContent.append(json.dumps(sequenceDict))

                jsonContent = ','.join(jsonContent)
            else:
                if model == 'lgc':
                    tsvfile = 'results/lgc_outfile'
                    data = pd.read_csv(tsvfile, sep='\t')
                    nr = data.shape[0]
                    sequenceId = data['# Sequence Name'].tolist()
                    codingPotential = data['Conding Potential Score'].tolist()
                    lgc_class = data['Coding Label'].tolist()
                    jsonContent = []
                    for i in range(0, nr):
                        sequenceDict = {'Sequence Id':'', 
                         'Coding Potential Score':'',  'Coding Label':''}
                        sequenceDict['Coding Label'] = lgc_class[i]
                        sequenceDict['Sequence Id'] = sequenceId[i]
                        sequenceDict['Coding Potential Score'] = codingPotential[i]
                        jsonContent.append(json.dumps(sequenceDict))

                    jsonContent = ','.join(jsonContent)
                else:
                    if model == 'PLEK':
                        tsvfile = 'results/PLEK_outfile'
                        data = pd.read_csv(tsvfile, sep='\t', header=None)
                        nr = data.shape[0]
                        plekClass = data[0].tolist()
                        sequenceId = [data[2][i].split(' ')[0][1:] for i in range(0, nr)]
                        codingPotential = data[1].tolist()
                        jsonContent = []
                        for i in range(0, nr):
                            sequenceDict = {'Sequence Id':'', 
                             'Coding score':'',  'Coding Label':''}
                            sequenceDict['Coding Label'] = plekClass[i]
                            sequenceDict['Sequence Id'] = sequenceId[i]
                            sequenceDict['Coding score'] = codingPotential[i]
                            jsonContent.append(json.dumps(sequenceDict))

                        jsonContent = ','.join(jsonContent)
                    else:
                        if model == 'longdist':
                            tsvfile = 'results/longdist_outfile'
                            data = pd.read_csv(tsvfile, sep=',')
                            nr = data.shape[0]
                            longdistClass = ['noncoding' if data['lncRNA %'][i] >= 0.5 else 'coding RNA' for i in range(0, nr)]
                            sequenceId = data['sequence'].tolist()
                            codingPotential = data['pct %'].tolist()
                            jsonContent = []
                            for i in range(0, nr):
                                sequenceDict = {'Sequence Id':'', 
                                 'Coding Potential':'',  'Coding Label':''}
                                sequenceDict['Coding Label'] = longdistClass[i]
                                sequenceDict['Sequence Id'] = sequenceId[i]
                                sequenceDict['Coding Potential'] = codingPotential[i]
                                jsonContent.append(json.dumps(sequenceDict))

                            jsonContent = ','.join(jsonContent)
                        else:
                            if model == 'GFStack':
                                tsvfile = 'results/GFStack_outfile'
                                data = pd.read_csv(tsvfile, sep='\t')
                                nr = data.shape[0]
                                GFStackClass = data['Class'].tolist()
                                sequenceId = data['Sequence'].tolist()
                                lncrnaProb = data['LncRNA Probability'].tolist()
                                jsonContent = []
                                for i in range(0, nr):
                                    sequenceDict = {'Sequence Id':'', 
                                     'LncRNA Probability':'',  'Coding Label':''}
                                    sequenceDict['Coding Label'] = GFStackClass[i]
                                    sequenceDict['Sequence Id'] = sequenceId[i]
                                    sequenceDict['LncRNA Probability'] = lncrnaProb[i]
                                    jsonContent.append(json.dumps(sequenceDict))

                                jsonContent = ','.join(jsonContent)
                            else:
                                if model == 'CPPred':
                                    tsvfile = 'results/CPPred_outfile'
                                    data = pd.read_csv(tsvfile, sep='\t')
                                    nr = data.shape[0]
                                    cppredClass = ['noncoding' if data['T'][i] <= 0.5 else 'coding RNA' for i in range(0, nr)]
                                    codingPotential = data['T'].tolist()
                                    sequenceId = data['#ID'].tolist()
                                    jsonContent = []
                                    for i in range(0, nr):
                                        sequenceDict = {'Sequence Id':'', 
                                         'Coding Potential':'',  'Coding Label':''}
                                        sequenceDict['Coding Label'] = cppredClass[i]
                                        sequenceDict['Sequence Id'] = sequenceId[i]
                                        sequenceDict['Coding Potential'] = codingPotential[i]
                                        jsonContent.append(json.dumps(sequenceDict))

                                    jsonContent = ','.join(jsonContent)
                                else:
                                    if model == 'LncADeep':
                                        tsvfile = tsvfile + '/LncADeep.results'
                                        data = pd.read_csv(tsvfile, sep='\t', header=None)
                                        nr = data.shape[0]
                                        lncadeepClass = data[2].tolist()
                                        sequenceId = data[0].tolist()
                                        score = data[1].tolist()
                                        jsonContent = []
                                        for i in range(0, nr):
                                            sequenceDict = {'Sequence Id':'', 
                                             'Coding score':'',  'Coding Label':''}
                                            sequenceDict['Coding Label'] = lncadeepClass[i]
                                            sequenceDict['Sequence Id'] = sequenceId[i]
                                            sequenceDict['Coding score'] = score[i]
                                            jsonContent.append(json.dumps(sequenceDict))

                                        jsonContent = ','.join(jsonContent)
    with open('./results/result.json', 'w') as (f):
        f.write('[')
        f.write(jsonContent)
        f.write(']')