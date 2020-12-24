# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/mmd/mmd.py
# Compiled at: 2013-09-19 10:36:45
"""
mmd.py
===========
:Summary:
    My MMD helpers

:Author:
    David Young

:Date Created:
    September 19, 2013

:dryx syntax:
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script please email me: d.r.young@qub.ac.uk

:Tasks:
    @review: when complete add cl commands
    @review: make internal function private
    @review: pull all general functions and classes into dryxPython
"""
import sys, os

def convert_to_html(log, pathToMMDFile, css='amblin'):
    """convert mmd file to html

    **Key Arguments:**

    **Return:**
        - ``pathToHtmlFile`` -- the path to the html file

    **Todo**
        - @review: when complete, clean convert_to_html function
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract function to another module
    """
    from subprocess import Popen, PIPE
    log.info('starting the ``convert_to_html`` function')
    cssFile = os.path.dirname(__file__) + '/assets/%s.css' % (css,)
    pathToReadFile = cssFile
    try:
        log.debug('attempting to open the file %s' % (pathToReadFile,))
        readFile = open(pathToReadFile, 'r')
        cssData = readFile.read()
    except IOError as e:
        message = 'could not open the file %s' % (pathToReadFile,)
        log.critical(message)
        raise IOError(message)

    readFile.close()
    pathToHtmlFile = pathToMMDFile
    for ext in ['.md', '.mmd', '.markdown', '.txt', '.dat']:
        pathToHtmlFile = pathToHtmlFile.replace(ext, '.html')

    pathToReadFile = pathToMMDFile
    try:
        log.debug('attempting to open the file %s' % (pathToReadFile,))
        readFile = open(pathToReadFile, 'r')
        thisData = readFile.read()
    except IOError as e:
        message = 'could not open the file %s' % (pathToReadFile,)
        log.critical(message)
        raise IOError(message)

    readFile.close()
    basename = os.path.basename(pathToMMDFile)
    filenameNoExtension = os.path.splitext(basename)[0]
    if 'Filename: `%s`' % (filenameNoExtension,) not in thisData:
        thisData = 'Filename: %s\n\n%s' % (filenameNoExtension, thisData)
        pathToWriteFile = pathToMMDFile
        try:
            log.debug('attempting to open the file %s' % (pathToWriteFile,))
            writeFile = open(pathToWriteFile, 'w')
        except IOError as e:
            message = 'could not open the file %s' % (pathToWriteFile,)
            log.critical(message)
            raise IOError(message)

        writeFile.write(thisData)
        writeFile.close()
    mmdBinary = os.path.dirname(__file__) + '/assets/mmd'
    process = Popen([mmdBinary, pathToMMDFile], stdout=PIPE)
    stdout, stderr = process.communicate()
    pathToReadFile = pathToHtmlFile
    try:
        log.debug('attempting to open the file %s' % (pathToReadFile,))
        readFile = open(pathToReadFile, 'r')
        thisData = readFile.read()
    except IOError as e:
        message = 'could not open the file %s' % (pathToReadFile,)
        log.critical(message)
        raise IOError(message)

    readFile.close()
    thisData = thisData.replace('<body>', '<style>%s</style><body><div id="wrapper">' % (cssData,))
    thisData = thisData.replace('</body>', '</div></body>')
    pathToWriteFile = pathToHtmlFile
    try:
        log.debug('attempting to open the file %s' % (pathToWriteFile,))
        writeFile = open(pathToWriteFile, 'w')
    except IOError as e:
        message = 'could not open the file %s' % (pathToWriteFile,)
        log.critical(message)
        raise IOError(message)

    writeFile.write(thisData)
    writeFile.close()
    log.info('completed the ``convert_to_html`` function')
    return pathToHtmlFile


if __name__ == '__main__':
    main()