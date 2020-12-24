# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/config.py
# Compiled at: 2020-03-23 16:44:23
# Size of source mod 2**32: 37586 bytes
"""
Configuration object required to rund a Mapchete process.

Before running a process, a MapcheteConfig object has to be initialized by
either using a Mapchete file or a dictionary holding the process parameters.
Upon creation, all parameters are validated and the InputData objects are
created which are then exposed to the user process.

An invalid process configuration or an invalid process file cause an Exception
when initializing the configuration.
"""
from cached_property import cached_property
from collections import OrderedDict
from copy import deepcopy
import imp, importlib, inspect, logging, operator, os, oyaml as yaml, py_compile
from shapely import wkt
from shapely.geometry import box
from shapely.ops import cascaded_union
from tilematrix._funcs import Bounds
import warnings
from mapchete.validate import validate_bounds, validate_zooms, validate_values, validate_bufferedtilepyramid
from mapchete.errors import MapcheteConfigError, MapcheteProcessSyntaxError, MapcheteProcessImportError, MapcheteDriverError
from mapchete.formats import load_output_reader, load_output_writer, available_output_formats, load_input_reader
from mapchete.io import absolute_path
from mapchete.log import add_module_logger
from mapchete.tile import BufferedTilePyramid
logger = logging.getLogger(__name__)
_MANDATORY_PARAMETERS = [
 (
  'process', str),
 (
  'pyramid', dict),
 (
  'input', (dict, type(None))),
 (
  'output', dict),
 (
  'zoom_levels', (int, dict, list))]
_RESERVED_PARAMETERS = [
 'baselevels',
 'bounds',
 'process',
 'config_dir',
 'process_minzoom',
 'process_maxzoom',
 'process_zoom',
 'process_bounds',
 'metatiling',
 'pixelbuffer']

