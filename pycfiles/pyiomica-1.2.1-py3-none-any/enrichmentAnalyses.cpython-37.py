# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\A_MSU_NASA\VS\pyiomica\pyiomica\enrichmentAnalyses.py
# Compiled at: 2020-04-15 10:18:50
# Size of source mod 2**32: 74692 bytes
"""Annotations and Enumerations"""
import pymysql, datetime, urllib.request, requests
from .globalVariables import *
from . import utilityFunctions
from . import dataStorage

def internalAnalysisFunction(data, multiCorr, MultipleList, OutputID, InputID, Species, totalMembers, pValueCutoff, ReportFilterFunction, ReportFilter, TestFunction, HypothesisFunction, FilterSignificant, AssignmentForwardDictionary, AssignmentReverseDictionary, prefix, infoDict):
    """Analysis for Multi-Omics or Single-Omics input list
    The function is used internally and not intended to be used directly by user.
    
    Usage:
        Intended for internal use
    """
    listData = data[list(data.keys())[0]]
    if type(listData[0]) is not list:
        listData = [[item, 'Unknown'] for item in listData]
    else:
        if len(listData[0]) == 1:
            listData = [[item[0], 'Unknown'] for item in listData]
    dataForGeneTranslation = [item[0] if type(item) is list else item for item in listData]
    IDs = GeneTranslation(dataForGeneTranslation, OutputID, ConstantGeneDictionary, InputID=InputID, Species=Species)[OutputID]
    [item.remove('Missing') if 'Missing' in item else None for item in IDs]
    membersWithAssociations = {}
    for gene, geneIDs in zip(listData, IDs):
        if len(gene) == 4:
            geneKey, _, _, geneOmi = gene
        else:
            if len(gene) == 3:
                geneKey, geneOmi, _ = gene
            else:
                geneKey, geneOmi = gene
        if MultipleList:
            geneKey += '_' + geneOmi
        if geneKey in membersWithAssociations.keys():
            labels = membersWithAssociations[geneKey][0]
            if geneOmi not in labels:
                labels.append(geneOmi)
            else:
                membersWithAssociations[geneKey] = [
                 [
                  geneOmi], []]
            for ID in geneIDs:
                if prefix + ID in list(AssignmentForwardDictionary.keys()):
                    for AssignmentID in list(AssignmentForwardDictionary[(prefix + ID)]):
                        if AssignmentID not in membersWithAssociations[geneKey][1]:
                            membersWithAssociations[geneKey][1].append(AssignmentID)

            if len(membersWithAssociations[geneKey][1]) == 0:
                membersWithAssociations.pop(geneKey)

    allAssignmentIDs = []
    for thisGeneGOlist in [item[1] for item in list(membersWithAssociations.values())]:
        for AssignmentID in thisGeneGOlist:
            if AssignmentID not in allAssignmentIDs:
                allAssignmentIDs.append(AssignmentID)

    testCats = {}
    for AssignmentID in allAssignmentIDs:
        countsInList = len(membersWithAssociations.keys())
        countsInFamily = multiCorr * len(AssignmentReverseDictionary[AssignmentID])
        countsInMembers = np.sum([AssignmentID in item[1] for item in membersWithAssociations.values()])
        whereGeneHits = [AssignmentID in item[1] for item in membersWithAssociations.values()]
        listOfGenesHit = [[item, membersWithAssociations[item][0]] for item in np.array(list(membersWithAssociations.keys()))[whereGeneHits]]
        testValue = TestFunction(countsInList, countsInFamily, multiCorr * totalMembers, countsInMembers)
        testCats[AssignmentID] = [
         testValue, [countsInList, countsInFamily, multiCorr * totalMembers, countsInMembers], infoDict[AssignmentID], listOfGenesHit]

    correctedpValues = dict(zip(allAssignmentIDs, HypothesisFunction([item[0] for item in list(testCats.values())], pValueCutoff).T))
    for AssignmentID in allAssignmentIDs:
        testCats[AssignmentID][0] = [testCats[AssignmentID][0], correctedpValues[AssignmentID][1], correctedpValues[AssignmentID][2]]

    ResultsHCct = testCats
    whatIsFilteredLength = ReportFilterFunction(np.array([item[1][3] for item in list(ResultsHCct.values())]), ReportFilter)
    whatIsFilteredSignif = np.array([item[0][2] if FilterSignificant else True for item in list(ResultsHCct.values())]).astype(bool)
    whatIsFiltered = whatIsFilteredLength * whatIsFilteredSignif
    returning = dict(zip(list(np.array(list(ResultsHCct.keys()))[whatIsFiltered]), list(np.array(list(ResultsHCct.values()))[whatIsFiltered])))
    return {list(data.keys())[0]: returning}


def OBOGODictionary(FileURL='http://purl.obolibrary.org/obo/go/go-basic.obo', ImportDirectly=False, PyIOmicaDataDirectory=None, OBOFile='goBasicObo.txt'):
    """Generate Open Biomedical Ontologies (OBO) Gene Ontology (GO) vocabulary dictionary.
    
    Parameters: 
        FileURL: str, Default "http://purl.obolibrary.org/obo/go/go-basic.obo"
            Provides the location of the Open Biomedical Ontologies (OBO) Gene Ontology (GO) 
            file in case this will be downloaded from the web

        ImportDirectly: boolean, Default False
            Import from URL regardles is the file already exists

        PyIOmicaDataDirectory: str, Default None
            Path of directories to data storage

        OBOFile: str, Default "goBasicObo.txt"
            Name of file to store data in (file will be zipped)

    Returns:
        dictionary
            Dictionary of definitions

    Usage:
        OBODict = OBOGODictionary()
    """
    PyIOmicaDataDirectory = ConstantPyIOmicaDataDirectory if PyIOmicaDataDirectory == None else PyIOmicaDataDirectory
    fileGOOBO = os.path.join(PyIOmicaDataDirectory, OBOFile)
    fileGOOBOgz = fileGOOBO + '.gz'
    if not os.path.isfile(fileGOOBOgz):
        print('Did Not Find Annotation Files, Attempting to Download...')
        ImportDirectly = True
    if os.path.isfile(fileGOOBO):
        os.remove(fileGOOBO)
    if ImportDirectly:
        if os.path.isfile(fileGOOBOgz):
            os.remove(fileGOOBOgz)
        urllib.request.urlretrieve(FileURL.strip('"'), fileGOOBO)
        if os.path.isfile(fileGOOBO):
            print('Created Annotation Files at ', fileGOOBO)
        else:
            print('Did Not Find Annotation Files, Aborting Process')
            return
            with open(fileGOOBO, 'rb') as (fileIn):
                with gzip.open(fileGOOBOgz, 'wb') as (fileOut):
                    shutil.copyfileobj(fileIn, fileOut)
            print('Compressed local file with GZIP.')
            os.remove(fileGOOBO)
    with gzip.open(fileGOOBOgz, 'r') as (tempFile):
        inputFile = tempFile.readlines()
    inputFile = [item.decode() for item in inputFile]
    outDictionary = {}
    for position in np.where([item == '[Term]\n' for item in inputFile])[0]:

        def getValue(index):
            return inputFile[(position + index)].strip(['id:', 'name:', 'namespace:'][(index - 1)]).strip('\n').strip()

        outDictionary[getValue(1)] = [
         getValue(2), getValue(3)]

    return outDictionary


def GetGeneDictionary(geneUCSCTable=None, UCSCSQLString=None, UCSCSQLSelectLabels=None, ImportDirectly=False, Species='human', KEGGUCSCSplit=[True, 'KEGG Gene ID']):
    """Create an ID/accession dictionary from a UCSC search - typically of gene annotations.
    
    Parameters: 
        geneUCSCTable: str, Default None
            Path to a geneUCSCTable file

        UCSCSQLString: str, Default None
            An association to be used to obtain data from the UCSC Browser tables. The key of the association must 
            match the Species option value used (default: human). The value for the species corresponds to the actual MySQL command used

        UCSCSQLSelectLabels: str, Default None
            An association to be used to assign key labels for the data imported from the UCSC Browser tables. 
            The key of the association must match the Species option value used (default: human). The value is a multi component string 
            list corresponding to the matrices in the data file, or the tables used in the MySQL query provided by UCSCSQLString

        ImportDirectly: boolean, Default False
            Import from URL regardles is the file already exists

        Species: str, Default "human"
            Species considered in the calculation, by default corresponding to human

        KEGGUCSCSplit: list, Default [True,"KEGG Gene ID"]
            Two component list, {True/False, label}. If the first component is set to True the initially imported KEGG IDs, 
            identified by the second component label,  are split on + string to fix nomenclature issues, retaining the string following +

    Returns:
        dictionary
            Gene dictionary

    Usage:
        geneDict = GetGeneDictionary()
    """
    UCSCSQLSelectLabels = {'human': ['UCSC ID', 'UniProt ID', 'Gene Symbol',
               'RefSeq ID', 'NCBI Protein Accession', 'Ensembl ID',
               'KEGG Gene ID', 'HGU133Plus2 Affymetrix ID']}
    UCSCSQLString = {'human': 'SELECT hg19.kgXref.kgID, hg19.kgXref.spID,         hg19.kgXref.geneSymbol, hg19.kgXref.refseq, hg19.kgXref.protAcc,         hg19.knownToEnsembl.value, hg19.knownToKeggEntrez.keggEntrez,         hg19.knownToU133Plus2.value FROM hg19.kgXref LEFT JOIN         hg19.knownToEnsembl ON hg19.kgXref.kgID = hg19.knownToEnsembl.name         LEFT JOIN hg19.knownToKeggEntrez ON hg19.kgXref.kgID =         hg19.knownToKeggEntrez.name LEFT JOIN hg19.knownToU133Plus2 ON         hg19.kgXref.kgID = hg19.knownToU133Plus2.name'}
    PyIOmicaDataDirectory = ConstantPyIOmicaDataDirectory
    if geneUCSCTable is None:
        geneUCSCTable = os.path.join(PyIOmicaDataDirectory, Species + 'GeneUCSCTable' + '.json.gz')
    elif not os.path.isfile(geneUCSCTable):
        print('Did Not Find Gene Translation Files, Attempting to Download from UCSC...')
        ImportDirectly = True
    else:
        termTable = dataStorage.read(geneUCSCTable, jsonFormat=True)[1]
        termTable = np.array(termTable)
    if ImportDirectly:
        ucscDatabase = pymysql.connect('genome-mysql.cse.ucsc.edu', 'genomep', 'password')
        if ucscDatabase == None:
            print('Could not establish connection to UCSC. Please try again or add the dictionary manually at ', geneUCSCTable)
            return
            ucscDatabaseCursor = ucscDatabase.cursor()
            try:
                ucscDatabaseCursor.execute(UCSCSQLString[Species])
                termTable = ucscDatabaseCursor.fetchall()
            except:
                print('Error: unable to fetch data')

            termTable = np.array(termTable).T
            termTable[np.where(termTable == '')] = None
            dataStorage.write((datetime.datetime.now().isoformat(), termTable.tolist()), geneUCSCTable, jsonFormat=True)
            ucscDatabase.close()
            if os.path.isfile(geneUCSCTable):
                print('Created Annotation Files at ', geneUCSCTable)
        else:
            print('Did Not Find Annotation Files, Aborting Process')
            return
    returning = {Species: dict(zip(UCSCSQLSelectLabels[Species], termTable))}
    if KEGGUCSCSplit[0]:
        returning[Species][KEGGUCSCSplit[1]] = np.array([item.split('+')[1] if item != None else item for item in returning[Species][KEGGUCSCSplit[1]]])
    return returning


