# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/cl_utils.py
# Compiled at: 2016-10-08 10:36:50
"""
*Parse and clean up webpage contents with options to print to PDF*

:Author:
    David Young

:Date Created:
    September 28, 2015

Usage:
    polygot [-oc] (pdf|html) <url> [<destinationFolder> -f <filename> -s <pathToSettingsFile>]

Options:
    pdf                   print webpage to pdf
    html                  parse and download webpage to a local HTML document

    -h, --help                                                      show this help message
    -v, --version                                                   show version
    -o, --open                                                      open the document after creation
    -c, --clean                                                     add polygot's clean styling to the output document
    <url>                                                           the url of the article's webpage
    -s <pathToSettingsFile>, --settings <pathToSettingsFile>        path to alternative settings file (optional)
    <destinationFolder>                                             the folder to save the parsed PDF or HTML document to (optional)
    -f <filename>, --filename <filename>                            the name of the file to save, otherwise use webpage title as filename (optional)
"""
import sys, os
os.environ['TERM'] = 'vt100'
import readline, glob, pickle
from subprocess import Popen, PIPE, STDOUT
from docopt import docopt
from fundamentals import tools, times
from polygot import printpdf
from polygot import htmlCleaner

def main(arguments=None):
    """
    *The main function used when ``cl_utils.py`` is run as a single script from the cl, or when installed as a cl command*
    """
    su = tools(arguments=arguments, docString=__doc__, logLevel='WARNING', options_first=False, projectName='polygot')
    arguments, settings, log, dbConn = su.setup()
    for arg, val in arguments.iteritems():
        if arg[0] == '-':
            varname = arg.replace('-', '') + 'Flag'
        else:
            varname = arg.replace('<', '').replace('>', '')
        if isinstance(val, str) or isinstance(val, unicode):
            exec varname + " = '%s'" % (val,)
        else:
            exec varname + ' = %s' % (val,)
        if arg == '--dbConn':
            dbConn = val
        log.debug('%s = %s' % (varname, val))

    startTime = times.get_now_sql_datetime()
    log.info('--- STARTING TO RUN THE cl_utils.py AT %s' % (
     startTime,))
    if not destinationFolder:
        destinationFolder = os.getcwd()
    if not filenameFlag:
        filenameFlag = False
    if not cleanFlag:
        readability = False
    else:
        readability = True
    if pdf:
        filepath = printpdf.printpdf(log=log, settings=settings, url=url, folderpath=destinationFolder, title=filenameFlag, append=False, readability=readability).get()
    if html:
        cleaner = htmlCleaner.htmlCleaner(log=log, settings=settings, url=url, outputDirectory=destinationFolder, title=filenameFlag, style=cleanFlag, metadata=True, h1=True)
        filepath = cleaner.clean()
    if openFlag:
        try:
            cmd = 'open %(filepath)s' % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass

        try:
            cmd = 'start %(filepath)s' % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass

    if 'dbConn' in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' % (
     endTime, runningTime))


if __name__ == '__main__':
    main()