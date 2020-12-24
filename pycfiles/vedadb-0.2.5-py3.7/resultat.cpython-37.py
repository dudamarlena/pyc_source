# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vedadb/resultat.py
# Compiled at: 2019-09-06 13:51:34
# Size of source mod 2**32: 2848 bytes
__all__ = [
 'resultat']
import sys, os, re, pandas as pd
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import vedadb.connexion as connexion
import vedadb.fileToDataframe as file
import vedadb.entete as entete

def readVdeToSetTable(myfile):
    d = {}
    Attribute = []
    Commodity = []
    Process = []
    Period = []
    Region = []
    Vintage = []
    TimeSlice = []
    UserConstraint = []
    PV = []
    with open(myfile) as (f):
        result = {}
        for line in f:
            if not re.findall('^\\*', line) != []:
                if line == '':
                    continue
                try:
                    line = line.split(',')
                    Attribute.append(line[0].split('"')[1].strip())
                    Commodity.append(line[1].split('"')[1].strip())
                    Process.append(line[2].split('"')[1].strip())
                    Period.append(line[3].split('"')[1].strip())
                    Region.append(line[4].split('"')[1].strip())
                    Vintage.append(line[5].split('"')[1].strip())
                    TimeSlice.append(line[6].split('"')[1].strip())
                    UserConstraint.append(line[7].split('"')[1].strip())
                    PV.append(line[8].split('\n')[0])
                except IndexError:
                    pass

        df = pd.DataFrame({'attribut':Attribute,  'commodity':Commodity, 
         'process':Process,  'periode':Period,  'region':Region,  'vintage':Vintage,  'timeSlice':TimeSlice, 
         'userconstraint':UserConstraint,  'pv':PV})
    return df


def writeResultInDb(db, line, importid=1):
    for index, row in line.iterrows():
        db.insert('resultat', attribut=(row.to_dict()['attribut']), commodity=(row.to_dict()['commodity']),
          process=(row.to_dict()['process']),
          periode=(row.to_dict()['periode']),
          region=(row.to_dict()['region']),
          vintage=(row.to_dict()['vintage']),
          timeSlice=(row.to_dict()['timeSlice']),
          userconstraint=(row.to_dict()['userconstraint']),
          pv=(row.to_dict()['pv']),
          importid=importid)


def execution(parameters_path, myvdfile):
    db = connexion.connect(parameters_path)
    df = readVdeToSetTable(myvdfile)
    importId = entete.readImportIdFromDb(db)
    writeResultInDb(db, df, importId)


def executionInExitingDb(parameters_path, myvdfile, importId):
    db = connexion.connect(parameters_path)
    df = readVdeToSetTable(myvdfile)
    writeResultInDb(db, df, importId)


if __name__ == '__main__':
    parameters_path = sys.argv[1]
    myvdfile = sys.argv[2]
    db = connexion.connect(parameters_path)
    df = readVdeToSetTable(myvdfile)
    importId = entete.readImportIdFromDb(db)
    writeResultInDb(db, df, importId)