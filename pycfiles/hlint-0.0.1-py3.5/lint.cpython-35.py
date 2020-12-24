# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hlint/lint.py
# Compiled at: 2018-08-22 12:52:40
# Size of source mod 2**32: 7126 bytes
from __future__ import print_function, with_statement
import os, sys, re, string, gzip
try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO

try:
    maketrans = str.maketrans
except AttributeError:
    maketrans = string.maketrans

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Result(object):

    def __init__(self, file_name='', message='', flag=False):
        self.file_name = file_name
        self.message = message
        self.flag = flag

    def __str__(self):
        return self.message


class Results(object):

    def __init__(self, data={}, file_list=[]):
        self.total_error_count = len(data)
        self.file_list = file_list
        self.data = data

    def __str__(self):
        message = ''
        for key, value in self.data.items():
            message += '{name}\n===========\n{value}\n'.format(name=key, value=value)

        return message


def valid(fileName):
    extPat = re.compile('^.*\\.([A-Za-z]+)$')
    extDict = {'html': 'text/html', 
     'htm': 'text/html', 
     'xhtml': 'application/xhtml+xml', 
     'xht': 'application/xhtml+xml', 
     'xml': 'application/xml'}
    forceXml = False
    forceHtml = False
    gnu = False
    errorsOnly = False
    encoding = None
    contentType = None
    inputHandle = None
    service = 'https://html5.validator.nu/'
    if forceXml and forceHtml:
        msg = 'Cannot force HTML and XHTML at the same time.'
        return (
         False, msg)
    if forceXml:
        contentType = 'application/xhtml+xml'
    else:
        if forceHtml:
            contentType = 'text/html'
        else:
            if fileName:
                m = extPat.match(os.path.join(BASE_DIR, fileName))
                if m:
                    ext = m.group(1)
                    ext = ext.translate(maketrans(string.ascii_uppercase, string.ascii_lowercase))
                    if ext in extDict:
                        contentType = extDict[ext]
                    else:
                        msg = 'Unable to guess Content-Type from file name'
                        return (False, msg)
                else:
                    msg = 'Could not extract a filename extension'
                    return (False, msg)
            else:
                msg = 'Need to force HTML or XHTML when reading from stdin'
                return (False, msg)
            if encoding:
                contentType = '%s; charset=%s' % (contentType, encoding)
            if fileName:
                inputHandle = fileName
            else:
                inputHandle = sys.stdin
        with open(inputHandle, mode='rb') as (inFile):
            data = inFile.read()
            with BytesIO() as (buf):
                zipFile = gzip.GzipFile(fileobj=buf, mode='wb')
                zipFile.write(data)
                zipFile.close()
                gzippeddata = buf.getvalue()
        url = service
        if gnu:
            url = url + '?out=gnu'
        else:
            url = url + '?out=text'
    if errorsOnly:
        url = url + '&level=error'
    connection = None
    response = None
    status = 302
    redirectCount = 0
    while status in (302, 301, 307) and redirectCount < 10:
        if redirectCount > 0:
            url = response.getheader('Location')
        parsed = urlparse.urlsplit(url)
        if redirectCount > 5:
            return (False, 'Failed to make connection!')
        if parsed.scheme == 'https':
            connection = httplib.HTTPSConnection(parsed[1])
        else:
            connection = httplib.HTTPConnection(parsed[1])
        headers = {'Accept-Encoding': 'gzip', 
         'Content-Type': contentType, 
         'Content-Encoding': 'gzip', 
         'Content-Length': len(gzippeddata), 
         'User-Agent': 'html5check'}
        urlSuffix = '%s?%s' % (parsed[2], parsed[3])
        connection.connect()
        connection.request('POST', urlSuffix, body=gzippeddata, headers=headers)
        response = connection.getresponse()
        status = response.status
        redirectCount += 1

    if status != 200:
        msg = '%s %s' % (status, response.reason)
        return (
         False, msg)
    if response.getheader('Content-Encoding', 'identity').lower() == 'gzip':
        response = gzip.GzipFile(fileobj=BytesIO(response.read()))
    if fileName and gnu:
        quotedName = '"%s"' % fileName.replace("'", '\\042')
        for line in response.read().split('\n'):
            if line:
                sys.stdout.write(quotedName)
                sys.stdout.write(line + '\n')

    else:
        output = response.read()
        if not isinstance(output, str):
            output = output.decode('utf-8')
        if output.strip() == 'The document is valid HTML5 + ARIA + SVG 1.1 + MathML 2.0 (subject to the utter previewness of this service).':
            connection.close()
            return (
             True, '{name} is clean!'.format(name=fileName))
        else:
            connection.close()
            return (False, str(output))


def check(file):
    flag, message = valid(file)
    result = Result(file_name=file, message=message, flag=flag)
    return result


def check_files(file_list):
    data = {}
    for f in file_list:
        flag, message = valid(f)
        if not flag:
            data[f] = message

    results = Results(data=data, file_list=file_list)
    return results