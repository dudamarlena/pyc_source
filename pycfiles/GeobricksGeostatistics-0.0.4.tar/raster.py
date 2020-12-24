# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_geostatistics/geobricks_geostatistics/core/raster.py
# Compiled at: 2015-03-16 09:48:56
import os, json
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import get_raster_path
from geobricks_spatial_query.core.spatial_query_core import SpatialQuery
from geobricks_gis_raster.core.raster import crop_raster_on_vector_bbox_and_postgis_db, get_statistics, get_srid, get_location_values
from multiprocessing import Process, Queue, Pool
log = logger(__file__)

class Stats:
    config = None

    def __init__(self, config):
        self.config = config['settings'] if 'settings' in config else config

    def zonal_stats(self, json_stats):
        """
        :param json_stats: json with statistics definitions
        :return: json with response
        """
        for raster in json_stats['raster']:
            raster['path'] = get_raster_path(raster)
            if not os.path.isabs(raster['path']):
                raster['path'] = os.path.normpath(os.path.join(os.path.dirname(__file__), raster['path']))

        if json_stats['vector']['type'] == 'database':
            return self._zonal_stats_by_vector_database(json_stats['raster'], json_stats['vector']['options'], json_stats['stats']['raster_stats'])
        else:
            if json_stats['vector']['type'] == 'geojson':
                log.warn('TODO: Geojson statistics not implemented yet')
            return

    def get_stats(self, json_stats):
        return get_statistics(get_raster_path(json_stats['raster']))

    def get_histogram(self, json_stats):
        return get_statistics(get_raster_path(json_stats['raster']), json_stats['stats'])

    def _zonal_stats_by_vector_database(self, rasters, vector, raster_statistics):
        sq = SpatialQuery(self.config)
        all_stats = []
        for raster in rasters:
            stats = []
            raster_path = raster['path']
            srid = get_srid(raster_path)
            if raster_path is None:
                log.warn('Raster path is null for', raster)
            else:
                column_filter_code_index = 0
                column_filter_label_index = 1
                db_datasource = vector['db']
                layer_code = vector['layer']
                column_code = vector['column'] if 'column' in vector else None
                codes = vector['codes'] if 'codes' in vector else None
                select = (',').join(vector['groupby'])
                groupyby = select
                query = sq.get_query_string_select_all(db_datasource, layer_code, column_code, codes, select, groupyby)
                subcodes = sq.query_db(vector['db'], query)
                print subcodes
                q = Queue()
                pool = Pool(2)
                processes = []
                subcolumn_code = vector['groupby'][column_filter_code_index]
                if subcodes:
                    for subcode in subcodes:
                        code = str(subcode[column_filter_code_index])
                        label = str(subcode[column_filter_label_index])
                        print code, label
                        processes.append(Process(target=self.do_process, args=(q, raster_path, srid, sq, db_datasource, layer_code, subcolumn_code, code, label, raster_statistics)))

                print 'PROCESSES'
                for p in processes:
                    print p
                    p.start()

                print 'JOIN'
                for p in processes:
                    print p
                    p.join()

                print 'HERE!'
                print len(processes)
                print q.get_nowait()
                for p in processes:
                    try:
                        stats.append(q.get_nowait())
                    except Exception as e:
                        print e

                print 'DAJE'
            all_stats.append(stats)

        print all_stats
        return all_stats

    def _get_zonalstat_db(self, raster_path, srid, sq, db_datasource, layer_code, column_code, codes, raster_statistics):
        bbox = sq.query_bbox(db_datasource, layer_code, column_code, codes, srid)
        db = sq.get_db_instance()
        db_connection_string = db.get_connection_string(True)
        query = sq.get_query_string_select_all(db_datasource, layer_code, column_code, codes, '*')
        log.info(query)
        filepath = crop_raster_on_vector_bbox_and_postgis_db(raster_path, db_connection_string, query, bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1])
        return get_statistics(filepath, raster_statistics)

    def get_location_values(self, input_layers, lat, lon, band=None):
        input_files = []
        for input_layer in input_layers:
            input_files.append(self.get_raster_path(input_layer))

        log.info(input_files)
        return get_location_values(input_files, lat, lon, band)

    def do_process(self, q, raster_path, srid, sq, db_datasource, layer_code, subcolumn_code, code, label, raster_statistics):
        try:
            raster_stats = self._get_zonalstat_db(raster_path, srid, sq, db_datasource, layer_code, subcolumn_code, [code], raster_statistics)
            print '->', code, label
            obj = {'code': code, 'label': label, 'data': raster_stats}
            q.put(obj)
        except Exception as e:
            print e