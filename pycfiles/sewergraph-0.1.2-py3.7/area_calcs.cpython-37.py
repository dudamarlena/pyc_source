# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sewergraph\area_calcs.py
# Compiled at: 2019-07-31 17:17:24
# Size of source mod 2**32: 15372 bytes
import pandas as pd, numpy as np, os, networkx as nx
from functools import reduce
import sewergraph as sg, sewergraph.save_load

def map_area_to_sewers(G, areas, idcol='facilityid'):
    a = areas.set_index(idcol)
    sewers = sewergraph.save_load.gdf_from_graph(G)
    sewerids = sewers[[idcol, 'source', 'target']]
    s1 = sewerids.set_index(idcol).join(a)
    local_areas = {(row.source, row.target):row.local_area for id, row in s1.iterrows()}
    nx.set_edge_attributes(G, local_areas, 'local_area')


def drainage_areas_from_sewers(sewersdf, SEWER_ID_COL, study_area=None, min_length=35):
    """
    create a GeoDataFrame of polygons representing sewersheds. Shed boundaries are
    created based on Voronoi polygons about each sewer segment.

    study_area: Shapely polygon
    """
    try:
        import geopandas as gp
        from scipy.spatial import Voronoi
        import shapely
    except:
        ImportError('scipy.spatial, GeoPandas, and shapely are required for drainage_areas_from_sewers')

    in_crs = sewersdf.crs
    working_crs = {'init': 'epsg:2272'}
    sewersdf1 = sewersdf.to_crs(working_crs)
    sewersdf1 = sewersdf1.loc[(sewersdf1.length > min_length)]
    sewer_shapes = shapely.geometry.MultiLineString([g for g in sewersdf1.geometry])
    pts = [(sewer.interpolate(pt).x, sewer.interpolate(pt).y) for sewer in sewer_shapes for pt in np.arange(0, sewer.length, 10.0)]
    if study_area is None:
        study_area = sewersdf1.unary_union.convex_hull
    study_area_buff = study_area.buffer(distance=5000)
    border_pts = [xy for xy in study_area_buff.boundary.coords]
    vor = Voronoi(pts + border_pts)
    drainage_bounds = [shapely.geometry.LineString(vor.vertices[line]) for line in vor.ridge_vertices if -1 not in line]
    da_list = [da.intersection(study_area) for da in shapely.ops.polygonize(drainage_bounds)]
    shed_pieces = shapely.geometry.MultiPolygon(da_list)
    shed_geoms = [g for g in shed_pieces.geoms]
    shed_areas_sf = [shed.area for shed in shed_geoms]
    sheds = gp.GeoDataFrame(geometry=shed_geoms, data={'local_area': shed_areas_sf},
      crs=(sewersdf1.crs))
    print('sewersdf1.crs: {}, sheds.crs: {}'.format(sewersdf1.crs, sheds.crs))
    sheds['SUBSHED_ID'] = sheds.index
    sewer_sheds = gp.sjoin(sheds, sewersdf1, how='inner')
    sewer_sheds = sewer_sheds.drop_duplicates(subset='SUBSHED_ID')
    sewer_sheds = sewer_sheds.dissolve(by=SEWER_ID_COL, aggfunc='sum', as_index=False)
    sewer_sheds = sewer_sheds[[SEWER_ID_COL, 'local_area', 'geometry']]
    sewer_sheds = sewer_sheds.to_crs(in_crs)
    return sewer_sheds


