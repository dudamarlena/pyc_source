# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sloancone/utKit.py
# Compiled at: 2020-05-06 13:40:52
"""
*Unit testing tools*
"""
from fundamentals import utKit

class utKit(utKit):
    """
    *Override dryx utKit*
    """

    def __init__(self, moduleDirectory, dbConn=False):
        self.moduleDirectory = moduleDirectory
        self.pathToInputDir = moduleDirectory + '/input/'
        self.pathToOutputDir = moduleDirectory + '/output/'
        self.loggerConfig = '\n        version: 1\n        formatters:\n            file_style:\n                format: \'* %(asctime)s - %(name)s - %(levelname)s (%(filename)s > %(funcName)s > %(lineno)d) - %(message)s  \'\n                datefmt: \'%Y/%m/%d %H:%M:%S\'\n            console_style:\n                format: \'* %(asctime)s - %(levelname)s: %(filename)s:%(funcName)s:%(lineno)d > %(message)s\'\n                datefmt: \'%H:%M:%S\'\n            html_style:\n                format: \'<div id="row" class="%(levelname)s"><span class="date">%(asctime)s</span>   <span class="label">file:</span><span class="filename">%(filename)s</span>   <span class="label">method:</span><span class="funcName">%(funcName)s</span>   <span class="label">line#:</span><span class="lineno">%(lineno)d</span> <span class="pathname">%(pathname)s</span>  <div class="right"><span class="message">%(message)s</span><span class="levelname">%(levelname)s</span></div></div>\'\n                datefmt: \'%Y-%m-%d <span class= "time">%H:%M <span class= "seconds">%Ss</span></span>\'\n        handlers:\n            console:\n                class: logging.StreamHandler\n                level: DEBUG\n                formatter: console_style\n                stream: ext://sys.stdout\n        root:\n            level: DEBUG\n            handlers: [console]'
        self.dbConfig = False
        if dbConn:
            self.dbConfig = '\n             version: 1\n             db: dryx_unit_testing\n             host: localhost\n             user: unittesting\n             password: utpass\n             '

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