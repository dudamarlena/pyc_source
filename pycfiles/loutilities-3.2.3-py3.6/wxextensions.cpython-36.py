# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\wxextensions.py
# Compiled at: 2019-11-27 15:15:01
# Size of source mod 2**32: 13429 bytes
"""
wxextensions - extensions for wxPython widgets
========================================================
"""
import optparse, wx

class InvalidParameter(Exception):
    pass


class AutoTextCtrl(wx.TextCtrl):
    __doc__ = '\n    TextCtrl enhanced by associated list containing suggestions while typing\n\n    :param *args: :class:`wx.TextCtrl` parameters\n    :param **kwargs: :class:`wx.TextCtrl` keyword parameters\n    :param items: list of initial items suggested while typing, default []\n    :param delcallback: function to call when item deleted from items, default None - takes one parameter, text from deleted item\n    '

    def __init__(self, *args, **kwargs):
        """
        remember items, instantiate TextCtrl using supplied parameters
        """
        items = kwargs.pop('items', [])
        if not isinstance(items, list):
            raise InvalidParameter('items must be list')
        self.setitems(items)
        self.setdelcallback(kwargs.pop('delcallback', None))
        self.typedText = ''
        self.itemndx = 0
        (wx.TextCtrl.__init__)(self, *args, **kwargs)
        self.Bind(wx.EVT_CHAR, self._OnKey)

    def setitems(self, items):
        """
        update the items used for autocompletion

        :param items: list of items suggested while typing
        """
        self.items = items
        if '' not in self.items:
            self.items.append('')
        self.items.sort(cmp=(lambda x, y: cmp(x.lower(), y.lower())))

    def setdelcallback(self, delcallback=None):
        """
        update the delcallback function, which is called when an item is deleted from items (list of suggested choices)

        :param delcallback: delcallback(item) is called when an item is deleted from items list.  None to disable
        """
        self.delcallback = delcallback

    def getitems(self):
        """
        return items used for autocompletion

        :rtype: list of items suggested while typing
        """
        return self.items

    def additem(self, item):
        """
        add an item to the list used for autocompletion

        :param item: item to add to list of items suggested while typing
        """
        if item not in self.items:
            self.items.append(item)
            self.setitems(self.items)

    def _FindPrefix(self, prefix):
        """
        find prefix as first substring of any item in self.items, ignoring case
        
        :param prefix: substring to look for
        """
        if prefix:
            prefix = prefix.lower()
            length = len(prefix)
            for i in range(len(self.items)):
                item = self.items[i]
                text = item.lower()
                if text[:length] == prefix:
                    return i

        return -1

    def _OnKey(self, evt):
        key = evt.GetKeyCode()
        if key >= 32:
            if key < 127:
                self.typedText = self.typedText + chr(key)
                self.itemndx = self._FindPrefix(self.typedText)
                self._SetSelection(self.itemndx)
            else:
                if key == wx.WXK_BACK:
                    self.typedText = self.typedText[:-1]
                    self.typedText or self._SetSelection(0)
                else:
                    self.itemndx = self._FindPrefix(self.typedText)
                    self._SetSelection(self.itemndx)
        else:
            if key == wx.WXK_DOWN:
                if self.itemndx != -1:
                    self.typedText = ''
                    self.itemndx += 1
                    if self.itemndx >= len(self.items):
                        self.itemndx = 0
                    self._SetSelection(self.itemndx)
            else:
                if key == wx.WXK_UP:
                    if self.itemndx != -1:
                        self.typedText = ''
                        self.itemndx -= 1
                        if self.itemndx == -1:
                            self.itemndx = len(self.items) - 1
                        self._SetSelection(self.itemndx)
                else:
                    if key == wx.WXK_DELETE:
                        self.itemndx = -1
                        self._SetSelection(self.itemndx)
                    else:
                        if key == wx.WXK_CONTROL_X:
                            if self.itemndx > 0:
                                item = self.items.pop(self.itemndx)
                                self.itemndx = 0
                                self._SetSelection(self.itemndx)
                                do = wx.TextDataObject()
                                do.SetText(item)
                                wx.TheClipboard.SetData(do)
                                if self.delcallback:
                                    self.delcallback(item)
                        else:
                            if key == wx.WXK_CONTROL_V:
                                do = wx.TextDataObject()
                                if wx.TheClipboard.GetData(do):
                                    self.typedText += do.GetText()
                                self.itemndx = self._FindPrefix(self.typedText)
                                self._SetSelection(self.itemndx)
                            else:
                                self.typedText = ''
                                evt.Skip()

    def _SetSelection(self, itemndx):
        """
        set the value of the TextCtrl to the found item,
        select the portion of the item which was not yet typed
        
        :param itemndx: index into self.items
        """
        if itemndx == -1:
            self.SetValue(self.typedText)
            self.SetInsertionPoint(len(self.typedText))
        else:
            self.SetValue(self.items[itemndx])
            self.SetInsertionPoint(len(self.typedText))
            self.SetSelection(len(self.typedText), len(self.items[itemndx]))


class _TestWindow(wx.Frame):
    __doc__ = '\n    Test Window for widgets in this package\n\n    :param parent: parent object for this form\n    '
    BTN_OK = wx.NewId()
    BTN_CNCL = wx.NewId()

    def __init__(self, parent):
        self.debug = False
        self.formname = 'test window'
        wx.Frame.__init__(self, parent, wx.ID_ANY, self.formname)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        """
        Initialize the form
        """
        self.panel = wx.Panel(self)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText((self.panel), label='Enter Text')
        st1.SetFont(font)
        hbox1.Add(st1, proportion=1, flag=(wx.RIGHT), border=8)
        self.tc = AutoTextCtrl((self.panel), style=(wx.TE_PROCESS_ENTER), items=[
         '124 North Market St, Frederick, MD, USA',
         '748 SW Bay Blvd, Newport, OR, USA',
         '30 Germania St, Boston, MA, USA'])
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        hbox1.Add((self.tc), proportion=5, border=8)
        self.vbox.Add(hbox1, flag=(wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP), border=10)
        self.vbox.Add((-1, 10))
        self.panel.SetSizerAndFit(self.vbox)
        self.Fit()

    def onEnter(self, evt):
        """
        Search for address, then display rest of frame
        """
        print('text entered: {0}\n'.format(self.tc.GetValue()))
        self.tc.SetValue('')

    def onClose(self, evt):
        """
        Just close the window without updating the station
        """
        self.tc.Destroy()
        self.Destroy()


class _MyApp(wx.App):

    def __init__(self):
        """
        return MyApp object
        """
        wx.App.__init__(self, False)
        self.frame = _TestWindow(None)


def test():
    usage = 'usage: %prog [options]\n'
    parser = optparse.OptionParser(usage=usage)
    options, args = parser.parse_args()
    app = _MyApp()
    app.MainLoop()


if __name__ == '__main__':
    test()