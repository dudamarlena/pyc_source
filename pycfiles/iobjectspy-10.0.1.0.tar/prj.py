# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\prj.py
# Compiled at: 2019-12-31 04:08:58
# Size of source mod 2**32: 78254 bytes
from .._logger import log_error
from ..enums import PrjCoordSysType, GeoSpheroidType, GeoCoordSysType, GeoDatumType, ProjectionType, CoordSysTransMethod, GeoSpatialRefType, GeoPrimeMeridianType, Unit
from .._gateway import get_jvm
from ._jvm import JVMBase
from .ex import ObjectDisposedError
from .geo import Geometry, Point2D
__all__ = [
 'PrjCoordSys', 'GeoCoordSys', 'GeoDatum', 'GeoSpheroid', 'GeoPrimeMeridian', 'Projection', 'PrjParameter',
 'CoordSysTransParameter', 'CoordSysTranslator']

class PrjCoordSys(JVMBase):
    __doc__ = '\n    投影坐标系类。投影坐标系统由地图投影方式、投影参数、坐标单位和地理坐标系组成。SuperMap Objects Java 中提供了很多预定义的投影系统，用户可以\n    直接使用，此外，用户还可以定制自己投影系统。投影坐标系是定义在二维平面上的，不同于地理坐标系用经纬度定位地面点，投影坐标系是用 X、Y 坐标来定位\n    的。每一个投影坐标系都基于一个地理坐标系。\n    '

    def __init__(self, prj_type=None):
        """
        构造投影坐标系对象

        :param prj_type: 投影坐标系类型
        :type prj_type: PrjCoordSysType or str
        """
        JVMBase.__init__(self)
        _prj = PrjCoordSysType._make(prj_type)
        if _prj is not None:
            self._java_object = self._jvm.com.supermap.data.PrjCoordSys(_prj._jobject)

    def __getstate__(self):
        return self.to_xml()

    def __setstate__(self, state):
        self.__init__()
        self.from_xml(state)

    def clone(self):
        """
        拷贝一个对象

        :rtype: PrjCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return PrjCoordSys().from_xml(self.to_xml())

    def _make_java_object(self):
        if self._java_object is None:
            self._java_object = self._jvm.com.supermap.data.PrjCoordSys()
        return self._java_object

    @staticmethod
    def _from_java_object(java_prj):
        if java_prj is None:
            return
        prj = PrjCoordSys()
        prj._java_object = java_prj
        return prj

    @property
    def name(self):
        """str: 投影坐标系对象的名称"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return self._jobject.getName()

    def set_name(self, name):
        """设置投影坐标系对象的名称

        :param str name: 投影坐标系对象的名称
        :return: self
        :rtype: PrjCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        self._jobject.setName(name)
        return self

    @property
    def type(self):
        """PrjCoordSysType: 投影坐标系类型"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return PrjCoordSysType._make(self._jobject.getType().name())

    def set_type(self, prj_type):
        """
        设置投影坐标系类型

        :param prj_type: 投影坐标系类型
        :type prj_type: PrjCoordSysType or str
        :return: self
        :rtype: PrjCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        self._jobject.setType(PrjCoordSysType._make(prj_type)._jobject)
        return self

    @property
    def coord_unit(self):
        """
        Unit: 返回投影系统坐标单位。投影系统的坐标单位与距离单位（distance_unit）可以不同，例如经纬度坐标下的坐标单位是度，距离单位可以是米、
        公里等；即使是普通平面坐标或者投影坐标，这两个单位同样可不同。
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return Unit._make(self._jobject.getCoordUnit().name())

    @property
    def distance_unit(self):
        """Unit: 距离（长度）单位"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return Unit._make(self._jobject.getDistanceUnit().name())

    @staticmethod
    def from_epsg_code(code):
        """
        由 EPSG 编码构造投影坐标系对象

        :param int code: EPSG 编码
        :rtype: PrjCoordSys
        """
        try:
            java_prj = get_jvm().com.supermap.data.PrjCoordSys()
            if java_prj.fromEPSGCode(code):
                return PrjCoordSys._from_java_object(java_prj)
            return
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def to_epsg_code(self):
        """
        返回当前对象的 EPSG 编码

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        try:
            return self._jobject.toEPSGCode()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def from_file(self, file_path):
        """
        从 xml 文件或 prj 文件中读取投影坐标信息

        :param str file_path: 文件路径
        :return: 构建成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        else:
            files = file_path
            if files.lower().endswith('.prj'):
                prjFileType = self._jvm.com.supermap.data.PrjFileType.ESRI
            else:
                if files.lower().endswith('.xml'):
                    prjFileType = self._jvm.com.supermap.data.PrjFileType.SUPERMAP
                else:
                    raise ValueError('invalid filePath, must be prj or xml file')
        return self._jobject.fromFile(file_path, prjFileType)

    def to_file(self, file_path):
        """将投影坐标信息输出到文件中。只支持输出为 xml 文件。

        :param str file_path:  XML 文件的全路径。
        :return: 导出成功返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return self._jobject.toFile(file_path, self._jvm.com.supermap.data.PrjFileVersion.UGC60)

    def from_xml(self, xml):
        """
        从 xml 字符串中读取投影信息

        :param str xml: xml 字符串
        :return: 如果构建成功返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return self._jobject.fromXML(xml)

    def to_xml(self):
        """
        将投影坐标系类的对象转换为 XML 格式的字符串。

        :return: 表示投影坐标系类的对象的 XML 字符串
        :rtype: str
        """
        return self._jobject.toXML()

    @staticmethod
    def from_wkt(wkt):
        """
        从 WKT 字符串中构建投影坐标系对象

        :param str wkt: WKT 字符串
        :rtype: PrjCoordSys
        """
        try:
            java_prj = get_jvm().com.supermap.data.Toolkit.FromWKT(wkt)
            if java_prj is not None:
                return PrjCoordSys._from_java_object(java_prj)
            return
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def to_wkt(self):
        """
        将当前投影信息输出为 WKT 字符串

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return get_jvm().com.supermap.data.Toolkit.ToWKT(self._jobject)

    def set_geo_coordsys(self, geo_coordsys):
        """
        设置投影坐标系的地理坐标系统对象。每个投影系都要依赖于一个地理坐标系。该方法仅在坐标系类型为自定义投影坐标系和自定义地理坐标系时有效。

        :param GeoCoordSys geo_coordsys:
        :return: self
        :rtype: PrjCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        if geo_coordsys is not None:
            self._jobject.setGeoCoordSys(geo_coordsys._jobject)
        return self

    @property
    def geo_coordsys(self):
        """GeoCoordSys: 投影坐标系的地理坐标系统对象"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return GeoCoordSys._from_java_object(self._jobject.getGeoCoordSys())

    def set_prj_parameter(self, parameter):
        """
        设置投影坐标系统对象的投影参数。

        :param PrjParameter parameter: 投影坐标系统对象的投影参数
        :return: self
        :rtype: PrjCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        if parameter is not None:
            self._jobject.setPrjParameter(parameter._jobject)
        return self

    @property
    def prj_parameter(self):
        """PrjParameter: 投影坐标系统对象的投影参数"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return PrjParameter._from_java_object(self._jobject.getPrjParameter())

    @property
    def projection(self):
        """Projection: 投影坐标系统的投影方式。投影方式如等角圆锥投影、等距方位投影等等。 """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        return Projection._from_java_object(self._jobject.getProjection())

    def set_projection(self, projection):
        """
        设置投影坐标系统的投影方式。投影方式如等角圆锥投影、等距方位投影等等。

        :param Projection projection:
        :return: self
        :rtype: PrjCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjCoordSys')
        if projection is not None:
            self._jobject.setProjection(projection._jobject)
        return self

    @staticmethod
    def make(prj):
        """
        构造 PrjCoordSys 对象，支持从 epsg 编码，PrjCoordSysType 类型，xml 或者 wkt，或者投影信息文件中构造。注意，如果传入整型值，
        必须是 epsg 编码，不能是 PrjCoordSysType 类型的整型值。

        :param prj: 投影信息
        :type prj: int or str or PrjCoordSysType
        :return: 投影对象
        :rtype: PrjCoordSys
        """
        if prj is None:
            return
        if isinstance(prj, PrjCoordSys):
            return prj
        if isinstance(prj, PrjCoordSysType):
            return PrjCoordSys(prj)
        if isinstance(prj, int):
            return PrjCoordSys.from_epsg_code(prj)
        if isinstance(prj, str):
            try:
                temp_prj_type = PrjCoordSysType._make(prj)
                if temp_prj_type is not None:
                    return PrjCoordSys(temp_prj_type)
                temp_prj = None
            except:
                temp_prj = None

            try:
                temp_prj = PrjCoordSys()
                if temp_prj.from_xml(prj):
                    return temp_prj
            except:
                pass

            try:
                temp_prj = PrjCoordSys.from_wkt(prj)
                if temp_prj is not None:
                    return temp_prj
            except:
                pass

            try:
                temp_prj = PrjCoordSys()
                if temp_prj.from_file(prj):
                    return temp_prj
            except:
                temp_prj = None

            return temp_prj
        return


class GeoCoordSys(JVMBase):
    __doc__ = '\n    地理坐标系类。\n\n    地理坐标系由大地参照系、中央子午线、坐标单位组成。在地理坐标系中，单位一般用度来表示，也可以用度分秒表示。东西向（水平方向）的范围为-180度至180\n    度。南北向（垂直方向）的范围为-90度至90度。\n\n    地理坐标是用经纬度表示地面点位置的球面坐标。在球形系统中，赤道面的平行面同地球椭球面相交所截的圈称为纬圈，也叫纬线，表示东西方向，通过地球旋转轴\n    的面与椭球面相交所截的圈为子午圈，也称经线，表示南北方向，这些包围着地球的网格称为经纬格网。\n\n    经纬线一般用度来表示（必要时也用度分秒表示）。经度是指地面上某点所在的经线面与本初子午面所成的二面角，规定本初子午线的经度为 0 度，从本初子午线\n    向东 0 到 180 度为“东经”，以“E”表示，向西 0 到 -180 度为“西经”，以字母“W”表示；纬度是指地面上某点与地球球心的连线和赤道面所成的线面角，规\n    定赤道的纬度为 0 度，从赤道向北 0 到 90 度为“北纬”，以字母“N”表示，向南 0 到 -90 度为“南纬”，以字母“S”表示。\n\n    '

    def __init__(self):
        JVMBase.__init__(self)

    def __getstate__(self):
        return self.to_xml()

    def __setstate__(self, state):
        self.__init__()
        self.from_xml(state)

    def clone(self):
        """
        复制对象

        :rtype: GeoCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        return GeoCoordSys().from_xml(self.to_xml())

    def _make_java_object(self):
        if self._java_object is None:
            self._java_object = self._jvm.com.supermap.data.GeoCoordSys()
        return self._java_object

    @staticmethod
    def _from_java_object(java_prj):
        if java_prj is None:
            return
        prj = GeoCoordSys()
        prj._java_object = java_prj
        return prj

    @property
    def type(self):
        """
        GeoCoordSysType: 返回地理坐标系类型
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        return GeoCoordSysType._make(self._jobject.getType().name())

    def set_type(self, coord_type):
        """
        设置地理坐标系类型

        :param coord_type: 地理坐标系类型
        :type coord_type: GeoCoordSysType or str
        :return: self
        :rtype: GeoCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        self._jobject.setType(GeoCoordSysType._make(coord_type)._jobject)
        return self

    @property
    def geo_spatial_ref_type(self):
        """
        GeoSpatialRefType: 返回空间坐标系类型。
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        return GeoSpatialRefType._make(self._jobject.getGeoSpatialRefType().name())

    def set_geo_spatial_ref_type(self, spatial_ref_type):
        """
        设置空间坐标系类型。

        :param spatial_ref_type: 空间坐标系类型
        :type spatial_ref_type: GeoSpatialRefType or str
        :return: self
        :rtype: GeoCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        self._jobject.setGeoSpatialRefType(GeoSpatialRefType._make(spatial_ref_type)._jobject)
        return self

    @property
    def name(self):
        """
        str:  返回地理坐标系对象的名称
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        return self._jobject.getName()

    def set_name(self, name):
        """
        设置地理坐标系对象的名称

        :param str name: 地理坐标系对象的名称
        :return: self
        :rtype: GeoCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        if name is not None:
            self._jobject.setName(name)
        return self

    @property
    def geo_datum(self):
        """
        GeoDatum: 返回大地参照系对象
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        return GeoDatum._from_java_object(self._jobject.getGeoDatum())

    def set_geo_datum(self, datum):
        """
        设置大地参照系对象

        :param GeoDatum datum:
        :return: self
        :rtype: GeoCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        if datum is not None:
            self._jobject.setGeoDatum(datum._jobject)
        return self

    @property
    def geo_prime_meridian(self):
        """
        GeoPrimeMeridian: 返回中央子午线对象
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        return GeoPrimeMeridian._from_java_object(self._jobject.getGeoPrimeMeridian())

    def set_geo_prime_meridian(self, prime_meridian):
        """
        设置中央子午线对象

        :param GeoPrimeMeridian prime_meridian:
        :return: self
        :rtype: GeoCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        if prime_meridian is not None:
            self._jobject.setGeoPrimeMeridian(prime_meridian._jobject)
        return self

    @property
    def coord_unit(self):
        """
        Unit: 返回地理坐标系的单位。默认值为 DEGREE
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        return Unit._make(self._jobject.getCoordUnit().name())

    def set_coord_unit(self, unit):
        """
        设置地理坐标系的单位。

        :param unit: 地理坐标系的单位
        :type unit: Unit or str
        :return: self
        :rtype: GeoCoordSys
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        if unit is not None:
            self._jobject.setCoordUnit(Unit._make(unit)._jobject)
        return self

    def to_xml(self):
        """
        将地理坐标系类的对象转换为 XML 格式的字符串。

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        return self._jobject.toXML()

    def from_xml(self, xml):
        """
        从指定的 XML 字符串中构建地理坐标系类的对象，成功返回 True

        :param str xml: XML 字符串
        :rtype:  bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoCoordSys')
        return self._jobject.fromXML(xml)


