# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/extra_guiqwt/image.py
# Compiled at: 2019-08-19 15:09:29
"""
Extension of :mod:`guiqwt.image`
"""
__all__ = [
 'TaurusImageItem', 'TaurusRGBImageItem', 'TaurusTrend2DItem',
 'TaurusTrend2DScanItem', 'TaurusEncodedImageItem',
 'TaurusEncodedRGBImageItem']
from taurus.core.units import Quantity
from taurus.external.qt import Qt
from taurus.qt.qtgui.base import TaurusBaseComponent
from taurus.qt.qtcore.util import baseSignal
import taurus.core
from taurus.core.util.containers import ArrayBuffer
from guiqwt.image import ImageItem, RGBImageItem, XYImageItem
from guiqwt.image import INTERP_NEAREST, INTERP_LINEAR
import numpy

class TaurusBaseImageItem(TaurusBaseComponent):
    """A ImageItem that gets its data from a taurus attribute"""
    dataChanged = baseSignal('dataChanged')

    def setModel(self, model):
        TaurusBaseComponent.setModel(self, model)
        try:
            value = self.getModelObj().read()
            self.fireEvent(self, taurus.core.taurusbasetypes.TaurusEventType.Change, value)
        except:
            pass

    def handleEvent(self, evt_src, evt_type, evt_value):
        if evt_value is None or getattr(evt_value, 'rvalue', None) is None:
            self.debug('Ignoring event from %s' % repr(evt_src))
            return
        else:
            v = evt_value.rvalue
            if isinstance(v, Quantity):
                v = v.magnitude
            try:
                v = self.filterData(v)
            except Exception as e:
                self.info('Ignoring event. Reason: %s', e.message)
                return

            lut_range = self.get_lut_range()
            if lut_range[0] == lut_range[1]:
                lut_range = None
            self.set_data(v, lut_range=lut_range)
            self.dataChanged.emit()
            p = self.plot()
            if p is not None:
                p.update_colormap_axis(self)
                p.replot()
            return

    def filterData(self, data):
        """Reimplement this method if you want to pre-process
        the data that will be passed to set_data.

        It should return something acceptable by :meth:`setData`
        and raise an exception if the data cannot be processed.

        This default implementation casts array types not
        supported by guiqwt to numpy.int32

        See:
          - http://code.google.com/p/guiqwt/issues/detail?id=44 and
          - https://sourceforge.net/tracker/?func=detail&atid=484769&aid=3603991&group_id=57612
          - https://sourceforge.net/p/tauruslib/tickets/33/
        """
        try:
            dtype = data.dtype
            v = data
        except:
            v = numpy.array(data)
            dtype = v.dtype

        if dtype not in (float, numpy.double, numpy.int32, numpy.uint16,
         numpy.int16, numpy.uint8, numpy.int8, bool):
            try:
                self.debug('casting to numpy.int32')
                v = numpy.int32(v)
            except OverflowError:
                raise OverflowError('type %s not supported by guiqwt and cannot be casted to int32' % repr(v.dtype))

        return v


class TaurusEncodedBaseImageItem(TaurusBaseImageItem):
    """A ImageItem that gets its data from a taurus DevEncoded attribute"""

    def setModel(self, model):
        TaurusBaseComponent.setModel(self, model)
        try:
            fmt, value = self.codec.decode(self.getModelObj().read())
            self.fireEvent(self, taurus.core.taurusbasetypes.TaurusEventType.Change, value)
        except:
            pass

    def filterData(self, data):
        """reimplementation to decode data using the DevEncoded codecs"""
        if type(data) == tuple:
            from taurus.core.util.codecs import CodecFactory
            codec = CodecFactory().getCodec(data[0])
            try:
                fmt, decoded_data = codec.decode(data)
            except Exception as e:
                self.info('Decoder error: %s', e.message)
                raise e

            try:
                dtype = decoded_data.dtype
                v = decoded_data
            except:
                v = numpy.array(decoded_data)
                dtype = v.dtype

            if dtype not in (float, numpy.double, numpy.int32, numpy.uint16,
             numpy.int16, numpy.uint8, numpy.int8, bool):
                try:
                    self.debug('casting to numpy.int32')
                    v = numpy.int32(v)
                except OverflowError:
                    raise OverflowError('type %s not supported by guiqwt and cannot be casted to int32' % repr(v.dtype))

            return v
        raise ValueError('Unexpected data type (%s) for DevEncoded attribute (tuple expected)' % type(data))


