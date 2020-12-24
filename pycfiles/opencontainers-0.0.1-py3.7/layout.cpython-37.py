# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/image/v1/layout.py
# Compiled at: 2019-11-05 17:20:36
# Size of source mod 2**32: 1026 bytes
from opencontainers.struct import Struct
ImageLayoutFile = 'oci-layout'
ImageLayoutVersion = '1.0.0'

class ImageLayout(Struct):
    __doc__ = 'ImageLayout is the structure in the "oci-layout" file, found in the root \n       of an OCI Image-layout directory.\n    '

    def __init__(self, version=None):
        super().__init__()
        regexp = '^(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patchlevel>\\d+)~?(?P<special>[a-z]\\w+[\\d+])?$'
        self.newAttr(name='Version', attType=str, jsonName='imageLayoutVersion', required=True,
          regexp=regexp)
        self.add('Version', version or ImageLayoutVersion)