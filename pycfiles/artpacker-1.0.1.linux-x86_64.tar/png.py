# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/artpacker/saver/png.py
# Compiled at: 2012-05-29 14:37:19
from artpacker.saver import Saver

class PNGSaver(Saver):

    def __init__(self, output_path, filename_prefix):
        Saver.__init__(self, 'png', output_path, filename_prefix)

    def save_file(self, image, filename):
        image.save(filename, optimize=True)