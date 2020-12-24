# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/TifImageFile.py
# Compiled at: 2019-04-10 08:38:03
from fastr.datatypes import URLType

class TifImageFile(URLType):
    description = 'Tif Image File format'
    extension = ('tiff', 'tif')