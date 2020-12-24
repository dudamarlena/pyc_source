# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/webcrawlers.py
# Compiled at: 2013-08-06 05:24:11
"""
**webcrawlers**

Created by David Young on October 25, 2012
If you have any questions requiring this script please email me: d.r.young@qub.ac.uk

dryx syntax:
p<Var> = variable formated in the way I want it output to file or screen
xxx = come back here and do some more work

"""

def main():
    import pmCommonUtils as p
    dbConn, log = p.settings()
    log.info('----- STARTING TO RUN THE modulename -----')
    password_protected_page_downloader(dbConn, log)
    dbConn.commit()
    dbConn.close()
    log.info('----- FINISHED ATTEMPT TO RUN THE modulename -----')


def _fetch(url):
    import logging as log
    from eventlet.green import urllib2
    try:
        log.debug('downloading ' + url)
        body = urllib2.urlopen(url).read()
    except Exception as e:
        log.debug('could not download ' + url + ' : ' + str(e) + '\n')
        url = None
        body = None

    return (url, body)


def _dump_files_to_local_drive(bodies, theseUrls, dbConn, log):
    """takes the files stored in memory and dumps them to the local drive

      ****Key Arguments:****
        - ``bodies`` -- array of file data (currently stored in memory)
        - ``theseUrls`` -- array of local files paths to dump the file data into
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger

      **Return:**
        - ``None``
  """
    j = 0
    log.debug('attempting to write file data to local drive')
    log.debug('10 URLS = %s' % (str(theseUrls),))
    for body in bodies:
        try:
            if theseUrls[j]:
                with open(theseUrls[j], 'w') as (f):
                    f.write(body)
                f.close()
            j += 1
        except Exception as e:
            log.error('could not write downloaded file to local drive - failed with this error %s: ' % (str(e),))
            return -1


def multiWebDocumentDownloader(urlList, downloadDirectory, log, dbConn, timeStamp=1, timeout=180, concurrentDownloads=10):
    """get multiple url documents and place in specified download directory

      ****Key Arguments:****
        - ``urlList`` -- list of document urls
        - ``downloadDirectory`` -- directory to download the documents to

      **Return:**
        - list of timestamped documents (same order as the input urlList)
  """
    import sys, os, eventlet
    from eventlet.green import urllib2
    import dryxPython.commonutils, socket, re
    socket.setdefaulttimeout(timeout)
    thisArray = []
    bodies = []
    localUrls = []
    theseUrls = []
    for url in urlList:
        filename = commonutils.extract_filename_from_url(log, url)
        if timeStamp:
            filename = commonutils.append_now_datestamp_to_filename(log, filename)
        localFilepath = downloadDirectory + '/' + filename
        thisArray.extend([[url, localFilepath]])

    pool = eventlet.GreenPool(concurrentDownloads)
    i = 0
    try:
        log.debug('starting mutli-threaded download batch - %s concurrent downloads' % (concurrentDownloads,))
        for url, body in pool.imap(_fetch, urlList):
            if body:
                bodies.extend([body])
                theseUrls.extend([thisArray[i][1]])
            else:
                theseUrls.extend([None])
                bodies.extend([None])
            if i % concurrentDownloads == 0:
                _dump_files_to_local_drive(bodies, theseUrls, dbConn, log)
                localUrls.extend(theseUrls)
                bodies = []
                theseUrls = []
            i += 1

    except eventlet.Timeout as e:
        log.error('something went wrong with the mutli-threaded download : ' + str(e) + '\n')

    _dump_files_to_local_drive(bodies, theseUrls, dbConn, log)
    localUrls.extend(theseUrls)
    return localUrls


def singleWebDocumentDownloader(url, downloadDirectory, log, dbConn, timeStamp):
    """get a url document and place in a specified directory

      ****Key Arguments:****
        - ``url`` -- document url
        - ``downloadDirectory`` -- download directory path
        - ``timeStamp`` -- boolean, add a timestamp the end of the document name

      **Return:**
        - path to the local document
  """
    import logging as log
    try:
        log.debug('converting single url to list and downloading')
        urlList = [url]
        localUrlList = multiWebDocumentDownloader(urlList, downloadDirectory, log, dbConn, timeStamp)
        filepath = localUrlList[0]
    except Exception as e:
        myError = 'could not convert single url to list and downloading : ' + str(e) + '\n'
        log.error(myError)

    return filepath


def password_protected_page_downloader(dbConn, log):
    """get a page that is behind HTTPS authentication password protection

  **Key Arguments:**
    - ``dbConn`` -- mysql database connection
    - ``log`` -- logger
    - ``___`` --

  **Return:**
    - None
  """
    import commands, urllib2
    theurl = 'https://groups.google.com/a/pessto.org/group/alerts/manage_members/alerts.csv'
    username = 'david.young'
    password = 'spac3d0ct0r'
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    pagehandle = urllib2.urlopen(theurl)
    return


if __name__ == '__main__':
    main()