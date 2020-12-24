# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\mapping.py
# Compiled at: 2019-12-31 04:08:59
# Size of source mod 2**32: 104354 bytes
from .data import Workspace, Colors, DatasetVector, Point2D, Geometry, Dataset, DatasetImage, DatasetGrid, GeoPoint, Rectangle, GeoRegion, PrjCoordSys, QueryParameter, GeoStyle, Feature, CoordSysTransParameter, Color, TextStyle
from data._jvm import JVMBase
from data._util import get_input_dataset
from .enums import *
from ._utils import *
from ._logger import log_error, log_warning
__all__ = [
 'Map', 'LayerSetting', 'LayerSettingImage', 'LayerSettingVector', 'LayerSettingGrid', 'TrackingLayer',
 'Layer', 'LayerGridAggregation', 'LayerHeatmap']

class LayerSetting(JVMBase):
    __doc__ = '\n    图层设置基类。该类是对图层的显示风格的设置的基类。\n    对矢量数据集，栅格数据集以及影像数据集的图层风格分别使用 LayerSettingVector， LayerSettingGrid 和 LayerSettingImage 类中提供的方法进行设置。\n    矢量图层中所有要素采用相同的渲染风格，栅格图层采用颜色表来显示其像元，影像的图层的风格设置是对影像的亮度，对比度以及透明度等的设置。\n    '

    def __init__(self):
        JVMBase.__init__(self)

    @staticmethod
    def _from_java_object(java_object):
        if java_object is None:
            return
        else:
            layer_setting_type = java_object.getType().name()
            if layer_setting_type == 'VECTOR':
                layer_setting = LayerSettingVector()
            else:
                if layer_setting_type == 'GRID':
                    layer_setting = LayerSettingGrid()
                else:
                    if layer_setting_type == 'IMAGE':
                        layer_setting = LayerSettingImage()
                    else:
                        log_warning('Unsupported layer setting type ' + layer_setting_type)
                        return
        layer_setting._java_object = java_object
        return layer_setting


class LayerSettingVector(LayerSetting):
    __doc__ = '\n    矢量图层设置类。\n\n    该类主要用来设置矢量图层的显示风格。矢量图层用单一的符号或风格绘制所有的要素。当你只想可视化地显示你的空间数据，只关心空间数据中\n    各要素在什么位置，而不关心各要素在数量或性质上的不同时，可以用普通图层来显示要素数据。\n    '

    def __init__(self):
        LayerSetting.__init__(self)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.LayerSettingVector()

    def get_style(self):
        """
        返回矢量图层的风格。

        :return: 矢量图层的风格。
        :rtype: GeoStyle
        """
        java_style = self._jobject.getStyle()
        if java_style:
            return GeoStyle._from_java_object(java_style)
        return

    def set_style(self, style):
        """
        设置矢量图层的风格。

        :param style: 矢量图层的风格。
        :type style: GeoStyle
        :return: 对象自身
        :rtype: LayerSettingVector
        """
        if isinstance(style, GeoStyle):
            self._jobject.setStyle(oj(style))
            return self
        raise ValueError('required GeoStyle')


class LayerSettingGrid(LayerSetting):
    __doc__ = '\n    栅格图层设置类。\n\n    栅格图层设置是针对普通图层而言的。栅格图层采用颜色表来显示其像元。SuperMap 的颜色表是按照 8 比特的 RGB 彩色坐标系来显示像元的，\n    您可以根据像元的属性值来设置其显示颜色值，从而形象直观地表示栅格数据反映的现象。\n\n    '

    def __init__(self):
        LayerSetting.__init__(self)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.LayerSettingGrid()

    def get_color_table(self):
        """
        返回颜色表

        :return: 颜色表
        :rtype: Colors
        """
        color_table = self._jobject.getColorTable()
        if color_table:
            return Colors._from_java_object(color_table)

    def set_color_table(self, value):
        """
        设置颜色表。

        :param Colors value: 颜色表
        :return: 对象自身
        :rtype: LayerSettingGrid
        """
        if isinstance(value, Colors):
            self._jobject.setColorTable(oj(value))
            return self
        raise ValueError('required Colors')

    def get_special_value_color(self):
        """
        返回栅格数据集特殊值数据的颜色。

        :return: 栅格数据集特殊值数据的颜色。
        :rtype: Color
        """
        value = self._jobject.getSpecialValueColor()
        if value:
            return Color._from_java_object(value)
        return

    def set_special_value_color(self, value):
        """
        设置栅格数据集特殊值数据的颜色。

        :param value: 栅格数据集特殊值数据的颜色。
        :type value: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 对象自身
        :rtype: LayerSettingGrid
        """
        if value:
            java_color = to_java_color(value)
            if java_color:
                self._jobject.setSpecialValueColor(java_color)
                return self
        raise ValueError('required Color or tuple')

    def get_special_value(self):
        """
        返回图层的特殊值。 在新增一个 Grid 图层时，该方法的返回值与数据集的 NoValue 属性值相等。

        :return:
        :rtype: float
        """
        return self._jobject.getSpecialValue()

    def set_special_value(self, value):
        """
        设置图层的特殊值。

        :param float value: 图层的特殊值
        :return: 对象自身
        :rtype: LayerSettingGrid
        """
        self._jobject.setSpecialValue(float(value))
        return self

    def get_brightness(self):
        """
        返回 Grid 图层的亮度，值域范围为 -100 到 100，增加亮度为正，降低亮度为负。

        :return: Grid 图层的亮度。
        :rtype: int
        """
        return self._jobject.getBrightness()

    def set_brightness(self, value):
        """
        设置 Grid 图层的亮度，值域范围为 -100 到 100，增加亮度为正，降低亮度为负。

        :param int value:
        :return: 对象自身
        :rtype: LayerSettingGrid
        """
        self._jobject.setBrightness(int(value))
        return self

    def get_contrast(self):
        """
        返回 Grid 图层的对比度，值域范围为 -100 到 100，增加对比度为正，降低对比度为负。

        :return: Grid 图层的对比度。
        :rtype: int
        """
        return self._jobject.getContrast()

    def set_contrast(self, value):
        """
        设置 Grid 图层的对比度，值域范围为 -100 到 100，增加对比度为正，降低对比度为负。

        :param int value: Grid 图层的对比度。
        :return: 对象自身
        :rtype: LayerSettingGrid
        """
        self._jobject.setContrast(int(value))
        return self

    def get_opaque_rate(self):
        """
        返回 Grid 图层显示不透明度。不透明度为一个 0-100 之间的数。0 为不显示；100 为完全不透明。只对栅格图层有效，在地图旋转的情况下也有效。

        :return: Grid 图层显示不透明度。
        :rtype: int
        """
        return self._jobject.getOpaqueRate()

    def set_opaque_rate(self, value):
        """
        设置 Grid 图层显示的不透明度。不透明度为一个 0-100 之间的数。0 为不显示；100 为完全不透明。只对栅格图层有效，在地图旋转的情况下也有效。

        :param int value: Grid 图层显示不透明度。
        :return: 对象自身
        :rtype: LayerSettingGrid
        """
        self._jobject.setOpaqueRate(int(value))
        return self

    def is_special_value_transparent(self):
        """
        返回图层的特殊值（SpecialValue）所处区域是否透明。

        :return: 一个布尔值，图层的特殊值（SpecialValue）所处区域透明返回 true，否则返回 false。
        :rtype: bool
        """
        return self._jobject.isSpecialValueTransparent()

    def set_special_value_transparent(self, value):
        """
        设置图层的特殊值（SpecialValue）所处区域是否透明。

        :param bool value: 图层的特殊值（SpecialValue）所处区域是否透明。
        :return: 对象自身
        :rtype: LayerSettingGrid
        """
        self._jobject.setSpecialValueTransparent(bool(value))
        return self

    def get_color_dictionary(self):
        """
        返回图层的颜色对照表。

        :return: 图层的颜色对照表。
        :rtype: dict[float, Color]
        """
        color_dicts = self._jobject.getColorDictionary()
        if color_dicts:
            keys = color_dicts.getKeys()
            colors = {}
            for key in keys:
                colors[key] = Color._from_java_object(color_dicts.getColor(key))

            return colors

    def set_color_dictionary(self, colors):
        """
        设置图层的颜色对照表

        :param colors: 指定图层的颜色对照表。
        :type colors: dict[float, Color]
        :return: 对象自身
        :rtype: LayerSettingGrid
        """
        if isinstance(colors, dict):
            java_color = self._jvm.com.supermap.data.ColorDictionary()
            for key, value in colors.items():
                java_color.setColor(float(key), to_java_color(value))

            self._jobject.setColorDictionary(java_color)
            return self
        raise ValueError('required dict[float,Color]')

    def get_image_interpolation_mode(self):
        """
        返回显示图像时使用的插值算法。

        :return: 显示图像时使用的插值算法
        :rtype: ImageInterpolationMode
        """
        mode = self._jobject.getImageInterpolationMode()
        if mode:
            return ImageInterpolationMode._make(mode.name())
        return

    def set_image_interpolation_mode(self, value):
        """
        设置显示图像时使用的插值算法。

        :param value: 指定的插值算法。
        :type value: ImageInterpolationMode or str
        :return: 对象自身
        :rtype: LayerSettingGrid
        """
        value = ImageInterpolationMode._make(value)
        if isinstance(value, ImageInterpolationMode):
            self._jobject.setImageInterpolationMode(oj(value))
            return self
        raise ValueError('required ImageInterpolationMode')


