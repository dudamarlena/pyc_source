# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_gis_vector/geobricks_gis_vector/core/vector.py
# Compiled at: 2015-03-16 09:21:35
import uuid, os, subprocess, fiona, shutil, time
from fiona.crs import to_string
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import create_tmp_filename, get_filename
from geobricks_proj4_to_epsg.core.proj4_to_epsg import get_epsg_code_from_proj4
log = logger(__file__)

def crop_vector_on_vector_bbox_and_postgis(input_path, db_connection_string, query, output_name=None):
    """
    Crop a shapefile by a postgis layer stored in the database
    :param input_path: input shapefile to crop
    :param db_connection_string: connections string to the database
    :param query: query to the postgis vector layer
    :param output_name: optional output_name of the shapefile
    :return: the path to the cropped shapefile
    """
    start = time.time()
    crop_shp_path = create_shp_from_postgis(db_connection_string, query)
    log.info('crop_shp_path: ' + crop_shp_path)
    cropped_by_bbox_path = crop_vector_with_bounding_box(crop_shp_path, input_path)
    log.info('cropped_by_bbox_path: ' + cropped_by_bbox_path)
    clipped_path = crop_by_vector_by_vector(crop_shp_path, cropped_by_bbox_path, output_name)
    log.info('Final output clipped_path: ' + str(clipped_path))
    shutil.rmtree(os.path.dirname(crop_shp_path))
    shutil.rmtree(os.path.dirname(cropped_by_bbox_path))
    end = time.time()
    log.info('Time to process:' + str(end - start))
    return clipped_path


def crop_vector_with_bounding_box(input_file_bbox, file_to_crop, output_path=None):
    with fiona.open(input_file_bbox) as (c):
        with fiona.open(file_to_crop) as (d):
            if output_path is None:
                output_path = create_tmp_filename('shp', 'tmp_shp_bbox', 'tmp_shp_bbox_' + str(uuid.uuid4()), False)
                bounds = c.bounds
                if bounds[0] == 0.0 and bounds[1] == 0.0 and bounds[2] == 0.0 and bounds[3] == 0.0:
                    msg = 'Shapefile ' + input_file_bbox + ' has 0 invalide size'
                    log.error(msg)
                    raise Exception(msg)
                args = [
                 'ogr2ogr',
                 '-f',
                 '"ESRI Shapefile"',
                 output_path,
                 file_to_crop,
                 '-clipsrc',
                 str(bounds[0]),
                 str(bounds[1]),
                 str(bounds[2]),
                 str(bounds[3])]
                try:
                    cmd = (' ').join(args)
                    log.info(cmd)
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    p.wait()
                except Exception as e:
                    log.error(e)
                    raise Exception(e)

    return output_path


def create_shp_from_postgis(db_connection_string, query, output_path=None):
    """
    Create a shp from a post
    :param db_connection_string:
    :param query:
    :return:
    """
    if output_path is None:
        output_path = create_tmp_filename('shp', 'tmp_shp_postgis', 'tmp_shp_postgis_' + str(uuid.uuid4()), False)
    else:
        log.warn('TODO: get the folder by output_path filename. check if the folder is created, otherwise create it.')
    args = ['ogr2ogr',
     '-f',
     '"ESRI Shapefile"',
     output_path,
     db_connection_string,
     '-sql',
     '"' + query + '"']
    try:
        cmd = (' ').join(args)
        log.info(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
    except Exception as e:
        log.error(e)
        raise Exception(e)

    return output_path


def crop_by_vector_by_vector(crop_shp_path, input_path, output_name=None):
    output_path = None
    if output_name is None:
        output_path = create_tmp_filename('shp', 'tmp_shp', 'tmp_shp_' + str(uuid.uuid4()), False)
    else:
        log.warn('TODO: get the folder by output_path filename. check if the folder is created, otherwise create it.')
        output_path = create_tmp_filename('shp', output_name, 'tmp_shp_' + str(uuid.uuid4()), False)
    args = ['ogr2ogr',
     '-skipfailures',
     '-clipsrc',
     crop_shp_path,
     output_path,
     input_path]
    try:
        cmd = (' ').join(args)
        log.info(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
    except Exception as e:
        log.error(e)
        raise Exception(e)

    if _check_if_shapefile_is_valid(output_path):
        return output_path
    else:
        return
        return


def _check_if_shapefile_is_valid(input_path):
    with fiona.open(input_path) as (c):
        bounds = c.bounds
        if bounds[0] == 0.0 and bounds[1] == 0.0 and bounds[2] == 0.0 and bounds[3] == 0.0:
            return False
        return True


def get_authority(file_path):
    """
    Get the authority used by a raster i.e. EPSG:4326
    :param file_path: path to the file
    :return: return the SRID of the raster projection
    """
    with fiona.open(file_path) as (c):
        log.info(c)
        if 'init' in c.crs:
            return c.crs['init']
        if 'proj' in c.crs:
            return 'EPSG:' + str(get_epsg_code_from_proj4(to_string(c.crs)))
    return


def get_srid(file_path):
    """
    Get the SRID of a raster (i.e. 4326 or 3857 and not EPSG:4326)
    :param file_path: path to the file
    :return: return the SRID of the raster projection
    """
    proj = get_authority(file_path)
    log.info(proj)
    if ':' in proj:
        return proj.split(':')[1]
    else:
        if proj.isdigit():
            return proj
        return