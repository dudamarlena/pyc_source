# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyromsgui.py
# Compiled at: 2014-11-26 23:59:34
import os, wx, datetime as dt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as Navbar
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import numpy as np, matplotlib.pyplot as plt
from matplotlib.path import Path
import scipy.io as sp, netCDF4 as nc
from lib import *
currentDirectory = os.getcwd()
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_VMIN = 0
DEFAULT_VMAX = 1.5
DEFAULT_CMAP = plt.cm.BrBG
DEFAULT_DEPTH_FOR_LAND = -50

class App(wx.App):

    def OnInit(self):
        self.frame = Interface('PyRomsGUI 0.1.0', size=(1024, 800))
        self.frame.Show()
        return True


class Interface(wx.Frame):

    def __init__(self, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, *args, **kwargs):
        wx.Frame.__init__(self, None, (-1), 'PyRomsGUI 0.1.0', pos=pos, size=size, style=style, *args, **kwargs)
        self.toolbar = MainToolBar(self)
        panel1 = wx.Panel(self, wx.ID_ANY, style=wx.SUNKEN_BORDER)
        mplpanel = wx.Panel(self, wx.ID_ANY, style=wx.SUNKEN_BORDER)
        mplpanel.SetBackgroundColour('WHITE')
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(panel1, 1, wx.EXPAND)
        box1.Add(mplpanel, 4, wx.EXPAND)
        box2 = wx.BoxSizer(wx.VERTICAL)
        box3 = wx.BoxSizer(wx.VERTICAL)
        variable = wx.StaticText(panel1, label='Variable')
        box2.Add(variable, proportion=0, flag=wx.CENTER)
        self.var_select = wx.ComboBox(panel1, value='Choose variable')
        box2.Add(self.var_select, proportion=0, flag=wx.CENTER)
        self.var_select.Bind(wx.EVT_COMBOBOX, self.toolbar.OnUpdateHslice)
        time = wx.StaticText(panel1, label='Time record')
        box2.Add(time, proportion=0, flag=wx.CENTER)
        self.time_select = wx.ComboBox(panel1, value='Choose time step')
        box2.Add(self.time_select, proportion=0, flag=wx.CENTER)
        self.time_select.Bind(wx.EVT_COMBOBOX, self.toolbar.OnUpdateHslice)
        self.mplpanel = SimpleMPLCanvas(mplpanel)
        box3.Add(self.mplpanel.canvas, 1, flag=wx.CENTER)
        self.SetAutoLayout(True)
        panel1.SetSizer(box2)
        mplpanel.SetSizer(box3)
        self.SetSizer(box1)
        self.InitMenu()
        self.Layout()
        self.Centre()
        return

    def InitMenu(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_OPEN, '&Open ROMS grid file')
        fileMenu.Append(wx.ID_OPEN, '&Open coastline file')
        fileMenu.Append(wx.ID_SAVE, '&Save grid')
        fileMenu.AppendSeparator()
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        opf = wx.MenuItem(fileMenu, wx.ID_OPEN, '&Open\tCtrl+O')
        opc = wx.MenuItem(fileMenu, wx.ID_OPEN, '&Open\tCtrl+O+C')
        svf = wx.MenuItem(fileMenu, wx.ID_SAVE, '&Save\tCtrl+S')
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        self.Bind(wx.EVT_MENU, self.toolbar.OnLoadFile, opf)
        self.Bind(wx.EVT_MENU, self.toolbar.OnLoadCoastline, opc)
        self.Bind(wx.EVT_MENU, self.toolbar.OnPlotVslice, svf)
        menubar.Append(fileMenu, '&PyRomsGUI')
        self.SetMenuBar(menubar)

    def OnQuit(self, e):
        """Fecha o programa"""
        self.Close()
        self.Destroy()

    def OnCloseWindow(self, e):
        self.Destroy()


