# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/tasks.py
# Compiled at: 2016-12-22 15:59:44
import os, shutil
from osgeo_importer.models import UploadFile
from celery.task import task
from osgeo_importer.views import OSGEO_IMPORTER

@task
def import_object(upload_file_id, configuration_options):
    """
    Imports a file into GeoNode.

    :param configuration_options: List of configuration objects for each layer that is being imported.
    """
    upload_file = UploadFile.objects.get(id=upload_file_id)
    gi = OSGEO_IMPORTER(upload_file.file.path, upload_file=upload_file)
    return gi.handle(configuration_options=configuration_options)


@task
def remove_path(path):
    """
    Removes a path using shutil.rmtree.
    """
    if os.path.exists(path):
        shutil.rmtree(path)