def drainage_areas_chunked(sewersdf, SEWER_ID_COL, study_area_chunks, min_length=35):
    try:
        from scipy.spatial import Voronoi
        import geopandas as gp, shapely
    except:
        ImportError('scipy.spatial, GeoPandas, and shapely is required for drainage_areas_from_sewers')

    all_sheds = gp.GeoDataFrame()
    study_boundary = study_area_chunks.unary_union
    for study_area in study_area_chunks.geometry:
        print('study_area processing')
        sewersdf1 = sewersdf.loc[(sewersdf.length > min_length)]
        sewersdf1 = sewersdf1[sewersdf1.intersects(study_area.buffer(distance=400))]
        sewersdf2 = sewersdf1[sewersdf1.intersects(study_area)]
        sewer_shapes = shapely.geometry.MultiLineString([g for g in sewersdf1.geometry])
        pts = [(sewer.interpolate(pt).x, sewer.interpolate(pt).y) for sewer in sewer_shapes for pt in np.arange(0, sewer.length, 10.0)]
        if study_area is None:
            study_area = sewer_shapes.convex_hull
        study_area_buff = study_area.buffer(distance=5000)
        border_pts = [xy for xy in study_area_buff.boundary.coords]
        vor = Voronoi(pts + border_pts)
        drainage_bounds = [shapely.geometry.LineString(vor.vertices[line]) for line in vor.ridge_vertices if -1 not in line]
        da_list = [da for da in shapely.ops.polygonize(drainage_bounds)]
        if da_list:
            shed_pieces = shapely.geometry.MultiPolygon(da_list)
            shed_geoms = [g for g in shed_pieces.geoms]
            sheds = gp.GeoDataFrame(geometry=shed_geoms)
            sheds.crs = sewersdf1.crs
            sheds['SUBSHED_ID'] = sheds.index
            sewer_sheds = gp.sjoin(sheds, sewersdf1, how='inner')
            sewer_sheds = sewer_sheds.drop_duplicates(subset='SUBSHED_ID')
            sewer_sheds = sewer_sheds.dissolve(by=SEWER_ID_COL, aggfunc='sum', as_index=False)
            sewer_sheds = sewer_sheds[[SEWER_ID_COL, 'geometry']]
            sewer_sheds = sewer_sheds[sewer_sheds.FACILITYID.isin(sewersdf2.FACILITYID)]
            all_sheds = all_sheds.append(sewer_sheds)

    all_sheds = all_sheds.dissolve(by=SEWER_ID_COL, aggfunc='sum', as_index=False)
    local_areas = all_sheds.apply((lambda r: r.geometry.area), axis=1)
    all_sheds = all_sheds.assign(local_area=local_areas)
    all_sheds.crs = sewersdf.crs
    return all_sheds


def apportion_overlays(zones, overlay, overlay_field='FCODE'):
    df = zones[:]
    for cat in overlay[overlay_field].unique():
        frac = calculate_overlay_fraction(zones, overlay, overlay_field=overlay_field, overlay_category=cat)
        kwargs = {str(cat): frac}
        df = (df.assign)(**kwargs)

    return df


def overlay_proportion(row, df, overlay_field, overlay_category):
    """
        calculate the fraction of area covered by an overlay. input df is a
        GeoDataFrame resulting from an intersection of two mutlipolygon data sets.
        """
    ov_frac = 0
    study_area_df = df.loc[(df['idx1'] == row.name)]
    study_area = study_area_df.geometry.area.sum()
    if study_area > 0:
        overlay_df = study_area_df.loc[(study_area_df[overlay_field] == overlay_category)]
        overlay_area = overlay_df.geometry.area.sum()
        ov_frac = overlay_area / study_area
    return ov_frac


def calculate_overlay_fraction(zones, overlay, overlay_field='FCODE', overlay_category='Impervious'):
    """
    calculate the fraction of each overlay category present in each polyon in the zone
    GeoDataFrame. E.g. calculate imperviousness of sewersheds by passing in drainage areas
    and an impervious coverage layer.
    """
    overlay = overlay[[overlay_field, 'geometry']]
    ovdf = spatial_overlays(zones, overlay, how='intersection')
    ov_frac = zones.apply((lambda row: overlay_proportion(row, ovdf, overlay_field, overlay_category)),
      axis=1)
    return ov_frac


def array2raster(newRasterfn, rasterOrigin, pixelWidth, pixelHeight, crs, array):
    """
    create a raster file from a numpy array
    """
    try:
        import gdal
    except:
        raise ImportError('Failed to import gdal. This is required for in the array2raster function')

    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRaster.SetProjection(crs.ExportToWkt())
    outband.FlushCache()