def GOAnalysisAssigner(PyIOmicaDataDirectory=None, ImportDirectly=False, BackgroundSet=[], Species='human', LengthFilter=None, LengthFilterFunction=np.greater_equal, GOFileName=None, GOFileColumns=[2, 5], GOURL='http://current.geneontology.org/annotations/'):
    """Download and create gene associations and restrict to required background set.

    Parameters: 
        PyIOmicaDataDirectory: str, Default None
            The directory where the default package data is stored

        ImportDirectly: boolean, Default False
            Import from URL regardles is the file already exists

        BackgroundSet: list, Default []
            Background list to create annotation projection to limited background space, involves
            considering pathways/groups/sets and that provides a list of IDs (e.g. gene accessions) that should 
            be considered as the background for the calculation

        Species: str, Default "human"
            Species considered in the calculation, by default corresponding to human

        LengthFilterFunction: function, Default np.greater_equal
            Performs computations of membership in pathways/ontologies/groups/sets, 
            that specifies which function to use to filter the number of members a reported category has 
            compared to the number typically provided by LengthFilter 

        LengthFilter: int, Default None
            Argument for LengthFilterFunction

        GOFileName: str, Default None
            The name for the specific GO file to download from the GOURL if option ImportDirectly is set to True

        GOFileColumns: list, Default [2, 5]
            Columns to use for IDs and GO:accessions respectively from the downloaded GO annotation file, 
            used when ImportDirectly is set to True to obtain a new GO association file

        GOURL: str, Default "http://current.geneontology.org/annotations/"
            The location (base URL) where the GO association annotation files are downloaded from

    Returns:
        dictionary
            Dictionary of IDToGO and GOToID dictionaries

    Usage:
        GOassignment = GOAnalysisAssigner()
    """
    PyIOmicaDataDirectory = ConstantPyIOmicaDataDirectory if PyIOmicaDataDirectory == None else PyIOmicaDataDirectory
    file = 'goa_' + Species + '.gaf.gz' if GOFileName == None else GOFileName
    localFile = os.path.join(PyIOmicaDataDirectory, 'goa_' + Species + '.gaf')
    localZipFile = os.path.join(PyIOmicaDataDirectory, 'goa_' + Species + '.gaf.gz')
    fileGOAssociations = [os.path.join(PyIOmicaDataDirectory, Species + item + '.json.gz') for item in ('GeneOntAssoc',
                                                                                                        'IdentifierAssoc')]
    if not np.array(list(map(os.path.isfile, fileGOAssociations))).all():
        print('Did Not Find Annotation Files, Attempting to Download...')
        ImportDirectly = True
    elif ImportDirectly:
        if os.path.isfile(localFile):
            os.remove(localFile)
        else:
            urllib.request.urlretrieve(GOURL + file, '\\'.join([localZipFile]))
            with gzip.open(localZipFile, 'rb') as (fileIn):
                with open(localFile, 'wb') as (fileOut):
                    shutil.copyfileobj(fileIn, fileOut)
            os.remove(localZipFile)
            with open(localFile, 'r') as (tempFile):
                goData = tempFile.readlines()
            goData = np.array(goData[np.where(np.array([line[0] != '!' for line in goData]))[0][0]:])
            goData = pd.DataFrame([item.strip('\n').split('\t') for item in goData]).values
            df = pd.DataFrame(goData.T[(np.array(GOFileColumns) - 1)].T)
            df = df[(np.count_nonzero((df.values != ''), axis=1) == 2)]
            dfGrouped = df.groupby(df.columns[1])
            keys, values = list(dfGrouped.indices.keys()), list(dfGrouped.indices.values())
            IDs = df.values.T[0]
            geneOntAssoc = dict(zip(keys, [np.unique(IDs[value]).tolist() for value in values]))
            identifierAssoc = utilityFunctions.createReverseDictionary(geneOntAssoc)
            dataStorage.write((datetime.datetime.now().isoformat(), geneOntAssoc), (fileGOAssociations[0]), jsonFormat=True)
            dataStorage.write((datetime.datetime.now().isoformat(), identifierAssoc), (fileGOAssociations[1]), jsonFormat=True)
            os.remove(localFile)
            if np.array(list(map(os.path.isfile, fileGOAssociations))).all():
                print('Created Annotation Files at ', fileGOAssociations)
            else:
                print('Did Not Find Annotation Files, Aborting Process')
                return
    else:
        geneOntAssoc = dataStorage.read((fileGOAssociations[0]), jsonFormat=True)[(-1)]
        identifierAssoc = dataStorage.read((fileGOAssociations[1]), jsonFormat=True)[(-1)]
    if BackgroundSet != []:
        keys, values = np.array(list(identifierAssoc.keys())), np.array(list(identifierAssoc.values()))
        index = np.where([((len(values[i]) == True) * (values[i][0] != values[i][0]) == False) * (keys[i] in BackgroundSet) for i in range(len(keys))])[0]
        identifierAssoc = dict(zip(keys[index], values[index]))
        geneOntAssoc = utilityFunctions.createReverseDictionary(identifierAssoc)
    if LengthFilter != None:
        keys, values = np.array(list(geneOntAssoc.keys())), np.array(list(geneOntAssoc.values()))
        index = np.where(LengthFilterFunction(np.array([len(value) for value in values]), LengthFilter))[0]
        geneOntAssoc = dict(zip(keys[index], values[index]))
        identifierAssoc = utilityFunctions.createReverseDictionary(geneOntAssoc)
    return {Species: {'IDToGO':identifierAssoc,  'GOToID':geneOntAssoc}}


def obtainConstantGeneDictionary(GeneDictionary, GetGeneDictionaryOptions, AugmentDictionary):
    """Obtain gene dictionary - if it exists can either augment with new information or Species or create new, 
    if not exist then create variable.

    Parameters:
        GeneDictionary: dictionary or None
            An existing variable to use as a gene dictionary in annotations. 
            If set to None the default ConstantGeneDictionary will be used

        GetGeneDictionaryOptions: dictionary
            A list of options that will be passed to this internal GetGeneDictionary function

        AugmentDictionary: boolean
            A choice whether or not to augment the current ConstantGeneDictionary global variable or create a new one

    Returns:
        None

    Usage:
        obtainConstantGeneDictionary(None, {}, False)
    """
    global ConstantGeneDictionary
    if ConstantGeneDictionary != None:
        if AugmentDictionary:
            ConstantGeneDictionary = {**ConstantGeneDictionary, **(GetGeneDictionary(**GetGeneDictionaryOptions) if GeneDictionary == None else GeneDictionary)}
        else:
            ConstantGeneDictionary = GetGeneDictionary(**GetGeneDictionaryOptions) if GeneDictionary == None else GeneDictionary
    else:
        ConstantGeneDictionary = GetGeneDictionary(**GetGeneDictionaryOptions) if GeneDictionary == None else GeneDictionary


