# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thyme/model/pom.py
# Compiled at: 2020-04-06 09:21:33
# Size of source mod 2**32: 15696 bytes
"""
Utility classes and methods for working with POM output.

The Princeton Ocean Modeling System (POM) is "a sigma coordinate (terrain-
following), free surface ocean model with embedded turbulence and wave
sub-models, and wet-dry capability." See http://www.ccpo.odu.edu/POMWEB/ for
more information.

This module provides functionality allowing POM output to be interpolated to a
regular, orthogonal lat/lon horizontal grid at a given depth-below-surface.

Currently, this module has only been tested to work with POM-based National
Ocean Service (NOS) Operational Forecast Systems (OFS), e.g. NYOFS, LOOFS, and
LSOFS, and would likely require modifications to support other POM-based model
output.
"""
import datetime, netCDF4, numpy
from osgeo import ogr, osr
from scipy import interpolate
from thyme.model import model
from thyme.util import interp
FILLVALUE = -9999.0

class POMIndexFile(model.ModelIndexFile):
    __doc__ = 'NetCDF file containing metadata/grid info used during POM processing.\n\n    Store a regular grid definition, mask, and other information needed to\n    process/convert native output from an POM-based hydrodynamic model, within\n    a reusable NetCDF file.\n\n    Support is included for defining a set of regular, orthogonal subgrids that\n    allow the data to be subset into multiple sub-domains during processing.\n    This is accomplished by specifying a polygon shapefile containing one or\n    more rectangular, orthogonal polygons defining areas where output data will\n    be cropped and written to distinct output files.\n\n    A unique model index file must be created for each combination of model,\n    output grid resolution, land mask, and subset grid definition, and must be\n    regenerated if anything changes (i.e., when a model domain extent is\n    modified or the target output grid is redefined, a new model index file\n    must be created before processing can resume). Until any of these\n    properties change, the index file may be kept on the data processing system\n    and reused in perpetuity.\n    '

    def __init__(self, path):
        super().__init__(path)

    def compute_grid_mask(self, model_file, reg_grid):
        """Create model domain mask and write to index file.

        Args:
            model_file: `POMOutputFile` instance containing irregular grid
                structure and variables.
            reg_grid: `RegularGrid` instance describing the regular grid for
                which the mask will be created.
        """
        driver = ogr.GetDriverByName('Memory')
        dset = driver.CreateDataSource('grid_cell_mask')
        dset_srs = osr.SpatialReference()
        dset_srs.ImportFromEPSG(4326)
        layer = dset.CreateLayer('', dset_srs, ogr.wkbMultiPolygon)
        layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        for nx1 in range(model_file.num_nx - 1):
            for ny1 in range(model_file.num_ny - 1):
                if nx1 == 0:
                    pass
                else:
                    if ny1 == 0:
                        pass
                    else:
                        if ny1 == model_file.num_ny - 1:
                            pass
                        else:
                            if nx1 == model_file.num_nx - 1:
                                pass
                            else:
                                nx2 = nx1 + 1
                                ny2 = ny1
                                nx3 = nx1 + 1
                                ny3 = ny1 + 1
                                nx4 = nx1
                                ny4 = ny1 + 1
                                nx5 = nx1 - 1
                                ny5 = ny1 + 1
                                nx6 = nx1 - 1
                                ny6 = ny1
                                nx7 = nx1 - 1
                                ny7 = ny1 - 1
                                nx8 = nx1
                                ny8 = ny1 - 1
                                nx9 = nx1 + 1
                                ny9 = ny1 - 1
                                buffer_distance = abs(model_file.var_lon[0][0] - model_file.var_lon[0][1])
                                quad1_valid_points = []
                                for ny, nx in ((ny1, nx1), (ny2, nx2), (ny3, nx3), (ny4, nx4)):
                                    if model_file.var_mask[(ny, nx)] == 1:
                                        quad1_valid_points.append((ny, nx))

                                if model_file.var_mask[(ny1, nx1)] == 1:
                                    quad2_valid_points = []
                                    for ny, nx in ((ny1, nx1), (ny4, nx4), (ny5, nx5), (ny6, nx6)):
                                        if model_file.var_mask[(ny, nx)] == 1:
                                            quad2_valid_points.append((ny, nx))

                                    quad3_valid_points = []
                                    for ny, nx in ((ny1, nx1), (ny6, nx6), (ny7, nx7), (ny8, nx8)):
                                        if model_file.var_mask[(ny, nx)] == 1:
                                            quad3_valid_points.append((ny, nx))

                                    quad4_valid_points = []
                                    for ny, nx in ((ny1, nx1), (ny8, nx8), (ny9, nx9), (ny2, nx2)):
                                        if model_file.var_mask[(ny, nx)] == 1:
                                            quad4_valid_points.append((ny, nx))

                                    if len(quad1_valid_points) < 3:
                                        if len(quad2_valid_points) < 3:
                                            if len(quad3_valid_points) < 3:
                                                if len(quad4_valid_points) < 3:
                                                    point = ogr.Geometry(ogr.wkbPoint)
                                                    point.AddPoint(model_file.var_lon[(ny1, nx1)], model_file.var_lat[(ny1, nx1)])
                                                    pt_wkt = point.ExportToWkt()
                                                    pt = ogr.CreateGeometryFromWkt(pt_wkt)
                                                    buffer = pt.Buffer(buffer_distance)
                                                    buffer_feature = ogr.Feature(layer.GetLayerDefn())
                                                    buffer_feature.SetField('id', 1)
                                                    buffer_feature.SetGeometry(buffer)
                                                    layer.CreateFeature(buffer_feature)
                if len(quad1_valid_points) < 3:
                    pass
                else:
                    ring = ogr.Geometry(ogr.wkbLinearRing)
                    for ny, nx in quad1_valid_points:
                        ring.AddPoint(model_file.var_lon[(ny, nx)], model_file.var_lat[(ny, nx)])

                    ny, nx = quad1_valid_points[0]
                    ring.AddPoint(model_file.var_lon[(ny, nx)], model_file.var_lat[(ny, nx)])
                    geom = ogr.Geometry(ogr.wkbPolygon)
                    geom.AddGeometry(ring)
                    grid_feature = ogr.Feature(layer.GetLayerDefn())
                    grid_buffer = geom.Buffer(buffer_distance)
                    grid_feature.SetGeometry(grid_buffer)
                    grid_feature.SetField('id', 1)
                    layer.CreateFeature(grid_feature)

        return self.rasterize_mask(reg_grid, layer)