class GeoDatum(JVMBase):
    __doc__ = '\n    大地参照系类。\n    该类包含有地球椭球参数。\n    地球椭球体仅仅是描述了地球的大小及形状，为了更准确地描述地球上的地物的具体位置，需要引入大地参照系。大地参照系确定了地球椭球体相对于地球球心的位置，为地表地物的测量提供了一个参照框架，确定了地表经纬网线的原点和方向。大地参照系把地球椭球体的球心当作原点。一个地区的大地参照系的地球椭球体或多或少地偏移了真正的地心，地表上的地物坐标都是相对于该椭球体的球心的。目前被广泛利用的是 WGS84，它被当着大地测量的基本框架。不同的大地参照系适用于不同的国家和地区，一个大地参照系并不适合于所有的地区。\n    '

    def __init__(self, datum_type=None):
        """
        构造大地参照系对象

        :param datum_type: 大地参照系类型
        :type datum_type: GeoDatumType or str
        """
        JVMBase.__init__(self)
        if datum_type is not None:
            java_datum = self._jvm.com.supermap.data.GeoDatum(GeoDatumType._make(datum_type)._jobject)
            if java_datum is not None:
                self._java_object = java_datum

    def __getstate__(self):
        return self.to_xml()

    def __setstate__(self, state):
        self.__init__()
        self.from_xml(state)

    def clone(self):
        """
        复制对象

        :rtype: GeoDatum
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoDatum')
        return GeoDatum().from_xml(self.to_xml())

    def _make_java_object(self):
        if self._java_object is None:
            self._java_object = self._jvm.com.supermap.data.GeoDatum()
        return self._java_object

    @staticmethod
    def _from_java_object(java_prj):
        if java_prj is None:
            return
        prj = GeoDatum()
        prj._java_object = java_prj
        return prj

    @property
    def name(self):
        """str: 大地参照系对象的名称"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoDatum')
        return self._jobject.getName()

    def set_name(self, name):
        """
        设置大地参照系对象的名称

        :param str name: 大地参照系对象的名称
        :return: self
        :rtype:  GeoDatum
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoDatum')
        if name is not None:
            self._jobject.setName(name)
        return self

    def from_xml(self, xml):
        """
        据 XML 字符串构建 GeoDatum 对象，成功返回 True。

        :param str xml:
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoDatum')
        return self._jobject.fromXML(xml)

    def to_xml(self):
        """
        将大地参照系类的对象转换为 XML 格式的字符串

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoDatum')
        return self._jobject.toXML()

    @property
    def type(self):
        """GeoDatumType: 大地参照系的类型"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoDatum')
        return GeoDatumType._make(self._jobject.getType().name())

    def set_type(self, datum_type):
        """
        设置大地参照系的类型。
        当大地参照系为自定义时，用户需另外指定椭球体参数；其它的值为系统预定义，用户不必指定椭球体参数。参见 :py:class:`GeoDatumType` 。

        :param datum_type: 大地参照系的类型
        :type datum_type: GeoDatumType or str
        :return: self
        :rtype: GeoDatum
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoDatum')
        if datum_type is not None:
            self._jobject.setType(GeoDatumType._make(datum_type)._jobject)
        return self

    @property
    def geo_spheroid(self):
        """GeoSpheroid: 地球椭球体对象"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoDatum')
        return GeoSpheroid._from_java_object(self._jobject.getGeoSpheroid())

    def set_geo_spheroid(self, geo_spheroid):
        """
        设置地球椭球体对象。只当大地参照系类型为自定义类型时才可以设置。
        人们通常用球体或椭球体来描述地球的形状和大小，有时为了计算方便，可以将地球看作一个球体，但更多的时候是把它看作椭球体。一般情况下在地图比例尺
        小于1：1,000,000 时，假设地球形状为一球体，因为在这种比例尺下球体和椭球体的差别几乎无法分辨；而在1：1,000,000 甚至更高精度要求的大比例
        尺时，则需用椭球体逼近地球。椭球体是以椭圆为基础的，所以用两个轴来表述地球球体的大小，即长轴（赤道半径）和短轴（极地半径）。

        :param GeoSpheroid geo_spheroid: 地球椭球体对象
        :return: self
        :rtype: GeoSpheroid
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoDatum')
        if geo_spheroid is not None:
            self._jobject.setGeoSpheroid(geo_spheroid._jobject)
        return self


class GeoSpheroid(JVMBase):
    __doc__ = '\n    地球椭球体参数类。 该类主要用来描述地球的长半径和扁率。\n\n    人们通常用球体或椭球体来描述地球的形状和大小，有时为了计算方便，可以将地球看作一个球体，但更多的时候是把它看作椭球体。一般情况下在地图比例尺小\n    于1：1,000,000 时，假设地球形状为一球体，因为在这种比例尺下球体和椭球体的差别几乎无法分辨；而在1：1,000,000 甚至更高精度要求的大比例尺时，\n    则需用椭球体逼近地球。椭球体是以椭圆为基础的，所以用两个轴来表述地球球体的大小，即长轴（赤道半径）和短轴（极地半径）。\n\n    因为同一个投影方法，不同的椭球体参数，相同的数据投影出来的结果可能相差很大，所以需要选择合适的椭球参数。不同年代、不同国家和地区使用的地球椭球参\n    数有可能不同，中国目前主要用的是克拉索夫斯基椭球参数；北美大陆及英法等主要用的是克拉克椭球参数。\n    '

    def __init__(self, spheroid_type=None):
        """
        构造地球椭球体参数类对象

        :param spheroid_type: 地球椭球体参数对象类型
        :type spheroid_type: GeoSpheroidType or str
        """
        JVMBase.__init__(self)
        if spheroid_type is not None:
            java_spheroid = self._jvm.com.supermap.data.GeoSpheroid(GeoSpheroidType._make(spheroid_type)._jobject)
            if java_spheroid is not None:
                self._java_object = java_spheroid

    def __getstate__(self):
        return self.to_xml()

    def __setstate__(self, state):
        self.__init__()
        self.from_xml(state)

    def clone(self):
        """
        复制对象

        :rtype: GeoSpheroid
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        return GeoSpheroid().from_xml(self.to_xml())

    def _make_java_object(self):
        if self._java_object is None:
            self._java_object = self._jvm.com.supermap.data.GeoSpheroid()
        return self._java_object

    @staticmethod
    def _from_java_object(java_prj):
        if java_prj is None:
            return
        prj = GeoSpheroid()
        prj._java_object = java_prj
        return prj

    @property
    def name(self):
        """str: 地球椭球体对象的名称"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        return self._jobject.getName()

    def set_name(self, name):
        """
        设置地球椭球体对象的名称

        :param str name: 地球椭球体对象的名称
        :return: self
        :rtype: GeoSpheroid
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        self._jobject.setName(name)
        return self

    def from_xml(self, xml):
        """
        从指定的 XML 字符串中构建地球椭球体参数类的对象。

        :param str xml: XML 字符串
        :return:  如果构建成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        return self._jobject.fromXML(xml)

    def to_xml(self):
        """
        将地球椭球参数类的对象转换为 XML 格式的字符串。

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        return self._jobject.toXML()

    @property
    def type(self):
        """GeoSpheroidType: 返回地球椭球体的类型"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        return GeoSpheroidType._make(self._jobject.getType().name())

    def set_type(self, spheroid_type):
        """
        设置地球椭球体的类型。该地球椭球体类型为自定义类型时，用户需另外指定椭球体的长半径和扁率；其余的值为系统预定义，用户不必指定长半径和扁率。
        可参见地球椭球体 :py:class:`GeoSpheroidType` 枚举类。

        :param spheroid_type:
        :type spheroid_type: GeoSpheroidType or str
        :return: self
        :rtype: GeoSpheroid
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        if spheroid_type is not None:
            self._jobject.setType(GeoSpheroidType._make(spheroid_type)._jobject)
        return self

    @property
    def axis(self):
        """float: 返回地球椭球体的长半径"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        return self._jobject.getAxis()

    def set_axis(self, value):
        """
        设置地球椭球体的长半径。地球椭球体的长半径也叫地球赤道半径，通过它和地球扁率可以求得地球椭球体的极地半径、第一偏心率、第二偏心率等等。只当
        地球椭球体的类型为自定义类型时，长半径才可以被设置。

        :param float value: 地球椭球体的长半径
        :return: self
        :rtype:  GeoSpheroid
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        if value is not None:
            self._jobject.setAxis(float(value))
        return self

    @property
    def flatten(self):
        """float: 返回地球椭球体的扁率"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        return self._jobject.getFlatten()

    def set_flatten(self, value):
        """
        设置地球椭球体的扁率。只当地球椭球体的类型为自定义类型时，扁率才可以被设置。地球椭球体的扁率反映了地球椭球体的圆扁情况， 一般为地球长短半轴
        之差与长半轴之比。

        :param float value:
        :return: self
        :rtype: GeoSpheroid
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoSpheroid')
        if value is not None:
            self._jobject.setFlatten(value)
        return self


