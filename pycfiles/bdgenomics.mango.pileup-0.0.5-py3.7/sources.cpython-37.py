# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/pileup/sources.py
# Compiled at: 2019-09-04 14:12:25
# Size of source mod 2**32: 7036 bytes
"""
=======
Sources
=======
.. currentmodule:: bdgenomics.mango.pileup.sources

Sources specify where the genomic data comes from. Sources can come from a url, a GA4GHDatasource, or a JSON string of GA4GH formatted data.

.. autosummary::
    :toctree: _generate/

    BamDataSource
    VcfDataSource
    TwoBitDataSource
    BigBedDataSource
    GA4GHAlignmentJson
    GA4GHVariantJson
    GA4GHFeatureJson
    GA4GHAlignmentSource
    GA4GHVariantSource
    GA4GHFeatureSource
"""
from bdgenomics.mango.io import *

class Source:
    dict_ = {}
    name = None


class GA4GHSource(Source):

    def __init__(self, endpoint, readGroupId, callSetIds=None):
        """ Initializes GA4GHSource.

        Args:
            :param str: url endpoint
            :param str: read group id
            :param str: optional call set ID for variants
        
        """
        self.dict_ = {'endpoint':endpoint, 
         'readGroupId':readGroupId}


class jsonString(Source):

    def __init__(self, json):
        """ Initializes GA4GH JSON.

        Args:
            :param str: json in GA4GH format
        
        """
        self.dict_ = json


class DataFrameSource(Source):

    def __init__(self, dataframe):
        """Initializes dataframe. Converts it to raw json. 

        Args:
            :param dataframe: dataframe
        """
        feature_transformed_json = dataframe._mango_to_json
        self.dict_ = feature_transformed_json
        self.name = dataframe._pileup_visualization


class FileSource(Source):

    def __init__(self, url, indexUrl=None):
        """ Initializes file sources.

        Args:
            :param str: url to file
            :param str: indexUrl to index file
        
        """
        self.dict_ = {'url':url, 
         'indexUrl':indexUrl}


class BamDataSource(FileSource):
    __doc__ = ' Initializes file source from bam file endpoint.\n\n    Args:\n        :param str: url to file\n        :param str: indexUrl to index file\n    \n    '
    name = 'bam'


class VcfDataSource(FileSource):
    __doc__ = ' Initializes file source from vcf file endpoint.\n\n    Args:\n        :param str: url to file\n        :param str: indexUrl to index file\n    \n    '
    name = 'vcf'


class TwoBitDataSource(FileSource):
    __doc__ = ' Initializes file source from twoBit file endpoint.\n\n    Args:\n        :param str: url to file\n    \n    '
    name = 'twoBit'


class BigBedDataSource(FileSource):
    __doc__ = ' Initializes file source from big bed (.bb) file endpoint.\n\n    Args:\n        :param str: url to file\n    \n    '
    name = 'bigBed'


class GA4GHAlignmentJson(jsonString):
    __doc__ = ' Initializes GA4GH Alignment JSON.\n\n    Args:\n        :param str: json in GA4GH format\n    \n    '
    name = 'alignmentJson'


class GA4GHVariantJson(jsonString):
    __doc__ = ' Initializes GA4GH variant JSON.\n\n    Args:\n        :param str: json in GA4GH format\n    \n    '
    name = 'variantJson'


class GA4GHFeatureJson(jsonString):
    __doc__ = ' Initializes GA4GH feature JSON.\n\n    Args:\n        :param str: json in GA4GH format\n    \n    '
    name = 'featureJson'


class GA4GHAlignmentSource(GA4GHSource):
    __doc__ = ' Initializes GA4GHAlignmentSource.\n\n    Args:\n        :param str: url endpoint\n        :param str: read group id    \n    '
    name = 'GAReadAlignment'


class GA4GHVariantSource(GA4GHSource):
    __doc__ = ' Initializes GA4GHSource.\n\n    Args:\n        :param str: url endpoint\n        :param str: call set ID\n        :param str: optional call set ID for variants\n    \n    '
    name = 'GAVariant'


class GA4GHFeatureSource(GA4GHSource):
    __doc__ = ' Initializes GA4GHFeatureSource.\n\n    Args:\n        :param str: url endpoint\n    '
    name = 'GAFeature'


vizNames = {'coverage':[
  BamDataSource.name, GA4GHFeatureJson.name], 
 'pileup':[
  BamDataSource.name, GA4GHAlignmentJson.name, GA4GHAlignmentSource.name], 
 'features':[
  BigBedDataSource.name, GA4GHFeatureJson.name, GA4GHFeatureSource.name], 
 'variants':[
  VcfDataSource.name, GA4GHVariantJson.name, GA4GHVariantSource.name], 
 'genome':[
  TwoBitDataSource.name], 
 'genes':[
  BigBedDataSource.name], 
 'scale':[],  'location':[],  'genotypes':[
  VcfDataSource.name, GA4GHVariantJson.name, GA4GHVariantSource.name]}
sourceNames = {BamDataSource.name: BamDataSource, 
 VcfDataSource.name: VcfDataSource, 
 TwoBitDataSource.name: TwoBitDataSource, 
 BigBedDataSource.name: BigBedDataSource, 
 GA4GHAlignmentJson.name: GA4GHAlignmentJson, 
 GA4GHFeatureJson.name: GA4GHFeatureJson, 
 GA4GHVariantJson.name: GA4GHVariantJson, 
 GA4GHAlignmentSource.name: GA4GHAlignmentSource, 
 GA4GHVariantSource.name: GA4GHVariantSource, 
 GA4GHFeatureSource.name: GA4GHFeatureSource, 
 DataFrameSource.name: DataFrameSource}