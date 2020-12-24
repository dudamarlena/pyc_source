# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/cat/__init__.py
# Compiled at: 2016-03-03 14:48:59
"""
Copyright (c) 2016, René Tanczos <gravmatt@gmail.com> (Twitter @gravmatt)
The MIT License (MIT)

cat is a amazing modul to get cat images. This Project won't be
posible without the great Cat API (http://thecatapi.com).
Big thanks!

Project on github https://github.com/gravmatt/random-cat
"""
__author__ = 'René Tanczos'
__version__ = '1.0.1'
__license__ = 'MIT'
import uuid, os, sys
download = None
try:
    import urllib
    download = urllib.urlretrieve
except:
    import urllib.request
    download = urllib.request.urlretrieve

url = 'https://thecatapi.com/api/images/get'

def getCat(directory=None, filename=None, format='png'):
    basename = '%s.%s' % (filename if filename else str(uuid.uuid4()), format)
    savefile = os.path.sep.join([directory.rstrip(os.path.sep), basename]) if directory else basename
    downloadlink = url + '?type=%s' % format
    download(downloadlink, savefile)
    return savefile


def main():
    format = 'png'
    filename = None
    directory = None
    if len(sys.argv) > 1:
        format = sys.argv[1]
        if format not in ('png', 'jpg', 'gif'):
            sys.stdout.write('Wrong format! Only png, jpg or gif')
            return
    if len(sys.argv) > 2:
        filename = sys.argv[2]
        directory = os.path.sep.join(filename.split(os.path.sep)[:-1])
        filename = os.path.basename(filename).split('.')[0]
    sys.stdout.write(getCat(directory, filename, format))
    return


if __name__ == '__main__':
    main()