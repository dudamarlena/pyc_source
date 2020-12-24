# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/handlers/geonode/backward_compatibility.py
# Compiled at: 2016-12-22 15:59:44
import datetime, logging
from geonode.layers.models import Attribute
logger = logging.getLogger(__name__)
try:
    from geonode.utils import set_attributes
except ImportError:
    set_attributes = None

def set_attributes_bw_compat(layer, attribute_map, overwrite=False, attribute_stats=None):
    """ *layer*: a geonode.layers.models.Layer instance
        *attribute_map*: a list of 2-lists specifying attribute names and types,
            example: [ ['id', 'Integer'], ... ]
        *overwrite*: replace existing attributes with new values if name/type matches.
        *attribute_stats*: dictionary of return values from get_attribute_statistics(),
            of the form to get values by referencing attribute_stats[<layer_name>][<field_name>].
    """
    attribute_map_dict = {'field': 0, 
       'ftype': 1, 
       'description': 2, 
       'label': 3, 
       'display_order': 4}
    for attribute in attribute_map:
        attribute.extend((None, None, 0))

    attributes = layer.attribute_set.all()
    for la in attributes:
        lafound = False
        for attribute in attribute_map:
            field, ftype, description, label, display_order = attribute
            if field == la.attribute:
                lafound = True
                attribute[attribute_map_dict['description']] = la.description
                attribute[attribute_map_dict['label']] = la.attribute_label
                attribute[attribute_map_dict['display_order']] = la.display_order

        if overwrite or not lafound:
            logger.debug('Going to delete [%s] for [%s]', la.attribute, layer.name.encode('utf-8'))
            la.delete()

    if attribute_map is not None:
        iter = len(Attribute.objects.filter(layer=layer)) + 1
        for attribute in attribute_map:
            field, ftype, description, label, display_order = attribute
            if field is not None:
                la, created = Attribute.objects.get_or_create(layer=layer, attribute=field, attribute_type=ftype, description=description, attribute_label=label, display_order=display_order)
                if created:
                    if not attribute_stats or layer.name not in attribute_stats or field not in attribute_stats[layer.name]:
                        result = None
                    else:
                        result = attribute_stats[layer.name][field]
                    if result is not None:
                        logger.debug('Generating layer attribute statistics')
                        la.count = result['Count']
                        la.min = result['Min']
                        la.max = result['Max']
                        la.average = result['Average']
                        la.median = result['Median']
                        la.stddev = result['StandardDeviation']
                        la.sum = result['Sum']
                        la.unique_values = result['unique_values']
                        la.last_stats_updated = datetime.datetime.now()
                    la.visible = ftype.find('gml:') != 0
                    la.display_order = iter
                    la.save()
                    iter += 1
                    logger.debug('Created [%s] attribute for [%s]', field, layer.name.encode('utf-8'))

    else:
        logger.debug('No attributes found')
    return


if set_attributes is None:
    set_attributes = set_attributes_bw_compat