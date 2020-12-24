# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\graphics\GraphicBook.py
# Compiled at: 2016-02-07 09:44:32
import wx
from wx.aui import AuiNotebook
from mplotlab import App
from GraphicPanel import GraphicPanel

class GraphicBook(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.__book = AuiNotebook(self)
        self.layout()

    def layout(self):
        sizer = wx.BoxSizer()
        sizer.Add(self.__book, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.__book.SendSizeEvent)

    def updateBook(self):
        """
        Delete graphicPanel pages that refer to 'obselete' slide
        And update book page name from its slide name
        """
        cs = {slide:slide.get_name() for slide in App().mainWin.getContainer().getSlides()}
        for i, gp in enumerate(self.getGraphicPanels()):
            s = gp.getSlide()
            if s not in cs.keys():
                self.__book.DeletePage(i)
            else:
                self.__book.SetPageText(i, cs[s])

    def createGraphicPanel(self, slide):
        """ Create the graphic panel for the slide
        if necessary and select it.
        There cannot be 2 graphic panels for the same
        slide
        """
        ss = self.getGraphicSlides()
        if slide not in ss:
            gp = GraphicPanel(self)
            gp.setSlide(slide)
            self.__book.AddPage(gp, slide.get_name())
            idx = self.__book.GetPageCount() - 1
        else:
            idx = ss.index(slide)
            gp = self.getGraphicPanels()[idx]
        self.__book.SetSelection(idx)
        return gp

    def getGraphicSlides(self):
        return [ gp.getSlide() for gp in self.getGraphicPanels() ]

    def getGraphicPanels(self):
        return [ self.__book.GetPage(i) for i in range(self.__book.GetPageCount())
               ]

    def getCurrentSlide(self):
        i = self.__book.GetSelection()
        if i == -1:
            return
        else:
            return self.getGraphicSlides()[i]
            return