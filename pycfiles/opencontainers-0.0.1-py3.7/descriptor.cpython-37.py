# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/image/v1/descriptor.py
# Compiled at: 2019-11-06 10:26:59
# Size of source mod 2**32: 3487 bytes
from opencontainers.struct import Struct
from opencontainers.digest import Digest

class Descriptor(Struct):
    __doc__ = 'Descriptor describes the disposition of targeted content.\n       This structure provides `application/vnd.oci.descriptor.v1+json`\n       mediatype when marshalled to JSON.\n    '

    def __init__(self, digest=None, size=None, mediatype=None, urls=None, annotations=None, platform=None):
        super().__init__()
        regexp = '^[A-Za-z0-9][A-Za-z0-9!#$&-^_.+]{0,126}/[A-Za-z0-9][A-Za-z0-9!#$&-^_.+]{0,126}$'
        self.newAttr(name='MediaType', attType=str, jsonName='mediaType', regexp=regexp)
        self.newAttr(name='Digest', attType=Digest, jsonName='digest', required=True)
        self.newAttr(name='Size', attType=int, jsonName='size', required=True)
        self.newAttr(name='URLs', attType=[str], jsonName='urls')
        self.newAttr(name='Annotations', attType=dict, jsonName='annotations')
        self.newAttr(name='Platform', attType=Platform, jsonName='platform')
        self.add('Digest', digest)
        self.add('Size', size)
        self.add('MediaType', mediatype)
        self.add('URLs', urls)
        self.add('Annotations', annotations)
        self.add('Platform', platform)


class Platform(Struct):
    __doc__ = 'Platform describes the platform which the image in the manifest runs on.\n    '

    def __init__(self, arch=None, platform_os=None, os_version=None, os_features=None, variant=None):
        super().__init__()
        self.newAttr(name='Architecture', attType=str, jsonName='architecture', required=True)
        self.newAttr(name='OS', attType=str, jsonName='os', required=True)
        self.newAttr(name='OSVersion', attType=str, jsonName='os.version')
        self.newAttr(name='OSFeatures', attType=[str], jsonName='os.features')
        self.newAttr(name='Variant', attType=str, jsonName='variant')
        self.add('Architecture', arch)
        self.add('OS', platform_os)
        self.add('OSVersion', os_version)
        self.add('OSFeatures', os_features)
        self.add('Variant', variant)