class MapcheteConfig(object):
    __doc__ = "\n    Process configuration.\n\n    MapcheteConfig reads and parses a Mapchete configuration, verifies the\n    parameters, creates the necessary metadata required and provides the\n    configuration snapshot for every zoom level.\n\n    Parameters\n    ----------\n    input_config : string or dictionary\n        a Mapchete configuration file or a configuration dictionary\n    zoom : list or integer\n        zoom level or a pair of minimum and maximum zoom level the process is\n        initialized with\n    bounds : tuple\n        left, bottom, right, top boundaries the process is initalized with\n    single_input_file : string\n        single input file if supported by process\n    mode : string\n        * ``memory``: Generate process output on demand without reading\n          pre-existing data or writing new data.\n        * ``readonly``: Just read data without processing new data.\n        * ``continue``: (default) Don't overwrite existing output.\n        * ``overwrite``: Overwrite existing output.\n\n    Attributes\n    ----------\n    mode : string\n        process mode\n    process : string\n        absolute path to process file\n    config_dir : string\n        path to configuration directory\n    process_pyramid : ``tilematrix.TilePyramid``\n        ``TilePyramid`` used to process data\n    output_pyramid : ``tilematrix.TilePyramid``\n        ``TilePyramid`` used to write output data\n    input : dictionary\n        inputs for process\n    output : ``OutputData``\n        driver specific output object\n    zoom_levels : list\n        process zoom levels\n    bounds : tuple\n        process bounds\n    init_zoom_levels : list\n        zoom levels the process configuration was initialized with\n    init_bounds : tuple\n        bounds the process configuration was initialized with\n    baselevels : dictionary\n        base zoomlevels, where data is processed; zoom levels not included are\n        generated from baselevels\n\n    Deprecated Attributes\n    ---------------------\n    raw : dictionary\n        raw process configuration\n    mapchete_file : string\n        path to Mapchete file\n    output_type : string (moved to OutputData)\n        process output type (``raster`` or ``vector``)\n    crs : ``rasterio.crs.CRS`` (moved to process_pyramid)\n        object describing the process coordinate reference system\n    pixelbuffer : integer (moved to process_pyramid)\n        buffer around process tiles\n    metatiling : integer (moved to process_pyramid)\n        process metatiling\n    "

    def __init__(self, input_config, zoom=None, bounds=None, single_input_file=None, mode='continue', debug=False):
        """Initialize configuration."""
        self._raw = _map_to_new_config(_config_to_dict(input_config))
        self._raw['init_zoom_levels'] = zoom
        self._raw['init_bounds'] = bounds
        self._cache_area_at_zoom = {}
        self._cache_full_process_area = None
        try:
            validate_values(self._raw, _MANDATORY_PARAMETERS)
        except Exception as e:
            raise MapcheteConfigError(e)

        logger.debug('validating process code')
        self.config_dir = self._raw['config_dir']
        self.process_name = self.process_path = self._raw['process']
        self.process_func
        logger.debug('initializing pyramids')
        try:
            process_metatiling = self._raw['pyramid'].get('metatiling', 1)
            output_metatiling = self._raw['output'].get('metatiling', process_metatiling)
            if output_metatiling > process_metatiling:
                raise ValueError('output metatiles must be smaller than process metatiles')
            self.process_pyramid = BufferedTilePyramid(self._raw['pyramid']['grid'], metatiling=process_metatiling, pixelbuffer=self._raw['pyramid'].get('pixelbuffer', 0))
            self.output_pyramid = BufferedTilePyramid(self._raw['pyramid']['grid'], metatiling=output_metatiling, pixelbuffer=self._raw['output'].get('pixelbuffer', 0))
        except Exception as e:
            logger.exception(e)
            raise MapcheteConfigError(e)

        if mode not in ('memory', 'continue', 'readonly', 'overwrite'):
            raise MapcheteConfigError('unknown mode %s' % mode)
        self.mode = mode
        self._init_inputs = False if self.mode == 'readonly' or (not len(set(self.baselevels['zooms']).intersection(set(self.init_zoom_levels))) if self.baselevels else False) else True
        logger.debug('preparing process parameters')
        self._params_at_zoom = _raw_at_zoom(self._raw, self.init_zoom_levels)
        self._delimiters = dict(zoom=self.init_zoom_levels, bounds=self.init_bounds, process_bounds=self.bounds, effective_bounds=self.effective_bounds)
        logger.debug('initializing output')
        self.output
        logger.debug('initializing input')
        self.input
        logger.debug('prepare output')
        self.output.prepare(process_area=self.area_at_zoom())

    @cached_property
    def zoom_levels(self):
        """Process zoom levels as defined in the configuration."""
        return validate_zooms(self._raw['zoom_levels'])

    @cached_property
    def init_zoom_levels(self):
        """
        Zoom levels this process is currently initialized with.

        This gets triggered by using the ``zoom`` kwarg. If not set, it will
        be equal to self.zoom_levels.
        """
        try:
            return get_zoom_levels(process_zoom_levels=self._raw['zoom_levels'], init_zoom_levels=self._raw['init_zoom_levels'])
        except Exception as e:
            raise MapcheteConfigError(e)

    @cached_property
    def bounds(self):
        """Process bounds as defined in the configuration."""
        if self._raw['bounds'] is None:
            return self.process_pyramid.bounds
            try:
                return validate_bounds(self._raw['bounds'])
            except Exception as e:
                raise MapcheteConfigError(e)

    @cached_property
    def init_bounds(self):
        """
        Process bounds this process is currently initialized with.

        This gets triggered by using the ``init_bounds`` kwarg. If not set, it will
        be equal to self.bounds.
        """
        if self._raw['init_bounds'] is None:
            return self.bounds
            try:
                return validate_bounds(self._raw['init_bounds'])
            except Exception as e:
                raise MapcheteConfigError(e)

    @cached_property
    def effective_bounds(self):
        """
        Effective process bounds required to initialize inputs.

        Process bounds sometimes have to be larger, because all intersecting process
        tiles have to be covered as well.
        """
        return snap_bounds(bounds=clip_bounds(bounds=self.init_bounds, clip=self.process_pyramid.bounds), pyramid=self.process_pyramid, zoom=min(self.baselevels['zooms']) if self.baselevels else min(self.init_zoom_levels))

    @cached_property
    def _output_params(self):
        """Output params of driver."""
        output_params = dict(self._raw['output'], grid=self.output_pyramid.grid, pixelbuffer=self.output_pyramid.pixelbuffer, metatiling=self.output_pyramid.metatiling, delimiters=self._delimiters, mode=self.mode)
        if 'path' in output_params:
            output_params.update(path=absolute_path(path=output_params['path'], base_dir=self.config_dir))
        if 'format' not in output_params:
            raise MapcheteConfigError('output format not specified')
        if output_params['format'] not in available_output_formats():
            raise MapcheteConfigError('format %s not available in %s' % (
             output_params['format'], str(available_output_formats())))
        return output_params

    @cached_property
    def output(self):
        """Output writer class of driver."""
        writer = load_output_writer(self._output_params)
        try:
            writer.is_valid_with_config(self._output_params)
        except Exception as e:
            logger.exception(e)
            raise MapcheteConfigError('driver %s not compatible with configuration: %s' % (
             writer.METADATA['driver_name'], e))

        return writer

    @cached_property
    def output_reader(self):
        """Output reader class of driver."""
        if self.baselevels:
            return load_output_reader(self._output_params)
        else:
            return self.output

    @cached_property
    def input(self):
        """
        Input items used for process stored in a dictionary.

        Keys are the hashes of the input parameters, values the respective InputData
        classes.

        If process mode is `readonly` or if only overviews are about to be built, no
        inputs are required and thus not initialized due to performance reasons. However,
        process bounds which otherwise are dependant on input bounds, may change if not
        explicitly provided in process configuration.
        """
        raw_inputs = OrderedDict([(get_hash(v), v) for zoom in self.init_zoom_levels if 'input' in self._params_at_zoom[zoom] for key, v in _flatten_tree(self._params_at_zoom[zoom]['input']) if v is not None])
        initalized_inputs = OrderedDict()
        if self._init_inputs:
            for k, v in raw_inputs.items():
                if isinstance(v, str):
                    logger.debug('load input reader for simple input %s', v)
                    try:
                        reader = load_input_reader(dict(path=absolute_path(path=v, base_dir=self.config_dir), pyramid=self.process_pyramid, pixelbuffer=self.process_pyramid.pixelbuffer, delimiters=self._delimiters), readonly=self.mode == 'readonly')
                    except Exception as e:
                        logger.exception(e)
                        raise MapcheteDriverError('error when loading input %s: %s' % (v, e))

                    logger.debug('input reader for simple input %s is %s', v, reader)
                else:
                    if isinstance(v, dict):
                        logger.debug('load input reader for abstract input %s', v)
                        try:
                            reader = load_input_reader(dict(abstract=deepcopy(v), pyramid=self.process_pyramid, pixelbuffer=self.process_pyramid.pixelbuffer, delimiters=self._delimiters, conf_dir=self.config_dir), readonly=self.mode == 'readonly')
                        except Exception as e:
                            logger.exception(e)
                            raise MapcheteDriverError('error when loading input %s: %s' % (v, e))

                        logger.debug('input reader for abstract input %s is %s', v, reader)
                    else:
                        raise MapcheteConfigError('invalid input type %s', type(v))
                reader.bbox(out_crs=self.process_pyramid.crs)
                initalized_inputs[k] = reader

        else:
            for k in raw_inputs.keys():
                initalized_inputs[k] = None

        return initalized_inputs

    @cached_property
    def baselevels(self):
        """
        Optional baselevels configuration.

        baselevels:
            min: <zoom>
            max: <zoom>
            lower: <resampling method>
            higher: <resampling method>
        """
        if 'baselevels' not in self._raw:
            return {}
        baselevels = self._raw['baselevels']
        minmax = {k:v for k, v in baselevels.items() if k in ('min', 'max') if k in ('min',
                                                                                     'max')}
        if not minmax:
            raise MapcheteConfigError('no min and max values given for baselevels')
        for v in minmax.values():
            if not isinstance(v, int) or v < 0:
                raise MapcheteConfigError('invalid baselevel zoom parameter given: %s' % minmax.values())

        zooms = list(range(minmax.get('min', min(self.zoom_levels)), minmax.get('max', max(self.zoom_levels)) + 1))
        if not set(self.zoom_levels).difference(set(zooms)):
            raise MapcheteConfigError('baselevels zooms fully cover process zooms')
        return dict(zooms=zooms, lower=baselevels.get('lower', 'nearest'), higher=baselevels.get('higher', 'nearest'), tile_pyramid=BufferedTilePyramid(self.output_pyramid.grid, pixelbuffer=self.output_pyramid.pixelbuffer, metatiling=self.process_pyramid.metatiling))

    @cached_property
    def process_func(self):
        return get_process_func(process_path=self.process_path, config_dir=self.config_dir, run_compile=True)

    def get_process_func_params(self, zoom):
        return {k:v for k, v in self.params_at_zoom(zoom).items() if k in inspect.signature(self.process_func).parameters}

    def get_inputs_for_tile(self, tile):

        def _open_inputs(i):
            for k, v in i.items():
                if v is None:
                    continue
                else:
                    if isinstance(v, dict):
                        yield (
                         k, list(_open_inputs(v)))
                    else:
                        yield (
                         k, v.open(tile))

        return OrderedDict(list(_open_inputs(self.params_at_zoom(tile.zoom)['input'])))

    def params_at_zoom(self, zoom):
        """
        Return configuration parameters snapshot for zoom as dictionary.

        Parameters
        ----------
        zoom : int
            zoom level

        Returns
        -------
        configuration snapshot : dictionary
        zoom level dependent process configuration
        """
        if zoom not in self.init_zoom_levels:
            raise ValueError('zoom level not available with current configuration')
        out = OrderedDict(self._params_at_zoom[zoom], input=OrderedDict(), output=self.output)
        if 'input' in self._params_at_zoom[zoom]:
            flat_inputs = OrderedDict()
            for k, v in _flatten_tree(self._params_at_zoom[zoom]['input']):
                if v is None:
                    flat_inputs[k] = None
                else:
                    flat_inputs[k] = self.input[get_hash(v)]

            out['input'] = _unflatten_tree(flat_inputs)
        else:
            out['input'] = OrderedDict()
        return out

    def area_at_zoom(self, zoom=None):
        """
        Return process bounding box for zoom level.

        Parameters
        ----------
        zoom : int or None
            if None, the union of all zoom level areas is returned

        Returns
        -------
        process area : shapely geometry
        """
        if not self._init_inputs:
            return box(*self.init_bounds)
        else:
            if zoom is None:
                if not self._cache_full_process_area:
                    logger.debug('calculate process area ...')
                    self._cache_full_process_area = cascaded_union([self._area_at_zoom(z) for z in self.init_zoom_levels]).buffer(0)
                return self._cache_full_process_area
            if zoom not in self.init_zoom_levels:
                raise ValueError('zoom level not available with current configuration')
            return self._area_at_zoom(zoom)

    def _area_at_zoom(self, zoom):
        if zoom not in self._cache_area_at_zoom:
            if 'input' in self._params_at_zoom[zoom]:
                input_union = cascaded_union([self.input[get_hash(v)].bbox(self.process_pyramid.crs) for k, v in _flatten_tree(self._params_at_zoom[zoom]['input']) if v is not None])
                self._cache_area_at_zoom[zoom] = input_union.intersection(box(*self.init_bounds)) if self.init_bounds else input_union
            else:
                self._cache_area_at_zoom[zoom] = box(*self.init_bounds)
            return self._cache_area_at_zoom[zoom]

    def bounds_at_zoom(self, zoom=None):
        """
        Return process bounds for zoom level.

        Parameters
        ----------
        zoom : integer or list

        Returns
        -------
        process bounds : tuple
            left, bottom, right, top
        """
        if self.area_at_zoom(zoom).is_empty:
            return ()
        return Bounds(*self.area_at_zoom(zoom).bounds)

    @cached_property
    def crs(self):
        """Deprecated."""
        warnings.warn(DeprecationWarning('self.crs is now self.process_pyramid.crs.'))
        return self.process_pyramid.crs

    @cached_property
    def metatiling(self):
        """Deprecated."""
        warnings.warn(DeprecationWarning('self.metatiling is now self.process_pyramid.metatiling.'))
        return self.process_pyramid.metatiling

    @cached_property
    def pixelbuffer(self):
        """Deprecated."""
        warnings.warn(DeprecationWarning('self.pixelbuffer is now self.process_pyramid.pixelbuffer.'))
        return self.process_pyramid.pixelbuffer

    @cached_property
    def inputs(self):
        """Deprecated."""
        warnings.warn(DeprecationWarning('self.inputs renamed to self.input.'))
        return self.input

    @cached_property
    def process_file(self):
        """Deprecated."""
        warnings.warn(DeprecationWarning("'self.process_file' is deprecated"))
        return os.path.join(self._raw['config_dir'], self._raw['process'])

    def at_zoom(self, zoom):
        """Deprecated."""
        warnings.warn(DeprecationWarning('Method renamed to self.params_at_zoom(zoom).'))
        return self.params_at_zoom(zoom)

    def process_area(self, zoom=None):
        """Deprecated."""
        warnings.warn(DeprecationWarning('Method renamed to self.area_at_zoom(zoom).'))
        return self.area_at_zoom(zoom)

    def process_bounds(self, zoom=None):
        """Deprecated."""
        warnings.warn(DeprecationWarning('Method renamed to self.bounds_at_zoom(zoom).'))
        return self.bounds_at_zoom(zoom)


