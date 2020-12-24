# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/image/v1/index.py
# Compiled at: 2019-11-06 08:31:54
# Size of source mod 2**32: 1888 bytes
from opencontainers.struct import Struct
from opencontainers.image.specs import Versioned
from opencontainers.logger import bot
from .mediatype import MediaTypeImageIndex, MediaTypeImageManifest
from .descriptor import Descriptor

class Index(Struct):
    __doc__ = 'Index references manifests for various platforms.\n       This structure provides `application/vnd.oci.image.index.v1+json` \n       mediatype when marshalled to JSON.\n    '

    def __init__(self, manifests=None, schemaVersion=None, annotations=None):
        super().__init__()
        self.newAttr(name='schemaVersion', attType=Versioned, required=True)
        self.newAttr(name='Manifests', attType=[Descriptor], jsonName='manifests', required=True)
        self.newAttr(name='Annotations', attType=dict, jsonName='annotations')
        self.add('Manifests', manifests)
        self.add('Annotations', annotations)
        self.add('schemaVersion', schemaVersion)

    def _validate(self):
        """custom validation function to ensure that Manifests mediaTypes
           are valid.
        """
        valid_types = [
         MediaTypeImageManifest, MediaTypeImageIndex]
        manifests = self.attrs.get('Manifests').value
        if manifests:
            for manifest in manifests:
                mediaType = manifest.attrs.get('MediaType')
                if mediaType.value not in valid_types:
                    bot.error('%s is not valid for index manifest.' % mediaType)
                    return False

        return True