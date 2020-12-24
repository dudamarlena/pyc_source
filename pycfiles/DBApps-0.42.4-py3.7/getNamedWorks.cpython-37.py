# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/getNamedWorks.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 4583 bytes
import argparse, csv
from typing import Union
from config.config import *
import pymysql, pathlib, os, datetime, DBApps.Writers.progressTimer

class GetReadyWorksArgs:
    __doc__ = '\n    Holds command line arguments\n    '


def setup_config(drsDbConfig: str) -> DBConfig:
    """
    gets dbConfig values for setup
    :param drsDbConfig: in section:file format
    :return:
    """
    try:
        args = drsDbConfig.split(':')
        dbName = args[0]
        dbConfigFile = os.path.expanduser(args[1])
    except IndexError:
        raise IndexError('Invalid argument %s: Must be formatted as section:file ' % drsDbConfig)

    return DBConfig(dbName, dbConfigFile)


def getResultsByName(dbConfig, outputDir):
    """

    :param dbConfig:
    :param outputDir:
    :return:
    """
    dbConnection = start_connect(dbConfig)
    with dbConnection:
        workCursor = dbConnection.cursor()
        workCursor.execute("select distinct workId from Works where WorkName in (                             'W00EGS1017042', 'W00EGS1017169', 'W00KG03797', 'W00KG09824', 'W12171', 'W12362', 'W17209', 'W19993', 'W1KG2855', 'W1KG3460', 'W1KG4215', 'W1KG4228', 'W1KG4313', 'W1KG4313', 'W1KG5256', 'W1KG5258', 'W1KG5478', 'W1KG5488', 'W1KG5945', 'W1KG6007', 'W1KG6058', 'W1KG6152', 'W1KG6160', 'W1KG6288', 'W1KG8579', 'W1KG8724', 'W1KG8837', 'W1KG8855', 'W1KG8896', 'W1KG8934', 'W1KG9090', 'W1KG9121', 'W1KG9561', 'W1KG9563', 'W1PD105801', 'W1PD105849', 'W1PD105855', 'W1PD105864', 'W1PD105899', 'W1CZ1293', 'W1CZ2403', 'W1CZ674', 'W1KG11708', 'W1KG14505', 'W1KG15407', 'W1KG1610', 'W1KG1616', 'W1KG16696', 'W1KG2230')                             ;")
        workIdResults = workCursor.fetchall()
        workCursor.close()
        workCursor = dbConnection.cursor(pymysql.cursors.DictCursor)
        outfile = pathlib.Path(outputDir) / datetime.datetime.now().strftime('%y%m%e%H%M%S')
        with outfile.open('w', newline='') as (fw):
            fieldNames = [
             'WorkName', 'HOLLIS', 'Volume', 'OutlineOSN', 'PrintMasterOSN']
            csvwr = csv.DictWriter(fw, fieldNames)
            for workTuple in workIdResults:
                print(workTuple)
                workCursor.callproc('GetReadyVolumesByWorkId', workTuple)
                workVolumeResults = workCursor.fetchall()
                csvwr.writeheader()
                for resultRow in workVolumeResults:
                    downRow = {fieldName:resultRow[fieldName] for fieldName in fieldNames}
                    csvwr.writerow(downRow)


def start_connect(cfg):
    """
    Opens a database connection using the DBConfig
    :param cfg:
    :return:
    """
    return pymysql.connect(read_default_file=(cfg.db_cnf), read_default_group=(cfg.db_host),
      charset='utf8')


def getNamedWorks():
    myArgs = GetReadyWorksArgs()
    parseByNameArgs(myArgs)
    dbConfig = setup_config(myArgs.drsDbConfig)
    outRoot = os.path.expanduser(myArgs.resultsRoot)
    if not os.path.exists(outRoot):
        os.mkdir(outRoot)
    getResultsByName(dbConfig, outRoot, myArgs.numWorks)


def parseByNameArgs(argNamespace: GetReadyWorksArgs) -> None:
    """
    :param argNamespace. class which holds arg values
    """
    _parser = argparse.ArgumentParser(description='Downloads ready works to folder, creating files related to folder name', usage='%(prog)s | -d DBAppSection:DbAppFile [ -n n How many works to download. ] resultsRoot')
    _parser.add_argument('-d', '--drsDbConfig', help='specify section:configFileName')
    _parser.add_argument('-n', '--numWorks', help='how many works to fetch', default=10, type=int)
    _parser.add_argument('resultsRoot', help='Directory containing WebAdminResults. Overwrites existing contents')
    _parser.parse_args(namespace=argNamespace)


if __name__ == '__main__':
    getNamedWorks()