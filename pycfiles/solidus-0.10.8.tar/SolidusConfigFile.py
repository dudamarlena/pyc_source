# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hhempste/Documents/python/solidus/solidus/SolidusConfigFile.py
# Compiled at: 2017-05-09 17:00:04
import SolidusErrorLog, os
strApplicationPath = os.path.dirname(os.path.realpath(__file__)) + '/'
SOLIDUS_CONFIG_FILE_NAME = 'Solidus.config'
SOLIDUS_CONFIG_FILE = strApplicationPath + SOLIDUS_CONFIG_FILE_NAME

class SolidusConfigFileError(Exception):
    pass


def writeSolidusConfigFile(strOriginGuidIn, strEmailAddressIn):
    try:
        outFile = open(SOLIDUS_CONFIG_FILE, 'w')
        outFile.write('Solidus Config File Version .1\n')
        outFile.write(strOriginGuidIn + '\n')
        outFile.write(strEmailAddressIn + '\n')
        outFile.close()
    except Exception as err:
        SolidusErrorLog.logError(str(err), 'writeSolidusConfigFile')
        raise SolidusConfigFileError('Write Failed: ' + str(err))


def getSolidusOriginGuidAndRegisteredEmailAddress():
    try:
        inFile = open(SOLIDUS_CONFIG_FILE, 'r')
        strFileVersionHeader = inFile.readline()
        strOriginGuid = inFile.readline().rstrip('\n')
        strEmailAddress = inFile.readline().rstrip('\n')
        if len(strEmailAddress) == 0:
            raise SolidusConfigFileError('Could not read in config settings')
        return (strOriginGuid, strEmailAddress)
    except Exception as err:
        try:
            if os.path.exists(SOLIDUS_CONFIG_FILE):
                SolidusErrorLog.logError(str(err), 'getSolidusOriginGuidAndRegisteredEmailAddress')
        except:
            pass

        return (None, None)

    return


def deleteSolidusConfigFile():
    try:
        if os.path.exists(SOLIDUS_CONFIG_FILE):
            os.remove(SOLIDUS_CONFIG_FILE)
    except:
        SolidusErrorLog.logError(str(err), 'deleteSolidusConfigFile')