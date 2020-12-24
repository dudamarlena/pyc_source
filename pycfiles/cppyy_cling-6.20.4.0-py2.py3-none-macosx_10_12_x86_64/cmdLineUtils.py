# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wlav/wheelie/cppyy-backend/cling/builddir/install/cppyy_backend/lib/cmdLineUtils.py
# Compiled at: 2020-04-01 04:28:13
"""Contain utils for ROOT command line tools"""
from contextlib import contextmanager
import os, sys
if sys.version_info.major > 2:
    _input = input
else:
    _input = raw_input

def fileno(file_or_fd):
    """
    Look for 'fileno' attribute.
    """
    fd = getattr(file_or_fd, 'fileno', lambda : file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError('Expected a file (`.fileno()`) or a file descriptor')
    return fd


@contextmanager
def streamRedirected(source=sys.stdout, destination=os.devnull):
    """
    Redirect the output from source to destination.
    """
    stdout_fd = fileno(source)
    with os.fdopen(os.dup(stdout_fd), 'wb') as (copied):
        source.flush()
        try:
            os.dup2(fileno(destination), stdout_fd)
        except ValueError:
            with open(destination, 'wb') as (destination_file):
                os.dup2(destination_file.fileno(), stdout_fd)

        try:
            yield source
        finally:
            source.flush()
            os.dup2(copied.fileno(), stdout_fd)


def stdoutRedirected():
    """
    Redirect the output from sys.stdout to os.devnull.
    """
    return streamRedirected(sys.stdout, os.devnull)


def stderrRedirected():
    """
    Redirect the output from sys.stderr to os.devnull.
    """
    return streamRedirected(sys.stderr, os.devnull)


with stdoutRedirected():
    import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.GetVersion()
import argparse, glob, fnmatch, logging
LOG_FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT)

def _getParser(theHelp, theEpilog):
    """
   Get a commandline parser with the defaults of the commandline utils.
   """
    return argparse.ArgumentParser(description=theHelp, formatter_class=argparse.RawDescriptionHelpFormatter, epilog=theEpilog)


def getParserSingleFile(theHelp, theEpilog=''):
    """
   Get a commandline parser with the defaults of the commandline utils and a
   source file or not.
   """
    parser = _getParser(theHelp, theEpilog)
    parser.add_argument('FILE', nargs='?', help='Input file')
    return parser


def getParserFile(theHelp, theEpilog=''):
    """
   Get a commandline parser with the defaults of the commandline utils and a
   list of source files.
   """
    parser = _getParser(theHelp, theEpilog)
    parser.add_argument('FILE', nargs='+', help='Input file')
    return parser


def getParserSourceDest(theHelp, theEpilog=''):
    """
   Get a commandline parser with the defaults of the commandline utils,
   a list of source files and a destination file.
   """
    parser = _getParser(theHelp, theEpilog)
    parser.add_argument('SOURCE', nargs='+', help='Source file')
    parser.add_argument('DEST', help='Destination file')
    return parser


@contextmanager
def _setIgnoreLevel(level):
    originalLevel = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = level
    yield
    ROOT.gErrorIgnoreLevel = originalLevel


def changeDirectory(rootFile, pathSplit):
    """
    Change the current directory (ROOT.gDirectory) by the corresponding (rootFile,pathSplit)
    """
    rootFile.cd()
    for directoryName in pathSplit:
        theDir = ROOT.gDirectory.Get(directoryName)
        if not theDir:
            logging.warning('Directory %s does not exist.' % directoryName)
            return 1
        theDir.cd()

    return 0


def createDirectory(rootFile, pathSplit):
    """
    Add a directory named 'pathSplit[-1]' in (rootFile,pathSplit[:-1])
    """
    retcode = changeDirectory(rootFile, pathSplit[:-1])
    if retcode == 0:
        ROOT.gDirectory.mkdir(pathSplit[(-1)])
    return retcode


def getFromDirectory(objName):
    """
    Get the object objName from the current directory
    """
    return ROOT.gDirectory.Get(objName)


def isExisting(rootFile, pathSplit):
    """
    Return True if the object, corresponding to (rootFile,pathSplit), exits
    """
    changeDirectory(rootFile, pathSplit[:-1])
    return ROOT.gDirectory.GetListOfKeys().Contains(pathSplit[(-1)])


def isDirectoryKey(key):
    """
    Return True if the object, corresponding to the key, inherits from TDirectory
    """
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TDirectory.Class())


def isTreeKey(key):
    """
    Return True if the object, corresponding to the key, inherits from TTree
    """
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TTree.Class())


def isTHnSparseKey(key):
    """
    Return True if the object, corresponding to the key, inherits from THnSparse
    """
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.THnSparse.Class())


def getKey(rootFile, pathSplit):
    """
    Get the key of the corresponding object (rootFile,pathSplit)
    """
    changeDirectory(rootFile, pathSplit[:-1])
    return ROOT.gDirectory.GetKey(pathSplit[(-1)])


def isDirectory(rootFile, pathSplit):
    """
    Return True if the object, corresponding to (rootFile,pathSplit), inherits from TDirectory
    """
    if pathSplit == []:
        return True
    else:
        return isDirectoryKey(getKey(rootFile, pathSplit))


def isTree(rootFile, pathSplit):
    """
    Return True if the object, corresponding to (rootFile,pathSplit), inherits from TTree
    """
    if pathSplit == []:
        return False
    else:
        return isTreeKey(getKey(rootFile, pathSplit))


def getKeyList(rootFile, pathSplit):
    """
    Get the list of keys of the directory (rootFile,pathSplit),
    if (rootFile,pathSplit) is not a directory then get the key in a list
    """
    if isDirectory(rootFile, pathSplit):
        changeDirectory(rootFile, pathSplit)
        return ROOT.gDirectory.GetListOfKeys()
    else:
        return [
         getKey(rootFile, pathSplit)]


