# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/tests/test_command_line.py
# Compiled at: 2013-08-21 09:32:56
import os, nose, dryxPython.command_line as cl
from unittest import TestCase

def setUpModule():
    global log
    global pathToInputDataDir
    global pathToInputDir
    global pathToOutputDataDir
    global pathToOutputDir
    global testlog
    import logging, logging.config, yaml
    print 'SETUP'
    moduleDirectory = os.path.dirname(__file__) + '/../tests'
    pathToInputDir = moduleDirectory + '/input/'
    pathToInputDataDir = pathToInputDir + 'data/'
    pathToOutputDir = moduleDirectory + '/output/'
    pathToOutputDataDir = pathToOutputDir + 'data/'
    testlog = open(pathToOutputDir + 'tests.log', 'w')
    loggerConfig = '\n    version: 1\n    formatters:\n        file_style:\n            format: \'* %(asctime)s - %(name)s - %(levelname)s (%(filename)s > %(funcName)s > %(lineno)d) - %(message)s  \'\n            datefmt: \'%Y/%m/%d %H:%M:%S\'\n        console_style:\n            format: \'* %(asctime)s - %(levelname)s: %(filename)s:%(funcName)s:%(lineno)d > %(message)s\'\n            datefmt: \'%H:%M:%S\'\n        html_style:\n            format: \'<div id="row" class="%(levelname)s"><span class="date">%(asctime)s</span>   <span class="label">file:</span><span class="filename">%(filename)s</span>   <span class="label">method:</span><span class="funcName">%(funcName)s</span>   <span class="label">line#:</span><span class="lineno">%(lineno)d</span> <span class="pathname">%(pathname)s</span>  <div class="right"><span class="message">%(message)s</span><span class="levelname">%(levelname)s</span></div></div>\'\n            datefmt: \'%Y-%m-%d <span class= "time">%H:%M <span class= "seconds">%Ss</span></span>\'\n    handlers:\n        console:\n            class: logging.StreamHandler\n            level: DEBUG\n            formatter: console_style\n            stream: ext://sys.stdout\n    root:\n        level: DEBUG\n        handlers: [console]'
    logging.config.dictConfig(yaml.load(loggerConfig))
    log = logging.getLogger(__name__)
    return


def tearDownModule():
    """tear down test fixtures"""
    print 'TEARDOWN'
    testlog.close()
    return


class emptyLogger:
    info = None
    error = None
    debug = None
    critical = None
    warning = None


class test_get_help_for_python_module:

    def test_fail_for_no_argv(self):
        result = cl.py_get_help_for_python_module()
        assert result == -1


class test_fits_print_fits_header:

    def test_docopt(self):
        clArgs = {}
        clArgs['<path-to-fits-file>'] = pathToInputDataDir + 'LSQ12dwl_20120808_B639_56462_1.fits'
        clArgs['--pydict'] = False
        clArgs['--help'] = False
        result = cl.dft_print_fits_header(clArgs)
        nose.tools.assert_is_instance(result, list)

    def test_result_to_python_dictionary(self):
        clArgs = {}
        clArgs['<path-to-fits-file>'] = pathToInputDataDir + 'LSQ12dwl_20120808_B639_56462_1.fits'
        clArgs['--pydict'] = True
        clArgs['--help'] = False
        result = cl.dft_print_fits_header(clArgs)
        nose.tools.assert_is_instance(result, dict)