class GeoPrimeMeridian(JVMBase):
    __doc__ = '\n    中央子午线类。\n    该对象主要应用于地理坐标系中，地理坐标系由三部分组成：中央子午线、参照系或者大地基准（Datum）和角度单位。\n\n    '

    def __init__(self, meridian_type=None):
        """
        构造中央子午线对象

        :param meridian_type:  中央经线类型
        :type meridian_type:  GeoPrimeMeridianType or str
        """
        JVMBase.__init__(self)
        if meridian_type is not None:
            java_meridian = self._jvm.com.supermap.data.GeoPrimeMeridian(GeoPrimeMeridianType._make(meridian_type)._jobject)
            if java_meridian is not None:
                self._java_object = java_meridian

    def __getstate__(self):
        return self.to_xml()

    def __setstate__(self, state):
        self.__init__()
        self.from_xml(state)

    def clone(self):
        """
        复制对象

        :rtype: GeoPrimeMeridian
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoPrimeMeridian')
        return GeoPrimeMeridian().from_xml(self.to_xml())

    def _make_java_object(self):
        if self._java_object is None:
            self._java_object = self._jvm.com.supermap.data.GeoPrimeMeridian()
        return self._java_object

    @staticmethod
    def _from_java_object(java_prj):
        if java_prj is None:
            return
        prj = GeoPrimeMeridian()
        prj._java_object = java_prj
        return prj

    @property
    def name(self):
        """str: 中央经线对象的名称"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoPrimeMeridian')
        return self._jobject.getName()

    def set_name(self, name):
        """
        设置中央经线对象的名称

        :param str name: 中央经线对象的名称
        :return: self
        :rtype:  GeoPrimeMeridian
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoPrimeMeridian')
        if name is not None:
            self._jobject.setName(name)
        return self

    @property
    def longitude_value(self):
        """float: 中央经线值，单位为度"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoPrimeMeridian')
        return self._jobject.getLongitudeValue()

    def set_longitude_value(self, value):
        """
        设置中央经线值，单位为度

        :param float value: 中央经线值，单位为度
        :return: self
        :rtype: GeoPrimeMeridian
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoPrimeMeridian')
        if value is not None:
            self._jobject.setLongitudeValue(float(value))
        return self

    @property
    def type(self):
        """GeoPrimeMeridianType: 中央经线类型"""
        if self._jobject is None:
            raise ObjectDisposedError('GeoPrimeMeridian')
        return GeoPrimeMeridianType._make(self._jobject.getType().name())

    def set_type(self, meridian_type):
        """
        设置中央经线类型

        :param meridian_type: 中央经线类型
        :type meridian_type: GeoPrimeMeridianType or str
        :return: self
        :rtype: GeoPrimeMeridian
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoPrimeMeridian')
        if meridian_type is not None:
            self._jobject.setType(GeoPrimeMeridianType._make(meridian_type)._jobject)
        return self

    def from_xml(self, xml):
        """
        指定的 XML 字符串构建 GeoPrimeMeridian 对象

        :param str xml: XML 字符串
        :return:
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoPrimeMeridian')
        if xml is not None:
            return self._jobject.fromXML(xml)
        return False

    def to_xml(self):
        """
        返回表示 GeoPrimeMeridian 对象的 XML 字符串

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError('GeoPrimeMeridian')
        return self._jobject.toXML()


class Projection(JVMBase):
    __doc__ = '\n    投影坐标系地图投影类。 地图投影就是将球面坐标转化为平面坐标的过程。\n\n    一般来说，地图投影按变形性质可以分为等角投影、等距投影和等积投影，适于不同的用途，如果是航海图，等角投影是很常用。还有一种是各类变形介于这几种之\n    间的任意投影，一般用作参考用途和教学地图。地图投影也可以按照构成方法分成两大类，分别为几何投影和非几何投影。几何投影是把椭球面上的经纬线网投影到\n    几何面上，然后将几何面展为平面而得的，包括方位投影、圆柱投影和圆锥投影；非几何投影不借助几何面，根据某些条件有数学解析法确定球面与平面之间点与点\n    的函数关系，包括伪方位投影、伪圆柱投影、伪圆锥投影和多圆锥投影。有关投影方式类型的详细信息请参考 :py:class:`ProjectionType`\n    '

    def __init__(self, projection_type=None):
        """

        :param projection_type:
        :type projection_type: ProjectionType or str
        """
        JVMBase.__init__(self)
        if projection_type is not None:
            java_projection = self._jvm.com.supermap.data.Projection(ProjectionType._make(projection_type)._jobject)
            if java_projection is not None:
                self._java_object = java_projection

    def __getstate__(self):
        return self.to_xml()

    def __setstate__(self, state):
        self.__init__()
        self.from_xml(state)

    def clone(self):
        """
        复制对象

        :rtype: Projection
        """
        if self._jobject is None:
            raise ObjectDisposedError('Projection')
        return Projection().from_xml(self.to_xml())

    def _make_java_object(self):
        if self._java_object is None:
            self._java_object = self._jvm.com.supermap.data.Projection()
        return self._java_object

    @staticmethod
    def _from_java_object(java_prj):
        if java_prj is None:
            return
        prj = Projection()
        prj._java_object = java_prj
        return prj

    @property
    def name(self):
        """str: 投影方式对象的名称"""
        if self._jobject is None:
            raise ObjectDisposedError('Projection')
        return self._jobject.getName()

    def set_name(self, name):
        """
        为您的自定义投影设置的名称

        :param str name: 自定义投影的名称
        :return: self
        :rtype: Projection
        """
        if self._jobject is None:
            raise ObjectDisposedError('Projection')
        if name is not None:
            self._jobject.setName(name)
        return self

    @property
    def type(self):
        """ProjectionType: 投影坐标系统的投影方式的类型"""
        if self._jobject is None:
            raise ObjectDisposedError('Projection')
        return ProjectionType._make(self._jobject.getType().name())

    def set_type(self, projection_type):
        """
        设置投影坐标系统的投影方式的类型。

        :param projection_type:  投影坐标系统的投影方式的类型
        :type projection_type:  ProjectionType or str
        :return: self
        :rtype: Projection
        """
        if self._jobject is None:
            raise ObjectDisposedError('Projection')
        self._jobject.setType(ProjectionType._make(projection_type)._jobject)
        return self

    def from_xml(self, xml):
        """
        根据 XML 字符串构建投影坐标方式对象，成功返回 True。

        :param str xml:  指定的 XML 字符串
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('Projection')
        if xml is not None:
            return self._jobject.fromXML(xml)
        return False

    def to_xml(self):
        """
        返回投影方式对象的 XML 字符串表示。

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError('Projection')
        return self._jobject.toXML()