def GOAnalysis(data, GetGeneDictionaryOptions={}, AugmentDictionary=True, InputID=['UniProt ID', 'Gene Symbol'], OutputID='UniProt ID', GOAnalysisAssignerOptions={}, BackgroundSet=[], Species='human', OntologyLengthFilter=2, ReportFilter=1, ReportFilterFunction=np.greater_equal, pValueCutoff=0.05, TestFunction=lambda n, N, M, x: 1.0 - scipy.stats.hypergeom.cdf(x - 1, M, n, N), HypothesisFunction=lambda data, SignificanceLevel: BenjaminiHochbergFDR(data, SignificanceLevel=SignificanceLevel)['Results'], FilterSignificant=True, OBODictionaryVariable=None, OBOGODictionaryOptions={}, MultipleListCorrection=None, MultipleList=False, GeneDictionary=None):
    """Calculate input data over-representation analysis for Gene Ontology (GO) categories.

    Parameters:
        data: pd.DataFrame or list
            Data to analyze

        GetGeneDictionaryOptions: dictionary, Default {}
            A list of options that will be passed to this internal GetGeneDictionary function

        AugmentDictionary: boolean, Default True
            A choice whether or not to augment the current ConstantGeneDictionary global variable or create a new one

        InputID: list, Default ["UniProt ID","Gene Symbol"]
            Kind of identifiers/accessions used as input

        OutputID: str, Default "UniProt ID"
            Kind of IDs/accessions to convert the input IDs/accession numbers in the function's analysis

        GOAnalysisAssignerOptions: dictionary, Default {}
            A list of options that will be passed to the internal GOAnalysisAssigner function

        BackgroundSet: list, Default []
            Background list to create annotation projection to limited background space, involves
            considering pathways/groups/sets and that provides a list of IDs (e.g. gene accessions) that should be 
            considered as the background for the calculation

        Species: str, Default "human"
            The species considered in the calculation, by default corresponding to human

        OntologyLengthFilter: int, Default 2
            Function that can be used to set the value for which terms to consider in the computation, 
            by excluding GO terms that have fewer items compared to the OntologyLengthFilter value. It is used by the internal
            GOAnalysisAssigner function

        ReportFilter: int, Default 1
            Functions that use pathways/ontologies/groups, and provides a cutoff for membership in ontologies/pathways/groups
            in selecting which terms/categories to return. It is typically used in conjunction with ReportFilterFunction

        ReportFilterFunction: function , Default np.greater_equal
            Specifies what operator form will be used to compare against ReportFilter option value in 
            selecting which terms/categories to return

        pValueCutoff: float, Default 0.05
            Significance cutoff

        TestFunction: function, Default lambda n, N, M, x: 1. - scipy.stats.hypergeom.cdf(x-1, M, n, N)
            Test function

        HypothesisFunction: function, Default lambda data, SignificanceLevel: BenjaminiHochbergFDR(data, SignificanceLevel=SignificanceLevel)["Results"]
            Allows the choice of function for implementing multiple hypothesis testing considerations

        FilterSignificant: boolean, Default True
            Can be set to True to filter data based on whether the analysis result is statistically significant, 
            or if set to False to return all membership computations

        OBODictionaryVariable: str, Default None
            A GO annotation variable. If set to None, OBOGODictionary will be used internally to 
            automatically generate the default GO annotation

        OBOGODictionaryOptions: dictionary, Default {}
            A list of options to be passed to the internal OBOGODictionary function that provides the GO annotations

        MultipleListCorrection: boolean, Default None
            Specifies whether or not to correct for multi-omics analysis. The choices are None, Automatic, 
            or a custom number, e.g protein+RNA

        MultipleList: boolean, Default False
            Specifies whether the input accessions list constituted a multi-omics list input that is annotated so

        GeneDictionary: str, Default None
            Points to an existing variable to use as a gene dictionary in annotations. If set to None 
            the default ConstantGeneDictionary will be used

    Returns:
        dictionary
            Enrichment dictionary

    Usage:
        goExample1 = GOAnalysis(["TAB1", "TNFSF13B", "MALT1", "TIRAP", "CHUK", 
                                "TNFRSF13C", "PARP1", "CSNK2A1", "CSNK2A2", "CSNK2B", "LTBR", 
                                "LYN", "MYD88", "GADD45B", "ATM", "NFKB1", "NFKB2", "NFKBIA", 
                                "IRAK4", "PIAS4", "PLAU"])
    """
    OBODict = OBOGODictionary(**OBOGODictionaryOptions) if OBODictionaryVariable == None else OBODictionaryVariable
    obtainConstantGeneDictionary(GeneDictionary, GetGeneDictionaryOptions, AugmentDictionary)
    Assignment = GOAnalysisAssigner(BackgroundSet=BackgroundSet, Species=Species, LengthFilter=OntologyLengthFilter) if GOAnalysisAssignerOptions == {} else GOAnalysisAssigner(**GOAnalysisAssignerOptions)
    listToggle = False
    if type(data) is list:
        data = {'dummy': data}
        listToggle = True
    else:
        if type(data) is pd.DataFrame:
            id = list(data.index.get_level_values('id'))
            source = list(data.index.get_level_values('source'))
            data = [[id[i], source[i]] for i in range(len(data))]
            data = {'dummy': data}
            listToggle = True
        returning = {}
        if 'linkage' in data.keys():
            if MultipleListCorrection == None:
                multiCorr = 1
            else:
                if MultipleListCorrection == 'Automatic':
                    multiCorr = 1
                    for keyGroup in sorted([item for item in list(data.keys()) if not item == 'linkage']):
                        for keySubGroup in sorted([item for item in list(data[keyGroup].keys()) if not item == 'linkage']):
                            multiCorr = max(max(np.unique((data[keyGroup][keySubGroup]['data'].index.get_level_values('id')), return_counts=True)[1]), multiCorr)

                else:
                    multiCorr = MultipleListCorrection
            for keyGroup in sorted([item for item in list(data.keys()) if not item == 'linkage']):
                returning[keyGroup] = {}
                for keySubGroup in sorted([item for item in list(data[keyGroup].keys()) if not item == 'linkage']):
                    SubGroupMultiIndex = data[keyGroup][keySubGroup]['data'].index
                    SubGroupGenes = list(SubGroupMultiIndex.get_level_values('id'))
                    SubGroupMeta = list(SubGroupMultiIndex.get_level_values('source'))
                    SubGroupList = [[SubGroupGenes[i], SubGroupMeta[i]] for i in range(len(SubGroupMultiIndex))]
                    returning[keyGroup][keySubGroup] = internalAnalysisFunction({keySubGroup: SubGroupList}, multiCorr,
                      MultipleList, OutputID, InputID, Species, (len(Assignment[Species]['IDToGO'])), pValueCutoff,
                      ReportFilterFunction, ReportFilter, TestFunction, HypothesisFunction, FilterSignificant, AssignmentForwardDictionary=(Assignment[Species]['IDToGO']),
                      AssignmentReverseDictionary=(Assignment[Species]['GOToID']),
                      prefix='',
                      infoDict=OBODict)[keySubGroup]

        else:
            for key in list(data.keys()):
                if MultipleListCorrection == None:
                    multiCorr = 1
                else:
                    if MultipleList and MultipleListCorrection == 'Automatic':
                        multiCorr = max(np.unique([item[0] for item in data[key]], return_counts=True)[1])
                    else:
                        multiCorr = MultipleListCorrection
                returning.update(internalAnalysisFunction({key: data[key]}, multiCorr, MultipleList, OutputID, InputID, Species, (len(Assignment[Species]['IDToGO'])), pValueCutoff,
                  ReportFilterFunction, ReportFilter, TestFunction, HypothesisFunction, FilterSignificant, AssignmentForwardDictionary=(Assignment[Species]['IDToGO']),
                  AssignmentReverseDictionary=(Assignment[Species]['GOToID']),
                  prefix='',
                  infoDict=OBODict))

        returning = returning['dummy'] if listToggle else returning
    return returning


