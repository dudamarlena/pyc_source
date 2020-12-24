# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fab_geoalchemy/interface.py
# Compiled at: 2018-06-22 07:44:54
# Size of source mod 2**32: 822 bytes
from flask_appbuilder.models.sqla.interface import SQLAInterface, _is_sqla_type
from geoalchemy2 import Geometry
import logging
log = logging.getLogger(__name__)

class GeoSQLAInterface(SQLAInterface):

    def __init__(self, *args, **kwargs):
        log.debug('Instantiating GeoSQLAInterface')
        super(GeoSQLAInterface, self).__init__(*args, **kwargs)

    def is_point(self, col_name):
        log.debug('Checking if {} is a point'.format(col_name))
        col = self.list_columns[col_name]
        try:
            point = _is_sqla_type(col.type, Geometry) and col.type.geometry_type == 'POINT'
            log.debug('Point? {}'.format(point))
            return point
        except Exception as e:
            log.exception(e)
            log.debug('Not a point')
            return False