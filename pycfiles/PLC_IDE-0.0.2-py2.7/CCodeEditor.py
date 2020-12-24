# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\IDE\CCodeEditor.py
# Compiled at: 2020-01-15 02:05:59
import wx, wx.xrc, wx.stc as stc
from CLogText import LogText

class Panel_Code(wx.Panel):

    def __init__(self, parent, hanndel):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 800), style=wx.TAB_TRAVERSAL)
        self.parent = hanndel
        bz = wx.BoxSizer(wx.VERTICAL)
        self.m_toolBar = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.m_tool_save = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_tool_refresh = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_GO_TO_PARENT), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_toolBar.AddSeparator()
        self.m_tool_add = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_tool_delete = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_toolBar.AddSeparator()
        self.m_tool_up = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_GO_UP), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_tool_dn = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_toolBar.Realize()
        bz.Add(self.m_toolBar, 0, wx.EXPAND, 5)
        self.list = CustListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_HRULES | wx.LC_VRULES)
        bz.Add(self.list, 1, wx.ALL | wx.EXPAND, 0)
        self.stc = CustScriptSTC(self, wx.ID_ANY)
        bz.Add(self.stc, 5, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(bz)
        self.Layout()
        self.Bind(wx.EVT_TOOL, self.OnSave, id=self.m_tool_save.GetId())
        self.Bind(wx.EVT_TOOL, self.OnAdd, id=self.m_tool_add.GetId())
        self.Bind(wx.EVT_TOOL, self.OnDelete, id=self.m_tool_delete.GetId())
        self.Bind(wx.EVT_TOOL, self.OnUp, id=self.m_tool_up.GetId())
        self.Bind(wx.EVT_TOOL, self.OnDn, id=self.m_tool_dn.GetId())
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        return

    def __del__(self):
        pass

    def OnSave(self, event):
        self.parent.SavePage(self.savedata())
        event.Skip()

    def OnAdd(self, event):
        index = self.list.InsertItem(self.list.GetItemCount(), '')
        self.list.SetItemData(index, index)
        event.Skip()

    def OnDelete(self, event):
        print self.currentItem
        self.list.DeleteItem(self.currentItem)
        event.Skip()

    def OnUp(self, event):
        event.Skip()

    def OnDn(self, event):
        event.Skip()

    def OnItemSelected(self, event):
        self.currentItem = event.Index
        print self.currentItem
        event.Skip()

    def savedata(self):
        data = {}
        data['Declare'] = []
        _lenth = self.list.GetItemCount()
        _cols = self.list.GetColumnCount()
        for i in xrange(_lenth):
            lt = []
            for j in xrange(_cols):
                v = self.list.GetItem(i, j).GetText()
                lt.append(v)

            data['Declare'].append(lt)

        data['Code'] = self.stc.GetValue()
        return data

    def renderdata(self, data):
        if data.has_key('Declare') == False:
            return
        for i in xrange(len(data['Declare'])):
            index = self.list.InsertItem(self.list.GetItemCount(), data['Declare'][i][0])
            for j in range(1, len(data['Declare'][i])):
                self.list.SetItem(index, j, data['Declare'][i][j])

        self.stc.SetValue(data['Code'])


if wx.Platform == '__WXMSW__':
    faces = {'times': 'Times New Roman', 'mono': 'Courier New', 'helv': 'Arial', 
       'other': 'Comic Sans MS', 
       'size': 10, 
       'size2': 8}
elif wx.Platform == '__WXMAC__':
    faces = {'times': 'Times New Roman', 'mono': 'Monaco', 'helv': 'Arial', 
       'other': 'Comic Sans MS', 
       'size': 12, 
       'size2': 10}
else:
    faces = {'times': 'Times', 'mono': 'Courier', 'helv': 'Helvetica', 
       'other': 'new century schoolbook', 
       'size': 12, 
       'size2': 10}
keyword = [
 'if', 'else', 'do', 'while', 'for']

class CustScriptSTC(stc.StyledTextCtrl):
    fold_symbols = 2

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)
        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.SetLexer(stc.STC_LEX_CPP)
        self.SetKeyWords(0, (' ').join(keyword))
        self.SetProperty('fold', '1')
        self.SetProperty('tab.timmy.whinge.level', '1')
        self.SetMargins(0, 0)
        self.SetViewWhiteSpace(False)
        self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        if self.fold_symbols == 0:
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_ARROWDOWN, 'black', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_ARROW, 'black', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, 'black', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, 'black', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, 'white', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, 'white', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, 'white', 'black')
        elif self.fold_symbols == 1:
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_MINUS, 'white', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_PLUS, 'white', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, 'white', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, 'white', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, 'white', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, 'white', 'black')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, 'white', 'black')
        elif self.fold_symbols == 2:
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_CIRCLEMINUS, 'white', '#404040')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_CIRCLEPLUS, 'white', '#404040')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, 'white', '#404040')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNERCURVE, 'white', '#404040')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_CIRCLEPLUSCONNECTED, 'white', '#404040')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, 'white', '#404040')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE, 'white', '#404040')
        elif self.fold_symbols == 3:
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, 'white', '#808080')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, 'white', '#808080')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, 'white', '#808080')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, 'white', '#808080')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, 'white', '#808080')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, 'white', '#808080')
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, 'white', '#808080')
        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'face:%(helv)s,size:%(size)d' % faces)
        self.StyleClearAll()
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'face:%(helv)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, 'back:#C0C0C0,face:%(helv)s,size:%(size2)d' % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, 'face:%(other)s' % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, 'fore:#FFFFFF,back:#0000FF,bold')
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, 'fore:#000000,back:#FF0000,bold')
        self.StyleSetSpec(stc.STC_P_DEFAULT, 'fore:#000000,face:%(helv)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, 'fore:#007F00,face:%(other)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_NUMBER, 'fore:#007F7F,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_STRING, 'fore:#7F007F,face:%(helv)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_CHARACTER, 'fore:#7F007F,face:%(helv)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_WORD, 'fore:#0000ff,bold,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_TRIPLE, 'fore:#7F0000,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, 'fore:#7F0000,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_CLASSNAME, 'fore:#0000FF,bold,underline,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_DEFNAME, 'fore:#007F7F,bold,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_OPERATOR, 'bold,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, 'fore:#000000,face:%(helv)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, 'fore:#7F7F7F,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_STRINGEOL, 'fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d' % faces)
        self.SetCaretForeground('BLUE')
        self.RegisterImage(2, wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16, 16)))
        self.RegisterImage(3, wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16, 16)))

    def OnKeyPressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()
            if event.ShiftDown():
                self.CallTipSetBackground('yellow')
                self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\nshow some suff, maybe parameters..\n\nfubar(param1, param2)')
            else:
                kw = keyword.kwlist[:]
                kw.append('zzzzzz?2')
                kw.append('aaaaa?2')
                kw.append('__init__?3')
                kw.append('zzaaaaa?2')
                kw.append('zzbaaaa?2')
                kw.append('this_is_a_longer_value')
                kw.sort()
                self.AutoCompSetIgnoreCase(False)
                for i in range(len(kw)):
                    if kw[i] in keyword.kwlist:
                        kw[i] = kw[i] + '?1'

                self.AutoCompShow(0, (' ').join(kw))
        else:
            event.Skip()

    def OnUpdateUI(self, evt):
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)
        if charBefore and chr(charBefore) in '[]{}()' and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
            if charAfter and chr(charAfter) in '[]{}()' and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos
        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)
        if braceAtCaret != -1 and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
        return

    def OnMarginClick(self, evt):
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and level & stc.STC_FOLDLEVELNUMBERMASK == stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)
                    if lastChild > lineNum:
                        self.HideLines(lineNum + 1, lastChild)
            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            elif doExpand:
                self.ShowLines(line, line)
            if level == -1:
                level = self.GetFoldLevel(line)
            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.Expand(line, doExpand, force, visLevels - 1)
                elif doExpand and self.GetFoldExpanded(line):
                    line = self.Expand(line, True, force, visLevels - 1)
                else:
                    line = self.Expand(line, False, force, visLevels - 1)
            else:
                line = line + 1

        return line


import sys, wx, wx.lib.mixins.listctrl as listmix

class CustListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.Populate()
        listmix.TextEditMixin.__init__(self)

    def Populate(self):
        self.InsertColumn(0, 'type')
        self.InsertColumn(1, 'name')
        self.InsertColumn(2, 'data type')
        self.InsertColumn(3, 'array lenth', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(4, 'default value')
        self.InsertColumn(5, 'cmmt')
        self.currentItem = 0