def GeneTranslation--- This code section failed: ---

 L. 669         0  LOAD_FAST                'InputID'
                2  LOAD_CONST               None
                4  COMPARE_OP               !=
                6  POP_JUMP_IF_FALSE    94  'to 94'

 L. 670         8  BUILD_LIST_0          0 
               10  STORE_FAST               'listOfKeysToUse'

 L. 671        12  LOAD_GLOBAL              type
               14  LOAD_FAST                'InputID'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  LOAD_GLOBAL              list
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    70  'to 70'

 L. 672        24  SETUP_LOOP           92  'to 92'
               26  LOAD_FAST                'InputID'
               28  GET_ITER         
             30_0  COME_FROM            52  '52'
               30  FOR_ITER             66  'to 66'
               32  STORE_FAST               'key'

 L. 673        34  LOAD_FAST                'key'
               36  LOAD_GLOBAL              list
               38  LOAD_FAST                'GeneDictionary'
               40  LOAD_FAST                'Species'
               42  BINARY_SUBSCR    
               44  LOAD_METHOD              keys
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  COMPARE_OP               in
               52  POP_JUMP_IF_FALSE    30  'to 30'

 L. 674        54  LOAD_FAST                'listOfKeysToUse'
               56  LOAD_METHOD              append
               58  LOAD_FAST                'key'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  POP_TOP          
               64  JUMP_BACK            30  'to 30'
               66  POP_BLOCK        
               68  JUMP_ABSOLUTE       110  'to 110'
             70_0  COME_FROM            22  '22'

 L. 675        70  LOAD_GLOBAL              type
               72  LOAD_FAST                'InputID'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  LOAD_GLOBAL              str
               78  COMPARE_OP               is
               80  POP_JUMP_IF_FALSE   110  'to 110'

 L. 676        82  LOAD_FAST                'listOfKeysToUse'
               84  LOAD_METHOD              append
               86  LOAD_FAST                'InputID'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_TOP          
             92_0  COME_FROM_LOOP       24  '24'
               92  JUMP_FORWARD        110  'to 110'
             94_0  COME_FROM             6  '6'

 L. 678        94  LOAD_GLOBAL              list
               96  LOAD_FAST                'GeneDictionary'
               98  LOAD_FAST                'Species'
              100  BINARY_SUBSCR    
              102  LOAD_METHOD              keys
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  STORE_FAST               'listOfKeysToUse'
            110_0  COME_FROM            92  '92'
            110_1  COME_FROM            80  '80'

 L. 680       110  BUILD_MAP_0           0 
              112  STORE_FAST               'returning'

 L. 682   114_116  SETUP_LOOP          412  'to 412'
              118  LOAD_GLOBAL              type
              120  LOAD_FAST                'TargetIDList'
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  LOAD_GLOBAL              str
              126  COMPARE_OP               is
              128  POP_JUMP_IF_FALSE   136  'to 136'
              130  LOAD_FAST                'TargetIDList'
              132  BUILD_LIST_1          1 
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           128  '128'
              136  LOAD_FAST                'TargetIDList'
            138_0  COME_FROM           134  '134'
              138  GET_ITER         
            140_0  COME_FROM           310  '310'
          140_142  FOR_ITER            410  'to 410'
              144  STORE_FAST               'TargetID'

 L. 683       146  BUILD_MAP_0           0 
              148  LOAD_FAST                'returning'
              150  LOAD_FAST                'TargetID'
              152  STORE_SUBSCR     

 L. 684       154  SETUP_LOOP          304  'to 304'
              156  LOAD_FAST                'listOfKeysToUse'
              158  GET_ITER         
              160  FOR_ITER            302  'to 302'
              162  STORE_FAST               'key'

 L. 685       164  BUILD_LIST_0          0 
              166  LOAD_FAST                'returning'
              168  LOAD_FAST                'TargetID'
              170  BINARY_SUBSCR    
              172  LOAD_FAST                'key'
              174  STORE_SUBSCR     

 L. 686       176  SETUP_LOOP          300  'to 300'
              178  LOAD_FAST                'InputList'
              180  GET_ITER         
              182  FOR_ITER            298  'to 298'
              184  STORE_FAST               'item'

 L. 687       186  LOAD_GLOBAL              np
              188  LOAD_METHOD              array
              190  LOAD_FAST                'GeneDictionary'
              192  LOAD_FAST                'Species'
              194  BINARY_SUBSCR    
              196  LOAD_FAST                'TargetID'
              198  BINARY_SUBSCR    
              200  CALL_METHOD_1         1  '1 positional argument'
              202  LOAD_GLOBAL              np
              204  LOAD_METHOD              where
              206  LOAD_GLOBAL              np
              208  LOAD_METHOD              array
              210  LOAD_FAST                'GeneDictionary'
              212  LOAD_FAST                'Species'
              214  BINARY_SUBSCR    
              216  LOAD_FAST                'key'
              218  BINARY_SUBSCR    
              220  CALL_METHOD_1         1  '1 positional argument'
              222  LOAD_FAST                'item'
              224  COMPARE_OP               ==
              226  CALL_METHOD_1         1  '1 positional argument'
              228  LOAD_CONST               0
              230  BINARY_SUBSCR    
              232  BINARY_SUBSCR    
              234  STORE_FAST               'allEntries'

 L. 688       236  LOAD_FAST                'returning'
              238  LOAD_FAST                'TargetID'
              240  BINARY_SUBSCR    
              242  LOAD_FAST                'key'
              244  BINARY_SUBSCR    
              246  LOAD_METHOD              append
              248  LOAD_GLOBAL              list
              250  LOAD_FAST                'InputID'
              252  LOAD_CONST               None
              254  COMPARE_OP               !=
          256_258  POP_JUMP_IF_FALSE   288  'to 288'
              260  LOAD_GLOBAL              np
              262  LOAD_METHOD              unique
              264  LOAD_FAST                'allEntries'
              266  LOAD_GLOBAL              np
              268  LOAD_METHOD              where
              270  LOAD_FAST                'allEntries'
              272  LOAD_CONST               None
              274  COMPARE_OP               !=
              276  CALL_METHOD_1         1  '1 positional argument'
              278  LOAD_CONST               0
              280  BINARY_SUBSCR    
              282  BINARY_SUBSCR    
              284  CALL_METHOD_1         1  '1 positional argument'
              286  JUMP_FORWARD        290  'to 290'
            288_0  COME_FROM           256  '256'
              288  LOAD_FAST                'allEntries'
            290_0  COME_FROM           286  '286'
              290  CALL_FUNCTION_1       1  '1 positional argument'
              292  CALL_METHOD_1         1  '1 positional argument'
              294  POP_TOP          
              296  JUMP_BACK           182  'to 182'
              298  POP_BLOCK        
            300_0  COME_FROM_LOOP      176  '176'
              300  JUMP_BACK           160  'to 160'
              302  POP_BLOCK        
            304_0  COME_FROM_LOOP      154  '154'

 L. 691       304  LOAD_FAST                'InputID'
              306  LOAD_CONST               None
              308  COMPARE_OP               !=
              310  POP_JUMP_IF_FALSE   140  'to 140'

 L. 692       312  LOAD_FAST                'returning'
              314  LOAD_METHOD              copy
              316  CALL_METHOD_0         0  '0 positional arguments'
              318  STORE_FAST               'returningCopy'

 L. 693       320  BUILD_LIST_0          0 
              322  LOAD_FAST                'returning'
              324  LOAD_FAST                'TargetID'
              326  STORE_SUBSCR     

 L. 694       328  SETUP_LOOP          408  'to 408'
              330  LOAD_GLOBAL              enumerate
              332  LOAD_FAST                'InputList'
              334  CALL_FUNCTION_1       1  '1 positional argument'
              336  GET_ITER         
              338  FOR_ITER            406  'to 406'
              340  UNPACK_SEQUENCE_2     2 
              342  STORE_FAST               'iitem'
              344  STORE_FAST               'item'

 L. 695       346  BUILD_LIST_0          0 
              348  STORE_FAST               'tempList'

 L. 696       350  SETUP_LOOP          388  'to 388'
              352  LOAD_FAST                'listOfKeysToUse'
              354  GET_ITER         
              356  FOR_ITER            386  'to 386'
              358  STORE_FAST               'key'

 L. 697       360  LOAD_FAST                'tempList'
              362  LOAD_METHOD              extend
              364  LOAD_FAST                'returningCopy'
              366  LOAD_FAST                'TargetID'
              368  BINARY_SUBSCR    
              370  LOAD_FAST                'key'
              372  BINARY_SUBSCR    
              374  LOAD_FAST                'iitem'
              376  BINARY_SUBSCR    
              378  CALL_METHOD_1         1  '1 positional argument'
              380  POP_TOP          
          382_384  JUMP_BACK           356  'to 356'
              386  POP_BLOCK        
            388_0  COME_FROM_LOOP      350  '350'

 L. 698       388  LOAD_FAST                'returning'
              390  LOAD_FAST                'TargetID'
              392  BINARY_SUBSCR    
              394  LOAD_METHOD              append
              396  LOAD_FAST                'tempList'
              398  CALL_METHOD_1         1  '1 positional argument'
              400  POP_TOP          
          402_404  JUMP_BACK           338  'to 338'
              406  POP_BLOCK        
            408_0  COME_FROM_LOOP      328  '328'
              408  JUMP_BACK           140  'to 140'
              410  POP_BLOCK        
            412_0  COME_FROM_LOOP      114  '114'

 L. 700       412  LOAD_FAST                'returning'
              414  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 92_0


def KEGGAnalysisAssigner(PyIOmicaDataDirectory=None, ImportDirectly=False, BackgroundSet=[], KEGGQuery1='pathway', KEGGQuery2='hsa', LengthFilter=None, LengthFilterFunction=np.greater_equal, Labels=['IDToPath', 'PathToID']):
    """Create KEGG: Kyoto Encyclopedia of Genes and Genomes pathway associations, 
    restricted to required background set, downloading the data if necessary.

    Parameters: 
        PyIOmicaDataDirectory: str, Default None
            Directory where the default package data is stored

        ImportDirectly: boolean, Default False
            Import from URL regardles is the file already exists

        BackgroundSet: list, Default []
            A list of IDs (e.g. gene accessions) that should be considered as the background for the calculation

        KEGGQuery1: str, Default "pathway"
            Make KEGG API calls, and sets string query1 in http://rest.kegg.jp/link/<> query1 <> / <> query2. 
            Typically this will be used as the target database to find related entries by using database cross-references

        KEGGQuery2: str, Default "hsa"
            KEGG API calls, and sets string query2 in http://rest.kegg.jp/link/<> query1 <> / <> query2. 
            Typically this will be used as the source database to find related entries by using database cross-references

        LengthFilterFunction: function, Default np.greater_equal
            Option for functions that perform computations of membership in 
            pathways/ontologies/groups/sets, that specifies which function to use to filter the number of members a reported 
            category has compared to the number typically provided by LengthFilter

        LengthFilter: int, Default None
            Allows the selection of how many members each category can have, as typically 
            restricted by the LengthFilterFunction

        Labels: list, Default ["IDToPath", "PathToID"]
            A string list for how keys in a created association will be named

    Returns:
        dictionary
            IDToPath and PathToID dictionary

    Usage:
        KEGGassignment = KEGGAnalysisAssigner()
    """
    PyIOmicaDataDirectory = ConstantPyIOmicaDataDirectory if PyIOmicaDataDirectory == None else PyIOmicaDataDirectory
    fileAssociations = [os.path.join(PyIOmicaDataDirectory, item) for item in [KEGGQuery1 + '_' + KEGGQuery2 + 'KEGGMemberToPathAssociation.json.gz',
     KEGGQuery1 + '_' + KEGGQuery2 + 'KEGGPathToMemberAssociation.json.gz']]
    if not np.array(list(map(os.path.isfile, fileAssociations))).all():
        print('Did Not Find Annotation Files, Attempting to Download...')
        ImportDirectly = True
    elif ImportDirectly:
        localFile = os.path.join(PyIOmicaDataDirectory, KEGGQuery1 + '_' + KEGGQuery2 + '.tsv')
        if os.path.isfile(localFile):
            os.remove(localFile)
        else:
            urllib.request.urlretrieve('http://rest.kegg.jp/link/' + KEGGQuery1 + ('' if KEGGQuery2 == '' else '/' + KEGGQuery2), localFile)
            with open(localFile, 'r') as (tempFile):
                tempLines = tempFile.readlines()
            df = pd.DataFrame([line.strip('\n').split('\t') for line in tempLines])
            dfGrouped = df.groupby(df.columns[1])
            keys, values = list(dfGrouped.indices.keys()), list(dfGrouped.indices.values())
            IDs = df.values.T[0]
            pathToID = dict(zip(keys, [np.unique(IDs[value]).tolist() for value in values]))
            idToPath = utilityFunctions.createReverseDictionary(pathToID)
            dataStorage.write((datetime.datetime.now().isoformat(), idToPath), (fileAssociations[0]), jsonFormat=True)
            dataStorage.write((datetime.datetime.now().isoformat(), pathToID), (fileAssociations[1]), jsonFormat=True)
            os.remove(localFile)
            if np.array(list(map(os.path.isfile, fileAssociations))).all():
                print('Created Annotation Files at ', fileAssociations)
            else:
                print('Did Not Find Annotation Files, Aborting Process')
                return
    else:
        idToPath = dataStorage.read((fileAssociations[0]), jsonFormat=True)[1]
        pathToID = dataStorage.read((fileAssociations[1]), jsonFormat=True)[1]
    if BackgroundSet != []:
        keys, values = np.array(list(idToPath.keys())), np.array(list(idToPath.values()))
        index = np.where([((len(values[i]) == True) * (values[i][0] != values[i][0]) == False) * (keys[i] in BackgroundSet) for i in range(len(keys))])[0]
        idToPath = dict(zip(keys[index], values[index]))
        pathToID = utilityFunctions.createReverseDictionary(idToPath)
    if LengthFilter != None:
        keys, values = np.array(list(pathToID.keys())), np.array(list(pathToID.values()))
        index = np.where(LengthFilterFunction(np.array([len(value) for value in values]), LengthFilter))[0]
        pathToID = dict(zip(keys[index], values[index]))
        idToPath = utilityFunctions.createReverseDictionary(pathToID)
    return {KEGGQuery2: {Labels[0]: idToPath, Labels[1]: pathToID}}