def keyListSort(keyList):
    """
    Sort list of keys by their names ignoring the case
    """
    keyList.sort(key=lambda x: x.GetName().lower())


def tupleListSort(tupleList):
    """
    Sort list of tuples by their first elements ignoring the case
    """
    tupleList.sort(key=lambda x: x[0].lower())


def dirListSort(dirList):
    """
    Sort list of directories by their names ignoring the case
    """
    dirList.sort(key=lambda x: [ n.lower() for n in x ])


def keyClassSpliter(rootFile, pathSplitList):
    """
    Return a list of directories and a list of keys corresponding
    to the other objects, for rootLs and rooprint use
    """
    keyList = []
    dirList = []
    for pathSplit in pathSplitList:
        if pathSplit == []:
            dirList.append(pathSplit)
        elif isDirectory(rootFile, pathSplit):
            dirList.append(pathSplit)
        else:
            keyList.append(getKey(rootFile, pathSplit))

    keyListSort(keyList)
    dirListSort(dirList)
    return (keyList, dirList)


def openROOTFile(fileName, mode='read'):
    """
    Open the ROOT file corresponding to fileName in the corresponding mode,
    redirecting the output not to see missing dictionnaries

    Returns:
        theFile (TFile)
    """
    with _setIgnoreLevel(ROOT.kError):
        theFile = ROOT.TFile.Open(fileName, mode)
    if not theFile:
        logging.warning('File %s does not exist', fileName)
    return theFile


def openROOTFileCompress(fileName, compress, recreate):
    """
    Open a ROOT file (like openROOTFile) with the possibility
    to change compression settings
    """
    if compress != None and os.path.isfile(fileName):
        logging.warning("can't change compression settings on existing file")
        return
    else:
        mode = 'recreate' if recreate else 'update'
        theFile = openROOTFile(fileName, mode)
        if compress != None:
            theFile.SetCompressionSettings(compress)
        return theFile


def joinPathSplit(pathSplit):
    """
    Join the pathSplit with '/'
    """
    return ('/').join(pathSplit)


MANY_OCCURENCE_WARNING = "Several versions of '{0}' are present in '{1}'. Only the most recent will be considered."

def manyOccurenceRemove(pathSplitList, fileName):
    """
    Search for double occurence of the same pathSplit and remove them
    """
    if len(pathSplitList) > 1:
        for n in pathSplitList:
            if pathSplitList.count(n) != 1:
                logging.warning(MANY_OCCURENCE_WARNING.format(joinPathSplit(n), fileName))
                while n in pathSplitList:
                    pathSplitList.remove(n)


def patternToPathSplitList(fileName, pattern):
    """
    Get the list of pathSplit of objects in the ROOT file
    corresponding to fileName that match with the pattern
    """
    rootFile = openROOTFile(fileName)
    if not rootFile:
        return []
    patternSplit = [ n for n in pattern.split('/') if n != '' ]
    pathSplitList = [[]]
    for patternPiece in patternSplit:
        newPathSplitList = []
        for pathSplit in pathSplitList:
            if isDirectory(rootFile, pathSplit):
                changeDirectory(rootFile, pathSplit)
                newPathSplitList.extend([ pathSplit + [key.GetName()] for key in ROOT.gDirectory.GetListOfKeys() if fnmatch.fnmatch(key.GetName(), patternPiece)
                                        ])

        pathSplitList = newPathSplitList

    if pathSplitList == []:
        logging.warning(("can't find {0} in {1}").format(pattern, fileName))
    manyOccurenceRemove(pathSplitList, fileName)
    return pathSplitList


def fileNameListMatch(filePattern, wildcards):
    """
    Get the list of fileName that match with objPattern
    """
    if wildcards:
        return [ os.path.expandvars(os.path.expanduser(i)) for i in glob.iglob(filePattern) ]
    else:
        return [
         os.path.expandvars(os.path.expanduser(filePattern))]


def pathSplitListMatch(fileName, objPattern, wildcards):
    """
    Get the list of pathSplit that match with objPattern
    """
    if wildcards:
        return patternToPathSplitList(fileName, objPattern)
    else:
        return [[ n for n in objPattern.split('/') if n != '' ]]


def patternToFileNameAndPathSplitList(pattern, wildcards=True):
    """
    Get the list of tuple containing both :
    - ROOT file name
    - list of splited path (in the corresponding file) of objects that matche
    Use unix wildcards by default
    """
    rootFilePattern = '*.root'
    rootObjPattern = rootFilePattern + ':*'
    httpRootFilePattern = 'htt*://*.root'
    httpRootObjPattern = httpRootFilePattern + ':*'
    xrootdRootFilePattern = 'root://*.root'
    xrootdRootObjPattern = xrootdRootFilePattern + ':*'
    s3RootFilePattern = 's3://*.root'
    s3RootObjPattern = s3RootFilePattern + ':*'
    gsRootFilePattern = 'gs://*.root'
    gsRootObjPattern = gsRootFilePattern + ':*'
    pcmFilePattern = '*.pcm'
    pcmObjPattern = pcmFilePattern + ':*'
    if fnmatch.fnmatch(pattern, httpRootObjPattern) or fnmatch.fnmatch(pattern, xrootdRootObjPattern) or fnmatch.fnmatch(pattern, s3RootObjPattern) or fnmatch.fnmatch(pattern, gsRootObjPattern):
        patternSplit = pattern.rsplit(':', 1)
        fileName = patternSplit[0]
        objPattern = patternSplit[1]
        pathSplitList = pathSplitListMatch(fileName, objPattern, wildcards)
        return [
         (
          fileName, pathSplitList)]
    if fnmatch.fnmatch(pattern, httpRootFilePattern) or fnmatch.fnmatch(pattern, xrootdRootFilePattern) or fnmatch.fnmatch(pattern, s3RootFilePattern) or fnmatch.fnmatch(pattern, gsRootFilePattern):
        fileName = pattern
        pathSplitList = [[]]
        return [
         (
          fileName, pathSplitList)]
    if fnmatch.fnmatch(pattern, rootObjPattern) or fnmatch.fnmatch(pattern, pcmObjPattern):
        patternSplit = pattern.split(':')
        filePattern = patternSplit[0]
        objPattern = patternSplit[1]
        fileNameList = fileNameListMatch(filePattern, wildcards)
        return [ (fileName, pathSplitListMatch(fileName, objPattern, wildcards)) for fileName in fileNameList ]
    if fnmatch.fnmatch(pattern, rootFilePattern) or fnmatch.fnmatch(pattern, pcmFilePattern):
        filePattern = pattern
        fileNameList = fileNameListMatch(filePattern, wildcards)
        pathSplitList = [[]]
        return [ (fileName, pathSplitList) for fileName in fileNameList ]
    logging.warning(('{0}: No such file (or extension not supported)').format(pattern))
    return []


