# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/commonutils.py
# Compiled at: 2013-08-17 16:36:58
"""
**commonutils**

A collection of miscellaneous useful utilities

| Initially created by David Young on October 8, 2012
| If you have any questions requiring this script please email me: d.r.young@qub.ac.uk

dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging
"""

def main():
    print get_current_mjd()


def get_now_datetime_filestamp():
    """A datetime stamp to be appended to the end of filenames:
        ``YYYYMMDDtHHMMSS``

        **Return:**
            - ``now`` -- current time and date in filename format
    """
    from datetime import datetime, date, time
    now = datetime.now()
    now = now.strftime('%Y%m%dt%H%M%S')
    return now


def get_now_sql_datetime():
    """A datetime stamp in MySQL format:
        ``YYYY-MM-DDTHH:MM:SS``

        **Return:**
            - ``now`` -- current time and date in MySQL format
    """
    from datetime import datetime, date, time
    now = datetime.now()
    now = now.strftime('%Y-%m-%dT%H:%M:%S')
    return now


def make_lowercase_nospace(theString):
    """Convert a string to a neatly formated filename type - no space, commas, lowercase etc

            **Key Arguments:**
                - ``theString`` -- the string to be made pretty

            **Return:**
                - ``prettyString`` -- the formatted string
    """
    x = theString.replace(' ', '_').strip()
    x = x.replace(',', '_').strip()
    x = x.lower()
    prettyString = x
    return prettyString


def extract_filename_from_url(log, url):
    """
        get the filename from a URL.
        Will return '*untitled.html*', if no filename is found.

        **Key Arguments:**
            - ``url`` -- the url to extract filename from

        Returns:
            - ``filename`` -- the filename
    """
    import re
    try:
        log.debug('extracting filename from url ' + url)
        reEoURL = re.compile('([\\w\\.]*)$')
        filename = reEoURL.findall(url)[0]
        if len(filename) == 0:
            filename = 'untitled.html'
        if not re.search('\\.', filename):
            filename = filename + '.html'
    except Exception as e:
        log.error('could not extracting filename from url : ' + str(e) + '\n')

    return filename


def append_now_datestamp_to_filename(log, filename):
    """append the current datestamp to the end of the filename (before the extension).

            **Key Arguments:**
                - ``filename`` -- the filename

            Return:
                - ``dsFilename`` -- datestamped filename
    """
    try:
        sliced = filename.split('.')
        dsFilename = sliced[0] + '_' + get_now_datetime_filestamp()
        if len(sliced) == 2:
            dsFilename += '.' + sliced[1]
        else:
            dsFilename += '.xhtml'
    except Exception as e:
        log.error('could not append date stamp to the filename : ' + filename + ' : ' + str(e) + '\n')

    return dsFilename


def pretty_date(date):
    """convert date to a relative datetime (e.g. +15m, +2hr, +1w)

    **Key Arguments:**
        - ``date`` -- absolute date

    **Return:**
        - a relative date
    """
    from datetime import datetime
    diff = datetime.now() - date
    s = diff.seconds
    if diff.days == 1:
        return ' + 1d'
    else:
        if diff.days > 1:
            return (' +{0}d').format(diff.days)
        if s <= 1:
            return ' just now'
        if s < 60:
            return (' +{0}sec').format(s)
        if s < 120:
            return ' +1min'
        if s < 3600:
            return (' +{0}min').format(s / 60)
        if s < 7200:
            return ' +1hr'
        return (' +{0}hr').format(s / 3600)


def calculate_time_difference(startDate, endDate):
    """Return the time difference between two dates

    **Key Arguments:**
        - ``startDate`` -- the first date in YYYY-MM-DDTHH:MM:SS format
        - ``endDate`` -- the final date YYYY-MM-DDTHH:MM:SS format

    **Return:**
        - ``diffDate`` -- the difference between the two dates in Y,M,D,h,m,s (string)
    """
    from datetime import datetime
    from dateutil import relativedelta
    startDate = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
    endDate = datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S')
    d = relativedelta.relativedelta(endDate, startDate)
    relTime = ''
    if d.years > 0:
        relTime += str(d.years) + 'yrs '
    if d.months > 0:
        relTime += str(d.months) + 'mths '
    if d.days > 0:
        relTime += str(d.days) + 'dys '
    if d.hours > 0:
        relTime += str(d.hours) + 'h '
    if d.minutes > 0:
        relTime += str(d.minutes) + 'm '
    if d.seconds > 0:
        relTime += str(d.seconds) + 's'
    return relTime


def dryx_mkdir(log, directoryPath):
    """Create a directory if it does not yet exist

            **Key Arguments:**
                - ``directoryPath`` -- absolute/relative path to required directory

            **Return:**
                - ``None``
    """
    import os
    if not os.path.exists(directoryPath):
        try:
            log.debug('creating the ' + directoryPath + ' d i rectory')
            os.mkdir(directoryPath)
        except Exception as e:
            log.error('could not create the ' + directoryPath + ' directory' + str(e) + '\n')

    else:
        log.debug(directoryPath + ' directory already exists')
    return


def strip_whitespace_from_dictionary_values(log, dictionary):
    """Strip the leading and trailing whitespace from dictionary values and returns the cleaned up dictionary

    **Key Arguments:**
        - ``log`` -- logger
        - ``dictionary`` -- dictionary to be cleaned

    Return:
        - ``dictionary`` -- cleaned dictionary
    """
    if len(dictionary) != 0:
        for k in dictionary.keys():
            if isinstance(dictionary[k].value, basestring):
                try:
                    log.debug('attempting to strip whitespace from dictionary values')
                    dictionary[k].value = dictionary[k].value.strip()
                except Exception as e:
                    log.error('could not strip whitespace from dictionary values - failed with this error %s: ' % (str(e),))
                    return -1

    return dictionary


