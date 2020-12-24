# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/io/raster.py
# Compiled at: 2020-03-24 01:27:34
# Size of source mod 2**32: 31032 bytes
"""Wrapper functions around rasterio and useful raster functions."""
from affine import Affine
from collections import namedtuple
import itertools, logging, numpy as np, numpy.ma as ma
from retry import retry
import rasterio
from rasterio.enums import Resampling
from rasterio.errors import RasterioIOError
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds as affine_from_bounds
from rasterio.vrt import WarpedVRT
from rasterio.warp import reproject
from rasterio.windows import from_bounds
from tilematrix import clip_geometry_to_srs_bounds, Shape, Bounds
from types import GeneratorType
import warnings
from mapchete.tile import BufferedTile
from mapchete.io import path_is_remote, get_gdal_options, path_exists
from mapchete.validate import validate_write_window_params
logger = logging.getLogger(__name__)
ReferencedRaster = namedtuple('ReferencedRaster', ('data', 'affine', 'bounds', 'crs'))

def read_raster_window(input_files, tile, indexes=None, resampling='nearest', src_nodata=None, dst_nodata=None, gdal_opts=None):
    """
    Return NumPy arrays from an input raster.

    NumPy arrays are reprojected and resampled to tile properties from input
    raster. If tile boundaries cross the antimeridian, data on the other side
    of the antimeridian will be read and concatenated to the numpy array
    accordingly.

    Parameters
    ----------
    input_files : string or list
        path to a raster file or list of paths to multiple raster files readable by
        rasterio.
    tile : Tile
        a Tile object
    indexes : list or int
        a list of band numbers; None will read all.
    resampling : string
        one of "nearest", "average", "bilinear" or "lanczos"
    src_nodata : int or float, optional
        if not set, the nodata value from the source dataset will be used
    dst_nodata : int or float, optional
        if not set, the nodata value from the source dataset will be used
    gdal_opts : dict
        GDAL options passed on to rasterio.Env()

    Returns
    -------
    raster : MaskedArray
    """
    with rasterio.Env(**get_gdal_options(gdal_opts, is_remote=path_is_remote(input_files[0] if isinstance(input_files, list) else input_files, s3=True) if isinstance(input_files, str) else False)) as (env):
        logger.debug('reading %s with GDAL options %s', input_files, env.options)
        return _read_raster_window(input_files, tile, indexes=indexes, resampling=resampling, src_nodata=src_nodata, dst_nodata=dst_nodata)


def _read_raster_window(input_files, tile, indexes=None, resampling='nearest', src_nodata=None, dst_nodata=None):
    if isinstance(input_files, list):
        dst_array = _read_raster_window(input_files[0], tile=tile, indexes=indexes, resampling=resampling, src_nodata=src_nodata, dst_nodata=dst_nodata)
        for f in input_files[1:]:
            f_array = _read_raster_window(f, tile=tile, indexes=indexes, resampling=resampling, src_nodata=src_nodata, dst_nodata=dst_nodata)
            dst_array = ma.MaskedArray(data=np.where(f_array.mask, dst_array, f_array).astype(dst_array.dtype, copy=False), mask=np.where(f_array.mask, dst_array.mask, f_array.mask).astype(np.bool, copy=False))

        return dst_array
    else:
        input_file = input_files
        dst_shape = tile.shape
        if not isinstance(indexes, int):
            if indexes is None:
                dst_shape = (None, ) + dst_shape
        else:
            if len(indexes) == 1:
                indexes = indexes[0]
            else:
                dst_shape = (
                 len(indexes),) + dst_shape
            if tile.tp.is_global and tile.pixelbuffer and tile.is_on_edge():
                return _get_warped_edge_array(tile=tile, input_file=input_file, indexes=indexes, dst_shape=dst_shape, resampling=resampling, src_nodata=src_nodata, dst_nodata=dst_nodata)
        return _get_warped_array(input_file=input_file, indexes=indexes, dst_bounds=tile.bounds, dst_shape=dst_shape, dst_crs=tile.crs, resampling=resampling, src_nodata=src_nodata, dst_nodata=dst_nodata)


