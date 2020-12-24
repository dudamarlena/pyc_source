# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ismailsunni/.qgis2/python/plugins/inasafe/safe/metadata/output_layer_metadata.py
# Compiled at: 2018-03-19 11:25:21
"""Metadata for Output Layer."""
from safe.metadata import GenericLayerMetadata
from safe.metadata.utilities import merge_dictionaries
__copyright__ = 'Copyright 2016, The InaSAFE Project'
__license__ = 'GPL version 3'
__email__ = 'info@inasafe.org'
__revision__ = '$Format:%H$'

class OutputLayerMetadata(GenericLayerMetadata):
    """
    Metadata class for exposure summary layers

    if you need to add a standard XML property that only applies to this
    subclass, do it this way. @property and @propname.setter will be
    generated automatically

    _standard_properties = {
        'TESTprop': (
            'gmd:identificationInfo/'
            'gmd:MD_DataIdentification/'
            'gmd:supplementalInformation/'
            'gco:CharacterString')
    }
    from safe.metadata.utils import merge_dictionaries
    _standard_properties = merge_dictionaries(
        BaseMetadata._standard_properties, _standard_properties)

    .. versionadded:: 3.2
    """
    _standard_properties = {'exposure_keywords': 'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/inasafe/exposure_keywords/gco:Dictionary', 
       'hazard_keywords': 'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/inasafe/hazard_keywords/gco:Dictionary', 
       'aggregation_keywords': 'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/inasafe/aggregation_keywords/gco:Dictionary', 
       'provenance_data': 'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/inasafe/provenance_data/gco:Dictionary'}
    _standard_properties = merge_dictionaries(GenericLayerMetadata._standard_properties, _standard_properties)