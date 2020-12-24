# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_mapclassify/geobricks_mapclassify/core/mapclassify.py
# Compiled at: 2015-04-01 04:09:55
import uuid, os
from geobricks_common.core.log import logger
from geobricks_common.core.utils import dict_merge
from geobricks_mapclassify.core.sld import create_sld_xml
from geobricks_mapclassify.core.colors import get_colors
from geobricks_mapclassify.core.classify import get_ranges
log = logger(__file__)
default_obj = {'intervals': 5, 
   'colorramp': 'Reds', 
   'colortype': None, 
   'colors': None, 
   'reverse': False, 
   'ranges': None, 
   'labels': None, 
   'nodata': {'codes': None, 
              'label': 'No Data Value', 
              'position': 'on top'}, 
   'classificationtype': 'jenks_caspall_forced', 
   'joincolumn': None, 
   'joindata': None, 
   'doublecounting': False, 
   'decimalvalues': 2, 
   'jointype': 'shaded'}

class MapClassify:
    config = None

    def __init__(self, config):
        self.config = config

    def classify(self, data, distribution_url=None, distribution_folder=None):
        data = dict_merge(default_obj, data)
        ranges = get_ranges(data)
        log.info('Ranges: ' + str(ranges))
        data['intervals'] = len(ranges)
        log.info('Intervals: ' + str(data['intervals']))
        colors = get_colors(data, data['intervals'])
        log.info('Colors: ' + str(colors))
        if data['jointype'] == 'shaded':
            return self.classify_sld(data, ranges, colors, distribution_url, distribution_folder)
        if data['jointype'] == 'point':
            sld, legend = create_sld_xml(data, ranges, colors)
            return {'legend': legend}
        raise Exception('Classification "type":"' + data['jointype'] + '" not supported.')

    def classify_sld(self, data, ranges, colors, distribution_url=None, distribution_folder=None):
        distribution_folder = get_distribution_folder(self.config, distribution_folder)
        sld, legend = create_sld_xml(data, ranges, colors)
        path, filename = _create_sld(distribution_folder, sld)
        if distribution_url is None:
            return path
        else:
            url = distribution_url + filename
            return {'url': url, 'legend': legend}


def _create_sld(distribution_folder, sld, extension='.sld'):
    filename = 'sld_' + str(uuid.uuid4()) + extension
    path = os.path.join(distribution_folder, filename)
    with open(path, 'w') as (f):
        f.write(sld)
    return (
     path, filename)


def get_distribution_folder(config, distribution_folder=None):
    try:
        if distribution_folder is None:
            if not os.path.isabs(config['settings']['folders']['distribution_sld']):
                config['settings']['folders']['distribution_sld'] = os.path.abspath(config['settings']['folders']['distribution_sld'])
            distribution_folder = config['settings']['folders']['distribution_sld']
        if not os.path.isdir(distribution_folder):
            os.makedirs(distribution_folder)
    except Exception as e:
        log.error(e)
        raise Exception(e)

    return distribution_folder