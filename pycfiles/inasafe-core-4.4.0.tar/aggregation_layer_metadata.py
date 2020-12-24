# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ismailsunni/.qgis2/python/plugins/inasafe/safe/metadata/aggregation_layer_metadata.py
# Compiled at: 2018-03-19 11:25:21
"""Aggregation Layer Metadata."""
from safe.metadata.generic_layer_metadata import GenericLayerMetadata
from safe.metadata.utilities import merge_dictionaries
__copyright__ = 'Copyright 2016, The InaSAFE Project'
__license__ = 'GPL version 3'
__email__ = 'info@inasafe.org'
__revision__ = '$Format:%H$'

class AggregationLayerMetadata(GenericLayerMetadata):
    """
    Metadata class for aggregation layers

    .. versionadded:: 3.2
    """
    _standard_properties = {}
    _standard_properties = merge_dictionaries(GenericLayerMetadata._standard_properties, _standard_properties)