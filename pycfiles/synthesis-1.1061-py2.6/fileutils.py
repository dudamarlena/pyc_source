# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/fileutils.py
# Compiled at: 2011-01-19 19:20:51
import os, glob, copy, shutil, csv
from time import sleep as ossleep
import datetime
from synthesis.conf import settings

def sleep(sleepTime):
    print 'Sleeping for %s' % sleepTime
    ossleep(sleepTime)


def getSmartPath(baseDir, filePath):
    if os.path.exists(filePath):
        return filePath
    newPath = os.path.join(baseDir, filePath)
    if os.path.exists(newPath):
        return newPath
    try:
        os.makedirs(newPath)
    except OSError:
        raise OSError


def checkPath(filePath):
    if os.path.exists(filePath):
        return 0
    try:
        os.makedirs(filePath)
        if os.path.exists(filePath):
            return 0
        raise
    except:
        raise


def keyToDict(listVals):
    dict = {}
    for key in range(0, len(listVals)):
        dict.setdefault(listVals[key], key)

    return dict


def stripData(record, delimiter='\n'):
    record = record.split(delimiter)
    record = record[0]
    return record


def unquoteList(parts=[], findChar='"'):
    newList = []
    for item in parts:
        item = unquoteField(item, findChar='"')
        newList.append(item)

    return newList


def unquoteField(field, findChar='"'):
    newField = ''
    newField = field.replace(findChar, '')
    newField = newField.replace(findChar, '')
    x = copy.deepcopy(newField)
    return x


def unquoteString(record='', findChar='"'):
    posFind = record.find(findChar)
    while not posFind == -1:
        record = record.replace(findChar, '')
        posFind = record.find(findChar)

    return record


def cleanRecord(record, delimitter, findChar, replaceChar, startPos=0):
    """ this function takes the input record (csv record) and 
    searches for a delimiter (") at the extremes of the record
    and replaces the findChar with a replaceChar in the substring
    between the delimited chars."""
    pos1Find = record.find(delimitter, startPos)
    if pos1Find == -1:
        return record
    pos2Find = record.find(delimitter, pos1Find + 1)
    if pos2Find == -1:
        return record
    badChars = record[pos1Find:pos2Find + 1]
    goodChars = badChars.replace(findChar, replaceChar)
    newRecord = record[0:pos1Find] + goodChars + record[pos2Find + 1:len(record)]
    pos3Find = newRecord.find(delimitter, pos2Find)
    if pos3Find == -1:
        return newRecord
    newRecord = cleanRecord(record=newRecord, delimitter=delimitter, findChar=findChar, replaceChar=replaceChar, startPos=pos2Find + 2)
    return newRecord


def parseRecord(record, delimiter=','):
    recParts = []
    findThis = '\r\n'
    if record.find(findThis) == -1:
        record = stripData(record)
    else:
        record = stripData(record, findThis)
    recParts = record.split(delimiter)
    return recParts


def suckFile2(filename):
    records = []
    print 'Ready to suck file2 in %s' % filename
    try:
        reader = csv.reader(open(filename, 'rb'))
        for row in reader:
            records.append(row)

    except:
        print 'ERROR: filename: %s not found.  Please investigate' % filename

    print 'sucked in %s records' % len(records)
    return records


def suckFile(filename):
    records = []
    print 'Ready to suck file in %s' % filename
    try:
        file = open(filename, 'r')
    except:
        print 'ERROR: filename: %s not found.  Please investigate' % filename

    records = file.readlines()
    print 'sucked in %s records' % len(records)
    return records


def pushIntoDict(dictName, theDict, theKey, theRow, appendRow=False):
    rc = 0
    tmpList = []
    if theDict.has_key(theKey):
        rc = 0
        if appendRow == True:
            rowVal = theDict[theKey]
            rowVal.append(theRow)
            theDict[theKey] = rowVal
            rc = 2
    else:
        if appendRow == True:
            tmpList.append(theRow)
            theDict[theKey] = tmpList
        else:
            theDict[theKey] = theRow
        rc = 1
    return rc


