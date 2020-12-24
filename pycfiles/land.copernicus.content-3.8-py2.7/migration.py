# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/browser/migration.py
# Compiled at: 2017-09-19 09:07:49
import logging
logger = logging.getLogger('land.copernicus.content')

class FixImageScales(object):
    """ Fix image scales for the image field
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        logger.info('Starting to convert scales')
        cat = self.context.portal_catalog
        for _type in ['LandItem', 'LandSection']:
            brains = cat(portal_type=_type)
            for brain in brains:
                obj = brain.getObject()
                field = obj.getField('image')
                field.removeScales(obj)
                field.createScales(obj)
                logger.info('Converted scales for %s', obj.absolute_url())

        logger.info('Finished converting scales')