def _get_warped_edge_array(tile=None, input_file=None, indexes=None, dst_shape=None, resampling=None, src_nodata=None, dst_nodata=None):
    tile_boxes = clip_geometry_to_srs_bounds(tile.bbox, tile.tile_pyramid, multipart=True)
    parts_metadata = dict(left=None, middle=None, right=None, none=None)
    for polygon in tile_boxes:
        part_metadata = {}
        left, bottom, right, top = polygon.bounds
        touches_right = left == tile.tile_pyramid.left
        touches_left = right == tile.tile_pyramid.right
        touches_both = touches_left and touches_right
        height = int(round((top - bottom) / tile.pixel_y_size))
        width = int(round((right - left) / tile.pixel_x_size))
        if indexes is None:
            dst_shape = (
             None, height, width)
        else:
            if isinstance(indexes, int):
                dst_shape = (
                 height, width)
            else:
                dst_shape = (
                 dst_shape[0], height, width)
        part_metadata.update(bounds=polygon.bounds, shape=dst_shape)
        if touches_both:
            parts_metadata.update(middle=part_metadata)
        else:
            if touches_left:
                parts_metadata.update(left=part_metadata)
            else:
                if touches_right:
                    parts_metadata.update(right=part_metadata)
                else:
                    parts_metadata.update(none=part_metadata)

    return ma.concatenate([_get_warped_array(input_file=input_file, indexes=indexes, dst_bounds=parts_metadata[part]['bounds'], dst_shape=parts_metadata[part]['shape'], dst_crs=tile.crs, resampling=resampling, src_nodata=src_nodata, dst_nodata=dst_nodata) for part in ['none', 'left', 'middle', 'right'] if parts_metadata[part]], axis=-1)


def _get_warped_array(input_file=None, indexes=None, dst_bounds=None, dst_shape=None, dst_crs=None, resampling=None, src_nodata=None, dst_nodata=None):
    """Extract a numpy array from a raster file."""
    try:
        return _rasterio_read(input_file=input_file, indexes=indexes, dst_bounds=dst_bounds, dst_shape=dst_shape, dst_crs=dst_crs, resampling=resampling, src_nodata=src_nodata, dst_nodata=dst_nodata)
    except Exception as e:
        logger.exception('error while reading file %s: %s', input_file, e)
        raise


@retry(tries=3, logger=logger, exceptions=RasterioIOError, delay=1)
def _rasterio_read(input_file=None, indexes=None, dst_bounds=None, dst_shape=None, dst_crs=None, resampling=None, src_nodata=None, dst_nodata=None):

    def _read(src, indexes, dst_bounds, dst_shape, dst_crs, resampling, src_nodata, dst_nodata):
        height, width = dst_shape[-2:]
        if indexes is None:
            dst_shape = (
             len(src.indexes), height, width)
            indexes = list(src.indexes)
        src_nodata = src.nodata if src_nodata is None else src_nodata
        dst_nodata = src.nodata if dst_nodata is None else dst_nodata
        dst_left, dst_bottom, dst_right, dst_top = dst_bounds
        with WarpedVRT(src, crs=dst_crs, src_nodata=src_nodata, nodata=dst_nodata, width=width, height=height, transform=affine_from_bounds(dst_left, dst_bottom, dst_right, dst_top, width, height), resampling=Resampling[resampling]) as (vrt):
            return vrt.read(window=vrt.window(*dst_bounds), out_shape=dst_shape, indexes=indexes, masked=True)

    if isinstance(input_file, str):
        logger.debug('got file path %s', input_file)
        try:
            with rasterio.open(input_file, 'r') as (src):
                return _read(src, indexes, dst_bounds, dst_shape, dst_crs, resampling, src_nodata, dst_nodata)
        except RasterioIOError as e:
            try:
                if path_exists(input_file):
                    raise e
            except:
                raise e

            raise FileNotFoundError('%s not found' % input_file)

    else:
        logger.debug('assuming file object %s', input_file)
        return _read(input_file, indexes, dst_bounds, dst_shape, dst_crs, resampling, src_nodata, dst_nodata)


