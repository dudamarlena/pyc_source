# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/tests/test_mmd.py
# Compiled at: 2013-09-19 09:42:57
import os, nose
from dryxPython.mmd import mmd

def setUpModule():
    global log
    global pathToInputDir
    global pathToOutputDir
    global testlog
    import logging, logging.config, yaml
    moduleDirectory = os.path.dirname(__file__) + '/../tests'
    pathToInputDir = moduleDirectory + '/input/'
    pathToOutputDir = moduleDirectory + '/output/'
    testlog = open(pathToOutputDir + 'tests.log', 'w')
    loggerConfig = '\n    version: 1\n    formatters:\n        file_style:\n            format: \'* %(asctime)s - %(name)s - %(levelname)s (%(filename)s > %(funcName)s > %(lineno)d) - %(message)s  \'\n            datefmt: \'%Y/%m/%d %H:%M:%S\'\n        console_style:\n            format: \'* %(asctime)s - %(levelname)s: %(filename)s:%(funcName)s:%(lineno)d > %(message)s\'\n            datefmt: \'%H:%M:%S\'\n        html_style:\n            format: \'<div id="row" class="%(levelname)s"><span class="date">%(asctime)s</span>   <span class="label">file:</span><span class="filename">%(filename)s</span>   <span class="label">method:</span><span class="funcName">%(funcName)s</span>   <span class="label">line#:</span><span class="lineno">%(lineno)d</span> <span class="pathname">%(pathname)s</span>  <div class="right"><span class="message">%(message)s</span><span class="levelname">%(levelname)s</span></div></div>\'\n            datefmt: \'%Y-%m-%d <span class= "time">%H:%M <span class= "seconds">%Ss</span></span>\'\n    handlers:\n        console:\n            class: logging.StreamHandler\n            level: DEBUG\n            formatter: console_style\n            stream: ext://sys.stdout\n    root:\n        level: DEBUG\n        handlers: [console]'
    logging.config.dictConfig(yaml.load(loggerConfig))
    log = logging.getLogger(__name__)
    return


def tearDownModule():
    """tear down test fixtures"""
    testlog.close()
    return


class emptyLogger:
    info = None
    error = None
    debug = None
    critical = None
    warning = None


class test_convert_to_html:

    def test_convert_to_html_works_as_expected(self):
        kwargs = {}
        kwargs['log'] = log
        kwargs['pathToMMDFile'] = pathToInputDir + 'test_file_for_mmd_module.md'
        kwargs['css'] = 'amblin'
        print mmd.convert_to_html(**kwargs)