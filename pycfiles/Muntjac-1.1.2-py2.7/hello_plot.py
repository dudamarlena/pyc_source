# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/invient/demo/hello_plot.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.api import VerticalLayout, HorizontalLayout, TextField, PasswordField, Button, Alignment, AbsoluteLayout
from muntjac.ui.button import IClickListener
from muntjac.api import Label, Window, Application
from muntjac.ui.window import Notification
from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet
from paste.urlmap import URLMap
from paste.session import SessionMiddleware
from paste.fileapp import DirectoryApp
from wsgiref.simple_server import make_server
from muntjac.terminal.sizeable import ISizeable
from muntjac.addon.invient.invient_charts import ChartZoomListener, DateTimePoint, InvientCharts, DateTimeSeries, SeriesType, XYSeries, DecimalPoint, PointClickListener, ChartSVGAvailableListener, ChartClickListener, ChartResetZoomListener, SeriesClickListerner, SeriesHideListerner, SeriesShowListerner, SeriesLegendItemClickListerner, PointRemoveListener, PointSelectListener, PointUnselectListener, PieChartLegendItemClickListener
from muntjac.addon.invient.invient_charts_config import DateTimePlotBand, DateTimeRange, InvientChartsConfig, Margin, DateTimeAxis, NumberYAxis, AxisTitle, LineConfig, SymbolMarker, MarkerState, ZoomType, YAxisDataLabel, Grid, AreaConfig, SeriesState, CategoryAxis, NumberPlotLine, Legend, Layout, Position, HorzAlign, VertAlign, NumberValue, NumberXAxis, ScatterConfig, DataLabel, SeriesConfig, Stacking, AxisTitleAlign, BarConfig, Tooltip, ColumnConfig, XAxisDataLabel, Spacing, Tick, TickmarkPlacement, Symbol, NumberPlotBand, NumberRange, AreaSplineConfig, PieConfig, PieDataLabel, PointConfig, SplineConfig, ImageMarker, MinorGrid, PlotLabel, ChartLabel, ChartLabelItem, DashStyle
from muntjac.addon.invient.color import RGBA, RGB
from muntjac.addon.invient.gradient import LinearColorStop, LinearGradient
from muntjac.util import totalseconds, OrderedSet
import numpy as N, time

class PlotWindow(Window):
    _TREE_ITEM_CAPTION_PROP_ID = 'PlotChartWindow'
    _SEPARATOR = '|'

    def __init__(self):
        super(PlotWindow, self).__init__()
        self.mainLayout = VerticalLayout()
        self.setContent(self.mainLayout)
        self.setCaption('Basic Example')
        infoBar = HorizontalLayout()
        self.mainLayout.addComponent(infoBar)
        infoBar.setHeight('50px')
        infoBar.setWidth('100%')
        self.showPlot()

    @classmethod
    def getPoints(cls, series, values):
        if len(values) > 0 and isinstance(values[0], (float, int)):
            points = OrderedSet()
            for value in values:
                points.add(DecimalPoint(series, value))

            return points
        points = OrderedSet()
        for value in values:
            y = None
            if len(value) == 0:
                continue
            if len(value) == 2:
                x = value[0]
                y = value[1]
            else:
                x = value[0]
            points.add(DecimalPoint(series, x, y))

        return points
        return

    def showPlot(self):
        chartConfig = InvientChartsConfig()
        chartConfig.getGeneralChartConfig().setType(SeriesType.LINE)
        chartConfig.getGeneralChartConfig().setZoomType(ZoomType.XY)
        chartConfig.getTitle().setText('Invient Test')
        chartConfig.getSubtitle().setText('Numpy Random')
        xAxis = NumberXAxis()
        xAxis.setTitle(AxisTitle('Data #'))
        xAxis.setStartOnTick(True)
        xAxis.setEndOnTick(True)
        xAxis.setShowLastLabel(True)
        xAxesSet = set()
        xAxesSet.add(xAxis)
        chartConfig.setXAxes(xAxesSet)
        yAxis = NumberYAxis()
        yAxis.setTitle(AxisTitle('Value'))
        yAxesSet = set()
        yAxesSet.add(yAxis)
        chartConfig.setYAxes(yAxesSet)
        legend = Legend()
        legend.setLayout(Layout.VERTICAL)
        legendPos = Position()
        legendPos.setAlign(HorzAlign.LEFT)
        legendPos.setVertAlign(VertAlign.TOP)
        legendPos.setX(100)
        legendPos.setY(70)
        legend.setPosition(legendPos)
        legend.setFloating(True)
        legend.setBorderWidth(1)
        legend.setBackgroundColor(RGB(255, 255, 255))
        chartConfig.setLegend(legend)
        plotCfg = LineConfig()
        marker = SymbolMarker(False)
        plotCfg.setMarker(marker)
        plotCfg.setColor(RGBA(223, 83, 83, 0.5))
        plotCfg.setAllowPointSelect(False)
        plotCfg.setEnableMouseTracking(False)
        plotCfg.setAnimation(False)
        chartConfig.addSeriesConfig(plotCfg)
        series = XYSeries('Set 1', plotCfg)
        series.setSeriesPoints(self.setData(series))
        chart = InvientCharts(chartConfig)
        chart.addSeries(series)
        self.addChart(chart)

    def setData(self, series):
        return self.getPoints(series, N.random.rand(250))

    def addChart(self, chart, isPrepend=False, isRegisterEvents=True, isRegisterSVGEvent=True, isSetHeight=True):
        chart.setSizeFull()
        chart.setStyleName('v-chart-min-width')
        if isSetHeight:
            chart.setHeight('410px')
        self.mainLayout.removeAllComponents()
        self.mainLayout.addComponent(chart)


class HelloPlot(Application):

    def init(self):
        """Init is invoked on application load (when a user accesses
        the application for the first time).
        """
        mainWindow = PlotWindow()
        self.setMainWindow(mainWindow)


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(HelloPlot, nogui=True, debug=True, contextRoot='.')