class SimpleMPLCanvas(object):
    """docstring for SimpleMPLCanvas"""

    def __init__(self, parent):
        super(SimpleMPLCanvas, self).__init__()
        self.parent = parent
        self.plot_properties()
        self.make_navbar()

    def make_navbar(self):
        self.navbar = Navbar(self.canvas)
        self.navbar.SetPosition(wx.Point(0, 0))

    def plot_properties(self):
        self.fig = Figure(facecolor='w', figsize=(12, 8))
        self.canvas = FigureCanvas(self.parent, -1, self.fig)
        self.ax = self.fig.add_subplot(111)


class MainToolBar(object):

    def __init__(self, parent):
        self.currentDirectory = os.getcwd()
        self.parent = parent
        self.toolbar = parent.CreateToolBar(style=1, winid=1, name='Toolbar')
        self.tools_params = {'load_file': (
                       load_bitmap('grid.png'), 'Load ROMS netcdf file',
                       'Load ocean_???.nc ROMS netcdf file'), 
           'load_coastline': (
                            load_bitmap('coast.png'), 'Load coastline',
                            'Load *.mat coastline file [lon / lat poligons]'), 
           'plot_vslice': (
                         load_bitmap('save.png'), 'Plot vertical slice',
                         'Plot vertical slice of some variable'), 
           'settings': (
                      load_bitmap('settings.png'), 'PyRomsGUI settings',
                      'PyRomsGUI configurations'), 
           'quit': (
                  load_bitmap('exit.png'), 'Quit',
                  'Quit PyRomsGUI')}
        self.createTool(self.toolbar, self.tools_params['load_file'], self.OnLoadFile)
        self.createTool(self.toolbar, self.tools_params['load_coastline'], self.OnLoadCoastline)
        self.toolbar.AddSeparator()
        self.plot_vslice = self.createTool(self.toolbar, self.tools_params['plot_vslice'], self.OnPlotVslice, isToggle=True)
        self.toolbar.AddSeparator()
        self.createTool(self.toolbar, self.tools_params['settings'], self.OnSettings)
        self.createTool(self.toolbar, self.tools_params['quit'], self.parent.OnQuit)
        self.toolbar.Realize()

    def createTool(self, parent, params, evt, isToggle=False):
        tool = parent.AddTool(wx.NewId(), bitmap=params[0], shortHelpString=params[1], longHelpString=params[2], isToggle=isToggle)
        self.parent.Bind(wx.EVT_TOOL, evt, id=tool.GetId())
        return tool

    def OnLoadFile(self, evt):
        openFileDialog = wx.FileDialog(self.parent, 'Open roms netcdf file [*.nc]', '/ops/forecast/roms/', ' ', 'netcdf files (*.nc)|*.nc', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        filename = openFileDialog.GetPath()
        self.ncfile = nc.Dataset(filename)
        varlist, axeslist, time = taste_ncfile(self.ncfile)
        timelist = romsTime2string(time)
        app.frame.var_select.SetItems(varlist)
        app.frame.time_select.SetItems(timelist)
        app.frame.time_select.SetValue(timelist[0])
        openFileDialog = wx.FileDialog(self.parent, 'Open roms GRID netcdf file [*_grd.nc]', '/ops/forecast/roms/', ' ', 'netcdf files (*.nc)|*.nc', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        grdname = openFileDialog.GetPath()
        self.grd = nc.Dataset(grdname)
        lon = self.grd.variables['lon_rho'][:]
        lat = self.grd.variables['lat_rho'][:]
        h = self.grd.variables['h'][:]
        mplpanel = app.frame.mplpanel
        ax = mplpanel.ax
        self.pcolor = ax.pcolormesh(lon, lat, h)
        ax.set_xlim([lon.min(), lon.max()])
        ax.set_ylim([lat.min(), lat.max()])
        ax.set_aspect('equal')
        mplpanel.canvas.draw()

    def OnUpdateHslice(self, evt):
        varname = app.frame.var_select.GetValue()
        var = self.ncfile.variables[varname]
        dimensions = var.dimensions
        grid = dimensions[(-1)].split('_')[(-1)]
        lon = self.grd.variables[('lon_' + grid)][:]
        lat = self.grd.variables[('lat_' + grid)][:]
        varlist, axeslist, time = taste_ncfile(self.ncfile)
        timestr = app.frame.time_select.GetValue()
        selected_time = string2romsTime(timestr, self.ncfile)
        tindex = np.where(time[:] == selected_time)[0][0]
        if len(dimensions) == 3:
            arr = var[(tindex, ...)]
        if len(dimensions) == 4:
            arr = var[(tindex, -1, ...)]
        mplpanel = app.frame.mplpanel
        ax = mplpanel.ax
        ax.clear()
        ax.pcolormesh(lon, lat, arr)
        ax.set_xlim([lon.min(), lon.max()])
        ax.set_ylim([lat.min(), lat.max()])
        ax.set_title('%s   %s' % (varname, timestr))
        ax.set_aspect('equal')
        mplpanel.canvas.draw()

    def OnLoadCoastline(self, evt):
        openFileDialog = wx.FileDialog(self.parent, 'Open coastline file - MATLAB Seagrid-like format', '/home/rsoutelino/metocean/projects/mermaid', ' ', 'MAT files (*.mat)|*.mat', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        filename = openFileDialog.GetPath()
        coast = sp.loadmat(filename)
        lon, lat = coast['lon'], coast['lat']
        mplpanel = app.frame.mplpanel
        ax = mplpanel.ax
        ax.plot(lon, lat, 'k')
        try:
            ax.set_xlim([self.grd.lonr.min(), self.grd.lonr.max()])
            ax.set_ylim([self.grd.latr.min(), self.grd.latr.max()])
        except AttributeError:
            ax.set_xlim([np.nanmin(lon), np.nanmax(lon)])
            ax.set_ylim([np.nanmin(lat), np.nanmax(lat)])

        ax.set_aspect('equal')
        mplpanel.canvas.draw()

    def OnPlotVslice(self, evt):
        mplpanel = app.frame.mplpanel
        if self.plot_vslice.IsToggled():
            self.cid = mplpanel.canvas.mpl_connect('button_press_event', self.vslice)
        else:
            mplpanel.canvas.mpl_disconnect(self.cid)

    def OnSettings(self, evt):
        pass

    def vslice(self, evt):
        if evt.inaxes != app.frame.mplpanel.ax:
            return
        mplpanel = app.frame.mplpanel
        ax = mplpanel.ax
        x, y = evt.xdata, evt.ydata
        button = evt.button
        p = ax.plot(x, y, 'wo')
        try:
            self.points.append(p)
            self.area.append((x, y))
        except AttributeError:
            self.points = [
             p]
            self.area = [(x, y)]

        if len(self.points) == 2:
            ax.plot([self.area[0][0], self.area[1][0]], [
             self.area[0][1], self.area[1][1]], 'k')
            p1, p2 = self.area[0], self.area[1]
        mplpanel.canvas.draw()
        if len(self.points) == 2:
            varname = app.frame.var_select.GetValue()
            var = self.ncfile.variables[varname]
            dimensions = var.dimensions
            grid = dimensions[(-1)].split('_')[(-1)]
            lon = self.grd.variables[('lon_' + grid)][:]
            lat = self.grd.variables[('lat_' + grid)][:]
            ts = self.ncfile.variables['theta_s'][:]
            tb = self.ncfile.variables['theta_b'][:]
            hc = self.ncfile.variables['hc'][:]
            nlev = var.shape[1]
            sc = (np.arange(1, nlev + 1) - nlev - 0.5) / nlev
            sigma = self.ncfile.variables['Cs_r'][:]
            dl = (np.gradient(lon)[1].mean() + np.gradient(lat)[0].mean()) / 2
            siz = int(np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) / dl)
            xs = np.linspace(p1[0], p2[0], siz)
            ys = np.linspace(p1[1], p2[1], siz)
            varlist, axeslist, time = taste_ncfile(self.ncfile)
            timestr = app.frame.time_select.GetValue()
            selected_time = string2romsTime(timestr, self.ncfile)
            tindex = np.where(time[:] == selected_time)[0][0]
            hsec, zeta, vsec = [], [], []
            for ind in range(xs.size):
                line, col = near2d(lon, lat, xs[ind], ys[ind])
                vsec.append(var[tindex, :, line, col])
                hsec.append(self.grd.variables['h'][(line, col)])
                zeta.append(self.ncfile.variables['zeta'][(tindex, line, col)])

            vsec = np.array(vsec).transpose()
            hsec, zeta = np.array(hsec), np.array(zeta)
            xs = xs.reshape(1, xs.size).repeat(nlev, axis=0)
            ys = ys.reshape(1, ys.size).repeat(nlev, axis=0)
            zsec = get_zlev(hsec, sigma, 5, sc, ssh=zeta, Vtransform=2)
            xs = np.ma.masked_where(vsec > 1e+20, xs)
            ys = np.ma.masked_where(vsec > 1e+20, ys)
            zsec = np.ma.masked_where(vsec > 1e+20, zsec)
            vsec = np.ma.masked_where(vsec > 1e+20, vsec)
            self.vslice_dialog = VsliceDialog(app.frame, xs, ys, zsec, vsec)
            del self.points
            del self.area
        mplpanel.canvas.draw()


class VsliceDialog(wx.Dialog):

    def __init__(self, parent, xs, ys, zsec, vsec, *args, **kwargs):
        wx.Dialog.__init__(self, parent, -1, 'VARIABLE Vertical Slice, TIMERECORD', pos=(0,
                                                                                         0), size=(1200,
                                                                                                   600), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.xs, self.ys, self.zsec, self.vsec = (
         xs, ys, zsec, vsec)
        panel1 = wx.Panel(self, wx.ID_ANY, style=wx.SUNKEN_BORDER)
        mplpanel = wx.Panel(self, wx.ID_ANY, style=wx.SUNKEN_BORDER)
        mplpanel.SetBackgroundColour('WHITE')
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(panel1, 1, wx.EXPAND)
        box1.Add(mplpanel, 4, wx.EXPAND)
        box2 = wx.BoxSizer(wx.VERTICAL)
        box3 = wx.BoxSizer(wx.VERTICAL)
        plot_type = wx.StaticText(panel1, label='Plot type')
        box2.Add(plot_type, proportion=0, flag=wx.CENTER)
        self.plot_select = wx.ComboBox(panel1, value='scatter')
        box2.Add(self.plot_select, proportion=0, flag=wx.CENTER)
        self.plot_select.Bind(wx.EVT_COMBOBOX, self.OnUpdatePlot)
        self.plot_select.SetItems(['scatter', 'pcolormesh',
         'contourf', 'contour'])
        minmax = wx.StaticText(panel1, label='Range')
        box2.Add(minmax, proportion=0, flag=wx.CENTER)
        self.max = wx.TextCtrl(panel1, value=str(vsec.max()))
        self.min = wx.TextCtrl(panel1, value=str(vsec.min()))
        box2.Add(self.max, proportion=0, flag=wx.CENTER)
        box2.Add(self.min, proportion=0, flag=wx.CENTER)
        scale = wx.StaticText(panel1, label='Scatter scale')
        box2.Add(scale, proportion=0, flag=wx.CENTER)
        self.scatter_scale = wx.SpinCtrl(panel1, value='50')
        box2.Add(self.scatter_scale, proportion=0, flag=wx.CENTER)
        self.mplpanel = SimpleMPLCanvas(mplpanel)
        box3.Add(self.mplpanel.canvas, 1, flag=wx.CENTER)
        ax = self.mplpanel.ax
        pl = ax.scatter(xs.ravel(), zsec.ravel(), s=50, c=vsec.ravel(), edgecolors='none')
        self.mplpanel.ax2 = self.mplpanel.fig.add_axes([0.93, 0.15, 0.015, 0.7])
        ax2 = self.mplpanel.ax2
        cbar = self.mplpanel.fig.colorbar(pl, cax=ax2)
        ax.set_xlim([xs.min(), xs.max()])
        ax.set_ylim([zsec.min(), zsec.max()])
        self.mplpanel.canvas.draw()
        self.SetAutoLayout(True)
        panel1.SetSizer(box2)
        mplpanel.SetSizer(box3)
        self.SetSizer(box1)
        self.Show()

    def OnUpdatePlot(self, evt):
        xs, ys, zsec, vsec = (
         self.xs, self.ys, self.zsec, self.vsec)
        ax, ax2 = self.mplpanel.ax, self.mplpanel.ax2
        ax.clear()
        ax2.clear()
        vmin, vmax = float(self.min.GetValue()), float(self.max.GetValue())
        plot_type = self.plot_select.GetValue()
        sc = self.scatter_scale.GetValue()
        if plot_type == 'scatter':
            pl = ax.scatter(xs.ravel(), zsec.ravel(), s=sc, c=vsec.ravel(), vmin=vmin, vmax=vmax, edgecolors='none')
        elif plot_type == 'pcolormesh':
            pl = ax.pcolormesh(xs, zsec, vsec, vmin=vmin, vmax=vmax)
        elif plot_type == 'contourf':
            zsec = np.array(zsec)
            f = np.where(np.isnan(zsec) == True)
            zsec[f] = 0
            levs = np.linspace(vmin, vmax, 50)
            pl = ax.contourf(xs, zsec, vsec, levs)
        elif plot_type == 'contour':
            zsec = np.array(zsec)
            f = np.where(np.isnan(zsec) == True)
            zsec[f] = 0
            levs = np.linspace(vmin, vmax, 50)
            pl = ax.contour(xs, zsec, vsec, levs)
        ax.set_xlim([xs.min(), xs.max()])
        ax.set_ylim([zsec.min(), zsec.max()])
        cbar = self.mplpanel.fig.colorbar(pl, cax=ax2)
        self.mplpanel.canvas.draw()


def taste_ncfile(ncfile):
    try:
        if 'history' in ncfile.type:
            filetype = 'his'
        elif 'restart' in ncfile.type:
            filetype = 'rst'
    except AttributeError:
        print 'Not a standard ROMS file !'
        filetype = 'clim'

    varlist = ROMSVARS[filetype]['variables']
    axeslist = ROMSVARS[filetype]['axes']
    for axes in axeslist:
        if 'time' in axes:
            time = ncfile.variables[axes]

    return (
     varlist, axeslist, time)


def romsTime2string(nctime):
    """
    nctime  :  netCDF4 variable
    """
    timeunits = nctime.units
    units = timeunits.split(' ')[0]
    tstart = dt.datetime.strptime(timeunits.split(' ')[(-2)], '%Y-%m-%d')
    timelist = []
    for t in nctime[:]:
        if units == 'seconds':
            current = tstart + dt.timedelta(seconds=t)
        if units == 'days':
            current = tstart + dt.timedelta(seconds=t * 86400)
        timelist.append(current.strftime('%Y-%m-%d  %H h'))

    return timelist


def string2romsTime(timelist, ncfile):
    if not isinstance(timelist, list):
        timelist = [
         timelist]
    varlist, axeslist, time = taste_ncfile(ncfile)
    timeunits = time.units
    units = timeunits.split(' ')[0]
    tstart = dt.datetime.strptime(timeunits.split(' ')[(-2)], '%Y-%m-%d')
    romstime = []
    for timestr in timelist:
        dttime = dt.datetime.strptime(timestr, '%Y-%m-%d  %H h')
        delta = dttime - tstart
        if units == 'seconds':
            current = delta.seconds
        if units == 'days':
            current = delta.days
        romstime.append(current)

    if len(romstime) == 1:
        return romstime[0]
    else:
        return romstime


def load_bitmap(filename, direc=None):
    """
    Load a bitmap file from the ./icons subdirectory. 
    The filename parameter should not
    contain any path information as this is determined automatically.

    Returns a wx.Bitmap object
    copied from matoplotlib resources
    """
    if not direc:
        basedir = os.path.join(PROJECT_DIR, 'icons')
    else:
        basedir = os.path.join(PROJECT_DIR, direc)
    bmpFilename = os.path.normpath(os.path.join(basedir, filename))
    if not os.path.exists(bmpFilename):
        raise IOError('Could not find bitmap file "%s"; dying' % bmpFilename)
    bmp = wx.Bitmap(bmpFilename)
    return bmp


if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
# global currentDirectory ## Warning: Unused global