class POMFile(model.ModelFile):
    __doc__ = 'Read/process data from a POM model NetCDF file.\n\n    Attributes:\n        path: Path (relative or absolute) of the file.\n    '

    def __init__(self, path, datetime_rounding=None):
        """Initialize POM file object and open file at specified path.

        Args:
            path: Path of target NetCDF file.
            datetime_rounding: The `dateutil.DatetimeRounding` constant
                representing how date/time values should be rounded, or None if
                no rounding should occur.
        """
        super().__init__(path, datetime_rounding=datetime_rounding)
        self.var_lat = None
        self.var_lon = None
        self.var_u = None
        self.var_v = None
        self.var_mask = None
        self.var_zeta = None
        self.var_depth = None
        self.var_sigma = None
        self.var_time = None
        self.time_units = None
        self.num_sigma = None
        self.num_ny = None
        self.num_nx = None
        self.num_times = None
        self.datetime_values = None

    def release_resources(self):
        """Allow GC to reclaim memory by releasing/deleting resources."""
        self.var_lat = None
        self.var_lon = None
        self.var_u = None
        self.var_v = None
        self.var_mask = None
        self.var_zeta = None
        self.var_depth = None
        self.var_sigma = None
        self.var_time = None
        self.time_units = None
        self.num_sigma = None
        self.num_ny = None
        self.num_nx = None
        self.num_times = None
        self.datetime_values = None

    def get_valid_extent(self):
        """Masked model domain extent."""
        water_lat_rho = numpy.ma.masked_array(self.var_lat, numpy.logical_not(self.var_mask))
        water_lon_rho = numpy.ma.masked_array(self.var_lon, numpy.logical_not(self.var_mask))
        lon_min = numpy.nanmin(water_lon_rho)
        lon_max = numpy.nanmax(water_lon_rho)
        lat_min = numpy.nanmin(water_lat_rho)
        lat_max = numpy.nanmax(water_lat_rho)
        return (
         lon_min, lon_max, lat_min, lat_max)

    def init_handles(self):
        """Initialize handles to NetCDF variables."""
        self.var_lat = self.nc_file.variables['lat'][:, :]
        self.var_lon = self.nc_file.variables['lon'][:, :]
        self.var_lat = self.var_lat.astype(numpy.float64)
        self.var_lon = self.var_lon.astype(numpy.float64)
        self.var_u = self.nc_file.variables['u'][:, :, :, :]
        self.var_v = self.nc_file.variables['v'][:, :, :, :]
        self.var_mask = self.nc_file.variables['mask'][:, :]
        self.var_zeta = self.nc_file.variables['zeta'][:, :, :]
        self.var_depth = self.nc_file.variables['depth'][:, :]
        self.var_sigma = self.nc_file.variables['sigma'][:]
        self.var_time = self.nc_file.variables['time'][:]
        self.time_units = self.nc_file.variables['time'].units
        self.num_sigma = self.nc_file.dimensions['sigma'].size
        self.num_ny = self.nc_file.dimensions['ny'].size
        self.num_nx = self.nc_file.dimensions['nx'].size
        self.num_times = self.nc_file.dimensions['time'].size
        self.update_datetime_values(netCDF4.num2date((self.var_time), units=(self.time_units)))
        if self.nc_file.variables['sigma'].positive == 'down':
            self.var_sigma = self.var_sigma * -1

    def get_vertical_coordinate_type(self):
        pass

    def uv_to_regular_grid(self, model_index, time_index, target_depth, interp_method=interp.INTERP_METHOD_SCIPY):
        """Call grid processing functions and interpolate u/v to a regular grid"""
        u_target_depth, v_target_depth = vertical_interpolation(self.var_u, self.var_v, self.var_mask, self.var_zeta, self.var_depth, self.var_sigma, self.num_sigma, self.num_ny, self.num_nx, time_index, target_depth)
        water_lat_rho = numpy.ma.masked_array(self.var_lat, numpy.logical_not(self.var_mask))
        water_lon_rho = numpy.ma.masked_array(self.var_lon, numpy.logical_not(self.var_mask))
        water_u = numpy.ma.masked_array(u_target_depth, numpy.logical_not(self.var_mask))
        water_v = numpy.ma.masked_array(v_target_depth, numpy.logical_not(self.var_mask))
        u_compressed = numpy.ma.compressed(water_u)
        v_compressed = numpy.ma.compressed(water_v)
        lat_compressed = numpy.ma.compressed(water_lat_rho)
        lon_compressed = numpy.ma.compressed(water_lon_rho)
        return interp.interpolate_to_regular_grid((u_compressed, v_compressed), lon_compressed,
          lat_compressed, (model_index.var_x),
          (model_index.var_y), interp_method=interp_method)

    def output_native_grid(self, time_index, target_depth):
        """Generate output using native grid coordinates"""
        u_target_depth, v_target_depth = vertical_interpolation(self.var_u, self.var_v, self.var_mask, self.var_zeta, self.var_depth, self.var_sigma, self.num_sigma, self.num_ny, self.num_nx, time_index, target_depth)
        water_lat_rho = numpy.ma.masked_array(self.var_lat, numpy.logical_not(self.var_mask))
        water_lon_rho = numpy.ma.masked_array(self.var_lon, numpy.logical_not(self.var_mask))
        water_u = numpy.ma.masked_array(u_target_depth, numpy.logical_not(self.var_mask))
        water_v = numpy.ma.masked_array(v_target_depth, numpy.logical_not(self.var_mask))
        u_compressed = numpy.ma.compressed(water_u)
        v_compressed = numpy.ma.compressed(water_v)
        lat_compressed = numpy.ma.compressed(water_lat_rho)
        lon_compressed = numpy.ma.compressed(water_lon_rho)
        return (
         u_compressed, v_compressed, lat_compressed, lon_compressed)