def get_hash(x):
    """Return hash of x."""
    if isinstance(x, str):
        return hash(x)
    if isinstance(x, dict):
        return hash(yaml.dump(x))


def get_zoom_levels(process_zoom_levels=None, init_zoom_levels=None):
    """Validate and return zoom levels."""
    process_zoom_levels = validate_zooms(process_zoom_levels)
    if init_zoom_levels is None:
        return process_zoom_levels
    else:
        init_zoom_levels = validate_zooms(init_zoom_levels)
        if not set(init_zoom_levels).issubset(set(process_zoom_levels)):
            raise ValueError('init zooms must be a subset of process zoom')
        return init_zoom_levels


def snap_bounds(bounds=None, pyramid=None, zoom=None):
    """
    Snaps bounds to tiles boundaries of specific zoom level.

    Parameters
    ----------
    bounds : bounds to be snapped
    pyramid : TilePyramid
    zoom : int

    Returns
    -------
    Bounds(left, bottom, right, top)
    """
    bounds = validate_bounds(bounds)
    pyramid = validate_bufferedtilepyramid(pyramid)
    lb = pyramid.tile_from_xy(bounds.left, bounds.bottom, zoom, on_edge_use='rt').bounds
    rt = pyramid.tile_from_xy(bounds.right, bounds.top, zoom, on_edge_use='lb').bounds
    return Bounds(lb.left, lb.bottom, rt.right, rt.top)


