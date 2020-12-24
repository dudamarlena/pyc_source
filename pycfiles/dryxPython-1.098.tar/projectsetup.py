# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/projectsetup.py
# Compiled at: 2013-08-06 06:05:30
"""
projectsetup
==================

Created by David Young on 20130521
If you have any questions requiring this script please email me: d.r.young@qub.ac.uk

dryx syntax:
xxx = come back here and do some more work
_someObject = a 'private' object that should only be changed for debugging

notes:
    -
"""
import sys, os

class projectSetup:
    """
    Load the settings in the general and specific settings files and give them a global scope.

    **Todo**
    - [ ] strip this class of data, clean it and create snippet from it
    """

    def __init__(self, dbConn, relativePathToProjectRoot):
        """
        Load the global settings in the __init__ method, ``projectSettings`` is a dictionary of the project settings.

        **Key Arguments:**
            - ``dbConn`` -- the database connection
            - ``relativePathToProjectRoot`` -- the relative path from the module calling this function to the project root.
        """
        self.relativePathToProjectRoot = relativePathToProjectRoot
        self.generalSettingsFilepath = relativePathToProjectRoot + '/settings/general_settings.yaml'
        self.set_python_path()
        self.dbConn = dbConn
        self.log = self.get_logger()
        if dbConn:
            self.dbConn = self.get_db_connection()
        self.settings, self.contentPaths = self.get_project_settings()
        return

    def get_project_atrributes(self):
        """Get all of the project attributes with one method

        **Key Arguments:**
            - None

        **Return:**
            - ``log``
            - ``dbConn``
            - ``settings``
            - ``contentPaths``
        """
        self.log.info('starting the ``get_project_atrributes`` function')
        log = self.log
        dbConn = self.dbConn
        settings = self.settings
        contentPaths = self.contentPaths
        self.log.info('completed the ``get_project_atrributes`` function')
        return (dbConn, log, settings, contentPaths)

    def set_python_path(self):
        """Setup the python path for the project modules

        **Key Arguments:**
            - None

        **Return:**
            - None
        """
        import yaml
        pathToYamlFile = self.relativePathToProjectRoot + 'settings/python_path.yaml'
        try:
            stream = file(pathToYamlFile, 'r')
            ppDict = yaml.load(stream)
        except Exception as e:
            print str(e)

        projectRoot = ppDict['project_root']
        pythonpaths = ppDict['python_path']
        for key in pythonpaths:
            if pythonpaths[key]:
                sys.path.append(projectRoot + pythonpaths[key])

        basePath = self.relativePathToProjectRoot + 'dependencies/'
        _recusively_add_directories_to_path(basePath)
        basePath = self.relativePathToProjectRoot + 'code/'
        _recusively_add_directories_to_path(basePath)
        return

    def get_project_settings(self):
        """Setup the project settings for the project from the general setting yaml file.

        **Key Arguments:**
            - None

        **Return:**
            - ``settings`` -- a dictionary of the project settings
            - ``contentPaths`` -- a dictionary of paths to various areas of the project
        """
        import os, yaml
        try:
            stream = file(self.generalSettingsFilepath, 'r')
        except Exception as e:
            print 'could not open the %s file - failed with this error: %s ' % (self.generalSettingsFilepath, str(e))
            return -1

        snippetMetadataDictionary = yaml.load(stream)
        stream.close()
        basename = os.path.basename(self.generalSettingsFilepath)
        folderPath = str(os.path.abspath(self.generalSettingsFilepath))
        folderPath = folderPath.replace(basename, '')
        try:
            stream = file(folderPath + snippetMetadataDictionary['specific_settings'], 'r')
        except Exception as e:
            print 'could not open the %s file - failed with this error: %s ' % (folderPath + snippetMetadataDictionary['specific_settings'], str(e))
            return -1

        settings = dict(snippetMetadataDictionary.items() + yaml.load(stream).items())
        contentPaths = settings['contentPaths']
        for k, v in contentPaths.iteritems():
            contentPaths[k] = settings['projectPath'] + v

        return (settings, contentPaths)

    def get_db_connection(self):
        """Setup the DB connection for the project

        **Key Arguments:**
            - None

        **Return:**
            - ``dbConn`` -- database connection
        """
        import dryxPython.mysql as m
        settings, contentPaths = self.get_project_settings()
        dbConn = m.set_db_connection(contentPaths['dbSettings'])
        return dbConn

    def get_logger(self):
        """Set the loggers for the project

        **Key Arguments:**
            - None

        **Return:**
            - ``log`` -- the logger for the project
        """
        import dryxPython.logs as l
        settings, contentPaths = self.get_project_settings()
        log = l.setup_dryx_logging(contentPaths['loggingSettings'])
        return log


def _add_directories_to_path(directoryPath):
    """Given a directory path, add its contained directories to the system path
    - this is a public function in commonutils

    **Key Arguments:**
        - ``directoryPath`` -- the path to the directory containing the directories you want to add to the system path

    **Return:**
        - None
    """
    import sys
    for d in os.listdir(directoryPath):
        fullPath = os.path.join(directoryPath, d)
        if os.path.isdir(os.path.join(directoryPath, d)):
            sys.path.append(fullPath)