class LayerSettingImage(LayerSetting):
    __doc__ = '\n    影像图层设置类。\n    '

    def __init__(self):
        LayerSetting.__init__(self)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.LayerSettingImage()

    def get_background_color(self):
        """
        获取背景值的显示颜色

        :return: 背景值的显示颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getBackgroundColor())

    def set_background_color(self, value):
        """
        设置指定的背景值的显示颜色。

        :param value: 定的背景值的显示颜色
        :type value: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        if value:
            self._jobject.setBackgroundColor(to_java_color(value))
        return self

    def get_background_value(self):
        """
        获取影像中被视为背景的值

        :return: 影像中被视为背景的值
        :rtype: float
        """
        return self._jobject.getBackgroundValue()

    def set_background_value(self, value):
        """
        设置影像中被视为背景的值

        :param float value: 影像中被视为背景的值
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        self._jobject.setBackgroundValue(float(value))
        return self

    def get_brightness(self):
        """
        返回影像图层的亮度。值域范围为 -100 到 100，增加亮度为正，降低亮度为负。亮度值可以保存到工作空间。

        :return: 影像图层的亮度值。
        :rtype: int
        """
        return self._jobject.getBrightness()

    def set_brightness(self, value):
        """
        设置影像图层的亮度。值域范围为 -100 到 100，增加亮度为正，降低亮度为负。

        :param int value: 影像图层的亮度值。
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        self._jobject.setBrightness(int(value))
        return self

    def get_contrast(self):
        """
        返回影像图层的对比度。值域范围为 -100 到 100，增加对比度为正，降低对比度为负。

        :return: 影像图层的对比度。
        :rtype: int
        """
        return self._jobject.getContrast()

    def set_contrast(self, value):
        """
        设置影像图层的对比度。值域范围为 -100 到 100，增加对比度为正，降低对比度为负。

        :param int value: 影像图层的对比度。
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        self._jobject.setContrast(int(value))
        return self

    def get_display_band_indexes(self):
        """
        返回当前影像图层显示的波段索引。假设当前影像图层有若干波段，当需要按照设置的色彩模式(如 RGB)设置显示波段时，指定色彩(如 RGB 中的红色、绿色、蓝色)对应的波段索引(如0，2，1)即可。

        :return: 当前影像图层显示的波段索引。
        :rtype: list[int]
        """
        return self._jobject.getDisplayBandIndexes()

    def set_display_band_indexes(self, indexes):
        """
        设置当前影像图层显示的波段索引。假设当前影像图层有若干波段，当需要按照设置的色彩模式(如 RGB)设置显示波段时，指定色彩(如 RGB 中的红色、绿色、蓝色)对应的波段索引(如0，2，1)即可。

        :param indexes: 当前影像图层显示的波段索引。
        :type indexes: list[int] or tuple[int]
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        values = split_input_list_from_str(indexes)
        if isinstance(values, list):
            self._jobject.setDisplayBandIndexes(to_java_int_array(values))
        return self

    def get_display_color_space(self):
        """
        返回影像图层的色彩显示模式。它会根据影像图层当前的色彩格式和显示的波段将该影像图层以该色彩模式进行显示。

        :return: 影像图层的色彩显示模式。
        :rtype: ColorSpaceType
        """
        return ColorSpaceType._make(self._jobject.getDisplayColorSpace().name())

    def set_display_color_space(self, value):
        """
        设置影像图层的色彩显示模式。它会根据影像图层当前的色彩格式和显示的波段将该影像图层以该色彩模式进行显示。

        :param value: 影像图层的色彩显示模式。
        :type value: ColorSpaceType
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        value = ColorSpaceType._make(value)
        if isinstance(value, ColorSpaceType):
            self._jobject.setDisplayColorSpace(oj(value))
        return self

    def get_display_mode(self):
        """
        返回影像显示模式。

        :return: 影像显示模式。
        :rtype: ImageDisplayMode
        """
        return ImageDisplayMode._make(self._jobject.getDisplayMode().name())

    def set_display_mode(self, value):
        """
        设置影像显示模式。

        :param value: 影像显示模式，多波段支持两种显示模式，单波段只支持拉伸显示模式。
        :type value: ImageDisplayMode
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        mode = ImageDisplayMode._make(value)
        if isinstance(mode, ImageDisplayMode):
            self._jobject.setDisplayMode(oj(mode))
        return self

    def get_image_interpolation_mode(self):
        """
        设置显示图像时使用的插值算法。

        :return: 显示图像时使用的插值算法
        :rtype: ImageInterpolationMode
        """
        mode = self._jobject.getImageInterpolationMode()
        if mode:
            return ImageInterpolationMode._make(mode.name())
        return

    def set_image_interpolation_mode(self, value):
        """
        设置显示图像时使用的插值算法

        :param value: 指定的插值算法
        :type value: ImageInterpolationMode or str
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        value = ImageInterpolationMode._make(value)
        if isinstance(value, ImageInterpolationMode):
            self._jobject.setImageInterpolationMode(oj(value))
            return self
        raise ValueError('required ImageInterpolationMode')

    def get_opaque_rate(self):
        """
        返回影像图层显示的不透明度。不透明度为一个 0-100 之间的数。0为不显示；100为完全不透明。只对影像图层有效，在地图旋转的情况下也有效。

        :return: 影像图层显示的不透明度。
        :rtype: int
        """
        return self._jobject.getOpaqueRate()

    def set_opaque_rate(self, value):
        """
        设置影像图层显示的不透明度。不透明度为一个 0-100 之间的数。0为不显示；100为完全不透明。只对影像图层有效，在地图旋转的情况下也有效

        :param int value: 影像图层显示的不透明度
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        self._jobject.setOpaqueRate(int(value))
        return self

    def get_special_value(self):
        """
        获取影像中的特殊值。该特殊值可以通过 :py:meth:`set_special_value_color` 指定显示颜色。

        :return: 影像中的特殊值
        :rtype: float
        """
        return self._jobject.getSpecialValue()

    def set_special_value(self, value):
        """
        设置影像中的特殊值，该特殊值可以通过 :py:meth:`set_special_value_color` 指定显示颜色。

        :param float value: 影像中的特殊值
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        self._jobject.setSpecialValue(float(value))
        return self

    def get_special_value_color(self):
        """
        获取特殊值的显示颜色

        :return: 特殊值的显示颜色
        :rtype: Color
        """
        java_color = self._jobject.getSpecialValueColor()
        if java_color:
            return Color._from_java_object(java_color)

    def set_special_value_color(self, color):
        """
        设置 :py:meth:`set_special_value` 所设定的特殊值的显示颜色

        :param color: 特殊值的显示颜色
        :type color: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        java_color = to_java_color(color)
        if java_color:
            self._jobject.setSpecialValueColor(java_color)
            return self

    def get_transparent_color(self):
        """
        返回背景透明色

        :return: 背景透明色
        :rtype: Color
        """
        java_color = self._jobject.getTransparentColor()
        if java_color:
            return Color._from_java_object(java_color)

    def set_transparent_color(self, color):
        """
        设置背景透明色。

        :param color: 背景透明色
        :type color: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        java_color = to_java_color(color)
        if java_color:
            self._jobject.setTransparentColor(java_color)
            return self

    def get_transparent_color_tolerance(self):
        """
        返回背景透明色容限，容限值范围为[0,255]。

        :return: 背景透明色容限
        :rtype: int
        """
        return self._jobject.getTransparentColorTolerance()

    def set_transparent_color_tolerance(self, value):
        """
        设置背景透明色容限，容限值范围为[0,255]。

        :param int value: 背景透明色容限
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        self._jobject.setTransparentColorTolerance(int(value))
        return self

    def is_transparent(self):
        """
        设置是否使影像图层背景透明

        :return: 一个布尔值指定是否使影像图层背景透明。
        :rtype: bool
        """
        return self._jobject.isTransparent()

    def set_transparent(self, value):
        """
        设置是否使影像图层背景透明

        :param bool value: 一个布尔值指定是否使影像图层背景透明
        :return: 对象自身
        :rtype: LayerSettingImage
        """
        self._jobject.setTransparent(bool(value))
        return self