def clip_bounds(bounds=None, clip=None):
    """
    Clips bounds by clip.

    Parameters
    ----------
    bounds : bounds to be clipped
    clip : clip bounds

    Returns
    -------
    Bounds(left, bottom, right, top)
    """
    bounds = validate_bounds(bounds)
    clip = validate_bounds(clip)
    return Bounds(max(bounds.left, clip.left), max(bounds.bottom, clip.bottom), min(bounds.right, clip.right), min(bounds.top, clip.top))


def raw_conf(mapchete_file):
    """
    Loads a mapchete_file into a dictionary.

    Parameters
    ----------
    mapchete_file : str
        Path to a Mapchete file.

    Returns
    -------
    dictionary
    """
    if isinstance(mapchete_file, dict):
        return _map_to_new_config(mapchete_file)
    else:
        return _map_to_new_config(yaml.safe_load(open(mapchete_file, 'r').read()))


def raw_conf_process_pyramid(raw_conf):
    """
    Loads the process pyramid of a raw configuration.

    Parameters
    ----------
    raw_conf : dict
        Raw mapchete configuration as dictionary.

    Returns
    -------
    BufferedTilePyramid
    """
    return BufferedTilePyramid(raw_conf['pyramid']['grid'], metatiling=raw_conf['pyramid'].get('metatiling', 1), pixelbuffer=raw_conf['pyramid'].get('pixelbuffer', 0))