def _recusively_add_directories_to_path(directoryPath):
    """Given a directory path, add its contained directories **recusively** to the system path

    **Key Arguments:**
           - ``directoryPath`` -- the path to the directory containing the directories you want to recusively add to the system path

    **Return:**
        - None
    """
    import sys
    _add_directories_to_path(directoryPath)
    parentDirectoryList = [directoryPath]
    while len(parentDirectoryList) != 0:
        childDirList = []
        for parentDir in parentDirectoryList:
            thisDirList = os.listdir(parentDir)
            for d in thisDirList:
                fullPath = os.path.join(parentDir, d)
                if os.path.isdir(fullPath):
                    _add_directories_to_path(fullPath)
                    aDirList = os.listdir(fullPath)
                    childDirList.append(fullPath)

        parentDirectoryList = childDirList


def set_python_path(relativePathToProjectRoot):
    """set the python path for the project modules
    - note, the Apache pythonpath is not the same as the users path so this function is particularly usful if the project is a web-based.

    **Key Arguments:**
        - ``relativePathToProjectRoot`` -- the relative path from the module calling this function to the project root.

    **Return:**
        - ``None``

    - [ ] depeciate this set_python_path function - now in projectSetup class
    """
    import yaml
    pathToYamlFile = relativePathToProjectRoot + 'settings/python_path.yaml'
    try:
        stream = file(pathToYamlFile, 'r')
        ppDict = yaml.load(stream)
    except Exception as e:
        print str(e)

    projectRoot = ppDict['project_root']
    pythonpaths = ppDict['python_path']
    for key in pythonpaths:
        if pythonpaths[key]:
            sys.path.append(projectRoot + pythonpaths[key])

    basePath = os.getcwd() + '/' + relativePathToProjectRoot + 'dependencies/'
    _recusively_add_directories_to_path(basePath)
    basePath = os.getcwd() + '/' + relativePathToProjectRoot + 'code/'
    _recusively_add_directories_to_path(basePath)


def settings(relativePathToProjectRoot, dbConn=True, log=True):
    """
    Create a connector to the database if required & setup logging

        **Key Arguments:**
            - ``relativePathToProjectRoot`` -- the relative path from the module calling this function to the project root.

        **Return:**
            - dbConn - database connection
            - log - logger

    - [ ] depeciate this settings function - now in projectSetup class
    """
    import os, dryxPython.mysql as m, dryxPython.logs as l
    path = os.getcwd()
    setup_helper_variables(relativePathToProjectRoot)
    if dbConn:
        dbConn = m.set_db_connection(pathToDBSettings)
    if log:
        log = l.setup_dryx_logging(pathToLoggingSettings)
    return (dbConn, log)


def setup_helper_variables(relativePathToProjectRoot):
    """Setup various helper variables - mainly paths to thespacedoctor boilerplate directories

    **Key Arguments:**
        - ``relativePathToProjectRoot`` -- the relative path from the module calling this function to the project root.    - ``relativePathToProjectRoot`` -- the relative path from the module calling this function to the project root.

    **Return:**
        - None

    **Tasks**
    - [ ] depeciate this setup_helper_variables function - now in projectSetup class
    """
    global mdLog
    global mdLogPath
    global pathToArchiveFolder
    global pathToAsciiLogsFolder
    global pathToCodeFolder
    global pathToDBSettings
    global pathToDependenciesFolder
    global pathToDocumentationFolder
    global pathToDynamicInputFolder
    global pathToHtmlLogsFolder
    global pathToInputFolder
    global pathToLoggingSettings
    global pathToLogsFolder
    global pathToOutputDataFolder
    global pathToOutputFolder
    global pathToOutputPlotsFolder
    global pathToOutputResultsFolder
    global pathToSettingsFolder
    global pathToStaticInputFolder
    global pathToYamlFile
    pathToRoot = relativePathToProjectRoot
    pathToArchiveFolder = pathToRoot + '.archive/'
    pathToCodeFolder = pathToRoot + 'code/'
    pathToDependenciesFolder = pathToRoot + 'dependencies/'
    pathToDocumentationFolder = pathToRoot + 'documentation/'
    pathToInputFolder = pathToRoot + 'input/'
    pathToStaticInputFolder = pathToInputFolder + 'static/'
    pathToDynamicInputFolder = pathToInputFolder + 'dynamic/'
    pathToLogsFolder = pathToRoot + 'logs/'
    pathToAsciiLogsFolder = pathToLogsFolder + 'ascii/'
    pathToHtmlLogsFolder = pathToLogsFolder + 'html/'
    pathToOutputFolder = pathToRoot + 'output/'
    pathToOutputDataFolder = pathToOutputFolder + 'data/'
    pathToOutputPlotsFolder = pathToOutputFolder + 'plots/'
    pathToOutputResultsFolder = pathToOutputFolder + 'results/'
    pathToSettingsFolder = pathToRoot + 'settings/'
    pathToYamlFile = pathToSettingsFolder + 'python_path.yaml'
    pathToDBSettings = pathToSettingsFolder + 'database_credentials.yaml'
    pathToLoggingSettings = pathToSettingsFolder + 'logging.yaml'
    mdLogPath = pathToOutputResultsFolder + 'generated_result_log.md'
    mdLog = open(mdLogPath, 'w')
    mdLog.close()
    mdLog = open(mdLogPath, 'a')


if __name__ == '__main__':
    main()