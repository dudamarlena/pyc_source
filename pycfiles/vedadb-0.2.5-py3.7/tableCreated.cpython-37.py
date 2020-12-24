# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vedadb/tableCreated.py
# Compiled at: 2019-09-13 13:06:56
# Size of source mod 2**32: 2474 bytes
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import vedadb.connexion as connexion

def allTable(db):
    return db.get_tables()


def createTable(db):
    db.query('create table if not exists entete (importid serial primary key, importidveda varchar, gdx2vedaversion varchar, vedaflavor varchar, dimensions varchar, parentdimensions varchar, setallowed varchar, fieldsize varchar, notindexed varchar, defaultvaluedim varchar, fieldseparator varchar, textdelim varchar)')
    db.query('create table IF NOT EXISTS set(idset serial primary key, typedimensionset varchar, region varchar, codeset varchar, description varchar, importid INTEGER REFERENCES entete(importid))')
    db.query('create table if not exists dimensioncontent (iddimensioncontent serial primary key, dimensioncode varchar, region varchar, codeset varchar, typedimension varchar, descriptiondimensioncode varchar, idset INTEGER REFERENCES set(idset), importid  INTEGER REFERENCES entete(importid))')
    db.query('create table if not exists vedatable (idvedatable serial primary key, nom varchar, importid  INTEGER REFERENCES entete(importid), description varchar)')
    db.query('create table if not exists vedatablecontent (idvedatable integer, iddimensioncontent integer, idset integer, PRIMARY KEY (idvedatable,iddimensioncontent,idset), importid  INTEGER REFERENCES entete(importid))')
    db.query('create table if not exists resultat (resultid serial primary key, attribut varchar, commodity varchar, process varchar, periode varchar, region varchar, vintage varchar, timeslice varchar, userconstraint varchar, pv varchar, importid  INTEGER REFERENCES entete(importid))')


def execution(parameters_path):
    r = connexion.connect(parameters_path)
    createTable(r)


def dropTableByName(db, tablename):
    myquery = 'drop table ' + tablename
    db.query(myquery)


if __name__ == '__main__':
    parameters_path = sys.argv[1]
    r = connexion.connect(parameters_path)
    createTable(r)