class PrjParameter(JVMBase):
    __doc__ = '\n    地图投影参数类。 地图投影的参数，比如中央经线、原点纬度、双标准纬线的第一和第二条纬线等\n    '

    def __init__(self):
        JVMBase.__init__(self)

    def __getstate__(self):
        return self.to_xml()

    def __setstate__(self, state):
        self.__init__()
        self.from_xml(state)

    def clone(self):
        """
        复制对象

        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return PrjParameter().from_xml(self.to_xml())

    def from_xml(self, xml):
        """
        根据传入的 XML 字符串构建 PrjParameter 对象

        :param str xml:
        :return:  如果构建成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if xml is not None:
            return self._jobject.fromXML(xml)
        return False

    def to_xml(self):
        """
        返回 PrjParameter 对象的 XML 字符串表示

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.toXML()

    @property
    def central_meridian(self):
        """float: 中央经线角度值。单位：度。 取值范围为-180度至180度"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getCentralMeridian()

    @property
    def standard_parallel2(self):
        """float: 返回第二标准纬线的纬度值。单位：度。主要应用于圆锥投影中。如果是单标准纬线，则第一标准纬线与第二标准纬线的纬度值相同；如果是双
        标准纬线，则其值不能与第一标准纬线的值相同。"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getStandardParallel2()

    @property
    def first_point_longitude(self):
        """float: 返回第一个点的经度。用于方位投影或斜投影。单位：度"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getFirstPointLongitude()

    @property
    def rectified_angle(self):
        """float: 返回改良斜正射投影（ProjectionType.RectifiedSkewedOrthomorphic）参数中的纠正角，单位为弧度"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getRectifiedAngle()

    @property
    def standard_parallel1(self):
        """float: 返回第一标准纬线的纬度值。单位：度。主要应用于圆锥投影中。如果是单标准纬线，则第一标准纬线与第二标准纬线的纬度值相同。"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getStandardParallel1()

    def set_central_meridian(self, value):
        """
        设置中央经线角度值。单位：度。 取值范围为-180度至180度。

        :param float value: 中央经线角度值。单位：度
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setCentralMeridian(float(value))
        return self

    def set_standard_parallel1(self, value):
        """
        设置第一标准纬线的纬度值。单位：度。主要应用于圆锥投影中。如果是单标准纬线，则第一标准纬线与第二标准纬线的纬度值相同。

        :param float value:  第一标准纬线的纬度值
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setStandardParallel1(float(value))
        return self

    def set_standard_parallel2(self, value):
        """
        设置第二标准纬线的纬度值。单位：度。 主要应用于圆锥投影中。如果是单标准纬线，则第一标准纬线与第二标准纬线的纬度值相同；如果是双标准纬线，则
        其值不能与第一标准纬线的值相同。

        :param float value: 第二标准纬线的纬度值。单位：度。
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setStandardParallel2(float(value))
        return self

    def set_central_parallel(self, value):
        """
        设置坐标原点对应纬度值。单位：度。 取值范围为-90度至90度，在圆锥投影中通常就是投影区域最南端的纬度值。

        :param float value:  坐标原点对应纬度值
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        self._jobject.setCentralParallel(float(value))
        return self

    def set_second_point_longitude(self, value):
        """
        设置第二个点的经度。用于方位投影或斜投影。单位：度。

        :param float value: 第二个点的经度。单位：度
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setSecondPointLongitude(float(value))
        return self

    def set_rectified_angle(self, value):
        """
        设置改良斜正射投影（ProjectionType.RectifiedSkewedOrthomorphic）参数中的纠正角，单位为弧度。

        :param float value:  改良斜正射投影（ProjectionType.RectifiedSkewedOrthomorphic）参数中的纠正角，单位为弧度
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setRectifiedAngle(float(value))
        return self

    def set_first_point_longitude(self, value):
        """
        设置第一个点的经度。用于方位投影或斜投影。单位：度

        :param float value: 第一个点的经度。单位：度
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setFirstPointLongitude(float(value))
        return self

    @property
    def central_parallel(self):
        """float: 返回坐标原点对应纬度值。单位：度。 取值范围为-90度至90度，在圆锥投影中通常就是投影区域最南端的纬度值。"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getCentralParallel()

    @property
    def second_point_longitude(self):
        """float: 返回第二个点的经度。用于方位投影或斜投影。单位：度"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getSecondPointLongitude()

    @property
    def scale_factor(self):
        """float: 返回投影转换的比例因子。 用于减少投影变换的误差。墨卡托、高斯--克吕格和 UTM 投影的值一般为0.9996"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getScaleFactor()

    def set_scale_factor(self, value):
        """
        设置投影转换的比例因子。 用于减少投影变换的误差。墨卡托、高斯--克吕格和 UTM 投影的值一般为0.9996。

        :param float value: 投影转换的比例因
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setScaleFactor(float(value))
        return self

    @property
    def false_northing(self):
        """float: 坐标垂直偏移量"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getFalseNorthing()

    @property
    def azimuth(self):
        """float: 方位角"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getAzimuth()

    def set_false_easting(self, value):
        """
        设置坐标水平偏移量。单位：米。 此方法的参数值是为了避免系统坐标出现负值而加上的一个偏移量。通常用于高斯--克吕格、UTM 和墨卡托投影中。一般的值为500000米。

        :param float value: 坐标水平偏移量。单位：米。
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setFalseEasting(float(value))
        return self

    def set_false_northing(self, value):
        """
        设置坐标垂直偏移量。单位：米。此方法的参数值是为了避免系统坐标出现负值而加上的一个偏移量。通常用于高斯--克吕格、UTM 和墨卡托投影中。一般的值为1000000米。

        :param float value: 坐标垂直偏移量。单位：米
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setFalseNorthing(float(value))
        return self

    @property
    def false_easting(self):
        """float: 坐标水平偏移量。单位：米"""
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        return self._jobject.getFalseEasting()

    def set_azimuth(self, value):
        """
        设置方位角。主要用于斜轴投影。单位：度

        :param float value: 方位角
        :return: self
        :rtype: PrjParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('PrjParameter')
        if value is not None:
            self._jobject.setAzimuth(float(value))
        return self

    def _make_java_object(self):
        if self._java_object is None:
            self._java_object = self._jvm.com.supermap.data.PrjParameter()
        return self._java_object

    @staticmethod
    def _from_java_object(java_obj):
        obj = PrjParameter()
        obj._java_object = java_obj
        return obj


class CoordSysTransParameter(JVMBase):
    __doc__ = '\n    投影转换参照系转换参数类，通常包括平移、旋转和比例因子。\n\n    在进行投影转换时，如果源投影和目标投影的地理坐标系不同，则需要进行参照系转换。SuperMap 提供常用的六种参照系转换方法，详见 CoordSysTransMethod\n    方法。不同的参照系转换方法需要指定不同的转换参数：\n\n    - 三参数转换法（GeocentricTranslation）、莫洛金斯基转换法（Molodensky）、简化的莫洛金斯基转换法（MolodenskyAbridged）属于精度较低的\n      几种转换方法，在数据精度要求不高的情况下一般可以采用这几种方法。这三种转换法需要给定三个平移转换参数：X 轴坐标偏移量（set_translate_x）、Y轴\n      坐标偏移量（set_translate_y）和 Z 轴坐标偏移量（set_translate_z）。\n    - 位置矢量法（PositionVector）、基于地心的七参数转换法（CoordinateFrame）、布尔莎方法（BursaWolf）属于精度较高的几种转换方法。需要七个\n      参数来进行调整和转换，包括除上述的三个平移转换参数外，还需要设置三个旋转转换参数（X 轴旋转角度（set_rotate_x）、Y 轴旋转角度（set_rotate_y）\n      和 Z 轴旋转角度（set_rotate_z））和投影比例尺差参数（set_scale_difference）。\n\n    '

    def __init__(self):
        JVMBase.__init__(self)

    @property
    def rotation_origin_x(self):
        """float: 旋转原点的X坐标"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getRotationOriginX()

    def set_scale_difference(self, value):
        """
        设置投影比例尺差。单位为百万分之一。用于不同大地参照系之间的转换

        :param float value: 投影比例尺差
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setScaleDifference(value)
        return self

    def set_rotation_origin_z(self, value):
        """
        设置旋转原点的 Z 坐标的量

        :param float value: 旋转原点的 Z 坐标的量
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setRotationOriginZ(value)
        return self

    @property
    def scale_difference(self):
        """float: 投影比例尺差。单位为百万分之一。用于不同大地参照系之间的转换"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getScaleDifference()

    @property
    def rotation_origin_y(self):
        """float:  旋转原点的 Y 坐标的量"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getRotationOriginY()

    def set_rotation_origin_x(self, value):
        """
        设置旋转原点的 X 坐标的量

        :param float value: 旋转原点的 X 坐标的量
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setRotationOriginX(float(value))
        return self

    def set_rotation_origin_y(self, value):
        """
        设置旋转原点的 Y 坐标的量

        :param float value: 旋转原点的 Y 坐标的量
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setRotationOriginY(float(value))
        return self

    @property
    def rotation_origin_z(self):
        """float: 旋转原点的Z坐标的量"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getRotationOriginZ()

    def set_translate_z(self, value):
        """
        设置 Z 轴的坐标偏移量。单位为米

        :param float value:  Z 轴的坐标偏移量
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setTranslateZ(float(value))
        return self

    @property
    def rotate_z(self):
        """float: Z 轴的旋转角度"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getRotateZ()

    @property
    def rotate_y(self):
        """float: Y 轴的旋转角度"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getRotateY()

    def set_translate_y(self, value):
        """
        设置 Y 轴的坐标偏移量。单位为米

        :param float value: Y 轴的坐标偏移量
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setTranslateY(float(value))
        return self

    @property
    def translate_x(self):
        """float: 返回 X 轴的坐标偏移量。单位为米"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getTranslateX()

    def set_translate_x(self, value):
        """
        设置 X 轴的坐标偏移量。单位为米

        :param float value: X 轴的坐标偏移量
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setTranslateX(float(value))
        return self

    def set_rotate_z(self, value):
        """
        设置 Z 轴的旋转角度。用于不同大地参照系之间的转换。单位为弧度。

        :param float value: Z 轴的旋转角度
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setRotateZ(float(value))
        return self

    @property
    def translate_y(self):
        """float: 返回 Y 轴的坐标偏移量。单位为米"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getTranslateY()

    @property
    def translate_z(self):
        """float: 返回 Z 轴的坐标偏移量。单位为米"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getTranslateZ()

    def set_rotate_y(self, value):
        """
        设置 Y 轴的旋转角度。用于不同大地参照系之间的转换。单位为弧度。

        :param float value: Y 轴的旋转角度
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setRotateY(float(value))
        return self

    @property
    def rotate_x(self):
        """float: X 轴的旋转角度"""
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.getRotateX()

    def set_rotate_x(self, value):
        """
        设置 X 轴的旋转角度。用于不同大地参照系之间的转换。单位为弧度。

        :param float value: X 轴的旋转角度
        :return: self
        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        if value is not None:
            self._jobject.setRotateX(float(value))
        return self

    def _make_java_object(self):
        if self._java_object is None:
            self._java_object = self._jvm.com.supermap.data.CoordSysTransParameter()
        return self._java_object

    @staticmethod
    def _from_java_object(java_obj):
        obj = CoordSysTransParameter()
        obj._java_object = java_obj
        return obj

    def from_xml(self, xml):
        """
        根据 XML 字符串构建 CoordSysTransParameter 对象，成功返回 True

        :param str xml:
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.fromXML(xml)

    def to_xml(self):
        """
        将该 CoordSysTransParameter 对象输出为 XML 字符串。

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return self._jobject.toXML()

    def __getstate__(self):
        return self.to_xml()

    def __setstate__(self, state):
        self.__init__()
        self.from_xml(state)

    def clone(self):
        """
        复制对象

        :rtype: CoordSysTransParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError('CoordSysTransParameter')
        return CoordSysTransParameter().from_xml(self.to_xml())


