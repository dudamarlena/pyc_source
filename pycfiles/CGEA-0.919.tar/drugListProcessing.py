# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/drugListProcessing.py
# Compiled at: 2017-01-17 15:30:12
from copy import deepcopy
from file import read_JSON
import os

class drugListProcessing:
    typesOfID = [
     'CAS', 'chembl_id', 'chebi_id', 'DrugBank', 'PubChem', 'MeSH_ID', 'KEGG_drug', 'name', 'Rname', 'stitch_id']
    namePrettifier = {'name': 'Name'}
    bannedCols = [
     'Rname']

    def __init__(self, cmap):
        if isinstance(cmap, basestring) and os.path.isfile(cmap):
            cmap = read_JSON(cmap)
        self.cmap = cmap
        allDrugIDsByType = dict(map(lambda x: (x,
         set(map(lambda y: y[x].lower(), filter(lambda y: x in y, cmap)))), self.typesOfID))
        entryLookupByID = {}
        for entry in cmap:
            for type in self.typesOfID:
                if type in entry and entry[type] not in ('NA', ''):
                    if entry[type].lower() not in entryLookupByID:
                        entryLookupByID[entry[type].lower()] = entry
                    elif entryLookupByID[entry[type].lower()] == entry:
                        pass
                    else:
                        countNA_1 = entry.values().count('NA')
                        countNA_2 = entryLookupByID[entry[type].lower()].values().count('NA')
                        if countNA_1 < countNA_2:
                            entryLookupByID[entry[type].lower()] = entry
                        elif countNA_1 == countNA_2:
                            pass

            for key, value in entry.items():
                if key in self.namePrettifier:
                    del entry[key]
                    entry[self.namePrettifier[key]] = value

            del entry['Rname']

        self.entryLookupByID = entryLookupByID
        allDrugIDs = set.union(*allDrugIDsByType.values())
        self.allDrugIDsByType = allDrugIDsByType
        self.allDrugIDs = allDrugIDs

    def inCMAP(self, ids, type=None):
        if type and type not in self.allDrugIDsByType:
            print str(type) + ' is not in the list of accepted types.'
            return False
        ids = deepcopy(ids)
        if (isinstance(ids, list) or isinstance(ids, set)) and isinstance(next(iter(ids)), basestring):
            for index, id in enumerate(ids):
                if not type:
                    ids[index] = (
                     id, id.lower() in self.allDrugIDs)
                else:
                    ids[index] = (
                     id, id.lower() in self.allDrugIDsByType[type])

            return ids
        if isinstance(ids, basestring):
            if not type:
                return ids.lower() in self.allDrugIDs
            else:
                return ids.lower() in self.allDrugIDsByType[type]

        elif isinstance(ids, list) or isinstance(ids, set):
            print str(type(next(iter(ids)))) + ' is not a valid input type for id'
        else:
            print str(type(ids)) + ' is not a valid input type for id'
        return False

    def getRegex(self):
        self.allDrugIDs

    def annotateIDs(self, ids):
        drugList = self.inCMAP(ids)
        hits = map(lambda x: x[0], filter(lambda x: x[1], drugList))
        misses = map(lambda x: x[0], filter(lambda x: not x[1], drugList))
        for index, hit in enumerate(hits):
            hits[index] = self.namePrettifier[self.entryLookupByID[hit.lower()]]

        return (
         hits, misses)

    def annotateCMAP(self, hits):
        if not isinstance(hits, set):
            hits = set(hits)
        for row in self.cmap:
            if row['Name'] in hits:
                row['In Query Set'] = 'True'
            else:
                row['In Query Set'] = 'False'

        return self.cmap