def slope_stats_in_sheds(sheds_pth, dem_pth, cell_size=3.2809045, stats='mean median std count min max'):
    """
    Given a shapefile and a DEM raster, calculate the slope statistics in each zone.
    Return: array of dicts with stats for each zone
    """
    try:
        import osr
        from rasterstats import zonal_stats
    except:
        raise ImportError('Failed to import osr and/or rasterstats, required for the slope_stats_in_sheds function.')

    raster = gdal.Open(dem_pth)
    upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size = raster.GetGeoTransform()
    band = raster.GetRasterBand(1)
    raster_srs = osr.SpatialReference()
    raster_srs.ImportFromWkt(raster.GetProjectionRef())
    dem_arr = band.ReadAsArray().astype(np.float)
    g = np.gradient(dem_arr, cell_size)
    xg = g[0]
    yg = g[1]
    slopes = np.sqrt(xg ** 2 + yg ** 2)
    wd = os.path.dirname(dem_pth)
    dem_rast_fname = os.path.splitext(os.path.basename(dem_pth))[0]
    slope_rast_path = os.path.join(wd, dem_rast_fname + '_slope.tif')
    array2raster(slope_rast_path, (upper_left_x, upper_left_y), x_size, y_size, raster_srs, slopes)
    slope_stats = zonal_stats(sheds_pth, slope_rast_path, stats=stats)
    return slope_stats


def max_depth_from_raster(row, dem_pth, dem_adjustment=-4.63):
    """
    return Max Depth for a df row passed with X & Y columns,
    for use in a SWMM5 Junctions table
    """
    try:
        from rasterstats import point_query
    except:
        raise ImportError('rasterstats not found. Try pip install rasterstats')

    if pd.isnull(row.X) or pd.isnull(row.Y):
        return
    point = 'POINT({} {})'.format(row.X, row.Y)
    rim_elev = point_query(point, dem_pth)[0] + dem_adjustment
    invert = row.InvertElev
    max_depth = rim_elev - invert
    return max_depth


def spatial_overlays(df1, df2, how='intersection'):
    """Compute overlay intersection of two
        GeoPandasDataFrames df1 and df2
    """
    try:
        import geopandas as gp
    except:
        raise ImportError('Failed to import GeoPandas. This is required for in the spatial_overlays function')

    df1 = df1.copy()
    df2 = df2.copy()
    df1['geometry'] = df1.geometry.buffer(0)
    df2['geometry'] = df2.geometry.buffer(0)
    if how == 'intersection':
        spatial_index = df2.sindex
        df1['bbox'] = df1.geometry.apply(lambda x: x.bounds)
        df1['histreg'] = df1.bbox.apply(lambda x: list(spatial_index.intersection(x)))
        pairs = df1['histreg'].to_dict()
        nei = []
        for i, j in list(pairs.items()):
            for k in j:
                nei.append([i, k])

        pairs = gp.GeoDataFrame(nei, columns=['idx1', 'idx2'], crs=(df1.crs))
        pairs = pairs.merge(df1, left_on='idx1', right_index=True)
        pairs = pairs.merge(df2, left_on='idx2', right_index=True, suffixes=['_1', '_2'])
        pairs['Intersection'] = pairs.apply((lambda x: x['geometry_1'].intersection(x['geometry_2']).buffer(0)), axis=1)
        pairs = gp.GeoDataFrame(pairs, columns=(pairs.columns), crs=(df1.crs))
        cols = pairs.columns.tolist()
        cols.remove('geometry_1')
        cols.remove('geometry_2')
        cols.remove('histreg')
        cols.remove('bbox')
        cols.remove('Intersection')
        dfinter = pairs[(cols + ['Intersection'])].copy()
        dfinter.rename(columns={'Intersection': 'geometry'}, inplace=True)
        dfinter = gp.GeoDataFrame(dfinter, columns=(dfinter.columns), crs=(pairs.crs))
        dfinter = dfinter.loc[(dfinter.geometry.is_empty == False)]
        return dfinter
    if how == 'difference':
        spatial_index = df2.sindex
        df1['bbox'] = df1.geometry.apply(lambda x: x.bounds)
        df1['histreg'] = df1.bbox.apply(lambda x: list(spatial_index.intersection(x)))
        df1['new_g'] = df1.apply((lambda x: reduce(lambda x, y: x.difference(y).buffer(0), [x.geometry] + list(df2.iloc[x.histreg].geometry))), axis=1)
        df1.geometry = df1.new_g
        df1 = df1.loc[(df1.geometry.is_empty == False)].copy()
        df1.drop(['bbox', 'histreg', new_g], axis=1, inplace=True)
        return df1