def get_current_mjd():
    """Get the current datetime as MJD

    **Key Arguments:**
        - ``None``

    **Return:**
        - ``MJD`` -- Current datetime as MJD
    """
    from datetime import datetime
    import time
    mjd = None
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    try:
        year, month, day = now[0:10].split('-')
        hours, minutes, seconds = now[11:19].split(':')
        t = (int(year), int(month), int(day),
         int(hours), int(minutes), int(seconds), 0, 0, 0)
        unixtime = int(time.mktime(t))
        mjd = unixtime / 86400.0 - 2400000.5 + 2440587.5
    except ValueError as e:
        mjd = None
        print 'String is not in SQL Date format.'

    return mjd


def add_directories_to_path(directoryPath, log):
    """add a directories to the system path

    **Key Arguments:**
        - ``directoryPath`` -- the path to the directory containing the directories you want to add to the system path
        - ``log`` -- logger

    **Return:**
        - None
    """
    import sys, os
    for d in os.listdir(directoryPath):
        fullPath = os.path.join(directoryPath, d)
        if os.path.isdir(os.path.join(directoryPath, d)):
            sys.path.append(fullPath)


def recusively_add_directories_to_path(directoryPath, log):
    """add contents of a directory **recusively** to the system path

    **Key Arguments:**
           - ``directoryPath`` -- the path to the directory containing the directories you want to recusively add to the system path

    **Return:**
        - None
    """
    import sys
    add_directories_to_path(directoryPath)
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


def get_python_module_partials(pathToModuleFile, log):
    """Get the names of the _partials imported into dryx python modules.

    **Key Arguments:**
        - ``pathToModuleFile`` -- the path to the python module we wish to extract the _partial names for
        - ``log`` -- logger

    **Return:**
        - ``partialsDictionary`` -- a dictionary of the _partial names imported into the dryx python module, and a list of their functions

    **Todo**
    - [ ] when complete, clean get_python_module_partials function & add logging
    """
    from modulefinder import ModuleFinder
    import re, os, sys
    log.info('starting the ``get_python_module_partials`` function')
    partialsDictionary = {}
    finder = ModuleFinder()
    finder.run_script(pathToModuleFile)
    baseName = os.path.basename(pathToModuleFile).replace('.py', '')
    if baseName == '__init__':
        pathToModuleFile = pathToModuleFile.replace('__init__.py', '')
        baseName = os.path.basename(pathToModuleFile)
    reBaseName = re.compile('%s' % (baseName,))
    for name, mod in finder.modules.iteritems():
        if reBaseName.search(name):
            importList = []
            for key in mod.globalnames.keys():
                if '/Users/' not in mod.__file__:
                    continue
                importList.append(key)

            if len(importList):
                partialsDictionary[name] = importList

    log.info('completed the ``get_python_module_partials`` function')
    return partialsDictionary


def get_recursive_list_of_directory_contents(log, baseFolderPath, whatToList='all'):
    """list directory contents recursively.

    Options to list only files or only directories.

    **Key Arguments:**
        - ``log`` -- logger
        - ``baseFolderPath`` -- path to the base folder to list contained files and folders recursively
        - ``whatToList`` -- list files only, durectories only or all [ "files" | "dirs" | "all" ]

    **Return:**
        - ``matchedPathList`` -- the matched paths
    """
    import os
    log.info('starting the ``get_recursive_list_of_directory_contents`` function')
    matchedPathList = []
    parentDirectoryList = [
     baseFolderPath]
    count = 0
    while os.listdir(baseFolderPath) and count < 20:
        count += 1
        while len(parentDirectoryList) != 0:
            childDirList = []
            for parentDir in parentDirectoryList:
                thisDirList = os.listdir(parentDir)
                for d in thisDirList:
                    fullPath = os.path.join(parentDir, d)
                    if whatToList is 'all':
                        matched = True
                    elif whatToList is 'dirs':
                        matched = os.path.isdir(fullPath)
                    elif whatToList is 'files':
                        matched = os.path.isfile(fullPath)
                    else:
                        log.error('cound not list files in %s, `whatToList` variable incorrect: [ "files" | "dirs" | "all" ]' % (baseFolderPath,))
                        sys.exit(0)
                    if matched:
                        matchedPathList.append(fullPath)
                    if os.path.isdir(fullPath):
                        childDirList.append(fullPath)

                parentDirectoryList = childDirList

    log.info('completed the ``get_recursive_list_of_directory_contents`` function')
    return matchedPathList


def get_help_for_python_module(pathToModuleFile, log):
    """print the help for python module

    **Key Arguments:**
        - ``pathToModuleFile`` -- the path to the python module
        - ``log`` -- logger

    **Return:**
        - None

    **Todo**
        - [ ] when complete, clean get_help_for_python_module function
        - [ ] when complete add logging
        - [ ] when complete, decide whether to abstract function to another module
    """
    log.info('starting the ``get_help_for_python_module`` function')
    basename = os.path.basename(pathToModuleFile).replace('.py')
    print basename
    log.info('completed the ``get_help_for_python_module`` function')
    return


if __name__ == '__main__':
    main()