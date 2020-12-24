# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vedadb/dimensionContent.py
# Compiled at: 2019-09-06 13:50:10
# Size of source mod 2**32: 6152 bytes
__all__ = [
 'dimensioncontent']
import sys, os, re, pandas as pd
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import vedadb.connexion as connexion
import vedadb.entete as entete
import vedadb.fileToDataframe as file
import vedadb.sets as set

def attributToSave(vdedf):
    attribut = vdedf[(vdedf['dimension'] == 'Attribute')]
    return attribut


def otherDimensionContentValue(vdsdf, vdedf):
    result = {}
    resultvds = vdsdf.drop_duplicates(subset='dimensionCode', keep='last')
    vdedf = vdedf.drop_duplicates(subset='codset', keep='last')
    resultvds = resultvds[(resultvds['dimension'] != 'Attribute')]
    for index, row in resultvds.iterrows():
        search = row.to_dict()['dimensionCode']
        for index, row in vdedf.iterrows():
            if search == row.to_dict()['codset']:
                result.update({search: row.to_dict()['description']})

    return result


def updateVdsDataframe(vdsdf, resultOfVdsVde):
    dimension = []
    region = []
    codset = []
    dimensionCode = []
    description = []
    for index, row in vdsdf.iterrows():
        for key, value in resultOfVdsVde.items():
            if row.to_dict()['dimensionCode'] == key:
                dimension.append(row.to_dict()['dimension'])
                region.append(row.to_dict()['region'])
                codset.append(row.to_dict()['codset'])
                dimensionCode.append(row.to_dict()['dimensionCode'])
                description.append(value)

    df = pd.DataFrame({'dimension':dimension,  'region':region, 
     'codset':codset,  'dimensionCode':dimensionCode,  'description':description})
    return df


def dimensionContentToSave(result, idtable):
    dimension = []
    region = []
    codset = []
    dimensionCode = []
    description = []
    setid = []
    for index, row in result.iterrows():
        p = 0
        for key, value in idtable.items():
            if row.to_dict()['codset'] == key:
                p = 1
                dimension.append(row.to_dict()['dimension'])
                region.append(row.to_dict()['region'])
                codset.append(row.to_dict()['codset'])
                dimensionCode.append(row.to_dict()['dimensionCode'])
                description.append(row.to_dict()['description'])
                setid.append(value)

        if p == 0:
            value = ''
            dimension.append(row.to_dict()['dimension'])
            region.append(row.to_dict()['region'])
            codset.append(row.to_dict()['codset'])
            dimensionCode.append(row.to_dict()['dimensionCode'])
            description.append(row.to_dict()['description'])
            setid.append(value)

    df = pd.DataFrame({'dimension':dimension,  'region':region, 
     'codset':codset,  'setid':setid,  'dimensionCode':dimensionCode,  'description':description})
    return df


def writeDimensionContentInDb(db, line, importid=1):
    for index, row in line.iterrows():
        db.insert('dimensioncontent', dimensioncode=(row.to_dict()['dimensionCode']), region=(row.to_dict()['region']), codeset=(row.to_dict()['codset']),
          typedimension=(row.to_dict()['dimension']),
          descriptiondimensioncode=(row.to_dict()['description']),
          idset=(row.to_dict()['setid']),
          importid=importid)


def writeAttributDimensionContentInDb(db, line, importid=1):
    for index, row in line.iterrows():
        db.insert('dimensioncontent', region=(row.to_dict()['region']), codeset=(row.to_dict()['codset']),
          typedimension=(row.to_dict()['dimension']),
          descriptiondimensioncode=(row.to_dict()['description']),
          importid=importid)


def execution(parameters_path, myfile, mysfile):
    db = connexion.connect(parameters_path)
    vdedf = file.vdeToDataframe(myfile)
    vdsdf = file.vdsToDataframe(mysfile)
    result = otherDimensionContentValue(vdsdf, vdedf)
    d = updateVdsDataframe(vdsdf, result)
    importId = entete.readImportIdFromDb(db)
    idtable = set.readSetIdFromDb(db, importId)
    d = dimensionContentToSave(d, idtable)
    writeDimensionContentInDb(db, d, importId)
    writeAttributDimensionContentInDb(db, attributToSave(vdedf), importId)


def executionInExitingDb(parameters_path, myfile, mysfile, importId):
    db = connexion.connect(parameters_path)
    vdedf = file.vdeToDataframe(myfile)
    vdsdf = file.vdsToDataframe(mysfile)
    result = otherDimensionContentValue(vdsdf, vdedf)
    d = updateVdsDataframe(vdsdf, result)
    idtable = set.readSetIdFromDb(db, importId)
    d = dimensionContentToSave(d, idtable)
    writeDimensionContentInDb(db, d, importId)
    writeAttributDimensionContentInDb(db, attributToSave(vdedf), importId)


if __name__ == '__main__':
    parameters_path = sys.argv[1]
    myfile = sys.argv[2]
    mysfile = sys.argv[3]
    db = connexion.connect(parameters_path)
    vdedf = file.vdeToDataframe(myfile)
    vdsdf = file.vdsToDataframe(mysfile)
    result = otherDimensionContentValue(vdsdf, vdedf)
    d = updateVdsDataframe(vdsdf, result)
    importId = entete.readImportIdFromDb(db)
    idtable = set.readSetIdFromDb(db, importId)
    d = dimensionContentToSave(d, idtable)
    writeDimensionContentInDb(db, d, importId)
    writeAttributDimensionContentInDb(db, attributToSave(vdedf), importId)