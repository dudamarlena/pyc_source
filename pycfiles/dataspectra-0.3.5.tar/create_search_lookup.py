# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: scripts/create_search_lookup.py
# Compiled at: 2017-10-08 14:17:02
import os

def search_term_file_auto_generate(self):
    """
    Should this be user generated?
    There are only going to be a few types.
    This can be automatically generated - but can also be user generated.    Automatically generate -
 by specifying the Type.

    ["SEARCHTYPE"] - if MULTIPLE - then there are multiple images.
        - if NONE - then there is only a single image. For example a reference image that you want someone to be able to jump to.
    
    #Step 2: If a dataset has a single search term. Then use that. 

    NOTES:
        - Currently - removes all the directories before in the search directory. 

    """
    searchSet = set()
    for dataset in self.datasets:
        if dataset.search.lower() == 'multiple':
            fileIN = open(dataset.genesP)
            dataset.searchDict = dict()
            for i in fileIN:
                i = i.rstrip().split('\t')
                dataset.searchDict[i[0]] = i[1].split('/')[(-1)]
                if i[0] not in searchSet:
                    searchSet.add(i[0])

            fileIN.close()
        if dataset.search.lower() == 'single':
            fileIN = open(dataset.genesP)
            dataset.singleFilePath = fileIN.readline().rstrip().split('\t')[(-1)].split('/')[(-1)]
            fileIN.close()

    outputFile = 'tmp/search_lookup_file.txt'
    fileOUT = open(outputFile, 'w')
    search_lookup_table = list()
    for searchTerm in searchSet:
        searchVec = list()
        for dataset in self.datasets:
            if dataset.search.lower() == 'multiple':
                if searchTerm not in dataset.searchDict:
                    matchFileName = 'NA'
                else:
                    matchFileName = dataset.searchDict[searchTerm]
            elif dataset.search.lower() == 'single':
                matchFileName = dataset.singleFilePath
            location = dataset.setkey + '/' + matchFileName
            searchVec.append(location)

        search_lookup_table.append([searchTerm] + searchVec)
        outString = searchTerm + '\t' + ('\t').join(searchVec) + '\n'
        fileOUT.write(outString)

    fileOUT.close()
    self.search_lookup_file = outputFile


def upload_search_lookup_to_google_cloud(self):
    cmd = [
     'gsutil', 'cp', self.search_lookup_file, 'gs://' + self.appid + '.appspot.com']
    os.system((' ').join(cmd))