def getArgs(parser):
    """
   Get arguments corresponding to parser.
   """
    return parser.parse_args()


def getSourceListArgs(parser, wildcards=True):
    """
   Create a list of tuples that contain source ROOT file names
   and lists of path in these files as well as the original arguments
   """
    args = getArgs(parser)
    inputFiles = []
    try:
        inputFiles = args.FILE
    except:
        inputFiles = args.SOURCE

    sourceList = [ tup for pattern in inputFiles for tup in patternToFileNameAndPathSplitList(pattern, wildcards)
                 ]
    return (sourceList, args)


def getSourceListOptDict(parser, wildcards=True):
    """
    Get the list of tuples and the dictionary with options

    returns:
        sourceList: a list of tuples with one list element per file
                    the first tuple entry being the root file,
                    the second a list of subdirectories,
                        each being represented as a list itself with a string per level
                    e.g.
                    rootls tutorial/tmva/TMVA.root:Method_BDT/BDT turns into
                    [('tutorials/tmva/TMVA.root', [['Method_BDT','BDT']])]
        vars(args): a dictionary of matched options, e.g.
                    {'longListing': False,
                     'oneColumn': False,
                     'treeListing': False,
                     'FILE': ['tutorials/tmva/TMVA.root:Method_BDT/BDT']
                     }
    """
    sourceList, args = getSourceListArgs(parser, wildcards)
    if sourceList == []:
        logging.error('Input file(s) not found!')
    return (
     sourceList, vars(args))


def getSourceDestListOptDict(parser, wildcards=True):
    """
    Get the list of tuples of sources, create destination name, destination pathSplit
    and the dictionary with options
    """
    sourceList, args = getSourceListArgs(parser, wildcards)
    destList = patternToFileNameAndPathSplitList(args.DEST, wildcards=False)
    if destList != []:
        destFileName, destPathSplitList = destList[0]
        destPathSplit = destPathSplitList[0]
    else:
        destFileName = ''
        destPathSplit = []
    return (
     sourceList, destFileName, destPathSplit, vars(args))


TARGET_ERROR = "target '{0}' is not a directory"
OMITTING_ERROR = "omitting {0} '{1}'. Did you forget to specify the -r option for a recursive copy?"
OVERWRITE_ERROR = "cannot overwrite non-directory '{0}' with directory '{1}'"

def copyRootObject(sourceFile, sourcePathSplit, destFile, destPathSplit, oneSource, recursive, replace):
    """
    Initialize the recursive function 'copyRootObjectRecursive', written to be as unix-like as possible
    """
    retcode = 0
    isMultipleInput = not (oneSource and sourcePathSplit != [])
    recursiveOption = recursive
    if isMultipleInput and destPathSplit != [] and not (isExisting(destFile, destPathSplit) and isDirectory(destFile, destPathSplit)):
        logging.warning(TARGET_ERROR.format(destPathSplit[(-1)]))
        retcode += 1
    if not recursiveOption:
        if sourcePathSplit == []:
            logging.warning(OMITTING_ERROR.format('file', sourceFile.GetName()))
            retcode += 1
        elif isDirectory(sourceFile, sourcePathSplit):
            logging.warning(OMITTING_DIRECTORY_ERROR.format('directory', sourcePathSplit[(-1)]))
            retcode += 1
    if sourcePathSplit == []:
        retcode += copyRootObjectRecursive(sourceFile, sourcePathSplit, destFile, destPathSplit, replace)
    else:
        setName = ''
        if not isMultipleInput and destPathSplit != [] and not isExisting(destFile, destPathSplit):
            setName = destPathSplit[(-1)]
        objectName = sourcePathSplit[(-1)]
        if isDirectory(sourceFile, sourcePathSplit):
            if setName != '':
                createDirectory(destFile, destPathSplit[:-1] + [setName])
                retcode += copyRootObjectRecursive(sourceFile, sourcePathSplit, destFile, destPathSplit[:-1] + [setName], replace)
            elif isDirectory(destFile, destPathSplit):
                if not isExisting(destFile, destPathSplit + [objectName]):
                    createDirectory(destFile, destPathSplit + [objectName])
                if isDirectory(destFile, destPathSplit + [objectName]):
                    retcode += copyRootObjectRecursive(sourceFile, sourcePathSplit, destFile, destPathSplit + [objectName], replace)
                else:
                    logging.warning(OVERWRITE_ERROR.format(objectName, objectName))
                    retcode += 1
            else:
                logging.warning(OVERWRITE_ERROR.format(destPathSplit[(-1)], objectName))
                retcode += 1
        elif setName != '':
            retcode += copyRootObjectRecursive(sourceFile, sourcePathSplit, destFile, destPathSplit[:-1], replace, setName)
        elif isDirectory(destFile, destPathSplit):
            retcode += copyRootObjectRecursive(sourceFile, sourcePathSplit, destFile, destPathSplit, replace)
        else:
            setName = destPathSplit[(-1)]
            retcode += copyRootObjectRecursive(sourceFile, sourcePathSplit, destFile, destPathSplit[:-1], replace, setName)
    return retcode


