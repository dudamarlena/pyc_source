# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dialogs/panel_schematic.py
# Compiled at: 2018-07-16 12:07:24
import wx, wx.xrc, wx.dataview

class PanelSchematic(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1120, 759), style=wx.TAB_TRAVERSAL)
        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        self.splitter_part = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D | wx.SP_LIVE_UPDATE)
        self.splitter_part.Bind(wx.EVT_IDLE, self.splitter_partOnIdle)
        self.m_panel1 = wx.Panel(self.splitter_part, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer4 = wx.BoxSizer(wx.VERTICAL)
        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)
        self.toolbar = wx.ToolBar(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.tool_export_bom = self.toolbar.AddLabelTool(wx.ID_ANY, 'export', wx.Bitmap('resources/export.gif', wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, 'Export bom from schematic', wx.EmptyString, None)
        self.toolbar.AddSeparator()
        self.tool_show_all = self.toolbar.AddLabelTool(wx.ID_ANY, 'Show all parts', wx.Bitmap('resources/hide.png', wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_CHECK, 'Export BOM', wx.EmptyString, None)
        self.toolbar.Realize()
        bSizer8.Add(self.toolbar, 1, wx.EXPAND, 5)
        self.m_toolBar2 = wx.ToolBar(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.tool_refresh_schematic = self.m_toolBar2.AddLabelTool(wx.ID_ANY, 'Refresh', wx.Bitmap('resources/refresh.png', wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, 'Refresh schematic file', wx.EmptyString, None)
        self.m_toolBar2.Realize()
        bSizer8.Add(self.m_toolBar2, 0, wx.EXPAND, 5)
        bSizer4.Add(bSizer8, 0, wx.EXPAND, 5)
        bSizer42 = wx.BoxSizer(wx.HORIZONTAL)
        self.tree_parts = wx.dataview.DataViewCtrl(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE)
        bSizer42.Add(self.tree_parts, 1, wx.ALL | wx.EXPAND, 5)
        bSizer4.Add(bSizer42, 1, wx.EXPAND, 5)
        self.m_panel1.SetSizer(bSizer4)
        self.m_panel1.Layout()
        bSizer4.Fit(self.m_panel1)
        self.menu_parts = wx.Menu()
        self.menu_parts_link = wx.MenuItem(self.menu_parts, wx.ID_ANY, 'Set kicad part', 'Link schematic part to a kipartman part', wx.ITEM_NORMAL)
        self.menu_parts.Append(self.menu_parts_link)
        self.menu_parts_unlink = wx.MenuItem(self.menu_parts, wx.ID_ANY, 'Remove kicad part', 'Unlink kipartman part', wx.ITEM_NORMAL)
        self.menu_parts.Append(self.menu_parts_unlink)
        self.menu_parts.AppendSeparator()
        self.menu_parts_hide = wx.MenuItem(self.menu_parts, wx.ID_ANY, 'Hide', 'Hide part', wx.ITEM_NORMAL)
        self.menu_parts.Append(self.menu_parts_hide)
        self.menu_parts_show = wx.MenuItem(self.menu_parts, wx.ID_ANY, 'Show', 'Show part', wx.ITEM_NORMAL)
        self.menu_parts.Append(self.menu_parts_show)
        self.m_panel1.Bind(wx.EVT_RIGHT_DOWN, self.m_panel1OnContextMenu)
        self.panel_preview = wx.Panel(self.splitter_part, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.splitter_part.SplitHorizontally(self.m_panel1, self.panel_preview, 453)
        bSizer3.Add(self.splitter_part, 1, wx.EXPAND, 5)
        self.SetSizer(bSizer3)
        self.Layout()
        self.Bind(wx.EVT_TOOL, self.onToolExportBomClicked, id=self.tool_export_bom.GetId())
        self.Bind(wx.EVT_TOOL, self.onToolShowAllClicked, id=self.tool_show_all.GetId())
        self.Bind(wx.EVT_TOOL, self.onToolRefreshSchematic, id=self.tool_refresh_schematic.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuPartsLinkSelection, id=self.menu_parts_link.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuPartsUnlinkSelection, id=self.menu_parts_unlink.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuPartsHideSelection, id=self.menu_parts_hide.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuPartsShowSelection, id=self.menu_parts_show.GetId())
        return

    def __del__(self):
        pass

    def onToolExportBomClicked(self, event):
        event.Skip()

    def onToolShowAllClicked(self, event):
        event.Skip()

    def onToolRefreshSchematic(self, event):
        event.Skip()

    def onMenuPartsLinkSelection(self, event):
        event.Skip()

    def onMenuPartsUnlinkSelection(self, event):
        event.Skip()

    def onMenuPartsHideSelection(self, event):
        event.Skip()

    def onMenuPartsShowSelection(self, event):
        event.Skip()

    def splitter_partOnIdle(self, event):
        self.splitter_part.SetSashPosition(453)
        self.splitter_part.Unbind(wx.EVT_IDLE)

    def m_panel1OnContextMenu(self, event):
        self.m_panel1.PopupMenu(self.menu_parts, event.GetPosition())