def KEGGDictionary(PyIOmicaDataDirectory=None, ImportDirectly=False, KEGGQuery1='pathway', KEGGQuery2='hsa'):
    """Create a dictionary from KEGG: Kyoto Encyclopedia of Genes and Genomes terms - 
    typically association of pathways and members therein.
    
    Parameters: 
        PyIOmicaDataDirectory: str, Default None
            directory where the default package data is stored

        ImportDirectly: boolean, Default False
            import from URL regardles is the file already exists

        KEGGQuery1: str, Default "pathway"
            make KEGG API calls, and sets string query1 in http://rest.kegg.jp/link/<> query1 <> / <> query2. 
            Typically this will be used as the target database to find related entries by using database cross-references

        KEGGQuery2: str, Default "hsa"
            KEGG API calls, and sets string query2 in http://rest.kegg.jp/link/<> query1 <> / <> query2. 
            Typically this will be used as the source database to find related entries by using database cross-references

    Returns:
        dictionary
            Dictionary of definitions

    Usage:
        KEGGDict = KEGGDictionary()
    """
    PyIOmicaDataDirectory = ConstantPyIOmicaDataDirectory if PyIOmicaDataDirectory == None else PyIOmicaDataDirectory
    fileKEGGDict = os.path.join(PyIOmicaDataDirectory, KEGGQuery1 + '_' + KEGGQuery2 + '_KEGGDictionary.json.gz')
    if os.path.isfile(fileKEGGDict):
        associationKEGG = dataStorage.read(fileKEGGDict, jsonFormat=True)[1]
    else:
        print('Did Not Find Annotation Files, Attempting to Download...')
        ImportDirectly = True
    if ImportDirectly:
        queryFile = os.path.join(PyIOmicaDataDirectory, KEGGQuery1 + '_' + KEGGQuery2 + '.tsv')
        if os.path.isfile(queryFile):
            os.remove(queryFile)
        else:
            urllib.request.urlretrieve('http://rest.kegg.jp/list/' + KEGGQuery1 + ('' if KEGGQuery2 == '' else '/' + KEGGQuery2), queryFile)
            with open(queryFile, 'r') as (tempFile):
                tempLines = tempFile.readlines()
            os.remove(queryFile)
            associationKEGG = dict([line.strip('\n').split('\t') for line in tempLines])
            dataStorage.write((datetime.datetime.now().isoformat(), associationKEGG), fileKEGGDict, jsonFormat=True)
            if os.path.isfile(fileKEGGDict):
                print('Created Annotation Files at ', fileKEGGDict)
            else:
                print('Did Not Find Annotation Files, Aborting Process')
                return
    return associationKEGG