class CoordSysTranslator:
    __doc__ = '\n    投影转换类。主要用于投影坐标之间及投影坐标系之间的转换。\n\n    投影转换一般有三种工作方式：地理（经纬度）坐标和投影坐标之间的转换使用 forward() 方法、投影坐标和地理（经纬度）坐标之间的转换使用inverse() 方法 、\n    两种投影坐标系之间的转换使用convert() 方法。\n\n    注意：当前版本不支持光栅数据的投影转换。即在同一数据源中，投影转换只转换矢量数据部分。地理坐标系（Geographic coordinate system）也称为地理\n    坐标系统，是以经纬度为地图的存储单位的。很明显，地理坐标系是球面坐标系统。如果将地球上的数字化信息存放到球面坐标系统上，就需要有这样的椭球体具有\n    如下特点：可以量化计算的，具有长半轴（Semimajor Axis），短半轴（Semiminor Axis），偏心率（Flattening），中央子午线（prime meridian）及大地基准面（datum）。\n\n    投影坐标系统（Projection coordinate system）实质上便是平面坐标系统，其地图单位通常为米。将球面坐标转化为平面坐标的过程便称为投影。所以每一个\n    投影坐标系统都必定会有地理坐标系统（Geographic Coordinate System）参数。 因此就存在着投影坐标之间的转换以及投影坐标系之间的转换。\n\n    在进行投影转换时，对文本对象（GeoText）投影转换后，文本对象的字高和角度会相应地转换，如果用户不需要这样的改变，需要对转换后的文本对象修正其字高和角度。\n\n    '

    @staticmethod
    def convert--- This code section failed: ---

 L.1744         0  LOAD_CONST               1
                2  LOAD_CONST               ('get_input_dataset', 'get_output_datasource', 'check_output_datasource', 'try_close_output_datasource')
                4  IMPORT_NAME              _util
                6  IMPORT_FROM              get_input_dataset
                8  STORE_FAST               'get_input_dataset'
               10  IMPORT_FROM              get_output_datasource
               12  STORE_FAST               'get_output_datasource'
               14  IMPORT_FROM              check_output_datasource
               16  STORE_FAST               'check_output_datasource'
               18  IMPORT_FROM              try_close_output_datasource
               20  STORE_FAST               'try_close_output_datasource'
               22  POP_TOP          

 L.1748        24  LOAD_CONST               1
               26  LOAD_CONST               ('DatasetVector',)
               28  IMPORT_NAME              dt
               30  IMPORT_FROM              DatasetVector
               32  STORE_FAST               'DatasetVector'
               34  POP_TOP          

 L.1750        36  LOAD_FAST                'get_input_dataset'
               38  LOAD_FAST                'source_data'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  STORE_FAST               '_source'

 L.1751        44  LOAD_FAST                '_source'
               46  LOAD_CONST               None
               48  COMPARE_OP               is
               50  POP_JUMP_IF_FALSE    60  'to 60'

 L.1752        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'source data is None'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L.1753        60  LOAD_GLOBAL              get_jvm
               62  CALL_FUNCTION_0       0  '0 positional arguments'
               64  STORE_FAST               'jvm'

 L.1754        66  LOAD_FAST                'coord_sys_trans_method'
               68  LOAD_CONST               None
               70  COMPARE_OP               is-not
               72  POP_JUMP_IF_FALSE    88  'to 88'

 L.1755        74  LOAD_GLOBAL              CoordSysTransMethod
               76  LOAD_METHOD              _make
               78  LOAD_FAST                'coord_sys_trans_method'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  LOAD_ATTR                _jobject
               84  STORE_FAST               'javaMethod'
               86  JUMP_FORWARD         92  'to 92'
             88_0  COME_FROM            72  '72'

 L.1757        88  LOAD_CONST               None
               90  STORE_FAST               'javaMethod'
             92_0  COME_FROM            86  '86'

 L.1758        92  LOAD_GLOBAL              isinstance
               94  LOAD_FAST                '_source'
               96  LOAD_FAST                'DatasetVector'
               98  CALL_FUNCTION_2       2  '2 positional arguments'
          100_102  POP_JUMP_IF_FALSE   380  'to 380'

 L.1759       104  LOAD_FAST                'out_data'
              106  LOAD_CONST               None
              108  COMPARE_OP               is-not
          110_112  POP_JUMP_IF_FALSE   288  'to 288'

 L.1760       114  LOAD_FAST                'get_output_datasource'
              116  LOAD_FAST                'out_data'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  STORE_FAST               '_out_datasource'

 L.1761       122  LOAD_FAST                'check_output_datasource'
              124  LOAD_FAST                '_out_datasource'
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  POP_TOP          

 L.1762       130  LOAD_FAST                'out_dataset_name'
              132  LOAD_CONST               None
              134  COMPARE_OP               is
              136  POP_JUMP_IF_FALSE   142  'to 142'

 L.1763       138  LOAD_STR                 'Translator_result'
              140  STORE_FAST               'out_dataset_name'
            142_0  COME_FROM           136  '136'

 L.1764       142  LOAD_FAST                '_out_datasource'
              144  LOAD_METHOD              get_available_dataset_name
              146  LOAD_FAST                'out_dataset_name'
              148  CALL_METHOD_1         1  '1 positional argument'
              150  STORE_FAST               '_outDatasetName'

 L.1766       152  SETUP_FINALLY       254  'to 254'
              154  SETUP_EXCEPT        204  'to 204'

 L.1767       156  LOAD_FAST                'jvm'
              158  LOAD_ATTR                com
              160  LOAD_ATTR                supermap
              162  LOAD_ATTR                data
              164  LOAD_ATTR                CoordSysTranslator
              166  LOAD_METHOD              convert
              168  LOAD_FAST                '_source'
              170  LOAD_ATTR                _jobject

 L.1768       172  LOAD_FAST                'target_prj_coordsys'
              174  LOAD_ATTR                _jobject

 L.1769       176  LOAD_FAST                '_out_datasource'
              178  LOAD_ATTR                _jobject

 L.1770       180  LOAD_FAST                '_outDatasetName'

 L.1771       182  LOAD_FAST                'coordsys_trans_parameter'
              184  LOAD_ATTR                _jobject

 L.1772       186  LOAD_FAST                'javaMethod'
              188  CALL_METHOD_6         6  '6 positional arguments'
              190  STORE_FAST               'result'

 L.1773       192  LOAD_FAST                'result'
              194  LOAD_METHOD              getName
              196  CALL_METHOD_0         0  '0 positional arguments'
              198  STORE_FAST               'result_name'
              200  POP_BLOCK        
              202  JUMP_FORWARD        250  'to 250'
            204_0  COME_FROM_EXCEPT    154  '154'

 L.1774       204  DUP_TOP          
              206  LOAD_GLOBAL              Exception
              208  COMPARE_OP               exception-match
              210  POP_JUMP_IF_FALSE   248  'to 248'
              212  POP_TOP          
              214  STORE_FAST               'e'
              216  POP_TOP          
              218  SETUP_FINALLY       236  'to 236'

 L.1775       220  LOAD_GLOBAL              log_error
              222  LOAD_FAST                'e'
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  POP_TOP          

 L.1776       228  LOAD_CONST               None
              230  STORE_FAST               'result_name'
              232  POP_BLOCK        
              234  LOAD_CONST               None
            236_0  COME_FROM_FINALLY   218  '218'
              236  LOAD_CONST               None
              238  STORE_FAST               'e'
              240  DELETE_FAST              'e'
              242  END_FINALLY      
              244  POP_EXCEPT       
              246  JUMP_FORWARD        250  'to 250'
            248_0  COME_FROM           210  '210'
              248  END_FINALLY      
            250_0  COME_FROM           246  '246'
            250_1  COME_FROM           202  '202'
              250  POP_BLOCK        
              252  LOAD_CONST               None
            254_0  COME_FROM_FINALLY   152  '152'

 L.1778       254  LOAD_FAST                'result_name'
              256  LOAD_CONST               None
              258  COMPARE_OP               is-not
          260_262  POP_JUMP_IF_FALSE   274  'to 274'

 L.1779       264  LOAD_FAST                '_out_datasource'
              266  LOAD_FAST                'result_name'
              268  BINARY_SUBSCR    
              270  STORE_FAST               'result_dt'
              272  JUMP_FORWARD        278  'to 278'
            274_0  COME_FROM           260  '260'

 L.1781       274  LOAD_CONST               None
              276  STORE_FAST               'result_dt'
            278_0  COME_FROM           272  '272'

 L.1782       278  LOAD_FAST                'try_close_output_datasource'
              280  LOAD_FAST                'result_dt'
              282  LOAD_FAST                '_out_datasource'
              284  CALL_FUNCTION_2       2  '2 positional arguments'
              286  RETURN_VALUE     
            288_0  COME_FROM           110  '110'

 L.1784       288  SETUP_EXCEPT        324  'to 324'

 L.1785       290  LOAD_FAST                'jvm'
              292  LOAD_ATTR                com
              294  LOAD_ATTR                supermap
              296  LOAD_ATTR                data
              298  LOAD_ATTR                CoordSysTranslator
              300  LOAD_METHOD              convert
              302  LOAD_FAST                '_source'
              304  LOAD_ATTR                _jobject

 L.1786       306  LOAD_FAST                'target_prj_coordsys'
              308  LOAD_ATTR                _jobject

 L.1787       310  LOAD_FAST                'coordsys_trans_parameter'
              312  LOAD_ATTR                _jobject

 L.1788       314  LOAD_FAST                'javaMethod'
              316  CALL_METHOD_4         4  '4 positional arguments'
              318  STORE_FAST               'result'
              320  POP_BLOCK        
              322  JUMP_FORWARD        372  'to 372'
            324_0  COME_FROM_EXCEPT    288  '288'

 L.1789       324  DUP_TOP          
              326  LOAD_GLOBAL              Exception
              328  COMPARE_OP               exception-match
          330_332  POP_JUMP_IF_FALSE   370  'to 370'
              334  POP_TOP          
              336  STORE_FAST               'e'
              338  POP_TOP          
              340  SETUP_FINALLY       358  'to 358'

 L.1790       342  LOAD_GLOBAL              log_error
              344  LOAD_FAST                'e'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  POP_TOP          

 L.1791       350  LOAD_CONST               False
              352  STORE_FAST               'result'
              354  POP_BLOCK        
              356  LOAD_CONST               None
            358_0  COME_FROM_FINALLY   340  '340'
              358  LOAD_CONST               None
              360  STORE_FAST               'e'
              362  DELETE_FAST              'e'
              364  END_FINALLY      
              366  POP_EXCEPT       
              368  JUMP_FORWARD        372  'to 372'
            370_0  COME_FROM           330  '330'
              370  END_FINALLY      
            372_0  COME_FROM           368  '368'
            372_1  COME_FROM           322  '322'

 L.1792       372  LOAD_FAST                'result'
              374  RETURN_VALUE     
          376_378  JUMP_FORWARD       1432  'to 1432'
            380_0  COME_FROM           100  '100'

 L.1793       380  LOAD_GLOBAL              isinstance
              382  LOAD_FAST                '_source'
              384  LOAD_GLOBAL              Geometry
              386  CALL_FUNCTION_2       2  '2 positional arguments'
          388_390  POP_JUMP_IF_FALSE   762  'to 762'

 L.1794       392  LOAD_FAST                'source_prj_coordsys'
              394  LOAD_CONST               None
              396  COMPARE_OP               is
          398_400  POP_JUMP_IF_FALSE   410  'to 410'

 L.1795       402  LOAD_GLOBAL              ValueError
              404  LOAD_STR                 'source_prj_coordsys is None'
              406  CALL_FUNCTION_1       1  '1 positional argument'
              408  RAISE_VARARGS_1       1  'exception instance'
            410_0  COME_FROM           398  '398'

 L.1796       410  LOAD_GLOBAL              PrjCoordSys
              412  LOAD_METHOD              make
              414  LOAD_FAST                'source_prj_coordsys'
              416  CALL_METHOD_1         1  '1 positional argument'
              418  STORE_FAST               'source_prj_coordsys'

 L.1797       420  LOAD_FAST                'out_data'
              422  LOAD_CONST               None
              424  COMPARE_OP               is-not
          426_428  POP_JUMP_IF_FALSE   666  'to 666'

 L.1798       430  LOAD_FAST                'get_output_datasource'
              432  LOAD_FAST                'out_data'
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  STORE_FAST               '_out_datasource'

 L.1799       438  LOAD_FAST                'check_output_datasource'
              440  LOAD_FAST                '_out_datasource'
              442  CALL_FUNCTION_1       1  '1 positional argument'
              444  POP_TOP          

 L.1800       446  LOAD_FAST                'out_dataset_name'
              448  LOAD_CONST               None
              450  COMPARE_OP               is
          452_454  POP_JUMP_IF_FALSE   460  'to 460'

 L.1801       456  LOAD_STR                 'Translator_result'
              458  STORE_FAST               'out_dataset_name'
            460_0  COME_FROM           452  '452'

 L.1802       460  LOAD_FAST                '_out_datasource'
              462  LOAD_METHOD              get_available_dataset_name
              464  LOAD_FAST                'out_dataset_name'
              466  CALL_METHOD_1         1  '1 positional argument'
              468  STORE_FAST               '_outDatasetName'

 L.1803       470  LOAD_FAST                '_out_datasource'
              472  LOAD_METHOD              write_spatial_data
              474  LOAD_FAST                '_source'
              476  BUILD_LIST_1          1 
              478  LOAD_FAST                '_outDatasetName'
              480  CALL_METHOD_2         2  '2 positional arguments'
              482  STORE_FAST               'result_dt'

 L.1804       484  LOAD_FAST                'result_dt'
              486  LOAD_CONST               None
              488  COMPARE_OP               is
          490_492  POP_JUMP_IF_FALSE   516  'to 516'

 L.1805       494  LOAD_FAST                'try_close_output_datasource'
              496  LOAD_CONST               None
              498  LOAD_FAST                '_out_datasource'
              500  CALL_FUNCTION_2       2  '2 positional arguments'
              502  POP_TOP          

 L.1806       504  LOAD_GLOBAL              log_error
              506  LOAD_STR                 'Failed to write source data to datasource'
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  POP_TOP          

 L.1807       512  LOAD_CONST               False
              514  RETURN_VALUE     
            516_0  COME_FROM           490  '490'

 L.1808       516  SETUP_EXCEPT        574  'to 574'

 L.1809       518  LOAD_FAST                'result_dt'
              520  STORE_FAST               'dt'

 L.1810       522  LOAD_FAST                'dt'
              524  LOAD_METHOD              open
              526  CALL_METHOD_0         0  '0 positional arguments'
              528  POP_TOP          

 L.1811       530  LOAD_FAST                'dt'
              532  LOAD_METHOD              set_prj_coordsys
              534  LOAD_FAST                'source_prj_coordsys'
              536  CALL_METHOD_1         1  '1 positional argument'
              538  POP_TOP          

 L.1812       540  LOAD_FAST                'jvm'
              542  LOAD_ATTR                com
              544  LOAD_ATTR                supermap
              546  LOAD_ATTR                data
              548  LOAD_ATTR                CoordSysTranslator
              550  LOAD_METHOD              convert
              552  LOAD_FAST                'dt'
              554  LOAD_ATTR                _jobject

 L.1813       556  LOAD_FAST                'target_prj_coordsys'
              558  LOAD_ATTR                _jobject

 L.1814       560  LOAD_FAST                'coordsys_trans_parameter'
              562  LOAD_ATTR                _jobject

 L.1815       564  LOAD_FAST                'javaMethod'
              566  CALL_METHOD_4         4  '4 positional arguments'
              568  STORE_FAST               'result'
              570  POP_BLOCK        
              572  JUMP_FORWARD        622  'to 622'
            574_0  COME_FROM_EXCEPT    516  '516'

 L.1816       574  DUP_TOP          
              576  LOAD_GLOBAL              Exception
              578  COMPARE_OP               exception-match
          580_582  POP_JUMP_IF_FALSE   620  'to 620'
              584  POP_TOP          
              586  STORE_FAST               'e'
              588  POP_TOP          
              590  SETUP_FINALLY       608  'to 608'

 L.1817       592  LOAD_GLOBAL              log_error
              594  LOAD_FAST                'e'
              596  CALL_FUNCTION_1       1  '1 positional argument'
              598  POP_TOP          

 L.1818       600  LOAD_CONST               False
              602  STORE_FAST               'result'
              604  POP_BLOCK        
              606  LOAD_CONST               None
            608_0  COME_FROM_FINALLY   590  '590'
              608  LOAD_CONST               None
              610  STORE_FAST               'e'
              612  DELETE_FAST              'e'
              614  END_FINALLY      
              616  POP_EXCEPT       
              618  JUMP_FORWARD        622  'to 622'
            620_0  COME_FROM           580  '580'
              620  END_FINALLY      
            622_0  COME_FROM           618  '618'
            622_1  COME_FROM           572  '572'

 L.1819       622  LOAD_FAST                'result'
          624_626  POP_JUMP_IF_TRUE    654  'to 654'

 L.1820       628  LOAD_FAST                '_out_datasource'
              630  LOAD_METHOD              detele
              632  LOAD_FAST                'result_dt'
              634  LOAD_ATTR                name
              636  CALL_METHOD_1         1  '1 positional argument'
              638  POP_TOP          

 L.1821       640  LOAD_FAST                'try_close_output_datasource'
              642  LOAD_CONST               None
              644  LOAD_FAST                '_out_datasource'
              646  CALL_FUNCTION_2       2  '2 positional arguments'
              648  POP_TOP          

 L.1822       650  LOAD_CONST               None
              652  RETURN_VALUE     
            654_0  COME_FROM           624  '624'

 L.1824       654  LOAD_FAST                'try_close_output_datasource'
              656  LOAD_FAST                'result_dt'
              658  LOAD_FAST                '_out_datasource'
              660  CALL_FUNCTION_2       2  '2 positional arguments'
              662  RETURN_VALUE     
              664  JUMP_FORWARD       1432  'to 1432'
            666_0  COME_FROM           426  '426'

 L.1826       666  SETUP_EXCEPT        706  'to 706'

 L.1827       668  LOAD_FAST                'jvm'
              670  LOAD_ATTR                com
              672  LOAD_ATTR                supermap
              674  LOAD_ATTR                data
              676  LOAD_ATTR                CoordSysTranslator
              678  LOAD_METHOD              convert
              680  LOAD_FAST                '_source'
              682  LOAD_ATTR                _jobject

 L.1828       684  LOAD_FAST                'source_prj_coordsys'
              686  LOAD_ATTR                _jobject

 L.1829       688  LOAD_FAST                'target_prj_coordsys'
              690  LOAD_ATTR                _jobject

 L.1830       692  LOAD_FAST                'coordsys_trans_parameter'
              694  LOAD_ATTR                _jobject

 L.1831       696  LOAD_FAST                'javaMethod'
              698  CALL_METHOD_5         5  '5 positional arguments'
              700  STORE_FAST               'result'
              702  POP_BLOCK        
              704  JUMP_FORWARD        754  'to 754'
            706_0  COME_FROM_EXCEPT    666  '666'

 L.1832       706  DUP_TOP          
              708  LOAD_GLOBAL              Exception
              710  COMPARE_OP               exception-match
          712_714  POP_JUMP_IF_FALSE   752  'to 752'
              716  POP_TOP          
              718  STORE_FAST               'e'
              720  POP_TOP          
              722  SETUP_FINALLY       740  'to 740'

 L.1833       724  LOAD_GLOBAL              log_error
              726  LOAD_FAST                'e'
              728  CALL_FUNCTION_1       1  '1 positional argument'
              730  POP_TOP          

 L.1834       732  LOAD_CONST               False
              734  STORE_FAST               'result'
              736  POP_BLOCK        
              738  LOAD_CONST               None
            740_0  COME_FROM_FINALLY   722  '722'
              740  LOAD_CONST               None
              742  STORE_FAST               'e'
              744  DELETE_FAST              'e'
              746  END_FINALLY      
              748  POP_EXCEPT       
              750  JUMP_FORWARD        754  'to 754'
            752_0  COME_FROM           712  '712'
              752  END_FINALLY      
            754_0  COME_FROM           750  '750'
            754_1  COME_FROM           704  '704'

 L.1835       754  LOAD_FAST                'result'
              756  RETURN_VALUE     
          758_760  JUMP_FORWARD       1432  'to 1432'
            762_0  COME_FROM           388  '388'

 L.1837       762  LOAD_GLOBAL              isinstance
              764  LOAD_FAST                '_source'
              766  LOAD_GLOBAL              list
              768  LOAD_GLOBAL              tuple
              770  BUILD_TUPLE_2         2 
              772  CALL_FUNCTION_2       2  '2 positional arguments'
          774_776  POP_JUMP_IF_FALSE  1412  'to 1412'

 L.1838       778  LOAD_FAST                'source_prj_coordsys'
              780  LOAD_CONST               None
              782  COMPARE_OP               is
          784_786  POP_JUMP_IF_FALSE   796  'to 796'

 L.1839       788  LOAD_GLOBAL              ValueError
              790  LOAD_STR                 'source_prj_coordsys is None'
              792  CALL_FUNCTION_1       1  '1 positional argument'
              794  RAISE_VARARGS_1       1  'exception instance'
            796_0  COME_FROM           784  '784'

 L.1840       796  LOAD_GLOBAL              PrjCoordSys
              798  LOAD_METHOD              make
              800  LOAD_FAST                'source_prj_coordsys'
              802  CALL_METHOD_1         1  '1 positional argument'
              804  STORE_FAST               'source_prj_coordsys'

 L.1841       806  LOAD_FAST                'out_data'
              808  LOAD_CONST               None
              810  COMPARE_OP               is-not
          812_814  POP_JUMP_IF_FALSE  1052  'to 1052'

 L.1842       816  LOAD_FAST                'get_output_datasource'
              818  LOAD_FAST                'out_data'
              820  CALL_FUNCTION_1       1  '1 positional argument'
              822  STORE_FAST               '_out_datasource'

 L.1843       824  LOAD_FAST                'check_output_datasource'
              826  LOAD_FAST                '_out_datasource'
              828  CALL_FUNCTION_1       1  '1 positional argument'
              830  POP_TOP          

 L.1844       832  LOAD_FAST                'out_dataset_name'
              834  LOAD_CONST               None
              836  COMPARE_OP               is
          838_840  POP_JUMP_IF_FALSE   846  'to 846'

 L.1845       842  LOAD_STR                 'Translator_result'
              844  STORE_FAST               'out_dataset_name'
            846_0  COME_FROM           838  '838'

 L.1846       846  LOAD_FAST                '_out_datasource'
              848  LOAD_METHOD              get_available_dataset_name
              850  LOAD_FAST                'out_dataset_name'
              852  CALL_METHOD_1         1  '1 positional argument'
              854  STORE_FAST               '_outDatasetName'

 L.1847       856  LOAD_FAST                '_out_datasource'
              858  LOAD_METHOD              write_spatial_data
              860  LOAD_FAST                '_source'
              862  LOAD_FAST                '_outDatasetName'
              864  CALL_METHOD_2         2  '2 positional arguments'
              866  STORE_FAST               'result_dt'

 L.1848       868  LOAD_FAST                'result_dt'
              870  LOAD_CONST               None
              872  COMPARE_OP               is
          874_876  POP_JUMP_IF_FALSE   900  'to 900'

 L.1849       878  LOAD_FAST                'try_close_output_datasource'
              880  LOAD_CONST               None
              882  LOAD_FAST                '_out_datasource'
              884  CALL_FUNCTION_2       2  '2 positional arguments'
              886  POP_TOP          

 L.1850       888  LOAD_GLOBAL              log_error
              890  LOAD_STR                 'Failed to write source data to datasource'
              892  CALL_FUNCTION_1       1  '1 positional argument'
              894  POP_TOP          

 L.1851       896  LOAD_CONST               False
              898  RETURN_VALUE     
            900_0  COME_FROM           874  '874'

 L.1852       900  SETUP_EXCEPT        958  'to 958'

 L.1853       902  LOAD_FAST                'result_dt'
              904  STORE_FAST               'dt'

 L.1854       906  LOAD_FAST                'dt'
              908  LOAD_METHOD              open
              910  CALL_METHOD_0         0  '0 positional arguments'
              912  POP_TOP          

 L.1855       914  LOAD_FAST                'dt'
              916  LOAD_METHOD              set_prj_coordsys
              918  LOAD_FAST                'source_prj_coordsys'
              920  CALL_METHOD_1         1  '1 positional argument'
              922  POP_TOP          

 L.1856       924  LOAD_FAST                'jvm'
              926  LOAD_ATTR                com
              928  LOAD_ATTR                supermap
              930  LOAD_ATTR                data
              932  LOAD_ATTR                CoordSysTranslator
              934  LOAD_METHOD              convert
              936  LOAD_FAST                'dt'
              938  LOAD_ATTR                _jobject

 L.1857       940  LOAD_FAST                'target_prj_coordsys'
              942  LOAD_ATTR                _jobject

 L.1858       944  LOAD_FAST                'coordsys_trans_parameter'
              946  LOAD_ATTR                _jobject

 L.1859       948  LOAD_FAST                'javaMethod'
              950  CALL_METHOD_4         4  '4 positional arguments'
              952  STORE_FAST               'result'
              954  POP_BLOCK        
              956  JUMP_FORWARD       1006  'to 1006'
            958_0  COME_FROM_EXCEPT    900  '900'

 L.1860       958  DUP_TOP          
              960  LOAD_GLOBAL              Exception
              962  COMPARE_OP               exception-match
          964_966  POP_JUMP_IF_FALSE  1004  'to 1004'
              968  POP_TOP          
              970  STORE_FAST               'e'
              972  POP_TOP          
              974  SETUP_FINALLY       992  'to 992'

 L.1861       976  LOAD_GLOBAL              log_error
              978  LOAD_FAST                'e'
              980  CALL_FUNCTION_1       1  '1 positional argument'
              982  POP_TOP          

 L.1862       984  LOAD_CONST               False
              986  STORE_FAST               'result'
              988  POP_BLOCK        
              990  LOAD_CONST               None
            992_0  COME_FROM_FINALLY   974  '974'
              992  LOAD_CONST               None
              994  STORE_FAST               'e'
              996  DELETE_FAST              'e'
              998  END_FINALLY      
             1000  POP_EXCEPT       
             1002  JUMP_FORWARD       1006  'to 1006'
           1004_0  COME_FROM           964  '964'
             1004  END_FINALLY      
           1006_0  COME_FROM          1002  '1002'
           1006_1  COME_FROM           956  '956'

 L.1863      1006  LOAD_FAST                'result'
         1008_1010  POP_JUMP_IF_TRUE   1038  'to 1038'

 L.1864      1012  LOAD_FAST                '_out_datasource'
             1014  LOAD_METHOD              detele
             1016  LOAD_FAST                'result_dt'
             1018  LOAD_ATTR                name
             1020  CALL_METHOD_1         1  '1 positional argument'
             1022  POP_TOP          

 L.1865      1024  LOAD_FAST                'try_close_output_datasource'
             1026  LOAD_CONST               None
             1028  LOAD_FAST                '_out_datasource'
             1030  CALL_FUNCTION_2       2  '2 positional arguments'
             1032  POP_TOP          

 L.1866      1034  LOAD_CONST               None
             1036  RETURN_VALUE     
           1038_0  COME_FROM          1008  '1008'

 L.1868      1038  LOAD_FAST                'try_close_output_datasource'
             1040  LOAD_FAST                'result_dt'
             1042  LOAD_FAST                '_out_datasource'
             1044  CALL_FUNCTION_2       2  '2 positional arguments'
             1046  RETURN_VALUE     
         1048_1050  JUMP_ABSOLUTE      1432  'to 1432'
           1052_0  COME_FROM           812  '812'

 L.1870      1052  LOAD_GLOBAL              len
             1054  LOAD_FAST                '_source'
             1056  CALL_FUNCTION_1       1  '1 positional argument'
             1058  LOAD_CONST               0
             1060  COMPARE_OP               ==
         1062_1064  POP_JUMP_IF_FALSE  1070  'to 1070'

 L.1871      1066  LOAD_CONST               False
             1068  RETURN_VALUE     
           1070_0  COME_FROM          1062  '1062'

 L.1872  1070_1072  SETUP_EXCEPT       1362  'to 1362'

 L.1873      1074  LOAD_CONST               1
             1076  LOAD_CONST               ('to_java_point2ds',)
             1078  IMPORT_NAME              _util
             1080  IMPORT_FROM              to_java_point2ds
             1082  STORE_FAST               'to_java_point2ds'
             1084  POP_TOP          

 L.1874      1086  LOAD_GLOBAL              isinstance
             1088  LOAD_FAST                '_source'
             1090  LOAD_CONST               0
             1092  BINARY_SUBSCR    
             1094  LOAD_GLOBAL              Point2D
             1096  CALL_FUNCTION_2       2  '2 positional arguments'
         1098_1100  POP_JUMP_IF_FALSE  1260  'to 1260'

 L.1875      1102  LOAD_FAST                'to_java_point2ds'
             1104  LOAD_FAST                '_source'
             1106  CALL_FUNCTION_1       1  '1 positional argument'
             1108  STORE_DEREF              'java_points'

 L.1876      1110  LOAD_CONST               False
             1112  STORE_FAST               'result'

 L.1877      1114  LOAD_DEREF               'java_points'
             1116  LOAD_METHOD              getCount
             1118  CALL_METHOD_0         0  '0 positional arguments'
             1120  LOAD_CONST               0
             1122  COMPARE_OP               >
         1124_1126  POP_JUMP_IF_FALSE  1256  'to 1256'

 L.1878      1128  LOAD_FAST                'jvm'
             1130  LOAD_ATTR                com
             1132  LOAD_ATTR                supermap
             1134  LOAD_ATTR                data
             1136  LOAD_ATTR                CoordSysTranslator
             1138  LOAD_METHOD              convert
             1140  LOAD_DEREF               'java_points'

 L.1879      1142  LOAD_FAST                'source_prj_coordsys'
             1144  LOAD_ATTR                _jobject

 L.1880      1146  LOAD_FAST                'target_prj_coordsys'
             1148  LOAD_ATTR                _jobject

 L.1881      1150  LOAD_FAST                'coordsys_trans_parameter'
             1152  LOAD_ATTR                _jobject

 L.1882      1154  LOAD_FAST                'javaMethod'
             1156  CALL_METHOD_5         5  '5 positional arguments'
             1158  STORE_FAST               'result'

 L.1883      1160  LOAD_FAST                'result'
         1162_1164  POP_JUMP_IF_FALSE  1256  'to 1256'

 L.1884      1166  LOAD_CLOSURE             'java_points'
             1168  BUILD_TUPLE_1         1 
             1170  LOAD_CODE                <code_object fun>
             1172  LOAD_STR                 'CoordSysTranslator.convert.<locals>.fun'
             1174  MAKE_FUNCTION_8          'closure'
             1176  STORE_DEREF              'fun'

 L.1888      1178  LOAD_CLOSURE             'fun'
             1180  BUILD_TUPLE_1         1 
             1182  LOAD_GENEXPR             '<code_object <genexpr>>'
             1184  LOAD_STR                 'CoordSysTranslator.convert.<locals>.<genexpr>'
             1186  MAKE_FUNCTION_8          'closure'
             1188  LOAD_GLOBAL              range
             1190  LOAD_DEREF               'java_points'
             1192  LOAD_METHOD              getCount
             1194  CALL_METHOD_0         0  '0 positional arguments'
             1196  CALL_FUNCTION_1       1  '1 positional argument'
             1198  GET_ITER         
             1200  CALL_FUNCTION_1       1  '1 positional argument'
             1202  STORE_FAST               '_r_points'

 L.1889      1204  LOAD_CONST               0
             1206  STORE_FAST               'i'

 L.1890      1208  SETUP_LOOP         1256  'to 1256'
             1210  LOAD_FAST                '_r_points'
             1212  GET_ITER         
             1214  FOR_ITER           1254  'to 1254'
             1216  STORE_FAST               'p'

 L.1891      1218  LOAD_FAST                'p'
             1220  LOAD_ATTR                x
             1222  LOAD_FAST                '_source'
             1224  LOAD_FAST                'i'
             1226  BINARY_SUBSCR    
             1228  STORE_ATTR               x

 L.1892      1230  LOAD_FAST                'p'
             1232  LOAD_ATTR                y
             1234  LOAD_FAST                '_source'
             1236  LOAD_FAST                'i'
             1238  BINARY_SUBSCR    
             1240  STORE_ATTR               y

 L.1893      1242  LOAD_FAST                'i'
             1244  LOAD_CONST               1
             1246  INPLACE_ADD      
             1248  STORE_FAST               'i'
         1250_1252  JUMP_BACK          1214  'to 1214'
             1254  POP_BLOCK        
           1256_0  COME_FROM_LOOP     1208  '1208'
           1256_1  COME_FROM          1162  '1162'
           1256_2  COME_FROM          1124  '1124'

 L.1894      1256  LOAD_FAST                'result'
             1258  RETURN_VALUE     
           1260_0  COME_FROM          1098  '1098'

 L.1895      1260  LOAD_GLOBAL              isinstance
             1262  LOAD_FAST                '_source'
             1264  LOAD_CONST               0
             1266  BINARY_SUBSCR    
             1268  LOAD_GLOBAL              Geometry
             1270  CALL_FUNCTION_2       2  '2 positional arguments'
         1272_1274  POP_JUMP_IF_FALSE  1358  'to 1358'

 L.1896      1276  SETUP_LOOP         1354  'to 1354'
             1278  LOAD_GLOBAL              range
             1280  LOAD_GLOBAL              len
             1282  LOAD_FAST                '_source'
             1284  CALL_FUNCTION_1       1  '1 positional argument'
             1286  CALL_FUNCTION_1       1  '1 positional argument'
             1288  GET_ITER         
           1290_0  COME_FROM          1310  '1310'
             1290  FOR_ITER           1352  'to 1352'
             1292  STORE_FAST               'i'

 L.1897      1294  LOAD_FAST                '_source'
             1296  LOAD_FAST                'i'
             1298  BINARY_SUBSCR    
             1300  STORE_FAST               'geo'

 L.1898      1302  LOAD_GLOBAL              isinstance
             1304  LOAD_FAST                'geo'
             1306  LOAD_GLOBAL              Geometry
             1308  CALL_FUNCTION_2       2  '2 positional arguments'
         1310_1312  POP_JUMP_IF_FALSE  1290  'to 1290'

 L.1899      1314  LOAD_FAST                'jvm'
             1316  LOAD_ATTR                com
             1318  LOAD_ATTR                supermap
             1320  LOAD_ATTR                data
             1322  LOAD_ATTR                CoordSysTranslator
             1324  LOAD_METHOD              convert
             1326  LOAD_FAST                'geo'
             1328  LOAD_ATTR                _jobject

 L.1900      1330  LOAD_FAST                'source_prj_coordsys'
             1332  LOAD_ATTR                _jobject

 L.1901      1334  LOAD_FAST                'target_prj_coordsys'
           1336_0  COME_FROM           664  '664'
             1336  LOAD_ATTR                _jobject

 L.1902      1338  LOAD_FAST                'coordsys_trans_parameter'
             1340  LOAD_ATTR                _jobject

 L.1903      1342  LOAD_FAST                'javaMethod'
             1344  CALL_METHOD_5         5  '5 positional arguments'
             1346  POP_TOP          
         1348_1350  JUMP_BACK          1290  'to 1290'
             1352  POP_BLOCK        
           1354_0  COME_FROM_LOOP     1276  '1276'

 L.1905      1354  LOAD_CONST               True
             1356  RETURN_VALUE     
           1358_0  COME_FROM          1272  '1272'
             1358  POP_BLOCK        
             1360  JUMP_FORWARD       1406  'to 1406'
           1362_0  COME_FROM_EXCEPT   1070  '1070'

 L.1906      1362  DUP_TOP          
             1364  LOAD_GLOBAL              Exception
             1366  COMPARE_OP               exception-match
         1368_1370  POP_JUMP_IF_FALSE  1404  'to 1404'
             1372  POP_TOP          
             1374  STORE_FAST               'e'
             1376  POP_TOP          
             1378  SETUP_FINALLY      1392  'to 1392'

 L.1907      1380  LOAD_GLOBAL              log_error
             1382  LOAD_FAST                'e'
             1384  CALL_FUNCTION_1       1  '1 positional argument'
             1386  POP_TOP          
             1388  POP_BLOCK        
             1390  LOAD_CONST               None
           1392_0  COME_FROM_FINALLY  1378  '1378'
             1392  LOAD_CONST               None
             1394  STORE_FAST               'e'
             1396  DELETE_FAST              'e'
             1398  END_FINALLY      
             1400  POP_EXCEPT       
             1402  JUMP_FORWARD       1406  'to 1406'
           1404_0  COME_FROM          1368  '1368'
             1404  END_FINALLY      
           1406_0  COME_FROM          1402  '1402'
           1406_1  COME_FROM          1360  '1360'

 L.1908      1406  LOAD_CONST               False
             1408  RETURN_VALUE     
             1410  JUMP_FORWARD       1432  'to 1432'
           1412_0  COME_FROM           774  '774'

 L.1910      1412  LOAD_GLOBAL              ValueError

 L.1912      1414  LOAD_STR                 'source_data is invalid, required DatasetVector, Geometry or Point2D                  list, but now is '
             1416  LOAD_GLOBAL              str
             1418  LOAD_GLOBAL              type
             1420  LOAD_FAST                '_source'
             1422  CALL_FUNCTION_1       1  '1 positional argument'
             1424  CALL_FUNCTION_1       1  '1 positional argument'
             1426  BINARY_ADD       
             1428  CALL_FUNCTION_1       1  '1 positional argument'
             1430  RAISE_VARARGS_1       1  'exception instance'
           1432_0  COME_FROM          1410  '1410'
           1432_1  COME_FROM           758  '758'
           1432_2  COME_FROM           376  '376'

