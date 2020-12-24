# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/publish/publish.py
# Compiled at: 2014-07-31 05:22:01
from pgeo.config import settings
from pgeo.geoserver.geoserver import Geoserver
from pgeo.metadata.metadata import Metadata

class Publish:
    metadata = Metadata(settings.metadata)
    geoserver = Geoserver(settings.geoserver)
    spatial_db = Geoserver(settings.geoserver)

    def __init__(self):
        return

    def publish(self):
        return

    def publish_shapefile(self):
        return

    def publish_coverage(self):
        return

    def delete(self):
        return

    def rollback(self):
        return