def KEGGAnalysis(data, AnalysisType='Genomic', GetGeneDictionaryOptions={}, AugmentDictionary=True, InputID=['UniProt ID', 'Gene Symbol'], OutputID='KEGG Gene ID', MolecularInputID=['cpd'], MolecularOutputID='cpd', KEGGAnalysisAssignerOptions={}, BackgroundSet=[], KEGGOrganism='hsa', KEGGMolecular='cpd', KEGGDatabase='pathway', PathwayLengthFilter=2, ReportFilter=1, ReportFilterFunction=np.greater_equal, pValueCutoff=0.05, TestFunction=lambda n, N, M, x: 1.0 - scipy.stats.hypergeom.cdf(x - 1, M, n, N), HypothesisFunction=lambda data, SignificanceLevel: BenjaminiHochbergFDR(data, SignificanceLevel=SignificanceLevel)['Results'], FilterSignificant=True, KEGGDictionaryVariable=None, KEGGDictionaryOptions={}, MultipleListCorrection=None, MultipleList=False, GeneDictionary=None, Species='human', MolecularSpecies='compound', NonUCSC=False, PyIOmicaDataDirectory=None):
    """Calculate input data over-representation analysis for KEGG: Kyoto Encyclopedia of Genes and Genomes pathways.
    Input can be a list, a dictionary of lists or a clustering object.

    Parameters:
        data: pandas.DetaFrame or list
            Data to analyze

        AnalysisType: str, Default "Genomic"
            Analysis methods that may be used, "Genomic", "Molecular" or "All"

        GetGeneDictionaryOptions: dictionary, Default {}
            A list of options that will be passed to this internal GetGeneDictionary function

        AugmentDictionary: boolean, Default True
            A choice whether or not to augment the current ConstantGeneDictionary global variable or create a new one

        InputID: list, Default ["UniProt ID", "Gene Symbol"]
            The kind of identifiers/accessions used as input

        OutputID: str, Default "KEGG Gene ID"
            A string value that specifies what kind of IDs/accessions to convert the input IDs/accession 
            numbers in the function's analysis

        MolecularInputID: list, Default ["cpd"]
            A string list to indicate the kind of ID to use for the input molecule entries

        MolecularOutputID: str, Default "cpd"
            A string list to indicate the kind of ID to use for the input molecule entries

        KEGGAnalysisAssignerOptions: dictionary, Default {}
            A list of options that will be passed to this internal KEGGAnalysisAssigner function

        BackgroundSet: list, Default []
            A list of IDs (e.g. gene accessions) that should be considered as the background for the calculation

        KEGGOrganism: str, Default "hsa"
            Indicates which organism (org) to use for "Genomic" type of analysis (default is human analysis: org="hsa")

        KEGGMolecular: str, Default "cpd"
            Which database to use for molecular analysis (default is the compound database: cpd)

        KEGGDatabase: str, Default "pathway"
            KEGG database to use as the target database

        PathwayLengthFilter: int, Default 2
            Pathways to consider in the computation, by excluding pathways that have fewer items 
            compared to the PathwayLengthFilter value

        ReportFilter: int, Default 1
            Provides a cutoff for membership in ontologies/pathways/groups in selecting which terms/categories 
            to return. It is typically used in conjunction with ReportFilterFunction

        ReportFilterFunction: function, Default np.greater_equal
            Operator form will be used to compare against ReportFilter option value in selecting 
            which terms/categories to return

        pValueCutoff: float, Default 0.05
            A cutoff p-value for (adjusted) p-values to assess statistical significance

        TestFunction: function, Default lambda n, N, M, x: 1. - scipy.stats.hypergeom.cdf(x-1, M, n, N)
            A function used to calculate p-values

        HypothesisFunction: function, Default lambda data, SignificanceLevel: BenjaminiHochbergFDR(data, SignificanceLevel=SignificanceLevel)["Results"]
            Allows the choice of function for implementing multiple hypothesis testing considerations

        FilterSignificant: boolean, Default True
            Can be set to True to filter data based on whether the analysis result is statistically significant, 
            or if set to False to return all membership computations

        KEGGDictionaryVariable: str, Default None
            KEGG dictionary, and provides a KEGG annotation variable. If set to None, KEGGDictionary 
            will be used internally to automatically generate the default KEGG annotation

        KEGGDictionaryOptions: dictionary, Default {}
            A list of options to be passed to the internal KEGGDictionary function that provides the KEGG annotations

        MultipleListCorrection: boolean, Default None
            Specifies whether or not to correct for multi-omics analysis. 
            The choices are None, Automatic, or a custom number

        MultipleList: boolean, Default False 
            Whether the input accessions list constituted a multi-omics list input that is annotated so

        GeneDictionary: str, Default None
            Existing variable to use as a gene dictionary in annotations. If set to None the default ConstantGeneDictionary will be used

        Species: str, Default "human"
            The species considered in the calculation, by default corresponding to human

        MolecularSpecies: str, Default "compound"
            The kind of molecular input

        NonUCSC: , Default 
            If UCSC browser was used in determining an internal GeneDictionary used in ID translations,
            where the KEGG identifiers for genes are number strings (e.g. 4790).The NonUCSC option can be set to True 
            if standard KEGG accessions are used in a user provided GeneDictionary variable, 
            in the form OptionValue[KEGGOrganism] <>:<>numberString, e.g. hsa:4790

        PyIOmicaDataDirectory: str, Default None
            Directory where the default package data is stored

    Returns:
        dictionary
            Enrichment dictionary

    Usage:
        keggExample1 = KEGGAnalysis(["TAB1", "TNFSF13B", "MALT1", "TIRAP", "CHUK", "TNFRSF13C", "PARP1", "CSNK2A1", "CSNK2A2", "CSNK2B", "LTBR", "LYN", "MYD88", 
                                    "GADD45B", "ATM", "NFKB1", "NFKB2", "NFKBIA", "IRAK4", "PIAS4", "PLAU", "POLR3B", "NME1", "CTPS1", "POLR3A"])
    """
    argsLocal = locals().copy()
    obtainConstantGeneDictionary(None, {}, True)
    PyIOmicaDataDirectory = ConstantPyIOmicaDataDirectory if PyIOmicaDataDirectory == None else PyIOmicaDataDirectory
    if AnalysisType == 'Genomic':
        keggDict = KEGGDictionary(**KEGGDictionaryOptions) if KEGGDictionaryVariable == None else KEGGDictionaryVariable
        obtainConstantGeneDictionary(GeneDictionary, GetGeneDictionaryOptions, AugmentDictionary)
        Assignment = KEGGAnalysisAssigner(BackgroundSet=BackgroundSet, KEGGQuery1=KEGGDatabase, KEGGQuery2=KEGGOrganism, LengthFilter=PathwayLengthFilter) if KEGGAnalysisAssignerOptions == {} else KEGGAnalysisAssigner(**KEGGAnalysisAssignerOptions)
    else:
        if AnalysisType == 'Molecular':
            InputID = MolecularInputID
            OutputID = MolecularOutputID
            Species = MolecularSpecies
            NonUCSC = True
            KEGGOrganism = KEGGMolecular
            MultipleListCorrection = None
            keggDict = KEGGDictionary(**{'KEGGQuery1':'pathway',  'KEGGQuery2':''} if KEGGDictionaryOptions == {} else KEGGDictionaryOptions) if KEGGDictionaryVariable == None else KEGGDictionaryVariable
            fileMolDict = os.path.join(PyIOmicaDataDirectory, 'PyIOmicaMolecularDictionary.json.gz')
            if os.path.isfile(fileMolDict):
                GeneDictionary = dataStorage.read(fileMolDict, jsonFormat=True)[1]
            else:
                fileCSV = os.path.join(PackageDirectory, 'data', 'MathIOmicaMolecularDictionary.csv')
                print('Attempting to read:', fileCSV)
                if os.path.isfile(fileCSV):
                    with open(fileCSV, 'r') as (tempFile):
                        tempLines = tempFile.readlines()
                    tempData = np.array([line.strip('\n').replace('"', '').split(',') for line in tempLines]).T
                    tempData = {'compound': {'pumchem':tempData[0].tolist(),  'cpd':tempData[1].tolist()}}
                    dataStorage.write((datetime.datetime.now().isoformat(), tempData), fileMolDict, jsonFormat=True)
                else:
                    print('Could not find annotation file at ' + fileMolDict + ' Please either obtain an annotation file from mathiomica.org or provide a GeneDictionary option variable.')
                    return
                GeneDictionary = dataStorage.read(fileMolDict, jsonFormat=True)[1]
            obtainConstantGeneDictionary(GeneDictionary, {}, AugmentDictionary)
            Assignment = KEGGAnalysisAssigner(BackgroundSet=BackgroundSet, KEGGQuery1=KEGGDatabase, KEGGQuery2=KEGGOrganism, LengthFilter=PathwayLengthFilter) if KEGGAnalysisAssignerOptions == {} else KEGGAnalysisAssigner(**KEGGAnalysisAssignerOptions)
        else:
            if AnalysisType == 'All':
                argsMolecular = argsLocal.copy()
                argsMolecular['AnalysisType'] = 'Molecular'
                argsGenomic = argsLocal.copy()
                argsGenomic['AnalysisType'] = 'Genomic'
                return {'Molecular':KEGGAnalysis(**argsMolecular), 
                 'Genomic':KEGGAnalysis(**argsGenomic)}
            print('AnalysisType %s is not a valid choice.' % AnalysisType)
            return
    listToggle = False
    if type(data) is list:
        data = {'dummy': data}
        listToggle = True
    if type(data) is pd.DataFrame:
        id = list(data.index.get_level_values('id'))
        source = list(data.index.get_level_values('source'))
        data = [[id[i], source[i]] for i in range(len(data))]
        data = {'dummy': data}
        listToggle = True
    returning = {}
    if 'linkage' in data.keys():
        if MultipleListCorrection == None:
            multiCorr = 1
        else:
            if MultipleListCorrection == 'Automatic':
                multiCorr = 1
                for keyGroup in sorted([item for item in list(data.keys()) if not item == 'linkage']):
                    for keySubGroup in sorted([item for item in list(data[keyGroup].keys()) if not item == 'linkage']):
                        multiCorr = max(max(np.unique((data[keyGroup][keySubGroup]['data'].index.get_level_values('id')), return_counts=True)[1]), multiCorr)

            else:
                multiCorr = MultipleListCorrection
        for keyGroup in sorted([item for item in list(data.keys()) if not item == 'linkage']):
            returning[keyGroup] = {}
            for keySubGroup in sorted([item for item in list(data[keyGroup].keys()) if not item == 'linkage']):
                SubGroupMultiIndex = data[keyGroup][keySubGroup]['data'].index
                SubGroupGenes = list(SubGroupMultiIndex.get_level_values('id'))
                SubGroupMeta = list(SubGroupMultiIndex.get_level_values('source'))
                SubGroupList = [[SubGroupGenes[i], SubGroupMeta[i]] for i in range(len(SubGroupMultiIndex))]
                returning[keyGroup][keySubGroup] = internalAnalysisFunction({keySubGroup: SubGroupList}, multiCorr,
                  MultipleList, OutputID, InputID, Species, (len(Assignment[KEGGOrganism]['IDToPath'])), pValueCutoff,
                  ReportFilterFunction, ReportFilter, TestFunction, HypothesisFunction, FilterSignificant, AssignmentForwardDictionary=(Assignment[KEGGOrganism]['IDToPath']),
                  AssignmentReverseDictionary=(Assignment[KEGGOrganism]['PathToID']),
                  prefix=('hsa:' if AnalysisType == 'Genomic' else ''),
                  infoDict=keggDict)[keySubGroup]

    else:
        for key in list(data.keys()):
            if MultipleListCorrection == None:
                multiCorr = 1
            else:
                if MultipleList and MultipleListCorrection == 'Automatic':
                    multiCorr = max(np.unique([item[0] for item in data[key]], return_counts=True)[1])
                else:
                    multiCorr = MultipleListCorrection
            returning.update(internalAnalysisFunction({key: data[key]}, multiCorr, MultipleList, OutputID, InputID, Species, (len(Assignment[KEGGOrganism]['IDToPath'])), pValueCutoff,
              ReportFilterFunction, ReportFilter, TestFunction, HypothesisFunction, FilterSignificant, AssignmentForwardDictionary=(Assignment[KEGGOrganism]['IDToPath']),
              AssignmentReverseDictionary=(Assignment[KEGGOrganism]['PathToID']),
              prefix=('hsa:' if AnalysisType == 'Genomic' else ''),
              infoDict=keggDict))

        returning = returning['dummy'] if listToggle else returning
    return returning


def MassMatcher(data, accuracy, MassDictionaryVariable=None, MolecularSpecies='cpd'):
    """Assign putative mass identification to input data based on monoisotopic mass 
    (using PyIOmica's mass dictionary). The accuracy in parts per million. 
    
    Parameters: 
        data: np.array
            Input data

        accuracy: float
            Accuracy

        MassDictionaryVariable: boolean, Default None
            Mass dictionary variable. If set to None, inbuilt 
            mass dictionary (MassDictionary) will be loaded and used

        MolecularSpecies: str, Default "cpd"
            The kind of molecular input

    Returns:
        list
            List of IDs 

    Usage:
       result = MassMatcher(18.010565, 2)
    """
    ppm = accuracy * 1e-06
    MassDict = MassDictionary() if MassDictionaryVariable == None else MassDictionaryVariable
    keys, values = np.array(list(MassDict[MolecularSpecies].keys())), np.array(list(MassDict[MolecularSpecies].values()))
    return keys[np.where((values > data * (1 - ppm)) * (values < data * (1 + ppm)))[0]]


def MassDictionary(PyIOmicaDataDirectory=None):
    """Load PyIOmica's current mass dictionary.
    
    Parameters:
        PyIOmicaDataDirectory: str, Default None
            Directory where the default package data is stored

    Returns:
        dictionary
            Mass dictionary

    Usage:
        MassDict = MassDictionary()
    """
    PyIOmicaDataDirectory = ConstantPyIOmicaDataDirectory if PyIOmicaDataDirectory == None else PyIOmicaDataDirectory
    fileMassDict = os.path.join(PyIOmicaDataDirectory, 'PyIOmicaMassDictionary.json.gz')
    if os.path.isfile(fileMassDict):
        MassDict = dataStorage.read(fileMassDict, jsonFormat=True)[1]
    else:
        fileCSV = os.path.join(PackageDirectory, 'data', 'MathIOmicaMassDictionary.csv')
        if os.path.isfile(fileCSV):
            print('Reading:', fileCSV)
            fileMassDictData = np.loadtxt(fileCSV, delimiter=',', dtype=str)
            MassDict = {fileMassDictData[0][0].split(':')[0]: dict(zip(fileMassDictData.T[0], fileMassDictData.T[1].astype(float)))}
            dataStorage.write((datetime.datetime.now().isoformat(), MassDict), fileMassDict, jsonFormat=True)
            print('Created mass dictionary at ', fileMassDict)
        else:
            print('Could not find mass dictionary at ', fileMassDict, 'Please either obtain a mass dictionary file from mathiomica.org or provide a custom file at the above location.')
            return
    return MassDict


