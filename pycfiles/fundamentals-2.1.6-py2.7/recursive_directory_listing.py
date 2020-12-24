# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/files/recursive_directory_listing.py
# Compiled at: 2020-04-17 06:44:40
"""
*List the contents of a directory recursively*

:Author:
    David Young
"""
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools

def recursive_directory_listing(log, baseFolderPath, whatToList='all'):
    """*list directory contents recursively.*

    Options to list only files or only directories.

    **Key Arguments**

    - ``log`` -- logger
    - ``baseFolderPath`` -- path to the base folder to list contained files and folders recursively
    - ``whatToList`` -- list files only, durectories only or all [ "files" | "dirs" | "all" ]
    

    **Return**

    - ``matchedPathList`` -- the matched paths
    

    **Usage**

    ```python
    from fundamentals.files import recursive_directory_listing
    theseFiles = recursive_directory_listing(
        log,
        baseFolderPath="/tmp"
    )

    # OR JUST FILE  

    from fundamentals.files import recursive_directory_listing
    theseFiles = recursive_directory_listing(
        log,
        baseFolderPath="/tmp",
        whatToList="files"
    )

    # OR JUST FOLDERS   

    from fundamentals.files import recursive_directory_listing
    theseFiles = recursive_directory_listing(
        log,
        baseFolderPath="/tmp",
        whatToList="dirs"
    )
    print theseFiles        
    ```
    """
    log.debug('starting the ``recursive_directory_listing`` function')
    matchedPathList = []
    parentDirectoryList = [
     baseFolderPath]
    count = 0
    while os.listdir(baseFolderPath) and count < 20:
        count += 1
        while len(parentDirectoryList) != 0:
            childDirList = []
            for parentDir in parentDirectoryList:
                try:
                    thisDirList = os.listdir(parentDir)
                except Exception as e:
                    log.error(e)
                    continue

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

    log.debug('completed the ``recursive_directory_listing`` function')
    return matchedPathList