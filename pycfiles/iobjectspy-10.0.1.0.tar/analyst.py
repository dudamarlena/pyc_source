# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\analyst.py
# Compiled at: 2019-12-31 04:08:57
# Size of source mod 2**32: 808690 bytes
r"""
ananlyst 模块提供了常用的空间数据处理和分析的功能，用户使用analyst 模块可以进行缓冲区分析( :py:meth:`create_buffer` )、叠加分析( :py:meth:`overlay` )、
创建泰森多边形( :py:meth:`create_thiessen_polygons` )、拓扑构面( :py:meth:`topology_build_regions` )、密度聚类( :py:meth:`kernel_density` )、
插值分析( :py:meth:`interpolate` )，栅格代数运算( :py:meth:`expression_math_analyst` )等功能。

在 analyst 模块的所有接口中，对输入数据参数要求为数据集（ :py:class:`.Dataset` , :py:class:`.DatasetVector` , :py:class:`.DatasetImage` , :py:class:`.DatasetGrid` ）的参数，
都接受直接输入一个数据集对象（Dataset）或数据源别名与数据集名称的组合（例如，'alias/dataset_name', 'alias\\\dataset_name'),也支持数据源连接信息与数据集名称的组合（例如，'E:/data.udb/dataset_name')。

    - 支持设置数据集

        >>> ds = Datasource.open('E:/data.udb')
        >>> create_buffer(ds['point'], 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

    - 支持设置数据集别名和数据集名称组合

        >>> create_buffer(ds.alias + '/point' + , 10, 10, unit='Meter', out_data='E:/buffer_out.udb')
        >>> create_buffer(ds.alias + '\\point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')
        >>> create_buffer(ds.alias + '|point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

    - 支持设置 udb 文件路径和数据集名称组合

        >>> create_buffer('E:/data.udb/point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

    - 支持设置数据源连接信息和数据集名称组合，数据源连接信息包括 dcf 文件、xml 字符串等，具体参考 :py:meth:`.DatasourceConnectionInfo.make`

        >>> create_buffer('E:/data_ds.dcf/point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

.. Note:: 当输入的是数据源信息时，程序会自动打开数据源，但是接口运行结束时不会自动关闭数据源，也就是打开后的数据源会存在当前工作空间中

在 analyst 模块中所有接口中，对输出数据参数要求为数据源（ :py:class:`.Datasource` ）的，均接受 Datasource 对象，也可以为 :py:class:`.DatasourceConnectionInfo` 对象，
同时，也支持当前工作空间下数据源的别名，也支持 UDB 文件路径，DCF 文件路径等。

    - 支持设置 udb 文件路径

        >>> create_buffer('E:/data.udb/point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

    - 支持设置数据源对象

        >>> ds = Datasource.open('E:/buffer_out.udb')
        >>> create_buffer('E:/data.udb/point', 10, 10, unit='Meter', out_data=ds)
        >>> ds.close()

    - 支持设置数据源别名

        >>> ds_conn = DatasourceConnectionInfo('E:/buffer_out.udb', alias='my_datasource')
        >>> create_buffer('E:/data.udb/point', 10, 10, unit='Meter', out_data='my_datasource')

.. Note:: 如果输出数据的参数输入的是数据源连接信息或 UDB 文件路径等，程序会自动打开数据源，如果是 UDB 数据源而本地不存在，还会自动新建一个UDB数据源，但需要确保UDB数据源所在的文件目录存在而且可写。
          在功能完成后，如果数据源是由程序自动打开或创建的，会被自动关闭掉（这里与输入数据为 Dataset 不同，输入数据中被自动打开的数据源不会自动关闭）。所以，对于有些接口
          输出结果为数据集的，就会返回结果数据集的名称，如果传入的是数据源对象，返回的便是结果数据集。

"""
from ._gateway import get_gateway, get_jvm, safe_start_callback_server, close_callback_server
from .data import Datasource, Colors, DatasetVector, Recordset, Point2D, Geometry, DatasetImage, DatasetGrid, Rectangle, GeoRegion, GeoLine, GeoRegion3D, Point3D, GeoLine3D
from data._listener import ProgressListener
from data._util import to_java_recordset_array, to_java_point2d_array, get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource, create_result_datasaet, to_java_stattype_array, to_java_geometry_array, to_java_point3ds, to_java_datasetgrid_array, to_java_datasetvector_array, to_java_point2ds, to_java_dataset_array
from .enums import *
from ._utils import *
from ._logger import *
__all__ = [
 'create_buffer', 'overlay', 'dissolve', 'aggregate_points', 'smooth_vector', 'resample_vector',
 'create_thiessen_polygons', 'summary_points', 'clip_vector', 'ProcessingOptions', 'topology_processing',
 'topology_build_regions', 'update_attributes', 'pickup_border', 'simplify_building', 'PreprocessOptions',
 'preprocess', 'topology_validate', 'resample_raster', 'ReclassSegment', 'ReclassMappingTable',
 'reclass_grid', 'aggregate_grid', 'slice_grid', 'compute_range_raster', 'compute_range_vector',
 'density_based_clustering', 'hierarchical_density_based_clustering', 'ordering_density_based_clustering',
 'NeighbourShape', 'NeighbourShapeRectangle', 'NeighbourShapeCircle',
 'NeighbourShapeAnnulus', 'NeighbourShapeWedge', 'kernel_density', 'point_density', 'clip_raster',
 'InterpolationDensityParameter', 'InterpolationIDWParameter', 'InterpolationKrigingParameter',
 'InterpolationRBFParameter', 'interpolate', 'interpolate_points', 'idw_interpolate', 'density_interpolate',
 'kriging_interpolate', 'rbf_interpolate', 'vector_to_raster', 'raster_to_vector', 'cost_distance',
 'cost_path', 'cost_path_line', 'path_line', 'straight_distance', 'surface_distance', 'surface_path_line',
 'calculate_hill_shade', 'calculate_slope', 'calculate_aspect', 'compute_point_aspect', 'compute_point_slope',
 'calculate_ortho_image', 'compute_surface_area', 'compute_surface_distance', 'compute_surface_volume',
 'divide_math_analyst', 'plus_math_analyst', 'minus_math_analyst', 'multiply_math_analyst',
 'to_float_math_analyst', 'to_int_math_analyst', 'expression_math_analyst', 'StatisticsField',
 'create_line_one_side_multi_buffer', 'create_multi_buffer', 'compute_min_distance',
 'compute_range_distance', 'integrate', 'eliminate', 'edge_match', 'region_to_center_line',
 'dual_line_to_center_line', 'grid_extract_isoline', 'grid_extract_isoregion', 'point_extract_isoline',
 'points_extract_isoregion', 'point3ds_extract_isoline', 'point3ds_extract_isoregion',
 'grid_basic_statistics', 'BasicStatisticsAnalystResult', 'grid_common_statistics',
 'grid_neighbour_statistics', 'altitude_statistics', 'pour_points',
 'GridHistogram', 'thin_raster', 'build_lake', 'build_terrain', 'area_solar_radiation_days',
 'area_solar_radiation_hours', 'basin', 'build_quad_mesh', 'fill_sink', 'flow_accumulation', 'flow_direction',
 'flow_length', 'stream_order', 'stream_to_line', 'stream_link', 'watershed', 'measure_central_element',
 'measure_directional', 'measure_linear_directional_mean', 'measure_mean_center',
 'measure_median_center', 'measure_standard_distance', 'AnalyzingPatternsResult', 'auto_correlation',
 'high_or_low_clustering', 'average_nearest_neighbor', 'incremental_auto_correlation', 'IncrementalResult',
 'cluster_outlier_analyst', 'hot_spot_analyst', 'optimized_hot_spot_analyst', 'collect_events',
 'build_weight_matrix', 'weight_matrix_file_to_table', 'GWR', 'GWRSummary', 'raster_mosaic',
 'split_lines_by_regions', 'zonal_statistics_on_raster_value',
 'OLSSummary', 'ordinary_least_squares', 'calculate_profile', 'CutFillResult', 'inverse_cut_fill',
 'cut_fill_grid', 'cut_fill_oblique', 'cut_fill_region', 'cut_fill_region3d', 'flood', 'thin_raster_bit',
 'ViewShedType', 'NDVI', 'NDWI', 'compute_features_envelope', 'calculate_view_shed', 'calculate_view_sheds',
 'VisibleResult', 'is_point_visible', 'are_points_visible', 'line_of_sight', 'radar_shield_angle',
 'InteractionDetectorResult', 'RiskDetectorMean', 'RiskDetectorResult', 'GeographicalDetectorResult',
 'geographical_detector']

class StatisticsField(object):
    __doc__ = '\n    对字段进行统计的信息。主要用于 :py:meth:`summary_points`\n    '

    def __init__(self, source_field=None, stat_type=None, result_field=None):
        """
        初始化对象

        :param str source_field: 被统计的字段名称
        :param stat_type: 统计类型
        :type stat_type: StatisticsFieldType or str
        :param str result_field: 结果字段名称
        """
        self._source_field = None
        self._stat_type = None
        self._result_field = None
        self.set_source_field(source_field).set_stat_type(stat_type).set_result_field(result_field)

    @property
    def source_field(self):
        """str: 被统计的字段名称"""
        return self._source_field

    @property
    def stat_type(self):
        """StatisticsFieldType: 字段统计类型"""
        return self._stat_type

    @property
    def result_field(self):
        """str: 结果字段名称"""
        return self._result_field

    def set_source_field(self, value):
        """
        设置被统计的字段名称

        :param str value: 字段名称
        :return: self
        :rtype: StatisticsField
        """
        if value is not None:
            self._source_field = value
        return self

    def set_stat_type(self, value):
        """
        设置字段统计类型

        :param value: 字段统计类型
        :type value: StatisticsFieldType or str
        :return: self
        :rtype: StatisticsField
        """
        if value is not None:
            self._stat_type = StatisticsFieldType._make(value)
        return self

    def set_result_field(self, value):
        """
        设置结果字段名称

        :param str value: 结果字段名称
        :return: self
        :rtype: StatisticsField
        """
        if value is not None:
            self._result_field = value
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        jvm = get_jvm()
        java_statField = jvm.com.supermap.analyst.spatialanalyst.StatisticsField()
        java_statField.setSourceField(self.source_field)
        java_statField.setMode(self.stat_type._jobject)
        java_statField.setResultField(self.result_field)
        return java_statField


def _throw_un_supported():
    raise Exception('Unsupported')


def create_buffer(input_data, distance_left, distance_right=None, unit=None, end_type=None, segment=24, is_save_attributes=True, is_union_result=False, out_data=None, out_dataset_name='BufferResult', progress=None):
    """
    创建矢量数据集或记录集的缓冲。

    缓冲区分析是围绕空间对象，使用一个或多个与这些对象的距离值（称为缓冲半径）作为半径，生成一个或多个区域的过程。缓冲区也可以理解为空间对象的一种影响或服务范围。

    缓冲区分析的基本作用对象是点、线、面。SuperMap 支持对二维点、线、面数据集（或记录集）和网络数据集进行缓冲区分析。其中，对网络数据集进行缓冲区分析时，是对其中的弧段作缓冲区。缓冲区的类型可以分析单重缓冲区（或称简单缓冲区）和多重缓冲区。下面以简单缓冲区为例分别介绍点、线、面的缓冲区。

    * 点缓冲区
      点的缓冲区是以点对象为圆心，以给定的缓冲距离为半径生成的圆形区域。当缓冲距离足够大时，两个或多个点对象的缓冲区可能有重叠。选择合并缓冲区时，重叠部分将被合并，最终得到的缓冲区是一个复杂面对象。

      .. image:: ../image/PointBuffer.png

    * 线缓冲区
      线的缓冲区是沿线对象的法线方向，分别向线对象的两侧平移一定的距离而得到两条线，并与在线端点处形成的光滑曲线（也可以形成平头）接合形成的封闭区域。同样，当缓冲距离足够大时，两个或多个线对象的缓冲区可能有重叠。合并缓冲区的效果与点的合并缓冲区相同。

      .. image:: ../image/LineBuffer.png

      线对象两侧的缓冲宽度可以不一致，从而生成左右不等缓冲区；也可以只在线对象的一侧创建单边缓冲区。此时只能生成平头缓冲区。

      .. image:: ../image/LineBuffer_1.png

    * 面缓冲区

      面的缓冲区生成方式与线的缓冲区类似，区别是面的缓冲区仅在面边界的一侧延展或收缩。当缓冲半径为正值时，缓冲区向面对象边界的外侧扩展；为负值时，向边界内收缩。同样，当缓冲距离足够大时，两个或多个线对象的缓冲区可能有重叠。也可以选择合并缓冲区，其效果与点的合并缓冲区相同。

      .. image:: ../image/RegionBuffer.png

    * 多重缓冲区是指在几何对象的周围，根据给定的若干缓冲区半径，建立相应数据量的缓冲区。对于线对象，还可以建立单边多重缓冲区，但注意不支持对网络数据集创建。

      .. image:: ../image/MultiBuffer.png

    缓冲区分析在 GIS 空间分析中经常用到，且往往结合叠加分析来共同解决实际问题。缓冲区分析在农业、城市规划、生态保护、防洪抗灾、军事、地质、环境等诸多领域都有应用。

    例如扩建道路时，可根据道路扩宽宽度对道路创建缓冲区，然后将缓冲区图层与建筑图层叠加，通过叠加分析查找落入缓冲区而需要被拆除的建筑；又如，为了保护环境和耕地，可对湿地、森林、草地和耕地进行缓冲区分析，在缓冲区内不允许进行工业建设。

    说明：

    *  对于面对象，在做缓冲区分析前最好先经过拓扑检查，排除面内相交的情况，所谓面内相交，指的是面对象自身相交，如图所示，图中数字代表面对象的节点顺序。

    .. image:: ../image/buffer_regioninter.png

    * 对“负半径”的说明

        * 如果缓冲区半径为数值型，则仅面数据支持负半径；
        * 如果缓冲区半径为字段或字段表达式，如果字段或字段表达式的值为负值，对于点、线数据取其绝对值；对于面数据，若合并缓冲区，则取其绝对值，若不合并，则按照负半径处理。

    :param input_data: 指定的创建缓冲区的源矢量记录集是数据集。支持点、线、面数据集和记录集。
    :type input_data: Recordset or DatasetVector or str
    :param distance_left: （左）缓冲区的距离。如果为字符串，则表示（左）缓冲距离所在的字段，即每个几何对象创建缓冲区时使用字段中存储的值作为缓冲半径。对于线对象，表示左缓冲区半径，对于点和面对象，表示缓冲区半径。
    :type distance_left: float or str
    :param distance_right: 右缓冲区的距离，如果为字符串，则表示右缓冲距离所在的字段，即每个线几何对象创建缓冲区时使用字段中存储的值作为右缓冲半径。该参数只对线对象有效。
    :type distance_right: float or str
    :param unit: 缓冲区距离半径单位，只支持距离单位，不支持角度和弧度单位。
    :type unit: Unit or str
    :param end_type: 缓冲区端点类型。用以区分线对象缓冲区分析时的端点是圆头缓冲还是平头缓冲。对于点或面对象，只支持圆头缓冲
    :type end_type: BufferEndType or str
    :param int segment: 半圆弧线段个数，即用多少个线段来模拟一个半圆，必须大于等于4。
    :param  bool is_save_attributes: 是否保留进行缓冲区分析的对象的字段属性。当合并结果面数据集时，该参数无效。即当 isUnion 参数为 false 时有效。
    :param bool is_union_result: 是否合并缓冲区，即是否将源数据各对象生成的所有缓冲区域进行合并运算后返回。对于面对象而言，要求源数据集中的面对象不相交。
    :param out_data: 存储结果数据的数据源
    :type out_data: Datasource
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _input = get_input_dataset(input_data)
    if _input is None:
        raise ValueError('input_data is None')
    else:
        if not isinstance(_input, (DatasetVector, Recordset)):
            raise ValueError('input_data required DatasetVector or Recordset, but now is ' + str(type(_input)))
        else:
            end_type = BufferEndType._make(end_type, BufferEndType.ROUND)
            if end_type is None:
                raise ValueError('invalid buffer end type object')
            else:
                _jvm = get_jvm()
                if unit is not None:
                    if isinstance(unit, Unit):
                        unit = unit.name
                    dist_unit = BufferRadiusUnit._make(unit, BufferRadiusUnit.METER)
                else:
                    dist_unit = BufferRadiusUnit.METER
            buffer_param = _jvm.com.supermap.analyst.spatialanalyst.BufferAnalystParameter()
            buffer_param.setEndType(end_type._jobject)
            buffer_param.setRadiusUnit(dist_unit._jobject)
            buffer_param.setSemicircleLineSegment(segment)
            buffer_param.setLeftDistance(distance_left)
            buffer_param.setRightDistance(distance_right)
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = 'buffer_result'
        else:
            _outDatasetName = out_dataset_name
    result_dt = create_result_datasaet(_ds, _outDatasetName, 'REGION')
    if isinstance(_input, DatasetVector):
        result_dt.set_prj_coordsys(_input.prj_coordsys)
    else:
        if isinstance(_input, Recordset):
            result_dt.set_prj_coordsys(_input.dataset.prj_coordsys)
        listener = None
        if progress is not None:
            if safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'create_buffer')
                    _jvm.com.supermap.analyst.spatialanalyst.BufferAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

        try:
            try:
                result = _jvm.com.supermap.analyst.spatialanalyst.BufferAnalyst.createBuffer(_input._jobject, result_dt._jobject, buffer_param, is_union_result, is_save_attributes)
            except Exception as e:
                try:
                    log_error(e)
                    result = False
                finally:
                    e = None
                    del e

        finally:
            if listener is not None:
                try:
                    _jvm.com.supermap.analyst.spatialanalyst.BufferAnalyst.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            if not result:
                out_datasource.delete(result_dt.name)
                result_dt = None
            if out_data is not None:
                return try_close_output_datasource(result_dt, out_datasource)
            return result_dt


def create_line_one_side_multi_buffer--- This code section failed: ---

 L. 401         0  LOAD_GLOBAL              check_lic
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  POP_TOP          

 L. 402         6  LOAD_GLOBAL              get_input_dataset
                8  LOAD_FAST                'input_data'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  STORE_FAST               '_input'

 L. 403        14  LOAD_FAST                '_input'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 404        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 'input_data is None'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 405        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                '_input'
               34  LOAD_GLOBAL              DatasetVector
               36  LOAD_GLOBAL              Recordset
               38  BUILD_TUPLE_2         2 
               40  CALL_FUNCTION_2       2  '2 positional arguments'
               42  POP_JUMP_IF_TRUE     64  'to 64'

 L. 406        44  LOAD_GLOBAL              ValueError
               46  LOAD_STR                 'input_data required DatasetVector or Recordset, but now is '
               48  LOAD_GLOBAL              str
               50  LOAD_GLOBAL              type
               52  LOAD_FAST                '_input'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  BINARY_ADD       
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            42  '42'

 L. 407        64  LOAD_FAST                'radius'
               66  LOAD_CONST               None
               68  COMPARE_OP               is
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 408        72  LOAD_GLOBAL              ValueError
               74  LOAD_STR                 'radius is None'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            70  '70'

 L. 410        80  BUILD_LIST_0          0 
               82  STORE_FAST               'radiuses'

 L. 411        84  LOAD_GLOBAL              isinstance
               86  LOAD_FAST                'radius'
               88  LOAD_GLOBAL              float
               90  LOAD_GLOBAL              int
               92  BUILD_TUPLE_2         2 
               94  CALL_FUNCTION_2       2  '2 positional arguments'
               96  POP_JUMP_IF_FALSE   114  'to 114'

 L. 412        98  LOAD_FAST                'radiuses'
              100  LOAD_METHOD              append
              102  LOAD_GLOBAL              float
              104  LOAD_FAST                'radius'
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  POP_TOP          
              112  JUMP_FORWARD        204  'to 204'
            114_0  COME_FROM            96  '96'

 L. 413       114  LOAD_GLOBAL              isinstance
              116  LOAD_FAST                'radius'
              118  LOAD_GLOBAL              list
              120  LOAD_GLOBAL              tuple
              122  BUILD_TUPLE_2         2 
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  POP_JUMP_IF_FALSE   158  'to 158'

 L. 414       128  SETUP_LOOP          204  'to 204'
              130  LOAD_FAST                'radius'
              132  GET_ITER         
              134  FOR_ITER            154  'to 154'
              136  STORE_FAST               'd'

 L. 415       138  LOAD_FAST                'radiuses'
              140  LOAD_METHOD              append
              142  LOAD_GLOBAL              float
              144  LOAD_FAST                'd'
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  CALL_METHOD_1         1  '1 positional argument'
              150  POP_TOP          
              152  JUMP_BACK           134  'to 134'
              154  POP_BLOCK        
              156  JUMP_FORWARD        204  'to 204'
            158_0  COME_FROM           126  '126'

 L. 416       158  LOAD_GLOBAL              isinstance
              160  LOAD_FAST                'radius'
              162  LOAD_GLOBAL              str
              164  CALL_FUNCTION_2       2  '2 positional arguments'
              166  POP_JUMP_IF_FALSE   204  'to 204'

 L. 417       168  LOAD_GLOBAL              split_input_list_from_str
              170  LOAD_FAST                'radius'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  STORE_FAST               'ds'

 L. 418       176  SETUP_LOOP          204  'to 204'
              178  LOAD_FAST                'ds'
              180  GET_ITER         
              182  FOR_ITER            202  'to 202'
              184  STORE_FAST               'd'

 L. 419       186  LOAD_FAST                'radiuses'
              188  LOAD_METHOD              append
              190  LOAD_GLOBAL              float
              192  LOAD_FAST                'd'
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  CALL_METHOD_1         1  '1 positional argument'
              198  POP_TOP          
              200  JUMP_BACK           182  'to 182'
              202  POP_BLOCK        
            204_0  COME_FROM_LOOP      176  '176'
            204_1  COME_FROM           166  '166'
            204_2  COME_FROM           156  '156'
            204_3  COME_FROM_LOOP      128  '128'
            204_4  COME_FROM           112  '112'

 L. 420       204  LOAD_GLOBAL              len
              206  LOAD_FAST                'radiuses'
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  LOAD_CONST               1
              212  COMPARE_OP               <
              214  POP_JUMP_IF_FALSE   224  'to 224'

 L. 421       216  LOAD_GLOBAL              ValueError
              218  LOAD_STR                 'radius have no valid value.'
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  RAISE_VARARGS_1       1  'exception instance'
            224_0  COME_FROM           214  '214'

 L. 423       224  LOAD_GLOBAL              get_jvm
              226  CALL_FUNCTION_0       0  '0 positional arguments'
              228  STORE_FAST               '_jvm'

 L. 424       230  LOAD_GLOBAL              BufferRadiusUnit
              232  LOAD_METHOD              _make
              234  LOAD_FAST                'unit'
              236  LOAD_GLOBAL              BufferRadiusUnit
              238  LOAD_ATTR                METER
              240  CALL_METHOD_2         2  '2 positional arguments'
              242  STORE_FAST               '_dist_unit'

 L. 426       244  LOAD_FAST                'out_data'
              246  LOAD_CONST               None
              248  COMPARE_OP               is-not
          250_252  POP_JUMP_IF_FALSE   268  'to 268'

 L. 427       254  LOAD_GLOBAL              get_output_datasource
              256  LOAD_FAST                'out_data'
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  STORE_FAST               'out_datasource'

 L. 428       262  LOAD_FAST                'out_datasource'
              264  STORE_FAST               '_ds'
              266  JUMP_FORWARD        274  'to 274'
            268_0  COME_FROM           250  '250'

 L. 430       268  LOAD_FAST                '_input'
              270  LOAD_ATTR                datasource
              272  STORE_FAST               '_ds'
            274_0  COME_FROM           266  '266'

 L. 431       274  LOAD_GLOBAL              check_output_datasource
              276  LOAD_FAST                '_ds'
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  POP_TOP          

 L. 432       282  LOAD_FAST                'out_dataset_name'
              284  LOAD_CONST               None
              286  COMPARE_OP               is
          288_290  POP_JUMP_IF_FALSE   298  'to 298'

 L. 433       292  LOAD_STR                 'buffer_result'
              294  STORE_FAST               '_outDatasetName'
              296  JUMP_FORWARD        302  'to 302'
            298_0  COME_FROM           288  '288'

 L. 435       298  LOAD_FAST                'out_dataset_name'
              300  STORE_FAST               '_outDatasetName'
            302_0  COME_FROM           296  '296'

 L. 436       302  LOAD_GLOBAL              create_result_datasaet
              304  LOAD_FAST                '_ds'
              306  LOAD_FAST                '_outDatasetName'
              308  LOAD_STR                 'REGION'
              310  CALL_FUNCTION_3       3  '3 positional arguments'
              312  STORE_FAST               'result_dt'

 L. 438       314  LOAD_GLOBAL              isinstance
              316  LOAD_FAST                '_input'
              318  LOAD_GLOBAL              DatasetVector
              320  CALL_FUNCTION_2       2  '2 positional arguments'
          322_324  POP_JUMP_IF_FALSE   340  'to 340'

 L. 439       326  LOAD_FAST                'result_dt'
              328  LOAD_METHOD              set_prj_coordsys
              330  LOAD_FAST                '_input'
              332  LOAD_ATTR                prj_coordsys
              334  CALL_METHOD_1         1  '1 positional argument'
              336  POP_TOP          
              338  JUMP_FORWARD        366  'to 366'
            340_0  COME_FROM           322  '322'

 L. 440       340  LOAD_GLOBAL              isinstance
              342  LOAD_FAST                '_input'
              344  LOAD_GLOBAL              Recordset
              346  CALL_FUNCTION_2       2  '2 positional arguments'
          348_350  POP_JUMP_IF_FALSE   366  'to 366'

 L. 441       352  LOAD_FAST                'result_dt'
              354  LOAD_METHOD              set_prj_coordsys
              356  LOAD_FAST                '_input'
              358  LOAD_ATTR                dataset
              360  LOAD_ATTR                prj_coordsys
              362  CALL_METHOD_1         1  '1 positional argument'
              364  POP_TOP          
            366_0  COME_FROM           348  '348'
            366_1  COME_FROM           338  '338'

 L. 443       366  LOAD_CONST               None
              368  STORE_FAST               'listener'

 L. 444       370  LOAD_FAST                'progress'
              372  LOAD_CONST               None
              374  COMPARE_OP               is-not
          376_378  POP_JUMP_IF_FALSE   478  'to 478'

 L. 445       380  LOAD_GLOBAL              safe_start_callback_server
              382  CALL_FUNCTION_0       0  '0 positional arguments'
          384_386  POP_JUMP_IF_FALSE   478  'to 478'

 L. 446       388  SETUP_EXCEPT        424  'to 424'

 L. 447       390  LOAD_GLOBAL              ProgressListener
              392  LOAD_FAST                'progress'
              394  LOAD_STR                 'create_line_one_side_multi_buffer'
              396  CALL_FUNCTION_2       2  '2 positional arguments'
              398  STORE_FAST               'listener'

 L. 448       400  LOAD_FAST                '_jvm'
              402  LOAD_ATTR                com
              404  LOAD_ATTR                supermap
              406  LOAD_ATTR                analyst
              408  LOAD_ATTR                spatialanalyst
              410  LOAD_ATTR                BufferAnalyst
              412  LOAD_METHOD              addSteppedListener
              414  LOAD_FAST                'listener'
              416  CALL_METHOD_1         1  '1 positional argument'
              418  POP_TOP          
              420  POP_BLOCK        
              422  JUMP_FORWARD        478  'to 478'
            424_0  COME_FROM_EXCEPT    388  '388'

 L. 449       424  DUP_TOP          
              426  LOAD_GLOBAL              Exception
              428  COMPARE_OP               exception-match
          430_432  POP_JUMP_IF_FALSE   476  'to 476'
              434  POP_TOP          
              436  STORE_FAST               'e'
              438  POP_TOP          
              440  SETUP_FINALLY       464  'to 464'

 L. 450       442  LOAD_GLOBAL              close_callback_server
              444  CALL_FUNCTION_0       0  '0 positional arguments'
              446  POP_TOP          

 L. 451       448  LOAD_GLOBAL              log_error
              450  LOAD_FAST                'e'
              452  CALL_FUNCTION_1       1  '1 positional argument'
              454  POP_TOP          

 L. 452       456  LOAD_CONST               None
              458  STORE_FAST               'listener'
              460  POP_BLOCK        
              462  LOAD_CONST               None
            464_0  COME_FROM_FINALLY   440  '440'
              464  LOAD_CONST               None
              466  STORE_FAST               'e'
              468  DELETE_FAST              'e'
              470  END_FINALLY      
              472  POP_EXCEPT       
              474  JUMP_FORWARD        478  'to 478'
            476_0  COME_FROM           430  '430'
              476  END_FINALLY      
            478_0  COME_FROM           474  '474'
            478_1  COME_FROM           422  '422'
            478_2  COME_FROM           384  '384'
            478_3  COME_FROM           376  '376'

 L. 454       478  SETUP_FINALLY       608  'to 608'
              480  SETUP_EXCEPT        556  'to 556'

 L. 455       482  LOAD_FAST                '_jvm'
              484  LOAD_ATTR                com
              486  LOAD_ATTR                supermap
              488  LOAD_ATTR                analyst
              490  LOAD_ATTR                spatialanalyst
              492  LOAD_ATTR                BufferAnalyst
              494  STORE_FAST               'buffer_func'

 L. 456       496  LOAD_FAST                'buffer_func'
              498  LOAD_METHOD              createLineOneSideMultiBuffer
              500  LOAD_FAST                '_input'
              502  LOAD_ATTR                _jobject

 L. 457       504  LOAD_FAST                'result_dt'
              506  LOAD_ATTR                _jobject

 L. 458       508  LOAD_GLOBAL              to_java_double_array
              510  LOAD_FAST                'radiuses'
              512  CALL_FUNCTION_1       1  '1 positional argument'

 L. 459       514  LOAD_FAST                '_dist_unit'
              516  LOAD_ATTR                _jobject

 L. 460       518  LOAD_GLOBAL              int
              520  LOAD_FAST                'segment'
              522  CALL_FUNCTION_1       1  '1 positional argument'

 L. 461       524  LOAD_GLOBAL              bool
              526  LOAD_FAST                'is_left'
              528  CALL_FUNCTION_1       1  '1 positional argument'

 L. 462       530  LOAD_GLOBAL              bool
              532  LOAD_FAST                'is_union_result'
              534  CALL_FUNCTION_1       1  '1 positional argument'

 L. 463       536  LOAD_GLOBAL              bool
              538  LOAD_FAST                'is_save_attributes'
              540  CALL_FUNCTION_1       1  '1 positional argument'

 L. 464       542  LOAD_GLOBAL              bool
              544  LOAD_FAST                'is_ring'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  CALL_METHOD_9         9  '9 positional arguments'
              550  STORE_FAST               'result'
              552  POP_BLOCK        
              554  JUMP_FORWARD        604  'to 604'
            556_0  COME_FROM_EXCEPT    480  '480'

 L. 465       556  DUP_TOP          
              558  LOAD_GLOBAL              Exception
              560  COMPARE_OP               exception-match
          562_564  POP_JUMP_IF_FALSE   602  'to 602'
              566  POP_TOP          
              568  STORE_FAST               'e'
              570  POP_TOP          
              572  SETUP_FINALLY       590  'to 590'

 L. 466       574  LOAD_GLOBAL              log_error
              576  LOAD_FAST                'e'
              578  CALL_FUNCTION_1       1  '1 positional argument'
              580  POP_TOP          

 L. 467       582  LOAD_CONST               False
              584  STORE_FAST               'result'
              586  POP_BLOCK        
              588  LOAD_CONST               None
            590_0  COME_FROM_FINALLY   572  '572'
              590  LOAD_CONST               None
              592  STORE_FAST               'e'
              594  DELETE_FAST              'e'
              596  END_FINALLY      
              598  POP_EXCEPT       
              600  JUMP_FORWARD        604  'to 604'
            602_0  COME_FROM           562  '562'
              602  END_FINALLY      
            604_0  COME_FROM           600  '600'
            604_1  COME_FROM           554  '554'
              604  POP_BLOCK        
              606  LOAD_CONST               None
            608_0  COME_FROM_FINALLY   478  '478'

 L. 469       608  LOAD_FAST                'listener'
              610  LOAD_CONST               None
              612  COMPARE_OP               is-not
          614_616  POP_JUMP_IF_FALSE   694  'to 694'

 L. 470       618  SETUP_EXCEPT        644  'to 644'

 L. 471       620  LOAD_FAST                '_jvm'
              622  LOAD_ATTR                com
              624  LOAD_ATTR                supermap
              626  LOAD_ATTR                analyst
              628  LOAD_ATTR                spatialanalyst
              630  LOAD_ATTR                BufferAnalyst
              632  LOAD_METHOD              removeSteppedListener
              634  LOAD_FAST                'listener'
              636  CALL_METHOD_1         1  '1 positional argument'
              638  POP_TOP          
              640  POP_BLOCK        
              642  JUMP_FORWARD        688  'to 688'
            644_0  COME_FROM_EXCEPT    618  '618'

 L. 472       644  DUP_TOP          
              646  LOAD_GLOBAL              Exception
              648  COMPARE_OP               exception-match
          650_652  POP_JUMP_IF_FALSE   686  'to 686'
              654  POP_TOP          
              656  STORE_FAST               'e1'
              658  POP_TOP          
              660  SETUP_FINALLY       674  'to 674'

 L. 473       662  LOAD_GLOBAL              log_error
              664  LOAD_FAST                'e1'
              666  CALL_FUNCTION_1       1  '1 positional argument'
              668  POP_TOP          
              670  POP_BLOCK        
              672  LOAD_CONST               None
            674_0  COME_FROM_FINALLY   660  '660'
              674  LOAD_CONST               None
              676  STORE_FAST               'e1'
              678  DELETE_FAST              'e1'
              680  END_FINALLY      
              682  POP_EXCEPT       
              684  JUMP_FORWARD        688  'to 688'
            686_0  COME_FROM           650  '650'
              686  END_FINALLY      
            688_0  COME_FROM           684  '684'
            688_1  COME_FROM           642  '642'

 L. 474       688  LOAD_GLOBAL              close_callback_server
              690  CALL_FUNCTION_0       0  '0 positional arguments'
              692  POP_TOP          
            694_0  COME_FROM           614  '614'

 L. 476       694  LOAD_FAST                'result'
          696_698  POP_JUMP_IF_TRUE    716  'to 716'

 L. 477       700  LOAD_FAST                'out_datasource'
              702  LOAD_METHOD              delete
              704  LOAD_FAST                'result_dt'
              706  LOAD_ATTR                name
              708  CALL_METHOD_1         1  '1 positional argument'
              710  POP_TOP          

 L. 478       712  LOAD_CONST               None
              714  STORE_FAST               'result_dt'
            716_0  COME_FROM           696  '696'

 L. 479       716  LOAD_FAST                'out_data'
              718  LOAD_CONST               None
              720  COMPARE_OP               is-not
          722_724  POP_JUMP_IF_FALSE   736  'to 736'

 L. 480       726  LOAD_GLOBAL              try_close_output_datasource
              728  LOAD_FAST                'result_dt'
              730  LOAD_FAST                'out_datasource'
              732  CALL_FUNCTION_2       2  '2 positional arguments'
              734  RETURN_VALUE     
            736_0  COME_FROM           722  '722'

 L. 482       736  LOAD_FAST                'result_dt'
              738  RETURN_VALUE     
              740  END_FINALLY      

Parse error at or near `COME_FROM_LOOP' instruction at offset 204_3


def create_multi_buffer--- This code section failed: ---

 L. 508         0  LOAD_GLOBAL              get_input_dataset
                2  LOAD_FAST                'input_data'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               '_input'

 L. 509         8  LOAD_FAST                '_input'
               10  LOAD_CONST               None
               12  COMPARE_OP               is
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 510        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'input_data is None'
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 511        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                '_input'
               28  LOAD_GLOBAL              DatasetVector
               30  LOAD_GLOBAL              Recordset
               32  BUILD_TUPLE_2         2 
               34  CALL_FUNCTION_2       2  '2 positional arguments'
               36  POP_JUMP_IF_TRUE     58  'to 58'

 L. 512        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'input_data required DatasetVector or Recordset, but now is '
               42  LOAD_GLOBAL              str
               44  LOAD_GLOBAL              type
               46  LOAD_FAST                '_input'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  BINARY_ADD       
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            36  '36'

 L. 513        58  LOAD_FAST                'radius'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 514        66  LOAD_GLOBAL              ValueError
               68  LOAD_STR                 'radius is None'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            64  '64'

 L. 516        74  BUILD_LIST_0          0 
               76  STORE_FAST               'radiuses'

 L. 517        78  LOAD_GLOBAL              isinstance
               80  LOAD_FAST                'radius'
               82  LOAD_GLOBAL              float
               84  LOAD_GLOBAL              int
               86  BUILD_TUPLE_2         2 
               88  CALL_FUNCTION_2       2  '2 positional arguments'
               90  POP_JUMP_IF_FALSE   108  'to 108'

 L. 518        92  LOAD_FAST                'radiuses'
               94  LOAD_METHOD              append
               96  LOAD_GLOBAL              float
               98  LOAD_FAST                'radius'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  CALL_METHOD_1         1  '1 positional argument'
              104  POP_TOP          
              106  JUMP_FORWARD        198  'to 198'
            108_0  COME_FROM            90  '90'

 L. 519       108  LOAD_GLOBAL              isinstance
              110  LOAD_FAST                'radius'
              112  LOAD_GLOBAL              list
              114  LOAD_GLOBAL              tuple
              116  BUILD_TUPLE_2         2 
              118  CALL_FUNCTION_2       2  '2 positional arguments'
              120  POP_JUMP_IF_FALSE   152  'to 152'

 L. 520       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                'radius'
              126  GET_ITER         
              128  FOR_ITER            148  'to 148'
              130  STORE_FAST               'd'

 L. 521       132  LOAD_FAST                'radiuses'
              134  LOAD_METHOD              append
              136  LOAD_GLOBAL              float
              138  LOAD_FAST                'd'
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  POP_TOP          
              146  JUMP_BACK           128  'to 128'
              148  POP_BLOCK        
              150  JUMP_FORWARD        198  'to 198'
            152_0  COME_FROM           120  '120'

 L. 522       152  LOAD_GLOBAL              isinstance
              154  LOAD_FAST                'radius'
              156  LOAD_GLOBAL              str
              158  CALL_FUNCTION_2       2  '2 positional arguments'
              160  POP_JUMP_IF_FALSE   198  'to 198'

 L. 523       162  LOAD_GLOBAL              split_input_list_from_str
              164  LOAD_FAST                'radius'
              166  CALL_FUNCTION_1       1  '1 positional argument'
              168  STORE_FAST               'ds'

 L. 524       170  SETUP_LOOP          198  'to 198'
              172  LOAD_FAST                'ds'
              174  GET_ITER         
              176  FOR_ITER            196  'to 196'
              178  STORE_FAST               'd'

 L. 525       180  LOAD_FAST                'radiuses'
              182  LOAD_METHOD              append
              184  LOAD_GLOBAL              float
              186  LOAD_FAST                'd'
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  CALL_METHOD_1         1  '1 positional argument'
              192  POP_TOP          
              194  JUMP_BACK           176  'to 176'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      170  '170'
            198_1  COME_FROM           160  '160'
            198_2  COME_FROM           150  '150'
            198_3  COME_FROM_LOOP      122  '122'
            198_4  COME_FROM           106  '106'

 L. 526       198  LOAD_GLOBAL              len
              200  LOAD_FAST                'radiuses'
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  LOAD_CONST               1
              206  COMPARE_OP               <
              208  POP_JUMP_IF_FALSE   218  'to 218'

 L. 527       210  LOAD_GLOBAL              ValueError
              212  LOAD_STR                 'radius have no valid value.'
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  RAISE_VARARGS_1       1  'exception instance'
            218_0  COME_FROM           208  '208'

 L. 529       218  LOAD_GLOBAL              get_jvm
              220  CALL_FUNCTION_0       0  '0 positional arguments'
              222  STORE_FAST               '_jvm'

 L. 530       224  LOAD_GLOBAL              BufferRadiusUnit
              226  LOAD_METHOD              _make
              228  LOAD_FAST                'unit'
              230  LOAD_GLOBAL              BufferRadiusUnit
              232  LOAD_ATTR                METER
              234  CALL_METHOD_2         2  '2 positional arguments'
              236  STORE_FAST               '_dist_unit'

 L. 532       238  LOAD_FAST                'out_data'
              240  LOAD_CONST               None
              242  COMPARE_OP               is-not
          244_246  POP_JUMP_IF_FALSE   262  'to 262'

 L. 533       248  LOAD_GLOBAL              get_output_datasource
              250  LOAD_FAST                'out_data'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  STORE_FAST               'out_datasource'

 L. 534       256  LOAD_FAST                'out_datasource'
              258  STORE_FAST               '_ds'
              260  JUMP_FORWARD        268  'to 268'
            262_0  COME_FROM           244  '244'

 L. 536       262  LOAD_FAST                '_input'
              264  LOAD_ATTR                datasource
              266  STORE_FAST               '_ds'
            268_0  COME_FROM           260  '260'

 L. 537       268  LOAD_GLOBAL              check_output_datasource
              270  LOAD_FAST                '_ds'
              272  CALL_FUNCTION_1       1  '1 positional argument'
              274  POP_TOP          

 L. 538       276  LOAD_FAST                'out_dataset_name'
              278  LOAD_CONST               None
              280  COMPARE_OP               is
          282_284  POP_JUMP_IF_FALSE   292  'to 292'

 L. 539       286  LOAD_STR                 'buffer_result'
              288  STORE_FAST               '_outDatasetName'
              290  JUMP_FORWARD        296  'to 296'
            292_0  COME_FROM           282  '282'

 L. 541       292  LOAD_FAST                'out_dataset_name'
              294  STORE_FAST               '_outDatasetName'
            296_0  COME_FROM           290  '290'

 L. 542       296  LOAD_GLOBAL              create_result_datasaet
              298  LOAD_FAST                '_ds'
              300  LOAD_FAST                '_outDatasetName'
              302  LOAD_STR                 'REGION'
              304  CALL_FUNCTION_3       3  '3 positional arguments'
              306  STORE_FAST               'result_dt'

 L. 544       308  LOAD_GLOBAL              isinstance
              310  LOAD_FAST                '_input'
              312  LOAD_GLOBAL              DatasetVector
              314  CALL_FUNCTION_2       2  '2 positional arguments'
          316_318  POP_JUMP_IF_FALSE   334  'to 334'

 L. 545       320  LOAD_FAST                'result_dt'
              322  LOAD_METHOD              set_prj_coordsys
              324  LOAD_FAST                '_input'
              326  LOAD_ATTR                prj_coordsys
              328  CALL_METHOD_1         1  '1 positional argument'
              330  POP_TOP          
              332  JUMP_FORWARD        360  'to 360'
            334_0  COME_FROM           316  '316'

 L. 546       334  LOAD_GLOBAL              isinstance
              336  LOAD_FAST                '_input'
              338  LOAD_GLOBAL              Recordset
              340  CALL_FUNCTION_2       2  '2 positional arguments'
          342_344  POP_JUMP_IF_FALSE   360  'to 360'

 L. 547       346  LOAD_FAST                'result_dt'
              348  LOAD_METHOD              set_prj_coordsys
              350  LOAD_FAST                '_input'
              352  LOAD_ATTR                dataset
              354  LOAD_ATTR                prj_coordsys
              356  CALL_METHOD_1         1  '1 positional argument'
              358  POP_TOP          
            360_0  COME_FROM           342  '342'
            360_1  COME_FROM           332  '332'

 L. 549       360  LOAD_CONST               None
              362  STORE_FAST               'listener'

 L. 550       364  LOAD_FAST                'progress'
              366  LOAD_CONST               None
              368  COMPARE_OP               is-not
          370_372  POP_JUMP_IF_FALSE   472  'to 472'

 L. 551       374  LOAD_GLOBAL              safe_start_callback_server
              376  CALL_FUNCTION_0       0  '0 positional arguments'
          378_380  POP_JUMP_IF_FALSE   472  'to 472'

 L. 552       382  SETUP_EXCEPT        418  'to 418'

 L. 553       384  LOAD_GLOBAL              ProgressListener
              386  LOAD_FAST                'progress'
              388  LOAD_STR                 'create_multi_buffer'
              390  CALL_FUNCTION_2       2  '2 positional arguments'
              392  STORE_FAST               'listener'

 L. 554       394  LOAD_FAST                '_jvm'
              396  LOAD_ATTR                com
              398  LOAD_ATTR                supermap
              400  LOAD_ATTR                analyst
              402  LOAD_ATTR                spatialanalyst
              404  LOAD_ATTR                BufferAnalyst
              406  LOAD_METHOD              addSteppedListener
              408  LOAD_FAST                'listener'
              410  CALL_METHOD_1         1  '1 positional argument'
              412  POP_TOP          
              414  POP_BLOCK        
              416  JUMP_FORWARD        472  'to 472'
            418_0  COME_FROM_EXCEPT    382  '382'

 L. 555       418  DUP_TOP          
              420  LOAD_GLOBAL              Exception
              422  COMPARE_OP               exception-match
          424_426  POP_JUMP_IF_FALSE   470  'to 470'
              428  POP_TOP          
              430  STORE_FAST               'e'
              432  POP_TOP          
              434  SETUP_FINALLY       458  'to 458'

 L. 556       436  LOAD_GLOBAL              close_callback_server
              438  CALL_FUNCTION_0       0  '0 positional arguments'
              440  POP_TOP          

 L. 557       442  LOAD_GLOBAL              log_error
              444  LOAD_FAST                'e'
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  POP_TOP          

 L. 558       450  LOAD_CONST               None
              452  STORE_FAST               'listener'
              454  POP_BLOCK        
              456  LOAD_CONST               None
            458_0  COME_FROM_FINALLY   434  '434'
              458  LOAD_CONST               None
              460  STORE_FAST               'e'
              462  DELETE_FAST              'e'
              464  END_FINALLY      
              466  POP_EXCEPT       
              468  JUMP_FORWARD        472  'to 472'
            470_0  COME_FROM           424  '424'
              470  END_FINALLY      
            472_0  COME_FROM           468  '468'
            472_1  COME_FROM           416  '416'
            472_2  COME_FROM           378  '378'
            472_3  COME_FROM           370  '370'

 L. 560       472  SETUP_FINALLY       596  'to 596'
              474  SETUP_EXCEPT        544  'to 544'

 L. 561       476  LOAD_FAST                '_jvm'
              478  LOAD_ATTR                com
              480  LOAD_ATTR                supermap
              482  LOAD_ATTR                analyst
              484  LOAD_ATTR                spatialanalyst
              486  LOAD_ATTR                BufferAnalyst
              488  STORE_FAST               'buffer_func'

 L. 562       490  LOAD_FAST                'buffer_func'
              492  LOAD_METHOD              createMultiBuffer
              494  LOAD_FAST                '_input'
              496  LOAD_ATTR                _jobject

 L. 563       498  LOAD_FAST                'result_dt'
              500  LOAD_ATTR                _jobject

 L. 564       502  LOAD_GLOBAL              to_java_double_array
              504  LOAD_FAST                'radiuses'
              506  CALL_FUNCTION_1       1  '1 positional argument'

 L. 565       508  LOAD_FAST                '_dist_unit'
              510  LOAD_ATTR                _jobject

 L. 566       512  LOAD_GLOBAL              int
              514  LOAD_FAST                'segment'
              516  CALL_FUNCTION_1       1  '1 positional argument'

 L. 567       518  LOAD_GLOBAL              bool
              520  LOAD_FAST                'is_union_result'
              522  CALL_FUNCTION_1       1  '1 positional argument'

 L. 568       524  LOAD_GLOBAL              bool
              526  LOAD_FAST                'is_save_attributes'
              528  CALL_FUNCTION_1       1  '1 positional argument'

 L. 569       530  LOAD_GLOBAL              bool
              532  LOAD_FAST                'is_ring'
              534  CALL_FUNCTION_1       1  '1 positional argument'
              536  CALL_METHOD_8         8  '8 positional arguments'
              538  STORE_FAST               'result'
              540  POP_BLOCK        
              542  JUMP_FORWARD        592  'to 592'
            544_0  COME_FROM_EXCEPT    474  '474'

 L. 570       544  DUP_TOP          
              546  LOAD_GLOBAL              Exception
              548  COMPARE_OP               exception-match
          550_552  POP_JUMP_IF_FALSE   590  'to 590'
              554  POP_TOP          
              556  STORE_FAST               'e'
              558  POP_TOP          
              560  SETUP_FINALLY       578  'to 578'

 L. 571       562  LOAD_GLOBAL              log_error
              564  LOAD_FAST                'e'
              566  CALL_FUNCTION_1       1  '1 positional argument'
              568  POP_TOP          

 L. 572       570  LOAD_CONST               False
              572  STORE_FAST               'result'
              574  POP_BLOCK        
              576  LOAD_CONST               None
            578_0  COME_FROM_FINALLY   560  '560'
              578  LOAD_CONST               None
              580  STORE_FAST               'e'
              582  DELETE_FAST              'e'
              584  END_FINALLY      
              586  POP_EXCEPT       
              588  JUMP_FORWARD        592  'to 592'
            590_0  COME_FROM           550  '550'
              590  END_FINALLY      
            592_0  COME_FROM           588  '588'
            592_1  COME_FROM           542  '542'
              592  POP_BLOCK        
              594  LOAD_CONST               None
            596_0  COME_FROM_FINALLY   472  '472'

 L. 574       596  LOAD_FAST                'listener'
              598  LOAD_CONST               None
              600  COMPARE_OP               is-not
          602_604  POP_JUMP_IF_FALSE   682  'to 682'

 L. 575       606  SETUP_EXCEPT        632  'to 632'

 L. 576       608  LOAD_FAST                '_jvm'
              610  LOAD_ATTR                com
              612  LOAD_ATTR                supermap
              614  LOAD_ATTR                analyst
              616  LOAD_ATTR                spatialanalyst
              618  LOAD_ATTR                BufferAnalyst
              620  LOAD_METHOD              removeSteppedListener
              622  LOAD_FAST                'listener'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  POP_TOP          
              628  POP_BLOCK        
              630  JUMP_FORWARD        676  'to 676'
            632_0  COME_FROM_EXCEPT    606  '606'

 L. 577       632  DUP_TOP          
              634  LOAD_GLOBAL              Exception
              636  COMPARE_OP               exception-match
          638_640  POP_JUMP_IF_FALSE   674  'to 674'
              642  POP_TOP          
              644  STORE_FAST               'e1'
              646  POP_TOP          
              648  SETUP_FINALLY       662  'to 662'

 L. 578       650  LOAD_GLOBAL              log_error
              652  LOAD_FAST                'e1'
              654  CALL_FUNCTION_1       1  '1 positional argument'
              656  POP_TOP          
              658  POP_BLOCK        
              660  LOAD_CONST               None
            662_0  COME_FROM_FINALLY   648  '648'
              662  LOAD_CONST               None
              664  STORE_FAST               'e1'
              666  DELETE_FAST              'e1'
              668  END_FINALLY      
              670  POP_EXCEPT       
              672  JUMP_FORWARD        676  'to 676'
            674_0  COME_FROM           638  '638'
              674  END_FINALLY      
            676_0  COME_FROM           672  '672'
            676_1  COME_FROM           630  '630'

 L. 579       676  LOAD_GLOBAL              close_callback_server
              678  CALL_FUNCTION_0       0  '0 positional arguments'
              680  POP_TOP          
            682_0  COME_FROM           602  '602'

 L. 581       682  LOAD_FAST                'result'
          684_686  POP_JUMP_IF_TRUE    704  'to 704'

 L. 582       688  LOAD_FAST                'out_datasource'
              690  LOAD_METHOD              delete
              692  LOAD_FAST                'result_dt'
              694  LOAD_ATTR                name
              696  CALL_METHOD_1         1  '1 positional argument'
              698  POP_TOP          

 L. 583       700  LOAD_CONST               None
              702  STORE_FAST               'result_dt'
            704_0  COME_FROM           684  '684'

 L. 584       704  LOAD_FAST                'out_data'
              706  LOAD_CONST               None
              708  COMPARE_OP               is-not
          710_712  POP_JUMP_IF_FALSE   724  'to 724'

 L. 585       714  LOAD_GLOBAL              try_close_output_datasource
              716  LOAD_FAST                'result_dt'
              718  LOAD_FAST                'out_datasource'
              720  CALL_FUNCTION_2       2  '2 positional arguments'
              722  RETURN_VALUE     
            724_0  COME_FROM           710  '710'

 L. 587       724  LOAD_FAST                'result_dt'
              726  RETURN_VALUE     
              728  END_FINALLY      

Parse error at or near `COME_FROM_LOOP' instruction at offset 198_3


def overlay--- This code section failed: ---

 L. 631         0  LOAD_GLOBAL              check_lic
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  POP_TOP          

 L. 632         6  LOAD_GLOBAL              get_input_dataset
                8  LOAD_FAST                'source_input'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  STORE_FAST               '_source_input'

 L. 633        14  LOAD_GLOBAL              get_input_dataset
               16  LOAD_FAST                'overlay_input'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  STORE_FAST               '_overlay_input'

 L. 634        22  LOAD_FAST                '_source_input'
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 635        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'source input_data is None'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 636        38  LOAD_FAST                '_overlay_input'
               40  LOAD_CONST               None
               42  COMPARE_OP               is
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 637        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'overlay input_data is None'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L. 639        54  LOAD_GLOBAL              isinstance
               56  LOAD_FAST                '_source_input'
               58  LOAD_GLOBAL              DatasetVector
               60  LOAD_GLOBAL              Recordset
               62  LOAD_GLOBAL              list
               64  LOAD_GLOBAL              tuple
               66  BUILD_TUPLE_4         4 
               68  CALL_FUNCTION_2       2  '2 positional arguments'
               70  POP_JUMP_IF_TRUE     92  'to 92'

 L. 640        72  LOAD_GLOBAL              ValueError

 L. 641        74  LOAD_STR                 'source_input required DatasetVector, Recordset, list, tuple, but now is : '
               76  LOAD_GLOBAL              str
               78  LOAD_GLOBAL              type
               80  LOAD_FAST                '_source_input'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  BINARY_ADD       
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            70  '70'

 L. 642        92  LOAD_GLOBAL              isinstance
               94  LOAD_FAST                '_overlay_input'
               96  LOAD_GLOBAL              DatasetVector
               98  LOAD_GLOBAL              Recordset
              100  LOAD_GLOBAL              list
              102  LOAD_GLOBAL              tuple
              104  BUILD_TUPLE_4         4 
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  POP_JUMP_IF_TRUE    130  'to 130'

 L. 643       110  LOAD_GLOBAL              ValueError

 L. 644       112  LOAD_STR                 'overlay_input required DatasetVector, Recordset, list, tuple, but now is : '
              114  LOAD_GLOBAL              str
              116  LOAD_GLOBAL              type
              118  LOAD_FAST                '_overlay_input'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  BINARY_ADD       
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           108  '108'

 L. 645       130  LOAD_GLOBAL              isinstance
              132  LOAD_FAST                '_source_input'
              134  LOAD_GLOBAL              list
              136  CALL_FUNCTION_2       2  '2 positional arguments'
              138  POP_JUMP_IF_FALSE   158  'to 158'

 L. 646       140  LOAD_GLOBAL              list
              142  LOAD_GLOBAL              filter
              144  LOAD_LAMBDA              '<code_object <lambda>>'
              146  LOAD_STR                 'overlay.<locals>.<lambda>'
              148  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              150  LOAD_FAST                '_source_input'
              152  CALL_FUNCTION_2       2  '2 positional arguments'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  STORE_FAST               '_source_input'
            158_0  COME_FROM           138  '138'

 L. 647       158  LOAD_GLOBAL              isinstance
              160  LOAD_FAST                '_overlay_input'
              162  LOAD_GLOBAL              list
              164  CALL_FUNCTION_2       2  '2 positional arguments'
              166  POP_JUMP_IF_FALSE   186  'to 186'

 L. 648       168  LOAD_GLOBAL              list
              170  LOAD_GLOBAL              filter
              172  LOAD_LAMBDA              '<code_object <lambda>>'
              174  LOAD_STR                 'overlay.<locals>.<lambda>'
              176  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              178  LOAD_FAST                '_overlay_input'
              180  CALL_FUNCTION_2       2  '2 positional arguments'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  STORE_FAST               '_overlay_input'
            186_0  COME_FROM           166  '166'

 L. 650       186  LOAD_GLOBAL              OverlayMode
              188  LOAD_METHOD              _make
              190  LOAD_FAST                'overlay_mode'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  STORE_FAST               '_overlayMode'

 L. 651       196  LOAD_GLOBAL              get_jvm
              198  CALL_FUNCTION_0       0  '0 positional arguments'
              200  STORE_FAST               '_jvm'

 L. 653       202  LOAD_FAST                'out_data'
              204  LOAD_CONST               None
              206  COMPARE_OP               is-not
              208  POP_JUMP_IF_FALSE   224  'to 224'

 L. 654       210  LOAD_GLOBAL              get_output_datasource
              212  LOAD_FAST                'out_data'
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  STORE_FAST               'out_datasource'

 L. 655       218  LOAD_FAST                'out_datasource'
              220  STORE_FAST               '_ds'
              222  JUMP_FORWARD        278  'to 278'
            224_0  COME_FROM           208  '208'

 L. 657       224  LOAD_GLOBAL              hasattr
              226  LOAD_FAST                '_source_input'
              228  LOAD_STR                 'datasource'
              230  CALL_FUNCTION_2       2  '2 positional arguments'
              232  POP_JUMP_IF_FALSE   246  'to 246'

 L. 658       234  LOAD_GLOBAL              getattr
              236  LOAD_FAST                '_source_input'
              238  LOAD_STR                 'datasource'
              240  CALL_FUNCTION_2       2  '2 positional arguments'
              242  STORE_FAST               '_ds'
              244  JUMP_FORWARD        278  'to 278'
            246_0  COME_FROM           232  '232'

 L. 659       246  LOAD_GLOBAL              hasattr
              248  LOAD_FAST                '_overlay_input'
              250  LOAD_STR                 'datasource'
              252  CALL_FUNCTION_2       2  '2 positional arguments'
          254_256  POP_JUMP_IF_FALSE   270  'to 270'

 L. 660       258  LOAD_GLOBAL              getattr
              260  LOAD_FAST                '_overlay_input'
              262  LOAD_STR                 'datasource'
              264  CALL_FUNCTION_2       2  '2 positional arguments'
              266  STORE_FAST               '_ds'
              268  JUMP_FORWARD        278  'to 278'
            270_0  COME_FROM           254  '254'

 L. 662       270  LOAD_GLOBAL              ValueError
              272  LOAD_STR                 'must set valid out_datasource datasource'
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  RAISE_VARARGS_1       1  'exception instance'
            278_0  COME_FROM           268  '268'
            278_1  COME_FROM           244  '244'
            278_2  COME_FROM           222  '222'

 L. 663       278  LOAD_GLOBAL              check_output_datasource
              280  LOAD_FAST                '_ds'
              282  CALL_FUNCTION_1       1  '1 positional argument'
              284  POP_TOP          

 L. 664       286  LOAD_FAST                'out_dataset_name'
              288  LOAD_CONST               None
              290  COMPARE_OP               is
          292_294  POP_JUMP_IF_FALSE   314  'to 314'

 L. 665       296  LOAD_GLOBAL              OverlayMode
              298  LOAD_METHOD              _make
              300  LOAD_FAST                'overlay_mode'
              302  CALL_METHOD_1         1  '1 positional argument'
              304  LOAD_ATTR                name
              306  LOAD_STR                 '_output'
              308  BINARY_ADD       
              310  STORE_FAST               '_outDatasetName'
              312  JUMP_FORWARD        318  'to 318'
            314_0  COME_FROM           292  '292'

 L. 667       314  LOAD_FAST                'out_dataset_name'
              316  STORE_FAST               '_outDatasetName'
            318_0  COME_FROM           312  '312'

 L. 669       318  LOAD_CONST               None
              320  STORE_FAST               'geo_type'

 L. 670       322  LOAD_GLOBAL              isinstance
              324  LOAD_FAST                '_source_input'
              326  LOAD_GLOBAL              DatasetVector
              328  CALL_FUNCTION_2       2  '2 positional arguments'
          330_332  POP_JUMP_IF_FALSE   342  'to 342'

 L. 671       334  LOAD_FAST                '_source_input'
              336  LOAD_ATTR                type
              338  STORE_FAST               'result_dt_type'
              340  JUMP_FORWARD        448  'to 448'
            342_0  COME_FROM           330  '330'

 L. 672       342  LOAD_GLOBAL              isinstance
              344  LOAD_FAST                '_source_input'
              346  LOAD_GLOBAL              Recordset
              348  CALL_FUNCTION_2       2  '2 positional arguments'
          350_352  POP_JUMP_IF_FALSE   364  'to 364'

 L. 673       354  LOAD_FAST                '_source_input'
              356  LOAD_ATTR                dataset
              358  LOAD_ATTR                type
              360  STORE_FAST               'result_dt_type'
              362  JUMP_FORWARD        448  'to 448'
            364_0  COME_FROM           350  '350'

 L. 675       364  LOAD_FAST                '_source_input'
              366  LOAD_CONST               0
              368  BINARY_SUBSCR    
              370  LOAD_ATTR                type
              372  STORE_FAST               'geo_type'

 L. 676       374  LOAD_FAST                'geo_type'
              376  LOAD_GLOBAL              GeometryType
              378  LOAD_ATTR                GEOPOINT
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   394  'to 394'

 L. 677       386  LOAD_GLOBAL              DatasetType
              388  LOAD_ATTR                POINT
              390  STORE_FAST               'result_dt_type'
              392  JUMP_FORWARD        448  'to 448'
            394_0  COME_FROM           382  '382'

 L. 678       394  LOAD_FAST                'geo_type'
              396  LOAD_GLOBAL              GeometryType
              398  LOAD_ATTR                GEOLINE
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   414  'to 414'

 L. 679       406  LOAD_GLOBAL              DatasetType
              408  LOAD_ATTR                LINE
              410  STORE_FAST               'result_dt_type'
              412  JUMP_FORWARD        448  'to 448'
            414_0  COME_FROM           402  '402'

 L. 680       414  LOAD_FAST                'geo_type'
              416  LOAD_GLOBAL              GeometryType
              418  LOAD_ATTR                GEOREGION
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   434  'to 434'

 L. 681       426  LOAD_GLOBAL              DatasetType
              428  LOAD_ATTR                REGION
              430  STORE_FAST               'result_dt_type'
              432  JUMP_FORWARD        448  'to 448'
            434_0  COME_FROM           422  '422'

 L. 683       434  LOAD_GLOBAL              ValueError
              436  LOAD_STR                 'invalid geometry type : '
              438  LOAD_FAST                'geo_type'
              440  LOAD_ATTR                name
              442  BINARY_ADD       
              444  CALL_FUNCTION_1       1  '1 positional argument'
              446  RAISE_VARARGS_1       1  'exception instance'
            448_0  COME_FROM           432  '432'
            448_1  COME_FROM           412  '412'
            448_2  COME_FROM           392  '392'
            448_3  COME_FROM           362  '362'
            448_4  COME_FROM           340  '340'

 L. 685       448  LOAD_FAST                'geo_type'
              450  LOAD_GLOBAL              GeometryType
              452  LOAD_ATTR                GEOREGION
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   510  'to 510'

 L. 686       460  LOAD_GLOBAL              isinstance
              462  LOAD_FAST                '_overlay_input'
              464  LOAD_GLOBAL              list
              466  CALL_FUNCTION_2       2  '2 positional arguments'
          468_470  POP_JUMP_IF_FALSE   510  'to 510'
              472  LOAD_FAST                '_overlay_input'
              474  LOAD_CONST               0
              476  BINARY_SUBSCR    
              478  LOAD_ATTR                type
              480  LOAD_GLOBAL              GeometryType
              482  LOAD_ATTR                GEOREGION
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   510  'to 510'

 L. 687       490  LOAD_GLOBAL              _overlay_geometrys
              492  LOAD_FAST                '_source_input'
              494  LOAD_FAST                '_overlay_input'
              496  LOAD_FAST                'overlay_mode'
              498  LOAD_FAST                '_ds'
              500  LOAD_FAST                '_outDatasetName'
              502  LOAD_FAST                'tolerance'

 L. 688       504  LOAD_FAST                'progress'
              506  CALL_FUNCTION_7       7  '7 positional arguments'
              508  RETURN_VALUE     
            510_0  COME_FROM           486  '486'
            510_1  COME_FROM           468  '468'
            510_2  COME_FROM           456  '456'

 L. 690       510  LOAD_GLOBAL              create_result_datasaet
              512  LOAD_FAST                '_ds'
              514  LOAD_FAST                '_outDatasetName'
              516  LOAD_FAST                'result_dt_type'
              518  CALL_FUNCTION_3       3  '3 positional arguments'
              520  STORE_FAST               'result_dt'

 L. 691       522  LOAD_GLOBAL              isinstance
              524  LOAD_FAST                '_source_input'
              526  LOAD_GLOBAL              DatasetVector
              528  CALL_FUNCTION_2       2  '2 positional arguments'
          530_532  POP_JUMP_IF_FALSE   548  'to 548'

 L. 692       534  LOAD_FAST                'result_dt'
              536  LOAD_METHOD              set_prj_coordsys
              538  LOAD_FAST                '_source_input'
              540  LOAD_ATTR                prj_coordsys
              542  CALL_METHOD_1         1  '1 positional argument'
              544  POP_TOP          
              546  JUMP_FORWARD        628  'to 628'
            548_0  COME_FROM           530  '530'

 L. 693       548  LOAD_GLOBAL              isinstance
              550  LOAD_FAST                '_source_input'
              552  LOAD_GLOBAL              Recordset
              554  CALL_FUNCTION_2       2  '2 positional arguments'
          556_558  POP_JUMP_IF_FALSE   576  'to 576'

 L. 694       560  LOAD_FAST                'result_dt'
              562  LOAD_METHOD              set_prj_coordsys
              564  LOAD_FAST                '_source_input'
              566  LOAD_ATTR                dataset
              568  LOAD_ATTR                prj_coordsys
              570  CALL_METHOD_1         1  '1 positional argument'
              572  POP_TOP          
              574  JUMP_FORWARD        628  'to 628'
            576_0  COME_FROM           556  '556'

 L. 695       576  LOAD_GLOBAL              isinstance
              578  LOAD_FAST                '_overlay_input'
              580  LOAD_GLOBAL              DatasetVector
              582  CALL_FUNCTION_2       2  '2 positional arguments'
          584_586  POP_JUMP_IF_FALSE   602  'to 602'

 L. 696       588  LOAD_FAST                'result_dt'
              590  LOAD_METHOD              set_prj_coordsys
              592  LOAD_FAST                '_overlay_input'
              594  LOAD_ATTR                prj_coordsys
              596  CALL_METHOD_1         1  '1 positional argument'
              598  POP_TOP          
              600  JUMP_FORWARD        628  'to 628'
            602_0  COME_FROM           584  '584'

 L. 697       602  LOAD_GLOBAL              isinstance
              604  LOAD_FAST                '_overlay_input'
              606  LOAD_GLOBAL              Recordset
              608  CALL_FUNCTION_2       2  '2 positional arguments'
          610_612  POP_JUMP_IF_FALSE   628  'to 628'

 L. 698       614  LOAD_FAST                'result_dt'
              616  LOAD_METHOD              set_prj_coordsys
              618  LOAD_FAST                '_overlay_input'
              620  LOAD_ATTR                dataset
              622  LOAD_ATTR                prj_coordsys
              624  CALL_METHOD_1         1  '1 positional argument'
              626  POP_TOP          
            628_0  COME_FROM           610  '610'
            628_1  COME_FROM           600  '600'
            628_2  COME_FROM           574  '574'
            628_3  COME_FROM           546  '546'

 L. 700       628  LOAD_CONST               None
              630  STORE_FAST               'temp_ds'

 L. 701       632  LOAD_CONST               None
              634  STORE_FAST               'listener'

 L. 702       636  LOAD_CONST               None
              638  STORE_FAST               'source_recordset'

 L. 703       640  LOAD_CONST               None
              642  STORE_FAST               'overlay_recordset'

 L. 704       644  LOAD_CONST               None
              646  STORE_FAST               'java_source'

 L. 705       648  LOAD_CONST               None
              650  STORE_FAST               'java_overlay'

 L. 706       652  LOAD_GLOBAL              oj
              654  LOAD_FAST                'result_dt'
              656  CALL_FUNCTION_1       1  '1 positional argument'
              658  STORE_FAST               'java_result_dt'

 L. 707   660_662  SETUP_FINALLY      1448  'to 1448'
          664_666  SETUP_EXCEPT       1384  'to 1384'

 L. 708       668  LOAD_GLOBAL              isinstance
              670  LOAD_FAST                '_source_input'
              672  LOAD_GLOBAL              DatasetVector
              674  CALL_FUNCTION_2       2  '2 positional arguments'
          676_678  POP_JUMP_IF_FALSE   758  'to 758'

 L. 709       680  LOAD_GLOBAL              isinstance
              682  LOAD_FAST                '_overlay_input'
              684  LOAD_GLOBAL              DatasetVector
              686  CALL_FUNCTION_2       2  '2 positional arguments'
          688_690  POP_JUMP_IF_FALSE   706  'to 706'

 L. 710       692  LOAD_FAST                '_source_input'
              694  LOAD_ATTR                _jobject
              696  STORE_FAST               'java_source'

 L. 711       698  LOAD_FAST                '_overlay_input'
              700  LOAD_ATTR                _jobject
              702  STORE_FAST               'java_overlay'
              704  JUMP_FORWARD       1042  'to 1042'
            706_0  COME_FROM           688  '688'

 L. 712       706  LOAD_GLOBAL              isinstance
              708  LOAD_FAST                '_overlay_input'
              710  LOAD_GLOBAL              Recordset
              712  CALL_FUNCTION_2       2  '2 positional arguments'
          714_716  POP_JUMP_IF_FALSE   740  'to 740'

 L. 713       718  LOAD_FAST                '_source_input'
              720  LOAD_METHOD              get_recordset
              722  CALL_METHOD_0         0  '0 positional arguments'
              724  STORE_FAST               'source_recordset'

 L. 714       726  LOAD_FAST                'source_recordset'
              728  LOAD_ATTR                _jobject
              730  STORE_FAST               'java_source'

 L. 715       732  LOAD_FAST                '_overlay_input'
              734  LOAD_ATTR                _jobject
              736  STORE_FAST               'java_overlay'
              738  JUMP_FORWARD       1042  'to 1042'
            740_0  COME_FROM           714  '714'

 L. 717       740  LOAD_FAST                '_source_input'
              742  LOAD_ATTR                _jobject
              744  STORE_FAST               'java_source'

 L. 718       746  LOAD_GLOBAL              to_java_geometry_array
              748  LOAD_FAST                '_overlay_input'
              750  CALL_FUNCTION_1       1  '1 positional argument'
              752  STORE_FAST               'java_overlay'
          754_756  JUMP_FORWARD       1042  'to 1042'
            758_0  COME_FROM           676  '676'

 L. 719       758  LOAD_GLOBAL              isinstance
              760  LOAD_FAST                '_source_input'
              762  LOAD_GLOBAL              Recordset
              764  CALL_FUNCTION_2       2  '2 positional arguments'
          766_768  POP_JUMP_IF_FALSE   882  'to 882'

 L. 720       770  LOAD_GLOBAL              isinstance
              772  LOAD_FAST                '_overlay_input'
              774  LOAD_GLOBAL              DatasetVector
              776  CALL_FUNCTION_2       2  '2 positional arguments'
          778_780  POP_JUMP_IF_FALSE   804  'to 804'

 L. 721       782  LOAD_FAST                '_source_input'
              784  LOAD_ATTR                _jobject
              786  STORE_FAST               'java_source'

 L. 722       788  LOAD_FAST                '_overlay_input'
              790  LOAD_METHOD              get_recordset
              792  CALL_METHOD_0         0  '0 positional arguments'
              794  STORE_FAST               'overlay_recordset'

 L. 723       796  LOAD_FAST                'overlay_recordset'
              798  LOAD_ATTR                _jobject
              800  STORE_FAST               'java_overlay'
              802  JUMP_FORWARD        880  'to 880'
            804_0  COME_FROM           778  '778'

 L. 724       804  LOAD_GLOBAL              isinstance
              806  LOAD_FAST                '_overlay_input'
              808  LOAD_GLOBAL              Recordset
              810  CALL_FUNCTION_2       2  '2 positional arguments'
          812_814  POP_JUMP_IF_FALSE   830  'to 830'

 L. 725       816  LOAD_FAST                '_source_input'
              818  LOAD_ATTR                _jobject
              820  STORE_FAST               'java_source'

 L. 726       822  LOAD_FAST                '_overlay_input'
              824  LOAD_ATTR                _jobject
              826  STORE_FAST               'java_overlay'
              828  JUMP_FORWARD        880  'to 880'
            830_0  COME_FROM           812  '812'

 L. 728       830  LOAD_FAST                'temp_ds'
              832  LOAD_CONST               None
              834  COMPARE_OP               is
          836_838  POP_JUMP_IF_FALSE   850  'to 850'

 L. 729       840  LOAD_GLOBAL              Datasource
              842  LOAD_METHOD              create
              844  LOAD_STR                 ':memory:'
              846  CALL_METHOD_1         1  '1 positional argument'
              848  STORE_FAST               'temp_ds'
            850_0  COME_FROM           836  '836'

 L. 730       850  LOAD_FAST                'temp_ds'
              852  LOAD_METHOD              write_spatial_data
              854  LOAD_FAST                '_overlay_input'
              856  CALL_METHOD_1         1  '1 positional argument'
              858  STORE_FAST               'dt'

 L. 731       860  LOAD_FAST                '_source_input'
              862  LOAD_ATTR                _jobject
              864  STORE_FAST               'java_source'

 L. 732       866  LOAD_FAST                'dt'
              868  LOAD_METHOD              get_recordset
              870  CALL_METHOD_0         0  '0 positional arguments'
              872  STORE_FAST               'overlay_recordset'

 L. 733       874  LOAD_FAST                'overlay_recordset'
              876  LOAD_ATTR                _jobject
              878  STORE_FAST               'java_overlay'
            880_0  COME_FROM           828  '828'
            880_1  COME_FROM           802  '802'
              880  JUMP_FORWARD       1042  'to 1042'
            882_0  COME_FROM           766  '766'

 L. 735       882  LOAD_FAST                'temp_ds'
              884  LOAD_CONST               None
              886  COMPARE_OP               is
          888_890  POP_JUMP_IF_FALSE   902  'to 902'

 L. 736       892  LOAD_GLOBAL              Datasource
              894  LOAD_METHOD              create
              896  LOAD_STR                 ':memory:'
              898  CALL_METHOD_1         1  '1 positional argument'
              900  STORE_FAST               'temp_ds'
            902_0  COME_FROM           888  '888'

 L. 737       902  LOAD_FAST                'temp_ds'
              904  LOAD_METHOD              write_spatial_data
              906  LOAD_FAST                '_source_input'
              908  CALL_METHOD_1         1  '1 positional argument'
              910  STORE_FAST               'dt'

 L. 738       912  LOAD_GLOBAL              isinstance
              914  LOAD_FAST                '_overlay_input'
              916  LOAD_GLOBAL              DatasetVector
              918  CALL_FUNCTION_2       2  '2 positional arguments'
          920_922  POP_JUMP_IF_FALSE   950  'to 950'

 L. 739       924  LOAD_FAST                '_overlay_input'
              926  LOAD_ATTR                _jobject
              928  STORE_FAST               'java_overlay'

 L. 740       930  LOAD_FAST                'dt'
              932  LOAD_METHOD              set_prj_coordsys
              934  LOAD_FAST                '_overlay_input'
              936  LOAD_ATTR                prj_coordsys
              938  CALL_METHOD_1         1  '1 positional argument'
              940  POP_TOP          

 L. 741       942  LOAD_FAST                'dt'
              944  LOAD_ATTR                _jobject
              946  STORE_FAST               'java_source'
              948  JUMP_FORWARD       1042  'to 1042'
            950_0  COME_FROM           920  '920'

 L. 742       950  LOAD_GLOBAL              isinstance
              952  LOAD_FAST                '_overlay_input'
              954  LOAD_GLOBAL              Recordset
              956  CALL_FUNCTION_2       2  '2 positional arguments'
          958_960  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 743       962  LOAD_FAST                'dt'
              964  LOAD_METHOD              set_prj_coordsys
              966  LOAD_FAST                '_overlay_input'
              968  LOAD_ATTR                dataset
              970  LOAD_ATTR                prj_coordsys
              972  CALL_METHOD_1         1  '1 positional argument'
              974  POP_TOP          

 L. 744       976  LOAD_FAST                'dt'
              978  LOAD_METHOD              get_recordset
              980  CALL_METHOD_0         0  '0 positional arguments'
              982  STORE_FAST               'source_recordset'

 L. 745       984  LOAD_GLOBAL              oj
              986  LOAD_FAST                'source_recordset'
              988  CALL_FUNCTION_1       1  '1 positional argument'
            990_0  COME_FROM           704  '704'
              990  STORE_FAST               'java_source'

 L. 746       992  LOAD_FAST                '_overlay_input'
              994  LOAD_ATTR                _jobject
              996  STORE_FAST               'java_overlay'
              998  JUMP_FORWARD       1042  'to 1042'
           1000_0  COME_FROM           958  '958'

 L. 748      1000  LOAD_FAST                'temp_ds'
             1002  LOAD_CONST               None
             1004  COMPARE_OP               is
         1006_1008  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 749      1010  LOAD_GLOBAL              Datasource
             1012  LOAD_METHOD              create
             1014  LOAD_STR                 ':memory:'
             1016  CALL_METHOD_1         1  '1 positional argument'
             1018  STORE_FAST               'temp_ds'
           1020_0  COME_FROM          1006  '1006'

 L. 750      1020  LOAD_FAST                'temp_ds'
             1022  LOAD_METHOD              write_spatial_data
           1024_0  COME_FROM           738  '738'
             1024  LOAD_FAST                '_overlay_input'
             1026  CALL_METHOD_1         1  '1 positional argument'
             1028  STORE_FAST               'dt_overlay'

 L. 751      1030  LOAD_FAST                'dt_overlay'
             1032  LOAD_ATTR                _jobject
             1034  STORE_FAST               'java_overlay'

 L. 752      1036  LOAD_FAST                'dt'
             1038  LOAD_ATTR                _jobject
             1040  STORE_FAST               'java_source'
           1042_0  COME_FROM           998  '998'
           1042_1  COME_FROM           948  '948'
           1042_2  COME_FROM           880  '880'
           1042_3  COME_FROM           754  '754'

 L. 754      1042  LOAD_FAST                '_jvm'
             1044  LOAD_ATTR                com
             1046  LOAD_ATTR                supermap
             1048  LOAD_ATTR                analyst
             1050  LOAD_ATTR                spatialanalyst
             1052  LOAD_METHOD              OverlayAnalystParameter
             1054  CALL_METHOD_0         0  '0 positional arguments'
             1056  STORE_FAST               'param'

 L. 755      1058  LOAD_FAST                'source_retained'
             1060  LOAD_CONST               None
             1062  COMPARE_OP               is-not
         1064_1066  POP_JUMP_IF_FALSE  1086  'to 1086'

 L. 756      1068  LOAD_FAST                'param'
             1070  LOAD_METHOD              setSourceRetainedFields
             1072  LOAD_GLOBAL              to_java_string_array
             1074  LOAD_GLOBAL              split_input_list_from_str
             1076  LOAD_FAST                'source_retained'
             1078  CALL_FUNCTION_1       1  '1 positional argument'
             1080  CALL_FUNCTION_1       1  '1 positional argument'
             1082  CALL_METHOD_1         1  '1 positional argument'
             1084  POP_TOP          
           1086_0  COME_FROM          1064  '1064'

 L. 757      1086  LOAD_FAST                'overlay_retained'
             1088  LOAD_CONST               None
             1090  COMPARE_OP               is-not
         1092_1094  POP_JUMP_IF_FALSE  1114  'to 1114'

 L. 758      1096  LOAD_FAST                'param'
             1098  LOAD_METHOD              setOperationRetainedFields
             1100  LOAD_GLOBAL              to_java_string_array
             1102  LOAD_GLOBAL              split_input_list_from_str
             1104  LOAD_FAST                'overlay_retained'
             1106  CALL_FUNCTION_1       1  '1 positional argument'
             1108  CALL_FUNCTION_1       1  '1 positional argument'
             1110  CALL_METHOD_1         1  '1 positional argument'
             1112  POP_TOP          
           1114_0  COME_FROM          1092  '1092'

 L. 759      1114  LOAD_FAST                'param'
             1116  LOAD_METHOD              setTolerance
             1118  LOAD_FAST                'tolerance'
             1120  CALL_METHOD_1         1  '1 positional argument'
             1122  POP_TOP          

 L. 761      1124  LOAD_FAST                'progress'
             1126  LOAD_CONST               None
             1128  COMPARE_OP               is-not
         1130_1132  POP_JUMP_IF_FALSE  1232  'to 1232'

 L. 762      1134  LOAD_GLOBAL              safe_start_callback_server
             1136  CALL_FUNCTION_0       0  '0 positional arguments'
         1138_1140  POP_JUMP_IF_FALSE  1232  'to 1232'

 L. 763      1142  SETUP_EXCEPT       1178  'to 1178'

 L. 764      1144  LOAD_GLOBAL              ProgressListener
             1146  LOAD_FAST                'progress'
             1148  LOAD_STR                 'overlay'
             1150  CALL_FUNCTION_2       2  '2 positional arguments'
             1152  STORE_FAST               'listener'

 L. 765      1154  LOAD_FAST                '_jvm'
             1156  LOAD_ATTR                com
             1158  LOAD_ATTR                supermap
             1160  LOAD_ATTR                analyst
             1162  LOAD_ATTR                spatialanalyst
             1164  LOAD_ATTR                OverlayAnalyst
             1166  LOAD_METHOD              addSteppedListener
             1168  LOAD_FAST                'listener'
             1170  CALL_METHOD_1         1  '1 positional argument'
             1172  POP_TOP          
             1174  POP_BLOCK        
             1176  JUMP_FORWARD       1232  'to 1232'
           1178_0  COME_FROM_EXCEPT   1142  '1142'

 L. 766      1178  DUP_TOP          
             1180  LOAD_GLOBAL              Exception
             1182  COMPARE_OP               exception-match
         1184_1186  POP_JUMP_IF_FALSE  1230  'to 1230'
             1188  POP_TOP          
             1190  STORE_FAST               'e'
             1192  POP_TOP          
             1194  SETUP_FINALLY      1218  'to 1218'

 L. 767      1196  LOAD_GLOBAL              close_callback_server
             1198  CALL_FUNCTION_0       0  '0 positional arguments'
             1200  POP_TOP          

 L. 768      1202  LOAD_GLOBAL              log_error
             1204  LOAD_FAST                'e'
             1206  CALL_FUNCTION_1       1  '1 positional argument'
             1208  POP_TOP          

 L. 769      1210  LOAD_CONST               None
             1212  STORE_FAST               'listener'
             1214  POP_BLOCK        
             1216  LOAD_CONST               None
           1218_0  COME_FROM_FINALLY  1194  '1194'
             1218  LOAD_CONST               None
             1220  STORE_FAST               'e'
             1222  DELETE_FAST              'e'
             1224  END_FINALLY      
             1226  POP_EXCEPT       
             1228  JUMP_FORWARD       1232  'to 1232'
           1230_0  COME_FROM          1184  '1184'
             1230  END_FINALLY      
           1232_0  COME_FROM          1228  '1228'
           1232_1  COME_FROM          1176  '1176'
           1232_2  COME_FROM          1138  '1138'
           1232_3  COME_FROM          1130  '1130'

 L. 771      1232  LOAD_GLOBAL              OverlayMode
             1234  LOAD_ATTR                CLIP
             1236  LOAD_FAST                '_jvm'
             1238  LOAD_ATTR                com
             1240  LOAD_ATTR                supermap
             1242  LOAD_ATTR                analyst
             1244  LOAD_ATTR                spatialanalyst
             1246  LOAD_ATTR                OverlayAnalyst
             1248  LOAD_ATTR                clip

 L. 772      1250  LOAD_GLOBAL              OverlayMode
             1252  LOAD_ATTR                ERASE
             1254  LOAD_FAST                '_jvm'
             1256  LOAD_ATTR                com
             1258  LOAD_ATTR                supermap
             1260  LOAD_ATTR                analyst
             1262  LOAD_ATTR                spatialanalyst
             1264  LOAD_ATTR                OverlayAnalyst
             1266  LOAD_ATTR                erase

 L. 773      1268  LOAD_GLOBAL              OverlayMode
             1270  LOAD_ATTR                INTERSECT
             1272  LOAD_FAST                '_jvm'
             1274  LOAD_ATTR                com
             1276  LOAD_ATTR                supermap
             1278  LOAD_ATTR                analyst
             1280  LOAD_ATTR                spatialanalyst
             1282  LOAD_ATTR                OverlayAnalyst
             1284  LOAD_ATTR                intersect

 L. 774      1286  LOAD_GLOBAL              OverlayMode
             1288  LOAD_ATTR                IDENTITY
             1290  LOAD_FAST                '_jvm'
             1292  LOAD_ATTR                com
             1294  LOAD_ATTR                supermap
             1296  LOAD_ATTR                analyst
             1298  LOAD_ATTR                spatialanalyst
             1300  LOAD_ATTR                OverlayAnalyst
             1302  LOAD_ATTR                identity

 L. 775      1304  LOAD_GLOBAL              OverlayMode
             1306  LOAD_ATTR                XOR
             1308  LOAD_FAST                '_jvm'
             1310  LOAD_ATTR                com
             1312  LOAD_ATTR                supermap
             1314  LOAD_ATTR                analyst
             1316  LOAD_ATTR                spatialanalyst
             1318  LOAD_ATTR                OverlayAnalyst
             1320  LOAD_ATTR                xOR

 L. 776      1322  LOAD_GLOBAL              OverlayMode
             1324  LOAD_ATTR                UPDATE
             1326  LOAD_FAST                '_jvm'
             1328  LOAD_ATTR                com
             1330  LOAD_ATTR                supermap
             1332  LOAD_ATTR                analyst
             1334  LOAD_ATTR                spatialanalyst
             1336  LOAD_ATTR                OverlayAnalyst
             1338  LOAD_ATTR                update

 L. 777      1340  LOAD_GLOBAL              OverlayMode
             1342  LOAD_ATTR                UNION
             1344  LOAD_FAST                '_jvm'
             1346  LOAD_ATTR                com
             1348  LOAD_ATTR                supermap
             1350  LOAD_ATTR                analyst
             1352  LOAD_ATTR                spatialanalyst
             1354  LOAD_ATTR                OverlayAnalyst
             1356  LOAD_ATTR                union
             1358  BUILD_MAP_7           7 
             1360  STORE_FAST               'overlay_funs'

 L. 779      1362  LOAD_FAST                'overlay_funs'
             1364  LOAD_FAST                '_overlayMode'
             1366  BINARY_SUBSCR    
             1368  LOAD_FAST                'java_source'
             1370  LOAD_FAST                'java_overlay'
             1372  LOAD_FAST                'java_result_dt'
             1374  LOAD_FAST                'param'
             1376  CALL_FUNCTION_4       4  '4 positional arguments'
             1378  STORE_FAST               'result'
             1380  POP_BLOCK        
             1382  JUMP_FORWARD       1444  'to 1444'
           1384_0  COME_FROM_EXCEPT    664  '664'

 L. 780      1384  DUP_TOP          
             1386  LOAD_GLOBAL              Exception
             1388  COMPARE_OP               exception-match
         1390_1392  POP_JUMP_IF_FALSE  1442  'to 1442'
             1394  POP_TOP          
             1396  STORE_FAST               'e'
             1398  POP_TOP          
             1400  SETUP_FINALLY      1430  'to 1430'

 L. 781      1402  LOAD_CONST               0
             1404  LOAD_CONST               None
             1406  IMPORT_NAME              traceback
             1408  STORE_FAST               'traceback'

 L. 782      1410  LOAD_GLOBAL              log_error
             1412  LOAD_FAST                'traceback'
             1414  LOAD_METHOD              format_exc
             1416  CALL_METHOD_0         0  '0 positional arguments'
             1418  CALL_FUNCTION_1       1  '1 positional argument'
             1420  POP_TOP          

 L. 783      1422  LOAD_CONST               False
             1424  STORE_FAST               'result'
             1426  POP_BLOCK        
             1428  LOAD_CONST               None
           1430_0  COME_FROM_FINALLY  1400  '1400'
             1430  LOAD_CONST               None
             1432  STORE_FAST               'e'
             1434  DELETE_FAST              'e'
             1436  END_FINALLY      
             1438  POP_EXCEPT       
             1440  JUMP_FORWARD       1444  'to 1444'
           1442_0  COME_FROM          1390  '1390'
             1442  END_FINALLY      
           1444_0  COME_FROM          1440  '1440'
           1444_1  COME_FROM          1382  '1382'
             1444  POP_BLOCK        
             1446  LOAD_CONST               None
           1448_0  COME_FROM_FINALLY   660  '660'

 L. 785      1448  LOAD_FAST                'listener'
             1450  LOAD_CONST               None
             1452  COMPARE_OP               is-not
         1454_1456  POP_JUMP_IF_FALSE  1534  'to 1534'

 L. 786      1458  SETUP_EXCEPT       1484  'to 1484'

 L. 787      1460  LOAD_FAST                '_jvm'
             1462  LOAD_ATTR                com
             1464  LOAD_ATTR                supermap
             1466  LOAD_ATTR                analyst
             1468  LOAD_ATTR                spatialanalyst
             1470  LOAD_ATTR                OverlayAnalyst
             1472  LOAD_METHOD              removeSteppedListener
             1474  LOAD_FAST                'listener'
             1476  CALL_METHOD_1         1  '1 positional argument'
             1478  POP_TOP          
             1480  POP_BLOCK        
             1482  JUMP_FORWARD       1528  'to 1528'
           1484_0  COME_FROM_EXCEPT   1458  '1458'

 L. 788      1484  DUP_TOP          
             1486  LOAD_GLOBAL              Exception
             1488  COMPARE_OP               exception-match
         1490_1492  POP_JUMP_IF_FALSE  1526  'to 1526'
             1494  POP_TOP          
             1496  STORE_FAST               'e1'
             1498  POP_TOP          
             1500  SETUP_FINALLY      1514  'to 1514'

 L. 789      1502  LOAD_GLOBAL              log_error
             1504  LOAD_FAST                'e1'
             1506  CALL_FUNCTION_1       1  '1 positional argument'
             1508  POP_TOP          
             1510  POP_BLOCK        
             1512  LOAD_CONST               None
           1514_0  COME_FROM_FINALLY  1500  '1500'
             1514  LOAD_CONST               None
             1516  STORE_FAST               'e1'
             1518  DELETE_FAST              'e1'
             1520  END_FINALLY      
             1522  POP_EXCEPT       
             1524  JUMP_FORWARD       1528  'to 1528'
           1526_0  COME_FROM          1490  '1490'
             1526  END_FINALLY      
           1528_0  COME_FROM          1524  '1524'
           1528_1  COME_FROM          1482  '1482'

 L. 790      1528  LOAD_GLOBAL              close_callback_server
             1530  CALL_FUNCTION_0       0  '0 positional arguments'
             1532  POP_TOP          
           1534_0  COME_FROM          1454  '1454'

 L. 792      1534  LOAD_FAST                'source_recordset'
             1536  LOAD_CONST               None
             1538  COMPARE_OP               is-not
         1540_1542  POP_JUMP_IF_FALSE  1574  'to 1574'

 L. 793      1544  SETUP_EXCEPT       1560  'to 1560'

 L. 794      1546  LOAD_FAST                'source_recordset'
             1548  LOAD_METHOD              close
             1550  CALL_METHOD_0         0  '0 positional arguments'
             1552  POP_TOP          

 L. 795      1554  DELETE_FAST              'source_recordset'
             1556  POP_BLOCK        
             1558  JUMP_FORWARD       1574  'to 1574'
           1560_0  COME_FROM_EXCEPT   1544  '1544'

 L. 796      1560  POP_TOP          
             1562  POP_TOP          
             1564  POP_TOP          

 L. 797      1566  DELETE_FAST              'source_recordset'
             1568  POP_EXCEPT       
             1570  JUMP_FORWARD       1574  'to 1574'
             1572  END_FINALLY      
           1574_0  COME_FROM          1570  '1570'
           1574_1  COME_FROM          1558  '1558'
           1574_2  COME_FROM          1540  '1540'

 L. 799      1574  LOAD_FAST                'overlay_recordset'
             1576  LOAD_CONST               None
             1578  COMPARE_OP               is-not
         1580_1582  POP_JUMP_IF_FALSE  1614  'to 1614'

 L. 800      1584  SETUP_EXCEPT       1600  'to 1600'

 L. 801      1586  LOAD_FAST                'overlay_recordset'
             1588  LOAD_METHOD              close
             1590  CALL_METHOD_0         0  '0 positional arguments'
             1592  POP_TOP          

 L. 802      1594  DELETE_FAST              'overlay_recordset'
             1596  POP_BLOCK        
             1598  JUMP_FORWARD       1614  'to 1614'
           1600_0  COME_FROM_EXCEPT   1584  '1584'

 L. 803      1600  POP_TOP          
             1602  POP_TOP          
             1604  POP_TOP          

 L. 804      1606  DELETE_FAST              'overlay_recordset'
             1608  POP_EXCEPT       
             1610  JUMP_FORWARD       1614  'to 1614'
             1612  END_FINALLY      
           1614_0  COME_FROM          1610  '1610'
           1614_1  COME_FROM          1598  '1598'
           1614_2  COME_FROM          1580  '1580'

 L. 806      1614  SETUP_EXCEPT       1640  'to 1640'

 L. 807      1616  LOAD_FAST                'temp_ds'
             1618  LOAD_CONST               None
             1620  COMPARE_OP               is-not
         1622_1624  POP_JUMP_IF_FALSE  1636  'to 1636'

 L. 808      1626  LOAD_FAST                'temp_ds'
             1628  LOAD_METHOD              close
             1630  CALL_METHOD_0         0  '0 positional arguments'
             1632  POP_TOP          

 L. 809      1634  DELETE_FAST              'temp_ds'
           1636_0  COME_FROM          1622  '1622'
             1636  POP_BLOCK        
             1638  JUMP_FORWARD       1654  'to 1654'
           1640_0  COME_FROM_EXCEPT   1614  '1614'

 L. 810      1640  POP_TOP          
             1642  POP_TOP          
             1644  POP_TOP          

 L. 811      1646  DELETE_FAST              'temp_ds'
             1648  POP_EXCEPT       
             1650  JUMP_FORWARD       1654  'to 1654'
             1652  END_FINALLY      
           1654_0  COME_FROM          1650  '1650'
           1654_1  COME_FROM          1638  '1638'

 L. 813      1654  LOAD_FAST                'result'
         1656_1658  POP_JUMP_IF_TRUE   1676  'to 1676'

 L. 814      1660  LOAD_FAST                'out_datasource'
             1662  LOAD_METHOD              delete
             1664  LOAD_FAST                'result_dt'
             1666  LOAD_ATTR                name
             1668  CALL_METHOD_1         1  '1 positional argument'
             1670  POP_TOP          

 L. 815      1672  LOAD_CONST               None
             1674  STORE_FAST               'result_dt'
           1676_0  COME_FROM          1656  '1656'

 L. 816      1676  LOAD_FAST                'result_dt'
         1678_1680  POP_JUMP_IF_TRUE   1690  'to 1690'

 L. 817      1682  LOAD_FAST                'result_dt'
             1684  LOAD_METHOD              open
             1686  CALL_METHOD_0         0  '0 positional arguments'
             1688  POP_TOP          
           1690_0  COME_FROM          1678  '1678'

 L. 819      1690  LOAD_FAST                'out_data'
             1692  LOAD_CONST               None
             1694  COMPARE_OP               is-not
         1696_1698  POP_JUMP_IF_FALSE  1710  'to 1710'

 L. 820      1700  LOAD_GLOBAL              try_close_output_datasource
             1702  LOAD_FAST                'result_dt'
             1704  LOAD_FAST                'out_datasource'
             1706  CALL_FUNCTION_2       2  '2 positional arguments'
             1708  RETURN_VALUE     
           1710_0  COME_FROM          1696  '1696'

 L. 822      1710  LOAD_FAST                'result_dt'
             1712  RETURN_VALUE     
             1714  END_FINALLY      

Parse error at or near `COME_FROM' instruction at offset 990_0


def _overlay_geometrys(source_geos, overlay_geos, overlay_mode, ds, out_name, tolerance, progress):
    _overlayMode = OverlayMode._make(overlay_mode)
    _jvm = get_jvm()
    overlay_funs = {OverlayMode.CLIP: _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.clip, 
     OverlayMode.ERASE: _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.erase, 
     OverlayMode.INTERSECT: _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.intersect, 
     OverlayMode.IDENTITY: _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.identity, 
     OverlayMode.XOR: _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.xOR, 
     OverlayMode.UPDATE: _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.update, 
     OverlayMode.UNION: _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.union}
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'overlay')
                _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            result = overlay_funs[_overlayMode](to_java_geometry_array(source_geos), to_java_geometry_array(overlay_geos), tolerance)
        except:
            import traceback
            log_error(traceback.format_exc())
            result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if result is None:
            return try_close_output_datasource(None, ds)
        from .data import FieldInfo, Feature
        field_infos = [FieldInfo('SourceIndex', 'INT32'), FieldInfo('OverlayIndex', 'INT32')]
        features = []
        for r in result:
            feature = Feature((Geometry._from_java_object(r.getGeometry())), [
             r.getSourceIndex(), r.getTargetIndex()],
              field_infos=field_infos)
            features.append(feature)

        dt = ds.write_features(features, out_name)
        return try_close_output_datasource(dt, ds)


class _DissolveParameter:
    __doc__ = '\n    融合是指将融合字段值相同的对象合并为一个简单对象或复杂对象。适用于线对象和面对象。简单对象是指只有一个子对象（即简单对象本身）的对象，与复杂对象对应。\n    复杂对象是指具有两个或多个子对象的对象，这些子对象类型相同。子对象是构成简单对象和复杂对象的基本对象。简单对象由一个子对象组成，即简单对象本身；复杂对象由两个或两个以上相同类型的子对象组成\n    '

    def __init__(self, dissolve_type=None, fields=None, stats_fields=None, stats_types=None, attr_filter=None, tolerance=1e-10, is_null_value_able=True, is_preprocess=True):
        """
        初始化融合参数对象
        :param dissolve_type: 融合类型
        :type dissolve_type: DissolveType or str
        :param fields: 融合字段，融合字段的字段值相同的记录才会融合。当 fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1,field2,field3"
        :type fields: list[str] or str
        :param stats_fields:  统计字段的名称的集合。当 stats_fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1,field2,field3"
        :type stats_fields: list[str] or str
        :param stats_types: 统计字段的类型的集合。必须与 stats_fields 数目相同。如果 stats_types 为 str 时，支持设置 ',' 分隔多个统计字段类型名称，比如'MAX,MIN,SUM'
        :type stats_types: list[StatisticsType] or str
        :param str attr_filter: 数据集融合时对象的过滤表达式
        :param float tolerance: 融合容限
        :param bool is_null_value_able: 是否处理融合字段值为空的对象
        :param bool is_preprocess: 是否进行拓扑预处理
        """
        self._dissolveType = None
        self._fields = None
        self._statsFields = None
        self._statsType = None
        self._filter = None
        self._tolerance = 1e-10
        self._isNullValue = True
        self._isPreprocess = True
        self.set_dissolve_type(dissolve_type)
        self.set_dissolve_fields(fields)
        self.set_statistics_field_names(stats_fields)
        self.set_statistics_types(stats_types)
        self.set_filter_string(attr_filter)
        self.set_tolerance(tolerance)
        self.set_null_value_able(is_null_value_able)
        self.set_preprocess(is_preprocess)

    def set_dissolve_type(self, value):
        """
        设置融合类型

        :param value:  融合类型
        :type value: DissolveType or str
        :return: self
        :rtype: _DissolveParameter
        """
        self._dissolveType = DissolveType._make(value)
        return self

    @property
    def dissolve_type(self):
        """DissolveType: 返回融合类型"""
        return self._dissolveType

    def set_dissolve_fields(self, value):
        """
        设置融合字段

        :param value: 融合字段的字段值相同的记录才会融合。当 value 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1,field2,field3"
        :type value: list[str] or str
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._fields = split_input_list_from_str(value)
        return self

    @property
    def dissolve_fields(self):
        """list[str]: 融合字段"""
        return self._fields

    def set_statistics_field_names(self, value):
        """
        设置属性统计字段名称
        :param value: 属性统计字段名称。如果 value 为 str 时，支持设置 ',' 分隔多个统计字段类型名称，比如'field1,field2,field3'
        :type value: list[str] or str
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._statsFields = split_input_list_from_str(value)
        return self

    @property
    def statistics_field_names(self):
        """list[str]: 属性统计字段名称"""
        return self._statsFields

    def set_statistics_types(self, value):
        """
        设置属性统计类型，数目必须与 statistics_field_names 数目相同

        :param value: 属性统计类型。如果 value 为 str 时，支持设置 ',' 分隔多个统计字段类型名称，比如'MAX,MIN,SUM'
        :type value: list[StatisticsType] or str
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            items = split_input_list_from_str(value)
            if items is not None:
                self._statsType = []
                for item in items:
                    self._statsType.append(StatisticsType._make(item))

        return self

    @property
    def statistics_types(self):
        """list[StatisticsType]: 属性统计类型列表"""
        return self._statsType

    def set_filter_string(self, value):
        """
        设置数据集融合时对象的过滤表达式

        :param str value: 数据集融合时对象的过滤表达式
        :return: self
        :rtype: _DissolveParameter
        """
        self._filter = value
        return self

    @property
    def filter_string(self):
        """str: 数据集融合时对象的过滤表达式 """
        return self._filter

    def set_tolerance(self, value):
        """
        设置融合过程中使用的节点容限

        :param float value: 节点容限
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._tolerance = float(value)
        return self

    @property
    def tolerance(self):
        """float: 融合过程使用的节点容限"""
        return self._tolerance

    def set_null_value_able(self, value):
        """
        设置是否处理空字段对象

        :param bool value: 是否处理空字段对象
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._isNullValue = bool(value)
        return self

    @property
    def is_null_value_able(self):
        """bool: 是否处理空字段的对象 """
        return self._isNullValue

    def set_preprocess(self, value):
        """
        设置是否进行拓扑预处理

        :param bool value: 是否进行拓扑预处理
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._isPreprocess = bool(value)
        return self

    @property
    def is_preprocess(self):
        """bool: 是否进行拓扑预处理"""
        return self._isPreprocess

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_parameter = get_jvm().com.supermap.analyst.spatialanalyst.DissolveParameter()
        java_parameter.setDissolveType(self.dissolve_type._jobject)
        java_parameter.setFieldNames(to_java_string_array(self.dissolve_fields))
        java_parameter.setFilterString(self.filter_string)
        java_parameter.setNullValue(self.is_null_value_able)
        java_parameter.setPreProcess(self.is_preprocess)
        if self.statistics_field_names is not None:
            java_parameter.setStatisticsFieldNames(to_java_string_array(self.statistics_field_names))
        if self.statistics_types is not None:
            java_parameter.setStatisticsTypes(to_java_stattype_array(self.statistics_types))
        java_parameter.setTolerance(self.tolerance)
        return java_parameter


def dissolve(input_data, dissolve_type, dissolve_fields, field_stats=None, attr_filter=None, is_null_value_able=True, is_preprocess=True, tolerance=1e-10, out_data=None, out_dataset_name='DissolveResult', progress=None):
    """
    融合是指将融合字段值相同的对象合并为一个简单对象或复杂对象。适用于线对象和面对象。子对象是构成简单对象和复杂对象的基本对象。简单对象由一个子对象组成，
    即简单对象本身；复杂对象由两个或两个以上相同类型的子对象组成。

    :param input_data: 待融合的矢量数据集。必须为线数据集或面数据集。
    :type input_data: DatasetVector or str
    :param dissolve_type: 融合类型
    :type dissolve_type: DissolveType or str
    :param dissolve_fields: 融合字段，融合字段的字段值相同的记录才会融合。当 dissolve_fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1,field2,field3"
    :type dissolve_fields: list[str] or str
    :param field_stats:  统计字段名称和对应的统计类型。stats_fields 为 list，list中每个元素为一个tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型。
                         当 stats_fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1:SUM, field2:MAX, field3:MIN"
    :type field_stats: list[tuple[str,StatisticsType]] or list[tuple[str,str]] or str
    :param str attr_filter: 数据集融合时对象的过滤表达式
    :param float tolerance: 融合容限
    :param bool is_null_value_able: 是否处理融合字段值为空的对象
    :param bool is_preprocess: 是否进行拓扑预处理
    :param out_data: 结果数据保存的数据源。如果为空，则结果数据集保存到输入数据集所在的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str

    >>> result = dissolve('E:/data.udb/zones', 'SINGLE', 'SmUserID', 'Area:SUM', tolerance=0.000001, out_data='E:/dissolve_out.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_Dissolve'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    stats_fields = []
    stats_types = []
    if field_stats is not None:
        field_stats = split_input_list_tuple_item_from_str(field_stats)
        if isinstance(field_stats, list):
            for name, stat_type in field_stats:
                stats_fields.append(name)
                stats_types.append(StatisticsType._make(stat_type))

    parameter = _DissolveParameter().set_dissolve_type(dissolve_type).set_dissolve_fields(dissolve_fields).set_statistics_field_names(stats_fields).set_statistics_types(stats_types).set_filter_string(attr_filter).set_tolerance(tolerance).set_null_value_able(is_null_value_able).set_preprocess(is_preprocess)
    _java_parameter = parameter._jobject
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'dissolve')
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.Generalization.dissolve(_source_input._jobject, _ds._jobject, _outDatasetName, _java_parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def aggregate_points(input_data, min_pile_point, distance, unit=None, class_field=None, out_data=None, out_dataset_name='AggregateResult', progress=None):
    """
    对点数据集进行聚类，使用密度聚类算法，返回聚类后的类别或同一簇构成的多边形。
    对点集合进行空间位置的聚类，使用密度聚类方法 DBSCAN，它能将具有足够高密度的区域划分为簇，并可以在带有噪声的空间数据中发现任意形状的聚类。它定义
    簇为密度相连的点的最大集合。DBSCAN 使用阈值 e 和 MinPts 来控制簇的生成。其中，给定对象半径 e 内的区域称为该对象的 e一邻域。如果一个对象的
    e一邻域至少包含最小数目 MinPtS 个对象，则称该对象为核心对象。给定一个对象集合 D，如果 P 是在 Q 的 e一邻域内，而 Q 是一个核心对象，我们说对象
    P 从对象 Q 出发是直接密度可达的。DBSCAN 通过检查数据里中每个点的 e-领域来寻找聚类，如果一个点 P 的 e-领域包含多于 MinPts 个点，则创建一个
    以 P 作为核心对象的新簇，然后，DBSCAN反复地寻找从这些核心对象直接密度可达的对象并加入该簇，直到没有新的点可以被添加。

    :param input_data: 输入的点数据集
    :type input_data: DatasetVector or str
    :param int min_pile_point:  密度聚类点数目阈值，必须大于等于2。阈值越大表示能聚类为一簇的条件越苛刻。
    :param float distance: 密度聚类半径。
    :param unit:  密度聚类半径的单位。
    :type unit: Unit or str
    :param str class_field: 输入的点数据集中用于保存密度聚类的结果聚类类别的字段，如果不为空，则必须是点数据集中合法的字段名称。
                            要求字段类型为INT16, INT32 或 INT64，如果字段名有效但不存在，将会创建一个 INT32 的字段。
                            参数有效，则会将聚类类别保存在此字段中。
    :param out_data: 结果数据源信息，结果数据源信息不能与 class_field同时为空，如果结果数据源有效时，将会生成结果面对象。
    :type out_data: Datasource or DatasourceConnectionInfo or st
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称，如果输入的结果数据源为空，将会返回一个布尔值，True 表示聚类成功，False 表示聚类失败。
    :rtype: DatasetVector or str or bool

    >>> result = aggregate_points('E:/data.udb/point', 4, 100, 'Meter', 'SmUserID', out_data='E:/aggregate_out.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    elif not isinstance(_source_input, DatasetVector):
        raise ValueError('source input_data must be DatasetVector')
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = _source_input.name + '_Agge'
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
        else:
            _ds = None
            _outDatasetName = None
        _jvm = get_jvm()
        if class_field is not None:
            field_info = _source_input.get_field_info(str(class_field))
            if field_info is not None:
                if field_info.type not in (FieldType.INT16, FieldType.INT32, FieldType.INT64):
                    raise ValueError('invalid class field type, required int16, int32 and int64, but is ' + str(field_info.type.name))
            else:
                from .data import FieldInfo
                _source_input.create_field(FieldInfo(class_field, FieldType.INT32))
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'aggregate_points')
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            is_success = _jvm.com.supermap.analyst.spatialanalyst.Generalization.aggregatePoints(oj(_source_input), float(distance), oj(Unit._make(unit)), min_pile_point, oj(_ds), _outDatasetName, class_field)
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif is_success:
            if _outDatasetName is not None:
                return try_close_output_datasource(_ds[_outDatasetName], _ds)
            return is_success
        else:
            if _outDatasetName is not None:
                return try_close_output_datasource(None, _ds)
            return False


def smooth_vector(input_data, smoothness, out_data=None, out_dataset_name=None, progress=None):
    """
    对矢量数据集进行光滑，支持线数据集、面数据集和网络数据集

    * 光滑的目的

        当折线或多边形的边界的线段过多时，就可能影响对原始特征的描述，不利用进一步的处理或分析，或显示和打印效果不够理想，因此需要对数据简化。简化的方法
        一般有重采样（:py:meth:`resample_vector`）和光滑。光滑是通过增加节点的方式使用曲线或直线段来代替原始折线的方法。需要注意，对折线进行光滑后，
        其长度通常会变短，折线上线段的方向也会发生明显改变，但两个端点的相对位置不会变化；面对象经过光滑后，其面积通常会变小。

    * 光滑方法与光滑系数的设置

        该方法采用 B 样条法对矢量数据集进行光滑。有关 B 样条法的介绍可参见 SmoothMethod 类。光滑系数（方法中对应 smoothness 参数）影响着光滑的程度，
        光滑系数越大，结果数据越光滑。光滑系数的建议取值范围为[2,10]。该方法支持对线数据集、面数据集和网络数据集进行光滑。

        * 对线数据集设置不同光滑系数的光滑效果：

        .. image:: ../image/Smooth_1.png

        * 对面数据集设置不同光滑系数的光滑效果：

        .. image:: ../image/Smooth_2.png

    :param input_data: 需要进行光滑处理的数据集，支持线数据集、面数据集和网络数据集
    :type input_data: DatasetVector or str
    :param int smoothness: 指定的光滑系数。取大于等于 2 的值有效，该值越大，线对象或面对象边界的节点数越多，也就越光滑。建议取值范围为[2,10]。
    :param out_data: 结果数据源所在半径，如果此参数为空，将直接对原始数据做光滑，也就是会改变原始数据。如果此参数不为空，将会先复制原始数据到此数据源中，
                     再对复制得到的数据集进行光滑处理。out_data 所指向数据源可以与源数据集所在的数据源相同。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称，当 out_data 不为空时才有效。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetVector):
        raise ValueError('source input_data must be DatasetVector')
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_Smooth'
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        result = out_datasource.copy_dataset(_source_input, _outDatasetName, None, progress=progress)
        if result is None:
            raise RuntimeError('Failed to copy dataset ' + _source_input.name)
        _source_input = result
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'smooth_vector')
                _source_input._jobject.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            is_success = _source_input._jobject.smooth(int(smoothness), listener is not None)
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _source_input._jobject.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if not is_success:
            _source_input = None
        if out_data is not None:
            return try_close_output_datasource(_source_input, out_datasource)
        return _source_input


def resample_vector(input_data, distance, resample_type=VectorResampleType.RTBEND, is_preprocess=True, tolerance=1e-10, is_save_small_geometry=False, out_data=None, out_dataset_name=None, progress=None):
    """
    对矢量数据集进行重采样，支持线数据集、面数据集和网络数据集。 矢量数据重采样是按照一定规则剔除一些节点，以达到对数据进行简化的目的（如下图所示），
    其结果可能由于使用不同的重采样方法而不同。SuperMap 提供了两种重采样方法，具体参考 :py:class:`.VectorResampleType`

    .. image:: ../image/VectorResample.png

    该方法可以对线数据集、面数据集和网络数据集进行重采样。对面数据集重采样时，实质是对面对象的边界进行重采样。对于多个面对象的公共边界，如果进行了
    拓扑预处理只对其中一个多边形的该公共边界重采样一次，其他多边形的该公共边界会依据该多边形重采样的结果进行调整使之贴合，因此不会出现缝隙。

    注意: 重采样容限过大时，可能影响数据正确性，如出现两多边形的公共边界处出现相交的情况。

    :param input_data: 需要进行重采样的矢量数据集，支持线数据集、面数据集和网络数据集
    :type input_data: DatasetVector or str
    :param float distance: 设置重采样距离。单位与数据集坐标系单位相同。重采样距离可设置为大于 0 的浮点型数值。但如果设置的值小于默认值，将使用默认值。设置的重采样容限值越大，采样结果数据越简化
    :param resample_type: 重采样方法。重采样支持光栏采样算法和道格拉斯算法。具体参考 :py:class:`.VectorResampleType` 。默认使用光栏采样。
    :type resample_type: VectorResampleType or str
    :param bool is_preprocess: 是否进行拓扑预处理。只对面数据集有效，如果数据集不进行拓扑预处理，可能会导致缝隙，除非能确保数据中两个相邻面公共线部分的节点坐标完全一致。
    :param float tolerance: 进行拓扑预处理时的节点捕捉容限，单位与数据集单位相同。
    :param bool is_save_small_geometry: 是否保留小对象。小对象是指面积为0的对象，重采样过程有可能产生小对象。true 表示保留小对象，false 表示不保留。
    :param out_data: 结果数据源所在半径，如果此参数为空，将直接对原始数据做采样，也就是会改变原始数据。如果此参数不为空，将会先复制原始数据到此数据源中，
                     再对复制得到的数据集进行采样处理。out_data 所指向数据源可以与源数据集所在的数据源相同。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称，当 out_data 不为空时才有效。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetVector):
        raise ValueError('source input_data must be DatasetVector')
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_resample'
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        result = out_datasource.copy_dataset(_source_input, _outDatasetName, None, progress=progress)
        if result is None:
            raise RuntimeError('Failed to copy dataset ' + _source_input.name)
        _source_input = result
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'resample_vector')
                _source_input._jobject.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            resample_parameter = get_jvm().com.supermap.data.ResampleInformation()
            resample_parameter.setResampleType(VectorResampleType._make(resample_type, VectorResampleType.RTBEND)._jobject)
            resample_parameter.setTolerance(float(distance))
            resample_parameter.setTopologyPreprocess(bool(is_preprocess))
            resample_parameter.setVertexInterval(float(tolerance))
            is_success = _source_input._jobject.resample(resample_parameter, listener is not None, bool(is_save_small_geometry))
            resample_parameter.dispose()
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _source_input._jobject.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if not is_success:
            _source_input = None
        if out_data is not None:
            return try_close_output_datasource(_source_input, out_datasource)
        return _source_input


def create_thiessen_polygons(input_data, clip_region, field_stats=None, out_data=None, out_dataset_name=None, progress=None):
    """
    创建泰森多边形。
    荷兰气候学家 A.H.Thiessen 提出了一种根据离散分布的气象站的降雨量来计算平均降雨量的方法，即将所有相邻气象站连成三角形，作这些三角形各边的垂直平分线，
    于是每个气象站周围的若干垂直平分线便围成一个多边形。用这个多边形内所包含的一个唯一气象站的降雨强度来表示这个多边形区域内的降雨强度，并称这个多边形为泰森多边形。

    泰森多边形的特性:

        - 每个泰森多边形内仅含有一个离散点数据；
        - 泰森多边形内的点到相应离散点的距离最近；
        - 位于泰森多边形边上的点到其两边的离散点的距离相等。
        - 泰森多边形可用于定性分析、统计分析、邻近分析等。例如，可以用离散点的性质来描述泰森多边形区域的性质；可用离散点的数据来计算泰森多边形区域的数据
        - 判断一个离散点与其它哪些离散点相邻时，可根据泰森多边形直接得出，且若泰森多边形是n边形，则就与n个离散点相邻；当某一数据点落入某一泰森多边形中时，它与相应的离散点最邻近，无需计算距离。

    邻近分析是 GIS 领域里又一个最为基础的分析功能之一，邻近分析是用来发现事物之间的某种邻近关系。邻近分析类所提供的进行邻近分析的方法都是实现泰森多边形的建立，
    就是根据所提供的点数据建立泰森多边形，从而获得点之间的邻近关系。泰森多边形用于将点集合中的点的周围区域分配给相应的点，使位于这个点所拥有的区域（即该点所关联的泰森多边形）
    内的任何地点离这个点的距离都要比离其他点的距离要小，同时，所建立的泰森多边形还满足上述所有的泰森多边形法的理论。

    泰森多边形是如何创建的？利用下面的图示来理解泰森多边形建立的过程：

        - 对待建立泰森多边形的点数据进行由左向右，由上到下的扫描，如果某个点距离之前刚刚扫描过的点的距离小于给定的邻近容限值，那么分析时将忽略该点；
        - 基于扫描检查后符合要求的所有点建立不规则三角网，即构建 Delaunay 三角网；
        - 画出每个三角形边的中垂线，由这些中垂线构成泰森多边形的边，而中垂线的交点是相应的泰森多边形的顶点；
        - 用于建立泰森多边形的点的点位将成为相应的泰森多边形的锚点。

    :param input_data: 输入的点数据，可以为点数据集、点记录集或 :py:class:`.Point2D` 的列表
    :type input_data: DatasetVector or Recordset or list[Point2D]
    :param GeoRegion clip_region:  指定的裁剪结果数据的裁剪区域。该参数可以为空，如果为空，结果数据集将不进行裁剪
    :param field_stats:  统计字段名称和对应的统计类型，输入为一个list，list中存储的每个元素为tuple，tuple的大小为2，第一个元素为被统计的字段名称，第二个元素为统计类型。
                         当 stats_fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1:SUM, field2:MAX, field3:MIN"
    :type field_stats: list[str,StatisticsType] or list[str,str] or str
    :param out_data: 结果面对象所在的数据源。如果 out_data 为空，则会将生成的泰森多边形面几何对象直接返回
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称，当 out_data 不为空时才有效。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 如果 out_data 为空，将返回 list[GeoRegion]，否则返回结果数据集或数据集名称。
    :rtype: DatasetVector or str or list[GeoRegion]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    _jvm = get_jvm()
    points = None
    if isinstance(_source_input, (list, set, tuple)):
        points = _jvm.com.supermap.data.Point2Ds()
        for p in _source_input:
            p = Point2D.make(p)
            if isinstance(p, Point2D):
                points.add(p._jobject)

    else:
        if isinstance(_source_input, (DatasetVector, Recordset)):
            pass
        else:
            raise ValueError('Create thiessen polygon only support DatasetVector, Recordset and list points for input_data')
        fields = None
        statTypes = None
        if field_stats is not None:
            field_stats = split_input_list_tuple_item_from_str(field_stats)
            if isinstance(field_stats, list):
                fields = []
                statTypes = []
                for name, stat_type in field_stats:
                    fields.append(name)
                    statTypes.append(StatisticsType._make(stat_type))

        listener = None
        if progress is not None and safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'create_thiessen_polygons')
                _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

            if clip_region is not None:
                java_clip_region = clip_region._jobject
            else:
                java_clip_region = None
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                check_output_datasource(out_datasource)
                _jvm = get_jvm()
                if out_dataset_name is None:
                    _outDatasetName = 'ThiessenPolygon'
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        try:
            try:
                if points is not None:
                    java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(points, out_datasource._jobject, _outDatasetName, java_clip_region)
                else:
                    if fields is None or statTypes is None:
                        java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(_source_input._jobject, out_datasource._jobject, _outDatasetName, java_clip_region)
                    else:
                        java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(_source_input._jobject, out_datasource._jobject, _outDatasetName, java_clip_region, to_java_string_array(fields), to_java_stattype_array(statTypes))
            except Exception as e:
                try:
                    log_error(e)
                    java_result_dt = None
                finally:
                    e = None
                    del e

        finally:
            if listener is not None:
                try:
                    _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            elif java_result_dt is not None:
                result_dt = out_datasource[java_result_dt.getName()]
            else:
                result_dt = None
            return try_close_output_datasource(result_dt, out_datasource)
            try:
                try:
                    if points is not None:
                        regions = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(points, java_clip_region)
                    else:
                        regions = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(_source_input._jobject, java_clip_region)
                except Exception as e:
                    try:
                        log_error(e)
                        regions = None
                    finally:
                        e = None
                        del e

            finally:
                return

            if listener is not None:
                try:
                    _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            if regions is not None:
                return list(map(lambda geo: Geometry._from_java_object(geo), regions))
            return


def summary_points(input_data, radius, unit=None, stats=None, is_random_save_point=False, is_save_attrs=False, out_data=None, out_dataset_name=None, progress=None):
    """
    根据指定的距离抽稀点数据集，即用一个点表示指定距离范围内的所有点。 该方法支持不同的单位，并且可以选择点抽稀的方式，还可以对抽稀点原始点集做统计。
    在结果数据集 resultDatasetName 中，会新建SourceObjID 和 StatisticsObjNum 两个字段。SourceObjID 字段存储抽稀后得到的点对象在原始数据集
    中的 SmID, StatisticsObjNum 表示当前点所代表的所有点数目，包括被抽稀的点和其自身。

    :param input_data: 待抽稀的点数据集
    :type input_data: DatasetVector or str or Recordset
    :param float radius:  抽稀点的半径。任取一个坐标点，在此坐标点半径内的所有点坐标通过此点表示。需注意选择抽稀点的半径的单位。
    :param unit: 抽稀点半径的单位。
    :type unit: Unit or str
    :param stats: 对抽稀点原始点集做统计。需要设置统计的字段名，统计结果的字段名和统计模式。当该数组为空表示不做统计。当 stats 为 str 时，支持设置以 ';'
                  分隔多个 StatisticsField，每个 StatisticsField 使用 ',' 分隔 'source_field,stat_type,result_name'，例如：
                  'field1,AVERAGE,field1_avg; field2,MINVALUE,field2_min'
    :type stats: list[StatisticsField] or str
    :param bool is_random_save_point:  是否随机保存抽稀点。True表示从抽稀半径范围内的点集中随机取一个点保存，False表示取抽稀半径范围内点集中距点集内所有点的距离之和最小的点。
    :param bool is_save_attrs: 是否保留属性字段
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, (DatasetVector, Recordset)):
            raise ValueError('source input_data must be DatasetVector or Recordset')
        else:
            if radius < 0:
                raise ValueError('radius must be greater 0')
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            if isinstance(_source_input, Recordset):
                _outDatasetName = _source_input.dataset.name + '_summary'
            else:
                _outDatasetName = _source_input.name + '_summary'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'summary_points')
                _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            statFields = []
            if stats is not None:
                if isinstance(stats, StatisticsField):
                    statFields.append(stats._jobject)
                else:
                    if isinstance(stats, (list, tuple, set)):
                        for item in stats:
                            if isinstance(item, StatisticsField):
                                statFields.append(item._jobject)

                    else:
                        if isinstance(stats, str):
                            tokens = stats.split(';')
                            for token in tokens:
                                keys = token.split(',')
                                if len(keys) == 3:
                                    statFields.append(StatisticsField(str(keys[0]), str(keys[1]), str(keys[2]))._jobject)

                        else:
                            raise ValueError('invalid stats type, required StatisticsField, (list,tuple,set of StatisticsField) or str')
            java_statFields = get_gateway().new_array(_jvm.com.supermap.analyst.spatialanalyst.StatisticsField, len(statFields))
            i = 0
            for item in statFields:
                java_statFields[i] = item
                i += 1

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.summaryPoints_source_input._jobjectfloat(radius)Unit._make(unit, Unit.METER)._jobjectjava_statFields_ds._jobject_outDatasetNamebool(is_random_save_point)bool(is_save_attrs)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def clip_vector(input_data, clip_region, is_clip_in_region=True, is_erase_source=False, out_data=None, out_dataset_name=None, progress=None):
    """
    对矢量数据集进行裁剪，结果存储为一个新的矢量数据集。

    :param input_data: 指定的要进行裁剪的矢量数据集，支持点、线、面、文本、CAD 数据集。
    :type input_data: DatasetVector or str
    :param GeoRegion  clip_region: 指定的裁剪区域
    :param bool is_clip_in_region: 指定是否对裁剪区内的数据集进行裁剪。若为 True，则对裁剪区域内的数据集进行裁剪，若为 False ，则对裁剪区域外的数据集进行裁剪。
    :param bool is_erase_source: 指定是否擦除裁剪区域，若为 True，表示对裁剪区域进行擦除，若为 False，则不对裁剪区域进行擦除。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        else:
            if clip_region is None:
                raise ValueError('clip_region is None')
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = input_data.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_clip'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'clip_datasetvector')
                _jvm.com.supermap.analyst.spatialanalyst.VectorClip.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.VectorClip.clipDatasetVector(_source_input._jobject, clip_region._jobject, bool(is_clip_in_region), bool(is_erase_source), _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.VectorClip.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class ProcessingOptions(object):
    __doc__ = '\n    拓扑处理参数类。该类提供了关于拓扑处理的设置信息。\n\n    如果未通过 set_vertex_tolerance,set_overshoots_tolerance 和 set_undershoots_tolerance 方法设置节点容限、短悬线容限和长悬线容限，\n    或设置为0，系统将使用数据集的容限中相应的容限值进行处理\n\n    '

    def __init__(self, pseudo_nodes_cleaned=False, overshoots_cleaned=False, redundant_vertices_cleaned=False, undershoots_extended=False, duplicated_lines_cleaned=False, lines_intersected=False, adjacent_endpoints_merged=False, overshoots_tolerance=1e-10, undershoots_tolerance=1e-10, vertex_tolerance=1e-10, filter_vertex_recordset=None, arc_filter_string=None, filter_mode=None):
        """
        构造拓扑处理参数类

        :param bool pseudo_nodes_cleaned: 是否去除假结点
        :param bool overshoots_cleaned: 是否去除短悬线。
        :param bool redundant_vertices_cleaned: 是否去除冗余点
        :param bool undershoots_extended: 是否进行长悬线延伸。
        :param bool duplicated_lines_cleaned: 是否去除重复线
        :param bool lines_intersected: 是否进行弧段求交。
        :param bool adjacent_endpoints_merged: 是否进行邻近端点合并。
        :param float overshoots_tolerance:  短悬线容限，该容限用于在去除短悬线时判断悬线是否是短悬线。
        :param float undershoots_tolerance: 长悬线容限，该容限用于在长悬线延伸时判断悬线是否延伸。单位与进行拓扑处理的数据集单位相同。
        :param float vertex_tolerance: 节点容限。该容限用于邻近端点合并、弧段求交、去除假结点和去除冗余点。单位与进行拓扑处理的数据集单位相同。
        :param Recordset filter_vertex_recordset: 弧段求交的过滤点记录集，即此记录集中的点位置线段不进行求交打断。
        :param str arc_filter_string: 弧段求交的过滤线表达式。 在进行弧段求交时，通过该属性可以指定一个字段表达式，符合该表达式的线对象将不被打断。
                                      该表达式是否有效，与 filter_mode 弧段求交过滤模式有关
        :param filter_mode: 弧段求交的过滤模式。
        :type filter_mode: ArcAndVertexFilterMode or str
        """
        self._pseudo_nodes_cleaned = True
        self._overshoots_cleaned = True
        self._redundant_vertices_cleaned = True
        self._undershoots_extended = True
        self._duplicated_lines_cleaned = True
        self._lines_intersected = True
        self._adjacent_endpoints_merged = True
        self._overshoots_tolerance = 0.0
        self._undershoots_tolerance = 0.0
        self._vertex_tolerance = 0.0
        self._filter_vertex_recordset = None
        self._arc_filter_string = None
        self._filter_mode = None
        self.set_pseudo_nodes_cleaned(pseudo_nodes_cleaned).set_overshoots_cleaned(overshoots_cleaned).set_overshoots_tolerance(overshoots_tolerance).set_redundant_vertices_cleaned(redundant_vertices_cleaned).set_undershoots_extended(undershoots_extended).set_undershoots_tolerance(undershoots_tolerance).set_duplicated_lines_cleaned(duplicated_lines_cleaned).set_lines_intersected(lines_intersected).set_adjacent_endpoints_merged(adjacent_endpoints_merged).set_vertex_tolerance(vertex_tolerance).set_filter_vertex_recordset(filter_vertex_recordset).set_arc_filter_string(arc_filter_string).set_filter_mode(filter_mode)

    @property
    def pseudo_nodes_cleaned(self):
        """bool: 是否去除假结点"""
        return self._pseudo_nodes_cleaned

    @property
    def overshoots_cleaned(self):
        """bool:  是否去除短悬线"""
        return self._overshoots_cleaned

    @property
    def redundant_vertices_cleaned(self):
        """bool: 是否去除冗余点"""
        return self._redundant_vertices_cleaned

    @property
    def undershoots_extended(self):
        """bool: 是否进行长悬线延伸"""
        return self._undershoots_extended

    @property
    def duplicated_lines_cleaned(self):
        """bool: 是否去除重复线"""
        return self._duplicated_lines_cleaned

    @property
    def lines_intersected(self):
        """bool: 是否进行弧段求交"""
        return self._lines_intersected

    @property
    def adjacent_endpoints_merged(self):
        """bool: 是否进行邻近端点合并"""
        return self._adjacent_endpoints_merged

    @property
    def overshoots_tolerance(self):
        """float: 短悬线容限，该容限用于在去除短悬线时判断悬线是否是短悬线"""
        return self._overshoots_tolerance

    @property
    def undershoots_tolerance(self):
        """float: 长悬线容限，该容限用于在长悬线延伸时判断悬线是否延伸。单位与进行拓扑处理的数据集单位相同"""
        return self._undershoots_tolerance

    @property
    def vertex_tolerance(self):
        """float: 节点容限。该容限用于邻近端点合并、弧段求交、去除假结点和去除冗余点。单位与进行拓扑处理的数据集单位相同"""
        return self._vertex_tolerance

    @property
    def filter_vertex_recordset(self):
        """Recordset: 弧段求交的过滤点记录集，即此记录集中的点位置线段不进行求交打断"""
        return self._filter_vertex_recordset

    @property
    def arc_filter_string(self):
        """str:  弧段求交的过滤线表达式。 在进行弧段求交时，通过该属性可以指定一个字段表达式，符合该表达式的线对象将不被打断。该表达式是否有效，与 filter_mode 弧段求交过滤模式有关"""
        return self._arc_filter_string

    @property
    def filter_mode(self):
        """ArcAndVertexFilterMode: 弧段求交的过滤模式"""
        return self._filter_mode

    def set_pseudo_nodes_cleaned(self, value):
        """
        设置是否去除假结点。结点又称为弧段连接点，至少连接三条弧段的才可称为一个结点。如果弧段连接点只连接了一条弧段（岛屿的情况）或连接了两条弧段（即它是两条弧段的公共端点），则该结点被称为假结点

        :param bool value: 是否去除假结点，True 表示去除，False 表示不去除。
        :return: ProcessingOptions
        :rtype: self
        """
        self._pseudo_nodes_cleaned = bool(value)
        return self

    def set_overshoots_cleaned(self, value):
        """
        设置是否去除短悬线。去除短悬线指如果一条悬线的长度小于悬线容限，则在进行去除短悬线操作时就会把这条悬线删除。通过 set_overshoots_tolerance 方法可以指定短悬线容限，如不指定则使用数据集的短悬线容限。

        悬线：如果一个线对象的端点没有与其它任意一个线对象的端点相连，则这个端点称之为悬点。具有悬点的线对象称之为悬线。

        :param bool value: 是否去除短悬线，True 表示去除，False 表示不去除。
        :return: ProcessingOptions
        :rtype: self
        """
        self._overshoots_cleaned = bool(value)
        return self

    def set_redundant_vertices_cleaned(self, value):
        """
        设置是否去除冗余点。任意弧段上两节点之间的距离小于节点容限时，其中一个即被认为是一个冗余点，在进行拓扑处理时可以去除。

        :param bool value: : 是否去除冗余点，True 表示去除，False 表示不去除。
        :return: ProcessingOptions
        :rtype: self
        """
        self._redundant_vertices_cleaned = bool(value)
        return self

    def set_undershoots_extended(self, value):
        """
        设置是否进行长悬线延伸。 如果一条悬线按其行进方向延伸了指定的长度（悬线容限）之后与某弧段有交点，则拓扑处理后会将该悬线自动延伸到某弧段上，
        称为长悬线延伸。通过 set_undershoots_tolerance 方法可以指定长悬线容限，如不指定则使用数据集的长悬线容限。

        :param bool value:  是否进行长悬线延伸
        :return: ProcessingOptions
        :rtype: self
        """
        self._undershoots_extended = bool(value)
        return self

    def set_duplicated_lines_cleaned(self, value):
        """
        设置是否去除重复线

        重复线：两条弧段若其所有节点两两重合，则可认为是重复线。重复线的判断不考虑方向。

        去除重复线的目的是为避免建立拓扑多边形时产生面积为零的多边形对象，因此，重复的线对象只应保留其中一个，多余的应删除。

        通常，出现重复线多是由于弧段求交造成的。

        :param bool value: 是否去除重复线
        :return: ProcessingOptions
        :rtype: self
        """
        self._duplicated_lines_cleaned = bool(value)
        return self

    def set_lines_intersected(self, value):
        """
        设置是否进行弧段求交。

        线数据建立拓扑关系之前，首先要进行弧段求交计算，根据交点分解成若干线对象，一般而言，在二维坐标系统中凡是与其他线有交点的线对象都需要从交点处打断，如十字路口。且此方法是后续错误处理方法的基础。
        在实际应用中，相交线段完全打断的处理方式在很多时候并不能很好地满足研究需求。例如，一条高架铁路横跨一条公路，在二维坐标上来看是两个相交的线对象，但事实上并没有相交
        ，如果打断将可能影响进一步的分析。在交通领域还有很多类似的实际场景，如河流水系与交通线路的相交，城市中错综复杂的立交桥等，对于某些相交点是否打断，
        需要根据实际应用来灵活处理，而不能因为在二维平面上相交就一律打断。

        这种情况可以通过设置过滤线表达式（ :py:meth:`set_arc_filter_string` ）和过滤点记录集 ( :py:meth:`set_vertex_filter_recordset` ) 来
        确定哪些线对象以及哪些相交位置处不打断:

          - 过滤线表达式用于查询出不需要打断的线对象
          - 过滤点记录集中的点对象所在位置处不打断

        这两个参数单独或组合使用构成了弧段求交的四种过滤模式，还有一种是不进行过滤。过滤模式通过 :py:meth:`set_filter_mode` 方法设置。对于上面的例子，使用不同的过滤模式，弧段求交的结果也不相同。关于过滤模式的详细介绍请参阅 :py:class:`.ArcAndVertexFilterMode` 类。

        注意：进行弧段求交处理时，可通过 :py:meth:`set_vertex_tolerance` 方法设置节点容限（如不设置，将使用数据集的节点容限），用于判断过滤点是否有效。若过滤点到线对象的距离在设置的容限范围内，则线对象在过滤点到其的垂足位置上不被打断。

        :param bool value: 是否进行弧段求交
        :return: ProcessingOptions
        :rtype: self
        """
        self._lines_intersected = bool(value)
        return self

    def set_adjacent_endpoints_merged(self, value):
        """
        设置是否进行邻近端点合并。

        如果多条弧段端点的距离小于节点容限，那么这些点就会被合并成为一个结点，该结点位置是原有点的几何平均（即 X、Y 分别为所有原有点 X、Y 的平均值）。

        用于判断邻近端点的节点容限，可通过\u3000:py:meth:`set_vertex_tolerance` 设置，如果不设置或设置为0，将使用数据集的容限中的节点容限。

        需要注意的是，如果有两个邻近端点，那么合并的结果就会是一个假结点，还需要进行去除假结点的操作。

        :param bool value: 是否进行邻近端点合并
        :return: ProcessingOptions
        :rtype: self
        """
        self._adjacent_endpoints_merged = bool(value)
        return self

    def set_overshoots_tolerance(self, value):
        """
        设置短悬线容限，该容限用于在去除短悬线时判断悬线是否是短悬线。单位与进行拓扑处理的数据集单位相同。

        “悬线”的定义：如果一个线对象的端点没有与其它任意一个线对象的端点相连，则这个端点称之为悬点。具有悬点的线对象称之为悬线。

        :param float value:  短悬线容限
        :return: ProcessingOptions
        :rtype: self
        """
        self._overshoots_tolerance = float(value)
        return self

    def set_undershoots_tolerance(self, value):
        """
        设置长悬线容限，该容限用于在长悬线延伸时判断悬线是否延伸。单位与进行拓扑处理的数据集单位相同。

        :param float value: 长悬线容限
        :return: ProcessingOptions
        :rtype: self
        """
        self._undershoots_tolerance = float(value)
        return self

    def set_vertex_tolerance(self, value):
        """
        设置节点容限。该容限用于邻近端点合并、弧段求交、去除假结点和去除冗余点。单位与进行拓扑处理的数据集单位相同。

        :param float value: 节点容限
        :return: ProcessingOptions
        :rtype: self
        """
        self._vertex_tolerance = float(value)
        return self

    def set_filter_vertex_recordset(self, value):
        """
        设置弧段求交的过滤点记录集，即此记录集中的点位置线段不进行求交打断。

        如果过滤点在线对象上或到线对象的距离在容限范围内，在过滤点到线对象的垂足位置上线对象不被打断。详细介绍请参见 :py:meth:`set_lines_intersected` 方法。

        注意：过滤点记录集是否有效，与 :py:meth:`set_filter_mode` 方法设置的弧段求交过滤模式有关。可参见 :py:class:`.ArcAndVertexFilterMode` 类。

        :param Recordset value:
        :return: ProcessingOptions
        :rtype: self
        """
        if value is not None:
            if not isinstance(value, Recordset):
                raise ValueError('FilterVertexRecordset value must be Recordset')
        self._filter_vertex_recordset = value
        return self

    def set_arc_filter_string(self, value):
        """
        设置弧段求交的过滤线表达式。

        在进行弧段求交时，通过该属性可以指定一个字段表达式，符合该表达式的线对象将不被打断。详细介绍请参见 :py:meth:`set_lines_intersected`  方法。

        :param str value:
        :return: ProcessingOptions
        :rtype: self
        """
        self._arc_filter_string = value
        return self

    def set_filter_mode(self, value):
        """
        设置弧段求交的过滤模式

        :param value: 弧段求交的过滤模式
        :type value: ArcAndVertexFilterMode
        :return: ProcessingOptions
        :rtype: self
        """
        self._filter_mode = ArcAndVertexFilterMode._make(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 端的对象"""
        jvm = get_jvm()
        java_options = jvm.com.supermap.data.topology.TopologyProcessingOptions()
        java_options.setAdjacentEndpointsMerged(self.adjacent_endpoints_merged)
        java_options.setDuplicatedLinesCleaned(self.duplicated_lines_cleaned)
        java_options.setLinesIntersected(self.lines_intersected)
        java_options.setOvershootsCleaned(self.overshoots_cleaned)
        java_options.setPseudoNodesCleaned(self.pseudo_nodes_cleaned)
        java_options.setRedundantVerticesCleaned(self.redundant_vertices_cleaned)
        java_options.setUndershootsExtended(self.undershoots_extended)
        java_options.setOvershootsTolerance(self.overshoots_tolerance)
        java_options.setUndershootsTolerance(self.undershoots_tolerance)
        java_options.setVertexTolerance(self.vertex_tolerance)
        if self.filter_vertex_recordset is not None:
            java_options.setVertexFilterRecordset(self.filter_vertex_recordset._jobject)
        if self.filter_mode is not None:
            java_options.setFilterMode(self.filter_mode._jobject)
        if self.arc_filter_string is not None:
            java_options.setArcFilterString(self.arc_filter_string)
        return java_options


def topology_processing(input_data, pseudo_nodes_cleaned=True, overshoots_cleaned=True, redundant_vertices_cleaned=True, undershoots_extended=True, duplicated_lines_cleaned=True, lines_intersected=True, adjacent_endpoints_merged=True, overshoots_tolerance=1e-10, undershoots_tolerance=1e-10, vertex_tolerance=1e-10, filter_vertex_recordset=None, arc_filter_string=None, filter_mode=None, options=None, progress=None):
    """
    根据拓扑处理选项对给定的数据集进行拓扑处理。将直接修改原始数据。

    :param input_data: 指定的拓扑处理的数据集。
    :type input_data: DatasetVector or str
    :param bool pseudo_nodes_cleaned: 是否去除假结点
    :param bool overshoots_cleaned: 是否去除短悬线。
    :param bool redundant_vertices_cleaned: 是否去除冗余点
    :param bool undershoots_extended: 是否进行长悬线延伸。
    :param bool duplicated_lines_cleaned: 是否去除重复线
    :param bool lines_intersected: 是否进行弧段求交。
    :param bool adjacent_endpoints_merged: 是否进行邻近端点合并。
    :param float overshoots_tolerance:  短悬线容限，该容限用于在去除短悬线时判断悬线是否是短悬线。
    :param float undershoots_tolerance: 长悬线容限，该容限用于在长悬线延伸时判断悬线是否延伸。单位与进行拓扑处理的数据集单位相同。
    :param float vertex_tolerance: 节点容限。该容限用于邻近端点合并、弧段求交、去除假结点和去除冗余点。单位与进行拓扑处理的数据集单位相同。
    :param Recordset filter_vertex_recordset: 弧段求交的过滤点记录集，即此记录集中的点位置线段不进行求交打断。
    :param str arc_filter_string: 弧段求交的过滤线表达式。 在进行弧段求交时，通过该属性可以指定一个字段表达式，符合该表达式的线对象将不被打断。
                                  该表达式是否有效，与 filter_mode 弧段求交过滤模式有关
    :param filter_mode: 弧段求交的过滤模式。
    :type filter_mode: ArcAndVertexFilterMode or str
    :param options: 拓扑处理参数类，如果 options 不为空，拓扑处理将会使用此参数设置的值。
    :type options: ProcessingOptions or None
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 是否拓扑处理成功
    :rtype: bool
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        _jvm = get_jvm()
        if options is not None:
            java_option = options._jobject
        else:
            java_option = ProcessingOptions(pseudo_nodes_cleaned, overshoots_cleaned, redundant_vertices_cleaned, undershoots_extended, duplicated_lines_cleaned, lines_intersected, adjacent_endpoints_merged, overshoots_tolerance, undershoots_tolerance, vertex_tolerance, filter_vertex_recordset, arc_filter_string, filter_mode)._jobject
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'TopologyBuildRegions')
                _jvm.com.supermap.data.topology.TopologyProcessing.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            is_success = _jvm.com.supermap.data.topology.TopologyProcessing.clean(_source_input._jobject, java_option)
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.data.topology.TopologyProcessing.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return is_success


def topology_build_regions(input_data, out_data=None, out_dataset_name=None, progress=None):
    """
    用于将线数据集或者网络数据集，通过拓扑处理来构建面数据集。在进行拓扑构面前，最好能使用拓扑处理 :py:meth:`topology_processing` 对数据集进行拓扑处理。

    :param input_data: 指定的用于进行多边形拓扑处理的源数据集，只能是线数据集或网络数据集。
    :type input_data: DatasetVector or str
    :param out_data: 用于存储结果数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = input_data.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_region'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'TopologyBuildRegions')
                _jvm.com.supermap.data.topology.TopologyProcessing.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.data.topology.TopologyProcessing.buildRegions(_source_input._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyProcessing.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def pickup_border(input_data, is_preprocess=True, extract_ids=None, out_data=None, out_dataset_name=None, progress=None):
    """
    提取面（或线）的边界，并保存为线数据集。若多个面（或线）共边界（线段），该边界（线段）只会被提取一次。

    不支持重叠面提取边界。

    :param input_data: 指定的面或线数据集。
    :type input_data: DatasetVector or str
    :param bool is_preprocess: 是否进行拓扑预处理
    :param extract_ids:  指定的面ID数组，可选参数，仅会提取给定ID数组对应的面对象边界。
    :type extract_ids: list[int] or str
    :param out_data: 用于存储结果数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = input_data.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_border'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'PickupBorder')
                _jvm.com.supermap.data.topology.TopologyProcessing.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            pickupBorder = get_jvm().com.supermap.data.topology.TopologyProcessing.pickupBorder
            if extract_ids is None:
                java_result_dt = pickupBorderoj(_source_input)oj(_ds)_outDatasetNamebool(is_preprocess)
            else:
                extract_ids = to_java_int_array(split_input_list_from_str(extract_ids))
                java_result_dt = pickupBorder(oj(_source_input), oj(_ds), _outDatasetName, extract_ids, bool(is_preprocess))
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyProcessing.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def simplify_building(source_data, width_threshold, height_threshold, save_failed=False, out_data=None, out_dataset_name=None):
    """
    面对象的直角多边形拟合
    如果一串连续的节点到最小面积外接矩形的下界的距离大于 height_threshold，且节点的总宽度大于 width_threshold，则对连续节点进行拟合。

    :param source_data: 需要处理的面数据集
    :type source_data: DatasetVector or str
    :param float width_threshold: 点到最小面积外接矩形的左右边界的阈值
    :param float height_threshold: 点到最小面积外接矩形的上下边界的阈值
    :param bool save_failed: 面对象进行直角化失败时，是否保存源面对象，如果为 False，则结果数据集中不含失败的面对象。
    :param out_data: 用于存储结果数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果数据集或数据集名称
    :rtype:  DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(source_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetVector):
        raise ValueError('source input_data must be DatasetVector')
    if not width_threshold > 0:
        raise ValueError('width_threshold must be greater than 0')
    else:
        if not height_threshold > 0:
            raise ValueError('height_threshold must be greater than 0')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = source_data.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_simplify'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    try:
        try:
            java_result_dt = get_jvm().com.supermap.jsuperpy.Utils.simplifyBuilding(oj(_source_input), oj(_ds), _outDatasetName, float(width_threshold), float(height_threshold), not save_failed)
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                java_result_dt = False
            finally:
                e = None
                del e

    finally:
        if java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def update_attributes(source_data, target_data, spatial_relation, update_fields, interval=1e-06):
    """
    矢量数据集属性更新，将 source_data 中的属性，根据 spatial_relation 指定的空间关系，更新到 target_data 数据集中。
    例如，有一份点数据和面数据，需要将点数据集中的属性值取平均值，然后将值写到包含点的面对象中，可以通过以下代码实现::

    >>> result = update_attributes('ds/points', 'ds/zones', 'WITHIN', [('trip_distance', 'mean'), ('', 'count')])

    spatial_relation 参数是指源数据集（ source_data）对目标被更新数据集（target_data）的空间关系。

    :param source_data: 源数据集。源数据集提供属性数据，将源数据集中的属性值根据空间关系更新到目标数据集中。
    :type source_data:  DatasetVector or str
    :param target_data: 目标数据集。被写入属性数据的数据集。
    :type target_data: DatasetVector or str
    :param spatial_relation: 空间关系类型，源数据（查询对象）对目标数据（被查询对象）的空间关系，具体参考 :py:class:`SpatialQueryMode`
    :type spatial_relation: SpatialQueryMode or str
    :param update_fields: 字段统计信息，可能有多个源数据中对象与目标数据对象满足空间关系，需要对源数据的属性字段值进行汇总统计，将统计的结果写入到目标数据集中
                          为一个list，list中每个元素为一个 tuple，tuple的大小为2，tuple的第一个元素为被统计的字段名称，tuple的第二个元素为统计类型。
    :type update_fields: list[tuple(str,AttributeStatisticsMode)] or list[tuple(str,str)] or str
    :param interval: 节点容限
    :type interval: float
    :return: 是否属性更新成功。更新成功返回 True，否则返回 False。
    :rtype: bool
    """
    check_lic()
    _updated_input = get_input_dataset(target_data)
    if not isinstance(_updated_input, DatasetVector):
        raise ValueError('target_data must be DatasetVector, but is ' + str(type(target_data)))
    _attribute_input = get_input_dataset(source_data)
    if not isinstance(_attribute_input, DatasetVector):
        raise ValueError('source_data must be DatasetVector, but is ' + str(type(source_data)))
    spatial_relation = SpatialQueryMode._make(spatial_relation)
    stat_fields = None
    stat_modes = None
    if update_fields is not None:
        stats = split_input_list_tuple_item_from_str(update_fields)
        if isinstance(stats, list):
            stat_fields = []
            stat_modes = []
            for name, stat_mode in stats:
                stat_mode = AttributeStatisticsMode._make(stat_mode)
                if stat_mode is not None and stat_mode is not AttributeStatisticsMode.MAXINTERSECTAREA:
                    stat_fields.append(name)
                    stat_modes.append(oj(stat_mode))

    try:
        try:
            result = get_jvm().com.supermap.jsuperpy.UpdateAttributes.updateAttributes(oj(_attribute_input), oj(_updated_input), oj(spatial_relation), stat_fields, stat_modes, interval)
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                result = False
            finally:
                e = None
                del e

    finally:
        return

    return result


def split_lines_by_regions(line_input, region_input, progress=None):
    """
    用面对象分割线对象。在提取线对象的左右多边形（即 pickupLeftRightRegions() 方法）操作前，需要调用该方法分割线对象，否则会出现一个线对象对应多个左（右）多边形的情形。
    如下图：线对象 AB，如果不用面对象进行分割，则 AB 的左多边形有两个，分别为1，3；右多边形也有两个，分别为1和3，进行分割操作后，线对象 AB 分割为 AC 与 CB，此时 AC 与 CB 各自对应的左、右多边形分别只有一个。

    .. image:: ../image/SplitLinesByRegions.png

    :param line_input:  指定的被分割的线记录集或数据集。
    :type line_input: DatasetVector or Recordset
    :param region_input: 指定的用于分割线记录集的面记录集或数据集。
    :type region_input: DatasetVector or Recordset
    :param function progress:
    :return: 成功返回 True，失败返回 False。
    :rtype: bool
    """
    _line_input = get_input_dataset(line_input)
    if _line_input is None:
        raise ValueError('lineInput is None')
    if not isinstance(_line_input, (DatasetVector, Recordset)):
        raise ValueError('lineInput must be DatasetVector or Recordset')
    _region_input = get_input_dataset(region_input)
    if _region_input is None:
        raise ValueError('regionInput is None')
    else:
        if not isinstance(_line_input, (DatasetVector, Recordset)):
            raise ValueError('regionInput must be DatasetVector or Recordset')
        else:
            _is_release_line = False
            if isinstance(_line_input, DatasetVector):
                _line_rd = _line_input.get_recordset(False, CursorType.STATIC)
                _is_release_line = True
            else:
                _line_rd = _line_input
        _is_release_region = False
        if isinstance(_region_input, DatasetVector):
            _region_rd = _region_input.get_recordset(False, CursorType.STATIC)
            _is_release_region = True
        else:
            _region_rd = _region_input
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'SplitLinesByRegions')
                _jvm.com.supermap.data.topology.TopologyProcessing.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            is_success = _jvm.com.supermap.data.topology.TopologyProcessing.splitLinesByRegions(_line_rd._jobject, _region_rd._jobject)
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyProcessing.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()

    if _is_release_line:
        _line_rd.close()
    if _is_release_region:
        _region_rd.close()
    return is_success


class PreprocessOptions(object):
    __doc__ = '\n    拓扑预处理参数类\n    '
    _arcs_inserted = False
    _vertex_arc_inserted = False
    _vertexes_snapped = False
    _polygons_checked = False
    _vertex_adjusted = False

    def __init__(self, arcs_inserted=False, vertex_arc_inserted=False, vertexes_snapped=False, polygons_checked=False, vertex_adjusted=False):
        """
        构造拓扑预处理参数类对象

        :param bool arcs_inserted: 是否进行线段间求交插入节点
        :param bool vertex_arc_inserted: 否进行节点与线段间插入节点
        :param bool vertexes_snapped: 是否进行节点捕捉
        :param bool polygons_checked: 是否进行多边形走向调整
        :param bool vertex_adjusted: 是否进行节点位置调整
        """
        self.set_arcs_inserted(arcs_inserted).set_polygons_checked(polygons_checked).set_vertex_adjusted(vertex_adjusted).set_vertex_arc_inserted(vertex_arc_inserted).set_vertexes_snapped(vertexes_snapped)

    @property
    def arcs_inserted(self):
        """bool: 是否进行线段间求交插入节点"""
        return self._arcs_inserted

    @property
    def vertex_arc_inserted(self):
        """bool: 否进行节点与线段间插入节点"""
        return self._vertex_arc_inserted

    @property
    def vertexes_snapped(self):
        """bool: 是否进行节点捕捉"""
        return self._vertexes_snapped

    @property
    def polygons_checked(self):
        """bool: 是否进行多边形走向调整"""
        return self._polygons_checked

    @property
    def vertex_adjusted(self):
        """bool: 是否进行节点位置调整"""
        return self._vertex_adjusted

    def set_arcs_inserted(self, value):
        """
        设置是否进行线段间求交插入节点

        :param bool value: 是否进行线段间求交插入节点
        :return: self
        :rtype: PreprocessOptions
        """
        self._arcs_inserted = bool(value)
        return self

    def set_polygons_checked(self, value):
        """
        设置是否进行多边形走向调整

        :param bool value: 是否进行多边形走向调整
        :return: self
        :rtype: PreprocessOptions
        """
        self._polygons_checked = bool(value)
        return self

    def set_vertex_adjusted(self, value):
        """
        设置是否进行节点位置调整

        :param bool value: 是否进行节点位置调整
        :return: self
        :rtype: PreprocessOptions
        """
        self._vertex_adjusted = bool(value)
        return self

    def set_vertex_arc_inserted(self, value):
        """
        设置否进行节点与线段间插入节点

        :param bool value: 否进行节点与线段间插入节点
        :return: self
        :rtype: PreprocessOptions
        """
        self._vertex_arc_inserted = bool(value)
        return self

    def set_vertexes_snapped(self, value):
        """
        设置是否进行节点捕捉

        :param bool value: 是否进行节点捕捉
        :return: self
        :rtype: PreprocessOptions
        """
        self._vertexes_snapped = bool(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_option = get_jvm().com.supermap.data.topology.TopologyPreprocessOptions()
        java_option.setArcsInserted(self.arcs_inserted)
        java_option.setPolygonsChecked(self.polygons_checked)
        java_option.setVertexAdjusted(self.vertex_adjusted)
        java_option.setVertexArcInserted(self.vertex_arc_inserted)
        java_option.setVertexesSnapped(self.vertexes_snapped)
        return java_option


def preprocess(inputs, arcs_inserted=True, vertex_arc_inserted=True, vertexes_snapped=True, polygons_checked=True, vertex_adjusted=True, precisions=None, tolerance=1e-10, options=None, progress=None):
    """
    对给定的拓扑数据集进行拓扑预处理。

    :param inputs: 输入数据集或记录集，如果是数据集，不能是只读。
    :type inputs: DatasetVector or list[DatasetVector] or str or list[str] or Recordset or list[Recordset]
    :param bool arcs_inserted: 是否进行线段间求交插入节点
    :param bool vertex_arc_inserted: 否进行节点与线段间插入节点
    :param bool vertexes_snapped: 是否进行节点捕捉
    :param bool polygons_checked: 是否进行多边形走向调整
    :param bool vertex_adjusted: 是否进行节点位置调整
    :param precisions: 指定的精度等级数组。精度等级的值越小，代表对应记录集的精度越高，数据质量越好。在进行顶点捕捉时，低精度的记录集中的点将被捕捉到高精度记录集中的点的位置上。精度等级数组必须与要进行拓扑预处理的记录集集合元素数量相同并一一对应。
    :type precisions: list[int]
    :param float tolerance: 指定的处理时需要的容限控制。单位与进行拓扑预处理的记录集单位相同。
    :param PreprocessOption options: 拓扑预处理参数类对象，如果此参数不为空，将优先使用此参数为拓扑预处理参数
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 拓扑预处理是否成功
    :rtype: bool
    """
    check_lic()
    if inputs is None:
        raise ValueError('inputs is None')
    else:
        is_def_orders = True if precisions is not None else False
        if is_def_orders:
            _precisions = split_input_list_from_str(precisions)
        else:
            _datasets = []
            _recordsets = []
            _datasets_orders = []
            _recordsets_orders = []
            if isinstance(inputs, (list, tuple)):
                for i in range(len(inputs)):
                    item = inputs[i]
                    temp = get_input_dataset(item)
                    if temp is not None:
                        if isinstance(temp, DatasetVector):
                            _datasets.append(temp)
                            if is_def_orders:
                                _datasets_orders.append(int(_precisions[i]))
                            else:
                                _datasets_orders.append(0)
                        elif isinstance(temp, Recordset):
                            _recordsets.append(temp)
                            if is_def_orders:
                                _recordsets_orders.append(int(precisions[i]))
                            else:
                                _datasets_orders.append(0)
                        else:
                            raise ValueError('Only support DatasetVector or Recordset')
                    else:
                        raise ValueError('input_data item is None' + str(item))

            else:
                temp = get_input_dataset(inputs)
                if temp is not None:
                    if isinstance(temp, DatasetVector):
                        _datasets_orders.append(0)
                        _datasets.append(temp)
                    else:
                        if isinstance(temp, Recordset):
                            _recordsets_orders.append(0)
                            _recordsets.append(temp)
                        else:
                            raise ValueError('Only support DatasetVector or Recordset')
                else:
                    raise ValueError('input_data item is None' + str(inputs))
    if len(_datasets) + len(_recordsets) == 0:
        raise ValueError('have no valid inputs')
    if len(_datasets) != len(_datasets_orders):
        raise ValueError('the count of precisionOrders must be equal with inputs')
    if len(_recordsets) != len(_recordsets_orders):
        raise ValueError('the count of precisionOrders must be equal with inputs')
    if options is not None and isinstance(options, PreprocessOptions):
        parameters = options
    else:
        parameters = PreprocessOptions(arcs_inserted, vertex_arc_inserted, vertexes_snapped, polygons_checked, vertex_adjusted)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'preprocess')
                _jvm.com.supermap.data.topology.TopologyValidator.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            _all_recordsets = []
            _all_orders = []
            _queryed_recordsets = []
            i = -1
            for rd in _recordsets:
                i += 1
                _all_recordsets.append(rd)
                _queryed_recordsets.append(rd)
                if is_def_orders:
                    _all_orders.append(_recordsets_orders[i])
                else:
                    _all_orders.append(0)

            i = -1
            for dt in _datasets:
                i += 1
                rd = dt.get_recordset(False, CursorType.DYNAMIC)
                if rd is not None:
                    _all_recordsets.append(rd)
                    if is_def_orders:
                        _all_orders.append(_datasets_orders[i])
                    else:
                        _all_orders.append(0)

            is_success = _jvm.com.supermap.data.topology.TopologyValidator.preprocess(to_java_recordset_array(_all_recordsets), to_java_int_array(_all_orders), parameters._jobject, float(tolerance))
        except:
            import traceback
            log_error(traceback.format_exc())
            is_success = False

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyValidator.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        for rd in _queryed_recordsets:
            rd.close()

        _queryed_recordsets.clear()

    return is_success


def topology_validate(source_data, validating_data, rule, tolerance, validate_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对数据集或记录集进行拓扑错误检查，返回含有拓扑错误的结果数据集。

    该方法的 tolerance 参数用于指定使用 rule 参数指定的拓扑规则对数据集检查时涉及的容限。例如，使用“线内无打折”（TopologyRule.LINE_NO_SHARP_ANGLE）规则检查时，tolerance 参数设置的为尖角容限（一个角度值）。

    对于以下拓扑检查算子在调用该方法对数据进行拓扑检查之前，建议先对相应的数据进行拓扑预处理（即调用 :py:meth:`preprocess` 方法），否则检查的结果可能不正确:

        - REGION_NO_OVERLAP_WITH
        - REGION_COVERED_BY_REGION_CLASS
        - REGION_COVERED_BY_REGION
        - REGION_BOUNDARY_COVERED_BY_LINE
        - REGION_BOUNDARY_COVERED_BY_REGION_BOUNDARY
        - REGION_NO_OVERLAP_ON_BOUNDARY
        - REGION_CONTAIN_POINT
        - LINE_NO_OVERLAP_WITH
        - LINE_BE_COVERED_BY_LINE_CLASS
        - LINE_END_POINT_COVERED_BY_POINT
        - POINT_NO_CONTAINED_BY_REGION
        - POINT_COVERED_BY_LINE
        - POINT_COVERED_BY_REGION_BOUNDARY
        - POINT_CONTAINED_BY_REGION
        - POINT_BECOVERED_BY_LINE_END_POINT

    对于以下拓扑检查算法需要设置参考数据集或记录集:

        - REGION_NO_OVERLAP_WITH
        - REGION_COVERED_BY_REGION_CLASS
        - REGION_COVERED_BY_REGION
        - REGION_BOUNDARY_COVERED_BY_LINE
        - REGION_BOUNDARY_COVERED_BY_REGION_BOUNDARY
        - REGION_CONTAIN_POINT
        - REGION_NO_OVERLAP_ON_BOUNDARY
        - POINT_BECOVERED_BY_LINE_END_POINT
        - POINT_NO_CONTAINED_BY_REGION
        - POINT_CONTAINED_BY_REGION
        - POINT_COVERED_BY_LINE
        - POINT_COVERED_BY_REGION_BOUNDARY
        - LINE_NO_OVERLAP_WITH
        - LINE_NO_INTERSECT_OR_INTERIOR_TOUCH
        - LINE_BE_COVERED_BY_LINE_CLASS
        - LINE_NO_INTERSECTION_WITH
        - LINE_NO_INTERSECTION_WITH_REGION
        - LINE_EXIST_INTERSECT_VERTEX
        - VERTEX_DISTANCE_GREATER_THAN_TOLERANCE
        - VERTEX_MATCH_WITH_EACH_OTHER

    :param source_data: 被检查的数据集或记录集
    :type source_data: DatasetVector or str or Recordset
    :param validating_data:  用于检查的参考记录集。如果使用的拓扑规则不需要参考记录集，则设置为 None
    :type validating_data: DatasetVector or str or Recordset
    :param rule: 拓扑检查类型
    :type rule: TopologyRule or str
    :param float tolerance:   指定的拓扑错误检查时使用的容限。单位与进行拓扑错误检查的数据集单位相同。
    :param GeoRegion validate_region: 被检查区域，None，则默认对整个拓扑数据集（validating_data）进行检查，否则对 validate_region 区域进行拓扑检查。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    if source_data is None:
        raise ValueError('sourceData is None')
    else:
        _rule_preprocess = {TopologyRule.REGION_NO_OVERLAP: (True, False), 
         TopologyRule.REGION_NO_GAPS: (True, False), 
         TopologyRule.REGION_NO_OVERLAP_WITH: (True, True), 
         TopologyRule.REGION_COVERED_BY_REGION_CLASS: (True, True), 
         TopologyRule.REGION_COVERED_BY_REGION: (True, True), 
         TopologyRule.REGION_BOUNDARY_COVERED_BY_LINE: (True, True), 
         TopologyRule.REGION_BOUNDARY_COVERED_BY_REGION_BOUNDARY: (True, True), 
         TopologyRule.REGION_CONTAIN_POINT: (False, True), 
         TopologyRule.REGION_NO_OVERLAP_ON_BOUNDARY: (True, True), 
         TopologyRule.REGION_NO_SELF_INTERSECTION: (True, False), 
         TopologyRule.LINE_NO_INTERSECTION: (False, False), 
         TopologyRule.LINE_NO_DANGLES: (False, False), 
         TopologyRule.LINE_NO_PSEUDO_NODES: (False, False), 
         TopologyRule.LINE_NO_OVERLAP_WITH: (True, True), 
         TopologyRule.LINE_NO_INTERSECT_OR_INTERIOR_TOUCH: (True, False), 
         TopologyRule.LINE_NO_SELF_OVERLAP: (False, False), 
         TopologyRule.LINE_NO_SELF_INTERSECT: (False, False), 
         TopologyRule.LINE_BE_COVERED_BY_LINE_CLASS: (True, True), 
         TopologyRule.LINE_END_POINT_COVERED_BY_POINT: (False, True), 
         TopologyRule.LINE_NO_INTERSECTION_WITH: (True, False), 
         TopologyRule.LINE_NO_INTERSECTION_WITH_REGION: (True, False), 
         TopologyRule.POINT_NO_IDENTICAL: (False, False), 
         TopologyRule.POINT_NO_CONTAINED_BY_REGION: (True, True), 
         TopologyRule.POINT_COVERED_BY_LINE: (True, True), 
         TopologyRule.POINT_COVERED_BY_REGION_BOUNDARY: (True, True), 
         TopologyRule.POINT_CONTAINED_BY_REGION: (True, True), 
         TopologyRule.POINT_BECOVERED_BY_LINE_END_POINT: (True, True), 
         TopologyRule.NO_MULTIPART: (False, False), 
         TopologyRule.VERTEX_DISTANCE_GREATER_THAN_TOLERANCE: (True, False), 
         TopologyRule.VERTEX_MATCH_WITH_EACH_OTHER: (True, False), 
         TopologyRule.LINE_EXIST_INTERSECT_VERTEX: (True, False), 
         TopologyRule.NO_REDUNDANT_VERTEX: (False, False), 
         TopologyRule.LINE_NO_SHARP_ANGLE: (False, False), 
         TopologyRule.LINE_NO_SMALL_DANGLES: (False, False), 
         TopologyRule.LINE_NO_EXTENDED_DANGLES: (False, False), 
         TopologyRule.REGION_NO_ACUTE_ANGLE: (False, False)}
        rule = TopologyRule._make(rule)
        if rule is None:
            raise ValueError('rule is None')
        else:
            if tolerance is None:
                tolerance = 1e-10
            else:
                tolerance = float(tolerance)
            _source_input = get_input_dataset(source_data)
            if _source_input is None:
                raise ValueError('source input_data data is None')
            if validating_data is not None:
                _validate_input = get_input_dataset(validating_data)
            else:
                _validate_input = None
        if isinstance(_source_input, DatasetVector):
            if _validate_input is not None and isinstance(_validate_input, Recordset):
                _source_input = _source_input.get_recordset()
        elif isinstance(_source_input, Recordset) and _validate_input is not None:
            if isinstance(_validate_input, DatasetVector):
                _validate_input = _validate_input.get_recordset()
            else:
                if _validate_input is not None:
                    java_validate_input = _validate_input._jobject
                else:
                    java_validate_input = None
                if out_data is not None:
                    out_datasource = get_output_datasource(out_data)
                    _ds = out_datasource
                else:
                    _ds = _source_input.datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = 'validate_Errors'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    javaValidateRegion = None
    if validate_region is not None:
        javaValidateRegion = validate_region._jobject
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'topology_validate')
                _jvm.com.supermap.data.topology.TopologyValidator.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.data.topology.TopologyValidator.validate(_source_input._jobject, java_validate_input, rule._jobject, tolerance, javaValidateRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyValidator.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def resample_raster(input_data, new_cell_size, resample_mode, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格数据重采样，返回结果数据集。

    栅格数据经过了配准或纠正、投影等几何操作后，栅格的像元中心位置通常会发生变化，其在输入栅格中的位置不一定是整数的行列号，因此需要根据输出栅格上每个格子在输入栅格中的位置，对输入栅格按一定规则进行重采样，进行栅格值的插值计算，建立新的栅格矩阵。不同分辨率的栅格数据之间进行代数运算时，需要将栅格大小统一到一个指定的分辨率上，此时也需要对栅格进行重采样。

    栅格重采样有三种常用方法：最邻近法、双线性内插法和三次卷积法。有关这三种重采样方法较为详细的介绍，请参见 ResampleMode 类。

    :param input_data:  指定的用于栅格重采样的数据集。支持影像数据集，包括多波段影像
    :type input_data: DatasetImage or DatasetGrid or str
    :param float new_cell_size: 指定的结果栅格的单元格大小
    :param resample_mode: 重采样计算方法
    :type resample_mode: ResampleMode or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetImage or DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, (DatasetGrid, DatasetImage)):
            raise ValueError('source input_data required DatasetGrid or DatasetImage')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_resample'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'resample_raster')
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.resample(_source_input._jobject, float(new_cell_size), RasterResampleMode._make(resample_mode)._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class ReclassSegment(object):
    __doc__ = '\n    栅格重分级区间类。该类主要用于重分级区间信息的相关设置，包括区间的起始值、终止值等。\n\n    该类用于设置在进行重分级时，重分级映射表中每个重分级区间的参数，重分级类型不同，需要设置的属性也有所不同。\n\n    - 当重分级类型为单值重分级时，需要通过 :py:meth:`set_start_value` 方法指定需要被重新赋值的源栅格的单值，并通过 :py:meth:`set_new_value` 方法设置该值对应的新值。\n    - 当重分级类型为范围重分级时，需要通过 :py:meth:`set_start_value` 方法指定需要重新赋值的源栅格值区间的起始值，通过 :py:meth:`set_end_value` 方法设置区间的终止值，\n      并通过 :py:meth:`set_new_value` 方法设置该区间对应的新值，还可以由 :py:meth:`set_segment_type` 方法设置区间类型是“左开右闭”还是“左闭右开”。\n\n    '

    def __init__(self, start_value=None, end_value=None, new_value=None, segment_type=None):
        """
        构造栅格重分级区间对象

        :param float start_value:  栅格重分级区间的起始值
        :param float end_value: 栅格重分级区间的终止值
        :param float new_value: 栅格重分级的区间值或旧值对应的新值
        :param segment_type:  栅格重分级区间类型
        :type segment_type: ReclassSegmentType or str
        """
        self._endValue = None
        self._startValue = None
        self._newValue = None
        self._segmentType = None
        self.set_start_value(start_value).set_end_value(end_value).set_new_value(new_value).set_segment_type(segment_type)

    def set_segment_type(self, value):
        """
        设置栅格重分级区间类型

        :param value: 栅格重分级区间类型
        :type value: ReclassSegmentType or str
        :return: self
        :rtype: ReclassSegment
        """
        self._segmentType = ReclassSegmentType._make(value)
        return self

    @property
    def end_value(self):
        """float: 栅格重分级区间的终止值"""
        return self._endValue

    def set_start_value(self, value):
        """
        设置栅格重分级区间的起始值

        :param float value: 栅格重分级区间的起始值
        :return: self
        :rtype: ReclassSegment
        """
        if value is not None:
            self._startValue = float(value)
        return self

    def set_new_value(self, value):
        """
        栅格重分级的区间值或旧值对应的新值

        :param float value: 栅格重分级的区间值或旧值对应的新值
        :return: self
        :rtype: ReclassSegment
        """
        if value is not None:
            self._newValue = float(value)
        return self

    @property
    def start_value(self):
        """float: 栅格重分级区间的起始值"""
        return self._startValue

    def set_end_value(self, value):
        """
        栅格重分级区间的终止值

        :param float value: 栅格重分级区间的终止值
        :return: self
        :rtype: ReclassSegment
        """
        if value is not None:
            self._endValue = float(value)
        return self

    @property
    def new_value(self):
        """float: 栅格重分级的区间值或旧值对应的新值"""
        return self._newValue

    @property
    def segment_type(self):
        """ReclassSegmentType: 栅格重分级区间类型"""
        return self._segmentType

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.ReclassSegment()
        if self.segment_type is not None:
            java_obj.setSegmentType(self.segment_type._jobject)
        if self.start_value is not None:
            java_obj.setStartValue(self.start_value)
        if self.new_value is not None:
            java_obj.setNewValue(self.new_value)
        if self.end_value is not None:
            java_obj.setEndValue(self.end_value)
        return java_obj

    def to_dict(self):
        """
        将当前对象信息输出到 dict

        :return: 包含当前对象信息的 dict 对象
        :rtype: dict
        """
        d = dict()
        if self.end_value is not None:
            d['end_value'] = self.end_value
        if self.start_value is not None:
            d['start_value'] = self.start_value
        if self.new_value is not None:
            d['new_value'] = self.new_value
        if self.segment_type is not None:
            d['segment_type'] = self.segment_type.name
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从dict中读取信息构造 ReclassSegment 对象

        :param values: 包含 ReclassSegment 信息的 dict
        :type values: dict
        :return: 栅格重分级区间对象
        :rtype: ReclassSegment
        """
        return ReclassSegment().from_dict(values)

    def from_dict(self, values):
        """
        从dict中读取信息

        :param values: 包含 ReclassSegment 信息的 dict
        :type values: dict
        :return: self
        :rtype: ReclassSegment
        """
        if 'end_value' in values.keys():
            self.set_end_value(values['end_value'])
        if 'start_value' in values.keys():
            self.set_start_value(values['start_value'])
        if 'new_value' in values.keys():
            self.set_new_value(values['new_value'])
        if 'segment_type' in values.keys():
            self.set_segment_type(values['segment_type'])
        return self


def _to_java_reclass_segment_array(values):
    if values is None:
        return
    if isinstance(values, ReclassSegment):
        java_array = get_gateway().new_array(get_jvm().com.supermap.analyst.spatialanalyst.ReclassSegment, 1)
        java_array[0] = values._jobject
        return java_array
    if isinstance(values, (list, tuple, set)):
        _size = len(values)
        java_array = get_gateway().new_array(get_jvm().com.supermap.analyst.spatialanalyst.ReclassSegment, _size)
        i = 0
        for value in values:
            java_array[i] = value._jobject
            i += 1

        return java_array
    return


class ReclassMappingTable(object):
    __doc__ = '\n    栅格重分级映射表类。提供对源栅格数据集进行单值或范围的重分级，且包含对无值数据和未分级单元格的处理。\n\n    重分级映射表，用于说明源数据和结果数据值之间的对应关系。这种对应关系由这几部分内容表达：重分级类型、重分级区间集合、无值和未分级数据的处理。\n\n    - 重分级的类型\n      重分级有两种类型，单值重分级和范围重分级。单值重分级是对指定的某些单值进行重新赋值，如将源栅格中值为100的单元格，赋值为1输出到结果\n      栅格中；范围重分级将一个区间内的值重新赋值为一个值，如将源栅格中栅格值在[100,500)范围内的单元格，重新赋值为200输出到结果栅格中。通过该类的 :py:meth:`set_reclass_type` 方法来设置重分级类型。\n\n    - 重分级区间集合\n      重分级的区间集合规定了源栅格某个栅格值或者一定区间内的栅格值与重分级后的新值的对应关系，通过该类的  :py:meth:`set_segments` 方法设置。\n      该集合由若干重分级区间（ReclassSegment）对象构成。该对象用于设置每个重分级区间的信息，包括要重新赋值的源栅格单值或区间的起始值、终止值，重分级区间的类型，\n      以及栅格重分级的区间值或源栅格单值对应的新值等，详见 :py:class:`.ReclassSegment` 类。\n\n    - 无值和未分级数据的处理\n      对源栅格数据中的无值，可以通过该类的 :py:meth:`set_retain_no_value` 方法来设置是否保持无值，如果为 False，即不保持为无值，则可通过 :py:meth:`set_change_no_value_to` 方法为无值数据指定一个值。\n\n      对在重分级映射表中未涉及的栅格值，可以通过该类的 :py:meth:`set_retain_missing_value` 方法来设置是否保持其原值，如果为 False，即不保持原值，则可通过 :py:meth:`set_change_missing_valueT_to` 方法为其指定一个值。\n\n    此外，该类还提供了将重分级映射表数据导出为 XML 字符串及 XML 文件的方法和导入 XML 字符串或文件的方法。当多个输入的栅格数据需要应用相同的分级范围时，可以将其导出为重分级映射表文件，\n    当对后续数据进行分级时，直接导入该重分级映射表文件，进而可以批量处理导入的栅格数据。有关栅格重分级映射表文件的格式和标签含义请参见 to_xml 方法。\n\n\n    '

    def __init__(self):
        self._retainMissingValue = None
        self._changeNoValueTo = None
        self._changeMissingValueTo = None
        self._segments = []
        self._retainNoValue = None
        self._reclassType = None

    @property
    def is_retain_missing_value(self):
        """bool: 源数据集中不在指定区间或单值之外的数据是否保留原值"""
        return self._retainMissingValue

    def set_change_missing_value_to(self, value):
        """
        设置不在指定区间或单值内的栅格的指定值。如果 :py:meth:`is_retain_no_value` 为 True 时，则该设置无效。

        :param float value: 不在指定区间或单值内的栅格的指定值
        :return: self
        :rtype: ReclassMappingTable
        """
        self._changeMissingValueTo = float(value)
        return self

    def set_retain_missing_value(self, value):
        """
        设置源数据集中不在指定区间或单值之外的数据是否保留原值。

        :param bool value:  源数据集中不在指定区间或单值之外的数据是否保留原值。
        :return: self
        :rtype: ReclassMappingTable
        """
        self._retainMissingValue = value
        return self

    @property
    def change_no_value_to(self):
        """float: 返回无值数据的指定值"""
        return self._changeNoValueTo

    @property
    def change_missing_value_to(self):
        """float: 返回不在指定区间或单值内的栅格的指定值。"""
        if self._changeMissingValueTo is not None:
            return float(self._changeMissingValueTo)

    def set_change_no_value_to(self, value):
        """
        设置无值数据的指定值。:py:meth:`is_retain_no_value` 为 True 时，该设置无效。

        :param float value: 无值数据的指定值
        :return: self
        :rtype: ReclassMappingTable
        """
        if value is not None:
            self._changeNoValueTo = float(value)
        return self

    @property
    def segments(self):
        """list[ReclassSegment]: 返回重分级区间集合。 每一个 ReclassSegment 就是一个区间范围或者是一个旧值和一个新值的对应关系。"""
        return self._segments

    @property
    def is_retain_no_value(self):
        """bool: 返回是否将源数据集中的无值数据保持为无值。 """
        return self._retainNoValue

    def set_segments(self, value):
        """
        设置重分级区间集合

        :param value: 重分级区间集合。当 value 为 str 时，支持使用 ';' 分隔多个ReclassSegment，每个 ReclassSegment使用 ','分隔 起始值、终止值、新值和分区类型。例如:
                        '0,100,50,CLOSEOPEN; 100,200,150,CLOSEOPEN'
        :type value: list[ReclassSegment] or str
        :return: self
        :rtype: ReclassMappingTable
        """
        if value is not None:
            if isinstance(value, (list, tuple)):
                self._segments = list(value)
            else:
                if isinstance(value, str):
                    segs = value.split(';')
                    self._segments = []
                    for seg in segs:
                        items = seg.split(',')
                        if len(items) == 4:
                            self._segments.append(ReclassSegmentfloat(items[0])float(items[1])float(items[2])str(items[3]))
                        else:
                            items = seg.split(' ')
                        if len(items) == 4:
                            self._segments.append(ReclassSegmentfloat(items[0])float(items[1])float(items[2])str(items[3]))

        return self

    @property
    def reclass_type(self):
        """ReclassType: 返回栅格重分级类型"""
        return self._reclassType

    def set_reclass_type(self, value):
        """
        设置栅格重分级类型

        :param value: 栅格重分级类型，默认值为 UNIQUE
        :type value: ReclassType or str
        :return: self
        :rtype: ReclassMappingTable
        """
        self._reclassType = ReclassType._make(value)
        return self

    def set_retain_no_value(self, value):
        """
        设置是否将源数据集中的无值数据保持为无值。设置是否将源数据集中的无值数据保持为无值。
        - 当 set_retain_no_value 方法设置为 True 时，表示保持源数据集中的无值数据为无值；
        - 当 set_retain_no_value 方法设置为 False 时，表示将源数据集中的无值数据设置为指定的值（ :py:meth:`set_change_no_value_to` ）

        :param bool value:
        :return: self
        :rtype: ReclassMappingTable
        """
        self._retainNoValue = value
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.ReclassMappingTable()
        if self.change_missing_value_to is not None:
            java_obj.setChangeMissingValueTo(float(self.change_missing_value_to))
        if self.is_retain_missing_value is not None:
            java_obj.setRetainMissingValue(self.is_retain_missing_value)
        if self.change_no_value_to is not None:
            java_obj.setChangeNoValueTo(self.change_no_value_to)
        if self.segments is not None:
            java_obj.setSegments(_to_java_reclass_segment_array(self.segments))
        if self.reclass_type is not None:
            java_obj.setReclassType(self.reclass_type._jobject)
        if self.is_retain_no_value is not None:
            java_obj.setRetainNoValue(self.is_retain_no_value)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        rel = ReclassMappingTable()
        rel.set_retain_no_value(java_obj.isRetainNoValue())
        rel.set_retain_missing_value(java_obj.isRetainMissingValue())
        rel.set_reclass_type(java_obj.getReclassType().name())
        rel.set_change_no_value_to(java_obj.getChangeNoValueTo())
        rel.set_change_missing_value_to(java_obj.getChangeMissingValueTo())
        java_segments = java_obj.getSegments()
        if java_segments is not None:
            segments = []
            for java_seg in java_segments:
                segments.append(ReclassSegmentjava_seg.getStartValue()java_seg.getEndValue()java_seg.getNewValue()java_seg.getSegmentType().name())

            rel.set_segments(segments)
        return rel

    def to_dict(self):
        """
        将当前信息输出到 dict 中

        :return: 包含当前信息的字典对象
        :rtype: dict
        """
        d = dict()
        if self.is_retain_missing_value is not None:
            d['is_retain_missing_value'] = self.is_retain_missing_value
        if self.change_no_value_to is not None:
            d['change_no_value_to'] = self.change_no_value_to
        if self.change_missing_value_to is not None:
            d['change_missing_value_to'] = self.change_missing_value_to
        if self.segments is not None:
            d['segments'] = self.segments
        if self.is_retain_no_value is not None:
            d['is_retain_no_value'] = self.is_retain_no_value
        if self.reclass_type is not None:
            d['reclass_type'] = self.reclass_type
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 对象中读取重分级映射表信息构造新的对象

        :param dict values: 包含重分级映射表信息的 dict 对象
        :return: 重分级映射表对象
        :rtype: ReclassMappingTable
        """
        return ReclassMappingTable().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 对象中读取重分级映射表信息

        :param dict values: 包含重分级映射表信息的 dict 对象
        :return: self
        :rtype: ReclassMappingTable
        """
        if 'is_retain_missing_value' in values.keys():
            self.set_retain_missing_value(values['is_retain_missing_value'])
        if 'change_no_value_to' in values.keys():
            self.set_change_no_value_to(values['change_no_value_to'])
        if 'change_missing_value_to' in values.keys():
            self.set_change_missing_value_to(values['change_missing_value_to'])
        if 'segments' in values.keys():
            self.set_segments(values['segments'])
        if 'is_retain_no_value' in values.keys():
            self.set_retain_no_value(values['is_retain_no_value'])
        if 'reclass_type' in values.keys():
            self.set_reclass_type(values['reclass_type'])
        return self

    def to_xml(self):
        """
        将当前对象信息输出为 xml 字符串

        :return: xml 字符串
        :rtype: str
        """
        return self._jobject.toXml()

    def to_xml_file(self, xml_file):
        """
        该方法用于将对重分级映射表对象的参数设置写入一个 XML 文件，称为栅格重分级映射表文件，其后缀名为 .xml，下面是一个栅格重分级映射表文件的例子：

        重分级映射表文件中各标签的含义如下：

        - <SmXml:ReclassType></SmXml:ReclassType> 标签：重分级类型。1表示单值重分级，2表示范围重分级。
        - <SmXml:SegmentCount></SmXml:SegmentCount> 标签：重分级区间集合，count 参数表示重分级的级数。
        - <SmXml:Range></SmXml:Range> 标签：重分级区间，重分级类型为单值重分级，格式为：区间起始值--区间终止值：新值-区间类型。对于区间类型，0表示左开右闭，1表示左闭右开。
        - <SmXml:Unique></SmXml:Unique> 标签：重分级区间，重分级类型为范围重分级，格式为：原值：新值。
        - <SmXml:RetainMissingValue></SmXml:RetainMissingValue> 标签：未分级单元格是否保留原值。0表示不保留，1表示保留。
        - <SmXml:RetainNoValue></SmXml:RetainNoValue> 标签：无值数据是否保持无值。0表示不保持，0表示不保持。
        - <SmXml:ChangeMissingValueTo></SmXml:ChangeMissingValueTo> 标签：为未分级单元格的指定的值。
        - <SmXml:ChangeNoValueTo></SmXml:ChangeNoValueTo> 标签：为无值数据的指定的值。

        :param str xml_file: xml 文件路径
        :type xml_file:
        :return: 导出成功返回 True，否则返回 False
        :rtype: bool
        """
        return self._jobject.toXmlFile(xml_file)

    @staticmethod
    def from_xml(xml):
        """
        从存储在XML格式字符串中的参数值导入到映射表数据中，并返回一个新的对象。

        :param str xml: XML格式字符串
        :return:  栅格重分级映射表对象
        :rtype: ReclassMappingTable
        """
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.ReclassMappingTable()
        if java_obj.fromXml(xml):
            return ReclassMappingTable._from_java_object(java_obj)
        return

    @staticmethod
    def from_xml_file(xml_file):
        """
        从已保存的XML格式的映射表文件中导入映射表数据，并返回一个新的对象。

        :param str xml_file: XML文件
        :return:  栅格重分级映射表对象
        :rtype: ReclassMappingTable
        """
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.ReclassMappingTable()
        if java_obj.fromXmlFile(xml_file):
            return ReclassMappingTable._from_java_object(java_obj)
        return


def reclass_grid(input_data, re_pixel_format, segments=None, reclass_type='UNIQUE', is_retain_no_value=True, change_no_value_to=None, is_retain_missing_value=False, change_missing_value_to=None, reclass_map=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格数据重分级，返回结果栅格数据集。
    栅格重分级就是对源栅格数据的栅格值进行重新分类和按照新的分类标准赋值，其结果是用新的值取代了栅格数据的原栅格值。对于已知的栅格数据，有时为了便于看清趋势，找出栅格值的规律，或者为了方便进一步的分析，重分级是很必要的：

        - 通过重分级，可以使用新值来替代单元格的旧值，以达到更新数据的目的。例如，在处理土地类型变更时，将已经开垦为耕地的荒地赋予新的栅格值；
        - 通过重分级，可以对大量的栅格值进行分组归类，同组的单元格赋予相同的值来简化数据。例如，将旱地、水浇地、水田等都归为农业用地；
        - 通过重分级，可以对多种栅格数据按照统一的标准进行分类。例如，某个建筑物的选址的影响因素包括土壤和坡度，则对输入的土壤类型和坡度的栅格数据，可以按照 1-10 的等级标准来进行重分级，便于进一步的选址分析；
        - 通过重分级，可以将某些不希望参与分析的单元格设为无值，也可以为原先为无值的单元格补充新测定的值，便于进一步的分析处理。

    例如，常常需要对栅格表面进行坡度分析得到坡度数据，来辅助与地形有关的分析。但我们可能需要知道坡度属于哪个等级而不是具体的坡度数值，来帮助我们了解地形的陡峭程度，从而辅助进一步的分析，如选址、分析道路铺设线路等。此时可以使用重分级，将不同的坡度划分到对应的等级中。

    :param input_data:  指定的用于栅格重采样的数据集。支持影像数据集，包括多波段影像
    :type input_data: DatasetImage or DatasetGrid or str
    :param re_pixel_format: 结果数据集的栅格值的存储类型
    :type re_pixel_format: ReclassPixelFormat
    :param segments: 重分级区间集合。重分级区间集合。当 segments 为 str 时，支持使用 ';' 分隔多个ReclassSegment，每个 ReclassSegment使用 ','分隔 起始值、终止值、新值和分区类型。例如: '0,100,50,CLOSEOPEN; 100,200,150,CLOSEOPEN'
    :type segments: list[ReclassSegment] or str
    :param reclass_type: 栅格重分级类型
    :type reclass_type: ReclassType or str
    :param bool is_retain_no_value: 是否将源数据集中的无值数据保持为无值
    :param float change_no_value_to: 无值数据的指定值。 is_retain_no_value 设置为 False 时，该设置有效，否则无效。
    :param bool is_retain_missing_value: 源数据集中不在指定区间或单值之外的数据是否保留原值
    :param float change_missing_value_to: 不在指定区间或单值内的栅格的指定值，is_retain_no_value 设置为 False 时，该设置有效，否则无效。
    :param ReclassMappingTable reclass_map: 栅格重分级映射表类。如果该对象不为空，使用该对象设置的值进行栅格重分级。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or DatasetImage or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, (DatasetGrid, DatasetImage)):
            raise ValueError('source input_data required DatasetGrid or DatasetImage')
        else:
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _source_input.datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = _source_input.name + '_reclass'
            else:
                _outDatasetName = out_dataset_name
        _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
        _jvm = get_jvm()
        if reclass_map is not None:
            java_reclassMap = reclass_map._jobject
        else:
            java_reclassMap = ReclassMappingTable().set_change_missing_value_to(change_missing_value_to).set_change_no_value_to(change_no_value_to).set_reclass_type(reclass_type).set_retain_missing_value(is_retain_missing_value).set_retain_no_value(is_retain_no_value).set_segments(segments)._jobject
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'reclass_grid')
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.reclass(_source_input._jobject, java_reclassMap, ReclassPixelFormat._make(re_pixel_format)._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def aggregate_grid(input_data, scale, aggregation_type, is_expanded, is_ignore_no_value, out_data=None, out_dataset_name=None, progress=None):
    """

    栅格数据聚合，返回结果栅格数据集。
    栅格聚合操作是以整数倍缩小栅格分辨率，生成一个新的分辨率较粗的栅格的过程。此时，每个像元由原栅格数据的一组像元聚合而成，其值由其包含的原栅格的值共
    同决定，可以取包含栅格的和、最大值、最小值、平均值、中位数。如缩小n（n为大于1的整数）倍，则聚合后栅格的行、列的数目均为原栅格的1/n，也就是单元格
    大小是原来的n倍。聚合可以通过对数据进行概化，达到清除不需要的信息或者删除微小错误的目的。

    注意：如果原栅格数据的行列数不是 scale 的整数倍，使用 is_expanded 参数来处理零头。

    - is_expanded 为 true，则在零头加上一个数，使之成为一个整数倍，扩大的范围其栅格值均为无值，因此，结果数据集的范围会比原始的大一些。

    - is_expanded 为 false，去掉零头，结果数据集的范围会比原始的小一些。

    :param input_data: 指定的进行聚合操作的栅格数据集。
    :type input_data: DatasetGrid or str
    :param int scale: 指定的结果栅格与输入栅格之间栅格大小的比例。取值为大于 1 的整型数值。
    :param aggregation_type: 聚合操作类型
    :type aggregation_type: AggregationType
    :param bool is_expanded: 指定是否处理零头。当原栅格数据的行列数不是 scale 的整数倍时，栅格边界处则会出现零头。
    :param bool is_ignore_no_value:  在聚合范围内含有无值数据时聚合操作的计算方式。如果为 True，使用聚合范围内除无值外的其余栅格值来计算；如果为 False，则聚合结果为无值。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError('source input_data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_aggregate'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'aggregate_grid')
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.aggregate(_source_input._jobject, int(scale), AggregationType._make(aggregation_type)._jobject, bool(is_expanded), bool(is_ignore_no_value), _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def slice_grid(input_data, number_zones, base_output_zones, out_data=None, out_dataset_name=None, progress=None):
    """
    自然分割重分级，适用于分布不均匀的数据。

    Jenks自然间断法:

    该重分级方法利用的是Jenks自然间断法。Jenks自然间断法基于数据中固有的自然分组，这是方差最小化分级的形式，间断通常不均匀，且间断 选择在值出现剧
    烈变动的地方，所以该方法能对相似值进行恰当分组并可使各分级间差异最大化。Jenks间断点分级法会将相似值（聚类值）放置在同一类中，所以该方法适用于
    分布不均匀的数据值。

    :param input_data: 指定的进行重分级操作的栅格数据集。
    :type input_data: DatasetGrid or str
    :param int number_zones: 将栅格数据集重分级的区域数量。
    :param int base_output_zones:  结果栅格数据集中最低区域的值
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    设置分级区域数为9,将待分级栅格数据的最小值到最大值自然分割为9份。最低区域值设为1，重分级后的值以1为起始值每级递增。

    >>> slice_grid('E:/data.udb/DEM', 9, 1, 'E:/Slice_out.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError('source input_data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_Slice'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'slice_grid')
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.slice(_source_input._jobject, _ds._jobject, _outDatasetName, int(number_zones), int(base_output_zones))
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def compute_range_raster(input_data, count, progress=None):
    """
    计算栅格像元值的自然断点中断值

    :param input_data: 栅格数据集
    :type input_data: DatasetGrid or str
    :param count: 自然分段的个数
    :type count: int
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 自然分段的中断值（包括像元的最大和最小值）
    :rtype: Array
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'compute_range_raster')
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_arr = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.ComputeRange(_source_input._jobject, int(count))
        except Exception as e:
            try:
                log_error(e)
                java_result_arr = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result_arr is not None:
            result_arr = java_result_arr
            return result_arr
        return


def compute_range_vector(input_data, value_field, count, progress=None):
    """
    计算矢量自然断点中断值

    :param input_data: 矢量数据集
    :type input_data: DatasetVector or str
    :param value_field: 分段的标准字段
    :type value_field: str
    :param count: 自然分段的个数
    :type count: int
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 自然分段的中断值（包括属性的最大和最小值）
    :rtype: Array
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetVector):
        raise ValueError('source input_data must be DatasetVector')
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'compute_range_vector')
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_arr = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.ComputeRange(_source_input._jobject, str(value_field), int(count))
        except Exception as e:
            try:
                log_error(e)
                java_result_arr = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result_arr is not None:
            result_arr = java_result_arr
            return result_arr
        return


def density_based_clustering(input_data, min_pile_point_count, search_distance, unit, out_data=None, out_dataset_name=None, progress=None):
    """
    密度聚类的DBSCAN实现

    该方法根据给定的搜索半径（search_distance）和该范围内需包含的最少点数（min_pile_point_count）将空间点数据中密度足够大且空间相近的区域相连，并消除噪声的干扰，以达到较好的聚类效果。

    :param input_data: 指定的要聚类的矢量数据集，支持点数据集。
    :type input_data: DatasetVector or str
    :param min_pile_point_count: 每类包含的最少点数
    :type min_pile_point_count: int
    :param search_distance: 搜索邻域的距离
    :type search_distance: int
    :param unit: 搜索距离的单位
    :type unit: Unit
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetVector):
        raise ValueError('source input_data must be DatasetVector')
    if min_pile_point_count is None:
        raise ValueError('min pile point count is None')
    if search_distance is None:
        raise ValueError('search distance is None')
    else:
        if not isinstance(unit, Unit):
            raise ValueError('unit is illegal')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_dbscan'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'density_based_clustering')
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.densityBasedClustering(_source_input._jobject, _ds._jobject, _outDatasetName, int(min_pile_point_count), float(search_distance), Unit._make(unit)._jobject)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def hierarchical_density_based_clustering(input_data, min_pile_point_count, out_data=None, out_dataset_name=None, progress=None):
    """
    密度聚类的HDBSCAN实现

    该方法是对DBSCAN方法的改进，只需给定空间邻域范围内的最少点数（min_pile_point_count）。在DBSCAN的基础上，计算不同的搜索半径选择最稳定的空间聚类分布作为密度聚类结果。

    :param input_data: 指定的要聚类的矢量数据集，支持点数据集。
    :type input_data: DatasetVector or str
    :param min_pile_point_count: 每类包含的最少点数
    :type min_pile_point_count: int
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        else:
            if min_pile_point_count is None:
                raise ValueError('min pile point count is None')
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_hdbscan'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'hierarchical_density_based_clustering')
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.hierarchicalDensityBasedClustering(_source_input._jobject, _ds._jobject, _outDatasetName, int(min_pile_point_count))
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def ordering_density_based_clustering(input_data, min_pile_point_count, search_distance, unit, cluster_sensitivity, out_data=None, out_dataset_name=None, progress=None):
    """
    密度聚类的OPTICS实现

    该方法在DBSCAN的基础上，额外计算了每个点的可达距离，并基于排序信息和聚类系数（cluster_sensitivity）得到聚类结果。该方法对于搜索半径（search_distance）和该范围内需包含的最少点数（min_pile_point_count）不是很敏感，主要决定结果的是聚类系数（cluster_sensitivity）

    概念定义：
    - 可达距离：取核心点的核心距离和其到周围临近点距离的最大值。
    - 核心点：某个点在搜索半径内，存在点的个数不小于每类包含的最少点数（min_pile_point_count）。
    - 核心距离：某个点成为核心点的最小距离。
    - 聚类系数：为1~100的整数，是对聚类类别多少的标准量化，系数为1时聚类类别最少、100最多。

    :param input_data: 指定的要聚类的矢量数据集，支持点数据集。
    :type input_data: DatasetVector or str
    :param min_pile_point_count: 每类包含的最少点数
    :type min_pile_point_count: int
    :param search_distance: 搜索邻域的距离
    :type search_distance: int
    :param unit: 搜索距离的单位
    :type unit: Unit
    :param cluster_sensitivity: 聚类系数
    :type cluster_sensitivity: int
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetVector):
        raise ValueError('source input_data must be DatasetVector')
    if min_pile_point_count is None:
        raise ValueError('min pile point count is None')
    if search_distance is None:
        raise ValueError('search distance is None')
    if cluster_sensitivity is None:
        raise ValueError('cluster sensitivity is None')
    else:
        if not isinstance(unit, Unit):
            raise ValueError('unit is illegal')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_optics'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'ordering_density_based_clustering')
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.orderingDensityBasedClustering(_source_input._jobject, _ds._jobject, _outDatasetName, int(min_pile_point_count), float(search_distance), Unit._make(unit)._jobject, int(cluster_sensitivity))
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class NeighbourShape:
    __doc__ = '邻域形状基类。邻域按照形状可分为：矩形邻域、圆形邻域、环形邻域和扇形邻域。邻域形状的相关参数设置'

    def __init__(self):
        self._shape_type = None

    @property
    def shape_type(self):
        """NeighbourShapeType: 域分析的邻域形状类型"""
        return self._shape_type


class NeighbourShapeRectangle(NeighbourShape):
    __doc__ = '矩形邻域形状类'

    def __init__(self, width, height):
        """
        构造矩形邻域形状类对象

        :param float width: 矩形邻域的宽
        :param float height: 矩形邻域的高
        """
        NeighbourShape.__init__(self)
        self._width = 0.0
        self._height = 0.0
        self.set_width(width).set_height(height)
        self._shape_type = NeighbourShapeType.RECTANGLE

    @property
    def width(self):
        """float: 矩形邻域的宽"""
        return self._width

    def set_width(self, value):
        """
        设置矩形邻域的宽

        :param float value: 矩形邻域的宽
        :return: self
        :rtype:  NeighbourShapeRectangle
        """
        self._width = float(value)
        return self

    @property
    def height(self):
        """float: 矩形邻域的高"""
        return self._height

    def set_height(self, value):
        """
        设置矩形邻域的高

        :param float value:  矩形邻域的高
        :return: self
        :rtype:  NeighbourShapeRectangle
        """
        self._height = float(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourShapeRectangle()
        java_obj.setWidth(self.width)
        java_obj.setHeight(self.height)
        return java_obj


class NeighbourShapeCircle(NeighbourShape):
    __doc__ = '圆形邻域形状类'

    def __init__(self, radius):
        """
        构造圆形邻域形状类对象

        :param float radius: 圆形邻域的半径
        """
        NeighbourShape.__init__(self)
        self._radius = None
        self.set_radius(radius)
        self._shape_type = NeighbourShapeType.CIRCLE

    @property
    def radius(self):
        """float: 圆形邻域的半径"""
        return self._radius

    def set_radius(self, value):
        """
        设置圆形邻域的半径

        :param float value: 圆形邻域的半径
        :return: self
        :rtype: NeighbourShapeCircle
        """
        self._radius = float(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourShapeCircle()
        java_obj.setRadius(self.radius)
        return java_obj


class NeighbourShapeAnnulus(NeighbourShape):
    __doc__ = '环形邻域形状类'

    def __init__(self, inner_radius, outer_radius):
        """
        构造环形邻域形状类对象

        :param float inner_radius: 内环半径
        :param float outer_radius: 外环半径
        """
        NeighbourShape.__init__(self)
        self._inner_radius = None
        self._outer_radius = None
        self.set_inner_radius(inner_radius).set_outer_radius(outer_radius)
        self._shape_type = NeighbourShapeType.ANNULUS

    @property
    def inner_radius(self):
        """float: 内环半径"""
        return self._inner_radius

    def set_inner_radius(self, value):
        """
        设置内环半径

        :param float value: 内环半径
        :return: self
        :rtype: NeighbourShapeAnnulus
        """
        self._inner_radius = float(value)
        return self

    @property
    def outer_radius(self):
        """float: 外环半径"""
        return float(self._out_radius)

    def set_outer_radius(self, value):
        """
        设置外环半径

        :param float value: 外环半径
        :return: self
        :rtype: NeighbourShapeAnnulus
        """
        self._out_radius = float(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourShapeAnnulus()
        java_obj.setInnerRadius(self.inner_radius)
        java_obj.setOuterRadius(self.outer_radius)
        return java_obj


class NeighbourShapeWedge(NeighbourShape):
    __doc__ = '扇形邻域形状类'

    def __init__(self, radius, start_angle, end_angle):
        """
        构造扇形邻域形状类对象

        :param float radius: 形邻域的半径
        :param float start_angle: 扇形邻域的起始角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。
        :param float end_angle: 扇形邻域的终止角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。
        """
        NeighbourShape.__init__(self)
        self._radius = 0.0
        self._start_angle = 0.0
        self._end_angle = 0.0
        self.set_radius(radius).set_start_angle(start_angle).set_end_angle(end_angle)
        self._shape_type = NeighbourShapeType.WEDGE

    @property
    def radius(self):
        """float: 扇形邻域的半径"""
        return self._radius

    @property
    def start_angle(self):
        """float: 扇形邻域的起始角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。 """
        return self._start_angle

    @property
    def end_angle(self):
        """float: 扇形邻域的终止角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。 """
        return self._end_angle

    def set_radius(self, value):
        """
        设置扇形邻域的半径

        :param float value: 扇形邻域的半径
        :return: self
        :rtype: NeighbourShapeWedge
        """
        self._radius = float(value)
        return self

    def set_start_angle(self, value):
        """
        设置扇形邻域的起始角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。

        :param float value: 扇形邻域的起始角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。
        :return: self
        :rtype: NeighbourShapeWedge
        """
        self._start_angle = float(value)
        return self

    def set_end_angle(self, value):
        """
        设置扇形邻域的终止角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。

        :param float value:
        :return: self
        :rtype: NeighbourShapeWedge
        """
        self._end_angle = float(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourShapeWedge()
        java_obj.setRadius(self.radius)
        java_obj.setStartAngle(self.start_angle)
        java_obj.setEndAngle(self.end_angle)
        return java_obj


def kernel_density(input_data, value_field, search_radius, resolution, bounds=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对点数据集或线数据集进行核密度分析，并返回分析结果。
    核密度分析，即使用核函数，来计算点或线邻域范围内的每单位面积量值。其结果是中间值大周边值小的光滑曲面，在邻域边界处降为0。

    :param input_data: 需要进行核密度分析的点数据集或线数据集。
    :type input_data: DatasetVector or str
    :param str value_field: 存储用于进行密度分析的测量值的字段名称。若传 None 则所有几何对象都按值为1处理。不支持文本类型的字段。
    :param float search_radius: 栅格邻域内用于计算密度的查找半径。单位与用于分析的数据集的单位相同。当计算某个栅格位置的未知数值时，会以该位置
                                为圆心，以该属性设置的值为半径，落在这个范围内的采样对象都将参与运算，即该位置的预测值由该范围内采样对象的测量
                                值决定。查找半径越大，生成的密度栅格越平滑且概化程度越高。值越小，生成的栅格所显示的信息越详细。

    :param float resolution: 密度分析结果栅格数据的分辨率
    :param Rectangle bounds: 密度分析的范围，用于确定运行结果所得到的栅格数据集的范围
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    >>> kernel_density(data_dir + 'example_data.udb/taxi', 'passenger_count', 0.01, 0.001, out_data=out_dir + 'density_result.udb'

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_density'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'KernelDensity')
                _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            param = _jvm.com.supermap.analyst.spatialanalyst.DensityAnalystParameter()
            if bounds is not None:
                param.setBounds(bounds._jobject)
            else:
                param.setBounds(_source_input.bounds._jobject)
            param.setResolution(float(resolution))
            param.setSearchRadius(float(search_radius))
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.kernelDensity(param, _source_input._jobject, value_field, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def point_density(input_data, value_field, resolution, neighbour_shape, neighbour_unit='CELL', bounds=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对点数据集进行点密度分析，并返回分析结果。
    简单点密度分析，即计算每个点的指定邻域形状内的每单位面积量值。计算方法为指定测量值除以邻域面积。点的邻域叠加处，其密度值也相加。
    每个输出栅格的密度均为叠加在栅格上的所有邻域密度值之和。结果栅格值的单位为原数据集单位的平方的倒数，即若原数据集单位为米，则结果栅格值的单位
    为每平方米。注意对于地理坐标数据集，结果栅格值的单位为“每平方度”，是没有实际意义的。

    :param input_data: 需要进行核密度分析的点数据集或线数据集。
    :type input_data: DatasetVector or str
    :param str value_field: 存储用于进行密度分析的测量值的字段名称。若传 None 则所有几何对象都按值为1处理。不支持文本类型的字段。
    :param float resolution: 密度分析结果栅格数据的分辨率
    :param neighbour_shape: 计算密度的查找邻域形状。如果输入值为 str，则要求格式为:
                            - 'CIRCLE,radius', 例如 'CIRCLE, 10'
                            - 'RECTANGLE,width,height'，例如 'RECTANGLE,5.0,10.0'
                            - 'ANNULUS,inner_radius,outer_radius'，例如 'ANNULUS,5.0,10.0'
                            - 'WEDGE,radius,start_angle,end_angle'，例如 'WEDGE,10.0,0,45'
    :type neighbour_shape: NeighbourShape or str
    :param neighbour_unit: 邻域统计的单位类型。可以使用栅格坐标或地理坐标。
    :type neighbour_unit: NeighbourUnitType or str
    :param Rectangle bounds: 密度分析的范围，用于确定运行结果所得到的栅格数据集的范围
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    >>> point_density(data_dir + 'example_data.udb/taxi', 'passenger_count', 0.0001, 'CIRCLE,0.001', 'MAP', out_data=out_dir + 'density_result.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_density'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'PointDensity')
                _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            param = _jvm.com.supermap.analyst.spatialanalyst.DensityAnalystParameter()
            if bounds is not None:
                param.setBounds(bounds._jobject)
            else:
                param.setBounds(_source_input.bounds._jobject)
            param.setResolution(float(resolution))
            java_neighbourShape = None
            if neighbour_shape is not None:
                if isinstance(neighbour_shape, NeighbourShape):
                    java_neighbourShape = neighbour_shape._jobject
                else:
                    if isinstance(neighbour_shape, str):
                        tokens = neighbour_shape.split(',')
                        if len(tokens) > 1:
                            shapeType = NeighbourShapeType._make(tokens[0])
                            if shapeType is NeighbourShapeType.RECTANGLE:
                                if len(tokens) >= 3:
                                    java_neighbourShape = NeighbourShapeRectangle(float(tokens[1]), float(tokens[2]))._jobject
                            elif shapeType is NeighbourShapeType.CIRCLE:
                                if len(tokens) >= 2:
                                    java_neighbourShape = NeighbourShapeCircle(float(tokens[1]))._jobject
                            elif shapeType is NeighbourShapeType.WEDGE:
                                if len(tokens) >= 4:
                                    java_neighbourShape = NeighbourShapeWedge(float(tokens[1]), float(tokens[2]), float(tokens[3]))._jobject
                            elif shapeType is NeighbourShapeType.ANNULUS:
                                if len(tokens) >= 3:
                                    java_neighbourShape = NeighbourShapeAnnulus(float(tokens[1]), float(tokens[2]))._jobject
            if java_neighbourShape is None:
                raise ValueError('neighbourShape is invalid')
            java_neighbourShape.setUnitType(NeighbourUnitType._make(neighbour_unit)._jobject)
            param.setSearchNeighbourhood(java_neighbourShape)
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.pointDensity(param, _source_input._jobject, value_field, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class _RasterClipFileType(JEnum):
    TIF = 103
    IMG = 101
    SIT = 204
    BMP = 121
    JPG = 122
    PNG = 123
    GIF = 124

    @classmethod
    def _get_java_class_type(cls):
        return 'com.supermap.analyst.spatialanalyst.RasterClipFileType'


def clip_raster(input_data, clip_region, is_clip_in_region=True, is_exact_clip=False, out_data=None, out_dataset_name=None, progress=None):
    """
    对栅格或影像数据集进行裁剪，结果存储为一个新的栅格或影像数据集。有时，我们的研究范围或者感兴趣区域较小，仅涉及当前栅格数据
    的一部分，这时可以对栅格数据进行裁剪，即通过一个 GeoRegion 对象作为裁剪区域对栅格数据进行裁剪，提取该区域内（外）的栅格数
    据生成一个新的数据集，此外，还可以选择进行精确裁剪或显示裁剪。

    :param input_data:  指定的要进行裁剪的数据集，支持栅格数据集和影像数据集。
    :type input_data: DatasetGrid or DatasetImage or str
    :param clip_region: 裁剪区域
    :type clip_region: GeoRegion or Rectangle
    :param bool is_clip_in_region: 是否对裁剪区内的数据集进行裁剪。若为 True，则对裁剪区域内的数据集进行裁剪，若为 False，则对裁剪区域外的数据集进行裁剪。
    :param bool is_exact_clip: 是否使用精确裁剪。若为 True，表示使用精确裁剪对栅格或影像数据集进行裁剪，False 表示使用显示裁剪:

                                - 采用显示裁剪时，系统会按照像素分块（详见 DatasetGrid.block_size_option、DatasetImage.block_size_option 方法）的大小,
                                  对栅格或影像数据集进行裁剪。此时只有裁剪区域内的数据被保留，即如果裁剪区的边界没有恰好与单元格的边界重合，那么单元格将被分割，
                                  位于裁剪区的部分会保留下来；位于裁剪区域外，且在被裁剪的那部分栅格所在块的总范围内的栅格仍有栅格值，但不显示。此种方式适用于大数据的裁剪。

                                - 采用精确裁剪时，系统在裁剪区域边界，会根据裁剪区域压盖的单元格的中心点的位置确定是否保留该单元格。如果使用区域内裁剪方式，单元格的中心点位于裁剪区内则保留，反之不保留。

    :param out_data: 结果数据集所在的数据源或直接生成 tif 文件
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称。如果设置直接生成 tif 文件，则此参数无效。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称或第三方影像文件路径。
    :rtype: DatasetGrid or DatasetImage or str

    >>> clip_region = Rectangle(875.5, 861.2, 1172.6, 520.9)
    >>> result = clip_raster(data_dir + 'example_data.udb/seaport', clip_region, True, False, out_data=out_dir + 'clip_seaport.tif')
    >>> result = clip_raster(data_dir + 'example_data.udb/seaport', clip_region, True, False, out_data=out_dir + 'clip_out.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, (DatasetGrid, DatasetImage)):
        raise ValueError('source input_data must be DatasetGrid or DatasetImage')
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'clip_raster')
                _jvm.com.supermap.analyst.spatialanalyst.RasterClip.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    if isinstance(clip_region, Rectangle):
        clip_region = clip_region.to_region()
    else:
        import os
        try:
            ext_name = os.path.basename(out_data).split('.')[(-1)]
        except:
            ext_name = None

        if ext_name is not None and ext_name.lower() in set(['tif', 'tiff']):
            try:
                if not isinstance(_source_input, DatasetImage):
                    raise ValueError('input_data must be DatasetImage')
                targetFileName = out_data
                ext_type = ext_name
                if ext_type == 'tiff':
                    ext_type = 'tif'
                targetFileType = _RasterClipFileType._make('TIF')
                java_result = _jvm.com.supermap.analyst.spatialanalyst.RasterClip.clip(_source_input._jobject, clip_region._jobject, bool(is_clip_in_region), targetFileName, targetFileType._jobject)
            except Exception as e:
                try:
                    log_error(e)
                    java_result = False
                finally:
                    e = None
                    del e

            if java_result:
                return targetFileName
            return
        else:
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _source_input.datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = _source_input.name + '_clip'
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
            try:
                try:
                    java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.RasterClip.clip(_source_input._jobject, clip_region._jobject, bool(is_clip_in_region), bool(is_exact_clip), _ds._jobject, _outDatasetName)
                except Exception as e:
                    try:
                        log_error(e)
                        java_result_dt = None
                    finally:
                        e = None
                        del e

            finally:
                if listener is not None:
                    try:
                        _jvm.com.supermap.analyst.spatialanalyst.RasterClip.removeSteppedListener(listener)
                    except Exception as e1:
                        try:
                            log_error(e1)
                        finally:
                            e1 = None
                            del e1

                    close_callback_server()
                elif java_result_dt is not None:
                    result_dt = _ds[java_result_dt.getName()]
                else:
                    result_dt = None
                if out_data is not None:
                    return try_close_output_datasource(result_dt, out_datasource)
                return result_dt


class InterpolationParameter(object):

    def __init__(self, bounds, resolution):
        self._type = None
        self._bounds = None
        self._resolution = None
        self.set_bounds(bounds).set_resolution(resolution)

    @property
    def type(self):
        """InterpolationAlgorithmType: 插值分支所支持的算法的类型 """
        return self._type

    @property
    def bounds(self):
        """Rectangle: 插值分析的范围，用于确定运行结果的范围"""
        return self._bounds

    def set_bounds(self, value):
        """
        设置插值分析的范围，用于确定运行结果的范围

        :param Rectangle value: 插值分析的范围，用于确定运行结果的范围
        :return: self
        :rtype: InterpolationParameter
        """
        self._bounds = value
        return self

    @property
    def resolution(self):
        """float: 插值运算时使用的分辨率"""
        return self._resolution

    def set_resolution(self, value):
        """
        设置插值运算时使用的分辨率。

        :param float value: 插值运算时使用的分辨率
        :return: self
        :rtype: InterpolationParameter
        """
        self._resolution = float(value)
        return self


class InterpolationDensityParameter(InterpolationParameter):
    __doc__ = '\n    点密度差值（Density）插值参数类。点密度插值方法，用于表达采样点的密度分布情况。\n    点密度插值的结果栅格的分辨率设置需要结合点数据集范围大小来取值，一般结果栅格行列值（即结果栅格数据集范围除以分辨率）在 500\n    以内即可以较好的体现出密度走势。由于点密度插值暂时只支持定长搜索模式，因此搜索半径（search_radius）值设置较为重要，此值需要用户根据待插值点数据分布状况和点数据集范围进行设置。\n    '

    def __init__(self, resolution, search_radius=0.0, expected_count=12, bounds=None):
        """
        构造点密度差值插值参数类对象

        :param float resolution: 插值运算时使用的分辨率
        :param float search_radius: 查找参与运算点的查找半径
        :param int expected_count: 期望参与插值运算的点数
        :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
        """
        InterpolationParameter.__init__(self, bounds, resolution)
        self._search_mode = SearchMode.KDTREE_FIXED_RADIUS
        self._search_radius = None
        self._expected_count = None
        self._type = InterpolationAlgorithmType.DENSITY
        self.set_search_radius(search_radius).set_expected_count(expected_count)

    @property
    def search_mode(self):
        """SearchMode: 在插值运算时，查找参与运算点的方式，只支持定长查找（KDTREE_FIXED_RADIUS）方式"""
        return self._search_mode

    @property
    def search_radius(self):
        """float: 查找参与运算点的查找半径"""
        return self._search_radius

    def set_search_radius(self, value):
        """
        设置查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置
        的未知数值时，会以该位置为圆心，以search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。

        :param float value: 查找参与运算点的查找半径
        :return: self
        :rtype: InterpolationDensityParameter
        """
        self._search_radius = float(value)
        return self

    @property
    def expected_count(self):
        """int: 返回期望参与插值运算的点数，表示期望参与运算的最少样点数"""
        return self._expected_count

    def set_expected_count(self, value):
        """
        设置期望参与插值运算的点数

        :param int value: 表示期望参与运算的最少样点数
        :return: self
        :rtype: InterpolationDensityParameter
        """
        self._expected_count = value
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.InterpolationDensityParameter()
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.expected_count:
            java_obj.setExpectedCount(self.expected_count)
        if self.resolution:
            java_obj.setResolution(self.resolution)
        if self.search_mode:
            java_obj.setSearchMode(self.search_mode._jobject)
        if self.search_radius:
            java_obj.setSearchRadius(self.search_radius)
        return java_obj


class InterpolationIDWParameter(InterpolationParameter):
    __doc__ = '\n    距离反比权值插值（Inverse Distance Weighted）参数类，\n    '

    def __init__(self, resolution, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, power=1, bounds=None):
        """
        构造 IDW 插值参数类。

        :param float resolution: 插值运算时使用的分辨率
        :param search_mode: 查找方式，不支持 QUADTREE
        :type search_mode: SearchMode or str
        :param float search_radius: 查找参与运算点的查找半径
        :param int expected_count: 期望参与插值运算的点数
        :param int power: 距离权重计算的幂次，幂次值越低，内插结果越平滑，幂次值越高，内插结果细节越详细。此参数应为一个大于0的值。如果不指定此参数，方法缺省将其设置为1
        :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
        """
        InterpolationParameter.__init__(self, bounds, resolution)
        self._search_mode = SearchMode.KDTREE_FIXED_RADIUS
        self._search_radius = None
        self._expected_count = None
        self._power = 1
        self._type = InterpolationAlgorithmType.IDW
        self.set_search_mode(search_mode)
        self.set_search_radius(search_radius)
        self.set_expected_count(expected_count)
        self.set_power(power)

    @property
    def search_mode(self):
        """SearchMode: 在插值运算时，查找参与运算点的方式，不支持 QUADTREE"""
        return self._search_mode

    def set_search_mode(self, value):
        """
        设置在插值运算时，查找参与运算点的方式。不支持 QUADTREE

        :param value: 在插值运算时，查找参与运算点的方式
        :type value:  SearchMode or str
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._search_mode = SearchMode._make(value)
        return self

    @property
    def search_radius(self):
        """float: 查找参与运算点的查找半径"""
        return self._search_radius

    def set_search_radius(self, value):
        """
        设置查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置
        的未知数值时，会以该位置为圆心，以search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。

        如果设置 search_mode 为KDTREE_FIXED_COUNT，同时指定查找参与运算点的范围，当查找范围内的点数小于指定的点数时赋为空值，当查找范围内的点数
        大于指定的点数时，则返回距离插值点最近的指定个数的点进行插值。

        :param float value: 查找参与运算点的查找半径
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._search_radius = float(value)
        return self

    @property
    def expected_count(self):
        """int: 期望参与插值运算的点数，如果设置 search_mode 为 KDTREE_FIXED_RADIUS ，同时指定参与插值运算点的个数，当查找范围内的点数小于指定的点数时赋为空值。 """
        return self._expected_count

    def set_expected_count(self, value):
        """
        设置期望参与插值运算的点数。如果设置 search_mode 为 KDTREE_FIXED_RADIUS ，同时指定参与插值运算点的个数，当查找范围内的点数小于指定的点数时赋为空值。

        :param int value: 表示期望参与运算的最少样点数
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._expected_count = value
        return self

    @property
    def power(self):
        """int: 距离权重计算的幂次"""
        return self._power

    def set_power(self, value):
        """
        设置距离权重计算的幂次。幂次值越低，内插结果越平滑，幂次值越高，内插结果细节越详细。此参数应为一个大于0的值。如果不指定此参数，方法缺省
        将其设置为1。

        :param int value: 距离权重计算的幂次
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._power = int(value)
        return self

    @property
    def _jobject(self):
        """ Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.InterpolationIDWParameter()
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.expected_count:
            java_obj.setExpectedCount(self.expected_count)
        if self.resolution:
            java_obj.setResolution(self.resolution)
        if self.search_mode:
            java_obj.setSearchMode(self.search_mode._jobject)
        if self.search_radius:
            java_obj.setSearchRadius(self.search_radius)
        if self.power:
            java_obj.setPower(self.power)
        return java_obj


class InterpolationKrigingParameter(InterpolationParameter):
    __doc__ = '\n    克吕金（Kriging）内插法参数。\n\n    Kriging 法为地质统计学上一种空间资料内插处理方法，主要的目的是利用各数据点间变异数（variance）的大小来推求某一未知点与各已知点的权重关系，再\n    由各数据点的值和其与未知点的权重关系推求未知点的值。Kriging 法最大的特色不仅是提供一个最小估计误差的预测值，并且可明确的指出误差值的大小。一般\n    而言，许多地质参数，如地形面本身即具有连续的性质，故在一短距离内的任两点必有空间上的关系。反之，在一不规则面上的两点若相距甚远，则在统计意义上可\n    视为互为独立 (stastically indepedent)，这种随距离而改变的空间上连续性，可用半变异图 (semivariogram) 来表现。因此，若想由已知的散乱点来\n    推求某一未知点的值，则可利用半变异图推求各已知点及欲求值点的空间关系。再由此空间参数推求半变异数，由各数据点间的半变异数可推求未知点与已知点间的\n    权重关系，进而推求出未知点的值。克吕金法的优点是以空间统计学作为其坚实的理论基础。物理含义明确；不但能估计测定参数的空间变异分布，而且还可以估算\n    参数的方差分布。克吕金法的缺点是计算步骤较烦琐，计算量大，且变异函数有时需要根据经验人为选定。\n\n    克吕金插值法可以采用两种方式来获取参与插值的采样点，进而获得相应位置点的预测值，一个是在待计算预测值位置点周围一定范围内，获取该范围内的所有采样\n    点，通过特定的插值计算公式获得该位置点的预测值；另一个是在待计算预测值位置点周围获取一定数目的采样点，通过特定的插值计算公式获得该位置点的预测值。\n\n    克吕金插值过程是一个多步骤的处理过程，包括:\n        - 创建变异图和协方差函数来估计统计相关（也称为空间自相关）的值；\n        - 预测待计算位置点的未知值。\n\n    半变异函数与半变异图:\n        - 计算所有采样点中相距 h 个单位的任意两点的半变异函数值，那么任意两点的距离 h 一般是唯一的，将所有的点对的距离与相应的半变函数值快速显示在以 h\n          为 X 坐标轴和以半变函数值为 Y 坐标轴的坐标空间内，就得到了半变异图。相距距离愈小的点其半变异数愈小，而随着距离的增加，任两点间的空间相依关系愈\n          小，使得半变异函数值趋向于一稳定值。此稳定值我们称之为基台值（Sill）；而达到基台值时的最小 h 值称之为自相关阈值（Range）。\n\n    块金效应:\n        - 当点间距离为 0（比如，步长=0）时，半变函数值为 0。然而，在一个无限小的距离内，半变函数通常显示出块金效应，这是一个大于 0 的值。如果半变函数\n          在Y周上的截距式 2 ，则块金效应值为 2。\n        - 块金效应属于测量误差，或者是小于采样步长的小距离上的空间变化，或者两者兼而有之。测量误差主要是由于观测仪器的内在误差引起的。自然现象的空间变异\n          范围很大（可以在很小的尺度上，也可以在很大的尺度上）。小于步长尺度上的变化就表现为块金的一部分。\n\n    半变异图的获得是进行空间插值预测的关键步骤之一，克吕金法的主要应用之一就是预测非采样点的属性值，半变异图提供了采样点的空间自相关信息，根据半变\n    异图，选择合适的半变异模型，即拟合半变异图的曲线模型。\n\n    不同的模型将会影响所获得的预测结果，如果接近原点处的半变异函数曲线越陡，则较近领域对该预测值的影响就越大。因此输出表面就会越不光滑。\n\n    SuperMap 支持的半变函数模型有指数型、球型和高斯型。详细信息参见 VariogramMode 类\n\n    '

    def __init__(self, resolution, krighing_type=InterpolationAlgorithmType.KRIGING, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, max_point_count_in_node=50, max_point_count_for_interpolation=200, variogram=VariogramMode.SPHERICAL, angle=0.0, mean=0.0, exponent=Exponent.EXP1, nugget=0.0, range_value=0.0, sill=0.0, bounds=None):
        """
        构造 克吕金插值参数对象。

        :param float resolution: 插值运算时使用的分辨率
        :param krighing_type: 插值分析的算法类型。支持设置 KRIGING, SimpleKRIGING, UniversalKRIGING 三种，默认使用 KRIGING。
        :type krighing_type: InterpolationAlgorithmType or str
        :param search_mode: 查找模式。
        :type search_mode: SearchMode or str
        :param float search_radius:  查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与
                                     运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，search_radius 为半径，落在这个范围内的
                                     采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
        :param int expected_count:  期望参与插值运算的点数，当查找方式为变长查找时，表示期望参与运算的最多样点数。
        :param int max_point_count_in_node: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。
        :param int max_point_count_for_interpolation: 设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数
        :param variogram:  克吕金（Kriging）插值时的半变函数类型。默认值为 VariogramMode.SPHERICAL
        :type variogram: VariogramMode or str
        :param float angle:  克吕金算法中旋转角度值
        :param float mean: 插值字段的平均值，即采样点插值字段值总和除以采样点数目。
        :param exponent: 用于插值的样点数据中趋势面方程的阶数
        :type exponent: Exponent or str
        :param float nugget: 块金效应值。
        :param float range_value: 自相关阈值。
        :param float sill: 基台值
        :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
        """
        InterpolationParameter.__init__(self, bounds, resolution)
        self._search_mode = None
        self._search_radius = None
        self._expected_count = None
        self._max_point_count_in_node = None
        self._max_point_count_for_interpolation = None
        self._variogram_mode = None
        self._angle = None
        self._mean = None
        self._exponent = None
        self._nugget = None
        self._range = None
        self._sill = None
        self._type = InterpolationAlgorithmType._make(krighing_type)
        if self._type not in (InterpolationAlgorithmType.KRIGING,
         InterpolationAlgorithmType.SIMPLEKRIGING,
         InterpolationAlgorithmType.UNIVERSALKRIGING):
            raise ValueError('Only Support KRIGING, SimpleKRIGING and UniversalKRIGING, but now is ' + str(self._type))
        self.set_search_mode(search_mode)
        self.set_search_radius(search_radius)
        self.set_expected_count(expected_count)
        self.set_max_point_count_in_node(max_point_count_in_node)
        self.set_max_point_count_for_interpolation(max_point_count_for_interpolation)
        self.set_variogram_mode(variogram)
        self.set_angle(angle)
        self.set_mean(mean)
        self.set_exponent(exponent)
        self.set_nugget(nugget)
        self.set_range(range_value)
        self.set_sill(sill)

    @property
    def max_point_count_in_node(self):
        """int:  单个块内最多查找点数"""
        return self._max_point_count_in_node

    def set_max_point_count_in_node(self, value):
        """
        设置单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。

        :param int value: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._max_point_count_in_node = int(value)
        return self

    @property
    def max_point_count_for_interpolation(self):
        """int:块查找时，最多参与插值的点数 """
        return self._max_point_count_for_interpolation

    def set_max_point_count_for_interpolation(self, value):
        """
        设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数

        :param int value: 块查找时，最多参与插值的点数
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._max_point_count_for_interpolation = int(value)
        return self

    @property
    def variogram_mode(self):
        """VariogramMode: 克吕金（Kriging）插值时的半变函数类型。默认值为 VariogramMode.SPHERICAL"""
        return self._variogram_mode

    def set_variogram_mode(self, value):
        """
        设置克吕金（Kriging）插值时的半变函数类型。默认值为 VariogramMode.SPHERICAL

        :param value: 克吕金（Kriging）插值时的半变函数类型
        :type value: VariogramMode or
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._variogram_mode = VariogramMode._make(value)
        return self

    @property
    def angle(self):
        """float: 克吕金算法中旋转角度值"""
        return self._angle

    def set_angle(self, value):
        """
        设置克吕金算法中旋转角度值

        :param float value: 克吕金算法中旋转角度值
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._angle = float(value)
        return self

    @property
    def mean(self):
        """float: 插值字段的平均值，即采样点插值字段值总和除以采样点数目。"""
        return self._mean

    def set_mean(self, value):
        """
        设置插值字段的平均值，即采样点插值字段值总和除以采样点数目。

        :param float value: 插值字段的平均值，即采样点插值字段值总和除以采样点数目。
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._mean = float(value)
        return self

    @property
    def exponent(self):
        """Exponent: 用于插值的样点数据中趋势面方程的阶数"""
        return self._exponent

    def set_exponent(self, value):
        """
        设置用于插值的样点数据中趋势面方程的阶数

        :param value: 用于插值的样点数据中趋势面方程的阶数
        :type value: Exponent or str
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._exponent = Exponent._make(value)
        return self

    @property
    def nugget(self):
        """float:  块金效应值。"""
        return self._nugget

    def set_nugget(self, value):
        """
        设置块金效应值。

        :param float value: 块金效应值。
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._nugget = float(value)
        return self

    @property
    def range(self):
        """float: 自相关阈值"""
        return self._range

    def set_range(self, value):
        """
        设置自相关阈值

        :param float value: 自相关阈值
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._range = float(value)
        return self

    @property
    def sill(self):
        """float: 基台值"""
        return self._sill

    def set_sill(self, value):
        """
        设置基台值

        :param float value: 基台值
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._sill = float(value)
        return self

    @property
    def search_mode(self):
        """SearchMode: 在插值运算时，查找参与运算点的方式"""
        return self._search_mode

    def set_search_mode(self, value):
        """
        设置在插值运算时，查找参与运算点的方式

        :param value: 在插值运算时，查找参与运算点的方式
        :type value:  SearchMode or str
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._search_mode = SearchMode._make(value)
        return self

    @property
    def search_radius(self):
        """float: 查找参与运算点的查找半径"""
        return self._search_radius

    def set_search_radius(self, value):
        """
        设置查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置
        的未知数值时，会以该位置为圆心，以 search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。

        查找模式设置为“变长查找”（KDTREE_FIXED_COUNT），将使用最大查找半径范围内的固定数目的样点值进行插值，最大查找半径为点数据集的区域范围对
        应的矩形的对角线长度的 0.2 倍。

        :param float value: 查找参与运算点的查找半径
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._search_radius = float(value)
        return self

    @property
    def expected_count(self):
        """int: 期望参与插值运算的点数 """
        return self._expected_count

    def set_expected_count(self, value):
        """
        设置期望参与插值运算的点数

        :param int value: 表示期望参与运算的最少样点数
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._expected_count = int(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.InterpolationKrigingParameter(self.type._jobject)
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.expected_count:
            java_obj.setExpectedCount(self.expected_count)
        if self.resolution:
            java_obj.setResolution(self.resolution)
        if self.search_mode:
            java_obj.setSearchMode(self.search_mode._jobject)
        if self.search_radius:
            java_obj.setSearchRadius(self.search_radius)
        if self.search_mode == SearchMode.QUADTREE:
            if self.max_point_count_in_node:
                java_obj.setMaxPointCountInNode(self.max_point_count_in_node)
            if self.max_point_count_for_interpolation:
                java_obj.setMaxPointCountForInterpolation(self.max_point_count_for_interpolation)
        if self.variogram_mode:
            java_obj.setVariogramMode(self.variogram_mode._jobject)
        if self.angle:
            if self.search_mode != SearchMode.QUADTREE:
                java_obj.setAngle(self.angle)
        if self.type == InterpolationAlgorithmType.SIMPLEKRIGING:
            if self.mean:
                java_obj.setMean(self.mean)
        if self.type == InterpolationAlgorithmType.UNIVERSALKRIGING:
            if self.exponent:
                java_obj.setExponent(self.exponent._jobject)
        if self.nugget:
            java_obj.setNugget(self.nugget)
        if self.range:
            java_obj.setRange(self.range)
        if self.sill:
            java_obj.setSill(self.sill)
        if self.bounds:
            java_obj.setBounds(self.bounds._jobject)
        return java_obj


class InterpolationRBFParameter(InterpolationParameter):
    __doc__ = '\n    径向基函数 RBF（Radial Basis Function）插值法参数类\n    '

    def __init__(self, resolution, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, max_point_count_in_node=50, max_point_count_for_interpolation=200, smooth=0.100000001490116, tension=40, bounds=None):
        """
        构造径向基函数插值法参数类对象。

        :param float resolution: 插值运算时使用的分辨率
        :param search_mode: 查找模式。
        :type search_mode: SearchMode or str
        :param float search_radius:  查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与
                                     运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，search_radius 为半径，落在这个范围内的
                                     采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
        :param int expected_count:  期望参与插值运算的点数，当查找方式为变长查找时，表示期望参与运算的最多样点数。
        :param int max_point_count_in_node: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。
        :param int max_point_count_for_interpolation: 设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数
        :param float smooth: 光滑系数，值域为 [0,1]
        :param float tension: 张力系数
        :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
        """
        InterpolationParameter.__init__(self, bounds, resolution)
        self._search_mode = None
        self._search_radius = None
        self._expected_count = None
        self._max_point_count_in_node = None
        self._max_point_count_for_interpolation = None
        self._smooth = None
        self._tension = None
        self._type = InterpolationAlgorithmType.RBF
        self.set_search_mode(search_mode)
        self.set_search_radius(search_radius)
        self.set_expected_count(expected_count)
        self.set_max_point_count_in_node(max_point_count_in_node)
        self.set_max_point_count_for_interpolation(max_point_count_for_interpolation)
        self.set_smooth(smooth)
        self.set_tension(tension)

    @property
    def smooth(self):
        """float: 光滑系数"""
        return self._smooth

    def set_smooth(self, value):
        """
        设置光滑系数

        :param float value: 光滑系数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        if value is not None:
            self._smooth = float(value)
        return self

    @property
    def tension(self):
        """float: 张力系数"""
        return self._tension

    def set_tension(self, value):
        """
        设置张力系数

        :param float value: 张力系数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._tension = float(value)
        return self

    @property
    def max_point_count_in_node(self):
        """int:  单个块内最多查找点数"""
        return self._max_point_count_in_node

    def set_max_point_count_in_node(self, value):
        """
        设置单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。

        :param int value: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._max_point_count_in_node = int(value)
        return self

    @property
    def max_point_count_for_interpolation(self):
        """int:块查找时，最多参与插值的点数 """
        return self._max_point_count_for_interpolation

    def set_max_point_count_for_interpolation(self, value):
        """
        设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数

        :param int value: 块查找时，最多参与插值的点数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._max_point_count_for_interpolation = int(value)
        return self

    @property
    def search_mode(self):
        """SearchMode: 在插值运算时，查找参与运算点的方式，不支持 KDTREE_FIXED_RADIUS """
        return self._search_mode

    def set_search_mode(self, value):
        """
        设置在插值运算时，查找参与运算点的方式。

        :param value: 在插值运算时，查找参与运算点的方式
        :type value:  SearchMode or str
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._search_mode = SearchMode._make(value)
        return self

    @property
    def search_radius(self):
        """float: 查找参与运算点的查找半径"""
        return self._search_radius

    def set_search_radius(self, value):
        """
        设置查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置
        的未知数值时，会以该位置为圆心，以 search_radiu s为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。

        查找模式设置为“变长查找”（KDTREE_FIXED_COUNT），将使用最大查找半径范围内的固定数目的样点值进行插值，最大查找半径为点数据集的区域范围对
        应的矩形的对角线长度的 0.2 倍。

        :param float value: 查找参与运算点的查找半径
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._search_radius = float(value)
        return self

    @property
    def expected_count(self):
        """int: 期望参与插值运算的点数 """
        return self._expected_count

    def set_expected_count(self, value):
        """
        设置期望参与插值运算的点数

        :param int value: 表示期望参与运算的最少样点数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._expected_count = int(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.InterpolationRBFParameter()
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.expected_count:
            java_obj.setExpectedCount(self.expected_count)
        if self.resolution:
            java_obj.setResolution(self.resolution)
        if self.search_mode:
            java_obj.setSearchMode(self.search_mode._jobject)
        if self.search_radius:
            java_obj.setSearchRadius(self.search_radius)
        if self.search_mode == SearchMode.QUADTREE:
            if self.max_point_count_in_node:
                java_obj.setMaxPointCountInNode(self.max_point_count_in_node)
            if self.max_point_count_for_interpolation:
                java_obj.setMaxPointCountForInterpolation(self.max_point_count_for_interpolation)
        if self.smooth:
            java_obj.setSmooth(self.smooth)
        if self.tension:
            java_obj.setTension(self.tension)
        return java_obj


def interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    插值分析类。该类提供插值分析功能，用于对离散的点数据进行插值得到栅格数据集。插值分析可以将有限的采样点数据，通过插值对采样点周围的数值情况进行预测，
    从而掌握研究区域内数据的总体分布状况，而使采样的离散点不仅仅反映其所在位置的数值情况，而且可以反映区域的数值分布。

    为什么要进行插值？

    由于地理空间要素之间存在着空间关联性，即相互邻近的事物总是趋于同质，也就是具有相同或者相似的特征，举个例子，街道的一边下雨了，那么街道的另一边在大
    多数情况下也一定在下雨，如果在更大的区域范围，一个乡镇的气候应当与其接壤的另一的乡镇的气候相同，等等，基于这样的推理，我们就可以利用已知地点的信息
    来间接获取与其相邻的其他地点的信息，而插值分析就是基于这样的思想产生的，也是插值重要的应用价值之一。

    将某个区域的采样点数据插值生成栅格数据，实际上是将研究区域按照给定的格网尺寸（分辨率）进行栅格化，栅格数据中每一个栅格单元对应一块区域，栅格单元的
    值由其邻近的采样点的数值通过某种插值方法计算得到，因此，就可以预测采样点周围的数值情况，进而了解整个区域的数值分布情况。其中，插值方法主要有距离反
    比权值插值法、克吕金（Kriging）内插法、径向基函数RBF（Radial Basis Function）插值。
    利用插值分析功能能够预测任何地理点数据的未知值，如高程、降雨量、化学物浓度、噪声级等等。

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param InterpolationParameter parameter: 插值方法需要的参数信息
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float z_value_scale: 插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, (DatasetVector, Recordset)):
            raise ValueError('source input_data must be DatasetVector or Recordset')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            if isinstance(_source_input, DatasetVector):
                _outDatasetName = _source_input.name + '_interpolate'
            else:
                _outDatasetName = _source_input.dataset.name + '_interpolate'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'Interpolate')
                _jvm.com.supermap.analyst.spatialanalyst.Interpolator.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.Interpolator.interpolate(parameter._jobject, _source_input._jobject, str(z_value_field), float(z_value_scale), _ds._jobject, _outDatasetName, PixelFormat._make(pixel_format)._jobject)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.Interpolator.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def interpolate_points(points, values, parameter, pixel_format, prj, out_data, z_value_scale=1.0, out_dataset_name=None, progress=None):
    """
    对点数组进行插值分析，并返回分析结果

    :param points: 需要进行插值分析的点数据
    :type points: list[Point2D]
    :param values:  点数组对应的用于插值分析的值。
    :type values: list[float]
    :param InterpolationParameter parameter:  插值方法需要的参数信息
    :param  pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param PrjCoordSys prj: 点数组的坐标系统。生成的结果数据集也参照该坐标系统。
    :param out_data:  结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param float z_value_scale: 插值分析值的缩放比率
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    """
    check_lic()
    if not isinstance(points, (list, tuple)):
        raise ValueError('source input_data must be list or tuple')
    if len(points) != len(values):
        raise ValueError('The count of points or values must be equal.')
    if out_data is None:
        raise ValueError('out_data cannot be None')
    if prj is None:
        raise ValueError('prj cannot be None')
    else:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        _ds = out_datasource
        if out_dataset_name is None:
            _outDatasetName = 'point_interpolate'
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
        _jvm = get_jvm()
        listener = None
        if progress is not None and safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'interpolate_points')
                _jvm.com.supermap.analyst.spatialanalyst.Interpolator.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

            try:
                try:
                    _points = to_java_point2d_array(points)
                    _values = to_java_double_array(values)
                    if prj is not None:
                        java_prj = prj._jobject
                    else:
                        java_prj = None
                    java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.Interpolator.interpolateparameter._jobject_points_valuesjava_prjfloat(z_value_scale)_ds._jobject_outDatasetNamePixelFormat._make(pixel_format)._jobject
                except Exception as e:
                    try:
                        log_error(e)
                        java_result_dt = None
                    finally:
                        e = None
                        del e

            finally:
                return

            if listener is not None:
                try:
                    _jvm.com.supermap.analyst.spatialanalyst.Interpolator.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            if java_result_dt is not None:
                result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
    return try_close_output_datasource(result_dt, out_datasource)


def idw_interpolate(input_data, z_value_field, pixel_format, resolution, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, power=1, bounds=None, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    使用 IDW 插值方法对点数据集或记录集进行插值。具体参考 :py:meth:`interpolate` 和 :py:class:`.InterpolationIDWParameter`

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float resolution: 插值运算时使用的分辨率
    :param search_mode: 插值运算时，查找参与运算点的方式。不支持 QUADTREE
    :type search_mode: SearchMode or str
    :param float search_radius: 查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，以search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
                                如果设置 search_mode 为KDTREE_FIXED_COUNT，同时指定查找参与运算点的范围，当查找范围内的点数小于指定的点数时赋为空值，当查找范围内的点数大于指定的点数时，则返回距离插值点最近的指定个数的点进行插值。
    :param int expected_count: 期望参与插值运算的点数。如果设置 search_mode 为 KDTREE_FIXED_RADIUS ，同时指定参与插值运算点的个数，当查找范围内的点数小于指定的点数时赋为空值。
    :param int power: 距离权重计算的幂次。幂次值越低，内插结果越平滑，幂次值越高，内插结果细节越详细。此参数应为一个大于0的值。如果不指定此参数，方法缺省将其设置为1。
    :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
    :param float z_value_scale: 插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    parameter = InterpolationIDWParameter(resolution, search_mode, search_radius, expected_count, power, bounds)
    return interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale, out_data, out_dataset_name, progress)


def density_interpolate(input_data, z_value_field, pixel_format, resolution, search_radius=0.0, expected_count=12, bounds=None, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    使用点密度插值方法对点数据集或记录集进行插值。具体参考 :py:meth:`interpolate` 和 :py:class:`.InterpolationDensityParameter`

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float resolution: 插值运算时使用的分辨率
    :param float search_radius: 查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，以search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
    :param int expected_count: 期望参与插值运算的点数
    :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
    :param float z_value_scale:  插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    parameter = InterpolationDensityParameterresolutionsearch_radiusexpected_countbounds
    return interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale, out_data, out_dataset_name, progress)


def kriging_interpolate(input_data, z_value_field, pixel_format, resolution, krighing_type='KRIGING', search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, max_point_count_in_node=50, max_point_count_for_interpolation=200, variogram_mode=VariogramMode.SPHERICAL, angle=0.0, mean=0.0, exponent=Exponent.EXP1, nugget=0.0, range_value=0.0, sill=0.0, bounds=None, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    使用克吕金插值方法对点数据集或记录集进行插值。具体参考 :py:meth:`interpolate` 和 :py:class:`.InterpolationKrigingParameter`

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float resolution: 插值运算时使用的分辨率
    :param krighing_type: 插值分析的算法类型。支持设置 KRIGING, SimpleKRIGING, UniversalKRIGING 三种，默认使用 KRIGING。
    :type krighing_type: InterpolationAlgorithmType or str
    :param search_mode: 查找模式。
    :type search_mode: SearchMode or str
    :param float search_radius:  查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与
                                     运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，search_radius 为半径，落在这个范围内的
                                     采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
    :param int expected_count:  期望参与插值运算的点数，当查找方式为变长查找时，表示期望参与运算的最多样点数。
    :param int max_point_count_in_node: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。
    :param int max_point_count_for_interpolation: 设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数
    :param variogram:  克吕金（Kriging）插值时的半变函数类型。默认值为 VariogramMode.SPHERICAL
    :type variogram: VariogramMode or str
    :param float angle:  克吕金算法中旋转角度值
    :param float mean: 插值字段的平均值，即采样点插值字段值总和除以采样点数目。
    :param exponent: 用于插值的样点数据中趋势面方程的阶数
    :type exponent: Exponent or str
    :param float nugget: 块金效应值。
    :param float range_value: 自相关阈值。
    :param float sill: 基台值
    :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
    :param float z_value_scale: 插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    parameter = InterpolationKrigingParameter(resolution, krighing_type, search_mode, search_radius, expected_count, max_point_count_in_node, max_point_count_for_interpolation, variogram_mode, angle, mean, exponent, nugget, range_value, sill, bounds)
    return interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale, out_data, out_dataset_name, progress)


def rbf_interpolate(input_data, z_value_field, pixel_format, resolution, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, max_point_count_in_node=50, max_point_count_for_interpolation=200, smooth=0.100000001490116, tension=40, bounds=None, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    使用径向基函数（RBF） 插值方法对点数据集或记录集进行插值。具体参考 :py:meth:`interpolate` 和 :py:class:`.InterpolationRBFParameter`

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float resolution: 插值运算时使用的分辨率
    :param search_mode: 查找模式。
    :type search_mode: SearchMode or str
    :param float search_radius: 查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，search_radius 为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
    :param int expected_count: 期望参与插值运算的点数，当查找方式为变长查找时，表示期望参与运算的最多样点数。
    :param int max_point_count_in_node: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。
    :param int max_point_count_for_interpolation: 设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数
    :param float smooth: 光滑系数，值域为 [0,1]
    :param float tension: 张力系数
    :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
    :param float z_value_scale: 插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    parameter = InterpolationRBFParameter(resolution, search_mode, search_radius, expected_count, max_point_count_in_node, max_point_count_for_interpolation, smooth, tension, bounds)
    return interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale, out_data, out_dataset_name, progress)


def vector_to_raster(input_data, value_field, clip_region=None, cell_size=None, pixel_format=PixelFormat.SINGLE, out_data=None, out_dataset_name=None, progress=None):
    """
    通过指定转换参数设置将矢量数据集转换为栅格数据集。

    :param input_data: 待转换的矢量数据集。支持点、线和面数据集
    :type input_data: DatasetVector or str
    :param str value_field: 矢量数据集中存储栅格值的字段
    :param clip_region: 转换的有效区域
    :type clip_region: GeoRegion or Rectangle
    :param float cell_size: 结果栅格数据集的单元格大小
    :param pixel_format: 如果将矢量数据转为像素格式 为 UBIT1、UBIT4 和 UBIT8 的栅格数据集，矢量数据中值为 0 的对象在结果栅格中会丢失。
    :type pixel_format: PixelFormat or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_raster'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setValueFieldName(value_field)
            if clip_region is not None:
                if isinstance(clip_region, Rectangle):
                    clip_region = clip_region.to_region()
                if isinstance(clip_region, GeoRegion):
                    parameter.setClipRegion(clip_region._jobject)
            if cell_size is not None:
                parameter.setCellSize(float(cell_size))
            if pixel_format is not None:
                parameter.setPixelFormat(PixelFormat._make(pixel_format)._jobject)
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setTargetDatasetName(_outDatasetName)
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'VectorToRaster')
                        _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.vectorToRaster(parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def raster_to_vector(input_data, value_field, out_dataset_type=DatasetType.POINT, back_or_no_value=-9999, back_or_no_value_tolerance=0.0, specifiedvalue=None, specifiedvalue_tolerance=0.0, valid_region=None, is_thin_raster=True, smooth_method=None, smooth_degree=0.0, out_data=None, out_dataset_name=None, progress=None):
    """
    通过指定转换参数设置将栅格数据集转换为矢量数据集。

    :param input_data: 待转换的栅格数据集或影像数据集
    :type input_data: DatasetGrid or DatasetImage or str
    :param str value_field:  结果矢量数据集中存储值的字段
    :param out_dataset_type: 结果数据集类型，支持点、线和面数据集。当结果数据集类型为线数据聚集时，is_thin_raster, smooth_method, smooth_degree 才有效。
    :type out_dataset_type: DatasetType or str
    :param back_or_no_value: 设置栅格的背景色或表示无值的值，只在栅格转矢量时有效。 允许用户指定一个值来标识那些不需要转换的单元格:

                              - 当被转换的栅格数据为栅格数据集时，栅格值为指定的值的单元格被视为无值，这些单元格不会被转换，而栅格的原无值将作为有效值来参与转换。
                              - 当被转化的栅格数据为影像数据集时，栅格值为指定的值的单元格被视为背景色，从而不参与转换。

                             需要注意，影像数据集中栅格值代表的是一个颜色或颜色的索引值，与其像素格式（PixelFormat）有关。对于 BIT32、UBIT32、RGBA、RGB 和 BIT16

                             格式的影像数据集，其栅格值对应为 RGB 颜色，可以使用一个 tuple 或 int 来表示 RGB 值 或 RGBA 值

                             对于 UBIT8 和 UBIT4 格式的影像数据集，其栅格值对应的是颜色的索引值，因此，应为该属性设置的值为被视为背景色的颜色对应的索引值。
    :type back_or_no_value: int or tuple
    :param back_or_no_value_tolerance: 栅格背景色的容限或无值的容限，只在栅格转矢量时有效。用于配合 back_or_no_value 方法（指定栅格无值或者背景色）来共同确定栅格数据中哪些值不被转换:

                                        - 当被转换的栅格数据为栅格数据集时，如果指定为无值的值为 a，指定的无值的容限为 b，则栅格值在[a-b,a+b]范围内的单元格均被视为无值。需要注意，无值的容限是用户指定的无值的值的容限，与栅格中原无值无关。
                                        - 当被转化的栅格数据为影像数据集时，该容限值为一个32位整型值或tuple，tuple用于表示 RGB值或RGBA值。
                                        - 该值代表的意义与影像数据集的像素格式有关：对于栅格值对应 RGB 颜色的影像数据集，该值在系统内部被转为分别对应 R、G、B 的三个容限值，
                                          例如，指定为背景色的颜色为(100,200,60)，指定的容限值为329738，该值对应的 RGB 值为(10,8,5)，则值在 (90,192,55) 和 (110,208,65)
                                          之间的颜色均为背景色；对于栅格值为颜色索引值的影像数据集，该容限值为颜色索引值的容限，在该容限范围内的栅格值均视为背景色。

    :type back_or_no_value_tolerance: int or float or tuple
    :param specifiedvalue: 栅格按值转矢量时指定的栅格值。只将具有该值的栅格转为矢量。
    :type specifiedvalue: int or float or tuple
    :param specifiedvalue_tolerance: 栅格按值转矢量时指定的栅格值的容限
    :type specifiedvalue_tolerance: int or float or tuple
    :param valid_region: 转换的有效区域
    :type valid_region: GeoRegion or Rectangle
    :param bool is_thin_raster: 转换之前是否进行栅格细化。
    :param smooth_method: 光滑方法，只在栅格转为矢量线数据时有效
    :type smooth_method: SmoothMethod or str
    :param int smooth_degree: 光滑度。光滑度的值越大，光滑度的值越大，则结果矢量线的光滑度越高。当 smooth_method 不为 NONE 时有效。光滑度的有效取值与光滑方法有关，光滑方法有 B 样条法和磨角法:

                                - 光滑方法为 B 样条法时，光滑度的有效取值为大于等于2的整数，建议取值范围为[2,10]。
                                - 光滑方法为磨角法时，光滑度代表一次光滑过程中磨角的次数，设置为大于等于1的整数时有效

    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, (DatasetGrid, DatasetImage)):
            raise ValueError('source input_data must be DatasetGrid or DatasetImage')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_vector'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setValueFieldName(value_field)
            if out_dataset_type is not None:
                parameter.setTargetDatasetType(DatasetType._make(out_dataset_type)._jobject)
            if back_or_no_value is not None:
                if isinstance(back_or_no_value, tuple):
                    back_or_no_value = tuple_to_color(back_or_no_value)
                parameter.setBackOrNoValue(int(back_or_no_value))
            if back_or_no_value_tolerance is not None:
                if isinstance(back_or_no_value_tolerance, tuple):
                    back_or_no_value_tolerance = tuple_to_color(back_or_no_value_tolerance)
                parameter.setBackOrNoValueTolerance(float(back_or_no_value_tolerance))
            if specifiedvalue is not None:
                if isinstance(specifiedvalue, tuple):
                    specifiedvalue = tuple_to_color(specifiedvalue)
                parameter.setSpecifiedValue(int(specifiedvalue))
            if specifiedvalue_tolerance is not None:
                if isinstance(specifiedvalue_tolerance, tuple):
                    specifiedvalue_tolerance = tuple_to_color(specifiedvalue_tolerance)
                parameter.setSpecifiedValueTolerance(float(specifiedvalue_tolerance))
            if is_thin_raster is not None:
                parameter.setThinRaster(bool(is_thin_raster))
            if smooth_method is not None:
                parameter.setSmoothMethod(SmoothMethod._make(smooth_method)._jobject)
            if smooth_degree is not None:
                parameter.setSmoothDegree(int(smooth_degree))
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setTargetDatasetName(_outDatasetName)
            if valid_region is not None:
                if isinstance(valid_region, Rectangle):
                    valid_region = valid_region.to_region()
            if isinstance(valid_region, GeoRegion):
                parameter.setClipRegion(oj(valid_region))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'RasterToVector')
                        _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.rasterToVector(parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def cost_distance(input_data, cost_grid, max_distance=-1.0, cell_size=None, out_data=None, out_distance_grid_name=None, out_direction_grid_name=None, out_allocation_grid_name=None, progress=None):
    """
    根据给定的参数，生成耗费距离栅格，以及耗费方向栅格和耗费分配栅格。

    实际应用中，直线距离往往不能满足要求。例如，从 B 到最近源 A 的直线距离与从 C 到最近源 A 的直线距离相同，若 BA 路段交通拥堵，而 CA 路段交通畅
    通，则其时间耗费必然不同；此外，通过直线距离对应的路径到达最近源时常常是不可行的，例如，遇到河流、高山等障碍物就需要绕行，这时就需要考虑其耗费距离。

    该方法根据源数据集和耗费栅格生成相应的耗费距离栅格、耗费方向栅格（可选）和耗费分配栅格（可选）。源数据可以是矢量数据（点、线、面），也可以是栅格数据。
    对于栅格数据，要求除标识源以外的单元格为无值。

     * 耗费距离栅格的值表示该单元格到最近源的最小耗费值（可以是各种类型的耗费因子，也可以是各感兴趣的耗费因子的加权）。最近源
       是当前单元格到达所有的源中耗费最小的一个源。耗费栅格中为无值的单元格在输出的耗费距离栅格中仍为无值。

       单元格到达源的耗费的计算方法是，从待计算单元格的中心出发，到达最近源的最小耗费路径在每个单元格上经过的距离乘以耗费栅格
       上对应单元格的值，将这些值累加即为单元格到源的耗费值。因此，耗费距离的计算与单元格大小和耗费栅格有关。在下面的示意图中，
       源栅格和耗费栅格的单元格大小（cell_size）均为2，单元格（2,1）到达源（0,0）的最小耗费路线如右图中红线所示：

       .. image:: ../image/CostDistance_1.png

       那么单元格（2,1）到达源的最小耗费（即耗费距离）为：

       .. image:: ../image/CostDistance_2.png

     * 耗费方向栅格的值表达的是从该单元格到达最近的源的最小耗费路径的行进方向。在耗费方向栅格中，可能的行进方向共有八个（正北、
       正南、正西、正东、西北、西南、东南、东北），使用1到8八个整数对这八个方向进行编码，如下图所示。注意，源所在的单元格在耗费
       方向栅格中的值为0，耗费栅格中为无值的单元格在输出的耗费方向栅格中将被赋值为15。

       .. image:: ../image/CostDistance_3.png

     * 耗费分配栅格的值为单元格的最近源的值（源为栅格时，为最近源的栅格值；源为矢量对象时，为最近源的 SMID），单元格到达最近的
       源具有最小耗费距离。耗费栅格中为无值的单元格在输出的耗费分配栅格中仍为无值。

       下图为生成耗费距离的示意图。其中，在耗费栅格上，使用蓝色箭头标识了单元格到达最近源的行进路线，耗费方向栅格的值即标示了
       当前单元格到达最近源的最小耗费路线的行进方向。

       .. image:: ../image/CostDistance_4.png

    下图为生成耗费距离栅格的一个实例，其中源数据集为点数据集，耗费栅格为对应区域的坡度栅格的重分级结果，生成了耗费距离栅格、耗费方向栅格和耗费分配栅格。

    .. image:: ../image/CostDistance.png

    :param input_data: 生成距离栅格的源数据集。源是指感兴趣的研究对象或地物，如学校、道路或消防栓等。包含源的数据集，即为源数据集。源数据集可以为
                        点、线、面数据集，也可以为栅格数据集，栅格数据集中具有有效值的栅格为源，对于无值则视为该位置没有源。
    :type input_data: DatasetVector or DatasetGrid or str
    :param DatasetGrid cost_grid:  耗费栅格。其栅格值不能为负值。该数据集为一个栅格数据集，每个单元格的值表示经过此单元格时的单位耗费。
    :param float max_distance: 生成距离栅格的最大距离，大于该距离的栅格其计算结果取无值。若某个栅格单元格 A 到最近源之间的最短距离大于该值，则结果数据集中该栅格的值取无值。
    :param float cell_size: 结果数据集的分辨率，是生成距离栅格的可选参数
    :param out_data: 结果数据集所在的数据源
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_distance_grid_name: 结果距离栅格数据集的名称。如果名称为空，将自动获取有效的数据集名称。
    :param str out_direction_grid_name: 方向栅格数据集的名称，如果为空，将不生成方向栅格数据集
    :param str out_allocation_grid_name:  分配栅格数据集的名称，如果为空，将不生成 分配栅格数据集
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 如果生成成功，返回结果数据集或数据集名称的元组，其中第一个为距离栅格数据集，第二个为方向栅格数据集，第三个为分配栅格数据集，如果没有设置方向栅格数据集名称和
             分配栅格数据集名称，对应的值为 None
    :rtype: tuple[DataetGrid] or tuple[str]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, (DatasetVector, DatasetGrid)):
        raise ValueError('source input_data must be DatasetVector,  DatasetGrid')
    _source_cost_grid = get_input_dataset(cost_grid)
    if _source_cost_grid is None:
        raise ValueError('cost grid dataset is None')
    else:
        if not isinstance(_source_cost_grid, DatasetGrid):
            raise ValueError('cost input_data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_distance_grid_name is None:
            _outDistanceGridName = _source_input.name + '_distance'
        else:
            _outDistanceGridName = out_distance_grid_name
    _outDistanceGridName = _ds.get_available_dataset_name(_outDistanceGridName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setCostGrid(_source_cost_grid._jobject)
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setDistanceGridName(_outDistanceGridName)
            if max_distance is not None:
                parameter.setMaxDistance(float(max_distance))
            if cell_size is not None:
                parameter.setCellSize(float(cell_size))
            if out_direction_grid_name is not None:
                parameter.setDirectionGridName(out_direction_grid_name)
            if out_allocation_grid_name is not None:
                parameter.setAllocationGridName(out_allocation_grid_name)
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'CostDistance')
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            distance_analyst_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.costDistance(parameter)
        except Exception as e:
            try:
                log_error(e)
                distance_analyst_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif distance_analyst_result is not None:
            results = []
            dt = distance_analyst_result.getDistanceDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getDirectionDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getAllocationDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            if out_data is not None:
                return try_close_output_datasource(results, out_datasource)
            return results
        else:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return


def cost_path(input_data, distance_dataset, direction_dataset, compute_type, out_data=None, out_dataset_name=None, progress=None):
    """
    根据耗费距离栅格和耗费方向栅格，分析从目标出发到达最近源的最短路径栅格。
    该方法根据给定的目标数据集，以及通过“生成耗费距离栅格”功能得到的耗费距离栅格和耗费方向栅格，来计算每个目标对象到达最近的源的最短路径，也就是最小
    耗费路径。该方法不需要指定源所在的数据集，因为源的位置在距离栅格和方向栅格中能够体现出来，即栅格值为 0 的单元格。生成的最短路径栅格是一个二值栅
    格，值为 1 的单元格表示路径，其他单元格的值为 0。

    例如，将购物商场（一个点数据集）作为源，各居民小区（一个面数据集）作为目标，分析从各居民小区出发，如何到达距其最近的购物商场。实现的过程是，首先
    针对源（购物商场）生成距离栅格和方向栅格，然后将居民小区作为目标区域，通过最短路径分析，得到各居民小区（目标）到最近购物商场（源）的最短路径。该
    最短路径包含两种含义：通过直线距离栅格与直线方向栅格，将得到最小直线距离路径；通过耗费距离栅格与耗费方向栅格，则得到最小耗费路径。

    注意，该方法中要求输入的耗费距离栅格和耗费方向栅格必须是匹配的，也就是说二者应是同一次使用“生成耗费距离栅格”功能生成的。此外，有三种计算最短路径
    的方式：像元路径、区域路径和单一路径，具体含义请参见 :py:class:`.ComputeType` 类。

    :param input_data: 目标所在的数据集。可以为点、线、面或栅格数据集。如果是栅格数据，要求除标识目标以外的单元格为无值。
    :type input_data: DatasetVector or DatasetGrid or DatasetImage or str
    :param distance_dataset: 耗费距离栅格数据集。
    :type distance_dataset: DatasetGrid or str
    :param direction_dataset:  耗费方向栅格数据集
    :type direction_dataset: DatasetGrid or str
    :param compute_type: 栅格距离最短路径分析的计算方式
    :type compute_type: ComputeType or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, (DatasetVector, DatasetGrid)):
        raise ValueError('source input_data must be DatasetGrid')
    _source_distance = get_input_dataset(distance_dataset)
    if _source_distance is None:
        raise ValueError('source distance dataset is None')
    if not isinstance(_source_distance, DatasetGrid):
        raise ValueError('source distance dataset must be DatasetGrid')
    _source_direction = get_input_dataset(direction_dataset)
    if _source_direction is None:
        raise ValueError('source direction dataset is None')
    else:
        if not isinstance(_source_direction, DatasetGrid):
            raise ValueError('source direction dataset must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_costpath'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'CostPath')
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.costPath(_source_input._jobject, _source_distance._jobject, _source_direction._jobject, ComputeType._make(compute_type)._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def cost_path_line(source_point, target_point, cost_grid, smooth_method=None, smooth_degree=0, progress=None):
    """
    根据给定的参数，计算源点和目标点之间的最小耗费路径（一个二维矢量线对象）。该方法用于根据给定的源点、目标点和耗费栅格，计算源点与目标点之间的最小耗费路径

    下图为计算两点间最小耗费路径的实例。该例以 DEM 栅格的坡度的重分级结果作为耗费栅格，分析给定的源点和目标点之间的最小耗费路径。

    .. image:: ../image/CostPathLine.png

    :param Point2D source_point: 指定的源点
    :param Point2D target_point: 指定的目标点
    :param DatasetGrid cost_grid:  耗费栅格。其栅格值不能为负值。该数据集为一个栅格数据集，每个单元格的值表示经过此单元格时的单位耗费。
    :param smooth_method: 计算两点（源和目标）间最短路径时对结果路线进行光滑的方法
    :type smooth_method: SmoothMethod or str
    :param int smooth_degree: 计算两点（源和目标）间最短路径时对结果路线进行光滑的光滑度。
                                光滑度的值越大，光滑度的值越大，则结果矢量线的光滑度越高。当 smooth_method 不为 NONE 时有效。光滑度的有效取值与光滑方法有关，光滑方法有 B 样条法和磨角法:
                                - 光滑方法为 B 样条法时，光滑度的有效取值为大于等于2的整数，建议取值范围为[2,10]。
                                - 光滑方法为磨角法时，光滑度代表一次光滑过程中磨角的次数，设置为大于等于1的整数时有效
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 返回表示最短路径的线对象和最短路径的花费
    :rtype: tuple[GeoLine,float]
    """
    _source_grid = get_input_dataset(cost_grid)
    if _source_grid is None:
        raise ValueError('source Grid dataset is None')
    if not isinstance(_source_grid, DatasetGrid):
        raise ValueError('source Grid dataset must be DatasetGrid')
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setCostGrid(_source_grid._jobject)
            if smooth_method is not None:
                parameter.setPathLineSmoothMethod(SmoothMethod._make(smooth_method)._jobject)
            if smooth_degree is not None:
                parameter.setPathLineSmoothDegree(int(smooth_degree))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'CostPathLine')
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.costPathLine(source_point._jobject, target_point._jobject, parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is not None:
            return (
             Geometry._from_java_object(java_result.getPathLine()), java_result.getCost())
        return


def path_line(target_point, distance_dataset, direction_dataset, smooth_method=None, smooth_degree=0):
    """
    根据距离栅格和方向栅格，分析从目标点出发到达最近源的最短路径（一个二维矢量线对象）。 该方法根据距离栅格和方向栅格，分析给定的目标点到达最近源的最短路径。其中距离栅格和方向栅格可以是耗费距离栅格和耗费方向栅格，也可以是表面距离栅格和表面方向栅格。

        - 当距离栅格为耗费距离栅格，方向栅格为耗费方向栅格时，该方法计算得出的是最小耗费路径。耗费距离栅格和耗费方向栅格可以通过 costDistance 方法生成。注意，此方法要求二者是同一次生成的结果。
        - 当距离栅格为表面距离栅格，方向栅格为表面方向栅格时，该方法计算得出的是最短表面距离路径。表面距离栅格和表面方向栅格可以通过 surfaceDistance 方法生成。同样，此方法要求二者是同一次生成的结果。

    源的位置在距离栅格和方向栅格中能够体现出来，即栅格值为 0 的单元格。源可以是一个，也可以有多个。当有多个源时，最短路径是目标点到达其最近的源的路径。

    下图为源、表面栅格、耗费栅格和目标点，其中耗费栅格是对表面栅格计算坡度后重分级的结果。

    .. image:: ../image/PathLine_2.png

    使用如上图所示的源和表面栅格生成表面距离栅格和表面方向栅格，然后计算目标点到最近源的最短表面距离路径；使用源和耗费栅格生成耗费距离栅格和耗费方向栅格，然后计算目标点到最近源的最小耗费路径。得到的结果路径如下图所示：

    .. image:: ../image/PathLine_3.png
    

    :param Point2D target_point: 指定的目标点。
    :param DatasetGrid distance_dataset: 指定的距离栅格。可以是耗费距离栅格或表面距离栅格。
    :param DatasetGrid direction_dataset: 指定的方向栅格。与距离栅格对应，可以是耗费方向栅格或表面方向栅格。
    :param smooth_method: 计算两点（源和目标）间最短路径时对结果路线进行光滑的方法
    :type smooth_method: SmoothMethod or str
    :param int smooth_degree: 计算两点（源和目标）间最短路径时对结果路线进行光滑的光滑度。
                                光滑度的值越大，光滑度的值越大，则结果矢量线的光滑度越高。当 smooth_method 不为 NONE 时有效。光滑度的有效取值与光滑方法有关，光滑方法有 B 样条法和磨角法:
                                - 光滑方法为 B 样条法时，光滑度的有效取值为大于等于2的整数，建议取值范围为[2,10]。
                                - 光滑方法为磨角法时，光滑度代表一次光滑过程中磨角的次数，设置为大于等于1的整数时有效
    :return: 返回表示最短路径的线对象和最短路径的花费
    :rtype: tuple[GeoLine,float]
    """
    check_lic()
    _source_distance = get_input_dataset(distance_dataset)
    if _source_distance is None:
        raise ValueError('source distance dataset is None')
    if not isinstance(_source_distance, DatasetGrid):
        raise ValueError('source distance dataset must be DatasetGrid')
    _source_direction = get_input_dataset(direction_dataset)
    if _source_direction is None:
        raise ValueError('source direction dataset is None')
    if not isinstance(_source_direction, DatasetGrid):
        raise ValueError('source direction dataset must be DatasetGrid')
    _jvm = get_jvm()
    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.pathLine(target_point._jobject, _source_distance._jobject, _source_direction._jobject, SmoothMethod._make(smooth_method)._jobject, int(smooth_degree))
        except Exception as e:
            try:
                log_error(e)
                java_result = None
            finally:
                e = None
                del e

    finally:
        if java_result is not None:
            return (
             Geometry._from_java_object(java_result.getPathLine()), java_result.getCost())
        return


def straight_distance(input_data, max_distance=-1.0, cell_size=None, out_data=None, out_distance_grid_name=None, out_direction_grid_name=None, out_allocation_grid_name=None, progress=None):
    """
    根据给定的参数，生成直线距离栅格，以及直线方向栅格和直线分配栅格。

    该方法用于对源数据集生成相应的直线距离栅格、直线方向栅格（可选）和直线分配栅格（可选），三个结果数据集的区域范围与源数据集的范围一致。生成直线距
    离栅格的源数据可以是矢量数据（点、线、面），也可以是栅格数据。对于栅格数据，要求除标识源以外的单元格为无值。

    * 直线距离栅格的值代表该单元格到最近的源的欧氏距离（即直线距离）。最近源是当前单元格到达所有源中直线距离最短的一个源。对于每个
      单元格，它的中心与源的中心相连的直线即为单元格到源的距离，计算的方法是通过二者形成的直角三角形的两条直角边来计算，因此直线
      距离的计算只与单元格大小（即分辨率）有关。下图为直线距离计算的示意图，其中源栅格的单元格大小（cell_size）为10。

      .. image:: ../image/StraightDistance_1.png

      那么第三行第三列的单元格到源的距离L为：

      .. image:: ../image/StraightDistance_2.png

    * 直线方向栅格的值表示该单元格到最近的源的方位角，单位为度。以正东方向为90度，正南为180度，正西为270度，正北为360度，顺时针方向旋转，范围为0-360度，并规定对应源的栅格值为0度。

    * 直线分配栅格的值为单元格的最近源的值（源为栅格时，为最近源的栅格值；源为矢量对象时，为最近源的 SMID），因此从直线分配栅格中可以得知每个单元格的最近的源是哪个。

    下图为生成直线距离的示意图。单元格大小均为2。

    .. image:: ../image/StraightDistance_3.png

    直线距离栅格通常用于分析经过的路线没有障碍或等同耗费的情况，例如，救援飞机飞往最近的医院时，空中没有障碍物，因此采用哪条路线的耗费均相同，此时通过直线距离栅格就可以确定从救援飞机所在地点到周围各医院的距离；根据直线分配栅格可以获知离救援飞机所在地点最近的医院；由直线方向栅格可以确定最近的医院在救援飞机所在地点的方位。

    然而，在救援汽车开往最近医院的实例中，因为地表有各种类型的障碍物，采用不同的路线的耗费不尽相同，这时，就需要使用耗费距离栅格来进行分析。有关耗费距离栅格请参见 CostDistance 方法。

    下图为生成直线距离栅格的一个实例，其中源数据集为点数据集，生成了直线距离栅格、直线方向栅格和直线分配栅格。

    .. image:: ../image/StraightDistance.png

    注意：当数据集的最小外接矩形（bounds）为某些特殊情形时，结果数据集的 Bounds 按以下规则取值：

    * 当源数据集的 Bounds 的高和宽均为 0 （如只有一个矢量点）时，结果数据集的 Bounds 的高和宽，均取源数据集 Bounds 的左边界值（Left）和下边界值（Right）二者绝对值较小的一个。
    * 当源数据集的 Bounds 的高为 0 而宽不为 0 （如只有一条水平线）时，结果数据集的 Bounds 的高和宽，均等于源数据集 Bounds 的宽。
    * 当源数据集的 Bounds 的宽为 0 而高不为 0 （如只有一条竖直线）时，结果数据集的 Bounds 的高和宽，均等于源数据集 Bounds 的高。

    :param input_data: 生成距离栅格的源数据集。源是指感兴趣的研究对象或地物，如学校、道路或消防栓等。包含源的数据集，即为源数据集。源数据集可以为
                        点、线、面数据集，也可以为栅格数据集，栅格数据集中具有有效值的栅格为源，对于无值则视为该位置没有源。
    :type input_data: DatasetVector or DatasetGrid or DatasetImage or str
    :param float max_distance: 生成距离栅格的最大距离，大于该距离的栅格其计算结果取无值。若某个栅格单元格 A 到最近源之间的最短距离大于该值，则结果数据集中该栅格的值取无值。
    :param float cell_size: 结果数据集的分辨率，是生成距离栅格的可选参数
    :param out_data: 结果数据集所在的数据源
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_distance_grid_name: 结果距离栅格数据集的名称。如果名称为空，将自动获取有效的数据集名称。
    :param str out_direction_grid_name: 方向栅格数据集的名称，如果为空，将不生成方向栅格数据集
    :param str out_allocation_grid_name:  分配栅格数据集的名称，如果为空，将不生成 分配栅格数据集
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 如果生成成功，返回结果数据集或数据集名称的元组，其中第一个为距离栅格数据集，第二个为方向栅格数据集，第三个为分配栅格数据集，如果没有设置方向栅格数据集名称和
             分配栅格数据集名称，对应的值为 None
    :rtype: tuple[DataetGrid] or tuple[str]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, (DatasetVector, DatasetGrid)):
            raise ValueError('source input_data must be DatasetVector or DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_distance_grid_name is None:
            _outDistanceGridName = _source_input.name + '_distance'
        else:
            _outDistanceGridName = out_distance_grid_name
    _outDistanceGridName = _ds.get_available_dataset_name(_outDistanceGridName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setDistanceGridName(_outDistanceGridName)
            if max_distance is not None:
                parameter.setMaxDistance(float(max_distance))
            if cell_size is not None:
                parameter.setCellSize(float(cell_size))
            if out_direction_grid_name is not None:
                parameter.setDirectionGridName(out_direction_grid_name)
            if out_allocation_grid_name is not None:
                parameter.setAllocationGridName(out_allocation_grid_name)
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'StraightDistance')
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            distance_analyst_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.straightDistance(parameter)
        except Exception as e:
            try:
                log_error(e)
                distance_analyst_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif distance_analyst_result is not None:
            results = []
            dt = distance_analyst_result.getDistanceDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getDirectionDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getAllocationDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            if out_data is not None:
                return try_close_output_datasource(results, out_datasource)
            return results
        else:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return


def surface_distance(input_data, surface_grid_dataset, max_distance=-1.0, cell_size=None, max_upslope_degrees=90.0, max_downslope_degree=90.0, out_data=None, out_distance_grid_name=None, out_direction_grid_name=None, out_allocation_grid_name=None, progress=None):
    """
    根据给定的参数，生成表面距离栅格，以及表面方向栅格和表面分配栅格。 该方法根据源数据集和表面栅格生成相应的表面距离栅格、表面方向栅格（可选）和表面
    分配栅格（可选）。源数据可以是矢量数据（点、线、面），也可以是栅格数据。对于栅格数据，要求除标识源以外的单元格为无值。

    * 表面距离栅格的值表示表面栅格上该单元格到最近源的表面最短距离。最近源是指当前单元格到达所有的源中表面距离最短的一个源。表面栅格中为无值的单元格在输出的表面距离栅格中仍为无值。
      从当前单元格（设为 g1）到达下一个单元格（设为 g2）的表面距离 d 的计算方法为：

      .. image:: ../image/SurfaceDistance_1.png

      其中，b 为 g1 的栅格值（即高程）与 g2 的栅格值的差；a 为 g1 与 g2 的中心点之间的直线距离，其值考虑两种情况，当 g2 是与
      g1 相邻的上、下、左、右四个单元格之一时，a 的值等于单元格大小；当 g2 是与 g1 对角相邻的四个单元格之一时，a 的值为单元格大小乘以根号 2。

      当前单元格到达最近源的距离值就是沿着最短路径的表面距离值。在下面的示意图中，源栅格和表面栅格的单元格大小（CellSize）均为
      1，单元格（2,1）到达源（0,0）的表面最短路径如右图中红线所示：

      .. image:: ../image/SurfaceDistance_2.png

      那么单元格（2,1）到达源的最短表面距离为：

      .. image:: ../image/SurfaceDistance_3.png

    * 表面方向栅格的值表达的是从该单元格到达最近源的最短表面距离路径的行进方向。在表面方向栅格中，可能的行进方向共有八个（正北、
      正南、正西、正东、西北、西南、东南、东北），使用 1 到 8 八个整数对这八个方向进行编码，如下图所示。注意，源所在的单元格在表面方向栅格中的值为 0，表面栅格中为无值的单元格在输出的表面方向栅格中将被赋值为 15。

      .. image:: ../image/CostDistance_3.png

    * 表面分配栅格的值为单元格的最近源的值（源为栅格时，为最近源的栅格值；源为矢量对象时，为最近源的 SMID），单元格到达最近的源具有最短表面距离。表面栅格中为无值的单元格在输出的表面分配栅格中仍为无值。
      下图为生成表面距离的示意图。其中，在表面栅格上，根据结果表面方向栅格，使用蓝色箭头标识了单元格到达最近源的行进方向。

      SurfaceDistance_4.png

    通过上面的介绍，可以了解到，结合表面距离栅格及对应的方向、分配栅格，可以知道表面栅格上每个单元格最近的源是哪个，表面距离是多少以及如何到达该最近源。

    注意，生成表面距离时可以指定最大上坡角度（max_upslope_degrees）和最大下坡角度（max_downslope_degree），从而在寻找最近源时
    避免经过上下坡角度超过指定值的单元格。从当前单元格行进到下一个高程更高的单元格为上坡，上坡角度即上坡方向与水平面的夹角，如果
    上坡角度大于给定值，则不会考虑此行进方向；从当前单元格行进到下一个高程小于当前高程的单元格为下坡，下坡角度即下坡方向与水平面
    的夹角，同样的，如果下坡角度大于给定值，则不会考虑此行进方向。如果由于上下坡角度限制，使得当前单元格没能找到最近源，那么在
    表面距离栅格中该单元格的值为无值，在方向栅格和分配栅格中也为无值。

    下图为生成表面距离栅格的一个实例，其中源数据集为点数据集，表面栅格为对应区域的 DEM 栅格，生成了表面距离栅格、表面方向栅格和表面分配栅格。

    .. image:: ../image/SurfaceDistance.png

    :param input_data: 生成距离栅格的源数据集。源是指感兴趣的研究对象或地物，如学校、道路或消防栓等。包含源的数据集，即为源数据集。源数据集可以为
                        点、线、面数据集，也可以为栅格数据集，栅格数据集中具有有效值的栅格为源，对于无值则视为该位置没有源。
    :type input_data: DatasetVector or DatasetGrid or DatasetImage or str
    :param surface_grid_dataset: 表面栅格
    :type surface_grid_dataset: DatasetGrid or str
    :param float max_distance: 生成距离栅格的最大距离，大于该距离的栅格其计算结果取无值。若某个栅格单元格 A 到最近源之间的最短距离大于该值，则结果数据集中该栅格的值取无值。
    :param float cell_size: 结果数据集的分辨率，是生成距离栅格的可选参数
    :param float max_upslope_degrees: 最大上坡角度。单位为度，取值范围为大于或等于0。默认值为 90 度，即不考虑上坡角度。
                                      如果指定了最大上坡角度，则选择路线的时候会考虑地形的上坡的角度。从当前单元格行进到下一个高程更高的单元格
                                      为上坡，上坡角度即上坡方向与水平面的夹角。如果上坡角度大于给定值，则不会考虑此行进方向，即给出的路线不会
                                      经过上坡角度大于该值的区域。可想而知，可能会因为该值的设置而导致没有符合条件的路线。此外，由于坡度的表示
                                      范围为0到90度，因此，虽然可以指定为一个大于90度的值，但产生的效果与指定为90度相同，即不考虑上坡角度。
    :param float max_downslope_degree: 设置最大下坡角度。单位为度，取值范围为大于或等于0。
                                      如果指定了最大下坡角度，则选择路线的时候会考虑地形的下坡的角度。从当前单元格行进到下一个高程小于当前高
                                      程的单元格为下坡，下坡角度即下坡方向与水平面的夹角。如果下坡角度大于给定值，则不会考虑此行进方向，即给
                                      出的路线不会经过下坡角度大于该值的区域。可想而知，可能会因为该值的设置而导致没有符合条件的路线。此外，
                                      由于坡度的表示范围为0到90度，因此，虽然可以指定为一个大于90度的值，但产生的效果与指定为90度相同，即不
                                      考虑下坡角度。
    :param out_data: 结果数据集所在的数据源
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_distance_grid_name: 结果距离栅格数据集的名称。如果名称为空，将自动获取有效的数据集名称。
    :param str out_direction_grid_name: 方向栅格数据集的名称，如果为空，将不生成方向栅格数据集
    :param str out_allocation_grid_name:  分配栅格数据集的名称，如果为空，将不生成 分配栅格数据集
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 如果生成成功，返回结果数据集或数据集名称的元组，其中第一个为距离栅格数据集，第二个为方向栅格数据集，第三个为分配栅格数据集，如果没有设置方向栅格数据集名称和
             分配栅格数据集名称，对应的值为 None
    :rtype: tuple[DataetGrid] or tuple[str]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, (DatasetVector, DatasetGrid)):
        raise ValueError('source input_data must be DatasetVector or DatasetGrid')
    _source_surface = get_input_dataset(surface_grid_dataset)
    if _source_surface is None:
        raise ValueError('surface grid dataset is None')
    else:
        if not isinstance(_source_surface, DatasetGrid):
            raise ValueError('surface grid dataset must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_distance_grid_name is None:
            _outDistanceGridName = _source_input.name + '_distance'
        else:
            _outDistanceGridName = out_distance_grid_name
    _outDistanceGridName = _ds.get_available_dataset_name(_outDistanceGridName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setDistanceGridName(_outDistanceGridName)
            if max_distance is not None:
                parameter.setMaxDistance(float(max_distance))
            if cell_size is not None:
                parameter.setCellSize(float(cell_size))
            if out_direction_grid_name is not None:
                parameter.setDirectionGridName(out_direction_grid_name)
            if out_allocation_grid_name is not None:
                parameter.setAllocationGridName(out_allocation_grid_name)
            if max_upslope_degrees is not None:
                parameter.setMaxUpslopeDegree(float(max_upslope_degrees))
            if max_downslope_degree is not None:
                parameter.setMaxDownslopeDegree(float(max_downslope_degree))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'StraightDistance')
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            distance_analyst_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.straightDistance(parameter)
        except Exception as e:
            try:
                log_error(e)
                distance_analyst_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif distance_analyst_result is not None:
            results = []
            dt = distance_analyst_result.getDistanceDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getDirectionDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getAllocationDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            if out_data is not None:
                return try_close_output_datasource(results, out_datasource)
            return results
        else:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return


def surface_path_line(source_point, target_point, surface_grid_dataset, max_upslope_degrees=90.0, max_downslope_degree=90.0, smooth_method=None, smooth_degree=0, progress=None):
    """
    根据给定的参数，计算源点和目标点之间的最短表面距离路径（一个二维矢量线对象）。该方法用于根据给定的源点、目标点和表面栅格，计算源点与目标点之间的最短表面距离路径。

    设置最大上坡角度（max_upslope_degrees）和最大下坡角度（max_downslope_degree）可以使分析得出的路线不经过过于陡峭的地形。
    但注意，如果指定了上下坡角度限制，也可能得不到分析结果，这与最大上下坡角度的值和表面栅格所表达的地形有关。下图展示了将最
    大上坡角度和最大下坡角度分别均设置为 5 度、10 度和 90 度（即不限制上下坡角度）时的表面距离最短路径，由于对上下坡角度做出
    了限制，因此表面距离最短路径是以不超过最大上下坡角度为前提而得出的。

    .. image:: ../image/SurfacePathLine.png

    :param Point2D source_point: 指定的源点。
    :param Point2D target_point:  指定的目标点。
    :param surface_grid_dataset: 表面栅格
    :type surface_grid_dataset: DatasetGrid or str
    :param float max_upslope_degrees: 最大上坡角度。单位为度，取值范围为大于或等于0。默认值为 90 度，即不考虑上坡角度。
                                      如果指定了最大上坡角度，则选择路线的时候会考虑地形的上坡的角度。从当前单元格行进到下一个高程更高的单元格
                                      为上坡，上坡角度即上坡方向与水平面的夹角。如果上坡角度大于给定值，则不会考虑此行进方向，即给出的路线不会
                                      经过上坡角度大于该值的区域。可想而知，可能会因为该值的设置而导致没有符合条件的路线。此外，由于坡度的表示
                                      范围为0到90度，因此，虽然可以指定为一个大于90度的值，但产生的效果与指定为90度相同，即不考虑上坡角度。
    :param float max_downslope_degree: 设置最大下坡角度。单位为度，取值范围为大于或等于0。
                                      如果指定了最大下坡角度，则选择路线的时候会考虑地形的下坡的角度。从当前单元格行进到下一个高程小于当前高
                                      程的单元格为下坡，下坡角度即下坡方向与水平面的夹角。如果下坡角度大于给定值，则不会考虑此行进方向，即给
                                      出的路线不会经过下坡角度大于该值的区域。可想而知，可能会因为该值的设置而导致没有符合条件的路线。此外，
                                      由于坡度的表示范围为0到90度，因此，虽然可以指定为一个大于90度的值，但产生的效果与指定为90度相同，即不
                                      考虑下坡角度。
    :param smooth_method: 计算两点（源和目标）间最短路径时对结果路线进行光滑的方法
    :type smooth_method: SmoothMethod or str
    :param int smooth_degree: 计算两点（源和目标）间最短路径时对结果路线进行光滑的光滑度。
                                光滑度的值越大，光滑度的值越大，则结果矢量线的光滑度越高。当 smooth_method 不为 NONE 时有效。光滑度的有效取值与光滑方法有关，光滑方法有 B 样条法和磨角法:
                                - 光滑方法为 B 样条法时，光滑度的有效取值为大于等于2的整数，建议取值范围为[2,10]。
                                - 光滑方法为磨角法时，光滑度代表一次光滑过程中磨角的次数，设置为大于等于1的整数时有效
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 返回表示最短路径的线对象和最短路径的花费
    :rtype: tuple[GeoLine,float]
    """
    _source_grid = get_input_dataset(surface_grid_dataset)
    if _source_grid is None:
        raise ValueError('source Grid dataset is None')
    if not isinstance(_source_grid, DatasetGrid):
        raise ValueError('source Grid dataset must be DatasetGrid')
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setSurfaceGrid(_source_grid._jobject)
            if smooth_method is not None:
                parameter.setPathLineSmoothMethod(SmoothMethod._make(smooth_method)._jobject)
            if smooth_degree is not None:
                parameter.setPathLineSmoothDegree(int(smooth_degree))
            if max_upslope_degrees is not None:
                parameter.setMaxUpslopeDegree(float(max_upslope_degrees))
            if max_downslope_degree is not None:
                parameter.setMaxDownslopeDegree(float(max_downslope_degree))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'CostPathLine')
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.surfacePathLine(source_point._jobject, target_point._jobject, parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is not None:
            return (
             Geometry._from_java_object(java_result.getPathLine()), java_result.getCost())
        return


def calculate_hill_shade(input_data, shadow_mode, azimuth, altitude_angle, z_factor, out_data=None, out_dataset_name=None, progress=None):
    """
    三维晕渲图是指通过模拟实际地表的本影与落影的方式反映地形起伏状况的栅格图。通过采用假想的光源照射地表，结合栅格数据得到的坡度坡向信息， 得到各像元
    的灰度值，面向光源的斜坡的灰度值较高，背向光源的灰度值较低，即为阴影区，从而形象表现出实际地表的地貌和地势。 由栅格数据计算得出的这种山体阴影图
    往往具有非常逼真的立体效果，因而称其为三维晕渲图。

    .. image:: ../image/CalculateHillShade.png

    三维晕渲图在描述地表三维状况和地形分析中都具有比较重要的价值，当将其他专题信息叠加在三维晕渲图之上时，将会更加提高三维晕渲图的应用价值和直观效果。

    在生成三维晕渲图时，需要指定假想光源的位置，该位置由光源的方位角和高度角确定。方位角确定光源的方向，高度角是光源照射时倾斜角度。例如，当光源的方位角
    为 315 度，高度角为 45 度时，其与地表的相对位置如下图所示。

    .. image:: ../image/CalculateHillShade_1.png

    三维晕渲图有三种类型：渲染阴影效果、渲染效果和阴影效果，通过 :py:class`ShadowMode` 类来指定。

    :param input_data: 指定的待生成三维晕渲图的栅格数据集
    :type input_data: DatasetGrid or str
    :param shadow_mode: 三维晕渲图的渲染类型
    :type shadow_mode: ShadowMode or str
    :param float azimuth: 指定的光源方位角。用于确定光源的方向，是从光源所在位置的正北方向线起，依顺时针方向到光源与目标方向线
                          的夹角，范围为 0-360 度，以正北方向为 0 度，依顺时针方向递增。

                          .. image:: ../image/Azimuth.png

    :param float altitude_angle: 指定的光源高度角。用于确定光源照射的倾斜角度，是光源与目标的方向线与水平面间的夹角，范围为
                                 0-90 度。当光源高度角为 90 度时，光源正射地表。

                                 .. image:: ../image/AltitudeAngle.png

    :param float z_factor:  指定的高程缩放系数。该值是指在栅格中，栅格值（Z 坐标，即高程值）相对于 X 和 Y 坐标的单位变换系数。通常有 X，Y，Z 都参加的计算中，需要将高程值乘以一个高程缩放系数，使得三者单位一致。例如，X、Y 方向上的单位是米，而 Z 方向的单位是英尺，由于 1 英尺等于 0.3048 米，则需要指定缩放系数为 0.3048。如果设置为 1.0，表示不缩放。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError('source input_data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_hill'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'CalculateHillShade')
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateHillShade(_source_input._jobject, ShadowMode._make(shadow_mode)._jobject, float(azimuth), float(altitude_angle), float(z_factor), _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def calculate_slope(input_data, slope_type, z_factor, out_data=None, out_dataset_name=None, progress=None):
    """
    计算坡度，并返回坡度栅格数据集，即坡度图。 坡度是地表面上某一点的切面和水平面所成的夹角。坡度值越大，表示地势越陡峭

    注意：
        计算坡度时，要求待计算的栅格值（即高程）的单位与 x，y 坐标的单位相同。如果不一致，可通过高程缩放系数（方法中对应 zFactor 参数）来调整。
        但注意，当高程值单位与坐标单位间的换算无法通过固定值来调节时，则需要通过其他途径对数据进行处理。最常见的情况之一是 DEM 栅格采用地理坐标系时，
        单位为度，而高程值单位为米，此时建议对 DEM 栅格进行投影转换，将 x，y 坐标转换为平面坐标。

    :param input_data: 指定的的待计算坡度的栅格数据集
    :type input_data: DatasetGrid or str
    :param slope_type: 坡度的单位类型
    :type slope_type: SlopeType or str
    :param float z_factor: 指定的高程缩放系数。该值是指在栅格中，栅格值（Z 坐标，即高程值）相对于 X 和 Y 坐标的单位变换系数。通常有 X，Y，Z 都参加的计算中，需要将高程值乘以一个高程缩放系数，使得三者单位一致。例如，X、Y 方向上的单位是米，而 Z 方向的单位是 英尺，由于 1 英尺等于 0.3048 米，则需要指定缩放系数为 0.3048。如果设置为 1.0，表示不缩放。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError('source input_data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_slope'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'calculate_slope')
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateSlope(_source_input._jobject, SlopeType._make(slope_type)._jobject, float(z_factor), _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def calculate_aspect(input_data, out_data=None, out_dataset_name=None, progress=None):
    """
    计算坡向，并返回坡向栅格数据集，即坡向图。
    坡向是指坡面的朝向，它表示地形表面某处最陡的下坡方向。坡向反映了斜坡所面对的方向，任意斜坡的倾斜方向可取 0～360 度中的任意方向，所以坡向计算的
    结果范围为 0～360 度。从正北方向（0 度）开始顺时针计算

    :param input_data: 指定的待计算坡向的栅格数据集
    :type input_data: DatasetGrid or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError('source input_data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_aspect'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'calculate_aspect')
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateAspect(_source_input._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def compute_point_aspect(input_data, specified_point):
    """
    计算 DEM 栅格上指定点处的坡向。 DEM 栅格上指定点处的坡向，与坡向图（calculate_aspect 方法）的计算方法相同，是将该点所在单元格与其周围的相
    邻的八个单元格所形成的 3 × 3 平面作为计算单元，通过三阶反距离平方权差分法计算水平高程变化率和垂直高程变化率从而得出坡向。更多介绍，请参阅 :py:meth:`calculate_aspect` 方法。

    注意：
        当指定点所在的单元格为无值时，计算结果为 -1，这与生成坡向图不同；当指定的点位于 DEM 栅格的数据集范围之外时，计算结果为 -1。

    :param input_data: 指定的待计算坡向的栅格数据集
    :type input_data: DatasetGrid or str
    :param Point2D specified_point:  指定的地理坐标点。
    :return: 指定点处的坡向。单位为度。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computePointAspect(_source_input._jobject, specified_point._jobject)
    except Exception as e:
        try:
            log_error(e)
        finally:
            e = None
            del e


def compute_point_slope(input_data, specified_point, slope_type, z_factor):
    """
    计算 DEM 栅格上指定点处的坡度。
    DEM 栅格上指定点处的坡度，与坡度图（calculate_slope 方法）的计算方法相同，是将该点所在单元格与其周围的相邻的八个单元格所形成的 3 × 3 平面作
    为计算单元，通过三阶反距离平方权差分法计算水平高程变化率和垂直高程变化率从而得出坡度。更多介绍，请参阅 calculate_slope 方法。

    注意：
        当指定点所在的单元格为无值时，计算结果为 -1，这与生成坡度图不同；当指定的点位于 DEM 栅格的数据集范围之外时，计算结果为 -1。

    :param input_data: 指定的待计算坡向的栅格数据集
    :type input_data: DatasetGrid or str
    :param Point2D specified_point: 指定的地理坐标点。
    :param slope_type: 指定的坡度单位类型。可以用角度、弧度或百分数来表示。以使用角度为例，坡度计算的结果范围为 0～90 度。
    :type slope_type: SlopeType or str
    :param float z_factor: 指定的高程缩放系数。该值是指在 DEM 栅格中，栅格值（Z 坐标，即高程值）相对于 X 和 Y 坐标的单位变换系数。通常有 X，Y，Z 都参加的计算中，需要将高程值乘以一个高程缩放系数，使得三者单位一致。例如，X、Y 方向上的单位是米，而 Z 方向的单位是英尺，由于 1 英尺等于 0.3048 米，则需要指定缩放系数为 0.3048。如果设置为 1.0，表示不缩放。
    :return: 指定点处的坡度。单位为 type 参数指定的类型。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computePointSlope(_source_input._jobject, specified_point._jobject, SlopeType._make(slope_type)._jobject, float(z_factor))
    except Exception as e:
        try:
            import traceback
            log_error(traceback.format_exc())
        finally:
            e = None
            del e


def calculate_ortho_image(input_data, colors, no_value_color, out_data=None, out_dataset_name=None, progress=None):
    """
    根据给定的颜色集合生成正射三维影像。

    正射影像是采用数字微分纠正技术，通过周边邻近栅格的高程得到当前点的合理日照强度，进行正射影像纠正。

    :param input_data: 指定的待计算三维正射影像的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param colors: 三维投影后的颜色集合。输入如果为 dict，则表示高程值与颜色值的对应关系。
                可以不必在高程颜色对照表中列出待计算栅格的所有栅格值（高程值）及其对应颜色，未在高程颜色对照表中列出的高程值，其在结果影像中的颜色将通过插值得出。
    :type colors: Colors or dict[float,tuple]
    :param no_value_color: 无值栅格的颜色
    :type no_value_color: tuple or int
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError('source input_data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_orthoImage'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            if isinstance(colors, dict):
                java_color = _jvm.com.supermap.data.ColorDictionary()
                for key, value in colors.items():
                    java_color.setColor(float(key), to_java_color(value))

            else:
                if isinstance(colors, Colors):
                    java_color = colors._jobject
                else:
                    raise ValueError('valid colors type, required dict or Colors, but now is ' + str(type(colors)))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'CalculateOrthoImage')
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateOrthoImage(oj(_source_input), java_color, to_java_color(no_value_color), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def compute_surface_area(input_data, region):
    """
    计算表面面积，即计算所选多边形区域内的 DEM 栅格拟合的三维曲面的总的表面面积。

    :param input_data: 指定的待计算表面面积的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param GeoRegion region: 指定的用于计算表面面积的多边形
    :return: 表面面积的值。单位为平方米。返回 -1 表示计算失败。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computeSurfaceArea(oj(_source_input), oj(region))
    except Exception as e:
        try:
            log_error(e)
        finally:
            e = None
            del e

    return -1.0


def compute_surface_distance(input_data, line):
    """
    计算栅格表面距离，即计算在 DEM 栅格拟合的三维曲面上沿指定的线段或折线段的曲面距离。

    注意：
        - 表面量算所量算的距离是曲面上的，因而比平面上的值要大。
        - 当用于量算的线超出了 DEM 栅格的范围时，会先按数据集范围对线对象进行裁剪，按照位于数据集范围内的那部分线来计算表面距离。

    :param input_data:  指定的待计算表面距离的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param GeoLine line: 用于计算表面距离的二维线。
    :return: 表面距离的值。单位为米。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computeSurfaceDistance(oj(_source_input), oj(line))
    except Exception as e:
        try:
            log_error(e)
        finally:
            e = None
            del e

    return -1.0


def compute_surface_volume(input_data, region, base_value):
    """
    计算表面体积，即计算所选多边形区域内的 DEM 栅格拟合的三维曲面与一个基准平面之间的空间上的体积。

    :param input_data: 待计算体积的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param GeoRegion region: 用于计算体积的多边形。
    :param float base_value: 基准平面的值。单位与待计算的 DEM 栅格的栅格值单位相同。
    :return: 指定的基准平面的值。单位与待计算的 DEM 栅格的栅格值单位相同。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computeSurfaceVolume(oj(_source_input), oj(region), float(base_value))
    except Exception as e:
        try:
            log_error(e)
        finally:
            e = None
            del e


def calculate_profile(input_data, line):
    """
    剖面分析，根据给定线路查看 DEM 栅格沿该线路的剖面，返回剖面线和采样点坐标。
    给定一条直线或者折线，查看 DEM 栅格沿此线的纵截面，称为剖面分析。剖面分析的结果包含两部分：剖面线和采样点集合。

    * 采样点

    剖面分析需要沿给定线路选取一些点，通过这些点所在位置的高程和坐标信息，来展现剖面效果，这些点称为采样点。采样点的选取依照以下规则，
    可结合下图来了解。

        - 给定路线途经的每个单元格内只选取一个采样点；
        - 给定路线的节点都被作为采样点；
        - 如果路线经过且节点不在该单元格内，则将线路与该单元格两条中心线中交角较大的一条的交点作为采样点。

    .. image:: ../image/CalculateProfile_1.png

    * 剖面线和采样点坐标集合

    剖面线是剖面分析的结果之一，是一条二维线（ :py:class:`GeoLine` ），它的节点与采样点一一对应，节点的 X 值表示当前采样点到给定线
    路的起点（也是第一个采样点）的直线距离，Y 值为当前采样点所在位置的高程。而采样点集合给出了所有采样点的位置，使用一个二维集合线对
    象来存储这些点。剖面线与采样点集合的点是一一对应的，结合剖面线和采样点集合可以知道在某位置的高程以及距离分析的起点的距离。

    下图展示了以剖面线的 X 值为横轴，Y 值为纵轴绘制二维坐标系下的剖面线示意图，通过剖面线可以直观的了解沿着给定的线路，地形的高程和地势。

    .. image:: ../image/CalculateProfile_2.png

    注意：指定的线路必须在 DEM 栅格的数据集范围内，否则可能分析失败。如果采样点位于无值栅格上，则剖面线上对应的点的高程为0。

    :param input_data:  指定的待进行剖面分析的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param line: 指定的线路，为一条线段或折线。剖面分析给出沿该线路的剖面。
    :type line: GeoLine
    :return: 剖面分析结果，剖面线和采样点集合。
    :rtype: tuple[GeoLine, GeoLine]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    if not isinstance(line, GeoLine):
        raise ValueError('line must be GeoLine')
    _jvm = get_jvm()
    try:
        profile_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateProfile(oj(_source_input), oj(line))
        if profile_result:
            return (
             Geometry._from_java_object(profile_result.getProfile()),
             Geometry._from_java_object(profile_result.getXYCoordinate()))
    except Exception:
        import traceback
        log_error(traceback.format_exc())


class CutFillResult:
    __doc__ = '\n    填挖方结果信息类。该对象用于获取对栅格数据集进行填方和挖方计算的结果，例如需要填方、挖方的面积、填方和挖方的体积数等。\n\n    关于填挖方结果面积和体积单位的说明：\n\n    填挖的面积单位为平方米，体积的单位为平方米乘以高程（即进行填挖的栅格值）的单位。但需注意，如果进行填挖方计算的栅格是地理坐标系，面积的值是一个近似转换到平方米单位的值。\n    '

    def __init__(self, cut_area, cut_volume, fill_area, fill_volume, remainder_area, cut_fill_grid_result):
        """
        内部构造函数，用户不需要使用

        :param float cut_area: 填挖方分析结果挖掘面积。单位为平方米。当进行填挖方的栅格为地理坐标系时，该值为近似转换
        :param float cut_volume: 填挖方分析结果挖掘体积。单位为平方米乘以填挖栅格的栅格值（即高程值）的单位
        :param float fill_area: 填挖方分析结果填充面积。单位为平方米。当进行填挖方的栅格为地理坐标系时，该值为近似转换。
        :param float fill_volume: 填挖方分析结果填充体积。单位为平方米乘以填挖栅格的栅格值（即高程值）的单位。
        :param float remainder_area: 填挖方分析中未进行填挖方的面积。单位为平方米。当进行填挖方的栅格为地理坐标系时，该值为近似转换。
        :param cut_fill_grid_result: 填挖方分析的结果数据集。 单元格值大于0表示要挖的深度，小于0表要填的深度。
        :type cut_fill_grid_result: DatasetGrid or str
        """
        self.cut_area = cut_area
        self.cut_fill_grid_result = cut_fill_grid_result
        self.cut_volume = cut_volume
        self.fill_area = fill_area
        self.fill_volume = fill_volume
        self.remainder = remainder_area

    @staticmethod
    def _from_java_object(java_object, grid_result):
        return CutFillResult(java_object.getCutArea(), java_object.getCutVolume(), java_object.getFillArea(), java_object.getFillVolume(), java_object.getRemainderArea(), grid_result)


def inverse_cut_fill(input_data, volume, is_fill, region=None, progress=None):
    """
    反算填挖方，即根据给定的填方或挖方的体积计算填挖后的高程
    反算填挖方用于解决这样一类实际问题：已知填挖前的栅格数据和该数据范围内要填或挖的体积，来推求填方或挖方后的高程值。例如，某建筑施
    工地的一片区域需要填方，现得知某地可提供体积为 V 的土方，此时使用反算填挖方就可以计算出将这批土填到施工区域后，施工区域的高程是
    多少。然后可判断是否达到施工需求，是否需要继续填方。

    :param input_data: 指定的待填挖的栅格数据。
    :type input_data: DatasetGrid or str
    :param float volume: 指定的填或挖的体积。该值为一个大于0的值，如果设置为小于或等于0会抛出异常。单位为平方米乘以待填挖栅格的栅格值单位。
    :param bool is_fill: 指定是否进行填方计算。如果为 true 表示进行填方计算，false 表示进行挖方计算。
    :param region: 指定的填挖方区域。如果为 None 则填挖计算应用于整个栅格区域。
    :type region: GeoRegion or Rectangle
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖后的高程值。单位与待填挖栅格的栅格值单位一致。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    if isinstance(region, Rectangle):
        region = region.to_region()
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'inverse_cut_fill')
                    _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif isinstance(region, GeoRegion):
                result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(_source_input), float(volume), bool(is_fill), oj(region))
            else:
                result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(_source_input), float(volume), bool(is_fill))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            result = None

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return result


def cut_fill_grid(before_cut_fill_grid, after_cut_full_grid, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格填挖方计算，即对填挖方前、后两个栅格数据集对应像元的计算。
    地表经常由于沉积和侵蚀等作用引起表面物质的迁移，表现为地表某些区域的表面物质增加，某些区域的表面物质减少。在工程中，通常将表面物质的减少称为“挖方”，而将表面物质的增加称为“填方”。

    栅格填挖方计算要求输入两个栅格数据集：填挖方前的栅格数据集和填挖方后的栅格数据集，生成的结果数据集的每个像元值为其两个输入数据集对应像元值的变化值。如果像元值为正，表示该像元处的表面物质减少；如果像元值为负，表示该像元处的表面物质增加。填挖方的计算方法如下图所示：

    .. image:: ../image/CalculationTerrain_CutFill.png

    通过该图可以发现，结果数据集=填挖方前栅格数据集-填挖方后栅格数据集。

    对于输入的两个栅格数据集及结果数据集有几点内容需要注意：

    - 要求两个输入的栅格数据集有相同的坐标和投影系统，以保证同一个地点有相同的坐标，如果两个输入的栅格数据集的坐标系统不一致，则很有可能产生错误的结果。

    - 理论上，要求输入的两个栅格数据集的空间范围也是一致的。对于空间范围不一致的两个栅格数据集，只计算其重叠区域的表面填挖方的结果。

    - 在其中一个栅格数据集的像元为空值处，计算结果数据集该像元值也为空值。

    :param before_cut_fill_grid: 指定的填挖方前的栅格数据集
    :type before_cut_fill_grid: DatasetGrid or str
    :param after_cut_full_grid: 指定的填挖方后的栅格数据集。
    :type after_cut_full_grid: DatasetGrid or str
    :param out_data: 指定的存放结果数据集的数据源。
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖方结果信息
    :rtype: CutFillResult
    """
    check_lic()
    _before_source_input = get_input_dataset(before_cut_fill_grid)
    if _before_source_input is None:
        raise ValueError('before cut fill grid is None')
    if not isinstance(_before_source_input, DatasetGrid):
        raise ValueError('before cut fill grid must be DatasetGrid')
    _after_source_input = get_input_dataset(after_cut_full_grid)
    if _after_source_input is None:
        raise ValueError('after cut fill grid is None')
    else:
        if not isinstance(_after_source_input, DatasetGrid):
            raise ValueError('after cut fill grid must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _before_source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _before_source_input.name + '_CutFill'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'cut_fill_grid')
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            cut_fill_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(_before_source_input), oj(_after_source_input), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                cut_fill_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    result_dt = None
    if cut_fill_result is not None:
        java_cut_fill_grid_result = cut_fill_result.getCutFillGridResult()
        if java_cut_fill_grid_result:
            result_dt = _ds[java_cut_fill_grid_result.getName()]
    if out_data is not None:
        result_dt = try_close_output_datasource(result_dt, out_datasource)
    return CutFillResult._from_java_object(cut_fill_result, result_dt)


def cut_fill_oblique(input_data, line3d, buffer_radius, is_round_head, out_data=None, out_dataset_name=None, progress=None):
    """
    斜面填挖方计算。
    斜面填挖方功能是统计在一个地形表面创建一个斜面所需要的填挖量。其原理与选面填挖方相似。

    :param input_data: 指定的待填挖方的栅格数据集。
    :type input_data: DatasetGrid or str
    :param line3d: 指定的填挖方路线
    :type line3d: GeoLine3D
    :param buffer_radius: 指定的填挖方线路的缓冲区半径。单位与待填挖的栅格数据集的坐标系单位相同。
    :type buffer_radius: float
    :param is_round_head: 指定是否使用圆头缓冲为填挖方路线创建缓冲区。
    :type is_round_head: bool
    :param out_data: 指定的存放结果数据集的数据源
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖方结果信息
    :rtype: CutFillResult
    """
    source_input = get_input_dataset(input_data)
    if source_input is None:
        raise ValueError('source input_data grid is None')
    if not isinstance(source_input, DatasetGrid):
        raise ValueError('source input_data grid must be DatasetGrid')
    else:
        if not isinstance(line3d, GeoLine3D):
            raise ValueError('line3d must GeoLine3D')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = source_input.name + '_CutFill'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'cut_fill_oblique')
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            cut_fill_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(source_input), oj(line3d), float(buffer_radius), bool(is_round_head), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                cut_fill_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    result_dt = None
    if cut_fill_result is not None:
        java_cut_fill_grid_result = cut_fill_result.getCutFillGridResult()
        if java_cut_fill_grid_result:
            result_dt = _ds[java_cut_fill_grid_result.getName()]
    if out_data is not None:
        result_dt = try_close_output_datasource(result_dt, out_datasource)
    return CutFillResult._from_java_object(cut_fill_result, result_dt)


def cut_fill_region(input_data, region, base_altitude, out_data=None, out_dataset_name=None, progress=None):
    """
    选面填挖方计算。
    当需要将一个高低起伏的区域夷为平地时，用户可以通过指定高低起伏的区域以及夷为平地的高程，利用该方法进行选面填挖方计算，计算出填方
    面积，挖方面积、 填方量以及挖方量。

    :param input_data:  指定的待填挖的栅格数据集。
    :type input_data: DatasetGrid or str
    :param region: 指定的填挖方区域。
    :type region: GeoRegion or Rectangle
    :param base_altitude:  指定的填挖方区域的结果高程。单位与待填挖的栅格数据集的栅格值单位相同。
    :type base_altitude: float
    :param out_data: 指定的存放结果数据集的数据源。
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖方结果信息
    :rtype: CutFillResult
    """
    check_lic()
    source_input = get_input_dataset(input_data)
    if source_input is None:
        raise ValueError('source input_data grid is None')
    else:
        if not isinstance(source_input, DatasetGrid):
            raise ValueError('source input_data grid must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = source_input.name + '_CutFill'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    if isinstance(region, Rectangle):
        region = region.to_region()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'cut_fill_region')
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            cut_fill_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(source_input), oj(region), float(base_altitude), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                cut_fill_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    result_dt = None
    if cut_fill_result is not None:
        java_cut_fill_grid_result = cut_fill_result.getCutFillGridResult()
        if java_cut_fill_grid_result:
            result_dt = _ds[java_cut_fill_grid_result.getName()]
    if out_data is not None:
        result_dt = try_close_output_datasource(result_dt, out_datasource)
    return CutFillResult._from_java_object(cut_fill_result, result_dt)


def cut_fill_region3d(input_data, region, out_data=None, out_dataset_name=None, progress=None):
    """
    三维面填挖方计算。
    一个高低起伏的区域，可以根据这个区域填挖方后的三维面，利用三维面填挖方计算出需要填方的面积，挖方的面积、填方量以及挖方量。

    :param input_data:  指定的待填挖的栅格数据集。
    :type input_data: DatasetGrid or str
    :param region: 指定的填挖方区域。
    :type region: GeoRegion3D
    :param out_data: 指定的存放结果数据集的数据源。
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖方结果信息
    :rtype: CutFillResult
    """
    source_input = get_input_dataset(input_data)
    if source_input is None:
        raise ValueError('source input_data grid is None')
    else:
        if not isinstance(source_input, DatasetGrid):
            raise ValueError('source input_data grid must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = source_input.name + '_CutFill'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'cut_fill_region3d')
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            cut_fill_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(source_input), oj(region), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                cut_fill_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    result_dt = None
    if cut_fill_result is not None:
        java_cut_fill_grid_result = cut_fill_result.getCutFillGridResult()
        if java_cut_fill_grid_result:
            result_dt = _ds[java_cut_fill_grid_result.getName()]
    if out_data is not None:
        result_dt = try_close_output_datasource(result_dt, out_datasource)
    return CutFillResult._from_java_object(cut_fill_result, result_dt)


def flood(input_data, height, region=None, progress=None):
    """
    根据指定的高程计算 DEM 栅格的淹没区域。
    淹没区域的计算基于 DEM 栅格数据，根据给定的一个淹没后的水位高程（由参数 height 指定），与 DEM 栅格的值（即高程值）进行比较，凡是高程值低于或等于给定水位的单元格均被划入淹没区域，然后将淹没区域转为矢量面输出，源 DEM 数据并不会被改变。通过淹没区域面对象，很容易统计出被淹没的范围、面积等。
    下图是计算水位达到 200 时的淹没区域的一个实例，由原始 DEM 数据和淹没区域的矢量面数据集（紫色区域）叠加而成

    .. image:: ../image/Flood.png

    注意：该方法返回的面对象是将所有淹没区域进行合并后的结果。

    :param input_data: 指定的需要计算淹没区域的 DEM 数据。
    :type input_data: DatasetGrid or str
    :param height: 指定的淹没后水位的高程值，DEM 数据中小于或等于该值的单元格会划入淹没区域。单位与待分析的 DEM 栅格的栅格值单位相同。
    :type height: float
    :param region: 指定的有效计算区域。指定该区域后，只在该区域内计算淹没区域。
    :type region: GeoRegion or Rectangle
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 将所有淹没区域合并后的面对象
    :rtype: GeoRegion
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    if isinstance(region, Rectangle):
        region = region.to_region()
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'flood')
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.flood(oj(_source_input), float(height), oj(region))
        except Exception as e:
            try:
                log_error(e)
                java_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    if java_result:
        return Geometry._from_java_object(java_result)


def divide_math_analyst(first_operand, second_operand, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格除法运算。将输入的两个栅格数据集的栅格值逐个像元地相除。栅格代数运算的具体使用，参考 :py:meth:`expression_math_analyst`

    如果输入两个像素类型（PixelFormat）均为整数类型的栅格数据集，则输出整数类型的结果数据集；否则，输出浮点型的结果数据集。如果输入的两个栅格数据集
    的像素类型精度不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。

    :param first_operand: 指定的第一栅格数据集。
    :type first_operand: DatasetGrid or str
    :param second_operand:  指定的第二栅格数据集。
    :type second_operand: DatasetGrid or str
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    _first_input = get_input_dataset(first_operand)
    if _first_input is None:
        raise ValueError('first operand data is None')
    if not isinstance(_first_input, DatasetGrid):
        raise ValueError('first operand data must be DatasetGrid')
    _second_input = get_input_dataset(second_operand)
    if _second_input is None:
        raise ValueError('second operand data is None')
    else:
        if not isinstance(_second_input, DatasetGrid):
            raise ValueError('second operand data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + '_divide'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'divide_math_analyst')
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.divide(_first_input._jobject, _second_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def plus_math_analyst(first_operand, second_operand, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格加法运算。将输入的两个栅格数据集的栅格值逐个像元地相加。 栅格代数运算的具体使用，参考 :py:meth:`expression_math_analyst`

    如果输入两个像素类型（PixelFormat）均为整数类型的栅格数据集，则输出整数类型的结果数据集；否则，输出浮点型的结果数据集。如果输入的两个栅格数据集
    的像素类型精度不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。

    :param first_operand: 指定的第一栅格数据集。
    :type first_operand: DatasetGrid or str
    :param second_operand:  指定的第二栅格数据集。
    :type second_operand: DatasetGrid or str
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _first_input = get_input_dataset(first_operand)
    if _first_input is None:
        raise ValueError('first operand data is None')
    if not isinstance(_first_input, DatasetGrid):
        raise ValueError('first operand data must be DatasetGrid')
    _second_input = get_input_dataset(second_operand)
    if _second_input is None:
        raise ValueError('second operand data is None')
    else:
        if not isinstance(_second_input, DatasetGrid):
            raise ValueError('second operand data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + '_plus'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'plus_math_analyst')
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.plus(_first_input._jobject, _second_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def minus_math_analyst(first_operand, second_operand, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格减法运算。逐个像元地从第一个栅格数据集的栅格值中减去第二个数据集的栅格值。进行此运算时，输入栅格数据集的顺序很重要，顺序不同，结果通常也是不相同的。栅格代数运算的具体使用，参考 :py:meth:`expression_math_analyst`

    如果输入两个像素类型（PixelFormat）均为整数类型的栅格数据集，则输出整数类型的结果数据集；否则，输出浮点型的结果数据集。如果输入的两个栅格数据集
    的像素类型精度不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。

    :param first_operand: 指定的第一栅格数据集。
    :type first_operand: DatasetGrid or str
    :param second_operand:  指定的第二栅格数据集。
    :type second_operand: DatasetGrid or str
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    _first_input = get_input_dataset(first_operand)
    if _first_input is None:
        raise ValueError('first operand data is None')
    if not isinstance(_first_input, DatasetGrid):
        raise ValueError('first operand data must be DatasetGrid')
    _second_input = get_input_dataset(second_operand)
    if _second_input is None:
        raise ValueError('second operand data is None')
    else:
        if not isinstance(_second_input, DatasetGrid):
            raise ValueError('second operand data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + '_minus'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'minus_math_analyst')
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.minus(_first_input._jobject, _second_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def multiply_math_analyst(first_operand, second_operand, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格乘法运算。将输入的两个栅格数据集的栅格值逐个像元地相乘。栅格代数运算的具体使用，参考 :py:meth:`expression_math_analyst`

    如果输入两个像素类型（PixelFormat）均为整数类型的栅格数据集，则输出整数类型的结果数据集；否则，输出浮点型的结果数据集。如果输入的两个栅格数据集
    的像素类型精度不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。

    :param first_operand: 指定的第一栅格数据集。
    :type first_operand: DatasetGrid or str
    :param second_operand:  指定的第二栅格数据集。
    :type second_operand: DatasetGrid or str
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    _first_input = get_input_dataset(first_operand)
    if _first_input is None:
        raise ValueError('first operand data is None')
    if not isinstance(_first_input, DatasetGrid):
        raise ValueError('first operand data must be DatasetGrid')
    _second_input = get_input_dataset(second_operand)
    if _second_input is None:
        raise ValueError('second operand data is None')
    else:
        if not isinstance(_second_input, DatasetGrid):
            raise ValueError('second operand data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + '_multiply'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'multiply_math_analyst')
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.multiply(_first_input._jobject, _second_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def to_float_math_analyst(input_data, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
      栅格浮点运算。将输入的栅格数据集的栅格值转换成浮点型。 如果输入的栅格值为双精度浮点型，进行浮点运算后的结果栅格值也转换为单精度浮点型。

      :param input_data: 指定的第一栅格数据集。
      :type input_data: DatasetGrid or str
      :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
      :param out_data: 结果数据集所在的数据源
      :type out_data: Datasource or DatasourceConnectionInfo or str
      :param str out_dataset_name: 结果数据集名称
      :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
      :return: 结果数据集或数据集名称
      :rtype: DatasetGrid or str

    """
    _first_input = get_input_dataset(input_data)
    if _first_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_first_input, DatasetGrid):
            raise ValueError('source input_data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + '_float'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'to_float_math_analyst')
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.toFloat(_first_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def to_int_math_analyst(input_data, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
      栅格取整运算。提供对输入的栅格数据集的栅格值进行取整运算。取整运算的结果是去除栅格值的小数部分，只保留栅格值的整数。如果输入栅格值为整数类型，进行取整运算后的结果与输入栅格值相同。

      :param input_data: 指定的第一栅格数据集。
      :type input_data: DatasetGrid or str
      :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
      :param out_data: 结果数据集所在的数据源
      :type out_data: Datasource or DatasourceConnectionInfo or str
      :param str out_dataset_name: 结果数据集名称
      :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
      :return: 结果数据集或数据集名称
      :rtype: DatasetGrid or str

    """
    _first_input = get_input_dataset(input_data)
    if _first_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_first_input, DatasetGrid):
            raise ValueError('source input_data must be DatasetGrid')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + '_int'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'to_int_math_analyst')
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.toInt(_first_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def expression_math_analyst(expression, pixel_format, out_data, is_ingore_no_value=True, user_region=None, out_dataset_name=None, progress=None):
    """
    栅格代数运算类。用于提供对一个或多个栅格数据集的数学运算及函数运算。

    栅格代数运算的思想是运用代数学的观点对地理特征和现象进行空间分析。实质上，是对多个栅格数据集（DatasetGrid）进行数学运算以及函数运算。运算结果
    栅格的像元值是由输入的一个或多个栅格同一位置的像元的值通过代数规则运算得到的。

    栅格分析中很多功能都是基于栅格代数运算的，作为栅格分析的核心内容，栅格代数运算用途十分广泛，能够帮助我们解决各种类型的实际问题。如建筑工程中的计
    算填挖方量，将工程实施前的DEM栅格与实施后的DEM栅格相减，就能够从结果栅格中得到施工前后的高程差，将结果栅格的像元值与像元所代表的实际面积相乘，
    就可以得知工程的填方量与挖方量；又如，想要提取2000年全国范围内平均降雨量介于20毫米和50毫米的地区，可以通过“20<年平均降雨量<50”关系运算表达式，
    对年平均降雨量栅格数据进行运算而获得。

    通过该类的方法进行栅格代数运算主要有以下两种途径:

        - 使用该类提供的基础运算方法。该类提供了六个用于进行基础运算的方法，包括 plus（加法运算）、minus（减法运算）、multiply（乘法运算）、
          divide（除法运算）、to_int（取整运算）和 to_float（浮点运算）。使用这几个方法可以完成一个或多个栅格数据对应栅格值的算术运算。对于相
          对简单的运算，可以通过多次调用这几个方法来实现，如 (A/B)-(A/C)。
        - 执行运算表达式。使用表达式不仅可以对一个或多个栅格数据集实现运算符运算，还能够进行函数运算。运算符包括算术运算符、关系运算符和布尔运算符，
          算术运算主要包括加法（+）、减法（-）、乘法（*）、除法（/）；布尔运算主要包括和（And）、或（Or）、异或（Xor）、非（Not）；关系运算主要包括
          =、<、>、<>、>=、<=。注意，对于布尔运算和关系运算均有三种可能的输出结果：真＝1、假=0及无值（只要有一个输入值为无值，结果即为无值）。

    此外，还支持 21 种常用的函数运算，如下图所示:

    .. image:: ../image/MathAnalyst_Function.png

    执行栅格代数运算表达式，支持自定义表达式栅格运算，通过自定义表达式可以进行算术运算、条件运算、逻辑运算、函数运算（常用函数、三角函数）以及复合运算。
    栅格代数运算表达式的组成需要遵循以下规则:

        - 运算表达式应为一个形如下式的字符串:

            [DatasourceAlias1.Raster1] + [DatasourceAlias2.Raster2]
            使用“ [数据源别名.数据集名] ”来指定参加运算的栅格数据集；注意要使用方括号把名字括起来。

        - 栅格代数运算支持四则运算符（"+" 、"-" 、"*" 、"/" ）、条件运算符（">" 、">=" 、"<" 、"<=" 、"<>" 、"==" ）、逻辑运算符（"|" 、"&" 、"Not()" 、"^" ）和一些常用数学函数（"abs()" 、"acos()" 、"asin()" 、"atan()" 、"acot()" 、"cos()" 、"cosh()" 、"cot()" 、"exp()" 、"floor()" 、"mod(,)" 、"ln()" 、"log()" 、"pow(,)" 、"sin()" 、"sinh()" 、"sqrt()" 、"tan()" 、"tanh()" 、"Isnull()" 、"Con(,,)" 、"Pick(,,,..)" ）。
        - 代数运算的表达式中各个函数之间可以嵌套使用，直接用条件运算符计算的栅格结果都为二值（如大于、小于等），即满足条件的用1代替，不满足的用0代替，若想使用其他值来表示满足条件和不满足条件的取值，可以使用条件提取函数Con(,,)。例如："Con(IsNull([SURFACE_ANALYST.Dem3] ) ,100,Con([SURFACE_ANALYST.Dem3] > 100,[SURFACE_ANALYST.Dem3] ,-9999) ) " ，该表达式的含义是：栅格数据集 Dem3 在别名为 SURFACE_ANALYST 的数据源中，将其中无值栅格变为 100，剩余栅格中，大于100 的，值保持不变，小于等于 100 的，值改成 -9999。
        - 如果栅格计算中有小于零的负值，注意要加小括号，如：[DatasourceAlias1.Raster1] - ([DatasourceAlias2.Raster2])。
        - 表达式中，运算符连接的操作数可以是一个栅格数据集，也可以是数字或者数学函数。
        - 数学函数的自变量可以为一个数值，也可以为某个数据集，或者是一个数据集或多个数据集的运算表达式。
        - 表达式必须是没有回车的单行表达式。
        - 表达式中必须至少含有一个输入栅格数据集。

    注意:

        - 参与运算的两个数据集，如果其像素类型（PixelFormat）不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。例如，一个为32位整型，一个为单精度浮点型，那么进行加法运算后，结果数据集的像素类型将为单精度浮点型。
        - 对于栅格数据集中的无值数据，如果忽略无值，则无论何种运算，结果仍为无值；如果不忽略无值，意味着无值将参与运算。例如，两栅格数据集 A 和 B 相加，A 某单元格为无值，值为-9999，B 对应单元格值为3000，如果不忽略无值，则运算结果该单元格值为-6999。

    :param str expression:  自定义的栅格运算表达式。
    :param pixel_format: 指定的结果数据集的像素格式。注意，如果指定的像素类型的精度低于参与运算的栅格数据集像素类型的精度，运算结果可能不正确。
    :type pixel_format: PixelFormat or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param bool is_ingore_no_value:  是否忽略无值栅格数据。true 表示忽略无值数据，即无值栅格不参与运算。
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集
                                 的范围的交集作为计算区域。
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    check_lic()
    _jvm = get_jvm()
    try:
        try:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = 'MathExpression'
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
            print('outdatasetName: ' + _outDatasetName + '\r\n')
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'expression_math_analyst')
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.execute(expression, javaRegion, oj(PixelFormat._make(pixel_format)), False, is_ingore_no_value, oj(out_datasource), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    elif java_result_dt is not None:
        result_dt = out_datasource[java_result_dt.getName()]
    else:
        result_dt = None
    return try_close_output_datasource(result_dt, out_datasource)


def compute_min_distance(source, reference, min_distance, max_distance, out_data=None, out_dataset_name=None, progress=None):
    """
    最近距离计算。求算“被计算记录集”中每一个对象到“参考记录集”中在查询范围内的所有对象的距离中的最小值（即最近距离），并将最近距离信息保存到一个新的属性表数据集中。
    最近距离计算功能用于计算“被计算记录集”中每一个对象（称为“被计算对象”）到“参考记录集”中在查询范围内的所有对象（称为“参考对象”）的距离中的最小值，也就是最近距离，计算的结果为一个纯属性表数据集，记录了“被计算对象”到最近的“参考对象”的距离信息，使用三个属性字段存储，分别为：Source_ID（“被计算对象”的 SMID）、根据参考对象的类型可能为 Point_ID、Line_ID、Region_ID（“参考对象”的 SMID）以及 Distance（前面二者的距离值）。如果被计算对象与多个参考对象具有最近距离，则属性表中相应的添加多条记录。

    * 支持的数据类型

      “被计算记录集”仅支持二维点记录集，“参考记录集”可以是为从二维点、线、面数据集以及二维网络数据集获得的记录集。从二维网络数据集可以获得存有弧段的记录集，或存有结点的记录集（从网络数据集的子集获取），将这两种记录集作为“参考记录集”，可用于查找最近的弧段或最近的结点。

      “被计算记录集”和“参考记录集”可以是同一个记录集，也可以是从同一个数据集查询出的不同记录集，这两种情况下，不会计算对象到自身的距离。

    * 查询范围

      查询范围由用户指定的一个最小距离和一个最大距离构成，用于过滤不参与计算的“参考对象”，即从“被计算对象”出发，只有与其距离介于最小距离和最大距离之间（包括等于）的“参考对象”参与计算。如果将查询范围设置为从“0”到“-1”，则表示计算到“参考记录集”中所有对象的最近距离。

      如下图所示，红色圆点来自“被计算记录集”，方块来自“参考记录集”，粉色区域表示查询范围，则只有位于查询范围内的蓝色方块参与最近距离计算，也就是说本例的计算的结果只包含红色圆点与距其最近的蓝色方块的 SMID 和距离值

      .. image:: ../image/ComputeDistance.png

    * 注意事项：

      * “被计算记录集”和“参考记录集”所属的数据集的必须具有相同的坐标系。

      * 如下图所示，点到线对象的距离，是计算点到整个线对象的最小距离，即在线上找到一点与被计算点的距离最短；同样的，点到面对象的距离，是计算点到面对象的整个边界的最小距离。

        .. image:: ../image/ComputeDistance_1.png

      * 计算两个对象间距离时，出现包含或（部分）重叠的情况时，距离均为 0。例如点对象在线对象上，二者间距离为 0。

    :param source:  指定的被计算记录集。只支持二维点记录集和数据集
    :type source: DatasetVector or Recordset or str
    :param reference: 指定的参考记录集。支持二维点、线、面记录集和数据集
    :type reference: DatasetVector or Recordset or str
    :param min_distance: 指定的查询范围的最小距离。取值范围为大于或等于 0。单位与被计算记录集所属数据集的单位相同。
    :type min_distance: float
    :param max_distance:  指定的查询范围的最大距离。取值范围为大于 0 的值及 -1。当设置为 -1 时，表示不限制最大距离。单位与被计算记录集所属数据集的单位相同。
    :type max_distance: float
    :param out_data: 指定的用于存储结果属性表数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的结果属性表数据集的名称。
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return:  结果数据集或数据集名称
    :rtype: DatasetVector
    """
    if isinstance(source, DatasetVector):
        source_rd = source.get_recordset(False, 'STATIC', list())
    else:
        if isinstance(source, Recordset):
            source_rd = source
        else:
            if isinstance(source, str):
                source_info = source
                source = get_input_dataset(source)
                if source is not None:
                    source_rd = source.get_recordset(False, 'STATIC', list())
                else:
                    raise ValueError('Failed to get source recordset from ' + source_info)
            else:
                assert isinstance(source_rd, Recordset), 'source required DatasetVector or Recordset, but now is ' + str(type(source))
            if isinstance(reference, DatasetVector):
                reference_rd = reference.get_recordset(False, 'STATIC', list())
            else:
                if isinstance(reference, Recordset):
                    reference_rd = reference
                else:
                    if isinstance(reference, str):
                        reference_info = reference
                        reference = get_input_dataset(reference)
                        if reference is not None:
                            reference_rd = reference.get_recordset(False, 'STATIC', list())
                        else:
                            if not isinstance(source, Recordset):
                                source_rd.close()
                                del source_rd
                            raise ValueError('Failed to get reference recordset from ' + reference_info)
                    else:
                        if not isinstance(reference_rd, Recordset):
                            if not isinstance(source, Recordset):
                                source_rd.close()
                                del source_rd
                            raise ValueError('reference required DatasetVector or Recordset, but now is ' + str(type(source)))
                        elif out_data is not None:
                            out_datasource = get_output_datasource(out_data)
                        else:
                            out_datasource = source.datasource
                        check_output_datasource(out_datasource)
                        if out_dataset_name is None:
                            _outDatasetName = 'MinDistance'
                        else:
                            _outDatasetName = out_dataset_name
                    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
                    try:
                        try:
                            if min_distance is None:
                                min_distance = 0
                            else:
                                if max_distance is None:
                                    max_distance = -1.0
                                listener = None
                                if progress is not None:
                                    if safe_start_callback_server():
                                        try:
                                            listener = ProgressListener(progress, 'compute_min_distance')
                                            get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.addSteppedListener(listener)
                                        except Exception as e:
                                            try:
                                                close_callback_server()
                                                log_error(e)
                                                listener = None
                                            finally:
                                                e = None
                                                del e

                            computeMinDistance = get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.computeMinDistance
                            success = computeMinDistance(oj(source_rd), oj(reference_rd), float(min_distance), float(max_distance), oj(out_datasource), _outDatasetName)
                        except:
                            import traceback
                            log_error(traceback.format_exc())
                            success = False

                    finally:
                        if listener is not None:
                            try:
                                get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
                            except Exception as e1:
                                try:
                                    log_error(e1)
                                finally:
                                    e1 = None
                                    del e1

                            close_callback_server()
                        else:
                            if not isinstance(source, Recordset):
                                source_rd.close()
                                del source_rd
                            if not isinstance(reference, Recordset):
                                reference_rd.close()
                                del reference_rd
                            if success:
                                result_dt = out_datasource[_outDatasetName]
                            else:
                                result_dt = None
                        if out_data is not None:
                            return try_close_output_datasource(result_dt, out_datasource)
                        return result_dt


def compute_range_distance(source, reference, min_distance, max_distance, out_data=None, out_dataset_name=None, progress=None):
    """
    范围距离计算。求算“被计算记录集”中每一个对象到“参考记录集”中在查询范围内的每一个对象的距离，并将距离信息保存到一个新的属性表数据集中。

    该功能用于计算记录集 A 中每一个对象到记录集 B 中在查询范围内的每一个对象的距离，记录集 A 称为“被计算记录集”，当中的对象称作“被计算对象”，记录集 B 称为“参考记录集”，当中的对象称作“参考对象”。“被计算记录集”和“参考记录集”可以是同一个记录集，也可以是从同一个数据集查询出的不同记录集，这两种情况下，不会计算对象到自身的距离。

    查询范围由一个最小距离和一个最大距离构成，用于过滤不参与计算的“参考对象”，即从“被计算对象”出发，只有与其距离介于最小距离和最大距离之间（包括等于）的“参考对象”参与计算。

    如下图所示，红色圆点为“被计算对象”，方块为“参考对象”，粉色区域表示查询范围，则只有位于查询范围内的蓝色方块参与距离计算，也就是说本例的计算的结果只包含红色圆点与粉色区域内的蓝色方块的 SMID 和距离值。

    .. image:: ../image/ComputeDistance.png

    范围距离计算的结果为一个纯属性表数据集，记录了“被计算对象”到“参考对象”的距离信息，使用三个属性字段存储，分别为：Source_ID（“被计算对象”的 SMID）、根据参考对象的类型可能为 Point_ID、Line_ID、Region_ID（“参考对象”的 SMID）以及 Distance（前面二者的距离值）。

    注意事项：

     * “被计算记录集”和“参考记录集”所属的数据集的必须具有相同的坐标系。

     * 如下图所示，点到线对象的距离，是计算点到整个线对象的最小距离，即在线上找到一点与被计算点的距离最短；同样的，点到面对象的距离，是计算点到面对象的整个边界的最小距离。

       .. image:: ../image/ComputeDistance_1.png

     * 计算两个对象间距离时，出现包含或（部分）重叠的情况时，距离均为 0。例如点对象在线对象上，二者间距离为 0。

    :param source: 指定的被计算记录集。只支持二维点记录集或数据集
    :type source: DatasetVector or Recordset or str
    :param reference: 指定的参考记录集。只支持二维点、线、面记录集或数据集
    :type reference: DatasetVector or Recordset or str
    :param min_distance: 指定的查询范围的最小距离。取值范围为大于或等于 0。 单位与被计算记录集所属数据集的单位相同。
    :type min_distance: float
    :param max_distance: 指定的查询范围的最大距离。取值范围为大于或等于 0，且必须大于或等于最小距离。单位与被计算记录集所属数据集的单位相同。
    :type max_distance: float
    :param out_data: 指定的用于存储结果属性表数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 指定的结果属性表数据集的名称。
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector
    """
    if isinstance(source, DatasetVector):
        source_rd = source.get_recordset(False, 'STATIC', list())
    else:
        if isinstance(source, Recordset):
            source_rd = source
        else:
            if isinstance(source, str):
                source_info = source
                source = get_input_dataset(source)
                if source is not None:
                    source_rd = source.get_recordset(False, 'STATIC', list())
                else:
                    raise ValueError('Failed to get source recordset from ' + source_info)
            else:
                assert isinstance(source_rd, Recordset), 'source required DatasetVector or Recordset, but now is ' + str(type(source))
            if isinstance(reference, DatasetVector):
                reference_rd = reference.get_recordset(False, 'STATIC', list())
            else:
                if isinstance(reference, Recordset):
                    reference_rd = reference
                else:
                    if isinstance(reference, str):
                        reference_info = reference
                        reference = get_input_dataset(reference)
                        if reference is not None:
                            reference_rd = reference.get_recordset(False, 'STATIC', list())
                        else:
                            if not isinstance(source, Recordset):
                                source_rd.close()
                                del source_rd
                            raise ValueError('Failed to get reference recordset from ' + reference_info)
                    else:
                        if not isinstance(reference_rd, Recordset):
                            if not isinstance(source, Recordset):
                                source_rd.close()
                                del source_rd
                            raise ValueError('reference required DatasetVector or Recordset, but now is ' + str(type(source)))
                        elif out_data is not None:
                            out_datasource = get_output_datasource(out_data)
                        else:
                            out_datasource = source.datasource
                        check_output_datasource(out_datasource)
                        if out_dataset_name is None:
                            _outDatasetName = 'RangeDistance'
                        else:
                            _outDatasetName = out_dataset_name
                    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
                    try:
                        try:
                            if min_distance is None:
                                min_distance = 0
                            else:
                                if max_distance is None or float(max_distance) <= float(min_distance):
                                    raise ValueError('max_distance cannot be None or zero, must be greater than min_distance')
                                listener = None
                                if progress is not None:
                                    if safe_start_callback_server():
                                        try:
                                            listener = ProgressListener(progress, 'compute_range_distance')
                                            get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.addSteppedListener(listener)
                                        except Exception as e:
                                            try:
                                                close_callback_server()
                                                log_error(e)
                                                listener = None
                                            finally:
                                                e = None
                                                del e

                            computeRangeDistance = get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.computeRangeDistance
                            success = computeRangeDistance(oj(source_rd), oj(reference_rd), float(min_distance), float(max_distance), oj(out_datasource), _outDatasetName)
                        except:
                            import traceback
                            log_error(traceback.format_exc())
                            success = False

                    finally:
                        if listener is not None:
                            try:
                                get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
                            except Exception as e1:
                                try:
                                    log_error(e1)
                                finally:
                                    e1 = None
                                    del e1

                            close_callback_server()
                        elif isinstance(source, DatasetVector):
                            if source_rd is not None:
                                source_rd.close()
                                del source_rd
                            if isinstance(reference, DatasetVector):
                                if reference_rd is not None:
                                    reference_rd.close()
                                    del reference_rd
                            if success:
                                result_dt = out_datasource[_outDatasetName]
                        else:
                            result_dt = None
                        if out_data is not None:
                            return try_close_output_datasource(result_dt, out_datasource)
                        return result_dt


def integrate(source, tolerance, unit=None, progress=None):
    """
    整合, 将容限范围内的节点捕捉在一起。节点容限较大会导致要素重叠或导致面和线对象被删除，还可能导致不被期望移动的节点发生移动。
    所以，选取容限值时应当根据实际情形设置合理的容限值。

    注意：整合功能将直接修改源数据集。

    :param source: 指定的待整合的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param tolerance: 指定的节点容限。
    :type tolerance: float
    :param unit:  指定的节点容限单位。
    :type unit: Unit or str
    :param progress:
    :type progress: function
    :return: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :rtype: bool
    """
    try:
        try:
            source_dt = get_input_dataset(source)
            if not isinstance(source_dt, DatasetVector):
                raise ValueError('source required DatasetVector, but now is ' + str(type(source_dt)))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'integrate')
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            unit = Unit._make(unit)
            if unit is None:
                unit = source_dt.prj_coordsys.coord_unit
            integrate = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.integrate
            success = integrate(oj(source_dt), float(tolerance), oj(unit))
        except:
            import traceback
            log_error(traceback.format_exc())
            success = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return success


def eliminate(source, region_tolerance, vertex_tolerance, is_delete_single_region=False, progress=None):
    """
    碎多边形合并，即将数据集中小于指定面积的多边形合并到相邻的多边形中。目前仅支持将碎多边形合并到与其相邻的具有最大面积的多边形中。

    在数据制作和处理过程中，或对不精确的数据进行叠加后，都可能产生一些细碎而无用的多边形，称为碎多边形。可以通过“碎多边形合并”
    功能将这些细碎多边形合并到相邻的多边形中，或删除孤立的碎多边形（没有与其他多边形相交或者相切的多边形），以达到简化数据的目的。

    一般面积远远小于数据集中其他对象的多边形才被认为是“碎多边形”，通常是同一数据集中最大面积的百万分之一到万分之一间，但可以依
    据实际研究的需求来设置最小多边形容限。如下图所示的数据中，在较大的多边形的边界上，有很多无用的碎多边形。

    .. image:: ../image/Eliminate_1.png

    下图是对该数据进行“碎多边形合并”处理后的结果，与上图对比可以看出，碎多边形都被合并到了相邻的较大的多边形中。

    .. image:: ../image/Eliminate_2.png

    注意：

        * 该方法适用于两个面具有公共边界的情况，处理后会把公共边界去除。
        * 进行碎多边形合并处理后，数据集内的对象数量可能减少。

    :param source: 指定的待进行碎多边形合并的数据集。只支持矢量二维面数据集，指定其他类型的数据集会抛出异常。
    :type source: DatasetVector or str
    :param region_tolerance: 指定的最小多边形容限。单位与系统计算的面积（SMAREA 字段）的单位一致。将 SMAREA 字段的值与该容限值对比，小于该值的多边形将被消除。取值范围为大于等于0，指定为小于0的值会抛出异常。
    :type region_tolerance: float
    :param vertex_tolerance: 指定的节点容限。单位与进行碎多边形合并的数据集单位相同。若两个节点之间的距离小于此容限值，则合并过程中会自动将这两个节点合并为一个节点。取值范围大于等于0，指定为小于0的值会抛出异常。
    :type vertex_tolerance: float
    :param is_delete_single_region: 指定是否删除孤立的小多边形。如果为 true 会删除孤立的小多边形，否则不删除。
    :type is_delete_single_region: bool
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 整合成功返回 True，失败返回 False
    :rtype: bool
    """
    listener = None
    try:
        try:
            source_dt = get_input_dataset(source)
            if not isinstance(source_dt, DatasetVector):
                raise ValueError('source required DatasetVector, but now is ' + str(type(source_dt)))
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'eliminate')
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            from .enums import _EliminateMode
            eliminate_mode = _EliminateMode._make('ELIMINATE_BY_AREA')
            eliminate = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.eliminate
            success = eliminate(oj(source_dt), float(region_tolerance), float(vertex_tolerance), oj(eliminate_mode), bool(is_delete_single_region))
        except:
            import traceback
            log_error(traceback.format_exc())
            success = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return success


def edge_match(source, target, edge_match_mode, tolerance=None, is_union=False, edge_match_line=None, out_data=None, out_dataset_name=None, progress=None):
    """
    图幅接边，对两个二维线数据集进行自动接边。

    :param source: 接边源数据集。只能是二维线数据集。
    :type source: DatasetVector
    :param target: 接边目标数据。只能是二维线数据集，与接边源数据有相同的坐标系。
    :type target: DatasetVector
    :param edge_match_mode: 接边模式。
    :type edge_match_mode: EdgeMatchMode or str
    :param tolerance: 接边容限。单位与进行接边的数据集的单位相同。
    :type tolerance: float
    :param is_union: 是否进行接边融合。
    :type is_union: bool
    :param edge_match_line: 数据接边的接边线。在接边方式为交点位置接边 EdgeMatchMode.THE_INTERSECTION 的时候用来计算交点，
                            不设置将按照数据集范围自动计算接边线来计算交点。
                            设置接边线后，发生接边关联的对象的端点将尽可能的靠到接边线上。
    :type edge_match_line: GeoLine
    :param out_data: 接边关联数据所在的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 接边关联数据的数据集名称。
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 如果设置了接边关联数据集且接边成功，则返回接边关联数据集对象或数据集名称。如果没有设置接边关联数据集，将不会生成
             接边关联数据集，则返回是否进行接边成功。
    :rtype: DatasetVector or str or bool
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but now is ' + str(type(source_dt)))
    else:
        target_dt = get_input_dataset(target)
        if not isinstance(target_dt, DatasetVector):
            raise ValueError('target required DatasetVector, but now is ' + str(type(target_dt)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
        else:
            out_datasource = None
        if out_datasource is not None:
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + '_edge_link'
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            _outDatasetName = None
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'edge_match')
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_edge_param = get_jvm().com.supermap.analyst.spatialanalyst.EdgeMatchParameter()
            if edge_match_line is not None:
                java_edge_param.setEdgeMatchLine(oj(edge_match_line))
            java_edge_param.setEdgeMatchMode(oj(EdgeMatchMode._make(edge_match_mode)))
            if is_union is not None:
                java_edge_param.setUnion(bool(is_union))
            if tolerance is not None:
                java_edge_param.setTolerance(float(tolerance))
            if out_datasource is not None:
                java_edge_param.setOutputDatasource(oj(out_datasource))
                java_edge_param.setOutputDatasetLinkName(_outDatasetName)
            edgeMatch = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.edgeMatch
            success = edgeMatch(oj(source_dt), oj(target_dt), java_edge_param)
            del java_edge_param
        except:
            import traceback
            log_error(traceback.format_exc())
            success = False

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if out_datasource is not None:
            if success:
                result_dt = out_datasource[_outDatasetName]
            else:
                result_dt = None
            return try_close_output_datasource(result_dt, out_datasource)
        return success


def region_to_center_line(region_data, out_data=None, out_dataset_name=None, progress=None):
    """
    提取面数据集或记录集的中心线，一般用于提取河流的中心线。

    该方法用于提取面对象的中心线。如果面包含岛洞，提取时会绕过岛洞，采用最短路径绕过。如下图。

    .. image:: ../image/RegionToCenterLine_1.png

    如果面对象不是简单的长条形，而是具有分叉结构，则提取的中心线是最长的一段。如下图所示。

    .. image:: ../image/RegionToCenterLine_2.png

    :param region_data: 指定的待提取中心线的面记录集或面数据集
    :type region_data: Recordset or DatasetVector
    :param out_data: 结果数据源信息或数据源对象
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果中心线数据集名称
    :type out_dataset_name: str
    :param progress:  进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集对象或结果数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    if isinstance(region_data, Recordset):
        source_rd = region_data
    else:
        if isinstance(region_data, DatasetVector):
            source_rd = region_data.get_recordset(False, 'STATIC')
        else:
            if isinstance(region_data, str):
                region_data = get_input_dataset(region_data)
                if region_data is not None:
                    source_rd = region_data.get_recordset(False, 'STATIC')
            else:
                if not isinstance(source_rd, Recordset):
                    raise ValueError('region_data required region Recordset or Dataset')
                else:
                    if source_rd.dataset.type is not DatasetType.REGION:
                        if not isinstance(region_data, Recordset):
                            source_rd.close()
                            del source_rd
                        raise ValueError('region_data required region Recordset or Dataset')
                    if out_data is not None:
                        out_datasource = get_output_datasource(out_data)
                    else:
                        out_datasource = source_rd.datasource
                check_output_datasource(out_datasource)
                if out_dataset_name is None:
                    _outDatasetName = source_rd.dataset.name + '_center'
                else:
                    _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
            try:
                try:
                    listener = None
                    if progress is not None:
                        if safe_start_callback_server():
                            try:
                                listener = ProgressListener(progress, 'region_to_center_line')
                                get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                            except Exception as e:
                                try:
                                    close_callback_server()
                                    log_error(e)
                                    listener = None
                                finally:
                                    e = None
                                    del e

                    regionToCenterLine = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.regionToCenterLine
                    java_result_dt = regionToCenterLine(oj(source_rd), oj(out_datasource), _outDatasetName)
                except:
                    import traceback
                    log_error(traceback.format_exc())
                    java_result_dt = None

            finally:
                if listener is not None:
                    try:
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
                    except Exception as e1:
                        try:
                            log_error(e1)
                        finally:
                            e1 = None
                            del e1

                    close_callback_server()
                else:
                    if not isinstance(region_data, Recordset):
                        source_rd.close()
                        del source_rd
                    if java_result_dt is not None:
                        result_dt = out_datasource[java_result_dt.getName()]
                    else:
                        result_dt = None
                if out_data is not None:
                    return try_close_output_datasource(result_dt, out_datasource)
                return result_dt


def dual_line_to_center_line(source_line, max_width, min_width, out_data=None, out_dataset_name=None, progress=None):
    """

    根据给定的宽度从双线记录集或数据集中提取中心线。
    该功能一般用于提取双线道路或河流的中心线。双线要求连续且平行或基本平行，提取效果如下图。

    .. image:: ../image/DualLineToCenterLine.png

    注意：

     * 双线一般为双线道路或双线河流，可以是线数据，也可以是面数据。
     * max_width 和 min_width 参数用于指定记录集中双线的最大宽度和最小宽度,用于提取最小和最大宽度之间的双线的中心线。小于最小宽度、大于最大宽度部分的双线不提取中心线，且大于最大宽度的双线保留，小于最小宽度的双线丢弃。
     * 对于双线道路或双线河流中比较复杂的交叉口，如五叉六叉，或者双线的最大宽度和最小宽度相差较大的情形，提取的结果可能不理想。

    :param source_line: 指定的双线记录集或数据集。要求为面类型的数据集或记录集。
    :type source_line: DatasetVector or Recordset or str
    :param max_width: 指定的双线的最大宽度。要求为大于 0 的值。单位与双线记录集所属的数据集相同。
    :type max_width: float
    :param min_width: 指定的双线的最小宽度。要求为大于或等于 0 的值。单位与双线记录集所属的数据集相同。
    :type min_width: float
    :param out_data: 指定的用于存储结果中心线数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 指定的结果中心线数据集的名称。
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集对象或结果数据集名称
    :rtype: DatasetVector or str
    """
    if isinstance(source_line, Recordset):
        source_rd = source_line
    else:
        if isinstance(source_line, DatasetVector):
            source_rd = source_line.get_recordset(False, 'STATIC')
        else:
            if isinstance(source_line, str):
                source_line = get_input_dataset(source_line)
                if source_line is not None:
                    source_rd = source_line.get_recordset(False, 'STATIC')
            else:
                if not isinstance(source_rd, Recordset):
                    raise ValueError('region_data required line or region Recordset or Dataset')
                else:
                    if source_rd.dataset.type not in (DatasetType.LINE, DatasetType.REGION):
                        if not isinstance(source_line, Recordset):
                            source_rd.close()
                            del source_rd
                        raise ValueError('region_data required line or region Recordset or Dataset')
                    if out_data is not None:
                        out_datasource = get_output_datasource(out_data)
                    else:
                        out_datasource = source_rd.datasource
                check_output_datasource(out_datasource)
                if out_dataset_name is None:
                    _outDatasetName = source_rd.dataset.name + '_centerline'
                else:
                    _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
            try:
                try:
                    listener = None
                    if progress is not None:
                        if safe_start_callback_server():
                            try:
                                listener = ProgressListener(progress, 'dual_line_to_center_line')
                                get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                            except Exception as e:
                                try:
                                    close_callback_server()
                                    log_error(e)
                                    listener = None
                                finally:
                                    e = None
                                    del e

                    dualLineToCenterLine = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.dualLineToCenterLine
                    java_result_dt = dualLineToCenterLine(oj(source_rd), float(max_width), float(min_width), oj(out_datasource), _outDatasetName)
                except:
                    import traceback
                    log_error(traceback.format_exc())
                    java_result_dt = None

            finally:
                if listener is not None:
                    try:
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
                    except Exception as e1:
                        try:
                            log_error(e1)
                        finally:
                            e1 = None
                            del e1

                    close_callback_server()
                else:
                    if not isinstance(source_line, Recordset):
                        source_rd.close()
                        del source_rd
                    if java_result_dt is not None:
                        result_dt = out_datasource[java_result_dt.getName()]
                    else:
                        result_dt = None
                if out_data is not None:
                    return try_close_output_datasource(result_dt, out_datasource)
                return result_dt


def _get_surface_extract_parameter(datum_value=0.0, interval=0.0, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, expected_z_values=None):
    java_param = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceExtractParameter()
    java_param.setDatumValue(float(datum_value))
    if interval <= 0:
        raise ValueError('interval must be greater than 0, now is ' + str(interval))
    java_param.setInterval(float(interval))
    java_param.setResampleTolerance(float(resample_tolerance))
    if smooth_method is not None:
        java_param.setSmoothMethod(oj(SmoothMethod._make(smooth_method)))
    java_param.setSmoothness(int(smoothness))
    if expected_z_values is not None:
        java_param.setExpectedZValues(to_java_double_array(split_input_list_from_str(expected_z_values)))
    return java_param


def grid_extract_isoline(extracted_grid, interval, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从栅格数据集中提取等值线，并将结果保存为数据集。

    等值线是由一系列具有相同值的点连接而成的光滑曲线或折线，如等高线、等温线。等值线的分布反映了栅格表面上值的变化，等值线分布越密集的地方， 表示栅格表面值的变化比较剧烈，例如，如果为等高线，则越密集，坡度越陡峭，反之坡度越平缓。通过提取等值线，可以找到高程、温度、降水等的值相同的位置， 同时等值线的分布状况也可以显示出变化的陡峭和平缓区。

    如下所示，上图为某个区域的 DEM 栅格数据，下图是从上图中提取的等高线。DEM 栅格数据的高程信息是存储在每一个栅格单元中的，栅格是有大小的，栅格的大小取决于栅格数据的分辨率 ，即每一个栅格单元代表实际地面上的相应地块的大小，因此，栅格数据不能很精确的反应每一位置上的高程信息 ，而矢量数据在这方面相对具有很大的优势，因此，从栅格数据中提取等高线 ，把栅格数据变成矢量数据，就可以突出显示数据的细节部分，便于分析，例如，从等高线数据中可以明显的区分地势的陡峭与舒缓的部位，可以区分出山脊山谷

    .. image:: ../image/SurfaceAnalyst_1.png

    .. image:: ../image/SurfaceAnalyst_2.png

    SuperMap 提供两种方法来提取等值线：

        * 通过设置基准值（datum_value）和等值距（interval）来提取等间距的等值线。该方法是以等值距为间隔向基准值的前后两个方向
          计算提取哪些高程的等值线。例如，高程范围为15-165的 DEM 栅格数据，设置基准值为50，等值距为20，则提取等值线的高程分别
          为：30、50、70、90、110、130和150。
        * 通过 expected_z_values 方法指定一个 Z 值的集合，则只提取高程为集合中值的等值线/面。例如，高程范围为0-1000的 DEM 栅
          格数据，指定 Z 值集合为[20,300,800]，那么提取的结果就只有 20、300、800 三条等值线或三者构成的等值面。

    注意：
        * 如果同时调用了上面两种方法所需设置的属性，那么只有 expected_z_values 方法有效，即只提取指定的值的等值线。因此，想要
          提取等间距的等值线，就不能调用 expected_z_values 方法。

    :param extracted_grid: 指定的提取操作需要的参数。
    :type extracted_grid: DatasetGrid or str
    :param  float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0.
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值线。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值线的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float

    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。

                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值线或等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。等值线提取时，光滑度可自由设置
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。如果不需要对操作结果进行裁剪，可以使用 None 值取代该参数。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则会直接返回等值线对象的列表。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值线得到的数据集或数据集名称，或等值线对象列表。
    :rtype: DatasetVector or str or list[GeoLine]
    """
    check_lic()
    source_dt = get_input_dataset(extracted_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('extracted_grid required DatasetGrid, but is ' + str(type(extracted_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + '_isoline'
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            out_datasource = None
            _outDatasetName = None
        if clip_region is not None:
            java_clip_region = oj(clip_region)
        else:
            java_clip_region = None
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'grid_extract_isoline')
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoline = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoline
            if out_datasource is not None:
                if java_clip_region is not None:
                    java_result = extractIsoline(java_param, oj(source_dt), oj(out_datasource), _outDatasetName, java_clip_region)
                else:
                    java_result = extractIsolinejava_paramoj(source_dt)oj(out_datasource)_outDatasetName
            else:
                java_result = extractIsoline(java_param, oj(source_dt), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_clip_region is not None:
            java_clip_region.dispose()
        del java_clip_region
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def point_extract_isoline(extracted_point, z_value_field, resolution, interval, terrain_interpolate_type=None, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从点数据集中提取等值线，并将结果保存为数据集。方法的实现原理类似“从点数据集中提取等值线”的方法，不同之处在于，
    这里的操作对象是点数据集，因此， 实现的过程是先对点数据集中的点数据使用 IDW 插值法（'InterpolationAlgorithmType.IDW` ）
    进行插值分析，得到栅格数据集（方法实现的中间结果，栅格值为单精度浮点型），然后从栅格数据集中提取等值线。

    点数据中的点是分散分布，点数据能够很好的表现位置信息，但对于点本身的其他属性信息却表现不出来，例如，已经获取了某个研究区域的
    大量采样点的高程信息，如下所示 （上图），从图上并不能看出地势高低起伏的趋势，看不出哪里地势陡峭、哪里地形平坦，如果我们运用
    等值线的原理，将这些点数据所蕴含的信息以等值线的形式表现出来， 即将相邻的具有相同高程值的点连接起来 ，形成下面下图所示的等
    高线图，那么关于这个区域的地形信息就明显的表现出来了。不同的点数据提取的等值线具有不同的含义，主要依据点数据多代表的信息而定，
    如果点的值代表温度，那么提取的等值线就是等温线；如果点的值代表雨量，那么提取的等值线就是等降水量线，等等。

    .. image:: ../image/SurfaceAnalyst_3.png

    .. image:: ../image/SurfaceAnalyst_4.png

    注意：

     * 从点数据（点数据集/记录集/三维点集合）中提取等值线（面）时，插值得出的中间结果栅格的分辨率如果太小，会导致提取等值线（面）
       失败。这里提供一个判断方法：使用点数据的 Bounds 的长和宽分别除以设置的分辨率，也就是中间结果栅格的行列数，如果行列数任何一
       个大于10000，即认为分辨率设置的过小了，此时系统会抛出异常

    :param extracted_point: 指定的待提取的点数据集或记录集
    :type extracted_point: DatasetVector or str or Recordset
    :param z_value_field: 指定的用于提取操作的字段名称。提取等值线时，将使用该字段中的值，对点数据集进行插值分析。
    :type z_value_field: str
    :param resolution: 指定的中间结果（栅格数据集）的分辨率。
    :type resolution: float
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param terrain_interpolate_type: 地形插值类型。
    :type terrain_interpolate_type: TerrainInterpolateType or str
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值线。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值线的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。

                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值线或等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。等值线提取时，光滑度可自由设置
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。 如果为空，则会直接返回等值线对象的列表。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值线得到的数据集或数据集名称，或等值线对象列表
    :rtype: DatasetVector or str or list[GeoLine]
    """
    check_lic()
    source_dt = get_input_dataset(extracted_point)
    if not isinstance(source_dt, (DatasetVector, Recordset)):
        raise ValueError('extracted_point required DatasetVector or Recordset, but is ' + str(type(extracted_point)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + '_isoline'
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            out_datasource = None
            _outDatasetName = None
        if clip_region is not None:
            java_clip_region = oj(GeoRegion(clip_region))
        else:
            java_clip_region = None
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'point_extract_isoline')
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoline = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoline
            if out_datasource is not None:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoline(java_param, oj(source_dt), str(z_value_field), oj(terrain_interpolate_type), oj(out_datasource), _outDatasetName, float(resolution), java_clip_region)
                else:
                    java_result = extractIsolinejava_paramoj(source_dt)str(z_value_field)oj(out_datasource)_outDatasetNamefloat(resolution)java_clip_region
            else:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoline(java_param, oj(source_dt), str(z_value_field), oj(terrain_interpolate_type), float(resolution), java_clip_region)
                else:
                    java_result = extractIsoline(java_param, oj(source_dt), str(z_value_field), float(resolution), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def point3ds_extract_isoline(extracted_points, resolution, interval, terrain_interpolate_type=None, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从三维点集合中提取等值线，并将结果保存为数据集。方法的实现原理是先利用点集合中存储的三维信息（高程或者温度等），也就是
    除了点的坐标信息的数据， 对点数据进行插值分析，得到栅格数据集（方法实现的中间结果，栅格值为单精度浮点型），然后从栅格数据集
    中提取等值线。

    点数据提取等值线介绍参考 :py:meth:`point_extract_isoline`

    注意：

     * 从点数据（点数据集/记录集/三维点集合）中提取等值线（面）时，插值得出的中间结果栅格的分辨率如果太小，会导致提取等值线（面）
       失败。这里提供一个判断方法：使用点数据的 Bounds 的长和宽分别除以设置的分辨率，也就是中间结果栅格的行列数，如果行列数任何一
       个大于10000，即认为分辨率设置的过小了，此时系统会抛出异常

    :param extracted_points: 指定的待提取等值线的点串，该点串中的点是三维点，每一个点存储了 X，Y 坐标信息和只有一个三维度的信息（例如：高程信息等）。
    :type extracted_points: list[Point3D]
    :param resolution: 指定的中间结果（栅格数据集）的分辨率。
    :type resolution: float
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param terrain_interpolate_type: 地形插值类型。
    :type terrain_interpolate_type: TerrainInterpolateType or str
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值线。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值线的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。
                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值线或等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。等值线提取时，光滑度可自由设置;
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则直接返回等值线对象列表
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值线得到的数据集或数据集名称，或等值线对象列表
    :rtype: DatasetVector or str or list[GeoLine]
    """
    check_lic()
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = 'isoline'
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    else:
        out_datasource = None
        _outDatasetName = None
    if clip_region is not None:
        java_clip_region = oj(GeoRegion(clip_region))
    else:
        java_clip_region = None
    java_point_3ds = to_java_point3ds(extracted_points)
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'point3ds_extract_isoline')
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoline = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoline
            if out_datasource is not None:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsolinejava_paramjava_point_3dsoj(terrain_interpolate_type)oj(out_datasource)_outDatasetNamefloat(resolution)java_clip_region
                else:
                    java_result = extractIsoline(java_param, java_point_3ds, oj(out_datasource), _outDatasetName, float(resolution), java_clip_region)
            else:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoline(java_param, java_point_3ds, oj(terrain_interpolate_type), float(resolution), java_clip_region)
                else:
                    java_result = extractIsolinejava_paramjava_point_3dsfloat(resolution)java_clip_region
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def grid_extract_isoregion(extracted_grid, interval, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从栅格数据集中提取等值面。

    SuperMap 提供两种方法来提取等值面：

    * 通过设置基准值（datum_value）和等值距（interval）来提取等间距的等值面。该方法是以等值距为间隔向基准值的前后两个方向计算
      提取哪些高程的等值线。例如，高程范围为15-165的 DEM 栅格数据，设置基准值为50，等值距为20，则提取等值线的高程分别为：
      30、50、70、90、110、130和150。
    * 通过 expected_z_values 方法指定一个 Z 值的集合，则只提取高程为集合中值的等值面。例如，高程范围为0-1000的 DEM 栅格数据，
      指定 Z 值集合为[20,300,800]，那么提取的结果就只有20、300、800三者构成的等值面。

    注意：

     * 如果同时调用了上面两种方法所需设置的属性，那么只有 setExpectedZValues 方法有效，即只提取指定的值的等值面。
       因此，想要提取等间距的等值面，就不能调用 expected_z_values 方法。

    :param extracted_grid: DatasetGrid or str
    :type extracted_grid:  指定的待提取的栅格数据集。
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值面。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值面的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。
                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。
                       对于等值面的提取，采用先提取等值线然后生成等值面的方式，若将光滑度设置为2，
                       则中间结果数据集，即等值线对象的点数将为原始数据集点数的2倍，当光滑度设定值不断增大时，点数将成2的指数倍
                       增长，这将大大降低等值面提取的效率甚至可能导致提取失败。
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则直接返回等值面对象列表
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值面得到的数据集或数据集名称，或等值面对象列表
    :rtype: DatasetVector or str or list[GeoRegion]
    """
    check_lic()
    source_dt = get_input_dataset(extracted_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('extracted_grid required DatasetGrid, but is ' + str(type(extracted_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + '_isoregion'
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            out_datasource = None
            _outDatasetName = None
        if clip_region is not None:
            java_clip_region = oj(GeoRegion(clip_region))
        else:
            java_clip_region = None
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'grid_extract_isoregion')
                    get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
                extractIsoregion = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoregion
                if out_datasource is not None:
                    java_result = extractIsoregion(java_param, oj(source_dt), oj(out_datasource), _outDatasetName, java_clip_region)
                else:
                    java_result = extractIsoregion(java_param, oj(source_dt), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                return try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def points_extract_isoregion(extracted_point, z_value_field, interval, resolution=None, terrain_interpolate_type=None, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从点数据集中提取等值面。方法的实现原理是先对点数据集使用 IDW 插值法（InterpolationAlgorithmType.IDW）进行插值分析，
    得到栅格数据集（方法实现的中间结果，栅格值为单精度浮点型），接着从栅格数据集中提取等值线， 最终由等值线构成等值面。

    等值面是由相邻的等值线封闭组成的面。等值面的变化可以很直观的表示出相邻等值线之间的变化，诸如高程、温度、降水、污染或大气压
    力等用等值面来表示是非常直观、 有效的。等值面分布的效果与等值线的分布相同，也是反映了栅格表面上的变化，等值面分布越密集的地
    方，表示栅格表面值有较大的变化，反之则表示栅格表面值变化较少； 等值面越窄的地方，表示栅格表面值有较大的变化，反之则表示栅格
    表面值变化较少。

    如下所示，上图为存储了高程信息的点数据集，下图为从上图点数据集中提取的等值面，从等值面数据中可以明显的分析出地形的起伏变化，
    等值面越密集， 越狭窄的地方表示地势越陡峭，反之，等值面越稀疏，较宽的地方表示地势较舒缓，变化较小。

    .. image:: ../image/SurfaceAnalyst_5.png

    .. image:: ../image/SurfaceAnalyst_6.png

    注意：

     * 从点数据（点数据集/记录集/三维点集合）中提取等值面时，插值得出的中间结果栅格的分辨率如果太小，会导致提取等值面
       失败。这里提供一个判断方法：使用点数据的 Bounds 的长和宽分别除以设置的分辨率，也就是中间结果栅格的行列数，如果行列数任何一个
       大于10000，即认为分辨率设置的过小了，此时系统会抛出异常。

    :param extracted_point: 指定的待提取的点数据集或记录集
    :type extracted_point: DatasetVector or str or Recordset
    :param z_value_field: 指定的用于提取操作的字段名称。提取等值面时，将使用该字段中的值，对点数据集进行插值分析。
    :type z_value_field: str
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param resolution: 指定的中间结果（栅格数据集）的分辨率。
    :type resolution: float
    :param terrain_interpolate_type: 指定的地形插值类型。
    :type terrain_interpolate_type: TerrainStatisticType
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值面。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值面的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。
                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。
                       对于等值面的提取，采用先提取等值线然后生成等值面的方式，若将光滑度设置为2，
                       则中间结果数据集，即等值线对象的点数将为原始数据集点数的2倍，当光滑度设定值不断增大时，点数将成2的指数倍
                       增长，这将大大降低等值面提取的效率甚至可能导致提取失败。
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则直接返回等值面对象列表
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值面得到的数据集或数据集名称，或等值面对象列表
    :rtype: DatasetVector or str or list[GeoRegion]
    """
    source_dt = get_input_dataset(extracted_point)
    if not isinstance(source_dt, (DatasetVector, Recordset)):
        raise ValueError('extracted_point required DatasetVector or Recordset, but is ' + str(type(extracted_point)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + '_isoregion'
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            out_datasource = None
            _outDatasetName = None
        if clip_region is not None:
            java_clip_region = oj(GeoRegion(clip_region))
        else:
            java_clip_region = None
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'points_extract_isoregion')
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoregion = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoregion
            if out_datasource is not None:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoregion(java_param, oj(source_dt), str(z_value_field), oj(terrain_interpolate_type), oj(out_datasource), _outDatasetName, float(resolution), java_clip_region)
                else:
                    java_result = extractIsoregionjava_paramoj(source_dt)str(z_value_field)oj(out_datasource)_outDatasetNamefloat(resolution)java_clip_region
            else:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoregion(java_param, oj(source_dt), str(z_value_field), oj(terrain_interpolate_type), float(resolution), java_clip_region)
                else:
                    java_result = extractIsoregion(java_param, oj(source_dt), str(z_value_field), float(resolution), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                return try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def point3ds_extract_isoregion(extracted_points, resolution, interval, terrain_interpolate_type=None, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从三维点集合中提取等值面，并将结果保存为数据集。方法的实现原理是先利用点集合中存储的第三维信息（高程或者温度等），也就
    是除了点的坐标信息的数据， 对点数据使用 IDW 插值法（InterpolationAlgorithmType.IDW）进行插值分析，得到栅格数据集（方法实现
    的中间结果，栅格值为单精度浮点型），接着从栅格数据集中提取等值面。

    点数据提取等值面介绍，参考 :py:meth:`points_extract_isoregion`

    :param extracted_points: 指定的待提取等值面的点串，该点串中的点是三维点，每一个点存储了 X，Y 坐标信息和只有一个第三维度的信息（例如：高程信息等）。
    :type extracted_points: list[Point3D]
    :param resolution: 指定的中间结果（栅格数据集）的分辨率
    :type resolution: float
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param terrain_interpolate_type: 指定的地形插值类型。
    :type terrain_interpolate_type: TerrainInterpolateType or str
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值面。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值面的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。
                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。
                       对于等值面的提取，采用先提取等值线然后生成等值面的方式，若将光滑度设置为2，
                       则中间结果数据集，即等值线对象的点数将为原始数据集点数的2倍，当光滑度设定值不断增大时，点数将成2的指数倍
                       增长，这将大大降低等值面提取的效率甚至可能导致提取失败。
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则直接返回等值面对象列表
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值面得到的数据集或数据集名称，或等值面对象列表
    :rtype: DatasetVector or str or list[GeoRegion]
    """
    check_lic()
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = 'isoregion'
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    else:
        out_datasource = None
        _outDatasetName = None
    if clip_region is not None:
        java_clip_region = oj(clip_region)
    else:
        java_clip_region = None
    java_point_3ds = to_java_point3ds(extracted_points)
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'point3ds_extract_isoregion')
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoRegion = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoregion
            if out_datasource is not None:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoRegionjava_paramjava_point_3dsoj(terrain_interpolate_type)oj(out_datasource)_outDatasetNamefloat(resolution)java_clip_region
                else:
                    java_result = extractIsoRegion(java_param, java_point_3ds, oj(out_datasource), _outDatasetName, float(resolution), java_clip_region)
            else:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoRegion(java_param, java_point_3ds, oj(terrain_interpolate_type), float(resolution), java_clip_region)
                else:
                    java_result = extractIsoRegionjava_paramjava_point_3dsfloat(resolution)java_clip_region
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


class BasicStatisticsAnalystResult:
    __doc__ = '\n    栅格基本统计分析结果类\n\n    '

    def __init__(self):
        self._first_quartile = None
        self._kurtosis = None
        self._max = None
        self._mean = None
        self._median = None
        self._min = None
        self._skewness = None
        self._std = None
        self._thd_quartile = None

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        obj = BasicStatisticsAnalystResult()
        obj._first_quartile = java_obj.getFirstQuartile()
        obj._kurtosis = java_obj.getKurtosis()
        obj._max = java_obj.getMax()
        obj._min = java_obj.getMin()
        obj._mean = java_obj.getMean()
        obj._median = java_obj.getMedian()
        obj._skewness = java_obj.getSkewness()
        obj._std = java_obj.getStandardDeviation()
        obj._thd_quartile = java_obj.getThirdQuartile()
        return obj

    def __str__(self):
        return '\n'.join(['Basic statistics analyst result: ',
         'first_quartile: ' + str(self.first_quartile),
         'kurtosis:       ' + str(self.kurtosis),
         'max:            ' + str(self.max),
         'min:            ' + str(self.min),
         'mean:           ' + str(self.mean),
         'median:         ' + str(self.median),
         'skewness:       ' + str(self.skewness),
         'std:            ' + str(self.std),
         'third_quartile: ' + str(self.third_quartile)])

    @property
    def first_quartile(self):
        """float: 栅格基本统计分析计算所得的第一四分值"""
        return self._first_quartile

    @property
    def kurtosis(self):
        """float: 栅格基本统计分析计算所得的峰度"""
        return self._kurtosis

    @property
    def max(self):
        """float: 栅格基本统计分析计算所得的最大值"""
        return self._max

    @property
    def min(self):
        """float: """
        return self._min

    @property
    def mean(self):
        """float: 栅格基本统计分析计算所得的最小值"""
        return self._mean

    @property
    def median(self):
        """float: 栅格基本统计分析计算所得的中位数"""
        return self._median

    @property
    def skewness(self):
        """float: 栅格基本统计分析计算所得的偏度"""
        return self._skewness

    @property
    def std(self):
        """float: 栅格基本统计分析计算所得的均方差（标准差）"""
        return self._std

    @property
    def third_quartile(self):
        """float: 栅格基本统计分析计算所得的第三四分值"""
        return self._thd_quartile

    def to_dict(self):
        """
        输出为 dict 对象

        :rtype: dict
        """
        return {'first_quartile':self.first_quartile, 
         'kurtosis':self.kurtosis, 
         'max':self.max, 
         'min':self.min, 
         'mean':self.mean, 
         'median':self.median, 
         'skewness':self.skewness, 
         'std':self.std, 
         'third_quartile':self.third_quartile}


def grid_basic_statistics(grid_data, function_type=None, progress=None):
    """
    栅格基本统计分析，可指定变换函数类型。用于对栅格数据集进行基本的统计分析，包括最大值、最小值、平均值和标准差等。

    指定变换函数时，用来统计的数据是原始栅格值经过函数变换后得到的值。

    :param grid_data: 待统计的栅格数据
    :type grid_data: DatasetGrid or str
    :param function_type: 变换函数类型
    :type function_type: FunctionType or str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 基本统计分析结果
    :rtype: BasicStatisticsAnalystResult
    """
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('extracted_point required DatasetGrid, but is ' + str(type(grid_data)))
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'grid_basic_statistics')
                    get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                basicStatistics = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.basicStatistics
                if function_type is not None:
                    function_type = FunctionType._make(function_type)
                    java_result = basicStatistics(oj(source_dt), oj(function_type))
                else:
                    java_result = basicStatistics(oj(source_dt))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return BasicStatisticsAnalystResult._from_java_object(java_result)


def grid_common_statistics(grid_data, compare_datasets_or_value, compare_type, is_ignore_no_value, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格常用统计分析，将一个栅格数据集逐行逐列按照某种比较方式与一个（或多个）栅格数据集，或一个固定值进行比较，比较结果为“真”的像元值为 1，为“假”的像元值为 0。

    关于无值的说明：

     * 当待统计源数据集的栅格有无值时，如果忽略无值，则统计结果栅格也为无值，否则使用该无值参与统计；当各比较数据集的栅格有无值时，
       如果忽略无值，则此次统计（待统计栅格与该比较数据集的计算）不计入结果，否则使用该无值进行比较。
     * 当无值不参与运算（即忽略无值）时，统计结果数据集中无值的值，由结果栅格的像素格式决定，为最大像元值，例如，结果栅格数据集像素
       格式为 PixelFormat.UBIT8，即每个像元使用 8 个比特表示，则无值的值为 255。在此方法中，结果栅格的像素格式是由比较栅格数据集
       的数量来决定的。比较数据集得个数、结果栅格的像素格式和结果栅格中无值的值三者的对应关系如下所示：

    .. image:: ../image/CommonStatistics.png

    :param grid_data:  指定的待统计的栅格数据。
    :type grid_data: DatasetGrid or str
    :param compare_datasets_or_value: 指定的比较的数据集集合或固定值。指定固定值时，固定值的单位与待统计的栅格数据集的栅格值单位相同。
    :type compare_datasets_or_value: list[DatasetGrid] or list[str] or float
    :param compare_type: 指定的比较类型
    :type compare_type: StatisticsCompareType or str
    :param is_ignore_no_value: 指定是否忽略无值。如果为 true，即忽略无值，则计算区域内的无值不参与计算，结果栅格值仍为无值；若为 false，则计算区域内的无值参与计算。
    :type is_ignore_no_value: bool
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 统计结果栅格数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('extracted_point required DatasetGrid, but is ' + str(type(grid_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_stats'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'grid_common_statistics')
                    get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                func_commonStatistics = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.commonStatistics
                compare_value = None
                if isinstance(compare_datasets_or_value, (float, int)):
                    compare_value = float(compare_datasets_or_value)
                else:
                    if isinstance(compare_datasets_or_value, DatasetGrid):
                        compare_value = [
                         compare_datasets_or_value]
                    else:
                        if isinstance(compare_datasets_or_value, str):
                            compare_value = []
                            for t in split_input_list_from_str(compare_datasets_or_value):
                                dt = get_input_dataset(t)
                                if isinstance(dt, DatasetGrid):
                                    compare_value.append(dt)

                        else:
                            if isinstance(compare_datasets_or_value, list):
                                compare_value = []
                                for t in compare_datasets_or_value:
                                    dt = get_input_dataset(t)
                                    if isinstance(dt, DatasetGrid):
                                        compare_value.append(dt)

            if compare_value is None:
                raise ValueError('have no valid compare value or compare dataset')
            if isinstance(compare_value, float):
                java_result = func_commonStatistics(oj(source_dt), compare_value, oj(StatisticsCompareType._make(compare_type)), bool(is_ignore_no_value), oj(out_datasource), _outDatasetName)
            else:
                java_dts = to_java_datasetgrid_array(compare_value)
                java_result = func_commonStatistics(oj(source_dt), java_dts, oj(StatisticsCompareType._make(compare_type)), bool(is_ignore_no_value), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def grid_neighbour_statistics(grid_data, neighbour_shape, is_ignore_no_value=True, grid_stat_mode='SUM', unit_type='CELL', out_data=None, out_dataset_name=None, progress=None):
    """
    栅格邻域统计分析。

    邻域统计分析，是对输入数据集中的每个像元的指定扩展区域中的像元进行统计，将运算结果作为像元的值。统计的方法包括：总和、
    最大值、最小值、众数、少数、中位数等，请参见 GridStatisticsMode 枚举类型。目前提供的邻域范围类型（请参见 NeighbourShapeType
    枚举类型）有：矩形、圆形、圆环和扇形。

    下图为邻域统计的原理示意，假设使用“总和”作为统计方法做矩形邻域统计，邻域大小为 3×3，那么对于图中位于第二行第三列的单元格，
    它的值则由以其为中心向周围扩散得到的一个 3×3 的矩形内所有像元值的和来决定。

    .. image:: ../image/NeighbourStatistics.png

    邻域统计的应用十分广泛。例如：

    * 对表示物种种类分布的栅格计算每个邻域内的生物种类（统计方法：种类），从而观察该地区的物种丰度；
    * 对坡度栅格统计邻域内的坡度差（统计方法：值域），从而评估该区域的地形起伏状况；
    
      .. image:: ../image/NeighbourStatistics_1.png

    * 邻域统计还用于图像处理，如统计邻域内的平均值（称为均值滤波）或中位数（称为中值滤波）可以达到平滑的效果，从而去除噪声或过多的细节，等等。

      .. image:: ../image/NeighbourStatistics_2.png

    :param grid_data: 指定的待统计的栅格数据。
    :type grid_data: DatasetGrid or str
    :param neighbour_shape: 邻域形状
    :type neighbour_shape: NeighbourShape
    :param is_ignore_no_value: 指定是否忽略无值。如果为 true，即忽略无值，则计算区域内的无值不参与计算，结果栅格值仍为无值；若为 false，则计算区域内的无值参与计算。
    :type is_ignore_no_value: bool
    :param grid_stat_mode: 邻域分析的统计方法
    :type grid_stat_mode: GridStatisticsMode or str
    :param unit_type: 邻域统计的单位类型
    :type unit_type: NeighbourUnitType or str
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 统计结果栅格数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('extracted_point required DatasetGrid, but is ' + str(type(grid_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_stats'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'grid_neighbour_statistics')
                    get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                neighbourStatistics = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.neighbourStatistics
                if neighbour_shape.shape_type is NeighbourShapeType.RECTANGLE:
                    java_param = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourStatisticsRectangleParameter()
                    java_param.setWidth(neighbour_shape.width)
                    java_param.setHeight(neighbour_shape.height)
                else:
                    if neighbour_shape.shape_type is NeighbourShapeType.ANNULUS:
                        java_param = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourStatisticsAnnulusParameter()
                        java_param.setInnerRadius(neighbour_shape.inner_radius)
                        java_param.setOuterRadius(neighbour_shape.outer_radius)
                    else:
                        if neighbour_shape.shape_type is NeighbourShapeType.CIRCLE:
                            java_param = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourStatisticsCircleParameter()
                            java_param.setRadius(neighbour_shape.radius)
                        else:
                            if neighbour_shape.shape_type is NeighbourShapeType.WEDGE:
                                java_param = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourStatisticsWedgeParameter()
                                java_param.setRadius(neighbour_shape.radius)
                                java_param.setStartAngle(neighbour_shape.start_angle)
                                java_param.setEndAngle(neighbour_shape.end_angle)
                            else:
                                raise ValueError('invalid shape type')
            java_param.setIgnoreNoValue(bool(is_ignore_no_value))
            java_param.setSourceDataset(oj(source_dt))
            java_param.setStatisticsMode(oj(GridStatisticsMode._make(grid_stat_mode)))
            java_param.setTargetDatasource(oj(out_datasource))
            java_param.setTargetDatasetName(_outDatasetName)
            java_param.setUnitType(oj(NeighbourUnitType._make(unit_type)))
            java_result = neighbourStatistics(java_param)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def altitude_statistics(point_data, grid_data, out_data=None, out_dataset_name=None):
    """
    高程统计，统计二维点数据集中每个点对应的栅格值，并生成一个三维点数据集，三维点对象的 Z 值即为被统计的栅格像素的高程值。

    :param point_data: 二维点数据集
    :type point_data: DatasetVector or str
    :param grid_data: 被统计的栅格数据集
    :type grid_data: DatasetGrid or str
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :return: 统计三维数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('grid_data required DatasetGrid, but is ' + str(type(grid_data)))
    else:
        point_dt = get_input_dataset(point_data)
        if isinstance(point_dt, DatasetVector):
            if point_dt.type is not DatasetType.POINT:
                raise ValueError('point_data required Point DatasetVector, but is ' + str(type(point_data)))
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
            else:
                out_datasource = point_dt.datasource
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + '_stats'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Utils.AltitudeStatistics(oj(point_dt), oj(grid_data), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def zonal_statistics_on_raster_value(value_data, zonal_data, zonal_field, is_ignore_no_value=True, grid_stat_mode='SUM', out_data=None, out_dataset_name=None, out_table_name=None, progress=None):
    """
    栅格分带统计，方法中值数据为栅格的数据集，带数据可以是矢量或栅格数据。

    栅格分带统计，是以某种统计方法对区域内的单元格的值进行统计，将每个区域内的统计值赋给该区域所覆盖的所有单元格，从而得到结果栅格。栅格分带统计涉及两种数据，值数据和带数据。值数据即被统计的栅格数据，带数据为标识统计区域的数据，可以为栅格或矢量面数据。下图为使用栅格带数据进行分带统计的算法示意，其中灰色单元格代表无值数据。

    .. image:: ../image/ZonalStatisticsOnRasterValue_1.png

    当带数据为栅格数据集时，连续的栅格值相同的单元格作为一个带（区域）；当带数据为矢量面数据集时，要求其属性表中有一个标识带的字段，以数值来区分不同的带，如果两个及以上的面对象（可以相邻，也可以不相邻）的标识值相同，则进行分带统计时，它们将作为一个带进行统计，即在结果栅格中，这些面对象对应位置的栅格值都是这些面对象范围内的所有单元格的栅格值的统计值。

    分带统计的结果包含两部分：一是分带统计结果栅格，每个带内的栅格值相同，即按照统计方法计算所得的值；二是一个记录了每个分带内统计信息的属性表，包含 ZONALID（带的标识）、PIXELCOUNT（带内单元格数）、MININUM（最小值）、MAXIMUM（最大值）、RANGE_VALUE（值域）、SUM_VALUE（和）、MEAN（平均值）、STD（标准差）、VARIETY（种类）、MAJORITY（众数）、MINORITY（少数）、MEDIAN（中位数）等字段。

    下面通过一个实例来了解分带统计的应用。

      1. 如下图所示，左图是 DEM 栅格值，将其作为值数据，右图为对应区域的行政区划，将其作为带数据，进行分带统计；

      .. image:: ../image/ZonalStatisticsOnRasterValue_2.png

      2. 使用上面的数据，将最大值作为统计方法，进行分带统计。结果包括如下图所示的结果栅格，以及对应的统计信息属性表（略）。结果栅格中，每个带内的栅格值均相等，即在该带范围内的值栅格中最大的栅格值，也就是高程值。该例统计了该地区每个行政区内最高的高程。

      .. image:: ../image/ZonalStatisticsOnRasterValue_3.png

    注意，分带统计的结果栅格的像素类型（PixelFormat）与指定的分带统计类型（通过 ZonalStatisticsAnalystParameter 类的 setStatisticsMode 方法设置）有关：

    \u3000*\u3000当统计类型为种类（VARIETY）时，结果栅格像素类型为 BIT32；
    \u3000*\u3000当统计类型为最大值（MAX）、最小值（MIN）、值域（RANGE）时，结果栅格的像素类型与源栅格保持一致；
    \u3000*\u3000当统计类型为平均值（MEAN）、标准差（STDEV）、总和（SUM）、众数（MAJORITY）、最少数（MINORITY）、中位数（MEDIAN）时，结果栅格的像素类型为 DOUBLE。

    :param value_data: 需要被统计的值数据
    :type value_data: DatasetGrid or str
    :param zonal_data: 待统计的分带数据集。仅支持像素格式（PixelFormat）为 UBIT1、UBIT4、UBIT8 和 UBIT16 的栅格数据集或矢量面数据集。
    :type zonal_data: DatasetGrid or DatasetVector or str
    :param str zonal_field: 矢量分带数据中用于标识带的字段。字段类型只支持32位整型。
    :param bool is_ignore_no_value: 统计时是否忽略无值数据。 如果为 True，表示无值栅格不参与运算；若为 False，表示有无值参与的运算，结果仍为无值
    :param grid_stat_mode: 分带统计类型
    :type grid_stat_mode:  GridStatisticsMode or str
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param out_table_name: 分析结果属性表的名称
    :type out_table_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个 tuple，tuple 有两个元素，第一个为结果数据集或名称，第二个为结果属性表数据集或名称
    :rtype: tuple[DatasetGrid, DatasetGrid] or tuple[str,str]
    """
    check_lic()
    source_dt = get_input_dataset(value_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('value_data required DatasetGrid, but is ' + str(type(value_data)))
    else:
        zonal_dt = get_input_dataset(zonal_data)
        if not isinstance(zonal_dt, (DatasetGrid, DatasetVector)):
            raise ValueError('zonal_data required DatasetGrid or DatasetVector, but is ' + str(type(zonal_data)))
        else:
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
            else:
                out_datasource = source_dt.datasource
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + '_zonal_stats'
            else:
                _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        if out_table_name is None:
            _outTableName = source_dt.name + '_zonal_tabular'
        else:
            _outTableName = out_table_name
    _outTableName = out_datasource.get_available_dataset_name(_outTableName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'zonal_statistics_on_raster_value')
                        get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            zonalStatisticsOnRasterValue = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.zonalStatisticsOnRasterValue
            java_param = get_jvm().com.supermap.analyst.spatialanalyst.ZonalStatisticsAnalystParameter()
            java_param.setIgnoreNoValue(bool(is_ignore_no_value))
            java_param.setValueDataset(oj(source_dt))
            java_param.setZonalDataset(oj(zonal_dt))
            java_param.setZonalFieldName(str(zonal_field))
            java_param.setStatisticsMode(oj(GridStatisticsMode._make(grid_stat_mode)))
            java_param.setTargetDatasource(oj(out_datasource))
            java_param.setTargetDatasetName(_outDatasetName)
            java_param.setTargetTableName(_outTableName)
            java_result = zonalStatisticsOnRasterValue(java_param)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return
        result_dt = out_datasource[_outDatasetName]
        result_table = out_datasource[_outTableName]
        if out_data is not None:
            return try_close_output_datasource((result_dt, result_table), out_datasource)
        return (result_dt, result_table)


class GridHistogram:
    __doc__ = '\n    创建给定栅格数据集的直方图。\n\n    直方图，又称柱状图，由一系列高度不等的矩形块来表示一份数据的分布情况。一般横轴表示类别，纵轴表示分布情况。\n\n    栅格直方图的横轴表示栅格值的分组，栅格值将被划分到这 N（默认为 100）个组中，即每个组对应着一个栅格值范围；纵轴表示频数，即\n    栅格值在每组的值范围内的单元格的个数。\n\n    下图是栅格直方图的示意图。该栅格数据的最小值和最大值分别为 0 和 100，取组数为 10，得出每组的频数，绘制如下的直方图。矩形块\n    上方标注了该组的频数，例如，第 6 组的栅格值范围为 [50,60)，栅格数据中值在此范围内的单元格共有 3 个，因此该组的频数为 3。\n\n    .. image:: ../image/BuildHistogram.png\n\n    注：直方图分组的最后一组的值范围为前闭后闭，其余均为前闭后开。\n\n    在通过此方法获得栅格数据集的直方图（GridHistogram）对象后，可以通过该对象的 get_frequencies 方法返回每个组的频数，还可以通过\n    get_group_count 方法重新指定栅格直方图的组数，然后再通过 get_frequencies 方法返回每组的频数。\n\n    下图为创建栅格直方图的一个实例。本例中，最小栅格值为 250，最大栅格值为 1243，组数为 500，获取各组的频数，绘制出如右侧所示的\n    栅格直方图。从右侧的栅格直方图，可以非常直观的了解栅格数据集栅格值的分布情况。\n\n    .. image:: ../image/BuildHistogram_1.png\n\n    '

    def __init__(self, source_data, group_count, function_type=None, progress=None):
        """
        构造栅格直方图对象

        :param source_data:  指定的栅格数据集
        :type source_data: DatasetGrid or str
        :param group_count:  指定的直方图的组数。必须大于 0。
        :type group_count: int
        :param function_type: FunctionType
        :type function_type: 指定的变换函数类型。
        :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
        :type progress: function
        """
        self._source_data = get_input_dataset(source_data)
        self._group_count = int(group_count)
        if function_type is not None:
            self._function_type = FunctionType._make(function_type)
        else:
            self._function_type = None
        self._progress = progress
        self._jobject = None

    def get_frequencies(self):
        """
        返回栅格直方图每个组的频数。直方图的每个组都对应了一个栅格值范围，值在这个范围内的所有单元格的个数即为该组的频数。

        :return:  返回栅格直方图每个组的频数。
        :rtype: list[int]
        """
        self._create_histogram()
        return self._jobject.getFrequencies()

    def get_group_count(self):
        """
        返回栅格直方图横轴上的组数。

        :return: 返回栅格直方图横轴上的组数。
        :rtype: int
        """
        self._create_histogram()
        return self._jobject.getGroupCount()

    def set_group_count(self, count):
        """
        设置栅格直方图横轴上的组数。

        :param int count: 栅格直方图横轴上的组数。必须大于 0。
        :rtype: self
        """
        self._jobject.setGroupCount(int(count))
        return self

    class HistogramSegmentInfo:
        __doc__ = '\n        栅格直方图每个分段区间的信息类。\n        '

        def __init__(self, count, max_value, min_value, range_max, range_min):
            self._count = count
            self._max = max_value
            self._min = min_value
            self._range_max = range_max
            self._range_min = range_min

        def __str__(self):
            s = []
            s.append('HistogramSegmentInfo:')
            s.append('count:           ' + str(self.count))
            s.append('max value:       ' + str(self.max))
            s.append('min value:       ' + str(self.min))
            s.append('range max value: ' + str(self.range_max))
            s.append('range min value: ' + str(self.range_min))
            return '\n'.join(s)

        @property
        def count(self):
            """int: 分段区间内容值的个数"""
            return self._count

        @property
        def max(self):
            """float: 分段区间内容值的最大值"""
            return self._max

        @property
        def min(self):
            """float: 分段区间内容值的最小值"""
            return self._min

        @property
        def range_max(self):
            """float: 分段区间的最大值"""
            return self._range_max

        @property
        def range_min(self):
            """float: 分段区间的最小值"""
            return self._range_min

    def get_segments(self):
        """
        返回栅格直方图每个组的区间信息。

        :return:  栅格直方图每个组的区间信息。
        :rtype: list[GridHistogram.HistogramSegmentInfo]
        """
        self._create_histogram()
        segments = self._jobject.getSegmentInfos()
        result = []
        for seg in segments:
            result.append(GridHistogram.HistogramSegmentInfo(seg.getCount(), seg.getMaxValue(), seg.getMinValue(), seg.getRangeMaxValue(), seg.getRangeMinValue()))

        del segments
        return result

    def _create_histogram(self):
        if self._jobject is not None:
            return self._jobject
        listener = None
        try:
            try:
                if self._progress is not None and safe_start_callback_server():
                    try:
                        listener = ProgressListener(self._progress, 'GridHistogram')
                        get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

                else:
                    createHistogram = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.createHistogram
                    if self._function_type is not None:
                        java_result = createHistogram(oj(self._source_data), int(self._group_count), oj(self._function_type))
                    else:
                        java_result = createHistogram(oj(self._source_data), int(self._group_count))
            except:
                import traceback
                log_error(traceback.format_exc())
                java_result = None

        finally:
            if listener is not None:
                try:
                    get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            self._jobject = java_result


def thin_raster(source, back_or_no_value, back_or_no_value_tolerance, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格细化，通常在将栅格转换为矢量线数据前使用。

    栅格数据细化处理可以减少栅格数据中用于标识线状地物的单元格的数量，从而提高矢量化的速度和精度。一般作为栅格转线矢量数据之
    前的预处理，使转换的效果更好。例如一幅扫描的等高线图上可能使用 5、6 个单元格来显示一条等高线的宽度，细化处理后，等高线的
    宽度就只用一个单元格来显示了，有利于更好地进行矢量化。

    .. image:: ../image/ThinRaster.png

    关于无值/背景色及其容限的说明：

    进行栅格细化时，允许用户标识那些不需要细化的单元格。对于栅格数据集，通过无值及其容限来确定这些值，对于影像数据集，则通过背景色及其容限来确定。

    * 当对栅格数据集进行细化时，栅格值为 back_or_no_value 参数指定的值的单元格被视为无值，不参与细化，而栅格的原无值将作为有效值来参与细化；
      同时，在 back_or_no_value_tolerance 参数指定的无值的容限范围内的单元格也不参与细化。例如，指定无值的值为 a，指定的无值的容限为 b，
      则栅格值在 [a-b,a+b] 范围内的单元格均不参与细化。

    * 当对影像数据集进行细化时，栅格值为指定的值的单元格被视为背景色，不参与细化；同时，在 back_or_no_value_tolerance 参数指
      定的背景色的容限范围内的单元格也不参与细化。

    需要注意，影像数据集中栅格值代表的是一个颜色值，因此，如果想要将某种颜色设为背景色，为 back_or_no_value 参数指定的值应为
    将该颜色（RGB 值）转为 32 位整型之后的值，系统内部会根据像素格式再进行相应的转换。背景色的容限同样为一个 32 位整型值。该
    值在系统内部被转为分别对应 R、G、B 的三个容限值，例如，指定为背景色的颜色为 (100,200,60)，指定的容限值为 329738，该值对应
    的 RGB 值为 (10,8,5)，则值在 (90,192,55) 和 (110,208,65) 之间的颜色均不参与细化。

    注意：对于栅格数据集，如果指定的无值的值，在待细化的栅格数据集的值域范围外，会分析失败，返回 None。

    :param source: 指定的待细化的栅格数据集。支持影像数据集。
    :type source: DatasetImage or DatasetGrid or str
    :param back_or_no_value: 指定栅格的背景色或表示无值的值。可以使用一个 int 或 tuple 来表示一个 RGB 或 RGBA 值。
    :type back_or_no_value: int or tuple
    :param back_or_no_value_tolerance: 栅格背景色的容限或无值的容限。可以使用一个 float 或 tuple 来表示一个 RGB 或 RGBA 值。
    :type back_or_no_value_tolerance: float or tuple
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: Dataset or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, (DatasetGrid, DatasetImage)):
        raise ValueError('source required DatasetGrid or DatasetImage, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_thin_raster'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    if back_or_no_value is not None:
        if isinstance(back_or_no_value, tuple):
            back_or_no_value = tuple_to_color(back_or_no_value)
    if back_or_no_value_tolerance is not None:
        if isinstance(back_or_no_value_tolerance, tuple):
            back_or_no_value_tolerance = tuple_to_color(back_or_no_value_tolerance)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'thin_raster')
                        get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            thinRaster = get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.thinRaster
            java_result = thinRaster(oj(source_dt), int(back_or_no_value), float(back_or_no_value_tolerance), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def thin_raster_bit(input_data, back_or_no_value, is_save_as_grid=True, out_data=None, out_dataset_name=None, progress=None):
    """
    通过减少要素宽度的像元来对栅格化的线状要素进行细化，该方法是处理二值图像的细化方法，如果不是二值图像会先处理为二值图像，只需指定背景色的值，背景色以外的值都是需要细化的值。该方法的效率最快。

    :param input_data: 指定的待细化的栅格数据集。支持影像数据集。
    :type input_data: DatasetImage or DatasetGrid or str
    :param back_or_no_value: 指定栅格的背景色或表示无值的值。可以使用一个 int 或 tuple 来表示一个 RGB 或 RGBA 值。
    :type back_or_no_value: int or tuple
    :param bool is_save_as_grid: 是否保存为栅格数据集，Ture 表示保存为栅格数据集，False保存为原数据类型（栅格或影像）。保存为栅格数据集便于栅格矢量化时指定值矢量化，方便快速获取线数据。
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: Dataset or str
    """
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, (DatasetGrid, DatasetImage)):
        raise ValueError('source required DatasetGrid or DatasetImage, but is ' + str(type(input_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_thin_raster'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    if back_or_no_value is not None:
        if isinstance(back_or_no_value, tuple):
            back_or_no_value = tuple_to_color(back_or_no_value)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'thin_raster_bit')
                        get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            thinRaster = get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.thinRaster
            java_result = thinRaster(oj(source_dt), oj(out_datasource), _outDatasetName, int(back_or_no_value), parse_bool(is_save_as_grid))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def build_lake(dem_grid, lake_data, elevation, progress=None):
    """
    挖湖，即修改面数据集区域范围内的 DEM 数据集的高程值为指定的数值。
    挖湖是指根据已有的湖泊面数据，在 DEM 数据集上显示湖泊信息。如下图所示，挖湖之后，DEM 在湖泊面数据对应位置的栅格值变成指定的高程值，且整个湖泊区域栅格值相同。

    .. image:: ../image/BuildLake.png

    :param dem_grid:  指定的待挖湖的 DEM 栅格数据集。
    :type dem_grid: DatasetGrid or str
    :param lake_data:  指定的湖区域，为面数据集。
    :type lake_data: DatasetVector or str
    :param elevation: 指定的湖区域的高程字段或指定的高程值。如果为 str，则要求字段类型为数值型。如果指定为 None 或空字符串，或湖区域数据集中不存在指定的
                      字段，则按照湖区域边界对应 DEM 栅格上的最小高程进行挖湖。高程值的单位与 DEM 栅格数据集的栅格值单位相同。
    :type elevation: str or float
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 成功返回 True，否则返回 False
    :rtype: bool
    """
    check_lic()
    source_dt = get_input_dataset(dem_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('dem_grid required DatasetGrid, but is ' + str(type(dem_grid)))
    lake_dt = get_input_dataset(lake_data)
    if not isinstance(lake_dt, DatasetVector):
        raise ValueError('lake_data required DatasetVector, but is ' + str(type(lake_dt)))
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'build_lake')
                    get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                buildLake = get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.buildLake
                if isinstance(elevation, (float, int)):
                    elevation = float(elevation)
                else:
                    elevation = str(elevation)
            java_result = buildLake(oj(source_dt), oj(lake_dt), elevation)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return java_result


def build_terrain(source_datas, lake_dataset=None, lake_altitude_field=None, clip_data=None, erase_data=None, interpolate_type='IDW', resample_len=0.0, z_factor=1.0, is_process_flat_area=False, encode_type='NONE', pixel_format='SINGLE', cell_size=0.0, out_data=None, out_dataset_name=None, progress=None):
    """
    根据指定的地形构建参数信息创建地形。
    DEM（Digital Elevation Model，数字高程模型）主要用于描述区域地貌形态的空间分布，是地面特性为高程和海拔高程的数字地面模型（DTM），
    通常通过高程测量点（或从等高线中进行采样提取高程点）进行数据内插而成。此方法用于构建地形，即对具有高程信息的点或线数据集通过插值生成 DEM 栅格。

    .. image:: ../image/BuildTerrain_1.png

    可以通过 source_datas 参数指定用于构建地形的数据集，支持仅高程点、仅等高线以及支持高程点和等高线共同构建。

    :param source_datas: 用于构建的点数据集和线数据集，以及数据集的高程字段。要求数据集的坐标系相同。
    :type source_datas: dict[DatasetVector,str] or dict[str,str]
    :param lake_dataset:  湖泊面数据集。在结果数据集中，湖泊面数据集区域范围内的高程值小于周边相邻的高程值。
    :type lake_dataset: DatasetVector or str
    :param str lake_altitude_field: 湖泊面数据集的高程字段
    :param clip_data: 设置用于裁剪的数据集。构建地形时，仅位于裁剪区域内的 DEM 结果被保留，区域外的部分被赋予无值。

                      .. image:: ../image/BuildTerrainParameter_1.png

    :type clip_data: DatasetVector or str
    :param erase_data: 用于擦除的数据集。构建地形时，位于擦除区域内的结果 DEM 栅格值为无值。仅在 interpolate_type 设置为 TIN 时有效。

                       .. image:: ../image/BuildTerrainParameter_2.png

    :type erase_data: DatasetVector or str
    :param interpolate_type: 地形插值类型。默认值为 IDW。
    :type interpolate_type: TerrainInterpolateType  or str
    :param float resample_len: 采样距离。只对线数据集有效。单位与用于构建地形的线数据集单位一致。仅在 interpolate_type 设置为TIN时有效。
                         首先对线数据集进行重采样过滤掉一些比较密集的节点，然后再生成 TIN 模型，提高生成速度。
    :param float z_factor: 高程缩放系数
    :param bool is_process_flat_area: 是否处理平坦区域。等值线生成DEM能较好地处理山顶山谷，点生成DEM也可以处理平坦区域，但效
                                      果没有等值线生成DEM处理的好，主要原因是根据点判断平坦区域结果较为粗糙。
    :param encode_type: 编码方式。对于栅格数据集，目前支持的编码方式有未编码、SGL、LZW 三种方式
    :type encode_type: EncodeType or str
    :param pixel_format: 结果数据集的像素格式
    :type pixel_format: PixelFormat or str
    :param float cell_size: 结果数据集的栅格单元的大小，如果指定为 0 或负数，则系统会使用 L/500（L 是指源数据集的区域范围对应的矩形的对角线长度）作为单元格大小。
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: Dataset or str
    """
    check_lic()
    point_datasets = []
    point_altitude_fields = []
    line_datasets = []
    line_altitude_fields = []
    if isinstance(source_datas, dict):
        for dt, field in source_datas.items():
            dt = get_input_dataset(dt)
            if isinstance(dt, DatasetVector) and dt.index_of_field(field) != -1:
                if dt.type is DatasetType.POINT:
                    point_datasets.append(dt)
                    point_altitude_fields.append(field)
                elif dt.type is DatasetType.LINE:
                    line_datasets.append(dt)
                    line_altitude_fields.append(field)

    if len(point_datasets) + len(line_datasets) == 0:
        raise ValueError('have no valid source  datasets')
    elif lake_dataset is not None:
        if lake_altitude_field is not None:
            lake_dataset = get_input_dataset(lake_dataset)
            lake_altitude_field = str(lake_altitude_field)
        else:
            lake_dataset = None
            lake_altitude_field = None
        clip_data = get_input_dataset(clip_data)
        if clip_data is not None:
            java_clip_data = oj(clip_data)
        else:
            java_clip_data = None
        erase_data = get_input_dataset(erase_data)
        if erase_data is not None:
            java_erase_data = oj(erase_data)
        else:
            java_erase_data = None
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            if len(point_datasets) > 0:
                out_datasource = point_datasets[0].datasource
            else:
                out_datasource = line_datasets[0].datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            if len(point_datasets) > 0:
                _outDatasetName = point_datasets[0].name + '_terrain'
        else:
            _outDatasetName = line_datasets[0].name + '_terrain'
    else:
        _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'build_terrain')
                        get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilderParameter()
            if len(point_datasets) > 0:
                java_param.setPointDatasets(to_java_datasetvector_array(point_datasets))
                java_param.setPointAltitudeFileds(to_java_string_array(point_altitude_fields))
            else:
                java_param.setLineDatasets(to_java_datasetvector_array(line_datasets))
                java_param.setLineAltitudeFileds(to_java_string_array(line_altitude_fields))
            if lake_dataset is not None:
                java_param.setLakeDataset(oj(lake_dataset))
                java_param.setLakeAltitudeFiled(lake_altitude_field)
            if cell_size is not None:
                java_param.setCellSize(float(cell_size))
            if java_clip_data is not None:
                java_param.setClipDataset(java_clip_data)
            if encode_type is not None:
                java_param.setEncodeType(oj(EncodeType._make(encode_type)))
            if java_erase_data is not None:
                java_param.setEraseDataset(java_erase_data)
            if interpolate_type is not None:
                java_param.setInterpolateType(oj(TerrainInterpolateType._make(interpolate_type)))
            if pixel_format is not None:
                java_param.setPixelFormat(oj(PixelFormat._make(pixel_format)))
            if is_process_flat_area is not None:
                java_param.setProcessFlatArea(parse_bool(is_process_flat_area))
            if resample_len is not None:
                java_param.setResampleLen(float(resample_len))
            if z_factor is not None:
                java_param.setZFactor(float(z_factor))
            java_result = get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.buildTerrain(java_param, oj(out_datasource), _outDatasetName)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def area_solar_radiation_days(grid_data, latitude, start_day, end_day=160, hour_start=0, hour_end=24, day_interval=5, hour_interval=0.5, transmittance=0.5, z_factor=1.0, out_data=None, out_total_grid_name='TotalGrid', out_direct_grid_name=None, out_diffuse_grid_name=None, out_duration_grid_name=None, progress=None):
    """
    计算多天的区域太阳辐射总量，即整个DEM范围内每个栅格的太阳辐射情况。需要指定每天的开始时点、结束时点和开始日期、结束日期。

    :param grid_data: 待计算太阳辐射的DEM栅格数据
    :type grid_data: DatasetGrid or str
    :param latitude: 待计算区域的平均纬度
    :type latitude: float
    :param start_day: 起始日期，可以是 "%Y-%m-%d" 格式的字符串，如果为 int，则表示一年中的第几天
    :type start_day: datetime.date or str or int
    :param end_day: 终止日期，可以是 "%Y-%m-%d" 格式的字符串，如果为 int，则表示一年中的第几天
    :type end_day: datetime.date or str or int
    :param hour_start: 起始时点，如果输入float 时，可以输入一个 [0,24]范围内的数值，表示一天中的第几个小时。也可以输入一个 datetime.datatime 或 "%H:%M:%S" 格式的字符串
    :type hour_start: float or str or datetime.datetime
    :param hour_end: 终止时点，如果输入float 时，可以输入一个 [0,24]范围内的数值，表示一天中的第几个小时。也可以输入一个 datetime.datatime 或 "%H:%M:%S" 格式的字符串
    :type hour_end:  float or str or datetime.datetime
    :param int day_interval: 天数间隔，单位为天
    :param float hour_interval: 小时间隔，单位为小时。
    :param float transmittance: 太阳辐射穿过大气的透射率，值域为[0,1]。
    :param float z_factor: 高程缩放系数
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_total_grid_name: 总辐射量结果数据集名称，数据集名称必须合法
    :param str out_direct_grid_name: 直射辐射量结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param str out_diffuse_grid_name: 散射辐射量结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param str out_duration_grid_name: 太阳直射持续时间结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个四个元素的 tuple：

               * 第一个为总辐射量结果数据集，
               * 如果设置了直射辐射量结果数据集名称，第二个为直射辐射量结果数据集，否则为 None，
               * 如果设置散射辐射量结果数据集的名称，第三个为散射辐射量结果数据集，否则为 None
               * 如果设置太阳直射持续时间结果数据集的名称，第四个为太阳直射持续时间结果数据集，否则为 None

    :rtype: tuple[DatasetGrid] or tuple[str]
    """
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('grid_data required DatasetGrid, but is ' + str(type(grid_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_total_grid_name is None:
            _out_total_grid_name = source_dt.name + '_solar'
        else:
            _out_total_grid_name = out_total_grid_name
    _out_total_grid_name = out_datasource.get_available_dataset_name(_out_total_grid_name)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'area_solar_radiation_days')
                        get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiationParameter()
            n_start_day = 0
            if start_day is not None:
                if isinstance(start_day, int):
                    n_start_day = start_day
                else:
                    start_day = get_struct_time(start_day)
                    if start_day is not None:
                        n_start_day = start_day.tm_yday
                    n_end_day = 0
                if end_day is not None:
                    if isinstance(end_day, int):
                        n_end_day = end_day
            else:
                end_day = get_struct_time(end_day)
            if end_day is not None:
                n_end_day = end_day.tm_yday
            java_param.setTimeMode(get_jvm().com.supermap.analyst.spatialanalyst.SolarTimeMode.MULTIDAYS)
            java_param.setDayStart(n_start_day)
            java_param.setDayEnd(n_end_day)
            if hour_start is not None:
                java_param.setHourStart(get_day_hour(hour_start))
            if hour_end is not None:
                java_param.setHourEnd(get_day_hour(hour_end))
            java_param.setLatitude(float(latitude))
            java_param.setTransmittance(float(transmittance))
            if z_factor is not None:
                java_param.setZFactor(float(z_factor))
            java_param.setDayInterval(int(day_interval))
            java_param.setHourInterval(float(hour_interval))
            areaSolarRadiation = get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.areaSolarRadiation
            java_result = areaSolarRadiationoj(source_dt)java_paramoj(out_datasource)_out_total_grid_nameout_direct_grid_nameout_diffuse_grid_nameout_duration_grid_name
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is None:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            else:
                return
                total_grid_dt = out_datasource[_out_total_grid_name]
                if out_direct_grid_name is not None:
                    direct_grid_dt = out_datasource[out_direct_grid_name]
                else:
                    direct_grid_dt = None
                if out_diffuse_grid_name is not None:
                    diffuse_grid_dt = out_datasource[out_diffuse_grid_name]
                else:
                    diffuse_grid_dt = None
            if out_duration_grid_name is not None:
                duration_grid_dt = out_datasource[out_duration_grid_name]
        else:
            duration_grid_dt = None
        if out_data is not None:
            return try_close_output_datasource((total_grid_dt, direct_grid_dt, diffuse_grid_dt, duration_grid_dt), out_datasource)
        return (
         total_grid_dt, direct_grid_dt, diffuse_grid_dt, duration_grid_dt)


def area_solar_radiation_hours(grid_data, latitude, day, hour_start=0, hour_end=24, hour_interval=0.5, transmittance=0.5, z_factor=1.0, out_data=None, out_total_grid_name='TotalGrid', out_direct_grid_name=None, out_diffuse_grid_name=None, out_duration_grid_name=None, progress=None):
    """
    计算一天内的太阳辐射，需要指定开始时点、结束时点及开始日期作为要计算的日期

    :param grid_data: 待计算太阳辐射的DEM栅格数据
    :type grid_data: DatasetGrid or str
    :param latitude: 待计算区域的平均纬度
    :type latitude: float
    :param day: 待计算的指定日期。可以是 "%Y-%m-%d" 格式的字符串，如果为 int，则表示一年中的第几天。
    :type day:  datetime.date or str or int
    :param hour_start: 起始时点，如果输入float 时，可以输入一个 [0,24]范围内的数值，表示一天中的第几个小时。也可以输入一个 datetime.datatime 或 "%H:%M:%S" 格式的字符串
    :type hour_start: float or str or datetime.datetime
    :param hour_end: 终止时点，如果输入float 时，可以输入一个 [0,24]范围内的数值，表示一天中的第几个小时。也可以输入一个 datetime.datatime 或 "%H:%M:%S" 格式的字符串
    :type hour_end:  float or str or datetime.datetime
    :param float hour_interval: 小时间隔，单位为小时。
    :param float transmittance: 太阳辐射穿过大气的透射率，值域为[0,1]。
    :param float z_factor: 高程缩放系数
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_total_grid_name: 总辐射量结果数据集名称，数据集名称必须合法
    :param str out_direct_grid_name: 直射辐射量结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param str out_diffuse_grid_name: 散射辐射量结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param str out_duration_grid_name: 太阳直射持续时间结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个四个元素的 tuple：

               * 第一个为总辐射量结果数据集，
               * 如果设置了直射辐射量结果数据集名称，第二个为直射辐射量结果数据集，否则为 None，
               * 如果设置散射辐射量结果数据集的名称，第三个为散射辐射量结果数据集，否则为 None
               * 如果设置太阳直射持续时间结果数据集的名称，第四个为太阳直射持续时间结果数据集，否则为 None

    :rtype: tuple[DatasetGrid] or tuple[str]
    """
    check_lic()
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('grid_data required DatasetGrid, but is ' + str(type(grid_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_total_grid_name is None:
            _out_total_grid_name = source_dt.name + '_solar'
        else:
            _out_total_grid_name = out_total_grid_name
    _out_total_grid_name = out_datasource.get_available_dataset_name(_out_total_grid_name)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'area_solar_radiation_hours')
                    get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

                java_param = get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiationParameter()
                n_start_day = 0
                if day is not None:
                    if isinstance(day, int):
                        n_start_day = day
            else:
                start_day = get_struct_time(day)
            if start_day is not None:
                n_start_day = start_day.tm_yday
            java_param.setTimeMode(get_jvm().com.supermap.analyst.spatialanalyst.SolarTimeMode.WITHINDAY)
            java_param.setDayStart(n_start_day)
            if hour_start is not None:
                java_param.setHourStart(get_day_hour(hour_start))
            if hour_end is not None:
                java_param.setHourEnd(get_day_hour(hour_end))
            java_param.setLatitude(float(latitude))
            java_param.setTransmittance(float(transmittance))
            if z_factor is not None:
                java_param.setZFactor(float(z_factor))
            java_param.setHourInterval(float(hour_interval))
            areaSolarRadiation = get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.areaSolarRadiation
            java_result = areaSolarRadiationoj(source_dt)java_paramoj(out_datasource)_out_total_grid_nameout_direct_grid_nameout_diffuse_grid_nameout_duration_grid_name
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is None:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            else:
                return
                total_grid_dt = out_datasource[_out_total_grid_name]
                if out_direct_grid_name is not None:
                    direct_grid_dt = out_datasource[out_direct_grid_name]
                else:
                    direct_grid_dt = None
                if out_diffuse_grid_name is not None:
                    diffuse_grid_dt = out_datasource[out_diffuse_grid_name]
                else:
                    diffuse_grid_dt = None
            if out_duration_grid_name is not None:
                duration_grid_dt = out_datasource[out_duration_grid_name]
        else:
            duration_grid_dt = None
        if out_data is not None:
            return try_close_output_datasource((total_grid_dt, direct_grid_dt, diffuse_grid_dt, duration_grid_dt), out_datasource)
        return (
         total_grid_dt, direct_grid_dt, diffuse_grid_dt, duration_grid_dt)


def basin(direction_grid, out_data=None, out_dataset_name=None, progress=None):
    """
    关于水文分析：

    * 水文分析基于数字高程模型（DEM）栅格数据建立水系模型，用于研究流域水文特征和模拟地表水文过程，并对未来的地表水文情况做出预估。水文分析模型能够帮助我们分析洪水的范围，定位径流污染源，预测地貌改变对径流的影响等，广泛应用于区域规划、农林、灾害预测、道路设计等诸多行业和领域。

    * 地表水的汇流情况很大程度上决定于地表形状，而 DEM 数据能够表达区域地貌形态的空间分布，在描述流域地形，如流域边界、坡度和坡向、河网提取等方面具有突出优势，因而非常适用于水文分析。

    * SuperMap 提供的水文分析主要内容有填充洼地、计算流向、计算流长、计算累积汇水量、流域划分、河流分级、连接水系及水系矢量化等。

        * 水文分析的一般流程为：

          .. image:: ../image/HydrologyAnalyst_2.png

        * 如何获得栅格水系？

          水文分析中很多功能都需要基于栅格水系数据，如提取矢量水系（:py:func:`stream_to_line` 方法）、河流分级（:py:func:`stream_order` 方法）、
          连接水系（::py:func:`stream_link` 方法）等。

          通常，可以从累积汇水量栅格中提取栅格水系数据。在累积汇水量栅格中，单元格的值越大，代表该区域的累积汇水量越大。累积汇水量
          较高的单元格可视为河谷，因此，可以通过设定一个阈值，提取累积汇水量大于该值的单元格，这些单元格就构成栅格水系。值得说明的
          是，对于不同级别的河谷、不同区域的相同级别的河谷，该值可能不同，因此该阈值的确定需要依据研究区域的实际地形地貌并通过不断的试验来确定。

          在 SuperMap 中，要求用于进一步分析（提取矢量水系、河流分级、连接水系等）的栅格水系为一个二值栅格，这可以通过栅格代数运算
          来实现，使大于或等于累积汇水量阈值的单元格为 1，否则为 0，如下图所示。

          .. image:: ../image/HydrologyAnalyst_3.png

          因此，提取栅格水系的过程如下：

           1. 获得累积汇水量栅格，可通过 :py:func:`flow_accumulation` 方法实现。
           2. 通过栅格代数运算 :py:func:`expression_math_analyst` 方法对累积汇水量栅格进行关系运算，就可以得到满足要求的栅格水系数据。假设设定
              阈值为 1000，则运算表达式为："[Datasource.FlowAccumulationDataset]>1000"。除此，使用 Con(x,y,z) 函数也可以得到想
              要的结果，即表达式为："Con([Datasource.FlowAccumulationDataset]>1000,1,0)"。

    根据流向栅格计算流域盆地。流域盆地即为集水区域，是用于描述流域的方式之一。

    计算流域盆地是依据流向数据为每个单元格分配唯一盆地的过程，如下图所示，流域盆地是描述流域的方式之一，展现了那些所有相互连接且处于同一流域盆地的栅格。

    .. image:: ../image/Basin.png

    :param direction_grid: 流向栅格数据集。
    :type direction_grid: DatasetGrid or str
    :param out_data: 存储结果数据集的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 流域盆地栅格数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(direction_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError('source required DatasetGrid, but is ' + str(type(direction_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_basin'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'basin')
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            func_basin = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.basin
            java_result = func_basin(oj(source_dt), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def build_quad_mesh(quad_mesh_region, left_bottom, left_top, right_bottom, right_top, cols=0, rows=0, out_col_field=None, out_row_field=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对单个简单面对象进行网格剖分。
    流体问题是一个连续性的问题，为了简化对其的研究以及建模处理的方便，对研究区域进行离散化处理，其思路就是建立离散的网格，网格划分就是对连续的物理区域进行剖分，把它分成若干个网格，并确定各个网格中的节点，用网格内的一个值来代替整个网格区域的基本情况，网格作为计算与分析的载体，其质量的好坏对后期的数值模拟的精度和计算效率有重要的影响。

    网格剖分的步骤：

     1．数据预处理，包含去除重复点等。给定一个合理的容限，去除重复点，使得最后的网格划分结果更趋合理，不会出现看起来从1个点
       （实际是重复点）出发有多条线的现象。

     2．多边形分解：对于复杂的多边形区域，我们采用分块逐步划分的方法来进行网格的构建，将一个复杂的不规则多边形区域划分为多个简
        单的单连通区域，然后对每个单连通区域执行网格划分程序，最后再将各个子区域网格拼接起来构成对整个区域的划分。

     3．选择四个角点：这4个角点对应着网格划分的计算区域上的4个顶点，其选择会对划分的结果造成影响。其选择应尽量在原区域近似四边
        形的四个顶点上，同时要考虑整体的流势。

        .. image:: ../image/SelectPoint.png

     4．为了使划分的网格呈现四边形的特征，构成多边形的顶点数据（不在同一直线上）需参与构网。

     5．进行简单区域网格划分。

    注：简单多边形：多边形内任何直线或边都不会交叉。

        .. image:: ../image/QuadMeshPart.png

    说明：

     RightTopIndex 为右上角点索引号，LeftTopIndex 为左上角点索引号，RightBottomIndex 为右下角点索引号，LeftBottomIndex
     为左下角点索引号。则 nCount1=（RightTopIndex- LeftTopIndex+1）和 nCount2=（RightBottomIndex- LeftBottomIndex+1），
     如果：nCount1不等于nCount2，则程序不处理。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param quad_mesh_region: 网格剖分的面对象
    :type quad_mesh_region: GeoRegion
    :param Point2D left_bottom: 网格剖分的区域多边形左下角点坐标。四个角点选择依据：4个角点对应着网格剖分的计算区域上的4个顶点，
                                其选择会对剖分的结果造成影响。其选择应尽量在原区域近似四边形的四个顶点上，同时要考虑整体的流势。
    :param Point2D left_top: 网格剖分的区域多边形左上角点坐标
    :param Point2D right_bottom: 网格剖分的区域多边形右下角点坐标
    :param Point2D right_top: 网格剖分的区域多边形右上角点坐标
    :param int cols: 网格剖分的列方向节点数。默认值为0，表示不参与处理；若不为0，但是此值若小于多边形列方向的最大点数减一，则
                     以多边形列方向的最大点数减一作为列数（cols）；若大于多边形列方向的最大点数减一，则会自动加点，使列方
                     向的数目为 cols。
                     举例来讲：如果用户希望将一矩形面对象划分为2*3（高*宽）=6个小矩形，则列方向数目（cols）为3。
    :param int rows: 网格剖分的行方向节点数。默认值为0，表示不参与处理；若不为0，但是此值小于多边形行方向的最大点数减一，则以
                     多边形行方向的最大点数减一作为行数（rows）；若大于多边形行方向的最大点数减一，则会自动加点，使行方向的
                     数目为 rows。举例来讲：如果用户希望将一矩形面对象划分为2*3（高*宽）=6个小矩形，则行方向数目（rows）为2。
    :param str out_col_field: 格网剖分结果对象的列属性字段名称。此字段用来保存剖分结果对象的列号。
    :param str out_row_field: 格网剖分结果对象的行属性字段名称。此字段用来保存剖分结果对象的行号。
    :param out_data: 存放剖分结果数据集的数据源。
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 剖分结果数据集的名称。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 剖分后的结果数据集，剖分出的多个面以子对象形式返回。
    :rtype: DatasetVector or str
    """
    check_lic()
    if not isinstance(quad_mesh_region, GeoRegion):
        raise ValueError('quad_mesh_region required GeoRegion, but now is ' + str(type(quad_mesh_region)))
    elif out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = 'quadmesh'
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    else:
        out_datasource = None
        _outDatasetName = None
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'build_quad_mesh')
                    get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                java_param = get_jvm().com.supermap.analyst.terrainanalyst.QuadMeshParameter()
                java_param.setQuadMeshRegion(oj(quad_mesh_region))
                java_param.setLeftBottomPoint(oj(Point2D.make(left_bottom)))
                java_param.setLeftTopPoint(oj(Point2D.make(left_top)))
                java_param.setRightBottomPoint(oj(Point2D.make(right_bottom)))
                java_param.setRightTopPoint(oj(Point2D.make(right_top)))
                java_param.setColCount(int(cols))
                java_param.setRowCount(int(rows))
                if out_col_field is not None:
                    java_param.setColField(str(out_col_field))
                if out_row_field is not None:
                    java_param.setRowField(str(out_row_field))
                buildQuadMesh = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.buildQuadMesh
                if out_datasource is None:
                    java_result = buildQuadMesh(java_param)
                else:
                    java_result = buildQuadMesh(java_param, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is None:
            return list((Geometry._from_java_object(geo) for geo in java_result))
        return try_close_output_datasource(out_datasource[_outDatasetName], out_datasource)


def fill_sink(surface_grid, exclude_area=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对 DEM 栅格数据填充伪洼地。
    洼地是指周围栅格都比其高的区域，分为自然洼地和伪洼地。

    \u3000* 自然洼地，是实际存在的洼地，是地表真实形态的反映，如冰川或喀斯特地貌、采矿区、坑洞等，一般远少于伪洼地；
    \u3000* 伪洼地，主要是由数据处理造成的误差、不合适的插值方法导致，在 DEM 栅格数据中很常见。

    在确定流向时，由于洼地高程低于周围栅格的高程，一定区域内的流向都将指向洼地，导致水流在洼地聚集不能流出，引起汇水网络的中断，
    因此，填充洼地通常是进行合理流向计算的前提。

    在填充某处洼地后，有可能产生新的洼地，因此，填充洼地是一个不断重复识别洼地、填充洼地的过程，直至所有洼地被填充且不再产生新
    的洼地。下图为填充洼地的剖面示意图。

    .. image:: ../image/FillSink.png

    该方法可以指定一个点或面数据集，用于指示的真实洼地或需排除的洼地，这些洼地不会被填充。使用准确的该类数据，将获得更为真实的
    无伪洼地地形，使后续分析更为可靠。

    用于指示洼地的数据，如果是点数据集，其中的一个或多个点位于洼地内即可，最理想的情形是点指示该洼地区域的汇水点；如果是面数据
    集，每个面对象应覆盖一个洼地区域。

    可以通过 exclude_area 参数，指定一个点或面数据集，用于指示的真实洼地或需排除的洼地，这些洼地不会被填充。使用准确的该类数据，
    将获得更为真实的无伪洼地地形，使后续分析更为可靠。用于指示洼地的数据，如果是点数据集，其中的一个或多个点位于洼地内即可，最
    理想的情形是点指示该洼地区域的汇水点；如果是面数据集，每个面对象应覆盖一个洼地区域。

    如果 exclude_area 为 None，则会将 DEM 栅格中所有洼地填充，包括伪洼地和真实洼地

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param surface_grid: 指定的要进行填充洼地的 DEM 数据
    :type surface_grid: DatasetGrid or str
    :param exclude_area: 指定的用于指示已知自然洼地或要排除的洼地的点或面数据。如果是点数据集，一个或多个点所在的区域指示为洼地；
                         如果是面数据集，每个面对象对应一个洼地区域。如果为 None，则会将 DEM 栅格中所有洼地填充，包括伪洼地和真实洼地
    :type exclude_area: DatasetVector or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集的名称。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 无伪洼地的 DEM 栅格数据集或数据集名称。如果填充伪洼地失败，则返回 None。
    :rtype: DatasetVector or str
    """
    check_lic()
    surface_dt = get_input_dataset(surface_grid)
    if not isinstance(surface_dt, DatasetGrid):
        raise ValueError('source required DatasetGrid, but is ' + str(type(surface_grid)))
    else:
        if exclude_area is not None:
            exclude_dt = get_input_dataset(exclude_area)
        else:
            exclude_dt = None
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = surface_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = surface_dt.name + '_sink'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'fill_sink')
                    get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                fillSink = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.fillSink
                if exclude_dt is not None:
                    java_result = fillSink(oj(surface_dt), oj(out_datasource), _outDatasetName)
                else:
                    java_result = fillSinkoj(surface_dt)oj(out_datasource)_outDatasetNameexclude_dt
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def flow_accumulation(direction_grid, weight_grid=None, out_data=None, out_dataset_name=None, progress=None):
    """
    根据流向栅格计算累积汇水量。可应用权重数据集计算加权累积汇水量。
    累积汇水量是指流向某个单元格的所有上游单元格的水流累积量，是基于流向数据计算得出的。

    累积汇水量的值可以帮助我们识别河谷和分水岭。单元格的累积汇水量较高，说明该地地势较低，可视为河谷；为0说明该地地势较高，可能为分水岭。因此，累积汇水量是提取流域的各种特征参数（如流域面积、周长、排水密度等）的基础。

    计算累积汇水量的基本思路是：假定栅格数据中的每个单元格处有一个单位的水量，依据水流方向图顺次计算每个单元格所能累积到的水量（不包括当前单元格的水量）。

    下图显示了由水流方向计算累积汇水量的过程。

    .. image:: ../image/FlowAccumulation_1.png

    下图为流向栅格和基于其生成的累积汇水量栅格。

    .. image:: ../image/FlowAccumulation_2.png

    在实际应用中，每个单元格的水量不一定相同，往往需要指定权重数据来获取符合需求的累积汇水量。使用了权重数据后，累积汇水量的计算过程中，每个单元格的水量不再是一个单位，而是乘以权重（权重数据集的栅格值）后的值。例如，将某时期的平均降雨量作为权重数据，计算所得的累积汇水量就是该时期的流经每个单元格的雨量。

    注意，权重栅格必须与流向栅格具有相同的范围和分辨率。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param direction_grid: 流向栅格数据。
    :type direction_grid: DatasetGrid or str
    :param weight_grid: 权重栅格数据。设置为 None 表示不使用权重数据集。
    :type weight_grid: DatasetGrid or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集的名称。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 累积汇水量栅格数据集或数据集名称。如果计算失败，则返回 None。
    :rtype: DatasetVector or str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError('direction_grid required DatasetGrid, but is ' + str(type(direction_grid)))
    elif weight_grid is not None:
        weight_dt = get_input_dataset(weight_grid)
        if not isinstance(weight_dt, DatasetGrid):
            raise ValueError('weight_grid required DatasetGrid, but is ' + str(type(weight_grid)))
        else:
            weight_dt = None
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + '_accum'
    else:
        _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'flow_accumulation')
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            flowAccumulation = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.flowAccumulation
            java_result = flowAccumulationoj(direction_dt)oj(weight_dt)oj(out_datasource)_outDatasetName
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def flow_direction(surface_grid, force_flow_at_edge, out_data=None, out_dataset_name=None, out_drop_grid_name=None, progress=None):
    """
    对 DEM 栅格数据计算流向。为保证流向计算的正确性，建议使用填充伪洼地之后的 DEM 栅格数据。

    流向，即水文表面水流的方向。计算流向是水文分析的关键步骤之一。水文分析的很多功能需要基于流向栅格，如计算累积汇水量、计算流
    长和流域等。

    SuperMap 使用最大坡降法（D8，Deterministic Eight-node）计算流向。这种方法通过计算单元格的最陡下降方向作为水流的方向。中心
    单元格与相邻单元格的高程差与距离的比值称为高程梯度。最陡下降方向即为中心单元格与高程梯度最大的单元格所构成的方向，也就是中
    心栅格的流向。单元格的流向的值，是通过对其周围的8个邻域栅格进行编码来确定的。如下图所示，若中心单元格的水流方向是左边，则其
    水流方向被赋值16；若流向右边，则赋值1。

    在 SuperMap 中，通过对中心栅格的 8 个邻域栅格编码（如下图所示），中心栅格的水流方向便可由其中的某一值来确定。例如，若中心
    栅格的水流方向是左边，则其水流方向被赋值 16；若流向右边，则赋值 1。

    .. image:: ../image/FlowDirection_1.png

    计算流向时，需要注意栅格边界单元格的处理。位于栅格边界的单元格比较特殊，通过 forceFlowAtEdge 参数可以指定其流向是否向外，
    如果向外，则边界栅格的流向值如下图（左）所示，否则，位于边界上的单元格将赋为无值，如下图（右）所示。

    .. image:: ../image/FlowDirection_2.png

    计算 DEM 数据每个栅格的流向得到流向栅格。下图显示了基于无洼地的 DEM 数据生成的流向栅格。

    .. image:: ../image/FlowDirection_3.png

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param surface_grid: 用于计算流向的 DEM 数据
    :type surface_grid: DatasetGrid or str
    :param bool force_flow_at_edge: 指定是否强制边界的栅格流向为向外。如果为 True，则 DEM 栅格边缘处的所有单元的流向都是从栅格向外流动。
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果流向数据集的名称
    :param str out_drop_grid_name: 结果高程梯度栅格数据集名称。可选参数。用于计算流向的中间结果。中心单元格与相邻单元格的高程差与距离的比值称
                                   为高程梯度。如下图所示，为流向计算的一个实例，该实例中生成了高程梯度栅格

                                   .. image:: ../image/FlowDirection.png

    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个2个元素的tuple，第一个元素为 结果流向栅格数据集或数据集名称，如果设置了结果高程梯度栅格数据集名称，
             则第二个元素为结果高程梯度栅格数据集或数据集名称，否则为 None
    :rtype: tuple[DatasetGrid,DatasetGrid] or tuple[str,str]
    """
    surface_dt = get_input_dataset(surface_grid)
    if not isinstance(surface_dt, DatasetGrid):
        raise ValueError('surface_grid required DatasetGrid, but is ' + str(type(surface_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = surface_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = surface_dt.name + '_direct'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, 'flow_direction')
                    get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                flowDirection = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.flowDirection
                if out_drop_grid_name is None:
                    java_result = flowDirectionoj(surface_dt)bool(force_flow_at_edge)oj(out_datasource)_outDatasetName
                else:
                    java_result = flowDirection(oj(surface_dt), bool(force_flow_at_edge), oj(out_datasource), _outDatasetName, str(out_drop_grid_name))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is None:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return
            result_dt = out_datasource[_outDatasetName]
            if out_drop_grid_name is not None:
                drop_dt = out_datasource[str(out_drop_grid_name)]
        else:
            drop_dt = None
        if out_data is not None:
            return try_close_output_datasource((result_dt, drop_dt), out_datasource)
        return (
         result_dt, drop_dt)


def flow_length(direction_grid, up_stream, weight_grid=None, out_data=None, out_dataset_name=None, progress=None):
    """
    根据流向栅格计算流长，即计算每个单元格沿着流向到其流向起始点或终止点之间的距离。可应用权重数据集计算加权流长。

    流长，是指每个单元格沿着流向到其流向起始点或终止点之间的距离，包括上游方向和下游方向的长度。水流长度直接影响地面径流的速度，
    进而影响地面土壤的侵蚀力，因此在水土保持方面具有重要意义，常作为土壤侵蚀、水土流失情况的评价因素。

    流长的计算基于流向数据，流向数据表明水流的方向，该数据集可由流向分析创建；权重数据定义了每个单元格的水流阻力。流长一般用于
    洪水的计算，水流往往会受到诸如坡度、土壤饱和度、植被覆盖等许多因素的阻碍，此时对这些因素建模，需要提供权重数据集。

    流长有两种计算方式：

     * 顺流而下：计算每个单元格沿流向到下游流域汇水点之间的最长距离。
     * 溯流而上：计算每个单元格沿流向到上游分水线顶点的最长距离。

    下图分别为以顺流而下和溯流而上计算得出的流长栅格：

    .. image:: ../image/FlowLength.png

    权重数据定义了每个栅格单元间的水流阻力，应用权重所获得的流长为加权距离（即距离乘以对应权重栅格的值）。例如，将流长分析应用
    于洪水的计算，洪水流往往会受到诸如坡度、土壤饱和度、植被覆盖等许多因素的阻碍，此时对这些因素建模，需要提供权重数据集。

    注意，权重栅格必须与流向栅格具有相同的范围和分辨率。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param direction_grid: 指定的流向栅格数据。
    :type direction_grid: DatasetGrid or str
    :param bool up_stream: 指定顺流而下计算还是溯流而上计算。True 表示溯流而上，False 表示顺流而下。
    :param weight_grid:  指定的权重栅格数据。设置为 None 表示不使用权重数据集。
    :type weight_grid: DatasetGrid or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果流长栅格数据集的名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果流长栅格数据集或数据集名称
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError('direction_grid required DatasetGrid, but is ' + str(type(direction_grid)))
    elif weight_grid is not None:
        weight_dt = get_input_dataset(weight_grid)
        if not isinstance(weight_dt, DatasetGrid):
            raise ValueError('weight_grid required DatasetGrid, but is ' + str(type(weight_grid)))
        else:
            weight_dt = None
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + '_flow'
    else:
        _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'flow_length')
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            flowLength = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.flowLength
            java_result = flowLength(oj(direction_dt), oj(weight_dt), parse_bool(up_stream), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def pour_points(direction_grid, accumulation_grid, area_limit, out_data=None, out_dataset_name=None, progress=None):
    """
    根据流向栅格和累积汇水量栅格生成汇水点栅格。

    汇水点位于流域的边界上，通常为边界上的最低点，流域内的水从汇水点流出，所以汇水点必定具有较高的累积汇水量。根据这一特点，就可以基于累积汇水量和流向栅格来提取汇水点。

    汇水点的确定需要一个累积汇水量阈值，累积汇水量栅格中大于或等于该阈值的位置将作为潜在的汇水点，再依据流向最终确定汇水点的位置。该阈值的确定十分关键，影响着汇水点的数量、位置以及子流域的大小和范围等。合理的阈值，需要考虑流域范围内的土壤特征、坡度特征、气候条件等多方面因素，根据实际研究的需求来确定，因此具有较大难度。

    获得了汇水点栅格后，可以结合流向栅格来进行流域的分割（ :py:func:`watershed` 方法）。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param accumulation_grid: 累积汇水量栅格数据
    :type accumulation_grid: DatasetGrid or str
    :param int area_limit: 汇水量限制值
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果栅格数据集的名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果栅格数据集或数据集名称
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError('direction_grid required DatasetGrid, but is ' + str(type(direction_grid)))
    else:
        accumulation_dt = get_input_dataset(accumulation_grid)
        if not isinstance(accumulation_dt, DatasetGrid):
            raise ValueError('accumulation_grid required DatasetGrid, but is ' + str(type(accumulation_grid)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + '_pour'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'pour_points')
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            pourPoints = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.pourPoints
            java_result = pourPoints(oj(direction_dt), oj(accumulation_dt), int(area_limit), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def stream_link(stream_grid, direction_grid, out_data=None, out_dataset_name=None, progress=None):
    """
    连接水系，即根据栅格水系和流向栅格为每条河流赋予唯一值。
    连接水系基于栅格水系和流向栅格，为水系中的每条河流分别赋予唯一值，值为整型。连接后的水系网络记录了水系节点的连接信息，体现了
    水系的网络结构。

    如下图所示，连接水系后，每条河段都有唯一的栅格值。图中红色的点为交汇点，即河段与河段相交的位置。河段是河流的一部分，它连接
    两个相邻交汇点，或连接一个交汇点和汇水点，或连接一个交汇点和分水线。因此，连接水系可用于确定流域盆地的汇水点。

    .. image:: ../image/StreamLink_1.png

    下图连接水系的一个实例。

    .. image:: ../image/StreamLink_2.png

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param stream_grid: 栅格水系数据
    :type stream_grid: DatasetGrid or str
    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果栅格数据集的名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 连接后的栅格水系，为一个栅格数据集。返回结果栅格数据集或数据集名称
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError('direction_grid required DatasetGrid, but is ' + str(type(direction_grid)))
    else:
        stream_dt = get_input_dataset(stream_grid)
        if not isinstance(stream_grid, DatasetGrid):
            raise ValueError('stream_grid required DatasetGrid, but is ' + str(type(stream_grid)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + '_stream'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'stream_link')
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            streamLink = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.streamLink
            java_result = streamLinkoj(stream_dt)oj(direction_dt)oj(out_datasource)_outDatasetName
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def stream_order(stream_grid, direction_grid, order_type, out_data=None, out_dataset_name=None, progress=None):
    """
    对河流进行分级，根据河流等级为栅格水系编号。

    流域中的河流分为干流和支流，在水文学中，根据河流的流量、形态等因素对河流进行分级。在水文分析中，可以从河流的级别推断出河流的某些特征。

    该方法以栅格水系为基础，依据流向栅格对河流分级，结果栅格的值即代表该条河流的等级，值越大，等级越高。SuperMap 提供两种河流
    分级方法：Strahler 法和 Shreve 法。有关这两种方法的介绍请参见 :py:class`StreamOrderType` 枚举类型。

    如下图所示，是河流分级的一个实例。根据 Shreve 河流分级法，该区域的河流被分为14个等级。

    .. image:: ../image/StreamOrder.png

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param stream_grid: 栅格水系数据
    :type stream_grid: DatasetGrid or str
    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param order_type: 流域水系编号方法
    :type order_type: StreamOrderType or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果栅格数据集的名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 编号后的栅格流域水系网络，为一个栅格数据集。返回结果数据集或数据集名称。
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError('direction_grid required DatasetGrid, but is ' + str(type(direction_grid)))
    else:
        stream_dt = get_input_dataset(stream_grid)
        if not isinstance(stream_grid, DatasetGrid):
            raise ValueError('stream_grid required DatasetGrid, but is ' + str(type(stream_grid)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + '_stream'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'stream_order')
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            stream_order_type = StreamOrderType._make(order_type)
            streamOrder = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.streamOrder
            java_result = streamOrder(oj(stream_dt), oj(direction_dt), oj(stream_order_type), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def stream_to_line(stream_grid, direction_grid, order_type, out_data=None, out_dataset_name=None, progress=None):
    """
    提取矢量水系，即将栅格水系转化为矢量水系。

    提取矢量水系是基于流向栅格，将栅格水系转化为矢量水系（一个矢量线数据集）的过程。得到矢量水系后，就可以进行各种基于矢量的计
    算、处理和空间分析，如构建水系网络。下图为 DEM 数据以及对应的矢量水系。

    .. image:: ../image/StreamToLine.png

    通过该方法获得的矢量水系数据集，保留了河流的等级和流向信息。

     * 在提取矢量水系的同时，系统计算每条河流的等级，并在结果数据集中自动添加一个名为“StreamOrder”的属性字段来存储该值。分级的方式可
       通过 order_type 参数设置。

     * 流向信息存储在结果数据集中名为“Direction”的字段中，以0或1来表示，0表示流向与该线对象的几何方向一致，1表示与线对象的几何
       方向相反。通过该方法获得的矢量水系的流向均与其几何方向相同，即“Direction”字段值都为0。在对矢量水系构建水系网络后，可直接
       使用（或根据实际需要进行修改）该字段作为流向字段。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param stream_grid: 栅格水系数据
    :type stream_grid: DatasetGrid or str
    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param order_type: 河流分级方法
    :type order_type: StreamOrderType or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果矢量水系数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 矢量水系数据集或数据集名称
    :rtype: DatasetVector or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError('direction_grid required DatasetGrid, but is ' + str(type(direction_grid)))
    else:
        stream_dt = get_input_dataset(stream_grid)
        if not isinstance(stream_grid, DatasetGrid):
            raise ValueError('stream_grid required DatasetGrid, but is ' + str(type(stream_grid)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + '_stream'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'stream_to_line')
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            stream_order_type = StreamOrderType._make(order_type)
            streamToLine = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.streamToLine
            java_result = streamToLine(oj(stream_dt), oj(direction_dt), oj(out_datasource), _outDatasetName, oj(stream_order_type))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def watershed(direction_grid, pour_points_or_grid, out_data=None, out_dataset_name=None, progress=None):
    """

    流域分割，即生成指定汇水点（汇水点栅格数据集）的流域盆地。

    将一个流域划分为若干个子流域的过程称为流域分割。通过 :py:meth:`basin` 方法，可以获取较大的流域，但实际分析中，可能需要将较大的流域划
    分出更小的流域（称为子流域）。

    确定流域的第一步是确定该流域的汇水点，那么，流域分割同样首先要确定子流域的汇水点。与使用 basin 方法计算流域盆地不同，子流
    域的汇水点可以在栅格的边界上，也可能位于栅格的内部。该方法要求输入一个汇水点栅格数据，该数据可通过提取汇水点功能（ :py:meth:`pour_points` 方法）
    获得。此外，还可以使用另一个重载方法，输入表示汇水点的二维点集合来分割流域。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param pour_points_or_grid: 汇水点栅格数据或指定的汇水点（二维点列表），汇水点使用地理坐标单位。
    :type pour_points_or_grid: DatasetGrid or str or list[Point2D]
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果汇水点的流域盆地栅格数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 汇水点的流域盆地栅格数据集或数据集名称
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError('direction_grid required DatasetGrid, but is ' + str(type(direction_grid)))
    else:
        if isinstance(pour_points_or_grid, (list, tuple)):
            java_pout_points = to_java_point2ds(pour_points_or_grid)
        else:
            java_pout_points = get_input_dataset(pour_points_or_grid)
            if not isinstance(java_pout_points, DatasetGrid):
                raise ValueError('pour_points_or_grid required DatasetGrid, but is ' + str(type(pour_points_or_grid)))
            java_pout_points = oj(java_pout_points)
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + '_watershed'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'watershed')
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            watershed = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.watershed
            java_result = watershedoj(direction_dt)java_pout_pointsoj(out_datasource)_outDatasetName
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def _to_java_spatial_stat_type_array(values):
    if values is None:
        return
        jvm = get_jvm()
        if isinstance(values, SpatialStatisticsType):
            java_array = get_gateway().new_array(jvm.com.supermap.analyst.spatialstatistics.StatisticsType, 1)
            java_array[0] = oj(values)
            return java_array
        if isinstance(values, (list, tuple, set)):
            _size = len(values)
            java_array = get_gateway().new_array(jvm.com.supermap.analyst.spatialstatistics.StatisticsType, _size)
            i = 0
            for value in values:
                if isinstance(value, SpatialStatisticsType):
                    java_array[i] = oj(value)
                else:
                    if isinstance(value, (str, int)):
                        v = SpatialStatisticsType._make(value)
                        if v is not None:
                            java_array[i] = oj(v)
                    else:
                        java_array[i] = value
                i += 1

            return java_array
        java_array = get_gateway().new_array(jvm.com.supermap.analyst.spatialstatistics.StatisticsType, 1)
        if isinstance(values, (str, int)):
            v = SpatialStatisticsType._make(values)
            if v is not None:
                java_array[0] = oj(v)
    else:
        java_array[0] = values
    return java_array


def _measure_param(group_field=None, weight_field=None, self_weight_field=None, distance_method='EUCLIDEAN', stats_fields=None, ellipse_size=None, is_orientation=None):
    java_param = get_jvm().com.supermap.analyst.spatialstatistics.MeasureParameter()
    java_param.setGroupFieldName(group_field)
    if weight_field is not None:
        java_param.setWeightFieldName(weight_field)
    else:
        if self_weight_field is not None:
            java_param.setSelfWeightFieldName(self_weight_field)
        if distance_method is not None:
            java_param.setDistanceMethod(oj(DistanceMethod._make(distance_method)))
        if isinstance(stats_fields, (list, str)):
            fields = []
            stat_types = []
            stats_fields = split_input_list_tuple_item_from_str(stats_fields)
            if isinstance(stats_fields, list):
                for f, t in stats_fields:
                    t = SpatialStatisticsType._make(t)
                    if t is not None:
                        fields.append(str(f))
                        stat_types.append(oj(t))

        else:
            fields = None
            stat_types = None
    if fields is not None:
        if len(fields) > 0:
            java_param.setStatisticsFieldNames(to_java_string_array(fields))
            java_param.setStatisticsTypes(_to_java_spatial_stat_type_array(stat_types))
    if ellipse_size is not None:
        java_param.setEllipseSize(oj(EllipseSize._make(ellipse_size)))
    if is_orientation is not None:
        java_param.setOrientation(parse_bool(is_orientation))
    return java_param


def measure_central_element(source, group_field=None, weight_field=None, self_weight_field=None, distance_method='EUCLIDEAN', stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """
    关于空间度量：

        空间度量用来计算的数据可以是点、线、面。对于点、线和面对象，在距离计算中会使用对象的质心。对象的质心为所有子对象的加权
        平均中心。点对象的加权项为1（即质心为自身），线对象的加权项是长度，而面对象的加权项是面积。

        用户可以通过空间度量计算来解决以下问题：

            1. 数据的中心在哪里？

            2. 数据的分布呈什么形状和方向？

            3. 数据是如何分散布局？

        空间度量包括中心要素（ :py:func:`measure_central_element` ）、方向分布（ :py:func:`measure_directional` ）、
        标准距离（ :py:func:`measure_standard_distance` ）、方向平均值（ :py:func:`measure_linear_directional_mean` ）、
        平均中心（ :py:func:`measure_mean_center` ）、中位数中心（ :py:func:`measure_median_center` ）等。

    计算矢量数据的中心要素，返回结果矢量数据集。

     * 中心要素是与其他所有对象质心的累积距离最小，位于最中心的对象。

     * 如果设置了分组字段，则结果矢量数据集将包含 “分组字段名_Group” 字段。

     * 实际上，距其他所有对象质心的累积距离最小的中心要素可能会有多个，但中心要素方法只会输出SmID 字段值最小的对象。

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段的名称
    :param str weight_field: 权重字段的名称
    :param str self_weight_field: 自身权重字段的名称
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param stats_fields: 统计字段的类型，为一个字典类型，字典类型的 key 为字段名，value 为统计类型。
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果矢量数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_measure'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'measure_central_element')
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, weight_field, self_weight_field, distance_method, stats_fields)
            measureCentralElement = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureCentralElement
            java_result = measureCentralElementoj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def measure_directional(source, group_field=None, ellipse_size='SINGLE', stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """
    计算矢量数据的方向分布，返回结果矢量数据集。

     * 方向分布是根据所有对象质心的平均中心（有权重，为加权）为圆点，计算x和y坐标的标准差为轴得到的标准差椭圆。

     * 标准差椭圆的圆心x和y坐标、两个标准距离（长半轴和短半轴）、椭圆的方向，分别储存在结果矢量数据集中的CircleCenterX、
       CircleCenterY、SemiMajorAxis、SemiMinorAxis、RotationAngle字段中。如果设置了分组字段，则结果矢量数据集将包含
       “分组字段名_Group” 字段。

     * 椭圆的方向RotationAngle字段中的正值表示正椭圆（长半轴的方向为X轴方向, 短半轴的方向为Y轴方向)）按逆时针旋转，负值表示
       正椭圆按顺时针旋转。

     * 输出的椭圆大小有三个级别：Single（一个标准差）、Twice（二个标准差）和Triple（三个标准差），详细介绍请参见 :py:class:`.EllipseSize` 类。

     * 用于计算方向分布的标准差椭圆算法是由D. Welty Lefever在1926年提出，用来度量数据的方向和分布。首先确定椭圆的圆心，即平均
       中心（有权重，为加权）；然后确定椭圆的方向；最后确定长轴和短轴的长度。

     .. image:: ../image/MeasureDirection.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段名称
    :param ellipse_size: 椭圆大小类型
    :type ellipse_size: EllipseSize or str
    :param stats_fields: 统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果矢量数据集
    :rtype: DatasetVector or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_measure'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'measure_direction_element')
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, None, None, None, stats_fields, ellipse_size)
            measureDirectional = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureDirectional
            java_result = measureDirectionaloj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def measure_linear_directional_mean(source, group_field=None, weight_field=None, is_orientation=False, stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """

    计算线数据集的方向平均值，并返回结果矢量数据集。

     * 线性方向平均值是根据所有线对象的质心的平均中心点为其中心、长度等于所有输入线对象的平均长度、方位或方向为由所有输入线对象
       的起点和终点（每个线对象都只会使用起点和终点来确定方向）计算得到的平均方位或平均方向创建的线对象。

     * 线对象的平均中心x和y坐标、平均长度、罗盘角、方向平均值、圆方差，分别储存在结果矢量数据集中的AverageX、AverageY、
       AverageLength、CompassAngle、DirectionalMean、CircleVariance字段中。如果设置了分组字段，则结果矢量数据集将包含
       “分组字段名_Group” 字段。

     * 线对象的罗盘角（CompassAngle）字段表示以正北方为基准方向按顺时针旋转;方向平均值（DirectionalMean）字段表示以正东方为
       基准方向按逆时针旋转;圆方差（CircleVariance）表示方向或方位偏离方向平均值的程度,如果输入线对象具有非常相似（或完全相同）
       的方向则该值会非常小，反之则相反。

     .. image:: ../image/MeasureLinearDirectionalMean.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。为线数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段名称
    :param str weight_field: 权重字段名称
    :param bool is_orientation: 是否忽略起点和终点的方向。为 False 时，将在计算方向平均值时使用起始点和终止点的顺序；为 True 时，将忽略起始点和终止点的顺序。
    :param stats_fields:  统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_measure'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'measure_linear_directional_mean')
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_paramgroup_fieldweight_fieldNoneNonestats_fieldsNoneis_orientation
            measureLinearDirectionalMean = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureLinearDirectionalMean
            java_result = measureLinearDirectionalMeanoj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def measure_mean_center(source, group_field=None, weight_field=None, stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """
    计算矢量数据的平均中心，返回结果矢量数据集。

     * 平均中心是根据输入的所有对象质心的平均x和y坐标构造的点。

     * 平均中心的x和y坐标分别储存在结果矢量数据集中的SmX和SmY字段中。如果设置了分组字段，则结果矢量数据集将包含 “分组字段名_Group” 字段。

     .. image:: ../image/MeasureMeanCenter.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段
    :param str weight_field: 权重字段
    :param stats_fields: 统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_measure'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'measure_mean_center')
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, weight_field, None, None, stats_fields)
            measureMeanCenter = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureMeanCenter
            java_result = measureMeanCenteroj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def measure_median_center(source, group_field, weight_field, stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """

    计算矢量数据的中位数中心，返回结果矢量数据集。

     * 中位数中心是根据输入的所有对象质心，使用迭代算法找出到所有对象质心的欧式距离最小的点。

     * 中位数中心的x和y坐标分别储存在结果矢量数据集中的SmX和SmY字段中。如果设置了分组字段，则结果矢量数据集将包含
       “分组字段名_Group” 字段。

     * 实际上，距所有对象质心的距离最小的点可能有多个，但中位数中心方法只会返回一个点。

     * 用于计算中位数中心的算法是由Kuhn,Harold W.和Robert E. Kuenne在1962年提出的迭代加权最小二乘法（Weiszfeld算法），之后由
       James E. Burt和Gerald M. Barber进一步概括。首先以平均中心（有权重，为加权）作为起算点，利用加权最小二乘法得到候选点，将
       候选点重新作为起算点代入计算得到新的候选点，迭代计算直到候选点到所有对象质心的欧式距离最小为止。

     .. image:: ../image/MeasureMedianCenter.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段
    :param str weight_field: 权重字段
    :param stats_fields: 统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_measure'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'measure_median_center')
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, weight_field, None, None, stats_fields)
            measureMedianCenter = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureMedianCenter
            java_result = measureMedianCenteroj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def measure_standard_distance(source, group_field, weight_field, ellipse_size='SINGLE', stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """

    计算矢量数据的标准距离，返回结果矢量数据集。

     * 标准距离是根据所有对象质心的平均中心（有权重，为加权）为圆心，计算x和y坐标的标准距离为半径得到的圆。

     * 圆的圆心x和y坐标、标准距离（圆的半径），分别储存在结果矢量数据集中的CircleCenterX、CircleCenterY、StandardDistance字
       段中。如果设置了分组字段，则结果矢量数据集将包含 “分组字段名_Group” 字段。

     * 输出的圆大小有三个级别：Single（一个标准差）、Twice（二个标准差）和Triple（三个标准差），详细介绍请参见 :py:class:`.EllipseSize` 枚举类型。

     .. image:: ../image/MeasureStandardDistance.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。为线数据集
    :type source: DatasetVector or str
    :param str group_field: 分组字段
    :param str weight_field: 权重字段
    :param ellipse_size: 椭圆大小类型
    :type ellipse_size: EllipseSize or str
    :param stats_fields: 统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_measure'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'measure_standard_distance')
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, weight_field, None, None, stats_fields, ellipse_size)
            measureStandardDistance = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureStandardDistance
            java_result = measureStandardDistanceoj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def _patterns_param(assessment_field=None, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, weight_file_path=None, k_neighbors=1, is_standardization=False, is_FDR_adj=False, self_weight_field=None):
    java_param = get_jvm().com.supermap.analyst.spatialstatistics.PatternsParameter()
    if assessment_field is not None:
        java_param.setAssessmentFieldName(str(assessment_field))
    if concept_model is not None:
        java_param.setConceptModel(oj(ConceptualizationModel._make(concept_model)))
    if distance_method is not None:
        java_param.setDistanceMethod(oj(DistanceMethod._make(distance_method)))
    if distance_tolerance is not None:
        java_param.setDistanceTolerance(float(distance_tolerance))
    if exponent is not None:
        java_param.setExponent(float(exponent))
    if weight_file_path is not None:
        java_param.setFilePath(str(weight_file_path))
    if k_neighbors is not None:
        java_param.setKNeighbors(int(k_neighbors))
    if is_standardization is not None:
        java_param.setStandardization(parse_bool(is_standardization))
    if is_FDR_adj is not None:
        java_param.setFDRAdjusted(bool(is_FDR_adj))
    if self_weight_field is not None:
        java_param.setSelfWeightFieldName(str(self_weight_field))
    return java_param


class AnalyzingPatternsResult:
    __doc__ = '\n    分析模式结果类。该类用于获取分析模式计算的结果，包括结果指数、期望、方差、Z得分和P值等。\n    '

    def __init__(self):
        self._expectation = None
        self._index = None
        self._p_value = None
        self._variance = None
        self._z_score = None

    def __str__(self):
        s = []
        s.append('AnalyzingPatternsResult: ')
        s.append('expectation: ' + str(self.expectation))
        s.append('index:       ' + str(self.index))
        s.append('variance:    ' + str(self.variance))
        s.append('P value:     ' + str(self.p_value))
        s.append('Z score:     ' + str(self.z_score))
        return '\n'.join(s)

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        result = AnalyzingPatternsResult()
        result._expectation = java_obj.getExpectation()
        result._index = java_obj.getIndex()
        result._p_value = java_obj.getPValue()
        result._variance = java_obj.getVariance()
        result._z_score = java_obj.getZScore()
        return result

    @property
    def expectation(self):
        """float: 分析模式结果中的期望值"""
        return self._expectation

    @property
    def index(self):
        """float: 分析模式结果中的莫兰指数或GeneralG指数"""
        return self._index

    @property
    def p_value(self):
        """float: 分析模式结果中的P值"""
        return self._p_value

    @property
    def z_score(self):
        """float: 分析模式结果中的Z得分"""
        return self._z_score

    @property
    def variance(self):
        """float: 分析模式结果中的方差值"""
        return self._variance


def auto_correlation(source, assessment_field, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, k_neighbors=1, is_standardization=False, weight_file_path=None, progress=None):
    """
    分析模式介绍：

        分析模式可评估一组数据是形成离散空间模式、聚类空间模式或者随机空间模式。

        * 分析模式用来计算的数据可以是点、线、面。对于点、线和面对象，在距离计算中会使用对象的质心。对象的质心为所有子对象的加权平均中心。点对象的加权项为1（即质心为自身），线对象的加权项是长度，而面对象的加权项是面积。
        * 分析模式类采用推论式统计,会在进行统计检验时预先建立"零假设",假设要素或要素之间相关的值都表现为随机空间模式。
        * 分析结果计算中会给出一个P值用来表示"零假设"的正确概率,用以判定是接受"零假设"还是拒绝"零假设"。
        * 分析结果计算中会给出一个Z得分用来表示标准差的倍数,用以判定数据是呈聚类、离散或随机。
        * 要拒绝"零假设",就必须要承担可能做出错误选择（即错误的拒绝"零假设"）的风险。

          下表显示了不同置信度下未经校正的临界P值和临界Z得分:

          .. image:: ../image/AnalyzingPatterns.png

        * 用户可以通过分析模式来解决以下问题：

            * 数据集中的要素或数据集中要素关联的值是否发生空间聚类？
            * 数据集的聚类程度是否会随时间变化？

        分析模式包括空间自相关分析（ :py:func:`auto_correlation` ）、平均最近邻分析（ :py:func:`average_nearest_neighbor` ）、
        高低值聚类分析（ :py:func:`high_or_low_clustering` ）、增量空间自相关分析（ :py:func:`incremental_auto_correlation` ）等。

    对矢量数据集进行空间自相关分析，并返回空间自相关分析结果。空间自相关返回的结果包括莫兰指数、期望、方差、z得分、P值,
    请参阅 :py:class:`.AnalyzingPatternsResult` 类。

    .. image:: ../image/AnalyzingPatterns_autoCorrelation.png

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param concept_model: 空间关系概念化模型。默认值 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE`。
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。
    :param int k_neighbors:  相邻数目，目标要素周围最近的K个要素为相邻要素。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param str weight_file_path: 空间权重矩阵文件路径
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 空间自相关结果
    :rtype: AnalyzingPatternsResult
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'auto_correlation')
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            autoCorrelation = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.autoCorrelation
            java_param = _patterns_param(assessment_field, concept_model, distance_method, distance_tolerance, exponent, weight_file_path, k_neighbors, is_standardization)
            java_result = autoCorrelation(oj(source_dt), java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return AnalyzingPatternsResult._from_java_object(java_result)


def high_or_low_clustering(source, assessment_field, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, k_neighbors=1, is_standardization=False, weight_file_path=None, progress=None):
    """
    对矢量数据集进行高低值聚类分析,并返回高低值聚类分析结果。 高低值聚类返回的结果包括GeneralG指数、期望、方差、z得分、P值,
    请参阅 :py:class:`.AnalyzingPatternsResult` 类。

    .. image:: ../image/AnalyzingPatterns_highOrLowClustering.png

    关于分析模式介绍，请参考 :py:func:`auto_correlation`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param concept_model: 空间关系概念化模型。默认值 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE`。
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。
    :param int k_neighbors:  相邻数目，目标要素周围最近的K个要素为相邻要素。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param str weight_file_path: 空间权重矩阵文件路径
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 高低值聚类结果
    :rtype: AnalyzingPatternsResult
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'high_or_low_clustering')
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            highOrLowClustering = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.highOrLowClustering
            java_param = _patterns_param(assessment_field, concept_model, distance_method, distance_tolerance, exponent, weight_file_path, k_neighbors, is_standardization)
            java_result = highOrLowClustering(oj(source_dt), java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return AnalyzingPatternsResult._from_java_object(java_result)


def average_nearest_neighbor(source, study_area, distance_method='EUCLIDEAN', progress=None):
    """

    对矢量数据集进行平均最近邻分析，并返回平均最近邻分析结果数组。

    * 平均最近邻返回的结果包括最近邻指数、预期平均距离、平均观测距离、z得分、P值,请参阅 :py:class:`.AnalyzingPatternsResult` 类。

    * 给定的研究区域面积大小必须大于等于0;如果研究区域面积等于0,则会自动生成输入数据集的最小面积外接矩形,用该矩形的面积来进行计算。
      该默认值为: 0 。

    * 距离计算方法类型可以指定相邻要素之间的距离计算方式(参阅 :py:class:`.DistanceMethod` )。如果输入数据集为地理坐标系，则会采用弦测量方法来
      计算距离。地球表面上的任意两点,两点之间的弦距离为穿过地球体连接两点的直线长度。

    .. image:: ../image/AnalyzingPatterns_AverageNearestNeighbor.png

    关于分析模式介绍，请参考 :py:func:`auto_correlation`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param float study_area: 研究区域面积
    :param distance_method: 距离计算方法
    :type distance_method: DistanceMethod or str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 平均最近邻分析结果
    :rtype: AnalyzingPatternsResult
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'average_nearest_neighbor')
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            averageNearestNeighbor = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.averageNearestNeighbor
            java_result = averageNearestNeighbor(oj(source_dt), float(study_area), oj(DistanceMethod._make(distance_method, 'EUCLIDEAN')))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return AnalyzingPatternsResult._from_java_object(java_result)


class IncrementalResult(AnalyzingPatternsResult):
    __doc__ = '\n    增量空间自相关结果类。该类用于获取增量空间自相关计算的结果，包括结果增量距离、莫兰指数、期望、方差、Z得分和P值等。\n    '

    def __init__(self):
        AnalyzingPatternsResult.__init__(self)
        self._distance = None

    def __str__(self):
        s = []
        s.append('IncrementalResult: ')
        s.append('expectation: ' + str(self.expectation))
        s.append('index:       ' + str(self.index))
        s.append('variance:    ' + str(self.variance))
        s.append('P value:     ' + str(self.p_value))
        s.append('Z score:     ' + str(self.z_score))
        s.append('distance:      ' + str(self.distance))
        return '\n'.join(s)

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        result = IncrementalResult()
        result._expectation = java_obj.getExpectation()
        result._index = java_obj.getIndex()
        result._p_value = java_obj.getPValue()
        result._variance = java_obj.getVariance()
        result._z_score = java_obj.getZScore()
        result._distance = java_obj.getDistance()
        return result

    @property
    def distance(self):
        """float: 增量空间自相关结果中的增量距离"""
        return self._distance


def incremental_auto_correlation(source, assessment_field, begin_distance=0.0, distance_method='EUCLIDEAN', incremental_distance=0.0, incremental_number=10, is_standardization=False, progress=None):
    """
    对矢量数据集进行增量空间自相关分析，并返回增量空间自相关分析结果数组。增量空间自相关返回的结果包括增量距离、莫兰指数、期望、方差、z得分、P值,
    请参阅 :py:class:`.IncrementalResult` 类。

    增量空间自相关会为一系列的增量距离运行空间自相关方法（参考 :py:func:`auto_correlation` ）,空间关系概念化模型默认为固定距离
    模型(参阅 :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` ）

    关于分析模式介绍，请参考 :py:func:`auto_correlation`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param float begin_distance: 增量空间自相关开始分析的起始距离。
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float incremental_distance: 距离增量，增量空间自相关每次分析的间隔距离。
    :param int incremental_number: 递增的距离段数目。为增量空间自相关指定分析数据集的次数，该值的范围为：2 ~ 30。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 增量空间自相关分析结果列表。
    :rtype: list[IncrementalResult]
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'incremental_auto_correlation')
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = get_jvm().com.supermap.analyst.spatialstatistics.IncrementalParameter()
            if assessment_field is not None:
                java_param.setAssessmentFieldName(str(assessment_field))
            if begin_distance is not None:
                java_param.setBeginDistance(float(begin_distance))
            if distance_method is not None:
                java_param.setDistanceMethod(oj(DistanceMethod._make(distance_method, 'EUCLIDEAN')))
            if incremental_distance is not None:
                java_param.setIncrementalDistance(float(incremental_distance))
            if incremental_number is not None:
                java_param.setIncrementalNumber(int(incremental_number))
            if is_standardization is not None:
                java_param.setStandardization(parse_bool(is_standardization))
            incrementalAutoCorrelation = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.incrementalAutoCorrelation
            java_result = incrementalAutoCorrelation(oj(source_dt), java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return list((IncrementalResult._from_java_object(item) for item in java_result))


def cluster_outlier_analyst(source, assessment_field, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, is_FDR_adjusted=False, k_neighbors=1, is_standardization=False, weight_file_path=None, out_data=None, out_dataset_name=None, progress=None):
    """
    聚类分布介绍：

        聚类分布可识别一组数据具有统计显著性的热点、冷点或者空间异常值。

        聚类分布用来计算的数据可以是点、线、面。对于点、线和面对象，在距离计算中会使用对象的质心。对象的质心为所有子对象的加权
        平均中心。点对象的加权项为1（即质心为自身），线对象的加权项是长度，而面对象的加权项是面积。

        用户可以通过聚类分布计算来解决以下问题：

            1. 聚类或冷点和热点出现在哪里？
            2. 空间异常值的出现位置在哪里？
            3. 哪些要素十分相似？

        聚类分布包括聚类和异常值分析（:py:func:`cluster_outlier_analyst`）、热点分析（:py:func:`hot_spot_analyst`）、
        优化热点分析（:py:func:`optimized_hot_spot_analyst`）等

    聚类和异常值分析，返回结果矢量数据集。

     * 结果数据集中包括局部莫兰指数（ALMI_MoranI）、z得分（ALMI_Zscore）、P值（ALMI_Pvalue）和聚类和异常值类型（ALMI_Type）。
     * z得分和P值都是统计显著性的度量,用于逐要素的判断是否拒绝"零假设"。置信区间字段会识别具有统计显著性的聚类和异常值。如果,
       要素的Z得分是一个较高的正值,则表示周围的要素拥有相似值（高值或低值）,聚类和异常值类型字段将具有统计显著性的高值聚类表示
       为"HH"，将具有统计显著性的低值聚类表示为"LL";如果,要素的Z得分是一个较低的负值值,则表示有一个具有统计显著性的空间数据异常
       值,聚类和异常值类型字段将指出低值要素围绕高值要素表示为"HL"，将高值要素围绕低值要素表示为"LH"。
     * 在没有设置 is_FDR_adjusted,统计显著性以P值和Z字段为基础,否则,确定置信度的关键P值会降低以兼顾多重测试和空间依赖性。

     .. image:: ../image/ClusteringDistributions_clusterOutlierAnalyst.png

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param concept_model: 空间关系概念化模型。默认值 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE`。
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。
    :param bool is_FDR_adjusted: 是否进行FDR（错误发现率）校正。若进行FDR（错误发现率）校正,则统计显著性将以错误发现率校正为基础,否则,统计显著性将以P值和z得分字段为基础。
    :param int k_neighbors:  相邻数目，目标要素周围最近的K个要素为相邻要素。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param str weight_file_path: 空间权重矩阵文件路径
    :param out_data: 结果数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_outlier'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'cluster_outlier_analyst')
                        get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            clusterOutlierAnalyst = get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.clusterOutlierAnalyst
            java_param = _patterns_param(assessment_field, concept_model, distance_method, distance_tolerance, exponent, weight_file_path, k_neighbors, is_standardization, is_FDR_adjusted)
            java_result = clusterOutlierAnalystoj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def hot_spot_analyst(source, assessment_field, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, is_FDR_adjusted=False, k_neighbors=1, is_standardization=False, self_weight_field=None, weight_file_path=None, out_data=None, out_dataset_name=None, progress=None):
    """
    热点分析，返回结果矢量数据集。

     * 结果数据集中包括z得分（Gi_Zscore）、P值（Gi_Pvalue）和置信区间（Gi_ConfInvl）。

     * z得分和P值都是统计显著性的度量,用于逐要素的判断是否拒绝"零假设"。置信区间字段会识别具有统计显著性的热点和冷点。置信区间
       为+3和-3的要素反映置信度为99%的统计显著性,置信区间为+2和-2的要素反映置信度为95%的统计显著性,置信区间为+1和-1的要素反映置
       信度为90%的统计显著性,而置信区间为0的要素的聚类则没有统计意义。

     * 在没有设置 is_FDR_adjusted 方法的情况下,统计显著性以P值和Z字段为基础,否则,确定置信度的关键P值会降低以兼顾多重测试和空间依赖性。

    .. image:: ../image/ClusteringDistributions_hotSpotAnalyst.png

    关于聚类分布介绍，参考 :py:func:`cluster_outlier_analyst`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param concept_model: 空间关系概念化模型。默认值 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE`。
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                           :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                           :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。
    :param bool is_FDR_adjusted: 是否进行 FDR（错误发现率）校正。若进行FDR（错误发现率）校正,则统计显著性将以错误发现率校正为基础,否则,统计显著性将以P值和z得分字段为基础。
    :param int k_neighbors:  相邻数目，目标要素周围最近的K个要素为相邻要素。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param str self_weight_field: 自身权重字段的名称，仅数值字段有效。
    :param str weight_file_path: 空间权重矩阵文件路径
    :param out_data: 结果数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_hotspot'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'hot_spot_analyst')
                        get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            hotSpotAnalyst = get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.hotSpotAnalyst
            java_param = _patterns_param(assessment_field, concept_model, distance_method, distance_tolerance, exponent, weight_file_path, k_neighbors, is_standardization, is_FDR_adjusted, self_weight_field)
            java_result = hotSpotAnalystoj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def optimized_hot_spot_analyst(source, assessment_field=None, aggregation_method='NETWORKPOLYGONS', aggregating_polygons=None, bounding_polygons=None, out_data=None, out_dataset_name=None, progress=None):
    """
    优化的热点分析，返回结果矢量数据集。

     * 结果数据集中包括z得分（Gi_Zscore）、P值（Gi_Pvalue）和置信区间（Gi_ConfInvl）,详细介绍请参阅 :py:func:`hot_spot_analyst` 方法结果。

     * z得分和P值都是统计显著性的度量,用于逐要素的判断是否拒绝"零假设"。置信区间字段会识别具有统计显著性的热点和冷点。置信区间
       为+3和-3的要素反映置信度为99%的统计显著性,置信区间为+2和-2的要素反映置信度为95%的统计显著性,置信区间为+1和-1的要素反映
       置信度为90%的统计显著性,而置信区间为0的要素的聚类则没有统计意义。

     * 如果提供分析字段，则会直接执行热点分析; 如果未提供分析字段，则会利用提供的聚合方法（参阅 :py:class:`AggregationMethod`）聚
       合所有输入事件点以获得计数，从而作为分析字段执行热点分析。

     * 执行热点分析时，默认概念化模型为 :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、错误发现率（FDR）为 True ,
       统计显著性将使用错误发现率（FDR）校正法自动兼顾多重测试和空间依赖性。

     .. image:: ../image/ClusteringDistributions_OptimizedHotSpotAnalyst.png

    关于聚类分布介绍，参考 :py:func:`cluster_outlier_analyst`

    :param source: 待计算的数据集。如果设置了评估字段，可以为点、线、面数据集，否则，则必须为点数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。
    :param aggregation_method: 聚合方法。如果未设置提供分析字段，则需要为优化的热点分析提供的聚合方法。

                               * 如果设置为 :py:attr:`.AggregationMethod.AGGREGATIONPOLYGONS` ，则必须设置 aggregating_polygons
                               * 如果设置为 :py:attr:`.AggregationMethod.NETWORKPOLYGONS` ，如果设置了 bounding_polygons，则使用
                                 bounding_polygons 进行聚合，如果没有设置 bounding_polygons， 则使用点数据集的地理范围进行聚合。
                               * 如果设置为 :py:attr:`.AggregationMethod.SNAPNEARBYPOINTS` , aggregating_polygons 和 bounding_polygons 都无效。

    :type aggregation_method: AggregationMethod or str
    :param aggregating_polygons: 聚合事件点以获得事件计数的面数据集。如果未提供分析字段(assessment_field） 且 aggregation_method
                                 设置为 :py:attr:`.AggregationMethod.AGGREGATIONPOLYGONS` 时，提供聚合事件点以获得事件计数的面数据集。
                                 如果设置了评估字段，此参数无效。
    :type aggregating_polygons: DatasetVector or str
    :param bounding_polygons: 事件点发生区域的边界面数据集。必须为面数据集。如果未提供分析字段(assessment_field)且 aggregation_method
                              设置为 :py:attr:`.AggregationMethod.NETWORKPOLYGONS` 时，提供事件点发生区域的边界面数据集。
    :type bounding_polygons: DatasetVector or str
    :param out_data: 结果数据源信息
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_hotspot'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'optimized_hot_spot_analyst')
                        get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            optimizedHotSpotAnalyst = get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.optimizedHotSpotAnalyst
            java_param = get_jvm().com.supermap.analyst.spatialstatistics.OptimizedParameter()
            if assessment_field is not None:
                java_param.setAssessmentFieldName(str(assessment_field))
            if aggregating_polygons is not None:
                java_param.setAggregatingPolygons(oj(get_input_dataset(aggregating_polygons)))
            if aggregation_method is not None:
                java_param.setAggregationMethod(oj(AggregationMethod._make(aggregation_method)))
            if bounding_polygons is not None:
                java_param.setBoundingPolygons(oj(get_input_dataset(bounding_polygons)))
            java_result = optimizedHotSpotAnalystoj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def collect_events(source, out_data=None, out_dataset_name=None, progress=None):
    """

    收集事件,将事件数据转换成加权数据。

     * 结果点数据集中包含一个 Counts 字段,该字段会保存每个唯一位置所有质心的总和。

     * 收集事件只会处理质心坐标完全相同的对象,并且只会保留一个质心,去除其余的重复点。

     * 对于点、线和面对象，在距离计算中会使用对象的质心。对象的质心为所有子对象的加权平均中心。点对象的加权项为1（即质心为自身），
       线对象的加权项是长度，而面对象的加权项是面积。

    :param source: 待收集的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param out_data: 用于存储结果点数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果点数据集名称。
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_events'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'collect_events')
                        get_jvm().com.supermap.analyst.spatialstatistics.StatisticsUtilities.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            collectEvents = get_jvm().com.supermap.analyst.spatialstatistics.StatisticsUtilities.collectEvents
            java_result = collectEvents(oj(source_dt), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.StatisticsUtilities.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def build_weight_matrix(source, unique_id_field, file_path, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, k_neighbors=1, is_standardization=False, progress=None):
    """
    构建空间权重矩阵。

     * 空间权重矩阵文件旨在生成、存储、重用和共享一组要素之间关系的空间关系概念化模型。文件采用的是二进制文件格式创建,要素关系
       存储为稀疏矩阵。

     * 该方法会生成一个空间权重矩阵文件，文件格式为 ‘*.swmb’。生成的空间权重矩阵文件可用来进行分析，只要将空间关系概念化模型设
       置为 :py:attr:`.ConceptualizationModel.SPATIALWEIGHTMATRIXFILE` 并且通过 weight_file_path 参数指定创建的空间权重矩阵
       文件的完整路径。

    :param source: 待构建空间权重矩阵的数据集，支持点线面。
    :type source: DatasetVector or str
    :param str unique_id_field: 唯一ID字段名，必须是数值型字段。
    :param str file_path: 空间权重矩阵文件保存路径。
    :param concept_model: 概念化模型
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                           :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                           :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

    :param int k_neighbors: 相邻数目。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 如果构建空间权重矩阵，返回 True，否则返回 False
    :rtype: bool
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'build_weight_matrix')
                        get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            if not file_path.lower().endswith('.swmb'):
                file_path = file_path + '.swmb'
            buildWeightMatrix = get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.buildWeightMatrix
            java_param = _patterns_param(None, concept_model, distance_method, distance_tolerance, exponent, None, k_neighbors, is_standardization, None, None)
            java_result = buildWeightMatrixoj(source_dt)str(unique_id_field)str(file_path)java_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return java_result


def weight_matrix_file_to_table(file_path, out_data, out_dataset_name=None, progress=None):
    """
    空间权重矩阵文件转换成属性表。

    结果属性表包含源唯一ID字段（UniqueID）、相邻要素唯一ID字段（NeighborsID）、权重字段（Weight）。

    :param str file_path: 空间权重矩阵文件路径。
    :param out_data: 用于存储结果属性表的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果属性表名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果属性表数据集或数据集名称。
    :rtype: DatasetVector or str
    """
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
    else:
        raise ValueError('out_data cannot be None')
    if out_dataset_name is None:
        _outDatasetName = 'NewDataset'
    else:
        _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'weight_matrix_file_to_table')
                        get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.converToTableDataset(str(file_path), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class GWRSummary:
    __doc__ = '\n    地理加权回归结果汇总类。该类给出了地理加权回归分析的结果汇总，例如带宽、相邻数、残差平方和、AICc和判定系数等。\n    '

    def __init__(self):
        self._AIC = None
        self._AICc = None
        self._band_width = None
        self._edf = None
        self._effective_number = None
        self._neighbours = None
        self._r2 = None
        self._r2_adjusted = None
        self._residual_squares = None
        self._sigma = None

    def __str__(self):
        s = []
        s.append('GWRSummary: ')
        s.append('AIC:              ' + str(self.AIC))
        s.append('AICc:             ' + str(self.AICc))
        s.append('Band Width:       ' + str(self.band_width))
        s.append('Edf:              ' + str(self.Edf))
        s.append('Effective Number: ' + str(self.effective_number))
        s.append('Neighbours:       ' + str(self.neighbours))
        s.append('R2:               ' + str(self.R2))
        s.append('R2 Adjusted:      ' + str(self.R2_adjusted))
        s.append('Residual Squares: ' + str(self.residual_squares))
        s.append('Sigma:            ' + str(self.sigma))
        return '\n'.join(s)

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        result = GWRSummary()
        result._AIC = java_obj.getAIC()
        result._AICc = java_obj.getAICc()
        result._band_width = java_obj.getBandwidth()
        result._edf = java_obj.getEdf()
        result._effective_number = java_obj.getEffectiveNumber()
        result._neighbours = java_obj.getNeighbors()
        result._r2 = java_obj.getR2()
        result._r2_adjusted = java_obj.getR2Adjusted()
        result._residual_squares = java_obj.getResidualSquares()
        result._sigma = java_obj.getSigma()
        return result

    @property
    def AIC(self):
        """float: 地理加权回归结果汇总中的AIC。与AICc类似，是衡量模型拟合优良性的一种标准，可以权衡所估计模型的复杂度和模型拟
                  合数据的优良性，在评价模型时是兼顾了简洁性和精确性。表明增加自由参数的数目提高了拟合的优良性，AIC鼓励数据的
                  拟合性，但是应尽量避免出现过度拟合的情况。所以优先考虑AIC值较小的，是寻找可以最好的解释数据但包含最少自由参
                  数的模型。"""
        return self._AIC

    @property
    def AICc(self):
        """float: 地理加权回归结果汇总中的AICc。当数据增加时，AICc收敛为AIC，也是模型性能的一种度量，有助与比较不同的回归模型。
                  考虑到模型复杂性，具有较低AICc值的模型将更好的拟合观测数据。AICc不是拟合度的绝对度量，但对于比较用于同一因变
                  量且具有不同解释变量的模型非常有用。如果两个模型的AICc值相差大于3，具有较低AICc值的模型将视为更佳的模型。"""
        return self._AICc

    @property
    def band_width(self):
        """float: 地理加权回归结果汇总中的带宽范围。

                   * 用于各个局部估计的带宽范围，它控制模型中的平滑程度。通常，你可以选择默认的带宽范围，方法是：设置带宽确定
                     方式(kernel_type)方法选择 :py:attr:`.BandWidthType.AICC` 或 :py:attr:`.BandWidthType.CV`，这两个选项都将尝试识别最佳带宽范围。

                   * 由于"最佳"条件对于 AIC 和 CV 并不相同，都会得到相对的最优 AICc 值和 CV 值，因而通常会获得不同的最佳值。

                   * 可以通过设置带宽类型（kernel_type）方法提供精确的带宽范围。
        """
        return self._band_width

    @property
    def Edf(self):
        """float: 地理加权回归结果汇总中的有效自由度。数据的数目与有效的参数数量（EffectiveNumber）的差值，不一定是整数，可用
                  来计算多个诊断测量值。自由度较大的模型拟合度会较差，能够较好的反应数据的真实情况，统计量会变得比较可靠；反之，
                  拟合效果会较好，但是不能较好的反应数据的真实情况，模型数据的独立性被削弱，关联度增加。"""
        return self._edf

    @property
    def effective_number(self):
        """float: 地理加权回归结果汇总中的有效的参数数量。反映了估计值的方差与系数估计值的偏差之间的折衷，该值与带宽的选择有关，
                  可用来计算多个诊断测量值。对于较大的带宽，系数的有效数量将接近实际参数数量，局部系数估计值将具有较小的方差，
                  但是偏差将会非常大;对于较小的带宽，系数的有效数量将接近观测值的数量，局部系数估计值将具有较大的方差，但是偏
                  差将会变小。"""
        return self._effective_number

    @property
    def neighbours(self):
        """int: 地理加权回归结果汇总中的相邻数目。

                 * 用于各个局部估计的相邻数目，它控制模型中的平滑程度。通常，你可以选择默认的相邻点值，方法是：设置带宽确定方式(kernel_type)
                   方法选择 :py:attr:`.BandWidthType.AICC` 或 :py:attr:`.BandWidthType.CV`，这两个选项都将尝试识别最佳自适应相邻点数目。

                 * 由于"最佳"条件对于 AIC 和 CV 并不相同，都会得到相对的最优 AICc 值和 CV 值，因而通常会获得不同的最佳值。

                 * 可以通过设置带宽类型（kernel_type）方法提供精确的自适应相邻点数目。

                """
        return self._neighbours

    @property
    def R2(self):
        """float: 地理加权回归结果汇总中的判定系数（R2）。判定系数是拟合度的一种度量，其值在0.0和1.0范围内变化，值越大模型越好。
                 此值可解释为回归模型所涵盖的因变量方差的比例。R2计算的分母为因变量值的平方和，添加一个解释变量不会更改分母但是
                 会更改分子，这将出现改善模型拟合的情况，但是也可能假象。"""
        return self._r2

    @property
    def R2_adjusted(self):
        """float: 地理加权回归结果汇总中的校正的判定系数。校正的判定系数的计算将按分子和分母的自由度对它们进行正规化。这具有对
                  模型中变量数进行补偿的效果，由于校正的R2值通常小于R2值。但是，执行校正时，无法将该值的解释作为所解释方差的比例。
                  自由度的有效值是带宽的函数，因此，AICc是对模型进行比较的首选方式。"""
        return self._r2_adjusted

    @property
    def residual_squares(self):
        """float: 地理加权回归结果汇总中的残差平方和。残差平方和为实际值与估计值（或拟合值）的平方之和。此测量值越小，模型越
                  拟合观测数据，即拟合程度越好。"""
        return self._residual_squares

    @property
    def sigma(self):
        """float: 地理加权回归结果汇总中的残差估计标准差。残差的估计标准差，为剩余平方和除以残差的有效自由度的平方根。此统计值
                  越小，模型拟合效果越好。"""
        return self._sigma


def GWR(source, explanatory_fields, model_field, kernel_function='GAUSSIAN', band_width_type='AICC', distance_tolerance=0.0, kernel_type='FIXED', neighbors=2, out_data=None, out_dataset_name=None, progress=None):
    """
    空间关系建模介绍：

     * 用户可以通过空间关系建模来解决以下问题：

       * 为什么某一现象会持续的发生,是什么因素导致了这种情况？
       * 导致某一事故发生率比预期的要高的因素有那些？有没有什么方法来减少整个城市或特定区域内的事故发生率？
       * 对某种现象建模以预测其他地点或者其他时间的数值？

     * 通过回归分析，你可以对空间关系进行建模、检查和研究，可以帮助你解释所观测到的空间模型后的诸多因素。比如线性关系是正或者
       是负；对于正向关系，即存在正相关性，某一变量随着另一个变量增加而增加；反之，某一变量随着另一个变量增加而减小；或者两个变量无关系。

    地理加权回归分析。

    * 地理加权回归分析结果信息包含一个结果数据集和地理加权回归结果汇总（请参阅 GWRSummary 类）。
    * 结果数据集包含交叉验证（CVScore）、预测值（Predicted）、回归系数（Intercept、C1_解释字段名）、残差（Residual）、标准误
      （StdError)、系数标准误(SE_Intercept、SE1_解释字段名）、伪t值（TV_Intercept、TV1_解释字段名）和Studentised残差（StdResidual）等。

    说明：

      * 地理加权回归分析是一种用于空间变化关系的线性回归的局部形式,可用来在空间变化依赖和独立变量之间的关系研究。对地理要素所
        关联的数据变量之间的关系进行建模，从而可以对未知值进行预测或者更好地理解可对要建模的变量产生影响的关键因素。回归方法使
        你可以对空间关系进行验证并衡量空间关系的稳固性。
      * 交叉验证（CVScore）：交叉验证在回归系数估计时不包括回归点本身即只根据回归点周围的数据点进行回归计算。该值就是每个回归
        点在交叉验证中得到的估计值与实际值之差，它们的平方和为CV值。作为一个模型性能指标。
      * 预测值（Predicted）：这些值是地理加权回归得到的估计值（或拟合值）。
      * 回归系数（Intercept）：它是地理加权回归模型的回归系数，为回归模型的回归截距，表示所有解释变量均为零时因变量的预测值。
      * 回归系数（C1_解释字段名）：它是解释字段的回归系数，表示解释变量与因变量之间的关系强度和类型。如果回归系数为正，则解释
        变量与因变量之间的关系为正向的；反之，则存在负向关系。如果关系很强，则回归系数也相对较大；关系较弱时，则回归系数接近于0。
      * 残差(Residual)：这些是因变量无法解释的部分，是估计值和实际值之差，标准化残差的平均值为0，标准差为1。残差可用于确定模
        型的拟合程度，残差较小表明模型拟合效果较好，可以解释大部分预测值，说明这个回归方程是有效的。
      * 标准误(StdError)：估计值的标准误差，用于衡量每个估计值的可靠性。较小的标准误表明拟合值与实际值的差异程度越小，模型拟合效果越好。
      * 系数标准误（SE_Intercept、SE1_解释字段名）:这些值用于衡量每个回归系数估计值的可靠性。系数的标准误差与实际系数相比较小
        时，估计值的可信度会更高。较大的标准误差可能表示存在局部多重共线性问题。
      * 伪t值(TV_Intercept、TV1_解释字段名)：是对各个回归系数的显著性检验。当T值大于临界值时，拒绝零假设，回归系数显著即回归系
        估计值是可靠的；当T值小于临界值时，则接受零假设，回归系数不显著。
      * Studentised残差（StdResidual）：残差和标准误的比值，该值可用来判断数据是否异常，若数据都在（-2，2）区间内，表明数据具
        有正态性和方差齐性；若数据超出（-2，2）区间，表明该数据为异常数据，无方差齐性和正态性。

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param explanatory_fields: 解释字段的名称的集合
    :type explanatory_fields: list[str] or str
    :param str model_field: 建模字段的名称
    :param kernel_function: 核函数类型
    :type kernel_function: KernelFunction or str
    :param band_width_type: 带宽确定方式
    :type band_width_type: BandWidthType or str
    :param float distance_tolerance: 带宽范围
    :param kernel_type: 带宽类型
    :type kernel_type: KernelType or str
    :param int neighbors: 相邻数目。只有当带宽类型设置为 :py:attr:`.KernelType.ADAPTIVE` 且宽确定方式设置为 :py:attr:`.BandWidthType.BANDWIDTH` 时有效。
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个两个元素的 tuple，tuple 的第一个元素为 :py:class:`.GWRSummary` ，第二个元素为地理加权回归结果数据集。
    :rtype: tuple[GWRSummary, DatasetVector]
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_gwr'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'geographic_weighted_regression')
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialRelModeling.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = get_jvm().com.supermap.analyst.spatialstatistics.GWRParameter()
            if explanatory_fields is not None:
                explanatory_fields = split_input_list_from_str(explanatory_fields)
                java_param.setExplanatoryFeilds(to_java_string_array(explanatory_fields))
            if model_field is not None:
                java_param.setModelFeild(str(model_field))
            if kernel_function is not None:
                java_param.setKernelFunction(oj(KernelFunction._make(kernel_function)))
            if kernel_type is not None:
                java_param.setKernelType(oj(KernelType._make(kernel_type)))
            if band_width_type is not None:
                java_param.setBandWidthType(oj(BandWidthType._make(band_width_type)))
            if distance_tolerance is not None:
                java_param.setDistanceTolerance(float(distance_tolerance))
            if neighbors is not None:
                java_param.setNeighbors(int(neighbors))
            gwr = get_jvm().com.supermap.analyst.spatialstatistics.SpatialRelModeling.geographicWeightedRegression
            java_result = gwroj(source_dt)oj(out_datasource)_outDatasetNamejava_param
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialstatistics.SpatialRelModeling.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    if java_result is None:
        if out_data is not None:
            try_close_output_datasource(None, out_datasource)
        return
    gwr_dt = out_datasource[java_result.getResultDataset().getName()]
    if out_data is not None:
        gwr_dt = try_close_output_datasource(gwr_dt, out_datasource)
    gwr_summary = GWRSummary._from_java_object(java_result.getGWRSummary())
    return (gwr_summary, gwr_dt)


def raster_mosaic(inputs, back_or_no_value, back_tolerance, join_method, join_pixel_format, cell_size, encode_type='NONE', valid_rect=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格数据集镶嵌。支持栅格数据集和影像数据集。

    栅格数据的镶嵌是指将两个或两个以上栅格数据按照地理坐标组成一个栅格数据。有时由于待研究分析的区域很大，或者感兴趣的目标对象
    分布很广，涉及到多个栅格数据集或者多幅影像，就需要进行镶嵌。下图展示了六幅相邻的栅格数据镶嵌为一幅数据。

    .. image:: ../image/Mosaic_1.png

    进行栅格数据镶嵌时，需要注意以下要点：

     * 待镶嵌栅格必须具有相同的坐标系
       镶嵌要求所有栅格数据集或影像数据集具有相同的坐标系，否则镶嵌结果可能出错。可以在镶嵌前通过投影转换统一所有带镶嵌栅格的
       坐标系。

     * 重叠区域的处理
       镶嵌时，经常会出现两幅或多幅栅格数据之间有重叠区域的情况（如下图，两幅影像在红色框内的区域是重叠的），此时需要指定对重
       叠区域栅格的取值方式。SuperMap 提供了五种重叠区域取值方式，使用者可根据实际需求选择适当的方式，详见 :py:class:`.RasterJoinType` 类。

       .. image:: ../image/Mosaic_2.png

     * 关于无值和背景色及其容限的说明
       待镶嵌的栅格数据有两种：栅格数据集和影像数据集。对于栅格数据集，该方法可以指定无值及无值的容限，对于影像数据集，该方法
       可以指定背景色及其容限。

       * 待镶嵌数据为栅格数据集:

          * 当待镶嵌的数据为栅格数据集时，栅格值为 back_or_no_value 参数所指定的值的单元格，以及在 back_tolerance 参数指定的容限范
            围内的单元格被视为无值，这些单元格不会参与镶嵌时的计算（叠加区域的计算），而栅格的原无值单元格则不再是无值数据从而参与运算。

          * 需要注意，无值的容限是用户指定的无值的值的容限，与栅格中原无值无关。

       * 待镶嵌数据为影像数据集

          * 当待镶嵌的数据为影像数据集时，栅格值为 back_or_no_value 参数所指定的值的单元格，以及在 back_tolerance 参数指定的容限
            范围内单元格被视为背景色，这些单元格不参与镶嵌时的计算。例如，指定无值的值为 a，指定的无值的容限为 b，则栅格值在
            [a-b,a+b] 范围内的单元格均不参与计算。

          * 注意，影像数据集中栅格值代表的是一个颜色。影像数据集的栅格值对应为 RGB 颜色，因此，如果想要将某种颜色设为背景色，
            为 back_or_no_value 参数指定的值应为将该颜色（RGB 值）转为 32 位整型之后的值，系统内部会根据像素格式再进行相应的转换。

          * 对于背景色的容限值的设置，与背景色的值的指定方式相同：该容限值为一个 32 位整型值，在系统内部被转换为对应背景色
            R、G、B 的三个容限值，例如，指定为背景色的颜色为 (100,200,60)，指定的容限值为 329738，该值对应的 RGB 值为
            (10,8,5)，则值在 (90,192,55) 和 (110,208,65) 之间的颜色均被视为背景色，不参与计算。

    注意：

    将两个或以上高像素格式的栅格镶嵌成低像素格式的栅格时，结果栅格值可能超出值域，导致错误，因此不建议进行此种操作。

    :param inputs: 指定的待镶嵌的数据集的集合。
    :type inputs: list[Dataset] or list[str] or str
    :param back_or_no_value: 指定的栅格背景颜色或无值的值。可以使用一个 float 或 tuple 表示一个 RGB 或 RGBA 值
    :type back_or_no_value: float or tuple
    :param back_tolerance: 指定的栅格背景颜色或无值的容限。可以使用一个 float 或 tuple 表示一个 RGB 或 RGBA 值
    :type back_tolerance: float or tuple
    :param join_method: 指定的镶嵌方法，即镶嵌时重叠区域的取值方式。
    :type join_method: RasterJoinType or str
    :param join_pixel_format: 指定的镶嵌结果栅格数据的像素格式。
    :type join_pixel_format: RasterJoinPixelFormat or str
    :param float cell_size: 指定的镶嵌结果数据集的单元格大小。
    :param encode_type: 指定的镶嵌结果数据集的编码方式。
    :type encode_type: EncodeType or str
    :param valid_rect: 指定的镶嵌结果数据集的有效范围。
    :type valid_rect: Rectangle
    :param out_data: 指定的用于存储镶嵌结果数据集的数据源信息
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 指定的镶嵌结果数据集的名称。
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 镶嵌结果数据集
    :rtype: Dataset
    """
    check_lic()
    datasets = []
    if isinstance(inputs, (list, tuple)):
        for i in range(len(inputs)):
            item = inputs[i]
            temp = get_input_dataset(item)
            if temp is not None:
                if isinstance(temp, (DatasetGrid, DatasetImage)):
                    datasets.append(temp)
                else:
                    raise ValueError('Only support DatasetGrid or DatasetImage')
            else:
                raise ValueError('input_data item is None' + str(item))

    else:
        temp = get_input_dataset(inputs)
        if temp is not None:
            if isinstance(temp, (DatasetGrid, DatasetImage)):
                datasets.append(temp)
            else:
                raise ValueError('Only support DatasetGrid or DatasetImage')
        else:
            raise ValueError('input_data item is None' + str(inputs))
    if len(datasets) == 0:
        raise ValueError('hava no valid source datasets')
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = datasets[0].datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = datasets[0].name + '_mosaic'
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        if join_method is not None:
            java_join_method = oj(RasterJoinType._make(join_method))
        else:
            java_join_method = oj(RasterJoinType.RJMFIRST)
        if join_pixel_format is not None:
            java_join_pixel_format = oj(RasterJoinPixelFormat._make(join_pixel_format))
        else:
            java_join_pixel_format = oj(RasterJoinPixelFormat.RJPMAX)
        if encode_type is not None:
            java_encode_type = oj(EncodeType._make(encode_type))
        else:
            java_encode_type = oj(EncodeType.NONE)
        if valid_rect is None:
            valid_rect = Rectangle.make((0, 0, 0, 0))
        elif back_or_no_value is not None:
            if isinstance(back_or_no_value, tuple):
                back_or_no_value = tuple_to_color(back_or_no_value)
            else:
                back_or_no_value = -9999
            if back_tolerance is not None:
                if isinstance(back_tolerance, tuple):
                    back_tolerance = tuple_to_color(back_tolerance)
        else:
            back_tolerance = 0.0
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'raster_mosaic')
                        get_jvm().com.supermap.analyst.spatialanalyst.RasterMosaic.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = get_jvm().com.supermap.analyst.spatialanalyst.RasterMosaic.mosaic(to_java_dataset_array(datasets), float(back_or_no_value), float(back_tolerance), java_join_method, java_join_pixel_format, float(cell_size), java_encode_type, oj(valid_rect), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.RasterMosaic.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class OLSSummary:
    __doc__ = '\n    普通最小二乘法结果汇总类。该类给出了普通最小二乘法分析的结果汇总，例如分布统计量、统计量概率、AICc和判定系数等。\n    '

    def __init__(self, java_object):
        self._java_object = java_object

    @property
    def AIC(self):
        """float: 普通最小二乘法结果汇总中的AIC。与AICc类似，是衡量模型拟合优良性的一种标准，可以权衡所估计模型的复杂度和模型拟合数
        据的优良性，在评价模型时是兼顾了简洁性和精确性。表明增加自由参数的数目提高了拟合的优良性，AIC鼓励数据的拟合性，但是应尽量避
        免出现过度拟合的情况。所以优先考虑AIC值较小的，是寻找可以最好的解释数据但包含最少自由参数的模型"""
        return self._java_object.getAIC()

    @property
    def AICc(self):
        """float: 普通最小二乘法结果汇总中的AICc。当数据增加时，AICc收敛为AIC，也是模型性能的一种度量，有助与比较不同的回归模型。
        考虑到模型复杂性，具有较低AICc值的模型将更好的拟合观测数据。AICc不是拟合度的绝对度量，但对于比较用于同一因变量且具有不同解
        释变量的模型非常有用。如果两个模型的AICc值相差大于3，具有较低AICc值的模型将视为更佳的模型。"""
        return self._java_object.getAICc()

    @property
    def coefficient(self):
        """list[float]: 普通最小二乘法结果汇总中的系数。 系数表示解释变量和因变量之间的关系和类型。"""
        return self._java_object.getCoefficient()

    @property
    def coefficient_std(self):
        """list[float]: 普通最小二乘法结果汇总中的系数标准差"""
        return self._java_object.getCoefficientStd()

    @property
    def F_dof(self):
        """int: 普通最小二乘法结果汇总中的联合F统计量自由度。 """
        return self._java_object.getFDof()

    @property
    def F_probability(self):
        """float: 普通最小二乘法结果汇总中的联合F统计量的概率。 """
        return self._java_object.getFProbability()

    @property
    def f_statistic(self):
        """float: 普通最小二乘法结果汇总中的联合F统计量。联合F统计量用于检验整个模型的统计显著性。只有在Koenker（Breusch-Pagan）
        统计量不具有统计显著性时,联合F统计量才可信。检验的零假设为模型中的解释变量不起作用。对于大小为95%的置信度,联合F统计量概率小
        于0.05表示模型具有统计显著性。"""
        return self._java_object.getFStatistic()

    @property
    def JB_dof(self):
        """int: 普通最小二乘法结果汇总中的Jarque-Bera统计量自由度。 """
        return self._java_object.getJBDof()

    @property
    def JB_probability(self):
        """float: 普通最小二乘法结果汇总中的Jarque-Bera统计量的概率"""
        return self._java_object.getJBProbability()

    @property
    def JB_statistic(self):
        """float: 普通最小二乘法结果汇总中的Jarque-Bera统计量。Jarque-Bera统计量能评估模型的偏差，用于指示残差是否呈正态分布。检
        验的零假设为残差呈正态分布。对于大小为95%的置信度,联合F统计量概率小于0.05表示模型具有统计显著性,回归不会呈正态分布,模型有
        偏差。"""
        return self._java_object.getJBStatistic()

    @property
    def KBP_dof(self):
        """int: 普通最小二乘法结果汇总中的Koenker（Breusch-Pagan）统计量自由度。 """
        return self._java_object.getKBPDof()

    @property
    def KBP_probability(self):
        """float: 普通最小二乘法结果汇总中的Koenker（Breusch-Pagan）统计量的概率"""
        return self._java_object.getKBPProbability()

    @property
    def KBP_statistic(self):
        """float: 普通最小二乘法结果汇总中的Koenker（Breusch-Pagan）统计量。Koenker（Breusch-Pagan）统计量能评估模型的稳态，用
        于确定模型的解释变量是否在地理空间和数据空间中都与因变量具有一致的关系。检验的零假设为检验的模型是稳态的。对于大小为95%的
        置信度,联合F统计量概率小于0.05表示模型具有统计显著异方差性或非稳态。当检验结果具有显著性时，则需要参考稳健系数标准差和
        概率来评估每个解释变量的效果。"""
        return self._java_object.getKBPStatistic()

    @property
    def probability(self):
        """list[float]: 普通最小二乘法结果汇总中的t分布统计量概率"""
        return self._java_object.getProbability()

    @property
    def R2(self):
        """float: 普通最小二乘法结果汇总中的判定系数（R2）。"""
        return self._java_object.getR2()

    @property
    def R2_adjusted(self):
        """float: 普通最小二乘法结果汇总中的校正的判定系数"""
        return self._java_object.getR2Adjusted()

    @property
    def robust_Pr(self):
        """list[float]: 普通最小二乘法结果汇总中的稳健系数概率。"""
        return self._java_object.getRobust_Pr()

    @property
    def robust_SE(self):
        """list[float]: 获取普通最小二乘法结果汇总中的稳健系数标准差。"""
        return self._java_object.getRobust_SE()

    @property
    def robust_t(self):
        """list[float]: 普通最小二乘法结果汇总中的稳健系数t分布统计量。"""
        return self._java_object.getRobust_t()

    @property
    def sigma2(self):
        """float: 普通最小二乘法结果汇总中的残差方差。"""
        return self._java_object.getSigma2()

    @property
    def std_error(self):
        """list[float]: 普通最小二乘法结果汇总中的标准误差。"""
        return self._java_object.getStdError()

    @property
    def t_statistic(self):
        """list[float]: 普通最小二乘法结果汇总中的t分布统计量。"""
        return self._java_object.gett_Statistic()

    @property
    def variable(self):
        """list[float]: 普通最小二乘法结果汇总中的变量数组"""
        return self._java_object.getVariable()

    @property
    def VIF(self):
        """list[float]: 普通最小二乘法结果汇总中的方差膨胀因子"""
        return self._java_object.getVIF()

    @property
    def wald_dof(self):
        """int: 普通最小二乘法结果汇总中的联合卡方统计量自由度"""
        return self._java_object.getWaldDof()

    @property
    def wald_probability(self):
        """float: 普通最小二乘法结果汇总中的联合卡方统计量的概率"""
        return self._java_object.getWaldProbability()

    @property
    def wald_statistic(self):
        """float: 普通最小二乘法结果汇总中的联合卡方统计量。联合卡方统计量用于检验整个模型的统计显著性。只有在
         Koenker（Breusch-Pagan）统计量具有统计显著性时,联合F统计量才可信。检验的零假设为模型中的解释变量不起作用。对于大小为
         95%的置信度,联合F统计量概率小于0.05表示模型具有统计显著性。 """
        return self._java_object.getWaldStatistic()


def ordinary_least_squares(input_data, explanatory_fields, model_field, out_data=None, out_dataset_name=None, progress=None):
    """
    普通最小二乘法。
    普通最小二乘法分析结果信息包含一个结果数据集和普通最小二乘法结果汇总。
    结果数据集包含预测值（Estimated）、残差（Residual）、标准化残差（StdResid）等。

    说明：

    - 预测值（Estimated）：这些值是普通最小二乘法得到的估计值（或拟合值）。
    - 残差（Residual）：这些是因变量无法解释的部分，是估计值和实际值之差，标准化残差的平均值为0，标准差为1。残差可用于确定模型的拟合程度，残差较小表明模型拟合效果较好，可以解释大部分预测值，说明这个回归方程是有效的。
    - 标准化残差（StdResid）：残差和标准误的比值，该值可用来判断数据是否异常，若数据都在（-2，2）区间内，表明数据具有正态性和方差齐性；若数据超出（-2，2）区间，表明该数据为异常数据，无方差齐性和正态性。

    :param input_data: 指定的待计算的数据集。可以为点、线、面数据集。
    :type input_data: DatasetVector or str
    :param explanatory_fields: 解释字段的名称的集合
    :type explanatory_fields: list[str] or str
    :param model_field: 建模字段的名称
    :type model_field: str
    :param out_data: 指定的用于存储结果数据集的数据源。
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集名称
    :type out_dataset_name: str
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个元组，元组的第一个元素为最小二乘法结果数据集或数据集名称，第二个元素为最小二乘法结果汇总
    :rtype: tuple[DatasetVector, OLSSummary] or tuple[str, OLSSummary]
    """
    check_lic()
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(input_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_OLS'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    _jvm = get_jvm()
    ols_parameter = _jvm.com.supermap.analyst.spatialstatistics.OLSParameter()
    ols_parameter.setExplanatoryFields(to_java_string_array(split_input_list_from_str(explanatory_fields)))
    ols_parameter.setModelField(model_field)
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'ordinary_least_squares')
                        _jvm.com.supermap.analyst.spatialstatistics.SpatialRelModeling.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            ordinaryLeastSquares = _jvm.com.supermap.analyst.spatialstatistics.SpatialRelModeling.ordinaryLeastSquares
            java_result = ordinaryLeastSquaresoj(source_dt)oj(out_datasource)_outDatasetNameols_parameter
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialstatistics.SpatialRelModeling.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getResultDataset().getName()]
        else:
            result_dt = None
        if out_data is not None:
            result_dt = try_close_output_datasource(result_dt, out_datasource)
        if java_result is not None:
            return (
             result_dt, OLSSummary(java_result.getOLSSummary()))
        return


def NDVI(input_data, nir_index, red_index, out_data=None, out_dataset_name=None):
    """
    归一化植被指数，也叫做归一化差分植被指数或者标准差异植被指数或生物量指标变化。可使植被从水和土中分离出来。

    :param input_data: 多波段影像数据集。
    :type input_data: DatasetImage or str
    :param int nir_index: 近红外波段的索引
    :param int red_index: 红波段的索引
    :param out_data: 结果数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果数据集，用于保存NDVI值。NDVI值的范围在-1到1之间。
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, DatasetImage):
        raise ValueError('source required DatasetImage, but is ' + str(type(input_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_NDVI'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            NDVI = get_jvm().com.supermap.analyst.spatialanalyst.ImageAnalyst.NDVI
            java_result = NDVI(oj(source_dt), int(nir_index), int(red_index), _outDatasetName, oj(out_datasource))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def NDWI(input_data, nir_index, green_index, out_data=None, out_dataset_name=None):
    """
    归一化水指数。NDWI一般用来提取影像中的水体信息，效果较好.

    :param input_data: 多波段影像数据集。
    :type input_data: DatasetImage or str
    :param int nir_index: 近红外波段的索引
    :param int green_index: 绿波段的索引
    :param out_data: 结果数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果数据集，用于保存NDWI值。
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, DatasetImage):
        raise ValueError('source required DatasetImage, but is ' + str(type(input_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + '_NDWI'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            NDWI = get_jvm().com.supermap.analyst.spatialanalyst.ImageAnalyst.NDWI
            java_result = NDWI(oj(source_dt), int(nir_index), int(green_index), _outDatasetName, oj(out_datasource))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def compute_features_envelope(input_data, is_single_part=True, out_data=None, out_dataset_name=None, progress=None):
    """
    计算几何对象的矩形范围面

    :param input_data: 待分析的数据集，仅支持线数据集和面数据集。
    :type input_data: DatasetVector or str
    :param bool is_single_part: 有组合线或者组合面时，是否拆分子对象。默认为 True，拆分子对象。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集，返回每个对象的范围面。结果数据集中新增了字段"ORIG_FID"用于保存输入对象的ID值。
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError('source input_data must be DatasetVector')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = _source_input.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_envelope'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'compute_features_envelope')
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.Generalization.featureEnvelope(oj(_source_input), _outDatasetName, oj(out_datasource), bool(is_single_part))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def calculate_view_shed(input_data, view_point, start_angle, view_angle, view_radius, out_data=None, out_dataset_name=None, progress=None):
    """
    单点可视域分析，即分析单个观察点的可视范围。
    单点可视域分析是在栅格表面数据集上，对于给定的一个观察点，查找其在给定的范围内（由观察半径、观察角度决定）所能观察到的区域，也就是给定点的通视区域范围。分析的结果为一个栅格数据集，其中可视区域保持原始栅格表面的栅格值，其他区域为无值。

    如下图所示，图中绿色的点为观察点，叠加在原始栅格表面上的蓝色区域即为对其进行可视域分析的结果。

    .. image:: ../image/CalculateViewShed.png

    注意：如果指定的观察点的高程小于当前栅格表面对应位置的高程值，则观察点的高程值将被自动设置为当前栅格表面的对应位置的高程。

    :param input_data: 指定的用于可视域分析的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param Point3D view_point: 指定的观察点位置。
    :param float start_angle: 指定的起始观察角度，单位为度，以正北方向为 0 度，顺时针方向旋转。指定为负值或大于 360 度，将自动换算到 0 到 360 度范围内。
    :param float view_angle:  指定的观察角度，单位为度，最大值为 360 度。观察角度基于起始角度，即观察角度范围为 [起始角度，起始角度+观察角度]。例如起始角度为 90 度，观察角度为 90 度，那么实际观察的角度范围是从 90 度到 180 度。但注意，当指定为 0 或负值时，无论起始角度为何值，观察角度范围都为 0 到 360 度
    :param float view_radius: 指定的观察半径。该值限制了视野范围的大小，若观测半径小于等于 0 时，表示无限制。单位为米
    :param out_data: 指定的用于存储结果数据集的数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 指定的结果数据集的名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 单点可视域分析结果数据集
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    else:
        view_point = Point3D.make(view_point)
        if not isinstance(view_point, Point3D):
            raise ValueError('view_point must be Point3D')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = _source_input.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_ViewShed'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'calculate_view_shed')
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.calculateViewShed(oj(_source_input), oj(view_point), float(start_angle), float(view_angle), float(view_radius), oj(out_datasource), _outDatasetName)
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def calculate_view_sheds(input_data, view_points, start_angles, view_angles, view_radiuses, view_shed_type, out_data=None, out_dataset_name=None, progress=None):
    """
    多点可视域分析，即分析多个观察点的可视范围，可以为共同可视域或非共同可视域。
    多点可视域分析，是根据栅格表面，对给定的观察点集合中每一个观察点进行可视域分析，然后根据指定的可视域类型，计算所有观察点的可视域的交集（称为“共同可视域”）或者并集（称为“非共同可视域”），并将结果输出到一个栅格数据集中，其中可视区域保持原始栅格表面的栅格值，其他区域为无值。

    如下图所示，图中绿色的点为观察点，叠加在原始栅格表面上的蓝色区域即为对其进行可视域分析的结果。左图展示了三个观察点的共同可视域，右图则是三个观察点的非共同可视域。

    .. image:: ../image/CalculateViewShed_1.png

    注意：如果指定的观察点的高程小于当前栅格表面对应位置的高程值，则观察点的高程值将被自动设置为当前栅格表面的对应位置的高程。

    :param input_data: 指定的用于可视域分析的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param view_points: 指定的观察点集合。
    :type view_points: list[Point3D]
    :param start_angles:  指定的起始观察角度集合，与观察点一一对应。单位为度，以正北方向为 0 度，顺时针方向旋转。指定为负值或大于 360 度，将自动换算到 0 到 360 度范围内。
    :type start_angles: list[float]
    :param view_angles: 指定的观察角度集合，与观察点和起始观察角度一一对应，单位为度，最大值为 360 度。观察角度基于起始角度，即观察角度范围为 [起始角度，起始角度+观察角度]。例如起始角度为 90 度，观察角度为 90 度，那么实际观察的角度范围是从 90 度到 180 度。    :type view_angles: list[float]
    :param view_radiuses: 指定的观察半径集合，与观察点一一对应。该值限制了视野范围的大小，若观测半径小于等于 0 时，表示无限制。单位为米。
    :type view_radiuses: list[float]
    :param view_shed_type: 指定的可视域的类型，可以是多个观察点的可视域的交集，也可以是多个观察点可视域的并集。
    :type view_shed_type: ViewShedType or str
    :param out_data: 指定的用于存储结果数据集的数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 指定的结果数据集的名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 多点可视域分析结果数据集。
    :rtype: DatasetGrid
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    if not isinstance(view_points, (list, tuple)):
        raise ValueError('view_points must be list or tuple')
    else:
        view_points = [Point3D.make(p) for p in view_points]
        if len(view_points) != len(start_angles) != len(view_angles) != len(view_radiuses):
            raise ValueError('The length of view_points, start_angles, view_angles and view_radius must be equal.')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = _source_input.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + '_ViewShed'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    view_shed_type = ViewShedType._make(view_shed_type)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'calculate_view_sheds')
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.calculateViewShedoj(_source_input)to_java_point3ds(view_points)to_java_double_array(start_angles)to_java_double_array(view_angles)to_java_double_array(view_radiuses)oj(out_datasource)_outDatasetNameoj(view_shed_type)
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class VisibleResult:
    __doc__ = '\n    可视性分析结果类。\n\n    该类给出了观察点与被观察点之间可视分析的结果，如果不可视的话，还会给出障碍点的相关信息。\n    '

    def __init__(self, java_object):
        self._java_object = java_object

    @property
    def barrier_alter_height(self):
        """float: 障碍点建议修改的最大高度值。若将障碍点所在栅格表面的单元格的栅格值（即高程）修改为小于或等于该值，则该点不再阻碍
        视线，但注意，并不表示该点之后不存在其他障碍点。可通过 DatasetGrid 类的 set_value() 方法修改栅格值"""
        return self._java_object.getBarrierAlterHeight()

    @property
    def barrier_point(self):
        """Point3D: 障碍点的坐标值。如果观察点与被观察点之间不可视，则该方法的返回值为观察点与被观察点之间的第一个障碍点。如果观察
        点与被观察点之间可视时，障碍点坐标取默认值。 """
        return Point3D._from_java_object(self._java_object.getBarrierPoint())

    @property
    def from_point_index(self):
        """int: 观察点的索引值。如果是两点之间进行可视性分析，则观察点的索引值为 0。"""
        return self._java_object.getFromPointIndex()

    @property
    def to_point_index(self):
        """int: 被观察点的索引值。如果是两点之间进行可视性分析，则被观察点的索引值为 0。 """
        return self._java_object.getToPointIndex()

    @property
    def visible(self):
        """bool: 观察点与被观察点对之间是否可视"""
        return self._java_object.getVisible()


def is_point_visible(input_data, from_point, to_point):
    """
    两点可视性分析，即判断两点之间是否相互可见。
    基于栅格表面，判断给定的观察点与被观察点之间是否可见，称为两点间可视性分析。两点间可视性分析的结果有两种：可视与不可视。该方法返
    回一个 VisibleResult 对象，该对象用于返回两点间可视性分析的结果，即两点是否可视，如果不可视，会返回第一个阻碍视线的障碍点，还会
    给出该障碍点的建议高程值以使该点不再阻碍视线。

    :param input_data: 指定的用于可视性分析的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param from_point: 指定的用于可视性分析的起始点，即观察点
    :type from_point: Point3D
    :param to_point: 指定的用于可视性分析的终止点，即被观察点。
    :type to_point: Point3D
    :return: 可视性分析的结果
    :rtype: VisibleResult
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    _jvm = get_jvm()
    from_point = Point3D.make(from_point)
    to_point = Point3D.make(to_point)
    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.isVisible(oj(_source_input), oj(from_point), oj(to_point))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        return

    if java_result is not None:
        return VisibleResult(java_result)


def are_points_visible(input_data, from_points, to_points):
    """
    多点可视性分析，即判断多点之间是否可两两通视。
    多点可视性分析，是根据栅格表面，计算观察点与被观察点之间是否两两通视。两点间可视性分析请参阅另一重载方法 isVisible 方法的介绍。

    如果有 m 个观测点和 n 个被观测点，将有 m * n 种观测组合。分析的结果通过一个 VisibleResult 对象数组返回，每个 VisibleResult
    对象包括对应的两点是否可视，如果不可视，会给出第一个障碍点，以及该点的建议高程值以使该点不再阻碍视线。

    注意：如果指定的观察点的高程小于当前栅格表面对应位置的高程值，则观察点的高程值将被自动设置为当前栅格表面的对应位置的高程。

    :param input_data: 指定的用于可视性分析的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param from_points: 指定的用于可视性分析的起始点，即观察点
    :type from_points: list[Point3D]
    :param to_points: 指定的用于可视性分析的终止点，即被观察点。
    :type to_points: list[Point3D]
    :return: 可视性分析的结果
    :rtype: list[VisibleResult]
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    _jvm = get_jvm()
    from_points = to_java_point3ds([Point3D.make(p) for p in from_points])
    to_points = to_java_point3ds([Point3D.make(p) for p in to_points])
    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.isVisible(oj(_source_input), from_points, to_points)
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        return

    if java_result is not None:
        return [VisibleResult(item) for item in java_result]


def line_of_sight(input_data, from_point, to_point):
    """
    计算两点间的通视线，即根据地形计算观察点到目标点的视线上的可视部分和不可视部分。
    依据地形的起伏，计算从观察点看向目标点的视线上哪些段可视或不可视，称为计算两点间的通视线。观察点与目标点间的这条线称为通视线。
    通视线可以帮助了解在给定点能够看到哪些位置，可服务于旅游线路规划、雷达站或信号发射站的选址，以及布设阵地、观察哨所设置等军事活动。

    .. image:: ../image/LineOfSight.png

    观察点和目标点的高程由其 Z 值确定。当观察点或目标点的 Z 值小于栅格表面上对应单元格的高程值时，则使用该单元格的栅格值作为观察点或
    目标点的高程来计算通视线。

    计算两点间通视线的结果为一个二维线对象数组，该数组的第 0 个元素为可视线对象，第 1 个元素为不可视线对象。该数组的长度可能为 1 或
     2，这是因为不可视线对象有可能不存在，此时结果数组只包含一个对象，即可视线对象。由于可视线（或不可视线）可能不连续，因此可视线或
     不可视线对象有可能是复杂线对象。

    :param input_data: 指定的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param from_point: 指定的观察点，是一个三维点对象。
    :type from_point: Point3D
    :param to_point: 指定的目标点，是一个三维点对象。
    :type to_point: Point3D
    :return: 结果通视线，是一个二维线数组
    :rtype: list[GeoLine]
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError('source input_data is None')
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError('source input_data must be DatasetGrid')
    _jvm = get_jvm()
    from_point = Point3D.make(from_point)
    to_point = Point3D.make(to_point)
    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.lineOfSight(oj(_source_input), oj(from_point), oj(to_point))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        return

    if java_result is not None:
        return [Geometry._from_java_object(item) for item in java_result]


def radar_shield_angle(input_data, view_point, start_angle, end_angle, view_radius, interval, out_data=None, out_dataset_name=None, progress=None):
    """
    根据地形图和雷达中心点，返回各方位上最大的雷达遮蔽角的点数据集。方位角是顺时针与正北方向的夹角。

    :param input_data:  删格数据集或DEM
    :type input_data: DatasetGrid or str or list[DatasetGrid] or list[str]
    :param view_point: 三维点对象，表示雷达中心点的坐标和雷达中心与地面的高度。
    :type view_point: Point3D
    :param float start_angle: 雷达方位起始角度,单位为度,以正北方向为 0 度,顺时针方向旋转。范围为0到360度。如果设置为小于0，默认值
                              为0；如果该值大于360，默认为360。
    :param float end_angle: 雷达方位终止角度，单位为度，最大值为 360 度。观察角度基于起始角度，即观察角度范围为 [起始角度，终止角度)。
                            该值必须大于起始角度。如果该值小于等于0,表示[0,360)。
    :param float view_radius: 观察范围，单位为米。如果设置为小于0，表示整个地形图范围。
    :param float interval: 方位角的间隔，即每隔多少度返回一个雷达遮蔽点。该值必须大于0且小于360。
    :param out_data: 目标数据源。
    :type out_data: Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress:  进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: funtion
    :return: 返回的三维点数据集,Z代表该点所在位置的地形高度。该数据集记录了每个方位上雷达遮蔽角最大的点,并增加了字段"ShieldAngle"、
             "ShieldPosition"和"RadarDistance"分别记录了雷达遮蔽角、该点与正北方向的夹角和点与雷达中心的距离。
    :rtype: DatasetVector or str
    """
    check_lic()
    inputs = []
    if isinstance(input_data, (list, tuple)):
        for item in input_data:
            inputs.append(get_input_dataset(item))

    else:
        inputs.append(get_input_dataset(input_data))
    inputs = list(filter(lambda x: isinstance(x, DatasetGrid), inputs))
    if len(inputs) == 0:
        raise ValueError('source input_data must be DatasetGrid or list[DatasetGrid]')
    else:
        view_point = Point3D.make(view_point)
        if not isinstance(view_point, Point3D):
            raise ValueError('view_point must be Point3D')
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = inputs[0].datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = inputs[0].name + '_radarShield'
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, 'radar_shield_angle')
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            if len(inputs) == 1:
                java_dt = oj(inputs[0])
            else:
                java_dt = to_java_datasetgrid_array(inputs)
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.radarShieldAnglejava_dtoj(view_point)float(start_angle)float(end_angle)float(view_radius)oj(out_datasource)_outDatasetNamefloat(interval)
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def geographical_detector(input_data, model_field, explanatory_fields, is_factor_detector=True, is_ecological_detector=True, is_interaction_detector=True, is_risk_detector=True, progress=None):
    """
    对数据进行地理探测器分析，并返回地理探测器的结果。
    地理探测器返回的结果包括因子探测器，生态探测器，交互探测器，风险探测器的分析结果

    地理探测器是探测空间分异性，以及揭示其背后驱动力的一组统计学方法。其核心思想是基于这样的假设：如果某个自变量对某个因变量有重要影
    响,那么自变量和因变量的空间分布应该具有相似性。地理分异既可以用分类算法来表达，例如环境遥感分类，也可以根据经验确定，例如胡焕庸线。
    地理探测器擅长分析类型量,而对于顺序量、比值量或间隔量,只要进行适当的离散化,也可以利用地理探测器对其进行统计分析。
    因此,地理探测器既可以探测数值型数据，也可以探测定性数据，这正是地理探测器的一大优势。地理探测器的另一个独特优势是探测两因子交互
    作用于因变量。交互作用一般的识别方法是在回归模型中增加两因子的乘积项，检验其统计显著性。然而,两因子交互作用不一定就是相乘关系。
    地理探测器通过分别计算和比较各单因子 q 值及两因子叠加后的 q 值，可以判断两因子是否存在交互作用，以及交互作用的强弱、方向、线性还是
    非线性等。两因子叠加既包括相乘关系，也包括其他关系，只要有关系，就能检验出来。

    :param input_data: 待计算的矢量数据集
    :type input_data: DatasetVector or str
    :param str model_field: 建模字段
    :param explanatory_fields: 解释变量数组
    :type explanatory_fields: list[str] or str
    :param bool is_factor_detector: 是否计算因子探测器
    :param bool is_ecological_detector: 是否计算生态探测器
    :param bool  is_interaction_detector: 是否计算交互探测器
    :param bool is_risk_detector: 是否进行风险探测器
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 地理探测器结果
    :rtype: GeographicalDetectorResult
    """
    check_lic()
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError('source required DatasetVector, but is ' + str(type(input_data)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, 'geographical_detector')
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            geographicalDetector = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.geographicalDetector
            java_result = geographicalDetector(oj(source_dt), str(model_field), to_java_string_array(split_input_list_from_str(explanatory_fields)), bool(is_factor_detector), bool(is_ecological_detector), bool(is_interaction_detector), bool(is_risk_detector), None)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        result = GeographicalDetectorResult(java_result)
        del java_result
        return result


class InteractionDetectorResult:
    __doc__ = '\n    交互作用探测器分析结果，用于获取对数据进行交互作用探测器得到的分析结果，包括不同解释变量之间交互作用的描述以及分析结果矩阵。\n    用户不能创建此对象。\n    '

    def __init__(self, java_object):
        self._descriptions = java_object.getInteractionDescriptions()
        self._interaction_values = InteractionDetectorResult._get_interaction_detector_values(java_object)

    @staticmethod
    def _get_interaction_detector_values(java_object):
        detector_values = java_object.getInteractionDetectorValues()
        values = []
        for i in range(len(detector_values)):
            result_item = detector_values[i]
            values.append([
             result_item.getVariableRow(), result_item.getVariableCol(), result_item.getInteractionValue()])

        import pandas as pd
        return pd.DataFrame(values, columns=['VariableRow', 'VariableCol', 'InteractionValues'])

    @property
    def descriptions(self):
        """list[str]: 交互作用探测器结果描述。评估不同解释变量共同作用时是否会增加或减弱对因变量的解释力，或这些因子对因变量的影响
        是否相互独立，两个解释变量对因变量交互作用的类型包括：非线性减弱、单因子非线性减弱、双因子增强、独立及非线性增强。"""
        return self._descriptions

    @property
    def interaction_values(self):
        """pandas.DataFrame: 交互作用探测器分析结果值。"""
        return self._interaction_values


class RiskDetectorMean:
    __doc__ = '\n    风险探测器结果均值类，用于获取对数据进行风险区域探测器得到的不同解释变量字段的结果均值。\n    '

    def __init__(self, java_object):
        self._variable = java_object.getVariable()
        self._unique_values = java_object.getVariableUniqueValues()
        self._means = java_object.getMeans()

    @property
    def variable(self):
        """str: 风险探测器解释变量名称"""
        return self._variable

    @property
    def unique_values(self):
        """list[str]: 风险探测器解释变量字段唯一值"""
        return self._unique_values

    @property
    def means(self):
        """list[float]: 风险探测器分析结果均值"""
        return self._means


class RiskDetectorResult:
    __doc__ = '风险区探测器分析结果类，用于获取对数据进行风险区探测器得到的分析结果，包括结果均值、结果矩阵'

    def __init__(self, java_object):
        self._means = [RiskDetectorMean(item) for item in java_object.getRiskDetectorMeans()]
        self._values = [RiskDetectorResult._get_risk_detector_values(values) for values in java_object.getRiskDetectorValues()]

    @staticmethod
    def _get_risk_detector_values(detector_values):
        values = []
        for i in range(len(detector_values)):
            result_item = detector_values[i]
            values.append([
             result_item.getVariableRow(), result_item.getVariableCol(), result_item.getSig()])

        import pandas as pd
        return pd.DataFrame(values, columns=['VariableRow', 'VariableCol', 'Sig'])

    @property
    def means(self):
        """list[iobjectspy.RiskDetectorMean]: 风险区探测器结果均值"""
        return self._means

    @property
    def values(self):
        """list[pandas.DataFrame]: 风险探测器分析结果值"""
        return self._values


class GeographicalDetectorResult:
    __doc__ = '\n    地理探测器结果类，用于获取地理探测器计算的结果，包括因子探测器、生态探测器、交互作用探测器、风险探测器分析结果。\n    '

    def __init__(self, java_object):
        self._variables = java_object.getVariables()
        self._factor_detector_result = GeographicalDetectorResult._get_java_factor_detector_results(java_object)
        self._risk_detector_result = RiskDetectorResult(java_object.getRiskDetectorResult())
        self._interaction_detector_result = InteractionDetectorResult(java_object.getInteractionDetectorResult())
        self._ecological_detector_result = GeographicalDetectorResult._get_java_ecological_detector_result(java_object)

    @property
    def variables(self):
        """list[str]: 地理探测器解释变量"""
        return self._variables

    @property
    def factor_detector_result(self):
        """pandas.DataFrame: 因子探测器分析结果。探测Y的空间分异性，以及探测某因子 X 多大程度上解释了属性Y的空间分异。用 q 值度量.

                             .. image:: ../image/GeographicalDetectorQformula.png

                             q 的值域为[0,1]，值越大，说明 y 的空间分异越明显，如果分层是由自变量 X 生成的，则 q 值越大，表示 X 和 Y 的空间分布越一致，
                             自变量 X 对属性 Y 的解释力越强，反之则越弱。极端情况下，q 值为1表明在 X 的层内，Y的方差为0，即因子 X 完全控制了 Y 的空间分布，
                             q 值为0 则表明 Y 按照 X 分层后的方差和与 Y 不分层的方差相等，Y 没有按照 X 进行分异，即因子 X 与 Y 没有任何关系。q 值 表示 X 解释了 100q% 的 Y。
        """
        return self._factor_detector_result

    @property
    def risk_detector_result(self):
        """RiskDetectorResult: 风险区探测器分析结果。用于判断两个子区域间的属性均值是否有显著的差别,用 t 统计量来检验。

                               .. image:: ../image/GeographicalDetectorTformula.png

        """
        return self._risk_detector_result

    @property
    def interaction_detector_result(self):
        """InteractionDetectorResult: 交互作用探测器分析结果。识别不同风险因子 Xs 之间的交互作用,即评估因子 X1 和 X2 共同作用时
                                      是否会增加或减弱对因变量Y的解释力，或这些因子对 Y 的影响是相互独立的？评估的方法是首先分别
                                      计算两种因子 X1 和 X2 对 Y 的 q 值: q(Y|X1) 和 q(Y|X2)。然后叠加变量 X1 和 X2 两个图层相切所形成的新的层，计算 X1∩X2 对 Y 的 q 值： q(Y|X1∩X2)。最后，对
                                      q(Y|X1)、q(Y|X2) 与 q(Y|X1∩X2) 的数值进行比较，判断交互作用。

                                       - q(X1∩X2) < Min(q(X1),q(X2))                     非线性减弱
                                       - Min(q(X1),q(X2)) < q(X1∩X2) < Max(q(X1),q(X2))  单因子非线性减弱
                                       - q(X1∩X2) > Max(q(X1),q(X2))                     双因子增强
                                       - q(X1∩X2) = q(X1) + q(X2)                        独立
                                       - q(X1∩X2) > q(X1) + q(X2)                        非线性增强
        """
        return self._interaction_detector_result

    @property
    def ecological_detector_result(self):
        """pandas.DataFrame: 生态探测器分析结果。生态探测器用于比较两因子X1和X2对属性Y的空间分布的影响是否有显著的差异，以 F 统计量来衡量。

                             .. image:: ../image/GeographicalDetectorFformula.png

                             """
        return self._ecological_detector_result

    @staticmethod
    def _get_java_factor_detector_results(java_object):
        results = java_object.getFactorDetectorResults()
        values = []
        for i in range(len(results)):
            result_item = results[i]
            values.append([result_item.getVariable(), result_item.getQValue(), result_item.getPValue()])

        del results
        import pandas as pd
        return pd.DataFrame(values, columns=['Variable', 'Q', 'P'])

    @staticmethod
    def _get_java_ecological_detector_result(java_object):
        results = java_object.getEcologicalDetectorResult()
        detector_values = results.getEcologicalDetectorValues()
        values = []
        for i in range(len(detector_values)):
            result_item = detector_values[i]
            values.append([
             result_item.getVariableRow(), result_item.getVariableCol(), result_item.getSig()])

        del results
        import pandas as pd
        return pd.DataFrame(values, columns=['VariableRow', 'VariableCol', 'Sig'])