def ExportEnrichmentReport(data, AppendString='', OutputDirectory=None):
    """Export results from enrichment analysis to Excel spreadsheets.
    
    Parameters:
        data: dictionary
            Enrichment results

        AppendString: str, Default ""
            Custom report name, if empty then time stamp will be used

        OutputDirectory: boolean, Default None
            Path of directories where the report will be saved

    Returns:
        None

    Usage:
        ExportEnrichmentReport(goExample1, AppendString='goExample1', OutputDirectory=None)
    """

    def FlattenDataForExport--- This code section failed: ---

 L.1247         0  BUILD_MAP_0           0 
                2  STORE_FAST               'returning'

 L.1249         4  LOAD_GLOBAL              type
                6  LOAD_FAST                'data'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  LOAD_GLOBAL              dict
               12  COMPARE_OP               is
            14_16  POP_JUMP_IF_FALSE   426  'to 426'

 L.1250        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'data'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  LOAD_CONST               0
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    50  'to 50'

 L.1251        30  LOAD_GLOBAL              print
               32  LOAD_STR                 'The result is empty.'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  POP_TOP          

 L.1252        38  LOAD_FAST                'data'
               40  LOAD_FAST                'returning'
               42  LOAD_STR                 'List'
               44  STORE_SUBSCR     

 L.1253        46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            28  '28'

 L.1254        50  LOAD_FAST                'data'
               52  LOAD_GLOBAL              list
               54  LOAD_FAST                'data'
               56  LOAD_METHOD              keys
               58  CALL_METHOD_0         0  '0 positional arguments'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  BINARY_SUBSCR    
               68  STORE_FAST               'idata'

 L.1255        70  LOAD_GLOBAL              type
               72  LOAD_FAST                'idata'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  LOAD_GLOBAL              dict
               78  COMPARE_OP               is-not
               80  POP_JUMP_IF_FALSE    94  'to 94'

 L.1256        82  LOAD_FAST                'data'
               84  LOAD_FAST                'returning'
               86  LOAD_STR                 'List'
               88  STORE_SUBSCR     
            90_92  JUMP_ABSOLUTE       434  'to 434'
             94_0  COME_FROM            80  '80'

 L.1257        94  LOAD_GLOBAL              type
               96  LOAD_FAST                'idata'
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  LOAD_GLOBAL              dict
              102  COMPARE_OP               is
          104_106  POP_JUMP_IF_FALSE   434  'to 434'

 L.1258       108  LOAD_FAST                'idata'
              110  LOAD_GLOBAL              list
              112  LOAD_FAST                'idata'
              114  LOAD_METHOD              keys
              116  CALL_METHOD_0         0  '0 positional arguments'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  LOAD_CONST               0
              122  BINARY_SUBSCR    
              124  BINARY_SUBSCR    
              126  STORE_FAST               'idata'

 L.1259       128  LOAD_GLOBAL              type
              130  LOAD_FAST                'idata'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  LOAD_GLOBAL              dict
              136  COMPARE_OP               is-not
              138  POP_JUMP_IF_FALSE   148  'to 148'

 L.1260       140  LOAD_FAST                'data'
              142  STORE_FAST               'returning'
          144_146  JUMP_ABSOLUTE       434  'to 434'
            148_0  COME_FROM           138  '138'

 L.1261       148  LOAD_GLOBAL              type
              150  LOAD_FAST                'idata'
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  LOAD_GLOBAL              dict
              156  COMPARE_OP               is
          158_160  POP_JUMP_IF_FALSE   434  'to 434'

 L.1262       162  LOAD_FAST                'idata'
              164  LOAD_GLOBAL              list
              166  LOAD_FAST                'idata'
              168  LOAD_METHOD              keys
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  BINARY_SUBSCR    
              180  STORE_FAST               'idata'

 L.1263       182  LOAD_GLOBAL              type
              184  LOAD_FAST                'idata'
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  LOAD_GLOBAL              dict
              190  COMPARE_OP               is-not
          192_194  POP_JUMP_IF_FALSE   278  'to 278'

 L.1265       196  SETUP_LOOP          424  'to 424'
              198  LOAD_GLOBAL              list
              200  LOAD_FAST                'data'
              202  LOAD_METHOD              keys
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  GET_ITER         
              210  FOR_ITER            274  'to 274'
              212  STORE_FAST               'keyClass'

 L.1266       214  SETUP_LOOP          272  'to 272'
              216  LOAD_GLOBAL              list
              218  LOAD_FAST                'data'
              220  LOAD_FAST                'keyClass'
              222  BINARY_SUBSCR    
              224  LOAD_METHOD              keys
              226  CALL_METHOD_0         0  '0 positional arguments'
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  GET_ITER         
              232  FOR_ITER            270  'to 270'
              234  STORE_FAST               'keySubClass'

 L.1267       236  LOAD_FAST                'data'
              238  LOAD_FAST                'keyClass'
              240  BINARY_SUBSCR    
              242  LOAD_FAST                'keySubClass'
              244  BINARY_SUBSCR    
              246  LOAD_FAST                'returning'
              248  LOAD_GLOBAL              str
              250  LOAD_FAST                'keyClass'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  LOAD_STR                 ' '
              256  BINARY_ADD       
              258  LOAD_GLOBAL              str
              260  LOAD_FAST                'keySubClass'
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  BINARY_ADD       
              266  STORE_SUBSCR     
              268  JUMP_BACK           232  'to 232'
              270  POP_BLOCK        
            272_0  COME_FROM_LOOP      214  '214'
              272  JUMP_BACK           210  'to 210'
              274  POP_BLOCK        
              276  JUMP_FORWARD        424  'to 424'
            278_0  COME_FROM           192  '192'

 L.1268       278  LOAD_GLOBAL              type
              280  LOAD_FAST                'idata'
              282  CALL_FUNCTION_1       1  '1 positional argument'
              284  LOAD_GLOBAL              dict
              286  COMPARE_OP               is
          288_290  POP_JUMP_IF_FALSE   434  'to 434'

 L.1269       292  SETUP_LOOP          434  'to 434'
              294  LOAD_GLOBAL              list
              296  LOAD_FAST                'data'
              298  LOAD_METHOD              keys
              300  CALL_METHOD_0         0  '0 positional arguments'
              302  CALL_FUNCTION_1       1  '1 positional argument'
              304  GET_ITER         
              306  FOR_ITER            422  'to 422'
              308  STORE_FAST               'keyAnalysisType'

 L.1271       310  SETUP_LOOP          418  'to 418'
              312  LOAD_GLOBAL              list
              314  LOAD_FAST                'data'
              316  LOAD_FAST                'keyAnalysisType'
              318  BINARY_SUBSCR    
              320  LOAD_METHOD              keys
              322  CALL_METHOD_0         0  '0 positional arguments'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  GET_ITER         
              328  FOR_ITER            416  'to 416'
              330  STORE_FAST               'keyClass'

 L.1272       332  SETUP_LOOP          412  'to 412'
              334  LOAD_GLOBAL              list
              336  LOAD_FAST                'data'
              338  LOAD_FAST                'keyAnalysisType'
              340  BINARY_SUBSCR    
              342  LOAD_FAST                'keyClass'
              344  BINARY_SUBSCR    
              346  LOAD_METHOD              keys
              348  CALL_METHOD_0         0  '0 positional arguments'
              350  CALL_FUNCTION_1       1  '1 positional argument'
              352  GET_ITER         
              354  FOR_ITER            410  'to 410'
              356  STORE_FAST               'keySubClass'

 L.1273       358  LOAD_FAST                'data'
              360  LOAD_FAST                'keyAnalysisType'
              362  BINARY_SUBSCR    
              364  LOAD_FAST                'keyClass'
              366  BINARY_SUBSCR    
              368  LOAD_FAST                'keySubClass'
              370  BINARY_SUBSCR    
              372  LOAD_FAST                'returning'
              374  LOAD_GLOBAL              str
              376  LOAD_FAST                'keyAnalysisType'
              378  CALL_FUNCTION_1       1  '1 positional argument'
              380  LOAD_STR                 ' '
              382  BINARY_ADD       
              384  LOAD_GLOBAL              str
              386  LOAD_FAST                'keyClass'
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  BINARY_ADD       
              392  LOAD_STR                 ' '
              394  BINARY_ADD       
              396  LOAD_GLOBAL              str
              398  LOAD_FAST                'keySubClass'
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  BINARY_ADD       
              404  STORE_SUBSCR     
          406_408  JUMP_BACK           354  'to 354'
              410  POP_BLOCK        
            412_0  COME_FROM_LOOP      332  '332'
          412_414  JUMP_BACK           328  'to 328'
              416  POP_BLOCK        
            418_0  COME_FROM_LOOP      310  '310'
          418_420  JUMP_BACK           306  'to 306'
              422  POP_BLOCK        
            424_0  COME_FROM_LOOP      292  '292'
            424_1  COME_FROM           276  '276'
            424_2  COME_FROM_LOOP      196  '196'
              424  JUMP_FORWARD        434  'to 434'
            426_0  COME_FROM            14  '14'

 L.1275       426  LOAD_GLOBAL              print
              428  LOAD_STR                 'Results type is not supported...'
              430  CALL_FUNCTION_1       1  '1 positional argument'
              432  POP_TOP          
            434_0  COME_FROM           424  '424'
            434_1  COME_FROM           288  '288'
            434_2  COME_FROM           158  '158'
            434_3  COME_FROM           104  '104'

 L.1277       434  LOAD_FAST                'returning'
              436  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 424_2

    def ExportToFile(fileName, data):
        writer = pd.ExcelWriter(fileName)
        for key in list(data.keys()):
            keys, values = list(data[key].keys()), list(data[key].values())
            listNum = [[item for sublist in list(value)[:2] for item in sublist] for value in values]
            listNon = [list(value)[2:] for value in values]
            dataDF = [listNum[i] + listNon[i] for i in range(len(keys))]
            columns = ['p-Value', 'BH-corrected p-Value', 'Significant', 'Counts in list', 'Counts in family', 'Total members', 'Counts in members', 'Description', 'List of gene hits']
            df = pd.DataFrame(data=dataDF, index=keys, columns=columns)
            df['Significant'] = df['Significant'].map(bool)
            cleanup = lambda value: value.replace("']], ['", ' | ').replace('[', '').replace(']', '').replace("'", '').replace(', Unknown', '')
            df['List of gene hits'] = df['List of gene hits'].map(str).apply(cleanup)
            df['Description'] = df['Description'].map(str).apply(cleanup)
            df.sort_values(by='BH-corrected p-Value', inplace=True)
            df.to_excel(writer, str(key))
            writer.sheets[str(key)].set_column('A:A', df.index.astype(str).map(len).max() + 2)
            format = writer.book.add_format({'text_wrap':True,  'valign':'top'})
            for idx, column in enumerate(df.columns):
                max_len = max((df[column].astype(str).map(len).max(),
                 len(str(df[column].name)))) + 1
                width = 50 if column == 'Description' else min(180, max_len)
                writer.sheets[str(key)].set_column(idx + 1, idx + 1, width, format)

        writer.save()
        print('Saved:', fileName)

    saveDir = os.path.join(os.getcwd(), 'Enrichment reports') if OutputDirectory == None else OutputDirectory
    utilityFunctions.createDirectories(saveDir)
    if AppendString == '':
        AppendString = datetime.datetime.now().isoformat().replace(' ', '_').replace(':', '_').split('.')[0]
    ExportToFile(saveDir + AppendString + '.xlsx', FlattenDataForExport(data))


