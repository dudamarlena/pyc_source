# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\graphics\ConfigPanel.py
# Compiled at: 2016-02-07 12:07:02
import wx, wx.propgrid as wxpg
from mplotlab.graphics import propertyMap
from mplotlab.utils import log
from mplotlab import App
from mplotlab.models import COLOR
from matplotlib.colors import ColorConverter, rgb2hex

class ConfigPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.txt = wx.StaticText(self, -1, '')
        self.panel = wx.Panel(self, -1)
        self.pg = wxpg.PropertyGridManager(self.panel, style=wxpg.PG_SPLITTER_AUTO_CENTER | wxpg.PG_AUTO_SORT)
        self.but = wx.Button(self.panel, -1, 'show')
        self.__modelSel = None
        self.but.Bind(wx.EVT_BUTTON, self.updateFigure)
        self.pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)
        self.setProperties()
        return

    def setProperties(self):
        topsizer = wx.BoxSizer(wx.VERTICAL)
        topsizer.Add(self.txt, 0, wx.EXPAND)
        topsizer.Add(self.pg, 1, wx.EXPAND)
        topsizer.Add(self.but, 0, wx.EXPAND)
        self.panel.SetSizer(topsizer)
        topsizer.SetSizeHints(self.panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()

    def updateFigure(self, event):
        if self.__modelSel is None:
            return
        else:
            for name, value in self.pg.GetPropertyValues().items():
                if COLOR == self.__modelSel.getProperties()[name]:
                    r, g, b = value.Get()
                    value = (r / 255.0, g / 255.0, b / 255.0)
                    value = rgb2hex(value)
                if isinstance(value, unicode):
                    value = value.encode()
                self.__modelSel.setAttr(name, value)

            App().mainWin.showSlideSel()
            return

    def updatePage(self, modelSel):
        if modelSel is None:
            self.txt.SetLabel('')
            return
        else:
            txtLabel = modelSel.get_name()
            self.txt.SetLabel(txtLabel)
            log.info(txtLabel)
            self.__modelSel = modelSel
            if self.pg.GetPageCount() > 0:
                self.pg.RemovePage(0)
            self.pg.AddPage(txtLabel)
            for name, propertyKey in modelSel.getProperties().items():
                propertyClass = propertyMap[propertyKey]
                value = modelSel.getAttr(name)
                if 'alpha' == name and value is None:
                    value = 1.0
                if 'color' == propertyKey:
                    c = ColorConverter()
                    if isinstance(value, (unicode, str)):
                        if 'none' == value.lower():
                            value = None
                        else:
                            value = c.to_rgb(value)
                    if value is not None:
                        try:
                            r, g, b = value
                        except:
                            r, g, b, _ = value

                        value = wx.Colour(r * 255, g * 255, b * 255)
                log.info('%s:%s' % (name, value))
                if value is not None:
                    self.pg.Append(propertyClass(name, value=value))
                else:
                    self.pg.Append(propertyClass(name))

            return