class TaurusImageItem(ImageItem, TaurusBaseImageItem):
    """A ImageItem that gets its data from a taurus attribute"""

    def __init__(self, param=None):
        ImageItem.__init__(self, numpy.zeros((1, 1)), param=param)
        TaurusBaseImageItem.__init__(self, self.__class__.__name__)


class TaurusEncodedImageItem(ImageItem, TaurusEncodedBaseImageItem):
    """A ImageItem that gets its data from a DevEncoded attribute"""

    def __init__(self, param=None):
        ImageItem.__init__(self, numpy.zeros((1, 1)), param=param)
        TaurusEncodedBaseImageItem.__init__(self, self.__class__.__name__)


class TaurusXYImageItem(XYImageItem, TaurusBaseImageItem):
    """A XYImageItem that gets its data from a taurus attribute"""

    def __init__(self, param=None):
        XYImageItem.__init__(self, numpy.arange(2), numpy.arange(2), numpy.zeros((2,
                                                                                  2)), param=param)
        TaurusBaseImageItem.__init__(self, self.__class__.__name__)


class TaurusRGBImageItem(RGBImageItem, TaurusBaseImageItem):
    """A RGBImageItem that gets its data from a taurus attribute"""

    def __init__(self, param=None):
        RGBImageItem.__init__(self, numpy.zeros((1, 1, 3)), param=param)
        TaurusBaseImageItem.__init__(self, self.__class__.__name__)

    def set_data(self, data, lut_range=None, **kwargs):
        """dummy reimplementation to accept the lut_range kwarg (just ignoring it)"""
        return RGBImageItem.set_data(self, data, **kwargs)


class TaurusEncodedRGBImageItem(RGBImageItem, TaurusEncodedBaseImageItem):
    """A RGBImageItem that gets its data from a DevEncoded attribute"""

    def __init__(self, param=None):
        RGBImageItem.__init__(self, numpy.zeros((1, 1, 3)), param=param)
        TaurusEncodedBaseImageItem.__init__(self, self.__class__.__name__)

    def set_data(self, data, lut_range=None, **kwargs):
        """dummy reimplementation to accept the lut_range kwarg (just ignoring it)"""
        return RGBImageItem.set_data(self, data, **kwargs)