DELETE_ERROR = 'object {0} was not existing, so it is not deleted'

def deleteObject(rootFile, pathSplit):
    """
    Delete the object 'pathSplit[-1]' from (rootFile,pathSplit[:-1])
    """
    retcode = changeDirectory(rootFile, pathSplit[:-1])
    if retcode == 0:
        fileName = pathSplit[(-1)]
        if isExisting(rootFile, pathSplit):
            ROOT.gDirectory.Delete(fileName + ';*')
        else:
            logging.warning(DELETE_ERROR.format(fileName))
            retcode += 1
    return retcode


def copyRootObjectRecursive(sourceFile, sourcePathSplit, destFile, destPathSplit, replace, setName=''):
    """
    Copy objects from a file or directory (sourceFile,sourcePathSplit)
    to an other file or directory (destFile,destPathSplit)
    - Has the will to be unix-like
    - that's a recursive function
    - Python adaptation of a root input/output tutorial :
      $ROOTSYS/tutorials/io/copyFiles.C
    """
    retcode = 0
    replaceOption = replace
    seen = {}
    for key in getKeyList(sourceFile, sourcePathSplit):
        objectName = key.GetName()
        if objectName not in seen.keys():
            seen[objectName] = key
        elif seen[objectName].GetCycle() < key.GetCycle():
            seen[objectName] = key
        else:
            continue
        if isDirectoryKey(key):
            if not isExisting(destFile, destPathSplit + [objectName]):
                createDirectory(destFile, destPathSplit + [objectName])
            if isDirectory(destFile, destPathSplit + [objectName]):
                retcode += copyRootObjectRecursive(sourceFile, sourcePathSplit + [objectName], destFile, destPathSplit + [objectName], replace)
            else:
                logging.warning(OVERWRITE_ERROR.format(objectName, objectName))
                retcode += 1
        elif isTreeKey(key):
            T = key.GetMotherDir().Get(objectName + ';' + str(key.GetCycle()))
            if replaceOption and isExisting(destFile, destPathSplit + [T.GetName()]):
                retcodeTemp = deleteObject(destFile, destPathSplit + [T.GetName()])
                if retcodeTemp:
                    retcode += retcodeTemp
                    continue
            changeDirectory(destFile, destPathSplit)
            newT = T.CloneTree(-1, 'fast')
            if setName != '':
                newT.SetName(setName)
            newT.Write()
        else:
            obj = key.ReadObj()
            if replaceOption and isExisting(destFile, destPathSplit + [setName]):
                changeDirectory(destFile, destPathSplit)
                otherObj = getFromDirectory(setName)
                if not otherObj == obj:
                    retcodeTemp = deleteObject(destFile, destPathSplit + [setName])
                    if retcodeTemp:
                        retcode += retcodeTemp
                        continue
                    else:
                        obj.SetName(setName)
                        changeDirectory(destFile, destPathSplit)
                        obj.Write()
                else:
                    obj.SetName(setName)
                    changeDirectory(destFile, destPathSplit)
                    obj.Write()
            elif issubclass(obj.__class__, ROOT.TCollection):
                changeDirectory(destFile, destPathSplit)
                obj.Write(setName, ROOT.TObject.kSingleKey)
            else:
                if setName != '':
                    obj.SetName(setName)
                else:
                    obj.SetName(objectName)
                changeDirectory(destFile, destPathSplit)
                obj.Write()
            obj.Delete()

    changeDirectory(destFile, destPathSplit)
    ROOT.gDirectory.SaveSelf(ROOT.kTRUE)
    return retcode


FILE_REMOVE_ERROR = "cannot remove '{0}': Is a ROOT file"
DIRECTORY_REMOVE_ERROR = "cannot remove '{0}': Is a directory"
ASK_FILE_REMOVE = "remove '{0}' ? (y/n) : "
ASK_OBJECT_REMOVE = "remove '{0}' from '{1}' ? (y/n) : "

def deleteRootObject(rootFile, pathSplit, interactive, recursive):
    """
    Remove the object (rootFile,pathSplit)
    -interactive : prompt before every removal
    -recursive : allow directory, and ROOT file, removal
    """
    retcode = 0
    if not recursive and isDirectory(rootFile, pathSplit):
        if pathSplit == []:
            logging.warning(FILE_REMOVE_ERROR.format(rootFile.GetName()))
            retcode += 1
        else:
            logging.warning(DIRECTORY_REMOVE_ERROR.format(pathSplit[(-1)]))
            retcode += 1
    else:
        if interactive:
            if pathSplit != []:
                answer = _input(ASK_OBJECT_REMOVE.format(('/').join(pathSplit), rootFile.GetName()))
            else:
                answer = _input(ASK_FILE_REMOVE.format(rootFile.GetName()))
            remove = answer.lower() == 'y'
        else:
            remove = True
        if remove:
            if pathSplit != []:
                retcode += deleteObject(rootFile, pathSplit)
            else:
                rootFile.Close()
                os.remove(rootFile.GetName())
    return retcode


