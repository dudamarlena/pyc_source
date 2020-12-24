# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vedadb/sets.py
# Compiled at: 2019-09-11 18:13:29
# Size of source mod 2**32: 1992 bytes
__all__ = [
 'set']
import sys, os, re, pandas as pd
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import vedadb.connexion as connexion
import vedadb.entete as entete

def readVdeToSetTable(myfile):
    d = []
    with open(myfile) as (f):
        for line in f:
            if re.findall('[A-Z,a-z]+SET', line) != []:
                d.append(line)

        return d


def setToDb(db, line=[], importID=''):
    for element in line:
        element = element.split(',')
        db.insert('set', typedimensionset=(element[0].split('"')[1]), region=(element[1].split('"')[1]),
          codeset=(element[2].split('"')[1]),
          description=(element[3].split('"')[1]),
          importid=importID)


def readSetIdFromDb(db, importID=0):
    result = {}
    for r in db.query('SELECT * FROM set WHERE importid=importID').dictresult():
        result.update({r['codeset']: r['idset']})

    return result


def executionInExitingDb(parameters_path, myvdefile, importId):
    db = connexion.connect(parameters_path)
    db = connexion.connect(parameters_path)
    line = readVdeToSetTable(myvdefile)
    setToDb(db, line, importId)


def execution(parameters_path, myvdefile):
    db = connexion.connect(parameters_path)
    importId = entete.readImportIdFromDb(db)
    line = readVdeToSetTable(myvdefile)
    setToDb(db, line, importId)


if __name__ == '__main__':
    parameters_path = sys.argv[1]
    myvdefile = sys.argv[2]
    db = connexion.connect(parameters_path)
    importId = entete.readImportIdFromDb(db)
    db = connexion.connect(parameters_path)
    line = readVdeToSetTable(myvdefile)
    setToDb(db, line, importId)