class TaurusTrend2DItem(XYImageItem, TaurusBaseComponent):
    """
    A XYImageItem that is constructed by stacking 1D arrays from events from 
    a Taurus 1D attribute
    """
    scrollRequested = baseSignal('scrollRequested', object, object, object)
    dataChanged = baseSignal('dataChanged')

    def __init__(self, param=None, buffersize=512, stackMode='datetime'):
        """
        :param param: param to be passed to XYImageItem constructor
        :param buffersize: (int) size of the stack
        :param stackMode: (str) can be 'datetime', 'timedelta' or 'event'
        """
        XYImageItem.__init__(self, numpy.arange(2), numpy.arange(2), numpy.zeros((2,
                                                                                  2)), param=param)
        TaurusBaseComponent.__init__(self, self.__class__.__name__)
        self.maxBufferSize = buffersize
        self._yValues = None
        self._xBuffer = None
        self._zBuffer = None
        self.stackMode = stackMode
        self.set_interpolation(INTERP_NEAREST)
        self.__timeOffset = None
        self.registerConfigProperty(self.get_lut_range, self.set_lut_range, 'lut_range')
        self.registerConfigProperty(self._get_interpolation_cfg, self._set_interpolation_cfg, 'interpolation')
        self.registerConfigProperty(self.get_color_map_name, self.set_color_map, 'color_map')
        return

    def _get_interpolation_cfg(self):
        ret = self.get_interpolation()
        if len(ret) == 2:
            ret = (
             ret[0], len(ret[1]))
        return ret

    def _set_interpolation_cfg(self, interpolate_cfg):
        self.set_interpolation(*interpolate_cfg)

    def setBufferSize(self, buffersize):
        """sets the size of the stack

        :param buffersize: (int) size of the stack
        """
        self.maxBufferSize = buffersize
        try:
            if self._xBuffer is not None:
                self._xBuffer.setMaxSize(buffersize)
            if self._zBuffer is not None:
                self._zBuffer.setMaxSize(buffersize)
        except ValueError:
            self.info('buffer downsizing  requested. Current contents will be discarded')
            self._xBuffer = None
            self._zBuffer = None

        return

    def setModel(self, model):
        TaurusBaseComponent.setModel(self, model)
        try:
            value = self.getModelObj().read()
            self.fireEvent(self, taurus.core.taurusbasetypes.TaurusEventType.Change, value)
        except:
            pass

    def handleEvent(self, evt_src, evt_type, evt_value):
        if evt_value is None or getattr(evt_value, 'rvalue', None) is None:
            self.debug('Ignoring event from %s' % repr(evt_src))
            return
        else:
            plot = self.plot()
            if plot is None:
                return
            ySize = len(evt_value.rvalue)
            if self._yValues is None:
                self._yValues = numpy.arange(ySize, dtype='d')
            if self._xBuffer is None:
                self._xBuffer = ArrayBuffer(numpy.zeros(min(128, self.maxBufferSize), dtype='d'), maxSize=self.maxBufferSize)
            if self._zBuffer is None:
                self._zBuffer = ArrayBuffer(numpy.zeros((
                 min(128, self.maxBufferSize), ySize), dtype='d'), maxSize=self.maxBufferSize)
                return
            if ySize != self._yValues.size:
                self.info('Incompatible shape in data from event (orig=%i, current=%i). Ignoring' % (
                 self._yValues.size, ySize))
                return
            if self.stackMode == 'datetime':
                x = evt_value.time.totime()
                if self.__timeOffset is None:
                    self.__timeOffset = x
                    plot.set_axis_title('bottom', 'Time')
                    plot.set_axis_unit('bottom', '')
            else:
                if self.stackMode == 'deltatime':
                    try:
                        x = evt_value.time.totime() - self.__timeOffset
                    except TypeError:
                        self.__timeOffset = evt_value.time.totime()
                        x = 0
                        plot.set_axis_title('bottom', 'Time since %s' % evt_value.time.isoformat())
                        plot.set_axis_unit('bottom', '')

                else:
                    if self.stackMode == 'event':
                        try:
                            step = 1
                            x = self._xBuffer[(-1)] + step
                        except IndexError:
                            x = 0
                            plot.set_axis_title('bottom', 'Event #')
                            plot.set_axis_unit('bottom', '')

                    else:
                        raise ValueError('Unsupported stack mode %s' % self.stackMode)
                    if len(self._xBuffer) and x <= self._xBuffer[(-1)]:
                        self.info('Ignoring event (non-increasing x value)')
                        return
                self._xBuffer.append(x)
                rvalue = evt_value.rvalue
                if isinstance(evt_value.rvalue, Quantity):
                    rvalue = evt_value.rvalue.magnitude
                self._zBuffer.append(rvalue)
                if len(self._xBuffer) < 2:
                    self.info('waiting for at least 2 values to start plotting')
                    return
            x = self._xBuffer.contents()
            y = self._yValues
            z = self._zBuffer.contents().transpose()
            lut_range = self.get_lut_range()
            if lut_range[0] == lut_range[1]:
                lut_range = None
            self.set_data(z, lut_range=lut_range)
            self.set_xy(x, y)
            self.dataChanged.emit()
            if plot is not None:
                value = x[(-1)]
                axis = self.xAxis()
                xmin, xmax = plot.get_axis_limits(axis)
                if value > xmax or value < xmin:
                    self.scrollRequested.emit(plot, axis, value)
                plot.update_colormap_axis(self)
                plot.replot()
            return