class Layer(JVMBase):
    __doc__ = '\n    图层类。\n\n    该类提供了图层显示和控制等的便于地图管理的一系列方法。当数据集被加载到地图窗口中显示时，就形成了一个图层，因此图层是数据集的可视\n    化显示。一个图层是对一个数据集的引用或参考。\n    图层分为普通图层和专题图层，矢量的普通图层中所有要素采用相同的渲染风格，栅格图层采用颜色表来显示其像元；而专题图层的则采用指定类\n    型的专题图风格来渲染其中的要素或像元。影像数据只对应普通图层。普通图层的风格通过 :py:meth:`get_layer_setting`\n     和 :py:meth:`set_layer_setting` 方法来返回或设置。\n\n    该类的实例不可被创建。只可以通过在 :py:class:`Map` 类 :py:meth:`Map.add_dataset` 方法来创建\n    '

    def __init__(self, java_object):
        JVMBase.__init__(self)
        self._java_object = java_object

    def from_xml(self, xml):
        """
        根据指定的XML字符串创建图层对象。 任何图层都可以导出成xml字符串，而图层的xml字符串也可以导入成为一个图层来进行显示。图层的
        xml字符串中存储了关于图层的显示的设置以及关联的数据信息等对图层的所有的设置。可以将图层的xml字符串保存成一个xml文件。

        :param str xml: 用来创建图层的XML字符串
        :return: 创建成功则返回true，否则返回false。

        :rtype: bool
        """
        if xml:
            return self._jobject.fromXML(str(xml))
        return False

    def to_xml(self):
        """
        返回此图层对象的 XML字符串形式的描述。 任何图层都可以导出成xml字符串，而图层的xml字符串也可以导入成为一个图层来进行显示。图
        层的xml字符串中存储了关于图层的显示的设置以及关联的数据信息等对图层的所有的设置。可以将图层的xml字符串保存成一个xml文件。

        :return: 返回此图层对象的 XML字符串形式的描述。
        :rtype: str
        """
        return self._jobject.toXML()

    @property
    def bounds(self):
        """Rectangle: 图层的范围"""
        return Rectangle._from_java_object(self._jobject.getBounds())

    @property
    def dataset(self):
        """Dataset: 返回此图层对应的数据集对象。图层是对数据集的引用，因而，一个图层与一个数据集相对应。 """
        java_dt = self._jobject.getDataset()
        if java_dt:
            ds = Workspace().get_datasource(java_dt.getDatasource().getAlias())
            return ds.get_dataset(java_dt.getName())

    def set_dataset(self, dt):
        """
        设置此图层对应的数据集对象。图层是对数据集的引用，因而，一个图层与一个数据集相对应

        :param Dataset dt: 此图层对应的数据集对象
        :return: 对象自身
        :rtype: Layer
        """
        dt = get_input_dataset(dt)
        if isinstance(dt, Dataset):
            if dt == self.dataset:
                return self
            self._jobject.setDataset(oj(dt))
            return self
        raise ValueError('required Dataset')

    @property
    def caption(self):
        """str: 返回图层的标题。图层的标题为图层的显示名称，例如在图例或排版制图时显示的图层的名称即为图层的标题。注意与图层的名称相区别。 """
        return self._jobject.getCaption()

    def set_caption(self, value):
        """
        设置图层的标题。图层的标题为图层的显示名称，例如在图例或排版制图时显示的图层的名称即为图层的标题。注意与图层的名称相区别。

        :param str value: 指定图层的标题。
        :return: 对象自身
        :rtype: Layer
        """
        self._jobject.setCaption(str(value))
        return self

    def get_clip_region(self):
        """
        返回图层的裁剪区域。

        :return: 返回图层的裁剪区域。
        :rtype: GeoRegion
        """
        region = self._jobject.getClipRegion()
        if region:
            return Geometry._from_java_object(region)

    def set_clip_region(self, region):
        """
        设置图层的裁剪区域。

        :param region:  图层的裁剪区域。
        :type region: GeoRegion or Rectangle
        :return: 对象自身
        :rtype: Layer
        """
        if isinstance(region, Rectangle):
            region = region.to_region()
        if isinstance(region, GeoRegion):
            self._jobject.setClipRegion(oj(region))
            return self
        raise ValueError('required GeoRegion')

    def get_display_filter(self):
        """
        返回图层显示过滤条件。通过设置显示过滤条件，可以使图层中的一些要素显示，而另一些要素不显示，以便重点分析感兴趣的要素，而过滤掉其他要素。

        注意：该方法仅支持属性查询，不支持空间查询

        :return: 图层显示过滤条件。
        :rtype: QueryParameter
        """
        param = self._jobject.getDisplayFilter()
        if param:
            return QueryParameter._from_java_object(param)
        return

    def set_display_filter(self, parameter):
        """
        设置图层显示过滤条件。通过设置显示过滤条件，可以使图层中的一些要素显示，而另一些要素不显示，以便重点分析感兴趣的要素，而过滤掉其他要素。比如说通过连接（JoinItem）的方式将一个外部表的字段作为专题图的表达字段，在生成专题图后进行显示时，需要调用此方法，否则专题图将创建失败。

        注意：该方法仅支持属性查询，不支持空间查询

        :param QueryParameter parameter:  指定图层显示过滤条件。
        :return: 对象自身
        :rtype: Layer
        """
        if isinstance(parameter, QueryParameter):
            self._jobject.setDisplayFilter(oj(parameter))
            return self
        raise ValueError('parameter required QueryParameter')

    def get_max_visible_scale(self):
        """
        返回此图层的最大可见比例尺。最大可见比例尺不可为负，当地图的当前显示比例尺大于或等于图层最大可见比例尺时，此图层将不显示。

        :return: 图层的最大可见比例尺。
        :rtype: float
        """
        return self._jobject.getMaxVisibleScale()

    def set_max_visible_scale(self, value):
        """
        设置此图层的最大可见比例尺。最大可见比例尺不可为负，当地图的当前显示比例尺大于或等于图层最大可见比例尺时，此图层将不显示。

        :param float value: 指定图层的最大可见比例尺。
        :return: 对象自身
        :rtype: Layer
        """
        self._jobject.setMaxVisibleScale(float(value))
        return self

    def get_min_visible_scale(self):
        """

        :return:
        :rtype: float
        """
        return self._jobject.getMinVisibleScale()

    def set_min_visible_scale(self, value):
        """
        返回此图层的最小可见比例尺。最小可见比例尺不可为负。当地图的当前显示比例尺小于图层最小可见比例尺时，此图层将不显示。

        :param float value: 图层的最小可见比例尺。
        :return: 对象自身
        :rtype: Layer
        """
        self._jobject.setMinVisibleScale(float(value))
        return self

    def get_opaque_rate(self):
        """
        返回图层的不透明度。

        :return: 图层的不透明度。
        :rtype: int
        """
        return self._jobject.getOpaqueRate()

    def set_opaque_rate(self, value):
        """
        设置图层的不透明度。

        :param int value: 图层的不透明度。
        :return: 对象自身
        :rtype: Layer
        """
        self._jobject.setOpaqueRate(int(value))
        return self

    def is_antialias(self):
        """
        返回图层是否开启反走样。

        :return: 指示图层是否开启反走样。true 为开启反走样，false 为不开启。
        :rtype: bool
        """
        return self._jobject.isAntialias()

    def set_antialias(self, value):
        """
        设置图层是否开启反走样。

        :param bool value: 指示图层是否开启反走样。true 为开启反走样，false 为不开启。
        :return: 对象自身
        :rtype: Layer
        """
        self._jobject.setAntialias(bool(value))
        return self

    def is_clip_region_enabled(self):
        """
        返回裁剪区域是否有效。

        :return: 指定裁剪区域是否有效。true 表示有效，false 表示无效。
        :rtype: bool
        """
        return self._jobject.isClipRegionEnabled()

    def set_clip_region_enabled(self, value):
        """
        设置裁剪区域是否有效。

        :param bool value: 指定裁剪区域是否有效，true 表示有效，false 表示无效。

        :return: 对象自身
        :rtype: Layer
        """
        self._jobject.setClipRegionEnabled(bool(value))
        return self

    def is_symbol_scalable(self):
        """
        返回图层的符号大小是否随图缩放。默认为 false。true 表示当图层被放大或缩小时，符号也随之放大或缩小。

        :return: 图层的符号大小是否随图缩放。
        :rtype: bool
        """
        return self._jobject.isSymbolScalable()

    def set_symbol_scalable(self, value):
        """
        设置图层的符号大小是否随图缩放。默认为 false。true 表示当图层被放大或缩小时，符号也随之放大或缩小。

        :param bool value: 指定图层的符号大小是否随图缩放。
        :return: 对象自身
        :rtype: Layer
        """
        self._jobject.setSymbolScalable(bool(value))
        return self

    def is_visible(self):
        """
        返回此图层是否可见。true 表示此图层可见，false 表示图层不可见。当图层不可见时，其他所有的属性的设置将无效

        :return: 图层是否可见。
        :rtype: bool
        """
        return self._jobject.isVisible()

    def set_visible(self, value):
        """
        设置此图层是否可见。true 表示此图层可见，false 表示图层不可见。当图层不可见时，其他所有的属性的设置将无效。

        :param bool value: 指定图层是否可见。
        :return: 对象自身
        :rtype: Layer
        """
        self._jobject.setVisible(bool(value))
        return self

    def is_visible_scale(self, scale):
        """
        返回指定的比例尺是否为可视比例尺，即在设定的最小显示比例尺和最大显示比例尺之间

        :param float scale: 指定的显示比例尺。
        :return: 返回 true，表示指定的比例尺为可视比例尺；否则为 false。
        :rtype: bool
        """
        return self._jobject.isVisibleScale(float(scale))

    def get_layer_setting(self):
        """
        返回普通图层的风格设置。普通图层风格的设置对矢量数据图层，栅格数据图层以及影像数据图层是不相同的。
        :py:class:`LayerSettingVector` , :py:class:`LayerSettingGrid` ， :py:class:`LayerSettingImage`  类分别用来对矢量数
        据图层，栅格数据图层和影像数据图层的风格进行设置和修改。

        :return: 普通图层的风格设置
        :rtype: LayerSetting
        """
        java_setting = self._jobject.getAdditionalSetting()
        if java_setting:
            return LayerSetting._from_java_object(java_setting)

    def set_layer_setting(self, setting):
        """
        设置普通图层的风格

        :param LayerSetting setting: 普通图层的风格设置。
        :return: 对象自身
        :rtype: Layer
        """
        if isinstance(setting, LayerSetting):
            self._jobject.setAdditionalSetting(oj(setting))
            return self
        raise ValueError('required LayerSetting')


