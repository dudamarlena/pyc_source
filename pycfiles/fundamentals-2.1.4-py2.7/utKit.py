# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/utKit.py
# Compiled at: 2020-04-17 06:44:40
"""
*A unit-testing kit to simplify my unit-tests*

:Author:
    David Young
"""
from builtins import object
import sys, os, logging, logging.config, yaml
try:
    yaml.warnings({'YAMLLoadWarning': False})
except:
    pass

class utKit(object):
    """
    *Default setup for fundamentals style unit-testing workflow (all tests base on nose module)*

    **Key Arguments**

    - ``moduleDirectory`` -- the directory to the unit-testing test file
    

    **Usage**

    To use this kit within any of your unit-test modules add the following code before your test methods:

    ```python
    from fundamentals.utKit import utKit
    # SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
    moduleDirectory = os.path.dirname(__file__)
    utKit = utKit(moduleDirectory)
    log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
    utKit.tearDownModule() 
    ```
    
    """

    def __init__(self, moduleDirectory):
        self.moduleDirectory = moduleDirectory
        self.pathToInputDir = moduleDirectory + '/input/'
        self.pathToOutputDir = moduleDirectory + '/output/'
        self.loggerConfig = '\n        version: 1\n        formatters:\n            file_style:\n                format: \'* %(asctime)s - %(name)s - %(levelname)s (%(pathname)s > %(funcName)s > %(lineno)d) - %(message)s  \'\n                datefmt: \'%Y/%m/%d %H:%M:%S\'\n            console_style:\n                format: \'* %(asctime)s - %(levelname)s: %(pathname)s:%(funcName)s:%(lineno)d > %(message)s\'\n                datefmt: \'%H:%M:%S\'\n            html_style:\n                format: \'<div id="row" class="%(levelname)s"><span class="date">%(asctime)s</span>   <span class="label">file:</span><span class="filename">%(filename)s</span>   <span class="label">method:</span><span class="funcName">%(funcName)s</span>   <span class="label">line#:</span><span class="lineno">%(lineno)d</span> <span class="pathname">%(pathname)s</span>  <div class="right"><span class="message">%(message)s</span><span class="levelname">%(levelname)s</span></div></div>\'\n                datefmt: \'%Y-%m-%d <span class= "time">%H:%M <span class= "seconds">%Ss</span></span>\'\n        handlers:\n            console:\n                class: logging.StreamHandler\n                level: DEBUG\n                formatter: console_style\n                stream: ext://sys.stdout\n        root:\n            level: DEBUG\n            handlers: [console]'
        self.dbConfig = '\n        version: 1\n        db: unit_tests\n        host: localhost\n        user: utuser\n        password: utpass\n        '

    def setupModule(self):
        """
        *The setupModule method*

        **Return**

        - ``log`` -- a logger
        - ``dbConn`` -- a database connection to a test database (details from yaml settings file)
        - ``pathToInputDir`` -- path to modules own test input directory
        - ``pathToOutputDir`` -- path to modules own test output directory
        
        """
        import pymysql as ms
        logging.config.dictConfig(yaml.load(self.loggerConfig))
        log = logging.getLogger(__name__)
        if self.dbConfig:
            connDict = yaml.load(self.dbConfig)
            dbConn = ms.connect(host=connDict['host'], user=connDict['user'], passwd=connDict['password'], db=connDict['db'], use_unicode=True, charset='utf8', local_infile=1, client_flag=ms.constants.CLIENT.MULTI_STATEMENTS, connect_timeout=3600)
            dbConn.autocommit(True)
        else:
            dbConn = False
        return (log, dbConn, self.pathToInputDir, self.pathToOutputDir)

    def tearDownModule(self):
        """
        *The tearDownModule method*

        **Key Arguments**

        # -
        

        **Return**

        - None
        
        """
        return

    def get_project_root(self):
        """
        *Get the root of the `python` package - useful for getting files in the root directory of a project*

        **Return**

        - ``rootPath`` -- the root path of a project
        
        """
        import os
        rootPath = os.path.dirname(__file__)
        return rootPath

    def refresh_database(self):
        """
        *Refresh the unit test database*
        """
        from fundamentals.mysql import directory_script_runner
        from fundamentals import tools
        packageDirectory = self.get_project_root()
        su = tools(arguments={'settingsFile': packageDirectory + '/test_settings.yaml'}, docString=__doc__, logLevel='DEBUG', options_first=False, projectName=None, defaultSettingsFile=False)
        arguments, settings, log, dbConn = su.setup()
        directory_script_runner(log=log, pathToScriptDirectory=packageDirectory + '/tests/input', databaseName=settings['database settings']['db'], force=True, loginPath=settings['database settings']['loginPath'], waitForResult=True, successRule=None, failureRule=None)
        return


if __name__ == '__main__':
    main()