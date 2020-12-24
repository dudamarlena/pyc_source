# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: CGEA/lib/featureListProcessing.py
# Compiled at: 2016-08-16 13:10:43
import re, os
from file import read_csv
from copy import deepcopy
base_path = os.path.abspath(os.path.dirname(__file__))

def parseSymbol2Entrez(filepath):
    data = read_csv(filepath)
    localdict = {}
    for row in data[1:]:
        row = row[0].split(' ')
        if row[1].startswith('"') and row[1].endswith('"'):
            row[1] = row[1][1:-1]
        localdict[row[1]] = row[0]

    return localdict


entrezLookup = parseSymbol2Entrez(base_path + '/../data/symbol2entrez.txt')

def formatFeatureFile(filepath):
    locallist = []
    f = open(filepath, 'r')
    for row in f:
        row = re.findall('[\\w]+', row) + re.findall("[\\w']+", row)
        for item in row:
            if item in entrezLookup:
                locallist.append(entrezLookup[item])
            elif item in entrezLookup.values():
                locallist.append(item)
            else:
                print item

    f.close()
    return list(set(locallist))


def formatFeatureList(featureList):
    localList = []
    for row in featureList:
        if isinstance(row, basestring):
            row = re.findall("[\\w']+", row)
            for item in row:
                if item in entrezLookup:
                    localList.append(entrezLookup[item])
                elif item in entrezLookup.values():
                    localList.append(item)
                else:
                    print item

        elif isinstance(row, int):
            if row in entrezLookup.values():
                localList.append(row)
            else:
                print row

    return localList


def formatFeatureString(featureString):
    featureList = []
    for item in re.findall("[\\w']+", featureString):
        if item in entrezLookup:
            featureList.append(entrezLookup[item])
        elif item in entrezLookup.values():
            featureList.append(item)
        else:
            print item

    return featureList


def formatGeneLists(geneLists):
    for index, genelist in enumerate(geneLists):
        if genelist:
            if isinstance(genelist, basestring):
                if os.path.isfile(genelist):
                    geneLists[index] = formatFeatureFile(genelist)
                else:
                    geneLists[index] = formatFeatureString(genelist)
            elif isinstance(genelist, list):
                geneLists[index] = formatFeatureList(genelist)
            else:
                print genelist

    geneLists = filter(lambda x: x, map(lambda x: map(int, x) if x else None, geneLists))
    return geneLists