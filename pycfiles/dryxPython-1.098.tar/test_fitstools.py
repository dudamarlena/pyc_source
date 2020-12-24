# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/tests/test_fitstools.py
# Compiled at: 2013-08-21 09:59:35
import os, nose
from .. import fitstools

def setUpModule():
    global log
    global pathToFitsFile
    global pathToInputDataDir
    global pathToInputDir
    global pathToOutputDataDir
    global pathToOutputDir
    global testlog
    import logging, logging.config, yaml
    moduleDirectory = os.path.dirname(__file__) + '/../tests'
    pathToInputDir = moduleDirectory + '/input/'
    pathToInputDataDir = pathToInputDir + 'data/'
    pathToOutputDir = moduleDirectory + '/output/'
    pathToOutputDataDir = pathToOutputDir + 'data/'
    testlog = open(pathToOutputDir + 'tests.log', 'w')
    pathToFitsFile = pathToInputDataDir + 'LSQ12dwl_20120808_B639_56462_1.fits'
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


class test_convert_fits_header_to_dictionary:

    def test_pathToFitsFile_argu_is_str(self):
        nose.tools.assert_raises(TypeError, fitstools.convert_fits_header_to_dictionary, log, ['not a string', 10])

    def test_error_raises_if_fits_file_does_not_exists(self):
        nose.tools.assert_raises(IOError, fitstools.convert_fits_header_to_dictionary, log, '/path/to/nothing')

    def test_dictionary_is_returned(self):
        result = fitstools.convert_fits_header_to_dictionary(log, pathToFitsFile)
        nose.tools.assert_is_instance(result, dict)

    def test_dictionary_values_are_lists_with_2_items(self):
        result = fitstools.convert_fits_header_to_dictionary(log, pathToFitsFile)
        lengthResult = True
        for k, v in result.iteritems():
            if len(v) != 2:
                lengthResult = False

        nose.tools.assert_true(lengthResult)