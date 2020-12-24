# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/download/multiobject_download.py
# Compiled at: 2020-04-17 06:44:40
"""
*Download resources from a list of URLs. 

There are options to rename all the downloaded resource, index the files, set differing download locations and pass basic authentication credentials.*

:Author:
    David Young
"""
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import str
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
import urllib

def multiobject_download(urlList, downloadDirectory, log, timeStamp=True, timeout=180, concurrentDownloads=10, resetFilename=False, credentials=False, longTime=False, indexFilenames=False):
    """
    *get multiple url documents and place them in specified download directory/directories*

    **Key Arguments**

    
      - ``urlList`` -- list of document urls
      - ``downloadDirectory`` -- directory(ies) to download the documents to - can be one directory path or a list of paths the same length as urlList
      - ``log`` -- the logger
      - ``timestamp`` -- append a timestamp the name of the URL (ensure unique filenames)
      - ``longTime`` -- use a longer timestamp when appending to the filename (greater uniqueness)
      - ``timeout`` -- the timeout limit for downloads (secs)
      - ``concurrentDownloads`` -- the number of concurrent downloads allowed at any one time
      - ``resetFilename`` -- a string to reset all filenames to
      - ``credentials`` -- basic http credentials { 'username' : "...", "password", "..." }
      - ``indexFilenames`` -- prepend filenames with index (where url appears in urllist)

    **Return**

    
      - list of timestamped documents (same order as the input urlList)

    **Usage**

    ```python
    # download the pages linked from the main list page
    from fundamentals.download import multiobject_download
    localUrls = multiobject_download(
        urlList=["https://www.python.org/dev/peps/pep-0257/","https://en.wikipedia.org/wiki/Docstring"],
        downloadDirectory="/tmp",
        log="log",
        timeStamp=True,
        timeout=180,
        concurrentDownloads=2,
        resetFilename=False,
        credentials=False,  # { 'username' : "...", "password", "..." }
        longTime=True
    )

    print localUrls
    # OUT: ['/tmp/untitled_20160316t160650610780.html', '/tmp/Docstring_20160316t160650611136.html']
    ```

    .. image:: https://i.imgur.com/QYoMm24.png width=600px
    
    """
    import sys, os, eventlet, socket, re, base64
    from fundamentals.download import _fetch, _dump_files_to_local_drive, append_now_datestamp_to_filename, extract_filename_from_url
    timeout = float(timeout)
    socket.setdefaulttimeout(timeout)
    thisArray = []
    bodies = []
    localUrls = []
    theseUrls = []
    requestList = []
    totalCount = len(urlList)
    if isinstance(downloadDirectory, (('').__class__, ('').__class__)):
        for i, url in enumerate(urlList):
            if resetFilename and len(resetFilename):
                filename = resetFilename[i]
            else:
                filename = extract_filename_from_url(log, url)
                if indexFilenames:
                    filename = '%(i)03d_%(filename)s' % locals()
            if not filename:
                from datetime import datetime, date, time
                now = datetime.now()
                filename = now.strftime('%Y%m%dt%H%M%S%f')
            if timeStamp:
                filename = append_now_datestamp_to_filename(log, filename, longTime=longTime)
            localFilepath = downloadDirectory + '/' + filename
            thisArray.extend([[url, localFilepath]])
            request = urllib.request.Request(url)
            if credentials != False:
                username = credentials['username']
                password = credentials['password']
                base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
                request.add_header('Authorization', 'Basic %s' % base64string)
            requestList.append(request)

    else:
        if isinstance(downloadDirectory, list):
            for u, d in zip(urlList, downloadDirectory):
                if resetFilename:
                    filename = resetFilename
                else:
                    filename = extract_filename_from_url(log, url)
                if not filename:
                    continue
                if timeStamp:
                    filename = append_now_datestamp_to_filename(log, filename)
                localFilepath = d + '/' + filename
                thisArray.extend([[u, localFilepath]])
                log.debug(' about to download %s' % (u,))
                request = urllib.request.Request(u)
                if credentials != False:
                    log.debug('adding the credentials')
                    username = credentials['username']
                    password = credentials['password']
                    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
                    request.add_header('Authorization', 'Basic %s' % base64string)
                requestList.append(request)

        pool = eventlet.GreenPool(concurrentDownloads)
        i = 0
        try:
            log.debug('starting mutli-threaded download batch - %s concurrent downloads' % (
             concurrentDownloads,))
            log.debug('len(requestList): %s' % (len(requestList),))
            for url, body in pool.imap(_fetch, requestList):
                urlNum = i + 1
                if urlNum > 1:
                    sys.stdout.write('\x1b[1A\x1b[2K')
                percent = float(urlNum) / float(totalCount) * 100.0
                print('  %(urlNum)s / %(totalCount)s (%(percent)1.1f%%) URLs downloaded' % locals())
                if body:
                    bodies.extend([body])
                    theseUrls.extend([thisArray[i][1]])
                else:
                    theseUrls.extend([None])
                    bodies.extend([None])
                if i % concurrentDownloads == 0:
                    _dump_files_to_local_drive(bodies, theseUrls, log)
                    localUrls.extend(theseUrls)
                    bodies = []
                    theseUrls = []
                i += 1

        except Exception as e:
            log.error('something went wrong with the mutli-threaded download : ' + str(e) + '\n')

    _dump_files_to_local_drive(bodies, theseUrls, log)
    localUrls.extend(theseUrls)
    return localUrls