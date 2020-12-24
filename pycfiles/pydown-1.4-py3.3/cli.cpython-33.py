# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pydown\cli.py
# Compiled at: 2013-05-17 13:38:40
# Size of source mod 2**32: 1572 bytes
import os, urllib.request, gzip

def originalCLI():
    print('Welcome to pydown!')
    print('This program is copyright 2013 Nathan2055, use is subject to the terms in the LICENSE.txt file included with the distribution.')
    print('-----')
    print('Welcome! Please enter the full path of your working directory:')
    dest = input()
    if dest != '':
        os.chdir(dest)
    cwd = os.getcwd()
    print('Your working directory is ' + cwd)
    print('Please enter the URL of the file you wish to download:')
    url = input()
    print('Would you like to compress the end result using gzip? (y/n)')
    willCompress = input()
    print('Downloading file...', end='')
    download = urllib.request.urlopen(url)
    filename = os.path.split(url)[(-1)]
    print('done!')
    if willCompress == 'y':
        print('Compressing and saving file...', end='')
        with gzip.open(filename + '.gz', 'wb') as (f):
            f.write(download.read())
        print('done!')
        print('Press enter to terminate')
        input()
    else:
        print('Saving to file...', end='')
        with open(filename, 'b+w') as (f):
            f.write(download.read())
        print('done!')
        print('Press enter to terminate')
        input()


originalCLI()