Parse error at or near `COME_FROM' instruction at offset 1336_0

    @staticmethod
    def forward(data, prj_coordsys, out_data=None, out_dataset_name=None):
        """
        在同一地理坐标系下，该方法用于将指定的 Point2D 列表中的点二维点对象从地理坐标转换到投影坐标

        :param data: 被转换的二维点列表
        :type data: list[Point2D] or tuple[Point2D]
        :param prj_coordsys: 二维点对象所在的投影坐标系
        :type prj_coordsys: PrjCoordSys
        :param out_data: 结果数据源对象，可以选择将转换后得到的点保存到数据源中。如果为空，将返回转换后得到点的列表
        :type out_data: Datasource or DatasourceConnectionInfo or str
        :param out_dataset_name: 结果数据集名称，out_datasource 有效时才起作用
        :type out_dataset_name: str
        :return: 转换失败返回None，转换成功，如果设置了有效的 out_datasource，返回结果数据集或数据集名称，否则，返回转换后得到的点的列表。
        :rtype: DatasetVector or str or list[Point2D]
        """
        if data is None:
            raise ValueError('data is None')
        else:
            if prj_coordsys is None:
                raise ValueError('prj_coordsys is None')
            if not isinstance(data, (list, tuple)):
                raise ValueError('data must be Point2D or Point2D list.')
            srcPoints = list(filter(lambda point: isinstance(point, Point2D), data))
            jvm = get_jvm()
            from ._util import to_java_point2ds, get_output_datasource, check_output_datasource, try_close_output_datasource
            java_points = to_java_point2ds(srcPoints)
            if jvm.com.supermap.data.CoordSysTranslator.forward(java_points, prj_coordsys._jobject):

                def fun(i):
                    point = java_points.getItem(i)
                    return Point2D(point.getX(), point.getY())

                _r_points = list((fun(i) for i in range(java_points.getCount())))
                if out_data is not None:
                    _out_datasource = get_output_datasource(out_data)
                    check_output_datasource(_out_datasource)
                    result_dt = _out_datasource.write_spatial_data(_r_points, out_dataset_name)
                    return try_close_output_datasource(result_dt, _out_datasource)
                return _r_points
            else:
                return

    @staticmethod
    def inverse(data, prj_coordsys, out_data=None, out_dataset_name=None):
        """
        在同一投影坐标系下，该方法用于将指定的 Point2D 列表中的二维点对象从投影坐标转换到地理坐标。

        :param data: 被转换的二维点列表
        :type data: list[Point2D] or tuple[Point2D]
        :param prj_coordsys: 二维点对象所在的投影坐标系
        :type prj_coordsys: PrjCoordSys
        :param out_data: 结果数据源对象，可以选择将转换后得到的点保存到数据源中。如果为空，将返回转换后得到点的列表
        :type out_data: Datasource or DatasourceConnectionInfo or str
        :param out_dataset_name: 结果数据集名称，out_datasource 有效时才起作用
        :type out_dataset_name: str
        :return: 转换失败返回None，转换成功，如果设置了有效的 out_datasource，返回结果数据集或数据集名称，否则，返回转换后得到的点的列表。
        :rtype: DatasetVector or str or list[Point2D]
        """
        if data is None:
            raise ValueError('data is None')
        else:
            if prj_coordsys is None:
                raise ValueError('prj_coordsys is None')
            if not isinstance(data, (list, tuple)):
                raise ValueError('data must be Point2D or Point2D list.')
            srcPoints = list(filter(lambda p: isinstance(p, Point2D), data))
            jvm = get_jvm()
            from ._util import to_java_point2ds, get_output_datasource, check_output_datasource, try_close_output_datasource
            java_points = to_java_point2ds(srcPoints)
            if jvm.com.supermap.data.CoordSysTranslator.inverse(java_points, prj_coordsys._jobject):

                def fun(i):
                    point = java_points.getItem(i)
                    return Point2D(point.getX(), point.getY())

                _r_points = list((fun(i) for i in range(java_points.getCount())))
                if out_data is not None:
                    _out_datasource = get_output_datasource(out_data)
                    check_output_datasource(_out_datasource)
                    resName = _out_datasource.write_spatial_data(_r_points, out_dataset_name)
                    try_close_output_datasource(None, _out_datasource)
                    if resName is None:
                        log_error('Failed to write inverse result data to output datasource')
                        return False
                    return resName
                else:
                    i = 0
                    for p in _r_points:
                        srcPoints[i].x = p.x
                        srcPoints[i].y = p.y
                        i += 1

                    return True
            else:
                return False