def BenjaminiHochbergFDR(pValues, SignificanceLevel=0.05):
    """HypothesisTesting BenjaminiHochbergFDR correction

    Parameters:
        pValues: 1d numpy.array
            Array of p-values

        SignificanceLevel: float, Default 0.05
            Significance level

    Returns:
        dictionary
            Corrected p-Values, p- and q-Value cuttoffs

    Usage:
        result = BenjaminiHochbergFDR(pValues)
    """
    nTests = len(pValues)
    sortedpVals = np.sort(pValues)
    sortingIDs = np.argsort(np.argsort(pValues))
    weightedpVals = sortedpVals * nTests / (1 + np.arange(nTests))
    adjustedpVals = np.array([np.min(weightedpVals[i:]) for i in range(nTests)])
    qVals = adjustedpVals[sortingIDs]
    pValqValAssociation = dict(zip(qVals, pValues))
    tempValues = np.flip(adjustedpVals)[(np.flip(adjustedpVals) <= SignificanceLevel)]
    cutoffqValue = tempValues[0] if len(tempValues) > 0 else np.nan
    if np.isnan(cutoffqValue):
        cutoffqValue = 0.0
        pValCutoff = 0.0
    else:
        pValCutoff = pValqValAssociation[cutoffqValue]
    returning = {'Results':np.vstack((pValues, qVals, qVals <= cutoffqValue)), 
     'p-Value Cutoff':pValCutoff, 
     'q-Value Cutoff':cutoffqValue}
    return returning


def ReactomeAnalysis(data, uploadURL='https://reactome.org/AnalysisService/identifiers/projection', preDownloadURL='https://reactome.org/AnalysisService/download/', postDownloadURL='/pathways/TOTAL/result.csv', headersPOST={'accept':'application/json', 
 'content-type':'text/plain'}, headersGET={'accept': 'text/plain'}, URLparameters=(('interactors', 'false'), ('pageSize', '20'), ('page', '1'), ('sortBy', 'ENTITIES_PVALUE'),
 ('order', 'ASC'), ('resource', 'TOTAL'))):
    """Reactome POST-GET-style analysis.
    
    Parameters: 
        data: pd.DataFrame or list
            Data to analyze

        uploadURL: str, Default 'https://reactome.org/AnalysisService/identifiers/projection'
            URL for POST request

        preDownloadURL: str, Default 'https://reactome.org/AnalysisService/download/'
            Part 1 of URL for GET request

        postDownloadURL: str, Default '/pathways/TOTAL/result.csv'
            Part 2 of URL for GET request

        headersPOST: dict, Default {'accept': 'application/json', 'content-type': 'text/plain'}
            URL headers for POST request

        headersGET: dict, Default {'accept': 'text/plain'}
            URL headers for GET request

        URLparameters: tuple, Default (('interactors', 'false'), ('pageSize', '20'), ('page', '1'), ('sortBy', 'ENTITIES_PVALUE'), ('order', 'ASC'), ('resource', 'TOTAL'))
            Parameters for POST request

    Returns:
        returning
            Enrichment object

    Usage:
        goExample1 = ReactomeAnalysis(["TAB1", "TNFSF13B", "MALT1", "TIRAP", "CHUK", 
                                "TNFRSF13C", "PARP1", "CSNK2A1", "CSNK2A2", "CSNK2B", "LTBR", 
                                "LYN", "MYD88", "GADD45B", "ATM", "NFKB1", "NFKB2", "NFKBIA", 
                                "IRAK4", "PIAS4", "PLAU"])
    """

    def internalQueryReactome(data):
        if type(data) is str:
            dataString = data.replace("'", '').replace('"', '')
        else:
            if type(data) is list:
                dataString = str(data).replace("'", '').replace('"', '').strip(']').strip('[')
            else:
                dataString = str(list(data)).replace("'", '').strip(']').strip('[')
        response = requests.post(uploadURL, headers=headersPOST, params=URLparameters, data=dataString)
        responseToken = response.json()['summary']['token']
        response = requests.get((preDownloadURL + responseToken + postDownloadURL), headers=headersGET)
        stream = io.StringIO(response.content.decode('utf-8'))
        enrichmentDataFrame = pd.read_csv(stream, index_col=0)
        return enrichmentDataFrame

    listToggle = False
    if type(data) is list:
        data = {'dummy': data}
        listToggle = True
    if type(data) is pd.DataFrame:
        id = list(data.index.get_level_values('id'))
        data = {'dummy': np.unique(id)}
        listToggle = True
    returning = {}
    if 'linkage' in data.keys():
        for keyGroup in sorted([item for item in list(data.keys()) if not item == 'linkage']):
            returning[keyGroup] = {}
            for keySubGroup in sorted([item for item in list(data[keyGroup].keys()) if not item == 'linkage']):
                SubGroupMultiIndex = data[keyGroup][keySubGroup]['data'].index
                SubGroupGenes = list(SubGroupMultiIndex.get_level_values('id'))
                SubGroupList = np.unique(SubGroupGenes)
                returning[keyGroup][keySubGroup] = internalQueryReactome(SubGroupList)

    else:
        for key in list(data.keys()):
            returning.update({key: internalQueryReactome(data[key])})

        returning = returning['dummy'] if listToggle else returning
    return returning


def ExportReactomeEnrichmentReport(data, AppendString='', OutputDirectory=None):
    """Export results from enrichment analysis to Excel spreadsheets.
    
    Parameters:
        data: dictionary or pandas.DataFrame
            Reactome pathway enrichment results

        AppendString: str, Default ""
            Custom report name, if empty then time stamp will be used

        OutputDirectory: boolean, Default None
            Path of directories where the report will be saved

    Returns:
        None

    Usage:
        ExportReactomeEnrichmentReport(example1, AppendString='example1', OutputDirectory=None)
    """

    def FlattenDataForExport(data):
        returning = {}
        if type(data) is pd.DataFrame:
            returning['List'] = data
        else:
            if type(data) is dict:
                idata = data[list(data.keys())[0]]
                if type(idata) is pd.DataFrame:
                    returning = data
                elif type(idata) is dict:
                    idata = idata[list(idata.keys())[0]]
                    if type(idata) is pd.DataFrame:
                        for keyClass in list(data.keys()):
                            for keySubClass in list(data[keyClass].keys()):
                                returning[str(keyClass) + ' ' + str(keySubClass)] = data[keyClass][keySubClass]

            else:
                print('Results type is not supported...')
        return returning

    def ExportToFile(fileName, data):
        writer = pd.ExcelWriter(fileName)
        for key in list(data.keys()):
            df = data[key]
            df.to_excel(writer, str(key))
            writer.sheets[str(key)].set_column('A:A', df.index.astype(str).map(len).max() + 2)
            format = writer.book.add_format({'text_wrap':True,  'valign':'top'})
            for idx, column in enumerate(df.columns):
                max_len = max((df[column].astype(str).map(len).max(),
                 len(str(df[column].name)))) + 1
                width = 50 if (column == 'Pathway name' or column == 'Found reaction identifiers') else (min(180, max_len))
                writer.sheets[str(key)].set_column(idx + 1, idx + 1, width, format)

        writer.save()
        print('Saved:', fileName)

    saveDir = os.path.join(os.getcwd(), 'Enrichment reports') if OutputDirectory == None else OutputDirectory
    utilityFunctions.createDirectories(saveDir)
    if AppendString == '':
        AppendString = datetime.datetime.now().isoformat().replace(' ', '_').replace(':', '_').split('.')[0]
    ExportToFile(os.path.join(saveDir, AppendString + '.xlsx'), FlattenDataForExport(data))