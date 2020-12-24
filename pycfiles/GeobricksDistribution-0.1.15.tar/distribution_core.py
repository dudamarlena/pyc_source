# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_distribution/geobricks_distribution/core/distribution_core.py
# Compiled at: 2015-03-16 08:15:22
import os, json, uuid
from shutil import move
import glob
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import get_raster_path, zip_files, get_filename, get_vector_path, make_archive, create_tmp_filename
from geobricks_common.core.email_utils import send_email
from geobricks_gis_raster.core.raster import get_authority, get_srid as get_srid_raster, crop_raster_on_vector_bbox_and_postgis_db
from geobricks_spatial_query.core.spatial_query_core import SpatialQuery
from geobricks_gis_vector.core.vector import crop_vector_on_vector_bbox_and_postgis, get_srid as get_srid_vector
log = logger(__file__)
zip_filename = 'layers'
email_header = 'Raster layers'
email_body = "<html><head></head><body><div><b>PGeo - Distribution Service</b></div><div style='padding-top:10px;'>The layers you asked to download are available at the following link:</div><div style='padding-top:10px;'><a href='{{LINK}}'>Download Zip File</a></div><div style='padding-top:10px;'><b>Please note that the link will work for the next 24h hours</b></div></body></html>"

class Distribution:
    config = None
    db_default = 'spatial'

    def __init__(self, config):
        self.config = config

    def _get_distribution_folder(self, distribution_folder=None):
        try:
            if distribution_folder is None:
                if not os.path.isabs(self.config['settings']['folders']['distribution']):
                    self.config['settings']['folders']['distribution'] = os.path.abspath(self.config['settings']['folders']['distribution'])
                distribution_folder = self.config['settings']['folders']['distribution']
            if not os.path.isdir(distribution_folder):
                os.makedirs(distribution_folder)
        except Exception as e:
            log.error(e)
            raise Exception(e)

        return distribution_folder

    def export_raster_by_spatial_query(self, user_json, distribution_url=None, distribution_folder=None):
        log.info(user_json)
        log.info(self.config)
        distribution_folder = self._get_distribution_folder(distribution_folder)
        sq = SpatialQuery(self.config)
        vector_filter = user_json['extract_by']
        db_options = vector_filter['options']
        db_datasource = db_options['db']
        layer_code = db_options['layer']
        column_code = db_options['column']
        codes = db_options['codes']
        email_address = None if 'email_address' not in user_json else user_json['email_address']
        rasters = user_json['raster']
        log.info(rasters)
        zip_folder_id = str(uuid.uuid4()).encode('utf-8')
        zip_folder = os.path.join(distribution_folder, zip_folder_id)
        os.mkdir(zip_folder)
        output_folder = os.path.join(zip_folder, 'layers')
        os.mkdir(output_folder)
        output_files = []
        for raster in rasters:
            log.info(raster)
            raster_path = get_raster_path(raster)
            log.info(raster_path)
            if not os.path.isabs(raster_path):
                raster_path = os.path.normpath(os.path.join(os.path.dirname(__file__), raster_path))
                log.info(raster_path)
                raster_path = os.path.abspath(raster_path)
            log.info(raster_path)
            srid = get_srid_raster(raster_path)
            log.info(srid)
            bbox = sq.query_bbox(db_datasource, layer_code, column_code, codes, srid)
            log.info(bbox)
            db = sq.get_db_instance()
            db_connection_string = db.get_connection_string(True)
            query = sq.get_query_string_select_all(db_datasource, layer_code, column_code, codes, '*')
            log.info(query)
            filepath = crop_raster_on_vector_bbox_and_postgis_db(raster_path, db_connection_string, query, bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1])
            path, filename, name = get_filename(filepath, True)
            dst_file = os.path.join(output_folder, filename)
            move(filepath, dst_file)
            output_filename = get_filename(raster_path) + '.tif'
            output_file = os.path.join(output_folder, output_filename)
            os.rename(dst_file, output_file)
            output_files.append(output_file)

        zip_path = zip_files(zip_filename, output_files, zip_folder)
        if distribution_url is None:
            return zip_path
        else:
            url = distribution_url + zip_folder_id
            self._send_email(url, email_address)
            return '{ "url" : "' + url + '"}'
            return

    def export_vector_by_spatial_query(self, user_json, distribution_url=None, distribution_folder=None):
        vector_filter = user_json['extract_by']
        db_options = vector_filter['options']
        db_datasource = db_options['db']
        layer_code = db_options['layer']
        column_code = db_options['column']
        codes = db_options['codes']
        email_address = None if 'email_address' not in user_json else user_json['email_address']
        vectors = user_json['vector']
        distribution_folder = self._get_distribution_folder(distribution_folder)
        sq = SpatialQuery(self.config)
        output_dirs = []
        for vector in vectors:
            vector_path = get_vector_path(vector)
            srid = get_srid_vector(vector_path)
            log.info(srid)
            query = sq.get_query_string_select_all(db_datasource, layer_code, column_code, codes, 'ST_Transform(geom, ' + srid + ')')
            log.info(query)
            db = sq.get_db_instance()
            db_connection_string = db.get_connection_string(True)
            output_name = get_filename(vector_path)
            output_file_path = crop_vector_on_vector_bbox_and_postgis(vector_path, '"' + db_connection_string + '"', query, output_name)
            if output_file_path:
                output_dirs.append(os.path.dirname(output_file_path))

        zip_folder_id = str(uuid.uuid4()).encode('utf-8')
        zip_folder = os.path.join(distribution_folder, zip_folder_id)
        os.mkdir(zip_folder)
        output_folder = os.path.join(zip_folder, 'layers')
        os.mkdir(output_folder)
        for output_dir in output_dirs:
            for file in glob.glob(os.path.join(output_dir, '*')):
                move(file, output_folder)

        tmp_file = create_tmp_filename()
        tmp_zip_path = make_archive(zip_folder, tmp_file)
        zip_path = os.path.join(zip_folder, 'layers.zip')
        os.rename(tmp_zip_path, zip_path)
        log.info(zip_path)
        if distribution_url is None:
            return zip_path
        else:
            url = distribution_url + zip_folder_id
            self._send_email(url, email_address)
            return '{ "url" : "' + url + '"}'
            return

    def _send_email(self, url, email_address=None):
        if email_address:
            log.info('sending email to: %s' % email_address)
            html = email_body.replace('{{LINK}}', url)
            email_user = self.config['settings']['email']['user']
            email_password = self.config['settings']['email']['password']
            send_email(email_user, email_address, email_password, email_header, html)