def vertical_interpolation(u, v, mask, zeta, depth, sigma, num_sigma, num_ny, num_nx, time_index, target_depth):
    """Vertically interpolate variables to target depth.

    Args:
        u: `numpy.ndarray` containing u values for entire grid.
        v: `numpy.ndarray` containing v values for entire grid.
        mask: `numpy.ndarray` containing masked values.
        zeta: `numpy.ndarray` containing MSL free surface in meters.
        depth: `numpy.ndarray` containing bathymetry in meters, positive down.
        sigma: Vertical coordinate, positive down, 0 - surface , 1 - bottom
        num_sigma: Number of sigma layers.
        num_ny: y dimensions.
        num_nx: x dimensions
        time_index: Single forecast time index value.
        target_depth: The target depth-below-sea-surface to which water
            currents will be interpolated, in meters. Must be zero or greater.
            For areas shallower than double this value, values will be
            interpolated to half the water column height instead. For
            navigationally significant currents, a value of 4.5 is recommended.
    """
    true_depth = zeta[time_index, :] + depth
    sigma_depth_layers = numpy.ma.empty(shape=[num_sigma, num_ny, num_nx])
    for k in range(num_sigma):
        sigma_depth_layers[k, :] = sigma[k] * true_depth

    if target_depth < 0:
        raise Exception('Target depth must be positive')
    interp_depth = -1 * numpy.minimum(target_depth * 2, true_depth) / 2
    u_target_depth = numpy.ma.empty(shape=[num_ny, num_nx])
    v_target_depth = numpy.ma.empty(shape=[num_ny, num_nx])
    for ny in range(num_ny):
        for nx in range(num_nx):
            if mask[(ny, nx)] != 0:
                u_interp_depth = interpolate.interp1d((sigma_depth_layers[:, ny, nx]), (u[time_index, :, ny, nx]), fill_value='extrapolate')
                u_target_depth[(ny, nx)] = u_interp_depth(interp_depth.data[(ny, nx)])
                v_interp_depth = interpolate.interp1d((sigma_depth_layers[:, ny, nx]), (v[time_index, :, ny, nx]), fill_value='extrapolate')
                v_target_depth[(ny, nx)] = v_interp_depth(interp_depth.data[(ny, nx)])

    return (
     u_target_depth, v_target_depth)