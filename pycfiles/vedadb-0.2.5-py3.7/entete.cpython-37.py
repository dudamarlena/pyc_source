# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vedadb/entete.py
# Compiled at: 2019-09-06 04:36:45
# Size of source mod 2**32: 2100 bytes
__all__ = [
 'entete']
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import vedadb.connexion as connexion

def writeEnteteInDb(db, line):
    db.insert('entete', importidveda=(line['ImportID']), gdx2vedaversion=(line['GDX2VEDAversion']), vedaflavor=(line['VEDAFlavor']),
      dimensions=(line['Dimensions']),
      parentdimensions=(line['ParentDimensions']),
      setallowed=(line['SetsAllowed']),
      fieldsize=(line['FieldSize']),
      notindexed=(line['NotIndexed']),
      defaultvaluedim=(line['DefaultValueDim']),
      fieldseparator=(line['FieldSeparator']),
      textdelim=(line['TextDelim']))


def readAndWriteEntete(myfile):
    vd_file = open(myfile, 'r')
    x = 0
    result = {}
    while x < 12:
        if x == 0:
            line = vd_file.readline()
            resultline = line.split('GDX2VEDAversion-')[1].strip()
            keyline = line.split('-')[0].split('*')[1].strip()
            result.update({keyline: resultline})
        else:
            line = vd_file.readline()
            keyline = line.split('-')[0].split('*')[1].strip()
            resultline = line.split('-')[1].strip()
            result.update({keyline: resultline})
        if not line:
            break
        x = x + 1

    return result


def readImportIdFromDb(db):
    for r in db.query('SELECT importid FROM entete ORDER BY importid DESC LIMIT 1').dictresult():
        result = r['importid']

    return result


def execution(parameters_path, myvdfile):
    r = connexion.connect(parameters_path)
    writeEnteteInDb(r, readAndWriteEntete(myvdfile))


if __name__ == '__main__':
    parameters_path = sys.argv[1]
    myvdfile = sys.argv[2]
    r = connexion.connect(parameters_path)
    writeEnteteInDb(r, readAndWriteEntete(myvdfile))