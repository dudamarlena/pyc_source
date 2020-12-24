# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/git_repos/dryxDropboxCL/dryxDropboxCL/utKit.py
# Compiled at: 2016-06-17 04:00:54
from fundamentals import utKit

class utKit(utKit):
    """
    *Override dryx utKit*
    """
    pass


from fundamentals import utKit

class utKit(utKit):
    """
    *Override dryx utKit*
    """

    def __init__(self, moduleDirectory):
        self.moduleDirectory = moduleDirectory
        self.pathToInputDir = moduleDirectory + '/input/'
        self.pathToOutputDir = moduleDirectory + '/output/'
        self.loggerConfig = '\n        version: 1\n        formatters:\n            file_style:\n                format: \'* %(asctime)s - %(name)s - %(levelname)s (%(filename)s > %(funcName)s > %(lineno)d) - %(message)s  \'\n                datefmt: \'%Y/%m/%d %H:%M:%S\'\n            console_style:\n                format: \'* %(asctime)s - %(levelname)s: %(filename)s:%(funcName)s:%(lineno)d > %(message)s\'\n                datefmt: \'%H:%M:%S\'\n            html_style:\n                format: \'<div id="row" class="%(levelname)s"><span class="date">%(asctime)s</span>   <span class="label">file:</span><span class="filename">%(filename)s</span>   <span class="label">method:</span><span class="funcName">%(funcName)s</span>   <span class="label">line#:</span><span class="lineno">%(lineno)d</span> <span class="pathname">%(pathname)s</span>  <div class="right"><span class="message">%(message)s</span><span class="levelname">%(levelname)s</span></div></div>\'\n                datefmt: \'%Y-%m-%d <span class= "time">%H:%M <span class= "seconds">%Ss</span></span>\'\n        handlers:\n            console:\n                class: logging.StreamHandler\n                level: DEBUG\n                formatter: console_style\n                stream: ext://sys.stdout\n        root:\n            level: DEBUG\n            handlers: [console]'
        self.dbConfig = '\n         version: 1\n         db: dryx_unit_testing\n         host: localhost\n         user: unittesting\n         password: utpass\n         '