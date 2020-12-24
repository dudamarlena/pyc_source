# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydown\__init__.py
# Compiled at: 2013-06-19 21:05:16
# Size of source mod 2**32: 2046 bytes
import os, urllib.request, gzip

def download(url):
    cwd = os.getcwd()
    filename = os.path.split(url)[(-1)]
    print('Downloading ' + url + ' to ' + cwd)
    print('y/n?')
    yn = input()
    if yn == 'y':
        download = urllib.request.urlopen(url)
        with open(filename, 'b+w') as (f):
            f.write(download.read())
        print('Press enter to terminate')
        input()
    else:
        print('Download cancelled.')
        print('Press enter to terminate')
        input()


def printDownload(url):
    cwd = os.getcwd()
    filename = os.path.split(url)[(-1)]
    print('Downloading ' + url + ' to ' + cwd)
    download = urllib.request.urlopen(url)
    with open(filename, 'b+w') as (f):
        f.write(download.read())


def printDownload(url):
    cwd = os.getcwd()
    filename = os.path.split(url)[(-1)]
    download = urllib.request.urlopen(url)
    with open(filename, 'b+w') as (f):
        f.write(download.read())