def raw_conf_output_pyramid(raw_conf):
    """
    Loads the process pyramid of a raw configuration.

    Parameters
    ----------
    raw_conf : dict
        Raw mapchete configuration as dictionary.

    Returns
    -------
    BufferedTilePyramid
    """
    return BufferedTilePyramid(raw_conf['pyramid']['grid'], metatiling=raw_conf['output'].get('metatiling', raw_conf['pyramid'].get('metatiling', 1)), pixelbuffer=raw_conf['pyramid'].get('pixelbuffer', raw_conf['pyramid'].get('pixelbuffer', 0)))


def bounds_from_opts(wkt_geometry=None, point=None, bounds=None, zoom=None, raw_conf=None):
    """
    Loads the process pyramid of a raw configuration.

    Parameters
    ----------
    raw_conf : dict
        Raw mapchete configuration as dictionary.

    Returns
    -------
    BufferedTilePyramid
    """
    if wkt_geometry:
        return Bounds(*wkt.loads(wkt_geometry).bounds)
    else:
        if point:
            x, y = point
            zoom_levels = get_zoom_levels(process_zoom_levels=raw_conf['zoom_levels'], init_zoom_levels=zoom)
            tp = raw_conf_process_pyramid(raw_conf)
            return Bounds(*tp.tile_from_xy(x, y, max(zoom_levels)).bounds)
        if bounds is not None:
            return validate_bounds(bounds)
        return bounds


