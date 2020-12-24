# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gapml/pdf_res.py
# Compiled at: 2018-08-31 14:33:57
# Size of source mod 2**32: 1895 bytes
"""
Copyright 2018(c), Andrew Ferlitsch
"""
import os.path

class PDFResource(object):
    __doc__ = ' Parse the Resource Definition of a PDF File '
    PAGES = 1

    def __init__(self, document, debug=False):
        self._debug = debug
        if os.path.isfile(document) == False:
            raise FileNotFoundError(document)
        self._document = document
        with open(document, 'rb') as (f):
            self._magic = f.read(5)
            if self._magic != b'%PDF-':
                raise ValueError('%PDF not found')
            self._version = f.read(3)
            if self._debug:
                print('PDF Version', str(self._version.decode('utf-8')))
            self._text = self._image = False
            while 1:
                try:
                    line = f.readline().decode()
                except:
                    continue

                if line.startswith('/Resources<</ProcSet[/PDF'):
                    resources = line[25:]
                    if self._debug:
                        print('resources', resources)
                    if '/Text' in resources:
                        self._text = True
                    if '/ImageB' in resources or '/ImageC' in resources or '/ImageI' in resources:
                        self._image = True
                    break

    @property
    def version(self):
        """ Get the PDF version """
        return self._version

    @property
    def text(self):
        """ Get whether the page contains text """
        return self._text

    @property
    def image(self):
        """ Get whether the page contains an image """
        return self._image


import sys
if __name__ == '__main__':
    p = PDFResource(sys.argv[1])
    print('Text', p.text)
    print('Image', p.image)