class LayerHeatmap(Layer):
    __doc__ = '\n    热力图图层类，该类继承自Layer类。\n\n    热力图是通过颜色分布，描述诸如人群分布、密度和变化趋势等的一种地图表现手法，因此，能够非常直观地呈现一些原本不易理解或表达的数据，比如密度、频度、温度等。\n    热力图图层除了可以反映点要素的相对密度，还可以表示根据属性进行加权的点密度，以此考虑点本身的权重对于密度的贡献。\n    热力图图层将随地图放大或缩小而发生更改，是一种动态栅格表面，例如，绘制全国旅游景点的访问客流量的热力图，当放大地图后，该热力图就可以反映某省内或者局部地区的旅游景点访问客流量分布情况。\n    '

    def __init__(self, java_object):
        Layer.__init__(self, java_object)

    def get_colorset(self):
        """
        返回用于显示当前热力图的颜色集合。

        :return: 用于显示当前热力图的颜色集合
        :rtype: Colors
        """
        java_colorset = self._jobject.getColorset()
        return Colors._from_java_object(java_colorset)

    def set_colorset(self, colors):
        """
        设置用于显示当前热力图的颜色集合。

        :param colors: 用于显示当前热力图的颜色集合
        :type colors: Colors
        :return: LayerHeatmap 对象自身
        :rtype: LayerHeatmap
        """
        if isinstance(colors, Colors):
            self._jobject.setColorset(oj(colors))
        return self

    def get_fuzzy_degree(self):
        """
        返回热力图中颜色渐变的模糊程度。

        :return: 热力图中颜色渐变的模糊程度
        :rtype: float
        """
        return self._jobject.getFuzzyDegree()

    def set_fuzzy_degree(self, value):
        """
        设置热力图中颜色渐变的模糊程度。

        :param float value: 热力图中颜色渐变的模糊程度。
        :return: LayerHeatmap 对象自身
        :rtype: LayerHeatmap
        """
        self._jobject.setFuzzyDegree(float(value))
        return self

    def get_intensity(self):
        """
        返回热力图中高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变色带中高点密度颜色（MaxColor）所占的比重，该值越
        大，表示在色带中高点密度颜色所占比重越大。

        :return: 热力图中高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变色带中高点密度颜色（MaxColor）所占的比重
        :rtype: float
        """
        return self._jobject.getIntensity()

    def set_intensity(self, value):
        """
        设置热力图中高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变色带中高点密度颜色（MaxColor）所占的比重，该值越大，表示在色带中高点密度颜色所占比重越大。

        :param float value: 热力图中高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变色带中高点密度颜色（MaxColor）所占的比重
        :return: LayerHeatmap 对象自身
        :rtype: LayerHeatmap
        """
        return self._jobject.setIntensity(float(value))

    def get_kernel_radius(self):
        """
        返回用于计算密度的核半径。单位为：屏幕坐标。

        :return: 用于计算密度的核半径
        :rtype: int
        """
        return self._jobject.getKernelRadius()

    def set_kernel_radius(self, value):
        """
        设置用于计算密度的核半径。单位为：屏幕坐标。
        核半径在热力图中所起的作用如下所述：

        - 热力图将根据设置的核半径值对每个离散点建立一个缓冲区。核半径数值的单位为：屏幕坐标；

        - 对每个离散点建立缓冲区后，对每个离散点的缓冲区，使用渐进的灰度带（完整的灰度带是0~255）从内而外，由浅至深地填充；

        - 由于灰度值可以叠加（值越大颜色越亮，在灰度带中则显得越白。在实际中，可以选择ARGB模型中任一通道作为叠加灰度值），从而对于有缓冲区交叉的区域，可以叠加灰度值，因而缓冲区交叉的越多，灰度值越大，这块区域也就越“热”；

        - 以叠加后的灰度值为索引，从一条有256种颜色的色带中（例如彩虹色）映射颜色，并对图像重新着色，从而实现热力图。

        查找半径越大，生成的密度栅格越平滑且概化程度越高；值越小，生成的栅格所显示的信息越详细。

        :param int value: 计算密度的核半径
        :return: LayerHeatmap 对象自身
        :rtype: LayerHeatmap
        """
        return self._jobject.setKernelRadius(int(value))

    def get_max_color(self):
        """
        返回高点密度的颜色，热力图图层将通过高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变的颜色方案。

        :return: 高点密度的颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getMaxColor())

    def set_max_color(self, value):
        """
        设置高点密度的颜色，热力图图层将通过高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变的颜色方案。

        :param value: 高点密度的颜色
        :type value: Color or tuple[int,int,int]
        :return: LayerHeatmap 对象自身
        :rtype: LayerHeatmap
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setMaxColor(to_java_color(value))
        return self

    def get_max_value(self):
        """
        返回一个最大值。当前热力图图层中最大值（MaxValue）与最小值（MinValue）之间栅格将使用MaxColor和MinColor所确定的色带进行渲
        染，其他大于MaxValue的栅格将以MaxColor渲染；而者小于MinValue的栅格将以MinColor渲染。

        :return: 最大值
        :rtype: float
        """
        return self._jobject.getMaxValue()

    def set_max_value(self, value):
        """
        设置一个最大值。当前热力图图层中最大值（MaxValue）与最小值（MinValue）之间栅格将使用MaxColor和MinColor所确定的色带进行渲
        染，其他大于MaxValue的栅格将以MaxColor渲染；而者小于MinValue的栅格将以MinColor渲染。 如果没有指定最大最小值，系统将自动
        计算获得当前热力图图层中的最大和最小值。

        :param float value: 最大值
        :return: LayerHeatmap 对象自身
        :rtype: LayerHeatmap
        """
        self._jobject.setMaxValue(float(value))
        return self

    def get_min_color(self):
        """
        返回低点密度的颜色，热力图图层将通过高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变的颜色方案。

        :return: 低点密度的颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getMinColor())

    def set_min_color(self, value):
        """
        设置低点密度的颜色，热力图图层将通过高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变的颜色方案。

        :param value: 低点密度的颜色
        :type value: Color or tuple[int,int,int]
        :return: LayerHeatmap 对象自身
        :rtype: LayerHeatmap
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setMinColor(to_java_color(value))
        return self

    def get_min_value(self):
        """
        返回一个最小值。当前热力图图层中最大值（MaxValue）与最小值（MinValue）之间栅格将使用MaxColor和MinColor所确定的色带进行渲
        染，其他大于MaxValue的栅格将以MaxColor渲染；而者小于MinValue的栅格将以MinColor渲染。

        :return: 最小值
        :rtype: float
        """
        return self._jobject.getMinValue()

    def set_min_value(self, value):
        """
        设置一个最小值。当前热力图图层中最大值（MaxValue）与最小值（MinValue）之间栅格将使用MaxColor和MinColor所确定的色带进行渲
        染，其他大于MaxValue的栅格将以MaxColor渲染；而者小于MinValue的栅格将以MinColor渲染。

        :param float value: 最小值
        :return: LayerHeatmap 对象自身
        :rtype: LayerHeatmap
        """
        self._jobject.setMinValue(float(value))
        return self

    def get_weight_field(self):
        """
        返回权重字段。热力图图层除了可以反映点要素的相对密度，还可以表示根据权重字段进行加权的点密度，以此考虑点本身的权重对于密度的贡献。

        :return: 权重字段
        :rtype: str
        """
        return self._jobject.getWeightField()

    def set_weight_field(self, value):
        """
        设置权重字段。热力图图层除了可以反映点要素的相对密度，还可以表示根据权重字段进行加权的点密度，以此考虑点本身的权重对于密度的贡献。
        根据核半径（KernelRadius）确定的离散点缓冲区，其叠加确定了热度分布密度，而权重则是确定了点对于密度的影响力，点的权重值确定了
        该点缓冲区的对于密度的影响力，即如果点缓冲区原来的影响系数为1，点的权重值为10，则引入权重后，该点缓冲区的影响系数为1*10=10，以此类推其他离散点缓冲区的密度影响系数。

        那么，引入权重后，将获得一个新的叠加后的灰度值为索引，在利用指定的色带为其着色，从而实现引入权重的热力图。

        :param str value: 权重字段。热力图图层除了可以反映点要素的相对密度，还可以表示根据权重字段进行加权的点密度，以此考虑点本身的权重对于密度的贡献。
        :return: LayerHeatmap 对象自身
        :rtype: LayerHeatmap
        """
        if value:
            self._jobject.setWeightField(str(value))
        return self


