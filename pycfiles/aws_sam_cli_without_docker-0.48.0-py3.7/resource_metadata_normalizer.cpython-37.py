# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/samlib/resource_metadata_normalizer.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 2033 bytes
"""
Class that Normalizes a Template based on Resource Metadata
"""
import logging
RESOURCES_KEY = 'Resources'
PROPERTIES_KEY = 'Properties'
METADATA_KEY = 'Metadata'
ASSET_PATH_METADATA_KEY = 'aws:asset:path'
ASSET_PROPERTY_METADATA_KEY = 'aws:asset:property'
LOG = logging.getLogger(__name__)

class ResourceMetadataNormalizer:

    @staticmethod
    def normalize(template_dict):
        """
        Normalize all Resources in the template with the Metadata Key on the resource.

        This method will mutate the template

        Parameters
        ----------
        template_dict dict
            Dictionary representing the template

        """
        resources = template_dict.get(RESOURCES_KEY, {})
        for logical_id, resource in resources.items():
            resource_metadata = resource.get(METADATA_KEY, {})
            asset_path = resource_metadata.get(ASSET_PATH_METADATA_KEY)
            asset_property = resource_metadata.get(ASSET_PROPERTY_METADATA_KEY)
            ResourceMetadataNormalizer._replace_property(asset_property, asset_path, resource, logical_id)

    @staticmethod
    def _replace_property(property_key, property_value, resource, logical_id):
        """
        Replace a property with an asset on a given resource

        This method will mutate the template

        Parameters
        ----------
        property str
            The property to replace on the resource
        property_value str
            The new value of the property
        resource dict
            Dictionary representing the Resource to change
        logical_id str
            LogicalId of the Resource

        """
        if property_key and property_value:
            resource.get(PROPERTIES_KEY, {})[property_key] = property_value
        else:
            if property_key or property_value:
                LOG.info('WARNING: Ignoring Metadata for Resource %s. Metadata contains only aws:asset:path or aws:assert:property but not both', logical_id)