def get_process_func(process_path=None, config_dir=None, run_compile=False):
    logger.debug('get process function from %s', process_path)
    process_module = _load_process_module(process_path=process_path, config_dir=config_dir, run_compile=run_compile)
    try:
        if hasattr(process_module, 'Process'):
            logger.error('instanciating MapcheteProcess is deprecated, provide execute() function instead')
        if hasattr(process_module, 'execute'):
            return process_module.execute
        raise ImportError('No execute() function found in %s' % process_path)
    except ImportError as e:
        raise MapcheteProcessImportError(e)


def _load_process_module(process_path=None, config_dir=None, run_compile=False):
    if process_path.endswith('.py'):
        abs_path = os.path.join(config_dir, process_path)
        if not os.path.isfile(abs_path):
            raise MapcheteConfigError('%s is not available' % abs_path)
        try:
            if run_compile:
                py_compile.compile(abs_path, doraise=True)
            module = imp.load_source(os.path.splitext(os.path.basename(abs_path))[0], abs_path)
            add_module_logger(module.__name__)
        except py_compile.PyCompileError as e:
            raise MapcheteProcessSyntaxError(e)
        except ImportError as e:
            raise MapcheteProcessImportError(e)

    else:
        try:
            module = importlib.import_module(process_path)
        except ImportError as e:
            raise MapcheteProcessImportError(e)

        return module


def _config_to_dict(input_config):
    if isinstance(input_config, dict):
        if 'config_dir' not in input_config:
            raise MapcheteConfigError('config_dir parameter missing')
        return OrderedDict(input_config, mapchete_file=None)
    if os.path.splitext(input_config)[1] == '.mapchete':
        with open(input_config, 'r') as (config_file):
            return OrderedDict(yaml.safe_load(config_file.read()), config_dir=os.path.dirname(os.path.realpath(input_config)), mapchete_file=input_config)
    else:
        raise MapcheteConfigError('Configuration has to be a dictionary or a .mapchete file.')


def _raw_at_zoom(config, zooms):
    """Return parameter dictionary per zoom level."""
    params_per_zoom = OrderedDict()
    for zoom in zooms:
        params = OrderedDict()
        for name, element in config.items():
            if name not in _RESERVED_PARAMETERS:
                out_element = _element_at_zoom(name, element, zoom)
                if out_element is not None:
                    params[name] = out_element

        params_per_zoom[zoom] = params

    return OrderedDict(params_per_zoom)


def _element_at_zoom(name, element, zoom):
    """
        Return the element filtered by zoom level.

        - An input integer or float gets returned as is.
        - An input string is checked whether it starts with "zoom". Then, the
          provided zoom level gets parsed and compared with the actual zoom
          level. If zoom levels match, the element gets returned.
        TODOs/gotchas:
        - Provided zoom levels for one element in config file are not allowed
          to "overlap", i.e. there is not yet a decision mechanism implemented
          which handles this case.
        """
    if isinstance(element, dict):
        if 'format' in element:
            return element
        out_elements = OrderedDict()
        for sub_name, sub_element in element.items():
            out_element = _element_at_zoom(sub_name, sub_element, zoom)
            if name == 'input':
                out_elements[sub_name] = out_element
            elif out_element is not None:
                out_elements[sub_name] = out_element

        if len(out_elements) == 1 and name != 'input':
            return next(iter(out_elements.values()))
        if len(out_elements) == 0:
            return
        return out_elements
    if isinstance(name, str):
        if name.startswith('zoom'):
            return _filter_by_zoom(conf_string=name.strip('zoom').strip(), zoom=zoom, element=element)
        else:
            return element
    else:
        return element