class LayerGridAggregation(Layer):
    __doc__ = '\n    网格聚合图\n    '

    def __init__(self, java_object):
        Layer.__init__(self, java_object)

    def get_colorset(self):
        """
        返回网格单元统计值最大值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :return: 网格单元统计值最大值对应的颜色
        :rtype: Colors
        """
        java_colorset = self._jobject.getColorset()
        return Colors._from_java_object(java_colorset)

    def set_colorset(self, colors):
        """
        设置网格单元统计值最大值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :param colors: 网格单元统计值最大值对应的颜色
        :type colors: Colors
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        if isinstance(colors, Colors):
            self._jobject.setColorset(oj(colors))
        return self

    def get_grid_type(self):
        """
        返回网格聚合图的格网类型

        :return: 网格聚合图的格网类型
        :rtype: LayerGridAggregationType
        """
        return LayerGridAggregationType._make(self._jobject.getGridAggregationType().name())

    def set_grid_type(self, value):
        """
        设置网格聚合图的格网类型，可以为矩形网格或者六边形网格。

        :param value: 网格聚合图的格网类型
        :type value: LayerGridAggregationType or str
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        value = LayerGridAggregationType._make(value)
        if isinstance(value, LayerGridAggregationType):
            self._jobject.setGridAggregationType(oj(value))
        return self

    def get_grid_height(self):
        """
        返回设置矩形格网的高度。单位为：屏幕坐标。

        :return: 矩形格网的高度
        :rtype: int
        """
        return self._jobject.getGridHeight()

    def set_grid_height(self, value):
        """
        设置矩形格网的高度。单位为：屏幕坐标。

        :param int value: 矩形格网的高度
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        self._jobject.setGridHeight(int(value))
        return self

    def get_grid_width(self):
        """
        返回六边形格网的边长，或者矩形格网的宽度。单位为：屏幕坐标。

        :return: 六边形格网的边长，或者矩形格网的宽度
        :rtype: int
        """
        return self._jobject.getGridwidth()

    def set_grid_width(self, value):
        """
        设置六边形格网的边长，或者矩形格网的宽度。单位为：屏幕坐标。

        :param int value: 六边形格网的边长，或者矩形格网的宽度
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        self._jobject.setGridWidth(int(value))
        return self

    def get_max_color(self):
        """
        返回网格单元统计值最大值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :return: 网格单元统计值最大值对应的颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getMaxColor())

    def set_max_color(self, value):
        """
        设置网格单元统计值最大值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :param value: 网格单元统计值最大值对应的颜色
        :type value: Color or tuple[int,int,int]
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setMaxColor(to_java_color(value))
        return self

    def get_min_color(self):
        """
        返回网格单元统计值最小值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :return: 网格单元统计值最小值对应的颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getMinColor())

    def set_min_color(self, value):
        """
        设置网格单元统计值最小值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :param value: 网格单元统计值最小值对应的颜色
        :type value: Color or tuple[int,int,int]
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setMinColor(to_java_color(value))
        return self

    def get_weight_field(self):
        """
        返回权重字段。网格聚合图每个网格单元的统计值默认为落在该单元格内的点对象数目，此外，还可以引入点的权重信息，考虑网格单元内点的加权值作为网格的统计值。

        :return: 权重字段
        :rtype: str
        """
        return self._jobject.getWeightField()

    def set_weight_field(self, value):
        """
        设置权重字段。网格聚合图每个网格单元的统计值默认为落在该单元格内的点对象数目，此外，还可以引入点的权重信息，考虑网格单元内点的加权值作为网格的统计值。

        :param str value: 权重字段。网格聚合图每个网格单元的统计值默认为落在该单元格内的点对象数目，此外，还可以引入点的权重信息，考虑网格单元内点的加权值作为网格的统计值。
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        if value:
            self._jobject.setWeightField(str(value))
        return self

    def is_show_label(self):
        """
        是否显示网格单元标签

        :return: 是否显示网格单元标签，true表示显示；false表示不显示。
        :rtype: bool
        """
        return self._jobject.getIsShowGridLabel()

    def set_show_label(self, value):
        """
        设置是否显示网格单元标签。

        :param bool value: 指示是否显示网格单元标签，true表示显示；false表示不显示。
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        self._jobject.setIsShowGridLabel(bool(value))
        return self

    def get_label_style(self):
        """
        返回网格单元内统计值标签的风格。

        :return: 网格单元内统计值标签的风格。
        :rtype: TextStyle
        """
        text_style = self._jobject.getGridLabelStyle()
        if text_style:
            return TextStyle._from_java_object(text_style)

    def set_label_style(self, value):
        """
        设置网格单元内统计值标签的风格。

        :param value: 网格单元内统计值标签的风格。
        :type value: TextStyle
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        if isinstance(value, TextStyle):
            self._jobject.setGridLabelStyle(oj(value))
            return self
        raise ValueError('required TextStyle')

    def get_line_style(self):
        """
        返回网格单元矩形边框线的风格。

        :return: 网格单元矩形边框线的风格
        :rtype: GeoStyle
        """
        line_style = self._jobject.getGridLineStyle()
        if line_style:
            return GeoStyle._from_java_object(line_style)

    def set_line_style(self, value):
        """
        设置网格单元矩形边框线的风格。

        :param value: 网格单元矩形边框线的风格
        :type value: GeoStyle
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        if isinstance(value, GeoStyle):
            self._jobject.setGridLineStyle(oj(value))
            return self
        raise ValueError('required GeoStyle')

    def get_original_point_style(self):
        """
        返回点数据显示的风格。对网格聚合图进行放大浏览，当比例尺较大时，将不显示聚合的网格效果，而显示原始点数据内容。

        :return: 点数据显示的风格。
        :rtype: GeoStyle
        """
        point_style = self._jobject.getOriginalPointStyle()
        if point_style:
            return GeoStyle._from_java_object(point_style)

    def set_original_point_style(self, value):
        """
        设置点数据显示的风格。 对网格聚合图进行放大浏览，当比例尺较大时，将不显示聚合的网格效果，而显示原始点数据内容。

        :param value: 点数据显示的风格
        :type value: GeoStyle
        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        if isinstance(value, GeoStyle):
            self._jobject.setOriginalPointStyle(oj(value))
            return self
        raise ValueError('required GeoStyle')

    def update_data(self):
        """
        根据数据变化自动更新当前网格聚合图

        :return: LayerGridAggregation 对象自身
        :rtype: LayerGridAggregation
        """
        self._jobject.updateData()
        return self


class TrackingLayer(JVMBase):
    __doc__ = '\n    跟踪图层类。\n\n    在 SuperMap 中，每个地图窗口都有一个跟踪图层，确切地说，每个地图显示时都有一个跟踪图层。 跟踪图层是一个空白的透明图层，总是在地\n    图各图层的最上层，主要用于在一个处理或分析过程中，临时存放一些图形对象，以及一些文本等。 只要地图显示，跟踪图层就会存在，你不可\n    以删除跟踪图层，也不可以改变其位置。\n\n    在 SuperMap 中跟踪图层的作用主要有以下方面：\n\n    - 当不想往记录集中添加几何对象，而又需要这个几何对象的时候，就可以把这个几何对象临时添加到跟踪图层上，用完该几何对象之后清除跟踪\n      图层即可。例如，当需要测量距离时，需要在地图上拉一条线，但是这一条线在地图上并不存在，此时就可以使用跟踪图层来实现。\n\n    - 当需要对目标进行动态跟踪的时候，如果把目标放到记录集中，要实现动态跟踪就得不断地刷新整个图层，这样会大大影响效率，如果将这个需\n      要进行跟踪地目标放到跟踪层上，这样就只需要刷新跟踪图层即可实现动态跟踪。\n\n    - 当需要进行批量地往记录集中添加几何对象的时候，可以先将这些对象临时放在跟踪图层上，确定需要添加之后再把跟踪图层上的几何对象批量\n      地添加到记录集中。\n\n    请注意避免把跟踪图层作为存储大量临时几何对象的容器，如果有大量的临时数据，建议在本地计算机临时目录下（如：c:\temp）创建临时数据\n    源，并在临时数据源中创建相应的临时数据集来保存临时数据。\n\n    你可以对跟踪图层进行控制，包括控制跟踪图层是否可显示以及符号是否随图缩放。跟普通图层不同的是，跟踪图层中的对象是不保存的，只是在\n    地图显示时，临时存在内存中。当地图关闭后，跟踪图层中的对象依然存在，相应内存释放掉才会消失，当地图再次被打开后，跟踪图层又显示为\n    一个空白而且透明的图层。\n\n    该类提供了对跟踪图层上的几何对象进行添加，删除等管理的方法。并且可以通过设置标签的方式对跟踪图层上的几何对象进行分类，你可以将标\n    签理解为对几何对象的描述，相同用途的几何对象可以具有相同的标签。\n    '

    def __init__(self, java_object):
        JVMBase.__init__(self)
        self._java_object = java_object

    def add(self, geo, tag):
        """
        向当前跟踪图层中添加一个几何对象，并给出其标签信息。

        :param geo: 要添加的几何对象。
        :type geo: Rectangle or Geometry or Point2D or Feature
        :param str tag: 要添加的几何对象的标签。
        :return: 添加到跟踪图层的几何对象的索引。
        :rtype: int
        """
        if isinstance(geo, Rectangle):
            geo = geo.to_region()
        else:
            if isinstance(geo, Point2D):
                geo = GeoPoint(geo)
            else:
                if isinstance(geo, Feature):
                    geo = geo.geometry
                else:
                    if not isinstance(geo, Geometry):
                        raise ValueError('required Geometry')
                    if tag:
                        tag = str(tag)
                    else:
                        tag = ''
                return self._jobject.add(oj(geo), tag)

    def get_tag(self, index):
        """
        返回此跟踪图层中指定索引的几何对象的标签。

        :param int index: 要返回标签的几何对象的索引。
        :return: 此跟踪图层中指定索引的几何对象的标签。
        :rtype: str
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.getTag(index)

    def set_tag(self, index, tag):
        """
        设置此跟踪图层中指定索引的几何对象的标签

        :param int index: 要设置标签的几何对象的索引。
        :param str tag: 几何对象的新标签。
        :return: 设置成功返回 true；否则返回 false。
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.setTag(index, str(tag))

    def index_of(self, tag):
        """
        返回第一个与指定标签相同的几何对象所处的索引值。

        :param str tag: 需要进行索引检查的标签。
        :return: 返回第一个与指定标签相同的几何对象所处的索引值。
        :rtype: int
        """
        if tag:
            tag = str(tag)
        else:
            raise ValueError('tag required str')
        return self._jobject.indexOf(tag)

    def remove(self, index):
        """
        在当前跟踪图层中删除指定索引的几何对象。

        :param int index: 要删除的几何对象的索引。
        :return: 删除成功返回 true；否则返回 false。
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.remove(int(index))

    def clear(self):
        """
        清空此跟踪图层中的所有几何对象。

        :return: 对象自身
        :rtype: TrackingLayer
        """
        self._jobject.clear()
        return self

    def flush_bulk_edit(self):
        """
        批量更新时强制刷新并保存本次批量编辑的数据。

        :return: 强制刷新返回 true，否则返回 false。
        :rtype: bool
        """
        return self._jobject.flushBulkEdit()

    def start_edit_bulk(self):
        """
        开始批量更新

        :return: 对象自身
        :rtype: TrackingLayer
        """
        return self._jobject.setEditBulk(True)

    def finish_edit_bulk(self):
        """
        完成批量更新

        :return: 对象自身
        :rtype: TrackingLayer
        """
        self.flush_bulk_edit()
        self._jobject.setEditBulk(False)
        return self

    def get(self, index):
        """
        返回此跟踪图层中指定索引的几何对象。

        :param int index:
        :return: 指定索引的几何对象。
        :rtype: Geometry
        """
        if index < 0:
            index = index + self._jobject.getCount()
        geo = self._jobject.get(int(index))
        if geo:
            return Geometry._from_java_object(geo)

    def set(self, index, geo):
        """
        将跟踪图层中的指定的索引处的几何对象替换为指定的几何对象，若此索引处原先有其他几何对象，则会被删除。

        :param int index:  要替换几何对象的索引。
        :param geo: 用来替换的新 Geometry 对象。
        :type geo: Geometry or Point2D or Rectangle or Feature
        :return: 替换成功返回 true；否则返回 false。
        :rtype: bool
        """
        if isinstance(geo, Rectangle):
            geo = geo.to_region()
        else:
            if isinstance(geo, Point2D):
                geo = GeoPoint(geo)
            else:
                if isinstance(geo, Feature):
                    geo = geo.geometry
                else:
                    assert isinstance(geo, Geometry), 'required Geometry'
                if index < 0:
                    index = index + self._jobject.getCount()
                return self._jobject.set(int(index), oj(geo))

    def __len__(self):
        return self._jobject.getCount()

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def get_symbol_scale(self):
        """
        返回此跟踪图层的符号缩放基准比例尺。

        :return: 跟踪图层的符号缩放基准比例尺。
        :rtype: float
        """
        return self._jobject.getSymbolScale()

    def set_symbol_scale(self, value):
        """
        设置此跟踪图层的符号缩放基准比例尺。

        :param float value: 此跟踪图层的符号缩放基准比例尺。
        :return: 对象自身
        :rtype: TrackingLayer
        """
        if value:
            self._jobject.setSymbolScale(float(value))
        return self

    def is_antialias(self):
        """
        返回一个布尔值指定是否反走样跟踪图层。文本、线型被设置为反走样后，可以去除一些显示锯齿，使显示更加美观。如图分别为线型和文本
        反走样前和反走样后的效果对比

        :return: 反走样跟踪图层返回 true；否则返回 false。
        :rtype: bool
        """
        return self._jobject.isAntialias()

    def set_antialias(self, value):
        """
        设置一个布尔值指定是否反走样跟踪图层。

        :param bool value: 指定是否反走样跟踪图层。
        :return: 对象自身
        :rtype: TrackingLayer
        """
        if value:
            self._jobject.setAntialias(bool(value))
        return self

    def is_symbol_scalable(self):
        """
        返回跟踪图层的符号大小是否随图缩放。true 表示当随着地图的缩放而缩放，在地图放大的同时，符号同时也放大。

        :return: 一个布尔值指示跟踪图层的符号大小是否随图缩放。
        :rtype: bool
        """
        return self._jobject.isSymbolScalable()

    def set_symbol_scalable(self, value):
        """
        设置跟踪图层的符号大小是否随图缩放。true 表示当随着地图的缩放而缩放，在地图放大的同时，符号同时也放大。

        :param bool value: 一个布尔值指示跟踪图层的符号大小是否随图缩放。
        :return: 对象自身
        :rtype: TrackingLayer
        """
        self._jobject.setSymbolScalable(bool(value))
        return self

    def is_visible(self):
        """
        返回此跟踪图层是否可见。true 表示此跟踪图层可见，false 表示此跟踪图层不可见。当此跟踪图层不可见时，其他的设置都将无效。

        :return: 指示此图层是否可见。
        :rtype: bool
        """
        return self._jobject.isVisible()

    def set_visible(self, value):
        """
        设置此跟踪图层是否可见。true 表示此跟踪图层可见，false 表示此跟踪图层不可见。当此跟踪图层不可见时，其他的设置都将无效。

        :param bool value: 指示此图层是否可见。
        :return: 对象自身
        :rtype: TrackingLayer
        """
        self._jobject.setVisible(bool(value))
        return self


