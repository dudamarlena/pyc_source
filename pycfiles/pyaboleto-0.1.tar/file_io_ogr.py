# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyabm\file_io_ogr.py
# Compiled at: 2012-11-18 17:36:44
__doc__ = '\nFunctions for writing shapefiles of model results, using OGR to process \nshapefiles.\n'
import sys, os
try:
    from osgeo import ogr
except ImportError:
    import ogr

try:
    from osgeo import gdal
except ImportError:
    import gdal

try:
    from osgeo import osr
except ImportError:
    import osr

def getFieldType(fieldValue):
    """Returns OGR field type appropriate for the given value"""
    if type(fieldValue) == float:
        return ogr.OFTReal
    if type(fieldValue) == int:
        return ogr.OFTInteger
    if type(fieldValue) == str:
        return ogr.OFTString


def write_NBH_shapefile(neighborhoods, output_file):
    """Generates a shapefile from a set of neighborhoods."""
    shpDriver = ogr.GetDriverByName('ESRI Shapefile')
    ds = shpDriver.CreateDataSource(output_file)
    outcs = osr.SpatialReference()
    outcs.SetProjCS('UTM 45N (WGS84)')
    outcs.SetWellKnownGeogCS('WGS84')
    outcs.SetUTM(45, True)
    layer = ds.CreateLayer('pyabm', srs=outcs, geom_type=ogr.wkbPoint)
    NID_field = ogr.FieldDefn('NID', ogr.OFTInteger)
    RID_field = ogr.FieldDefn('RID', ogr.OFTInteger)
    agveg_field = ogr.FieldDefn('agveg', ogr.OFTReal)
    nonagveg_field = ogr.FieldDefn('nonagveg', ogr.OFTReal)
    pubbldg_field = ogr.FieldDefn('pubbldg', ogr.OFTReal)
    privbldg_field = ogr.FieldDefn('privbldg', ogr.OFTReal)
    other_field = ogr.FieldDefn('other', ogr.OFTReal)
    total_area_field = ogr.FieldDefn('total_area', ogr.OFTReal)
    perc_agveg_field = ogr.FieldDefn('perc_agveg', ogr.OFTReal)
    perc_veg_field = ogr.FieldDefn('perc_veg', ogr.OFTReal)
    perc_bldg_field = ogr.FieldDefn('perc_bldg', ogr.OFTReal)
    layer.CreateField(NID_field)
    layer.CreateField(RID_field)
    layer.CreateField(agveg_field)
    layer.CreateField(nonagveg_field)
    layer.CreateField(pubbldg_field)
    layer.CreateField(privbldg_field)
    layer.CreateField(other_field)
    layer.CreateField(total_area_field)
    layer.CreateField(perc_agveg_field)
    layer.CreateField(perc_veg_field)
    layer.CreateField(perc_bldg_field)
    for neighborhood in neighborhoods:
        new_feature = ogr.Feature(feature_def=layer.GetLayerDefn())
        new_feature.SetField('NID', neighborhood.get_ID())
        new_feature.SetField('RID', neighborhood.get_parent_agent().get_ID())
        new_feature.SetField('agveg', neighborhood._land_agveg)
        new_feature.SetField('nonagveg', neighborhood._land_nonagveg)
        new_feature.SetField('pubbldg', neighborhood._land_pubbldg)
        new_feature.SetField('privbldg', neighborhood._land_privbldg)
        new_feature.SetField('other', neighborhood._land_other)
        total_area = neighborhood._land_agveg + neighborhood._land_nonagveg + neighborhood._land_pubbldg + neighborhood._land_privbldg + neighborhood._land_other
        percent_agveg = neighborhood._land_agveg / total_area
        percent_veg = (neighborhood._land_agveg + neighborhood._land_nonagveg) / total_area
        percent_bldg = (neighborhood._land_privbldg + neighborhood._land_pubbldg) / total_area
        new_feature.SetField('total_area', total_area)
        new_feature.SetField('perc_agveg', percent_agveg)
        new_feature.SetField('perc_veg', percent_veg)
        new_feature.SetField('perc_bldg', percent_bldg)
        x, y = neighborhood.get_coords()
        wkt = 'Point(%f %f)' % (x, y)
        geom = ogr.CreateGeometryFromWkt(wkt)
        new_feature.SetGeometry(geom)
        layer.CreateFeature(new_feature)

    ds.Destroy()


def read_single_band_raster(input_file):
    ds = gdal.Open(input_file)
    if ds.RasterCount > 1:
        raise IOError('Single-band raster %s has more than one band' % input_file)
    raster_array = ds.ReadAsArray()
    gt = ds.GetGeoTransform()
    prj = ds.GetProjection()
    ds = None
    return (
     raster_array, gt, prj)


def write_single_band_raster(array, gt, prj, output_file):
    format = 'GTiff'
    driver = gdal.GetDriverByName(format)
    dst_ds = driver.Create(output_file, array.shape[1], array.shape[0])
    dst_ds.SetProjection(prj)
    dst_ds.SetGeoTransform(gt)
    dst_ds.GetRasterBand(1).WriteArray(array)
    dst_ds = None
    return 0