def _filter_by_zoom(element=None, conf_string=None, zoom=None):
    """Return element only if zoom condition matches with config string."""
    for op_str, op_func in [
     (
      '=', operator.eq),
     (
      '<=', operator.le),
     (
      '>=', operator.ge),
     (
      '<', operator.lt),
     (
      '>', operator.gt)]:
        if conf_string.startswith(op_str):
            if op_func(zoom, _strip_zoom(conf_string, op_str)):
                return element
            else:
                return


def _strip_zoom(input_string, strip_string):
    """Return zoom level as integer or throw error."""
    try:
        return int(input_string.strip(strip_string))
    except Exception as e:
        raise MapcheteConfigError('zoom level could not be determined: %s' % e)


def _flatten_tree(tree, old_path=None):
    """Flatten dict tree into dictionary where keys are paths of old dict."""
    flat_tree = []
    for key, value in tree.items():
        new_path = '/'.join([old_path, key]) if old_path else key
        if isinstance(value, dict) and 'format' not in value:
            flat_tree.extend(_flatten_tree(value, old_path=new_path))
        else:
            flat_tree.append((new_path, value))

    return flat_tree


def _unflatten_tree(flat):
    """Reverse tree flattening."""
    tree = OrderedDict()
    for key, value in flat.items():
        path = key.split('/')
        if len(path) == 1:
            tree[key] = value
        else:
            if path[0] not in tree:
                tree[path[0]] = _unflatten_tree({'/'.join(path[1:]): value})
            else:
                branch = _unflatten_tree({'/'.join(path[1:]): value})
                if path[1] not in tree[path[0]]:
                    tree[path[0]][path[1]] = branch[path[1]]
                else:
                    tree[path[0]][path[1]].update(branch[path[1]])

    return tree


def _map_to_new_config(config):
    try:
        validate_values(config, [('output', dict)])
    except Exception as e:
        raise MapcheteConfigError(e)

    if 'type' in config['output']:
        warnings.warn(DeprecationWarning("'type' is deprecated and should be 'grid'"))
        if 'grid' not in config['output']:
            config['output']['grid'] = config['output'].pop('type')
    if 'pyramid' not in config:
        warnings.warn(DeprecationWarning("'pyramid' needs to be defined in root config element."))
        config['pyramid'] = dict(grid=config['output']['grid'], metatiling=config.get('metatiling', 1), pixelbuffer=config.get('pixelbuffer', 0))
    if 'zoom_levels' not in config:
        warnings.warn(DeprecationWarning("use new config element 'zoom_levels' instead of 'process_zoom', 'process_minzoom' and 'process_maxzoom'"))
        if 'process_zoom' in config:
            config['zoom_levels'] = config['process_zoom']
    else:
        if all([i in config for i in ['process_minzoom', 'process_maxzoom']]):
            config['zoom_levels'] = dict(min=config['process_minzoom'], max=config['process_maxzoom'])
        else:
            raise MapcheteConfigError('process zoom levels not provided in config')
        if 'bounds' not in config:
            if 'process_bounds' in config:
                warnings.warn(DeprecationWarning("'process_bounds' are deprecated and renamed to 'bounds'"))
                config['bounds'] = config['process_bounds']
        else:
            config['bounds'] = None
    if 'input' not in config:
        if 'input_files' in config:
            warnings.warn(DeprecationWarning("'input_files' are deprecated and renamed to 'input'"))
            config['input'] = config['input_files']
        else:
            raise MapcheteConfigError("no 'input' found")
    elif 'input_files' in config:
        raise MapcheteConfigError("'input' and 'input_files' are not allowed at the same time")
    if 'process_file' in config:
        warnings.warn(DeprecationWarning("'process_file' is deprecated and renamed to 'process'"))
        config['process'] = config.pop('process_file')
    return config