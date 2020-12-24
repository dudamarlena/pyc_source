# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/management/commands/hierarchy.py
# Compiled at: 2017-01-12 19:44:32
# Size of source mod 2**32: 1223 bytes
import os, logging
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_str
from ...models import City
from ..utils.base import GeoBaseCommand
from ..utils.common import *
from ..utils.handler import *
logger = logging.getLogger('geoware.cmd.hierarchy')

class Command(GeoBaseCommand):
    cmd_name = 'hierarchy'

    def is_entry_valid(self, item):
        """
        Checks for minimum hierarchy requirements.
        """
        is_valid = True
        try:
            parent = int(item[0])
            child = int(item[1])
        except:
            is_valid = False

        if is_valid and parent and child:
            return is_valid
        logger.warning('Invalid Record: ({item})'.format(item=item))
        return False

    def create_or_update_record(self, item):
        """
        Update parent, child hierarchy for district & city.
        """
        parent_id, child_id = get_int(item, 0), get_int(item, 1)
        parent, child = self._get_city_hierarchy_cache(parent_id, child_id)
        if parent:
            if child:
                child.district_of = parent
                child.save()
                logger.debug('Updated Hierarchy: {item}'.format(item=item))