SOURCE_HELP = 'path of the source.'
SOURCES_HELP = 'path of the source(s).'
DEST_HELP = 'path of the destination.'
COMPRESS_HELP = 'change the compression settings of the\ndestination file (if not already existing).'
INTERACTIVE_HELP = 'prompt before every removal.'
RECREATE_HELP = 'recreate the destination file.'
RECURSIVE_HELP = 'recurse inside directories'
REPLACE_HELP = 'replace object if already existing'

def _openBrowser(rootFile=None):
    browser = ROOT.TBrowser()
    _input('Press enter to exit.')


def rootBrowse(fileName=None):
    if fileName:
        rootFile = openROOTFile(fileName)
        if not rootFile:
            return 1
        _openBrowser(rootFile)
        rootFile.Close()
    else:
        _openBrowser()
    return 0


def _copyObjects(fileName, pathSplitList, destFile, destPathSplit, oneFile, recursive, replace):
    retcode = 0
    destFileName = destFile.GetName()
    rootFile = openROOTFile(fileName) if fileName != destFileName else destFile
    if not rootFile:
        return 1
    ROOT.gROOT.GetListOfFiles().Remove(rootFile)
    for pathSplit in pathSplitList:
        oneSource = oneFile and len(pathSplitList) == 1
        retcode += copyRootObject(rootFile, pathSplit, destFile, destPathSplit, oneSource, recursive, replace)

    if fileName != destFileName:
        rootFile.Close()
    return retcode


def rootCp(sourceList, destFileName, destPathSplit, compress=None, recreate=False, recursive=False, replace=False):
    if sourceList == [] or destFileName == '':
        return 1
    if recreate and destFileName in [ n[0] for n in sourceList ]:
        logging.error('cannot recreate destination file if this is also a source file')
        return 1
    destFile = openROOTFileCompress(destFileName, compress, recreate)
    if not destFile:
        return 1
    ROOT.gROOT.GetListOfFiles().Remove(destFile)
    retcode = 0
    for fileName, pathSplitList in sourceList:
        retcode += _copyObjects(fileName, pathSplitList, destFile, destPathSplit, len(sourceList) == 1, recursive, replace)

    destFile.Close()
    return retcode


def _setBranchStatus(tree, branchSelectionString, status=0):
    """This is used by _copyTreeSubset() to turn on/off branches"""
    for branchToModify in branchSelectionString.split(','):
        logging.info('Setting branch status to %d for %s' % (status, branchToModify))
        tree.SetBranchStatus(branchToModify, status)

    return tree


def _copyTreeSubset(sourceFile, sourcePathSplit, destFile, destPathSplit, firstEvent, lastEvent, selectionString, branchinclude, branchexclude):
    """Copy a subset of the tree from (sourceFile,sourcePathSplit)
    to (destFile,destPathSplit) according to options in optDict"""
    retcode = changeDirectory(sourceFile, sourcePathSplit[:-1])
    if retcode != 0:
        return retcode
    bigTree = getFromDirectory(sourcePathSplit[(-1)])
    nbrEntries = bigTree.GetEntries()
    retcode = changeDirectory(destFile, destPathSplit)
    if retcode != 0:
        return retcode
    if lastEvent == -1:
        lastEvent = nbrEntries - 1
    numberOfEntries = lastEvent - firstEvent + 1
    outputTree = bigTree
    if branchexclude:
        _setBranchStatus(outputTree, branchexclude, 0)
    if branchinclude:
        _setBranchStatus(outputTree, branchinclude, 1)
    if branchexclude or branchinclude:
        outputTree = outputTree.CloneTree()
    outputTree = outputTree.CopyTree(selectionString, '', numberOfEntries, firstEvent)
    outputTree.Write()
    return retcode


def _copyTreeSubsets(fileName, pathSplitList, destFile, destPathSplit, first, last, selectionString, branchinclude, branchexclude):
    retcode = 0
    destFileName = destFile.GetName()
    rootFile = openROOTFile(fileName) if fileName != destFileName else destFile
    if not rootFile:
        return 1
    for pathSplit in pathSplitList:
        if isTree(rootFile, pathSplit):
            retcode += _copyTreeSubset(rootFile, pathSplit, destFile, destPathSplit, first, last, selectionString, branchinclude, branchexclude)

    if fileName != destFileName:
        rootFile.Close()
    return retcode


def rootEventselector(sourceList, destFileName, destPathSplit, compress=None, recreate=False, first=0, last=-1, selectionString='', branchinclude='', branchexclude=''):
    if sourceList == [] or destFileName == '':
        return 1
    if recreate and destFileName in sourceList:
        logging.error('cannot recreate destination file if this is also a source file')
        return 1
    destFile = openROOTFileCompress(destFileName, compress, recreate)
    if not destFile:
        return 1
    retcode = 0
    for fileName, pathSplitList in sourceList:
        retcode += _copyTreeSubsets(fileName, pathSplitList, destFile, destPathSplit, first, last, selectionString, branchinclude, branchexclude)

    destFile.Close()
    return retcode


ANSI_BOLD = '\x1b[1m'
ANSI_BLUE = '\x1b[34m'
ANSI_GREEN = '\x1b[32m'
ANSI_END = '\x1b[0m'
ANSI_BOLD_LENGTH = len(ANSI_BOLD + ANSI_END)
ANSI_BLUE_LENGTH = len(ANSI_BLUE + ANSI_END)
ANSI_GREEN_LENGTH = len(ANSI_GREEN + ANSI_END)
IS_TERMINAL = sys.stdout.isatty()
IS_WIN32 = sys.platform == 'win32'

def isSpecial(ansiCode, string):
    """Use ansi code on 'string' if the output is the
    terminal of a not Windows platform"""
    if IS_TERMINAL and not IS_WIN32:
        return ansiCode + string + ANSI_END
    else:
        return string