@retry(tries=3, logger=logger, exceptions=RasterioIOError, delay=1)
def read_raster_no_crs(input_file, indexes=None, gdal_opts=None):
    """
    Wrapper function around rasterio.open().read().

    Parameters
    ----------
    input_file : str
        Path to file
    indexes : int or list
        Band index or list of band indexes to be read.
    gdal_opts : dict
        GDAL options passed on to rasterio.Env()

    Returns
    -------
    MaskedArray

    Raises
    ------
    FileNotFoundError if file cannot be found.
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        try:
            with rasterio.Env(**get_gdal_options(gdal_opts, is_remote=path_is_remote(input_file, s3=True))):
                with rasterio.open(input_file, 'r') as (src):
                    return src.read(indexes=indexes, masked=True)
        except RasterioIOError as e:
            try:
                if path_exists(input_file):
                    raise e
            except:
                raise e

            raise FileNotFoundError('%s not found' % input_file)


class RasterWindowMemoryFile:
    __doc__ = 'Context manager around rasterio.io.MemoryFile.'

    def __init__(self, in_tile=None, in_data=None, out_profile=None, out_tile=None, tags=None):
        """Prepare data & profile."""
        out_tile = out_tile or in_tile
        validate_write_window_params(in_tile, out_tile, in_data, out_profile)
        self.data = extract_from_array(in_raster=in_data, in_affine=in_tile.affine, out_tile=out_tile)
        if 'affine' in out_profile:
            out_profile['transform'] = out_profile.pop('affine')
        self.profile = out_profile
        self.tags = tags

    def __enter__(self):
        """Open MemoryFile, write data and return."""
        self.rio_memfile = MemoryFile()
        with self.rio_memfile.open(**self.profile) as (dst):
            dst.write(self.data.astype(self.profile['dtype'], copy=False))
            _write_tags(dst, self.tags)
        return self.rio_memfile

    def __exit__(self, *args):
        """Make sure MemoryFile is closed."""
        self.rio_memfile.close()


def write_raster_window(in_tile=None, in_data=None, out_profile=None, out_tile=None, out_path=None, tags=None, bucket_resource=None):
    """
    Write a window from a numpy array to an output file.

    Parameters
    ----------
    in_tile : ``BufferedTile``
        ``BufferedTile`` with a data attribute holding NumPy data
    in_data : array
    out_profile : dictionary
        metadata dictionary for rasterio
    out_tile : ``Tile``
        provides output boundaries; if None, in_tile is used
    out_path : string
        output path to write to
    tags : optional tags to be added to GeoTIFF file
    bucket_resource : boto3 bucket resource to write to in case of S3 output
    """
    if not isinstance(out_path, str):
        raise TypeError('out_path must be a string')
    logger.debug('write %s', out_path)
    if out_path == 'memoryfile':
        raise DeprecationWarning('Writing to memoryfile with write_raster_window() is deprecated. Please use RasterWindowMemoryFile.')
    out_tile = out_tile or in_tile
    validate_write_window_params(in_tile, out_tile, in_data, out_profile)
    window_data = extract_from_array(in_raster=in_data, in_affine=in_tile.affine, out_tile=out_tile) if in_tile != out_tile else in_data
    if 'affine' in out_profile:
        out_profile['transform'] = out_profile.pop('affine')
    if window_data.all() is not ma.masked:
        try:
            if out_path.startswith('s3://'):
                with RasterWindowMemoryFile(in_tile=out_tile, in_data=window_data, out_profile=out_profile, out_tile=out_tile, tags=tags) as (memfile):
                    logger.debug((out_tile.id, 'upload tile', out_path))
                    bucket_resource.put_object(Key='/'.join(out_path.split('/')[3:]), Body=memfile)
            else:
                with rasterio.open(out_path, 'w', **out_profile) as (dst):
                    logger.debug((out_tile.id, 'write tile', out_path))
                    dst.write(window_data.astype(out_profile['dtype'], copy=False))
                    _write_tags(dst, tags)
        except Exception as e:
            logger.exception('error while writing file %s: %s', out_path, e)
            raise

    else:
        logger.debug((out_tile.id, 'array window empty', out_path))


def _write_tags(dst, tags):
    if tags:
        for k, v in tags.items():
            if isinstance(k, int):
                dst.update_tags(k, **v)
            else:
                dst.update_tags(**{k: v})


def extract_from_array(in_raster=None, in_affine=None, out_tile=None):
    """
    Extract raster data window array.

    Parameters
    ----------
    in_raster : array or ReferencedRaster
    in_affine : ``Affine`` required if in_raster is an array
    out_tile : ``BufferedTile``

    Returns
    -------
    extracted array : array
    """
    if isinstance(in_raster, ReferencedRaster):
        in_affine, in_raster = in_raster.affine, in_raster.data
    minrow, maxrow, mincol, maxcol = bounds_to_ranges(out_bounds=out_tile.bounds, in_affine=in_affine, in_shape=in_raster.shape)
    if minrow >= 0 and mincol >= 0 and maxrow <= in_raster.shape[(-2)] and maxcol <= in_raster.shape[(-1)]:
        return in_raster[..., minrow:maxrow, mincol:maxcol]
    raise ValueError('extraction fails if output shape is not within input')


def resample_from_array(in_raster=None, in_affine=None, out_tile=None, in_crs=None, resampling='nearest', nodataval=None, nodata=0):
    """
    Extract and resample from array to target tile.

    Parameters
    ----------
    in_raster : array
    in_affine : ``Affine``
    out_tile : ``BufferedTile``
    resampling : string
        one of rasterio's resampling methods (default: nearest)
    nodata : integer or float
        raster nodata value (default: 0)

    Returns
    -------
    resampled array : array
    """
    if nodataval is not None:
        warnings.warn("'nodataval' is deprecated, please use 'nodata'")
        nodata = nodata or nodataval
    if isinstance(in_raster, ma.MaskedArray):
        pass
    else:
        if isinstance(in_raster, np.ndarray):
            in_raster = ma.MaskedArray(in_raster, mask=in_raster == nodata)
        else:
            if isinstance(in_raster, ReferencedRaster):
                in_affine = in_raster.affine
                in_crs = in_raster.crs
                in_raster = in_raster.data
            else:
                if isinstance(in_raster, tuple):
                    in_raster = ma.MaskedArray(data=np.stack(in_raster), mask=np.stack([band.mask if isinstance(band, ma.masked_array) else np.where(band == nodata, True, False) for band in in_raster]), fill_value=nodata)
                else:
                    raise TypeError('wrong input data type: %s' % type(in_raster))
                if in_raster.ndim == 2:
                    in_raster = ma.expand_dims(in_raster, axis=0)
                else:
                    if in_raster.ndim == 3:
                        pass
                    else:
                        raise TypeError('input array must have 2 or 3 dimensions')
            if in_raster.fill_value != nodata:
                ma.set_fill_value(in_raster, nodata)
        dst_data = np.empty((
         in_raster.shape[0],) + out_tile.shape, in_raster.dtype)
        reproject(in_raster.filled(), dst_data, src_transform=in_affine, src_crs=in_crs or out_tile.crs, src_nodata=nodata, dst_transform=out_tile.affine, dst_crs=out_tile.crs, dst_nodata=nodata, resampling=Resampling[resampling])
    return ma.MaskedArray(dst_data, mask=dst_data == nodata, fill_value=nodata)


def create_mosaic(tiles, nodata=0):
    """
    Create a mosaic from tiles.

    Tiles must be connected (also possible over Antimeridian), otherwise strange things
    can happen!

    Parameters
    ----------
    tiles : iterable
        an iterable containing tuples of a BufferedTile and an array
    nodata : integer or float
        raster nodata value to initialize the mosaic with (default: 0)

    Returns
    -------
    mosaic : ReferencedRaster
    """
    if isinstance(tiles, GeneratorType):
        tiles = list(tiles)
    elif not isinstance(tiles, list):
        raise TypeError('tiles must be either a list or generator')
    if not all([isinstance(pair, tuple) for pair in tiles]):
        raise TypeError('tiles items must be tuples')
    if not all([all([isinstance(tile, BufferedTile), isinstance(data, np.ndarray)]) for tile, data in tiles]):
        raise TypeError('tuples must be pairs of BufferedTile and array')
    if len(tiles) == 0:
        raise ValueError('tiles list is empty')
    logger.debug('create mosaic from %s tile(s)', len(tiles))
    if len(tiles) == 1:
        tile, data = tiles[0]
        return ReferencedRaster(data=data, affine=tile.affine, bounds=tile.bounds, crs=tile.crs)
    pyramid, resolution, dtype = _get_tiles_properties(tiles)
    shift = _shift_required(tiles)
    logger.debug('shift: %s' % shift)
    m_left, m_bottom, m_right, m_top = (None, None, None, None)
    for tile, data in tiles:
        num_bands = data.shape[0] if data.ndim > 2 else 1
        left, bottom, right, top = tile.bounds
        if shift:
            left += pyramid.x_size / 2
            right += pyramid.x_size / 2
            if right > pyramid.right:
                right -= pyramid.x_size
                left -= pyramid.x_size
            m_left = min([left, m_left]) if m_left is not None else left
            m_bottom = min([bottom, m_bottom]) if m_bottom is not None else bottom
            m_right = max([right, m_right]) if m_right is not None else right
            m_top = max([top, m_top]) if m_top is not None else top

    height = int(round((m_top - m_bottom) / resolution))
    width = int(round((m_right - m_left) / resolution))
    mosaic = ma.MaskedArray(data=np.full((num_bands, height, width), dtype=dtype, fill_value=nodata), mask=np.ones((num_bands, height, width)))
    affine = Affine(resolution, 0, m_left, 0, -resolution, m_top)
    for tile, data in tiles:
        data = prepare_array(data, nodata=nodata, dtype=dtype)
        t_left, t_bottom, t_right, t_top = tile.bounds
        if shift:
            t_left += pyramid.x_size / 2
            t_right += pyramid.x_size / 2
            if t_right > pyramid.right:
                t_right -= pyramid.x_size
                t_left -= pyramid.x_size
            minrow, maxrow, mincol, maxcol = bounds_to_ranges(out_bounds=(
             t_left, t_bottom, t_right, t_top), in_affine=affine, in_shape=(
             height, width))
            existing_data = mosaic[:, minrow:maxrow, mincol:maxcol]
            existing_mask = mosaic.mask[:, minrow:maxrow, mincol:maxcol]
            mosaic[:, minrow:maxrow, mincol:maxcol] = np.where(data.mask, existing_data, data)
            mosaic.mask[:, minrow:maxrow, mincol:maxcol] = np.where(data.mask, existing_mask, data.mask)

    if shift:
        m_left -= pyramid.x_size / 2
        m_right -= pyramid.x_size / 2
    if m_left < pyramid.left or m_right > pyramid.right:
        logger.debug('mosaic crosses Antimeridian')
        left_distance = abs(pyramid.left - m_left)
        right_distance = abs(pyramid.left - m_right)
        if left_distance > right_distance:
            m_left += pyramid.x_size
            m_right += pyramid.x_size
    logger.debug(Bounds(m_left, m_bottom, m_right, m_top))
    return ReferencedRaster(data=mosaic, affine=Affine(resolution, 0, m_left, 0, -resolution, m_top), bounds=Bounds(m_left, m_bottom, m_right, m_top), crs=tile.crs)


def bounds_to_ranges(out_bounds=None, in_affine=None, in_shape=None):
    """
    Return bounds range values from geolocated input.

    Parameters
    ----------
    out_bounds : tuple
        left, bottom, right, top
    in_affine : Affine
        input geolocation
    in_shape : tuple
        input shape

    Returns
    -------
    minrow, maxrow, mincol, maxcol
    """
    return itertools.chain(*from_bounds(*out_bounds, width=in_shape[(-1)]).round_lengths(pixel_precision=0).round_offsets(pixel_precision=0).toranges())


def tiles_to_affine_shape(tiles):
    """
    Return Affine and shape of combined tiles.

    Parameters
    ----------
    tiles : iterable
        an iterable containing BufferedTiles

    Returns
    -------
    Affine, Shape
    """
    if not tiles:
        raise TypeError('no tiles provided')
    pixel_size = tiles[0].pixel_x_size
    left, bottom, right, top = (
     min([t.left for t in tiles]),
     min([t.bottom for t in tiles]),
     max([t.right for t in tiles]),
     max([t.top for t in tiles]))
    return (
     Affine(pixel_size, 0, left, 0, -pixel_size, top),
     Shape(width=int(round((right - left) / pixel_size, 0)), height=int(round((top - bottom) / pixel_size, 0))))


def _get_tiles_properties(tiles):
    for tile, data in tiles:
        if tile.zoom != tiles[0][0].zoom:
            raise ValueError('all tiles must be from same zoom level')
        if tile.crs != tiles[0][0].crs:
            raise ValueError('all tiles must have the same CRS')
        if isinstance(data, np.ndarray) and data[0].dtype != tiles[0][1][0].dtype:
            raise TypeError('all tile data must have the same dtype')

    return (
     tile.tile_pyramid, tile.pixel_x_size, data[0].dtype)


def _shift_required(tiles):
    """Determine if distance over antimeridian is shorter than normal distance."""
    if tiles[0][0].tile_pyramid.is_global:
        tile_cols = sorted(list(set([t[0].col for t in tiles])))
        if tile_cols == list(range(min(tile_cols), max(tile_cols) + 1)):
            return False
        else:

            def gen_groups(items):
                """Group tile columns by sequence."""
                j = items[0]
                group = [j]
                for i in items[1:]:
                    if i == j + 1:
                        group.append(i)
                    else:
                        yield group
                        group = [i]
                    j = i

                yield group

            groups = list(gen_groups(tile_cols))
            if len(groups) == 1:
                return False
            normal_distance = groups[(-1)][(-1)] - groups[0][0]
            antimeridian_distance = groups[0][(-1)] + tiles[0][0].tile_pyramid.matrix_width(tiles[0][0].zoom) - groups[(-1)][0]
            return antimeridian_distance < normal_distance
    else:
        return False


def memory_file(data=None, profile=None):
    """
    Return a rasterio.io.MemoryFile instance from input.

    Parameters
    ----------
    data : array
        array to be written
    profile : dict
        rasterio profile for MemoryFile
    """
    memfile = MemoryFile()
    with memfile.open(**dict(profile, width=data.shape[(-2)], height=data.shape[(-1)])) as (dataset):
        dataset.write(data)
    return memfile


def prepare_array(data, masked=True, nodata=0, dtype='int16'):
    """
    Turn input data into a proper array for further usage.

    Output array is always 3-dimensional with the given data type. If the output
    is masked, the fill_value corresponds to the given nodata value and the
    nodata value will be burned into the data array.

    Parameters
    ----------
    data : array or iterable
        array (masked or normal) or iterable containing arrays
    nodata : integer or float
        nodata value (default: 0) used if input is not a masked array and
        for output array
    masked : bool
        return a NumPy Array or a NumPy MaskedArray (default: True)
    dtype : string
        data type of output array (default: "int16")

    Returns
    -------
    array : array
    """
    if isinstance(data, (list, tuple)):
        return _prepare_iterable(data, masked, nodata, dtype)
    if isinstance(data, np.ndarray) and data.ndim == 2:
        data = ma.expand_dims(data, axis=0)
    if isinstance(data, ma.MaskedArray):
        return _prepare_masked(data, masked, nodata, dtype)
    if isinstance(data, np.ndarray):
        if masked:
            return ma.masked_values(data.astype(dtype, copy=False), nodata, copy=False)
        else:
            return data.astype(dtype, copy=False)
    else:
        raise ValueError('Data must be array, masked array or iterable containing arrays. Current data: %s (%s)' % (
         data, type(data)))


def _prepare_iterable(data, masked, nodata, dtype):
    out_data = ()
    out_mask = ()
    for band in data:
        if isinstance(band, ma.MaskedArray):
            out_data += (band.data,)
            if masked:
                if band.shape == band.mask.shape:
                    out_mask += (band.mask,)
                else:
                    out_mask += (np.where(band.data == nodata, True, False),)
            else:
                if isinstance(band, np.ndarray):
                    out_data += (band,)
                    if masked:
                        out_mask += (np.where(band == nodata, True, False),)
                    else:
                        raise ValueError('input data bands must be NumPy arrays')

    if masked:
        return ma.MaskedArray(data=np.stack(out_data).astype(dtype, copy=False), mask=np.stack(out_mask))
    else:
        return np.stack(out_data).astype(dtype, copy=False)


def _prepare_masked(data, masked, nodata, dtype):
    if data.shape == data.mask.shape:
        if masked:
            return ma.masked_values(data.astype(dtype, copy=False), nodata, copy=False)
        else:
            return ma.filled(data.astype(dtype, copy=False), nodata)
    else:
        if masked:
            return ma.masked_values(data.astype(dtype, copy=False), nodata, copy=False)
        else:
            return ma.filled(data.astype(dtype, copy=False), nodata)