class Map(JVMBase):
    __doc__ = '\n    地图类，负责地图显示环境的管理。\n\n    地图是对地理数据的可视化，通常由一个或多个图层组成。地图必须与一个工作空间相关联，以便来显示该工作空间中的数据。另外，对地图的显\n    示方式的设置将对其中的所有图层起作用。该类提供了对地图的各种显示方式的返回和设置，如地图的显示范围，比例尺，坐标系统以及文本、点\n    等图层的默认显示方式等，并提供了对地图进行的相关操作的方法，如地图的打开与关闭，缩放、全幅显示，以及地图的输出等。\n    '

    def __init__(self):
        JVMBase.__init__(self)
        self._java_object = self._jvm.com.supermap.mapping.Map(oj(Workspace()))

    def open(self, name):
        """
        打开指定名称的地图。该指定名称为地图所关联的工作空间中的地图集合对象中的一个地图的名称，注意与地图的显示名称相区别。

        :param str name: 地图名称。
        :return:
        :rtype: bool
        """
        return self._jobject.open(str(name))

    def close(self):
        """
        关闭当前地图。
        """
        self._jobject.close()

    def set_image_size(self, width, height):
        """
        设置出图时图片的大小，以像素为单位。

        :param int width: 出图时图片的宽度
        :param int height: 出图时图片的高度
        :return: 对象自身
        :rtype: Map
        """
        if width:
            if height:
                dimension = self._jvm.java.awt.Dimension(int(width), int(height))
                self._jobject.setImageSize(dimension)
                return self
        raise ValueError('invalid input for width and height')

    def get_image_size(self):
        """
        返回出图时图片的大小，以像素为单位

        :return: 返回出图时图片的宽度和高度
        :rtype: tuple[int,int]
        """
        size = self._jobject.getImageSize()
        return (int(size.getWidth()), int(size.getHeight()))

    def set_dpi(self, dpi):
        """
        设置地图的DPI，代表每英寸有多少个像素，值域为(60，180)。

        :param float dpi: 图的DPI
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setDPI(float(dpi))
        return self

    def get_dpi(self):
        """
        返回地图的DPI，代表每英寸有多少个像素

        :return: 地图的DPI
        :rtype: float
        """
        return self._jobject.getDPI()

    def refresh(self, refresh_all=False):
        """
        重新绘制当前地图。

        :param bool refresh_all: 当 refresh_all 为 TRUE 时，在刷新地图时，同时刷新其中的快照图层。 快照图层，一种特殊的图层组，
                                 该图层组包含的图层作为地图的一个快照图层，采用特殊的绘制方式，快照图层只在第一次显示时进行绘制，
                                 此后，如果地图显示范围未发生变化，快照图层都将使用该显示，也就是快照图层不随地图刷新而重新绘制；
                                 如果地图显示范围发生变化，将自动触发快照图层的刷新绘制。快照图层是提高地图显示性能的手段之一。
                                 如果地图的显示范围不发生变化，刷新地图时，快照图层是不刷新的；如果需要强制刷新可以通过 refresh_all
                                 刷新地图便可以同时刷新快照图层。

        :return: 对象自身
        :rtype: Map
        """
        if refresh_all:
            self._jobject.refreshWithSnapshot()
        else:
            self._jobject.refresh()
        return self

    def refresh_tracking_layer(self):
        """
        用于刷新地图窗口中的跟踪图层。

        :return: 对象自身
        :rtype: Map
        """
        self._jobject.refreshTrackingLayer()
        return self

    def from_xml(self, xml, workspace_version=None):
        """
        根据指定的 XML 字符串创建地图对象。
        任何地图都可以导出成 xml 字符串，而地图的 xml 字符串也可以导入成为一个地图来显示。地图的 xml 字符串中存储了关于地图及其图
        层的显示设置以及关联的数据信息等。

        :param str xml: 用来创建地图的 xml 字符串。
        :param workspace_version: xml 内容所对应的工作空间的版本。使用该参数时，请确保指定的版本与 xml 内容相符。若不相符，可能会导致部分图层的风格丢失。
        :type workspace_version: WorkspaceVersion or str
        :return: 若地图对象创建成功，返回 true，否则返回 false。
        :rtype: bool
        """
        if workspace_version:
            workspace_version = WorkspaceVersion._make(workspace_version)
        if workspace_version:
            return self._jobject.fromXML(xml, oj(workspace_version))
        return self._jobject.fromXML(xml)

    def to_xml(self):
        """
        返回此地图对象的 XML 字符串形式的描述。
        任何地图都可以导出成 xml 字符串，而地图的 xml 字符串也可以导入成为一个地图来显示。地图的 xml 字符串中存储了关于地图及其图
        层的显示设置以及关联的数据信息等。此外，可以将地图的 xml 字符串保存成一个 xml 文件。

        :return: 地图的 XML 形式的描述
        :rtype: str
        """
        return self._jobject.toXML()

    def get_angle(self):
        """
        返回当前地图的旋转角度。单位为度，精度到 0.1 度。逆时针方向为正方向，如果用户输入负值，地图则以顺时针方向旋转。

        :return: 当前地图的旋转角度。
        :rtype: float
        """
        return self._jobject.getAngle()

    def set_angle(self, value):
        """
        设置当前地图的旋转角度。单位为度，精度到 0.1 度。逆时针方向为正方向，如果用户输入负值，地图则以顺时针方向旋转

        :param float value: 指定当前地图的旋转角度。
        :return: 对象自身
        :rtype: Map
        """
        if value:
            self._jobject.setAngle(float(value))
        return self

    def set_view_bounds(self, bounds):
        """
        设置当前地图的可见范围，也称显示范围。当前地图的可见范围除了可以通过 :py:meth:`set_view_bounds` 方法来进行设置，还可以通过设置显示范
        围的中心点（:py:meth:`set_center`）和显示比例尺（:py:meth:`set_scale`）的方式来进行设置。

        :param Rectangle bounds: 指定当前地图的可见范围。
        :return: 对象自身
        :rtype: Map
        """
        bounds = Rectangle.make(bounds)
        if isinstance(bounds, Rectangle):
            self._jobject.setViewBounds(oj(bounds))
            return self
        raise ValueError('Required Rectangle')

    def get_view_bounds(self):
        """
        返回当前地图的可见范围，也称显示范围。当前地图的可见范围除了可以通过 :py:meth:`set_view_bounds` 方法来进行设置，还可以通过设置显示范
        围的中心点（:py:meth:`set_center`）和显示比例尺（:py:meth:`set_scale`）的方式来进行设置。

        :return: 当前地图的可见范围。
        :rtype: Rectangle
        """
        return Rectangle._from_java_object(self._jobject.getViewBounds())

    def get_bounds(self):
        """
        返回当前地图的空间范围。地图的空间范围是其所显示的各数据集的范围的最小外接矩形，即包含各数据集范围的最小的矩形。当地图显示的数据集增加或删除时，其空间范围也会相应发生变化。

        :return: 当前地图的空间范围。
        :rtype: Rectangle
        """
        return Rectangle._from_java_object(self._jobject.getBounds())

    def get_prj(self):
        """
        返回地图的投影坐标系统

        :return: 地图的投影坐标系统。
        :rtype: PrjCoordSys
        """
        return PrjCoordSys._from_java_object(self._jobject.getPrjCoordSys())

    def set_prj(self, prj):
        """
        设置地图的投影坐标系统

        :param prj: 地图的投影坐标系统。
        :type prj: PrjCoordSys
        :return: 对象自身
        :rtype: Map
        """
        prj = PrjCoordSys.make(prj)
        if isinstance(prj, PrjCoordSys):
            self._jobject.setPrjCoordSys(oj(prj))
            return self
        raise ValueError('required PrjCoordSys')

    def get_scale(self):
        """
        返回当前地图的显示比例尺。

        :return: 当前地图的显示比例尺。
        :rtype: float
        """
        return self._jobject.getScale()

    def set_scale(self, scale):
        """
        设置当前地图的显示比例尺。

        :param float scale: 指定当前地图的显示比例尺。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setScale(float(scale))
        return self

    def get_min_scale(self):
        """
        返回地图的最小比例尺

        :return: 地图的最小比例尺。
        :rtype: float
        """
        return self._jobject.getMinScale()

    def set_min_scale(self, scale):
        """
        设置地图的最小比例尺。

        :param float scale: 地图的最小比例尺。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setMinScale(float(scale))
        return self

    def get_max_scale(self):
        """
        返回地图的最大比例尺。

        :return: 地图的最大比例尺。
        :rtype: float
        """
        return self._jobject.getMaxScale()

    def set_max_scale(self, scale):
        """
        设置地图的最大比例尺

        :param float scale:  地图的最大比例尺。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setMaxScale(float(scale))
        return self

    def get_clip_region(self):
        """
        返回地图显示裁剪的区域。
        用户可以任意设定一个地图显示的区域，该区域外的地图内容，将不会显示。

        :return: 地图显示裁剪的区域。
        :rtype: GeoRegion
        """
        clip_region = self._jobject.getClipRegion()
        if clip_region:
            return GeoRegion._from_java_object(clip_region)

    def set_clip_region(self, region):
        """
        设置地图显示裁剪的区域。
        用户可以任意设定一个地图显示的区域，该区域外的地图内容，将不会显示。

        :param region: 地图显示裁剪的区域。
        :type region: GeoRegion or Rectangle
        :return: 对象自身
        :rtype: Map
        """
        if isinstance(region, Rectangle):
            region = region.to_region()
        if isinstance(region, GeoRegion):
            self._jobject.setClipRegion(oj(region))
            return self
        raise ValueError('required GeoRegion')

    def is_clip_region_enabled(self):
        """
        返回地图显示裁剪区域是否有效，true 表示有效。

        :return: 地图显示裁剪区域是否有效
        :rtype: bool
        """
        return self._jobject.isClipRegionEnabled()

    def set_clip_region_enabled(self, value):
        """
        设置地图显示裁剪区域是否有效，true 表示有效。

        :param bool value: 显示裁剪区域是否有效。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setClipRegionEnabled(bool(value))
        return self

    def view_entire(self):
        """
        全幅显示此地图。

        :return: 对象自身
        :rtype: Map
        """
        self._jobject.viewEntire()
        return self

    def zoom(self, ratio):
        """
        将地图放大或缩小指定的比例。缩放之后地图的比例尺=原比例尺 *ratio，其中 ratio 必须为正数，当 ratio 为大于1时，地图被放大；
        当 ratio 小于1时，地图被缩小。

        :param float ratio: 缩放地图比例，此值不可以为负。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.zoom(float(ratio))
        return self

    def get_center(self):
        """
        返回当前地图的显示范围的中心点。

        :return: 地图的显示范围的中心点。
        :rtype: Point2D
        """
        return Point2D._from_java_object(self._jobject.getCenter())

    def set_center(self, center):
        """
        设置当前地图的显示范围的中心点。

        :param Point2D center: 当前地图的显示范围的中心点。
        :return: 对象自身
        :rtype: Map
        """
        center = Point2D.make(center)
        if isinstance(center, Point2D):
            self._jobject.setCenter(oj(center))
        else:
            raise ValueError('required Point2D')
        return self

    def get_color_mode(self):
        """
        返回当前地图的颜色模式。地图的颜色模式包括彩色模式，黑白模式，灰度模式以及黑白反色模式等，具体请参见 :py:class:`MapColorMode` 类。

        :return: 地图的颜色模式
        :rtype: MapColorMode
        """
        return MapColorMode._make(self._jobject.getColorMode().name())

    def set_color_mode(self, value):
        """
        设置当前地图的颜色模式

        :param value: 指定当前地图的颜色模式。
        :type value: str or MapColorMode
        :return: 对象自身
        :rtype: Map
        """
        value = MapColorMode._make(value)
        if isinstance(value, MapColorMode):
            self._jobject.setColorMode(oj(value))
        else:
            raise ValueError('required MapColorMode')
        return self

    def get_description(self):
        """
        返回当前地图的描述信息。

        :return: 当前地图的描述信息。
        :rtype: str
        """
        return self._jobject.getDescription()

    def set_description(self, value):
        """
        设置当前地图的描述信息。

        :param str value: 指定当前地图的描述信息。
        :return: 对象自身
        :rtype: Map
        """
        if value:
            self._jobject.setDescription(str(value))
        return self

    def is_dynamic_projection(self):
        """
        返回是否允许地图动态投影显示。地图动态投影显示是指如果当前地图窗口中地图的投影信息与数据源的投影信息不同，利用地图动态投影显
        示可以将当前地图的投影信息转换为数据源的投影信息。

        :return: 是否允许地图动态投影显示。
        :rtype: bool
        """
        return self._jobject.isDynamicProjection()

    def set_dynamic_projection(self, value):
        """
        设置是否允许地图动态投影显示。地图动态投影显示是指如果当前地图窗口中地图的投影信息与数据源的投影信息不同，利用地图动态投影显
        示可以将当前地图的投影信息转换为数据源的投影信息。

        :param bool value: 是否允许地图动态投影显示。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setDynamicProjection(bool(value))
        return self

    def get_dynamic_prj_trans_method(self):
        """
        返回地图动态投影时所使用的地理坐标系转换算法。默认值为 :py:attr:`CoordSysTransMethod.MTH_GEOCENTRIC_TRANSLATION`

        :return: 地图动态投影时所使用的投影算法
        :rtype: CoordSysTransMethod
        """
        method = self._jobject.getDynamicPrjTransMethod()
        if method:
            return CoordSysTransMethod._make(method.name())

    def set_dynamic_prj_trans_method(self, value):
        """
        设置地图动态投影时，当源投影与目标目标投影所基于的地理坐标系不同时，需要设置该转换算法。
        此处的投影算法不支持自定义算法，即：CoordSysTransMethod.MTH_EXTENTION。

        :param value: 地理坐标系转换算法
        :type value: CoordSysTransMethod or str
        :return: 对象自身
        :rtype: Map
        """
        value = CoordSysTransMethod._make(value)
        if isinstance(value, CoordSysTransMethod):
            self._jobject.setDynamicPrjTransMethod(oj(value))
            return self
        raise ValueError('required CoordSysTransMethod')

    def get_dynamic_prj_trans_parameter(self):
        """
        设置地图动态投影时，当源投影与目标目标投影所基于的地理坐标系不同时，可以通过该方法设置转换参数。

        :return: 动态投影坐标系的转换参数。
        :rtype: CoordSysTransParameter
        """
        parameter = self._jobject.getDynamicPrjTransParameter()
        if parameter:
            return CoordSysTransParameter._from_java_object(parameter)

    def set_dynamic_prj_trans_parameter(self, parameter):
        """
        设置动态投影坐标系的转换参数。

        :param CoordSysTransParameter parameter: 动态投影坐标系的转换参数。
        :return: 对象自身
        :rtype: Map
        """
        if isinstance(parameter, CoordSysTransParameter):
            self._jobject.setDynamicPrjTransParameter(oj(parameter))
            return self
        raise ValueError('required CoordSysTransParameter')

    def get_layers(self):
        """
        返回当前地图所包含的所有图层。

        :return: 当前地图所包含的所有图层对象。
        :rtype: list[Layer]
        """
        layers = self._jobject.getLayers()
        if layers:
            return [Layer(layers.get(i)) for i in range(0, layers.getCount())]

    def get_name(self):
        """
        返回当前地图的名称。

        :return: 当前地图的名称。
        :rtype: str
        """
        return self._jobject.getName()

    def set_name(self, name):
        """
        设置当前地图的名称。

        :param str name: 当前地图的名称。
        :return: 对象自身
        :rtype: Map
        """
        if name:
            self._jobject.setName(str(name))
            return self
        raise ValueError('name is None')

    def is_fill_marker_angle_fixed(self):
        """
        返回是否固定填充符号的填充角度。

        :return: 是否固定填充符号的填充角度。
        :rtype: bool
        """
        return self._jobject.isFillMarkerAngleFixed()

    def set_fill_marker_angle_fixed(self, value):
        """
        设置是否固定填充符号的填充角度。

        :param bool value:  是否固定填充符号的填充角度。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setFillMarkerAngleFixed(bool(value))
        return self

    def is_line_antialias(self):
        """
        返回是否地图线型反走样显示。

        :return: 是否地图线型反走样显示。
        :rtype: bool
        """
        return self._jobject.isLineAntialias()

    def set_line_antialias(self, value):
        """
        设置是否地图线型反走样显示。

        :param bool value:  是否地图线型反走样显示。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setLineAntialias(bool(value))
        return self

    def is_marker_angle_fixed(self):
        """
        返回一个布尔值指定点状符号的角度是否固定。针对地图中的所有点图层。

        :return: 用于指定点状符号的角度是否固定。
        :rtype: bool
        """
        return self._jobject.isMarkerAngleFixed()

    def set_mark_angle_fixed(self, value):
        """
        设置一个布尔值指定点状符号的角度是否固定。针对地图中的所有点图层。

        :param bool value: 指定点状符号的角度是否固定
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setMarkerAngleFixed(bool(value))
        return self

    def is_map_thread_drawing_enabled(self):
        """
        返回是否另启线程绘制地图元素，true表示另启线程绘制地图元素，可以提升大数据量地图的绘制性能。

        :return: 指示是否另启线程绘制地图元素，true表示另启线程绘制地图元素，可以提升大数据量地图的绘制性能。
        :rtype: bool
        """
        return self._jobject.isMapThreadDrawingEnabled()

    def set_map_thread_drawing_enabled(self, value):
        """
        设置是否另启线程绘制地图元素，true表示另启线程绘制地图元素，可以提升大数据量地图的绘制性能。

        :param bool value: 一个布尔值，指示是否另启线程绘制地图元素，true表示另启线程绘制地图元素，可以提升大数据量地图的绘制性能。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setMapThreadDrawingEnabled(bool(value))
        return self

    def is_use_system_dpi(self):
        """
        是否使用系统的 DPI

        :return: 是否使用系统 DPI
        :rtype: bool
        """
        return self._jobject.isUseSystemDPI()

    def set_use_system_dpi(self, value):
        """
        设置是否使用系统 DPI

        :param bool value: 是否使用系统 DPI。True，表示使用系统的DPI，False，表示使用地图的设置。
        :return: 对象自身
        :rtype: Map
        """
        self._jobject.setUseSystemDPI(bool(value))
        return self

    @staticmethod
    def _output_to_file(that_map, file_name, image_type, is_back_transparent):
        if image_type is ImageType.GIF:
            is_ok = oj(that_map).outputMapToGIF(file_name, is_back_transparent)
        else:
            if image_type is ImageType.BMP:
                is_ok = oj(that_map).outputMapToBMP(file_name)
            else:
                if image_type is ImageType.JPG:
                    is_ok = oj(that_map).outputMapToJPG(file_name)
                else:
                    if image_type is ImageType.PNG:
                        is_ok = oj(that_map).outputMapToPNG(file_name, is_back_transparent)
                    else:
                        if image_type is ImageType.TIFF:
                            is_ok = oj(that_map).outputMapToFile(file_name, oj(image_type), int(that_map.get_dpi()), oj(that_map.get_view_bounds()), is_back_transparent)
                        else:
                            if image_type is ImageType.PDF:
                                is_ok = oj(that_map).outputMapToPDF(file_name)
                            else:
                                raise ValueError('Unsupported image type ' + image_type.name)
        return is_ok

    def output_to_file(self, file_name, output_bounds=None, dpi=0, image_size=None, is_back_transparent=False, is_show_to_ipython=False):
        """
        将当前地图输出的文件中，支持 BMP, PNG, JPG, GIF, PDF, TIFF 文件。不保存跟踪图层。

        :param str file_name: 结果文件路径，必须带文件后缀名。
        :param image_size: 设置出图时图片的大小，以像素为单位。如果不设置，使用当前地图的 image_size，具体参考 :py:meth:`.get_image_size`
        :type image_size: tuple[int,int]
        :param Rectangle output_bounds: 地图输出范围。如果不设置，默认使用当前地图的视图范围，具体参考 :py:meth:`.get_view_bounds`
        :param int dpi: 地图的DPI，代表每英寸有多少个像素。如果不设置，默认使用当前地图的 DPI，具体参考 :py:meth:`.get_dpi`
        :param bool is_back_transparent: 是否背景透明。该参数仅在 type 参数设置为 GIF 和 PNG 类型时有效。
        :param bool is_show_to_ipython: 是否在 ipython 中显示。注意，只能在 jupyter python 环境中显示，所以需要 ipython 和
                                        jupyter 环境。只支持 PNG、JPG 和 GIF 在 jupyter 中显示。
        :return: 输出成功返回 True， 否则返回 False
        :rtype: bool
        """
        image_type = ImageType._make(str(file_name).split('.')[(-1)])
        if not isinstance(image_type, ImageType):
            raise ValueError('invalid image type ' + str(image_type))
        else:
            t_map = None
            if not output_bounds or output_bounds.is_empty():
                if dpi > 0 or isinstance(image_size, tuple):
                    t_map = Map()
                    t_map.from_xml(self.to_xml())
                    if dpi > 0:
                        t_map.set_use_system_dpi(False)
                        t_map.set_dpi(int(dpi))
                    if isinstance(image_size, tuple):
                        if len(image_size) > 1:
                            t_map.set_image_size(image_size[0], image_size[1])
                    if output_bounds:
                        t_map.set_view_bounds(Rectangle.make(output_bounds))
                    that_map = t_map
            that_map = self
        is_ok = Map._output_to_file(that_map, file_name, image_type, is_back_transparent)
        if is_ok:
            if image_type in (ImageType.JPG, ImageType.PNG, ImageType.GIF):
                if is_show_to_ipython:
                    width, height = that_map.get_image_size()
                    Map._show_to_ipython(file_name, width, height)
                if t_map:
                    t_map.close()
                return is_ok
        if t_map:
            t_map.close()
        return is_ok

    def output_tracking_layer_to_png(self, file_name, output_bounds=None, dpi=0, is_back_transparent=False, is_show_to_ipython=False):
        """
        将当前地图的跟踪图层输出为png 文件，在调用此接口前，用户可以通过 set_image_size 设置图片大小。

        :param str file_name: 结果文件路径，必须带文件后缀名。
        :param Rectangle output_bounds: 地图输出范围。如果不设置，默认使用当前地图的视图范围，具体参考 :py:meth:`.get_view_bounds`
        :param int dpi: 地图的DPI，代表每英寸有多少个像素。如果不设置，默认使用当前地图的 DPI，具体参考 :py:meth:`.get_dpi`
        :param bool is_back_transparent: 是否背景透明。
        :param bool is_show_to_ipython: 是否在 ipython 中显示。注意，只能在 jupyter python 环境中显示，所以需要 ipython 和
                                        jupyter 环境。
        :return: 输出成功返回 True， 否则返回 False
        :rtype: bool
        """
        if not output_bounds:
            output_bounds = self.get_view_bounds()
        else:
            output_bounds = Rectangle.make(output_bounds)
        is_ok = oj(self).outputTrackingLayerToPNG(file_name, is_back_transparent, dpi, oj(output_bounds))
        if is_ok:
            if is_show_to_ipython:
                width, height = self.get_image_size()
                Map._show_to_ipython(file_name, width, height)
        return is_ok

    def show_to_ipython(self):
        """
        将当前地图在 ipython 中显示，注意，只能在 jupyter python 环境中显示，所以需要 ipython 和 jupyter 环境

        :return: 显示成功返回 True，否则返回 False
        :rtype: bool
        """
        import tempfile
        temp_name = tempfile.mktemp('.png', 'mapping_show_temp')
        return self.output_to_file(temp_name, is_show_to_ipython=True)

    @staticmethod
    def _show_to_ipython(file_name, width, height):
        try:
            from IPython.display import Image, display
            display(Image(filename=file_name, width=width, height=height))
        except Exception:
            import traceback
            log_error(traceback.format_exc())

    def add_dataset(self, dataset, is_add_to_head=True, layer_setting=None):
        """
        添加数据集到地图中

        :param dataset: 被添加的数据集对象
        :type dataset: Dataset or DatasetVector or DatasetImage or DatasetGrid
        :param bool is_add_to_head: 是否添加到地图的最上层
        :param LayerSetting layer_setting: 地图图层设置对象
        :return: 添加成功返回图层对象，否则返回 None
        :rtype: Layer
        """
        dt = get_input_dataset(dataset)
        if not isinstance(dt, (DatasetVector, DatasetImage, DatasetGrid)):
            raise ValueError('Required DatasetVector, DatasetImage, DatasetGrid')
        elif isinstance(layer_setting, LayerSetting):
            layer = self._jobject.getLayers().add(oj(dt), oj(layer_setting), bool(is_add_to_head))
        else:
            layer = self._jobject.getLayers().add(oj(dt), bool(is_add_to_head))
        if layer:
            return Layer(layer)

    @property
    def tracking_layer(self):
        """TrackingLayer: 返回当前地图的跟踪图层对象"""
        java_tracking_layer = self._jobject.getTrackingLayer()
        if java_tracking_layer:
            return TrackingLayer(java_tracking_layer)
        raise RuntimeError('Failed to get TrackingLayer')

    def add_to_tracking_layer(self, geos, style=None, is_antialias=False, is_symbol_scalable=False, symbol_scale=None):
        """
        添加几何对象到跟踪图层

        :param geos: 需要添加的几何对象
        :type geos: list[Geometry] or list[Feature] or list[Point2D] or list[Rectangle]
        :param GeoStyle style: 几何对象的对象风格
        :param bool is_antialias: 是否反走样
        :param bool is_symbol_scalable: 跟踪图层的符号大小是否随图缩放
        :param float symbol_scale: 此跟踪图层的符号缩放基准比例尺
        :return: 当前地图对象的跟踪图层对象
        :rtype: TrackingLayer
        """
        if not isinstance(geos, (list, tuple)):
            geos = [
             geos]
        tracking_layer = self.tracking_layer
        if isinstance(geos, (list, tuple)):
            tracking_layer.set_antialias(is_antialias)
            tracking_layer.set_symbol_scalable(is_symbol_scalable)
            tracking_layer.set_symbol_scale(symbol_scale)
            tracking_layer.start_edit_bulk()
            for geo in geos:
                if isinstance(geo, Feature):
                    geo = geo.geometry
                else:
                    if isinstance(geo, Point2D):
                        geo = GeoPoint(geo)
                    else:
                        if isinstance(geo, Rectangle):
                            geo = geo.to_region()
                if isinstance(geo, Geometry):
                    if style:
                        geo.set_style(style)
                    tracking_layer.add(geo, str(geo.id))

            tracking_layer.finish_edit_bulk()
        return tracking_layer

    def clear_layers(self):
        """
        删除此图层集合对象中所有的图层。

        :return: 对象自身
        :rtype: Map
        """
        self._jobject.getLayers().clear()
        return self

    def is_contain_layer(self, layer_name):
        """
        判定此图层集合对象是否包含指定名称的图层。

        :param str layer_name: 可能包含在此图层集合中的图层对象的名称。
        :return: 若此图层中包含指定名称的图层则返回 true，否则返回 false。
        :rtype: bool
        """
        return self._jobject.getLayers().contains(str(layer_name))

    def find_layer(self, layer_name):
        """
        返回指定的图层名称的图层对象。

        :param str layer_name: 指定的图层名称。
        :return: 返回指定的图层名称的图层对象。
        :rtype: Layer
        """
        layer = self._jobject.getLayers().findLayer(str(layer_name))
        if layer:
            return Layer(layer)

    def get_layers_count(self):
        """
        返回此图层集合中图层对象的总数。

        :return: 此图层集合中图层对象的总数
        :rtype: int
        """
        return self._jobject.getLayers().getCount()

    def index_of_layer(self, layer_name):
        """
        返回此图层集合中指定名称的图层的索引。

        :param str layer_name:  要查找的图层的名称。
        :return: 找到指定图层则返回图层索引，否则返回-1。
        :rtype: int
        """
        return self._jobject.getLayers().indexOf(str(layer_name))

    def get_layer(self, index_or_name):
        """
        返回此图层集合中指定名称的图层对象。

        :param index_or_name: 图层的名称或索引
        :type index_or_name: str or int
        :return: 此图层集合中指定名称的图层对象。
        :rtype: Layer
        """
        if isinstance(index_or_name, int):
            if index_or_name < 0:
                index_or_name += self.get_layers_count()
            layer = self._jobject.getLayers().get(index_or_name)
            if layer:
                return Layer(layer)
            return
        layer = self._jobject.getLayers().get(str(index_or_name))
        if layer:
            return Layer(layer)
        return

    def remove_layer(self, index_or_name):
        """
        从此图层集合中删除一个指定名称的图层。删除成功则返回 true。

        :param index_or_name: 要删除图层的名称或索引
        :type index_or_name: str or int
        :return: 删除成功则返回 true，否则返回 false。
        :rtype: bool
        """
        if isinstance(index_or_name, int):
            if index_or_name < 0:
                index_or_name += self.get_layers_count()
            return self._jobject.getLayers().remove(index_or_name)
        if isinstance(index_or_name, Layer):
            return self._jobject.getLayers().remove(oj(index_or_name))
        return self._jobject.getLayers().remove(str(index_or_name))

    def move_layer_to(self, src_index, tag_index):
        """
        将此图层集合中的指定索引的图层移动到指定的目标索引。

        :param int src_index: 要移动图层的原索引
        :param int tag_index: 图层要移动到的目标索引。
        :return: 移动成功返回 true，否则返回 false。
        :rtype: bool
        """
        if src_index < 0:
            src_index += self.get_layers_count()
        if tag_index < 0:
            tag_index += self.get_layers_count()
        return self._jobject.getLayers().moveTo(int(src_index), int(tag_index))

    def add_heatmap(self, dataset, kernel_radius, max_color=None, min_color=None):
        """
        根据给定的点数据集和参数设置制作一幅热力图，也就是将给定的点数据以热力图的渲染方式进行显示。
        热力图是通过颜色分布，描述诸如人群分布、密度和变化趋势等的一种地图表现手法，因此，能够非常直观地呈现一些原本不易理解或表达的数据，比如密度、频度、温度等。
        热力图图层除了可以反映点要素的相对密度，还可以表示根据属性进行加权的点密度，以此考虑点本身的权重对于密度的贡献。

        :param dataset: 参与制作热力图的数据，该数据必须为点矢量数据集。
        :type dataset: DatasetVector
        :param int kernel_radius: 用于计算密度的查找半径。
        :param max_color: 低点密度的颜色。热力图图层将通过高点密度颜色（maxColor）和低点密度颜色（minColor）确定渐变的颜色方案。
        :type max_color: Color or tuple[int,int,int]
        :param min_color: 高点密度的颜色。热力图图层将通过高点密度颜色（maxColor）和低点密度颜色（minColor）确定渐变的颜色方案。
        :type min_color: Color or tuple[int,int,int]
        :return: 热力图图层对象
        :rtype: LayerHeatmap
        """
        dt = get_input_dataset(dataset)
        if not isinstance(dt, DatasetVector) or dt.type is not DatasetType.POINT:
            raise ValueError('Required Point Dataset')
        if min_color and max_color:
            layer = self._jobject.getLayers().AddHeatmap(oj(dt), int(kernel_radius), to_java_color(min_color), to_java_color(max_color))
        else:
            layer = self._jobject.getLayers().AddHeatmap(oj(dt), int(kernel_radius))
        if layer:
            return LayerHeatmap(layer)

    def add_aggregation(self, dataset, max_color=None, min_color=None):
        """
        根据给定的点数据集制作一幅默认风格的网格聚合图。

        :param dataset: 参与制作网格聚合图的数据，该数据必须为点矢量数据集。
        :type dataset: DatasetVector
        :param max_color: 网格单元统计值最大值对应的颜色，网格聚合图将通过maxColor和minColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。
        :type max_color: Color or tuple[int,int,int]
        :param min_color:  网格单元统计值最小值对应的颜色，网格聚合图将通过maxColor和minColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。
        :type min_color: Color or tuple[int,int,int]
        :return: 网格聚合图图层对象。
        :rtype: LayerGridAggregation
        """
        dt = get_input_dataset(dataset)
        if not isinstance(dt, DatasetVector) or dt.type is not DatasetType.POINT:
            raise ValueError('Required Point Dataset')
        if min_color and max_color:
            layer = self._jobject.getLayers().AddGridAggregation(oj(dt), to_java_color(min_color), to_java_color(max_color))
        else:
            layer = self._jobject.getLayers().AddGridAggregation(oj(dt))
        if layer:
            return LayerGridAggregation(layer)