def write(string, indent=0, end=''):
    """Use sys.stdout.write to write the string with an indentation
    equal to indent and specifying the end character"""
    sys.stdout.write(' ' * indent + string + end)


TREE_TEMPLATE = '{0:{nameWidth}}' + '{1:{titleWidth}}{2:{memoryWidth}}'

def _recursifTreePrinter(tree, indent):
    """Print recursively tree informations"""
    listOfBranches = tree.GetListOfBranches()
    if len(listOfBranches) > 0:
        maxCharName = max([ len(branch.GetName()) for branch in listOfBranches
                          ])
        maxCharTitle = max([ len(branch.GetTitle()) for branch in listOfBranches
                           ])
        dic = {'nameWidth': maxCharName + 2, 
           'titleWidth': maxCharTitle + 4, 
           'memoryWidth': 1}
    for branch in listOfBranches:
        rec = [
         branch.GetName(),
         '"' + branch.GetTitle() + '"',
         str(branch.GetTotBytes())]
        write(TREE_TEMPLATE.format(*rec, **dic), indent, end='\n')
        _recursifTreePrinter(branch, indent + 2)

    write('')


def _prepareTime(time):
    """Get time in the proper shape
    ex : 174512 for 17h 45m 12s
    ex : 094023 for 09h 40m 23s"""
    time = str(time)
    time = '000000' + time
    time = time[len(time) - 6:]
    return time


MONTH = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 
   8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
LONG_TEMPLATE = isSpecial(ANSI_BOLD, '{0:{classWidth}}') + '{1:{timeWidth}}' + '{2:{nameWidth}}{3:{titleWidth}}'

def _printClusters(tree, indent):
    clusterStart = 0
    nTotClusters = 0
    clusterIter = tree.GetClusterIterator(0)
    clusterStart = clusterIter()
    write(isSpecial(ANSI_BOLD, 'Cluster INCLUSIVE ranges:\n'), indent)
    while clusterStart < tree.GetEntries():
        clustLine = ' - # %d: [%d, %d]\n' % (
         nTotClusters, clusterStart, clusterIter.GetNextEntry() - 1)
        write(clustLine, indent)
        nTotClusters += 1
        clusterStart = clusterIter()

    write(isSpecial(ANSI_BOLD, 'The total number of clusters is %d\n' % nTotClusters), indent)


def _rootLsPrintLongLs(keyList, indent, treeListing):
    """Print a list of Tkey in columns
    pattern : classname, datetime, name and title"""
    if len(keyList) > 0:
        maxCharClass = max([ len(key.GetClassName()) for key in keyList ])
        maxCharTime = 12
        maxCharName = max([ len(key.GetName()) for key in keyList ])
        dic = {'classWidth': maxCharClass + 2, 
           'timeWidth': maxCharTime + 2, 
           'nameWidth': maxCharName + 2, 
           'titleWidth': 1}
    for key in keyList:
        datime = key.GetDatime()
        time = datime.GetTime()
        date = datime.GetDate()
        year = datime.GetYear()
        time = _prepareTime(time)
        rec = [
         key.GetClassName(),
         MONTH[int(str(date)[4:6])] + ' ' + str(date)[6:] + ' ' + time[:2] + ':' + time[2:4] + ' ' + str(year) + ' ',
         key.GetName(),
         '"' + key.GetTitle() + '"']
        write(LONG_TEMPLATE.format(*rec, **dic), indent, end='\n')
        if treeListing and isTreeKey(key):
            tree = key.ReadObj()
            _recursifTreePrinter(tree, indent + 2)
            tree = tree.GetTree()
            _printClusters(tree, indent + 2)
        if treeListing and isTHnSparseKey(key):
            hs = key.ReadObj()
            hs.Print('all')


import os, shlex, struct, platform, subprocess

