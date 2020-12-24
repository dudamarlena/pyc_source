# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Pyreb\Controls\RegexCtrl.py
# Compiled at: 2006-12-10 11:22:19
import wx, re, pickle, os.path, pkg_resources
from exceptions import RuntimeError, IOError
from string import replace
import wx.stc as stc, wx.xrc as xrc

class PyrebRegexCtrl(stc.StyledTextCtrl):
    """
    PyrebRegexCtrl is a subclass of wxTextCtrl.
    The text entered in the control is treated as a Python Regex.
    By using the Text method the user can set an arbitrary string
    to which the Regex is applied. The resulting match object can
    be retrieved with MatchObject() method.
    A list of pre-made Regex can be stored in PreMade.list file,
    distributed with Pyreb, and/or in a .pyrebrc in home directory.
    User home directory is obtained from wx.StandardPaths GetConfigDir().
    Upon a right click the list of pre-made Regexes is popped up.
    """
    __module__ = __name__

    def __init__(self, parent, id, pos, size, style, name):
        stc.StyledTextCtrl.__init__(self, parent, id, pos, size, style, name)
        self.SetViewWhiteSpace(True)
        self.SetMarginWidth(1, 0)
        self.StyleClearAll()
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, 'fore:#0000FF,back:#A0FFA0,bold')
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, 'fore:#000000,back:#FF0000,bold')
        self.__text = ''
        self.__regex = ''
        self.__flags = []
        self.Bind(stc.EVT_STC_CHARADDED, self.OnCharAdded)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCharAdded(self, event):
        """
        Check for matching braces and highlight them
        """
        event.Skip(True)
        caretPos = self.GetCurrentPos() - 1
        if caretPos < 0:
            return
        char = ''
        try:
            char = chr(self.GetCharAt(caretPos))
        except:
            return

        if char not in '(){}[]<>':
            return
        braceOpposite = self.BraceMatch(caretPos)
        if braceOpposite == -1:
            self.BraceBadLight(caretPos)
        else:
            self.BraceHighlight(caretPos, braceOpposite)

    def OnRightClick(self, event):
        """
        Load a map of commonly used regex and display them
        as a popup menu. The stock map is distributed with Pyreb
        in file PreMade.list, and a custom one is loaded from
        $HOME/.pyrebrc
        """
        AppObj = wx.GetApp()
        if not hasattr(self, '__PMMenu'):
            PM = {}
            try:
                ResourceAsString = AppObj.GetResourceAsString('PreMade.list')
                assert ResourceAsString != '', 'Cannot access PreMade.list resource'
                ResourceAsString = ResourceAsString.replace('\r', '')
                PM = pickle.loads(ResourceAsString)
            except IOError, msg:
                print msg
            except pickle.PickleError, msg:
                print msg
            except:
                pass
            else:
                try:
                    sp = wx.StandardPaths.Get()
                    fd = file(os.path.join(sp.GetConfigDir(), '.pyrebrc'), 'r')
                    PM2 = pickle.load(fd)
                    for K2 in PM2.keys():
                        PM[K2] = PM2[K2]

                except:
                    pass
                else:
                    if len(PM) == 0:
                        return
                    self.__PMMenu = wx.Menu('Pre-made regexes', wx.MENU_TEAROFF)
                    for K in PM.keys():
                        NewID = wx.NewId()
                        self.__PMMenu.Append(NewID, K, PM[K])
                        self.Bind(wx.EVT_MENU, self.OnPreMadeRegex, id=NewID)

        self.PopupMenu(self.__PMMenu, event.GetPosition())
        event.Skip(False)

    def OnPreMadeRegex(self, event):
        MIID = event.GetId()
        menu = event.GetEventObject()
        MI = menu.FindItemById(MIID)
        self.AppendText(MI.GetHelp())

    def Text(self, SetText=None, Flags=[]):
        """
        Set the text to which the Regex is applied.
        If SetText argument is not used the method just returns the actual text.
        @param SetText: Text to be setted
        @param Flags: Optional list of flags to be used while compiling the
            Regex. Please see Python re module documentation for more details.
        @type Flags: List of strings
        @return: The actual text
        """
        if SetText != None:
            self.__flags = Flags
            self.__text = SetText
            self.ApplyRegex()
        return self.__text

    def GetValue(self):
        """Implemented because it's the standard method name in wxWidgets."""
        return self.GetText()

    def SetValue(self, value):
        """Implemented because it's the standard method name in wxWidgets."""
        self.SetText(value)

    def MatchObject(self):
        """
        Return the regex MatchObject
        """
        return self.__results

    def ApplyRegex(self):
        """
        Compile the actual regex and apply to the actual text.
        """
        self.__regex = replace(self.GetText(), '\\', '\\\\')
        self.__regex = self.__regex.replace('\n', '\\n')
        self.__results = None
        if self.__regex == '' or self.__text == '':
            raise RuntimeError('No regular expression or no text to search')
        statement = "reobj = re.compile ('%s' " % self.__regex
        if len(self.__flags) != 0:
            refstring = ''
            for f in self.__flags:
                refstring += '%s|' % f

            refstring = refstring[0:-1]
            statement += ', '
            statement += refstring
        statement += ')'
        try:
            exec statement
        except re.error, msg:
            raise RuntimeError(str(msg))

        self.__results = reobj.search(self.__text)
        if not self.__results:
            raise RuntimeError('Cannot find expression')
        return

    def OnCloseWindow(self, event):
        self.Destroy()


class PyrebRegexCtrlXmlHandler(xrc.XmlResourceHandler):
    __module__ = __name__

    def __init__(self):
        xrc.XmlResourceHandler.__init__(self)
        self.AddWindowStyles()

    def CanHandle(self, node):
        return self.IsOfClass(node, 'PyrebRegexCtrl')

    def DoCreateResource(self):
        widget = self.GetInstance()
        assert widget is None
        widget = PyrebRegexCtrl(self.GetParentAsWindow(), self.GetID(), self.GetPosition(), self.GetSize(), self.GetStyle(), self.GetName())
        self.SetupWindow(widget)
        self.CreateChildren(widget)
        return widget