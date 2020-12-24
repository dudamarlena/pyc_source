# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/ProvNFile.py
# Compiled at: 2018-05-07 08:52:54
# Size of source mod 2**32: 841 bytes
from fastr.datatypes import URLType

class ProvNFile(URLType):
    description = 'Provenance file in the prov N format'
    extension = 'provn'