def getTerminalSize():
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,windows,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python"""
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
    if current_os in ('Linux', 'Darwin') or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        tuple_xy = (80, 25)
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy = struct.unpack('hhhhHhhhhhh', csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return (
             sizex, sizey)
    except:
        pass


def _get_terminal_size_tput():
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_terminal_size_linux():

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass

    if not cr:
        try:
            cr = (
             os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return

    return (
     int(cr[1]), int(cr[0]))


def _rootLsPrintSimpleLs(keyList, indent, oneColumn):
    """Print list of strings in columns
    - blue for directories
    - green for trees"""
    if len(keyList) == 0:
        return
    term_width, term_height = getTerminalSize()
    term_width = term_width - indent
    min_chars_between = 2
    min_element_width = min(len(key.GetName()) for key in keyList) + min_chars_between
    max_element_width = max(len(key.GetName()) for key in keyList) + min_chars_between
    if max_element_width >= term_width:
        ncol, col_widths = 1, [1]
    else:
        ncol = 1 if oneColumn else min(len(keyList), term_width // min_element_width)
        while True:
            col_widths = [ max(len(key.GetName()) + min_chars_between for j, key in enumerate(keyList) if j % ncol == i) for i in range(ncol)
                         ]
            if sum(col_widths) <= term_width:
                break
            else:
                ncol -= 1

        for i, key in enumerate(keyList):
            if i % ncol == 0:
                write('', indent)
            if (i + 1) % ncol != 0 and i != len(keyList) - 1:
                if not IS_TERMINAL:
                    write(key.GetName().ljust(col_widths[(i % ncol)]))
                elif isDirectoryKey(keyList[i]):
                    write(isSpecial(ANSI_BLUE, key.GetName()).ljust(col_widths[(i % ncol)] + ANSI_BLUE_LENGTH))
                elif isTreeKey(keyList[i]):
                    write(isSpecial(ANSI_GREEN, key.GetName()).ljust(col_widths[(i % ncol)] + ANSI_GREEN_LENGTH))
                else:
                    write(key.GetName().ljust(col_widths[(i % ncol)]))
            else:
                if not IS_TERMINAL:
                    write(key.GetName())
                elif isDirectoryKey(keyList[i]):
                    write(isSpecial(ANSI_BLUE, key.GetName()))
                elif isTreeKey(keyList[i]):
                    write(isSpecial(ANSI_GREEN, key.GetName()))
                else:
                    write(key.GetName())
                write('\n')


def _rootLsPrint(keyList, indent, oneColumn, longListing, treeListing):
    """Print informations given by keyList with a rootLs
    style chosen with the options"""
    if longListing or treeListing:
        _rootLsPrintLongLs(keyList, indent, treeListing)
    else:
        _rootLsPrintSimpleLs(keyList, indent, oneColumn)


def _rootLsProcessFile(fileName, pathSplitList, manySources, indent, oneColumn, longListing, treeListing):
    """rootls main routine for one file looping over paths in the file

    sorts out directories and key, and loops over all paths, then forwards to
    (_rootLsPrintLongLs or _rootLsPrintSimpleLs) - split in _rootLsPrint

    args:
       oneColumn   (bool):
       longListing (bool):
       treeListing (bool):
       indent       (int): how many columns the printout should be indented globally
       manySources (bool): if more than one file is printed
       fileName     (str): the root file name
       pathSplitList: a list of subdirectories,
                       each being represented as a list itself with a string per level
                       e.g.
                       [['Method_BDT','BDT']]
    Returns:
        retcode (int): 0 in case of success, 1 if the file could not be opened
    """
    retcode = 0
    rootFile = openROOTFile(fileName)
    if not rootFile:
        return 1
    keyList, dirList = keyClassSpliter(rootFile, pathSplitList)
    if manySources:
        write(('{0} :').format(fileName) + '\n')
    _rootLsPrint(keyList, indent, oneColumn, longListing, treeListing)
    manyPathSplits = len(pathSplitList) > 1
    indentDir = 2 if manyPathSplits else 0
    for pathSplit in dirList:
        keyList = getKeyList(rootFile, pathSplit)
        keyListSort(keyList)
        if manyPathSplits:
            write(('{0} :').format(('/').join(pathSplit)), indent, end='\n')
        _rootLsPrint(keyList, indent + indentDir, oneColumn, longListing, treeListing)

    rootFile.Close()
    return retcode


def rootLs(sourceList, oneColumn=False, longListing=False, treeListing=False):
    """rootls main routine for an arbitrary number of files

    args:
       oneColumn   (bool):
       longListing (bool):
       treeListing (bool):
       sourceList: a list of tuples with one list element per file
                   the first tuple entry being the root file,
                   the second a list of subdirectories,
                       each being represented as a list itself with a string per level
                   e.g.
                   rootls tutorial/tmva/TMVA.root:Method_BDT/BDT turns into
                   [('tutorials/tmva/TMVA.root', [['Method_BDT','BDT']])]

    returns:
       retcode (int): 0 in case of success
    """
    if sourceList == []:
        return 1
    tupleListSort(sourceList)
    retcode = 0
    manySources = len(sourceList) > 1
    indent = 2 if manySources else 0
    for fileName, pathSplitList in sourceList:
        retcode += _rootLsProcessFile(fileName, pathSplitList, manySources, indent, oneColumn, longListing, treeListing)

    return retcode


MKDIR_ERROR = "cannot create directory '{0}'"

def _createDirectories(rootFile, pathSplit, parents):
    """Same behaviour as createDirectory but allows the possibility
    to build an whole path recursively with the option "parents" """
    retcode = 0
    lenPathSplit = len(pathSplit)
    if lenPathSplit == 0:
        pass
    elif parents:
        for i in range(lenPathSplit):
            currentPathSplit = pathSplit[:i + 1]
            if not (isExisting(rootFile, currentPathSplit) and isDirectory(rootFile, currentPathSplit)):
                retcode += createDirectory(rootFile, currentPathSplit)

    else:
        doMkdir = True
        for i in range(lenPathSplit - 1):
            currentPathSplit = pathSplit[:i + 1]
            if not (isExisting(rootFile, currentPathSplit) and isDirectory(rootFile, currentPathSplit)):
                doMkdir = False
                break

        if doMkdir:
            retcode += createDirectory(rootFile, pathSplit)
        else:
            logging.warning(MKDIR_ERROR.format(('/').join(pathSplit)))
            retcode += 1
    return retcode


def _rootMkdirProcessFile(fileName, pathSplitList, parents):
    retcode = 0
    rootFile = openROOTFile(fileName, 'update')
    if not rootFile:
        return 1
    for pathSplit in pathSplitList:
        retcode += _createDirectories(rootFile, pathSplit, parents)

    rootFile.Close()
    return retcode


def rootMkdir(sourceList, parents=False):
    if sourceList == []:
        return 1
    retcode = 0
    for fileName, pathSplitList in sourceList:
        retcode += _rootMkdirProcessFile(fileName, pathSplitList, parents)

    return retcode


MOVE_ERROR = 'error during copy of {0}, it is not removed from {1}'

def _moveObjects(fileName, pathSplitList, destFile, destPathSplit, oneFile, interactive):
    retcode = 0
    recursive = True
    replace = True
    destFileName = destFile.GetName()
    rootFile = openROOTFile(fileName, 'update') if fileName != destFileName else destFile
    if not rootFile:
        return 1
    ROOT.gROOT.GetListOfFiles().Remove(rootFile)
    for pathSplit in pathSplitList:
        oneSource = oneFile and len(pathSplitList) == 1
        retcodeTemp = copyRootObject(rootFile, pathSplit, destFile, destPathSplit, oneSource, recursive, replace)
        if not retcodeTemp:
            retcode += deleteRootObject(rootFile, pathSplit, interactive, recursive)
        else:
            logging.warning(MOVE_ERROR.format(('/').join(pathSplit), rootFile.GetName()))
            retcode += retcodeTemp

    if fileName != destFileName:
        rootFile.Close()
    return retcode


def rootMv(sourceList, destFileName, destPathSplit, compress=None, interactive=False, recreate=False):
    if sourceList == [] or destFileName == '':
        return 1
    if recreate and destFileName in sourceList:
        logging.error('cannot recreate destination file if this is also a source file')
        return 1
    destFile = openROOTFileCompress(destFileName, compress, recreate)
    if not destFile:
        return 1
    ROOT.gROOT.GetListOfFiles().Remove(destFile)
    retcode = 0
    for fileName, pathSplitList in sourceList:
        retcode += _moveObjects(fileName, pathSplitList, destFile, destPathSplit, len(sourceList) == 1, interactive)

    destFile.Close()
    return retcode


def _keyListExtended(rootFile, pathSplitList):
    keyList, dirList = keyClassSpliter(rootFile, pathSplitList)
    for pathSplit in dirList:
        keyList.extend(getKeyList(rootFile, pathSplit))

    keyList = [ key for key in keyList if not isDirectoryKey(key) ]
    keyListSort(keyList)
    return keyList


def rootPrint(sourceList, directoryOption=None, divideOption=None, drawOption='', formatOption=None, outputOption=None, sizeOption=None, styleOption=None, verboseOption=False):
    if sourceList == []:
        return 1
    tupleListSort(sourceList)
    ROOT.gROOT.SetBatch()
    if styleOption:
        ROOT.gInterpreter.ProcessLine(('.x {0}').format(styleOption))
    if not verboseOption:
        ROOT.gErrorIgnoreLevel = 9999
    if sizeOption:
        try:
            width, height = sizeOption.split('x')
            width = int(width)
            height = int(height)
        except ValueError:
            logging.warning('canvas size is on a wrong format')
            return 1

        canvas = ROOT.TCanvas('canvas', 'canvas', width, height)
    else:
        canvas = ROOT.TCanvas('canvas')
    if divideOption:
        try:
            x, y = divideOption.split(',')
            x = int(x)
            y = int(y)
        except ValueError:
            logging.warning('divide is on a wrong format')
            return 1

        canvas.Divide(x, y)
        caseNumber = x * y
    if not formatOption and outputOption:
        fileName = outputOption
        fileFormat = fileName.split('.')[(-1)]
        formatOption = fileFormat
    if not formatOption:
        formatOption = 'pdf'
    if directoryOption:
        if not os.path.isdir(os.path.join(os.getcwd(), directoryOption)):
            os.mkdir(directoryOption)
    if outputOption:
        if formatOption in ('ps', 'pdf'):
            outputFileName = outputOption
            if directoryOption:
                outputFileName = directoryOption + '/' + outputFileName
            canvas.Print(outputFileName + '[', formatOption)
        else:
            logging.warning("can't merge pictures, only postscript or pdf files")
            return 1
    retcode = 0
    objDrawnNumber = 0
    openRootFiles = []
    for fileName, pathSplitList in sourceList:
        rootFile = openROOTFile(fileName)
        if not rootFile:
            retcode += 1
            continue
        openRootFiles.append(rootFile)
        keyList = _keyListExtended(rootFile, pathSplitList)
        for key in keyList:
            if isTreeKey(key):
                pass
            else:
                if divideOption:
                    canvas.cd(objDrawnNumber % caseNumber + 1)
                    objDrawnNumber += 1
                obj = key.ReadObj()
                obj.Draw(drawOption)
                if divideOption:
                    if objDrawnNumber % caseNumber == 0:
                        if not outputOption:
                            outputFileName = str(objDrawnNumber // caseNumber) + '.' + formatOption
                            if directoryOption:
                                outputFileName = os.path.join(directoryOption, outputFileName)
                        canvas.Print(outputFileName, formatOption)
                        canvas.Clear()
                        canvas.Divide(x, y)
                else:
                    if not outputOption:
                        outputFileName = key.GetName() + '.' + formatOption
                        if directoryOption:
                            outputFileName = os.path.join(directoryOption, outputFileName)
                    if outputOption or formatOption == 'pdf':
                        objTitle = 'Title:' + key.GetClassName() + ' : ' + key.GetTitle()
                        canvas.Print(outputFileName, objTitle)
                    else:
                        canvas.Print(outputFileName, formatOption)

    if divideOption:
        if objDrawnNumber % caseNumber != 0:
            if not outputOption:
                outputFileName = str(objDrawnNumber // caseNumber + 1) + '.' + formatOption
                if directoryOption:
                    outputFileName = os.path.join(directoryOption, outputFileName)
            canvas.Print(outputFileName, formatOption)
    if outputOption:
        if not divideOption:
            canvas.Print(outputFileName + ']', objTitle)
        else:
            canvas.Print(outputFileName + ']')
    map(lambda rootFile: rootFile.Close(), openRootFiles)
    return retcode


def _removeObjects(fileName, pathSplitList, interactive=False, recursive=False):
    retcode = 0
    rootFile = openROOTFile(fileName, 'update')
    if not rootFile:
        return 1
    for pathSplit in pathSplitList:
        retcode += deleteRootObject(rootFile, pathSplit, interactive, recursive)

    rootFile.Close()
    return retcode


def rootRm(sourceList, interactive=False, recursive=False):
    if sourceList == []:
        return 1
    retcode = 0
    for fileName, pathSplitList in sourceList:
        retcode += _removeObjects(fileName, pathSplitList, interactive, recursive)

    return retcode