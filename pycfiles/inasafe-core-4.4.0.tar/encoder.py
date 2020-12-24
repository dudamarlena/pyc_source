# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ismailsunni/.qgis2/python/plugins/inasafe/safe/metadata/encoder.py
# Compiled at: 2018-03-19 11:25:21
"""Tools for metadata encoding."""
import json
from datetime import datetime, date
from PyQt4.QtCore import QDate, Qt, QDateTime, QUrl
__copyright__ = 'Copyright 2016, The InaSAFE Project'
__license__ = 'GPL version 3'
__email__ = 'info@inasafe.org'
__revision__ = '$Format:%H$'

class MetadataEncoder(json.JSONEncoder):
    """Metadata Encoder."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.date().isoformat()
        if isinstance(obj, QDate):
            return obj.toString(Qt.ISODate)
        if isinstance(obj, QDateTime):
            return obj.toString(Qt.ISODate)
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, QUrl):
            return obj.toString()
        return json.JSONEncoder.default(self, obj)