def dumpObjToFile(dumpObject, filename):
    print 'dump File Processing'
    f = open(filename, 'w')
    if dir(dumpObject).count('__iter__') > 0:
        f.writelines(dumpObject)
    else:
        f.write(str(dumpObject))
    f.close()


def grabFiles(directoryToProcess):
    print 'Getting Files'
    validFiles = []
    files = glob.glob(directoryToProcess)
    for file in files:
        print 'processing: %s' % file
        validFiles.append(file)

    print 'Done Grabbing Files'
    return validFiles


def getTimeStampedFileName(unstamped_file_path):
    """Simply extract the name of a file from a path string, timestamp the file name, and return a file name string with the modification."""
    if settings.DEBUG:
        print 'unstamped_file_path in getTimeStampedFileName is: ', unstamped_file_path
    (old_file_path, old_file_name) = os.path.split(unstamped_file_path)
    old_file_name_prefix = os.path.splitext(old_file_name)[0]
    old_file_name_suffix = os.path.splitext(unstamped_file_path)[1]
    new_file_name_prefix = old_file_name_prefix + str(datetime.datetime.now())
    stamped_file_name = new_file_name_prefix + old_file_name_suffix
    stamped_file_name = stamped_file_name.replace(' ', '_')
    if settings.DEBUG:
        print 'stamped_file_name in getTimeStampedFileName is: ', stamped_file_name
    return stamped_file_name


def getUniqueFileNameForMove(attempted_file_name, destination_directory):
    """Returns a new unique timestamped file name string to use at destination_directory indicated."""
    attempted_file_path = destination_directory + '/' + attempted_file_name
    if settings.DEBUG:
        if os.path.isfile(attempted_file_path):
            print 'output location', attempted_file_path, 'already exists'
    stamped_file_path = getTimeStampedFileName(attempted_file_path)
    if os.path.isfile(stamped_file_path):
        print 'The renamed file is also already there, please check this out.'
    (file_path, unique_file_name) = os.path.split(stamped_file_path)
    return unique_file_name


def moveFile(source_file_path, destination_directory):
    """Move a file path to a destination directory.  But first, test if the destination exists.  If not make it.  Also timestamp it."""
    try:
        if not os.path.exists(destination_directory):
            os.mkdir(destination_directory)
        (source_file_path_prefix, source_file_name) = os.path.split(source_file_path)
        temp_file_path = os.path.join(settings.BASE_PATH, 'tmp', source_file_name)
        try:
            os.remove(temp_file_path)
        except OSError:
            pass

        shutil.move(source_file_path, temp_file_path)
        (temp_file_path_prefix, temp_file_name) = os.path.split(temp_file_path)
        timestamped_temp_file_name = getUniqueFileNameForMove(temp_file_name, destination_directory)
        timestamped_temp_file_path = os.path.join(temp_file_path_prefix, timestamped_temp_file_name)
        shutil.move(temp_file_path, timestamped_temp_file_path)
        try:
            shutil.move(timestamped_temp_file_path, destination_directory)
        except shutil.Error:
            raise

    except:
        raise


def renameFile(source, dest):
    try:
        shutil.copy(source, dest)
        deleteFile(source)
    except:
        pass


def copyFile(source, dest):
    shutil.copy2(source, dest)


def deleteFile(fileDelete):
    try:
        os.remove(fileDelete)
    except:
        print '\\T\\TFAILURE:Deletion of file %s failed' % fileDelete * 3
        raise

    print 'SUCCESS: Deletion of file %s succeeded' % fileDelete


def backupFile(project):
    copyFile(project, project + '.bak')


def makeBlock(wording, numChars=0):
    if numChars == 0:
        numChars = len(wording)
    if len(wording) >= numChars:
        numChars = len(wording) + 4
    numSpaces = (numChars - (len(wording) + 2)) / 2
    oddSpacing = (numChars - len(wording)) % 2
    print numChars * '*'
    print '*' + ' ' * numSpaces + wording + ' ' * numSpaces + oddSpacing * ' ' + '*'
    print numChars * '*'


def sortItems(incomingList, colToSort=''):
    from operator import itemgetter
    return sorted(incomingList, key=itemgetter(colToSort))