class TaurusTrend2DScanItem(TaurusTrend2DItem):
    _xDataKey = 'point_nb'

    def __init__(self, channelKey, xDataKey, door, param=None, buffersize=512):
        TaurusTrend2DItem.__init__(self, param=param, buffersize=buffersize, stackMode=None)
        self._channelKey = channelKey
        self._xDataKey = xDataKey
        self.connectWithQDoor(door)
        return

    def scanDataReceived(self, packet):
        """
        packet is a dict with {type:str, "data":object} and the accepted types are: data_desc, record_data, record_end
        and the data objects are: seq<ColumnDesc.Todict()>, record.data dict and dict , respectively
        """
        if packet is None:
            self.debug('Ignoring empty scan data packet')
            return
        else:
            id, packet = packet
            pcktype = packet.get('type', '__UNKNOWN_PCK_TYPE__')
            if pcktype == 'data_desc':
                self._dataDescReceived(packet['data'])
            elif pcktype == 'record_data':
                self._scanLineReceived(packet['data'])
            elif pcktype == 'record_end':
                pass
            else:
                self.debug('Ignoring packet of type %s' % repr(pcktype))
            return

    def clearTrend(self):
        self._yValues = None
        self._xBuffer = None
        self._zBuffer = None
        return

    def _dataDescReceived(self, datadesc):
        """prepares the plot according to the info in the datadesc dictionary"""
        self.clearTrend()
        if self._xDataKey is None or self._xDataKey == '<mov>':
            self._autoXDataKey = datadesc['ref_moveables'][0]
        else:
            if self._xDataKey == '<idx>':
                self._autoXDataKey = 'point_nb'
            else:
                self._autoXDataKey = self._xDataKey
            columndesc = datadesc.get('column_desc', [])
            xinfo = {'min_value': None, 'max_value': None}
            for e in columndesc:
                if e['label'] == self._autoXDataKey:
                    xinfo = e
                    break

        plot = self.plot()
        plot.set_axis_title('bottom', self._autoXDataKey)
        xmin, xmax = xinfo.get('min_value'), xinfo.get('max_value')
        if xmin is None or xmax is None:
            pass
        else:
            plot.set_axis_limits('bottom', xmin, xmax)
        return

    def _scanLineReceived(self, recordData):
        """Receives a recordData dictionary and updates the curves associated to it

        .. seealso:: <Sardana>/MacroServer/scan/scandata.py:Record.data

        """
        try:
            xval = recordData[self._autoXDataKey]
        except KeyError:
            self.warning('Cannot find data "%s" in the current scan record. Ignoring', self._autoXDataKey)
            return

        if not numpy.isscalar(xval):
            self.warning('Data for "%s" is of type "%s". Cannot use it for the X values. Ignoring', self._autoXDataKey, type(xval))
            return
        else:
            try:
                chval = recordData[self._channelKey]
            except KeyError:
                self.warning('Cannot find data "%s" in the current scan record. Ignoring', self._channelKey)

            if chval.shape != self._yValues.shape:
                self.warning('Incompatible shape of "%s" (%s). Ignoring', self._channelKey, repr(chval.shape))
                return
            if self._yValues is None:
                self._yValues = numpy.arange(chval.size, dtype='d')
            if self._xBuffer is None:
                self._xBuffer = ArrayBuffer(numpy.zeros(min(16, self.maxBufferSize), dtype='d'), maxSize=self.maxBufferSize)
            if self._zBuffer is None:
                self._zBuffer = ArrayBuffer(numpy.zeros((
                 min(16, self.maxBufferSize), chval.size), dtype='d'), maxSize=self.maxBufferSize)
            self._xBuffer.append(xval)
            self._zBuffer.append(chval)
            if len(self._xBuffer) < 2:
                self.info('waiting for at least 2 values to start plotting')
                return
            x = self._xBuffer.contents()
            y = self._yValues
            z = self._zBuffer.contents().transpose()
            lut_range = self.get_lut_range()
            if lut_range[0] == lut_range[1]:
                lut_range = None
            self.set_data(z, lut_range=lut_range)
            self.set_xy(x, y)
            self.dataChanged.emit()
            plot = self.plot()
            if plot is not None:
                value = x[(-1)]
                axis = self.xAxis()
                xmin, xmax = plot.get_axis_limits(axis)
                if value > xmax or value < xmin:
                    self.scrollRequested.emit(plot, axis, value)
                plot.update_colormap_axis(self)
                plot.replot()
            return

    def connectWithQDoor(self, doorname):
        """connects this TaurusTrend2DScanItem to a QDoor

        :param doorname: (str) the QDoor name
        """
        qdoor = taurus.Device(doorname)
        qdoor.recordDataUpdated.connect(self.scanDataReceived)

    def getModel(self):
        return self.__model

    def setModel(self, model):
        self.__model = model


