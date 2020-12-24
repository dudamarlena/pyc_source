# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/image/v1/manifest.py
# Compiled at: 2019-11-04 17:20:25
# Size of source mod 2**32: 3739 bytes
from opencontainers.struct import Struct
from opencontainers.image.specs import Versioned
from opencontainers.logger import bot
from .descriptor import Descriptor
from .mediatype import MediaTypeImageConfig, MediaTypeImageLayer, MediaTypeImageLayerGzip, MediaTypeImageLayerZstd, MediaTypeImageLayerNonDistributable, MediaTypeImageLayerNonDistributableGzip, MediaTypeImageLayerNonDistributableZstd

class Manifest(Struct):
    __doc__ = 'Manifest provides `application/vnd.oci.image.manifest.v1+json` \n       mediatype structure when marshalled to JSON.\n    '

    def __init__(self, manifestConfig=None, layers=None, schemaVersion=None, annotations=None):
        super().__init__()
        self.newAttr(name='schemaVersion', attType=Versioned, required=True)
        self.newAttr(name='Config', attType=Descriptor, jsonName='config', required=True)
        self.newAttr(name='Layers', attType=[Descriptor], jsonName='layers', required=True)
        self.newAttr(name='Annotations', attType=dict, jsonName='annotations')
        self.add('Config', manifestConfig)
        self.add('Layers', layers)
        self.add('Annotations', annotations)
        self.add('schemaVersion', schemaVersion)

    def _validate(self):
        """custom validation function to ensure that Config and Layers mediaTypes
           are valid. By the time we get here, we know there is a Config object,
           and there can be one or more layers.
        """
        return self._validateLayerMediaTypes() and self._validateConfigMediaType() or False
        return True

    def _validateConfigMediaType(self):
        """validate the config media type.
        """
        manifestConfig = self.attrs.get('Config').value
        if not manifestConfig:
            return False
        else:
            mediaType = manifestConfig.attrs.get('MediaType').value
            return mediaType or False
        if mediaType != MediaTypeImageConfig:
            bot.error('config mediaType %s is invalid, should be %s' % (mediaType, MediaTypeImageConfig))
            return False
        return True

    def _validateLayerMediaTypes(self):
        """validate the Layer Media Types
        """
        layerMediaTypes = [
         MediaTypeImageLayer,
         MediaTypeImageLayerGzip,
         MediaTypeImageLayerZstd,
         MediaTypeImageLayerNonDistributable,
         MediaTypeImageLayerNonDistributableGzip,
         MediaTypeImageLayerNonDistributableZstd]
        layers = self.attrs.get('Layers').value
        if not layers:
            return False
        for layer in layers:
            mediaType = layer.attrs.get('MediaType').value
            if mediaType not in layerMediaTypes:
                bot.error('layer mediaType %s is invalid' % mediaType)
                return False

        return True