# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/command_line.py
# Compiled at: 2013-09-09 07:36:26
from dryxPython import commonutils
from dryxPython import fitstools

def _set_up_command_line_tool():
    import logging, logging.config, yaml
    loggerConfig = '\n    version: 1\n    formatters:\n        file_style:\n            format: \'* %(asctime)s - %(name)s - %(levelname)s (%(filename)s > %(funcName)s > %(lineno)d) - %(message)s  \'\n            datefmt: \'%Y/%m/%d %H:%M:%S\'\n        console_style:\n            format: \'* %(asctime)s - %(levelname)s: %(filename)s:%(funcName)s:%(lineno)d > %(message)s\'\n            datefmt: \'%H:%M:%S\'\n        html_style:\n            format: \'<div id="row" class="%(levelname)s"><span class="date">%(asctime)s</span>   <span class="label">file:</span><span class="filename">%(filename)s</span>   <span class="label">method:</span><span class="funcName">%(funcName)s</span>   <span class="label">line#:</span><span class="lineno">%(lineno)d</span> <span class="pathname">%(pathname)s</span>  <div class="right"><span class="message">%(message)s</span><span class="levelname">%(levelname)s</span></div></div>\'\n            datefmt: \'%Y-%m-%d <span class= "time">%H:%M <span class= "seconds">%Ss</span></span>\'\n    handlers:\n        console:\n            class: logging.StreamHandler\n            level: DEBUG\n            formatter: console_style\n            stream: ext://sys.stdout\n    root:\n        level: DEBUG\n        handlers: [console]'
    logging.config.dictConfig(yaml.load(loggerConfig))
    log = logging.getLogger(__name__)
    return log


def py_get_help_for_python_module(argv=None):
    """print the help for python module

    **Key Arguments:**
        - ``argv`` -- arguments for the function
    """
    import sys, os
    log = _set_up_command_line_tool()
    if argv is None:
        argv = sys.argv
    if len(argv) != 2:
        print 'Usage: get_help_for_python_module <pathToModuleFile>'
        return -1
    else:
        print 'argv:', argv
        pathToModuleFile = argv[1]
        basename = os.path.basename(pathToModuleFile).replace('.py', '')
        print basename
        return


def dft_print_fits_header(clArgs=None):
    """
    Print a fits file headers to stout

    Usage:
        dft_print_fits_header <path-to-fits-file>
        dft_print_fits_header -p <path-to-fits-file>
        dft_print_fits_header -h

        -h, --help    show this help message
        -p, --pydict  print as python dictionary
    """
    import sys, os
    from docopt import docopt
    import pyfits as pf
    from dryxPython import fitstools as dft
    log = _set_up_command_line_tool()
    if clArgs == None:
        clArgs = docopt(dft_print_fits_header.__doc__)
    pathToFitsFile = clArgs['<path-to-fits-file>']
    hduList = pf.open(pathToFitsFile)
    fitsHeader = hduList[0].header
    fitsHeader = hduList[0].header
    cardList = fitsHeader.ascardlist()
    result = cardList
    hduList.close()
    if clArgs['--pydict']:
        thisDict = dft.convert_fits_header_to_dictionary(log, pathToFitsFile=pathToFitsFile)
        result = thisDict
    print result
    return