def taurusImageMain():
    from guiqwt.tools import RectangleTool, EllipseTool, HRangeTool, PlaceAxesTool, MultiLineTool, FreeFormTool, SegmentTool, CircleTool, AnnotatedRectangleTool, AnnotatedEllipseTool, AnnotatedSegmentTool, AnnotatedCircleTool, LabelTool, AnnotatedPointTool, ObliqueRectangleTool, AnnotatedObliqueRectangleTool
    try:
        from guiqwt.tools import AnnotatedVCursorTool, AnnotatedHCursorTool
        VCursorTool, HCursorTool = AnnotatedVCursorTool, AnnotatedHCursorTool
    except ImportError:
        from guiqwt.tools import VCursorTool, HCursorTool

    from taurus.qt.qtgui.extra_guiqwt.tools import TaurusImageChooserTool
    from guiqwt.plot import ImageDialog
    from taurus.qt.qtgui.extra_guiqwt.builder import make
    from taurus.qt.qtgui.application import TaurusApplication
    import taurus.core.util.argparse, sys
    parser = taurus.core.util.argparse.get_taurus_parser()
    parser.set_usage('%prog [options] [<model1> [<model2>] ...]')
    parser.set_description('a taurus application for plotting 2D data sets')
    app = TaurusApplication(cmd_line_parser=parser, app_name='taurusimage', app_version=taurus.Release.version)
    args = app.get_command_line_args()
    win = ImageDialog(edit=False, toolbar=True, wintitle='Taurus Image', options=dict(show_xsection=False, show_ysection=False))
    for toolklass in (TaurusImageChooserTool,
     LabelTool, HRangeTool,
     MultiLineTool, FreeFormTool, PlaceAxesTool,
     AnnotatedObliqueRectangleTool,
     AnnotatedEllipseTool, AnnotatedSegmentTool,
     AnnotatedPointTool, VCursorTool,
     HCursorTool):
        win.add_tool(toolklass)

    plot = win.get_plot()
    for m in args:
        img = make.image(taurusmodel=m)
        plot.add_item(img)
        img.dataChanged.connect(win.update_cross_sections)

    win.exec_()


def test1():
    """Adapted from guiqwt cross_section.py example"""
    from guiqwt.plot import ImageDialog
    from taurus.qt.qtgui.extra_guiqwt.builder import make
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(cmd_line_parser=None)
    model1 = 'sys/tg_test/1/ulong_image_ro'
    taurusimage = make.image(taurusmodel=model1)
    win = ImageDialog(edit=False, toolbar=True, wintitle='Taurus Cross sections test', options=dict(show_xsection=False, show_ysection=False))
    from taurus.qt.qtgui.extra_guiqwt.tools import TaurusImageChooserTool
    win.add_tool(TaurusImageChooserTool)
    plot = win.get_plot()
    plot.add_item(taurusimage)
    win.exec_()
    return


if __name__ == '__main__':
    test1()