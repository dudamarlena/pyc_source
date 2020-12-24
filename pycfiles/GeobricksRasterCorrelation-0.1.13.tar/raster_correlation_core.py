# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/geobricks/geobricks/server/geobricks_raster_correlation/geobricks_raster_correlation/core/raster_correlation_core.py
# Compiled at: 2015-07-15 04:19:57
import numpy as np, time, rasterio
from pysal.esda import mapclassify
from scipy.stats import linregress
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import get_raster_path
from geobricks_raster_correlation.core.colors import get_colors
log = logger(__file__)

def get_correlation_json(obj):
    try:
        raster = obj['raster']
        raster_path1 = get_raster_path(raster[0])
        raster_path2 = get_raster_path(raster[1])
        bins = 300
        intervals = 6
        color_ramp = 'Reds'
        if 'stats' in obj:
            if 'correlation' in obj['stats']:
                o = obj['stats']['correlation']
                if 'bins' in o:
                    bins = o['bins']
                if 'intervals' in o:
                    intervals = o['intervals']
                if 'color_ramp' in o:
                    color_ramp = o['colorRamp']
        return get_correlation(raster_path1, raster_path2, bins, intervals, color_ramp)
    except Exception as e:
        raise Exception(e)


def get_correlation(raster_path1, raster_path2, bins=300, intervals=6, color_ramp='Reds', reverse=False, min1=None, max1=None, min2=None, max2=None, band1=1, band2=1, classification_type='Jenks_Caspall'):
    with rasterio.open(raster_path1) as (ds1):
        with rasterio.open(raster_path2) as (ds2):
            if bins is None:
                bins = 300
            if _check_raster_equal_size(ds1, ds2):
                array1 = np.array(ds1.read()).flatten()
                nodata1 = ds1.meta['nodata'] if 'nodata' in ds1.meta else None
                array2 = np.array(ds2.read()).flatten()
                nodata2 = ds2.meta['nodata'] if 'nodata' in ds2.meta else None
                min1_computed = np.nanmin(array1)
                max1_computed = np.nanmax(array1)
                min2_computed = np.nanmin(array2)
                max2_computed = np.nanmax(array2)
                if min1 is None:
                    min1 = min1_computed
                if max1 is None:
                    max1 = max1_computed
                if min2 is None:
                    min2 = min2_computed
                if max2 is None:
                    max2 = max2_computed
                statistics = compute_frequencies(array1, array2, min1, min2, max1, max2, nodata1, nodata2, bins)
                series = get_series(statistics['scatter'].values(), intervals, color_ramp, reverse, classification_type)
                result = dict()
                result['series'] = series
                result['stats'] = statistics['stats']
                del ds1
                del ds2
                del array1
                del array2
                return result
    return


def _check_raster_equal_size(ds1, ds2):
    if ds1.shape != ds2.shape:
        return False
        raise Exception('The rasters cannot be processed because they have different dimensions')
    return True


def process_correlation(array1, array2, bins=300, add_stats=True, add_series=True):
    d = dict()
    try:
        if add_stats:
            slope, intercept, r_value, p_value, std_err = linregress(array1, array2)
            d['stats'] = {'slope': slope, 
               'intercept': intercept, 
               'r_value': r_value, 
               'p_value': p_value, 
               'std_err': std_err}
        if add_series:
            d['scatter'] = {}
            heatmap, xedges, yedges = np.histogram2d(array1, array2, bins)
            for x in range(0, len(xedges) - 1):
                for y in range(0, len(yedges) - 1):
                    if heatmap[x][y] > 0:
                        d['scatter'][str(xedges[x]) + '_' + str(yedges[y])] = {'data': [
                                  xedges[x], yedges[y]], 
                           'freq': heatmap[x][y]}

        log.info('Correlation computation End')
        return d
    except Exception as e:
        log.error(e)
        raise Exception(e, 400)


def compute_frequencies(array1, array2, min1, min2, max1, max2, nodata1=None, nodata2=None, bins=300):
    index1 = (array1 > min1) & (array1 <= max1) & (array1 != nodata1)
    index2 = (array1 > min2) & (array2 <= max2) & (array2 != nodata2)
    compound_index = index1 & index2
    del index1
    del index2
    array1 = array1[compound_index]
    array2 = array2[compound_index]
    d = process_correlation(array1, array2, bins)
    del array1
    del array2
    return d


def classify_values(values, k=5, classification_type='Jenks_Caspall'):
    start_time = time.time()
    array = np.array(values)
    result = mapclassify.Jenks_Caspall_Forced(array, k)
    log.info('Classification done in %s seconds ---' % str(time.time() - start_time))
    return result.bins


def get_series(values, intervals, color_ramp, reverse=False, classification_type='Jenks_Caspall'):
    classification_values = []
    for v in values:
        classification_values.append(float(v['freq']))

    classes = classify_values(classification_values, intervals, classification_type)
    colors = get_colors(color_ramp, intervals, reverse)
    series = []
    for color in colors:
        series.append({'color': color, 
           'data': []})

    for v in values:
        freq = v['freq']
        for i in range(len(classes)):
            if freq <= classes[i]:
                series[i]['data'].append([float(v['data'][0]), float(v['data'][1])])
                break

    return series