# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathbench/lab/library.py
# Compiled at: 2008-04-07 11:18:24
"""
Display any help (and code sample) available for the functions and
libraries that can be used in the shells and scripts.
"""
import sys, logging, logging.handlers, webbrowser, wx, wx.html as html, wx.py.dispatcher as dispatcher, lab_settings
from mathbench.basement.librarian import LibrarianSingleton

class OokOokHtmlWindow(wx.html.HtmlWindow):
    """
        Catch the links that are cicked and send them to the platform's
        web browser.
        """

    def __init__(self, parent, id=-1):
        html.HtmlWindow.__init__(self, parent, id, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        if 'gtk2' in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, linkinfo):
        if sys.version_info >= (2, 5):
            webbrowser.open_new_tab(linkinfo.GetHref())
        else:
            webbrowser.open_new(linkinfo.GetHref())


class LibraryDeskHTML(wx.Frame):
    """
        The library desk from where all info can be reach.

        Handles search queries, page history, search history...
        """

    def _init_html_window(self):
        """
                Create the html widget.

                This widget remains callable through 'self.html'.
                """
        wx.InitAllImageHandlers()
        self.html = OokOokHtmlWindow(parent=self)
        if 'gtk2' in wx.PlatformInfo:
            self.html.SetStandardFonts()

    def _init_navbar(self):
        """
                Create the bar gathering all naviation items.
                """
        self.navbar = wx.BoxSizer(wx.HORIZONTAL)
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        tb_img_size = (16, 16)
        tb.SetToolBitmapSize(tb_img_size)
        img = wx.ArtProvider_GetBitmap(wx.ART_GO_BACK, wx.ART_TOOLBAR, tb_img_size)
        tb.AddSimpleTool(10, img, 'Back', 'Go to previous page.')
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=10)
        img = wx.ArtProvider_GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, tb_img_size)
        tb.AddSimpleTool(20, img, 'Forward', 'Go to next page.')
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=20)
        tb.AddSeparator()
        img = wx.ArtProvider_GetBitmap(wx.ART_GO_HOME, wx.ART_TOOLBAR, tb_img_size)
        tb.AddSimpleTool(50, img, 'Home', 'Go to welcome page.')
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=50)
        dummylongtext = wx.StaticText(self, -1, "Type your query and press 'Enter'Type your query and press 'Enter'")
        dummylongtext.Fit()
        nice_width = dummylongtext.GetBestSize().width
        dummylongtext.Hide()
        self.query_widget = wx.ComboBox(parent=tb, size=wx.Size(nice_width, -1), style=wx.CB_DROPDOWN)
        self.query_widget.Bind(wx.EVT_TEXT_ENTER, self.OnQueryKeyDown)
        self.query_widget.SetValue("Type your query and press 'Enter'")
        self.query_widget.SelectAll()
        tb.AddControl(self.query_widget)
        img = wx.ArtProvider_GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, tb_img_size)
        tb.AddSimpleTool(30, img, 'Clear', 'Clear the search form.')
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=30)
        img = wx.ArtProvider_GetBitmap(wx.ART_FIND, wx.ART_TOOLBAR, tb_img_size)
        tb.AddSimpleTool(35, img, 'Search', 'Answer your query.')
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=35)
        tb.AddSeparator()
        self.printer = html.HtmlEasyPrinting()
        img = wx.ArtProvider_GetBitmap(wx.ART_PRINT, wx.ART_TOOLBAR, tb_img_size)
        tb.AddSimpleTool(40, img, 'Print', 'Print current page.')
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=40)
        tb.Realize()

    def __init__(self, title='Library Desk', parent=None):
        wx.Frame.__init__(self, parent, -1, title, size=wx.Size(800, 600))
        self.CreateStatusBar()
        self._init_html_window()
        self._init_navbar()
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.html, proportion=1, flag=wx.GROW)
        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(True)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        wx.CallAfter(self.query_widget.SetFocus)
        self.SetIcon(wx.ArtProvider().GetIcon(wx.ART_HELP_BOOK))
        self.Show()

    def showPage(self, page_txt):
        """
                Show an html page
                """
        self.html.SetPage(page_txt)

    def addToHistory(self, query_txt):
        """
                Add an element to the search history.
                """
        self.query_widget.Append(query_txt, query_txt.upper())

    def OnClose(self, event):
        """
                When the frame is closed
                """
        dispatcher.send(signal='LibraryDeskClosed', sender=self)
        event.Skip()

    def OnToolClick(self, event):
        """
                When the user clicks on the toolbar, find which button has
                been clicked and act !
                """
        eid = event.GetId()
        if eid == 10:
            if not self.html.HistoryBack():
                wx.MessageBox('No more items in history!')
            else:
                event.Skip()
        elif eid == 20:
            if not self.html.HistoryForward():
                wx.MessageBox('No more items in history!')
            else:
                event.Skip()
        elif eid == 30:
            self.query_widget.SetValue('')
        elif eid == 40:
            self.printer.PrintFile(self.html.GetOpenedPage())
        elif eid == 50:
            LibrarianSingleton.welcome()
        elif eid == 35:
            LibrarianSingleton.search(self.query_widget.GetValue())
        else:
            raise Exception('Event from unknown source!')

    def OnQueryKeyDown(self, event):
        """
                When user clicks on enter while typing in the query widget,
                then launch the search !
                """
        LibrarianSingleton.search(self.query_widget.GetValue())
        event.Skip()


if __name__ == '__main__':
    app = wx.PySimpleApp()

    def createDesk():
        """
                Sample desk factory 
                """
        return LibraryDeskHTML('Ooook!')


    LibrarianSingleton.setDeskFactory(createDesk)
    LibrarianSingleton.welcome()
    app.MainLoop()