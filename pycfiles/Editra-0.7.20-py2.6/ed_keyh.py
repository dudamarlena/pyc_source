# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_keyh.py
# Compiled at: 2012-03-17 12:57:55
"""
KeyHandler interface for implementing extended key action handling in Editra's
main text editting buffer.

@summary: Custom keyhandler interface

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_keyh.py 70747 2012-02-29 01:33:35Z CJP $'
__revision__ = '$Revision: 70747 $'
import re, wx, wx.stc, ed_event, ed_glob, ed_basestc, ed_stc, string, ed_vim

class KeyHandler(object):
    """KeyHandler base class"""

    def __init__(self, stc):
        super(KeyHandler, self).__init__()
        self.stc = stc
        self._blockmode = False

    STC = property(lambda self: self.stc)
    BlockMode = property(lambda self: self._blockmode, lambda self, m: setattr(self, '_blockmode', m))

    def ClearMode(self):
        """Clear any key input modes to normal input mode"""
        evt = ed_event.StatusEvent(ed_event.edEVT_STATUS, self.stc.Id, '', ed_glob.SB_BUFF)
        wx.PostEvent(self.stc.TopLevelParent, evt)

    def GetHandlerName(self):
        """Get the name of this handler
        @return: string

        """
        return 'NULL'

    def PreProcessKey(self, key_code, ctrldown=False, cmddown=False, shiftdown=False, altdown=False):
        """Pre process any keys before they get to the char handler
        @param key_code: Raw keycode
        @keyword ctrldown: Is the control key down
        @keyword cmddown: Is the Command key down (Mac osx)
        @keyword shiftdown: Is the Shift key down
        @keyword altdown: Is the Alt key down
        @return: bool

        """
        return False

    def ProcessKey(self, key_code, ctrldown=False, cmddown=False, shiftdown=False, altdown=False):
        """Process the key and return True if it was processed and
        false if it was not. The key is recieved at EVT_CHAR.
        @param key_code: Raw keycode
        @keyword ctrldown: Is the control key down
        @keyword cmddown: Is the Command key down (Mac osx)
        @keyword shiftdown: Is the Shift key down
        @keyword altdown: Is the Alt key down
        @return: bool

        """
        return False


class ViKeyHandler(KeyHandler):
    """Defines a key handler for Vi emulation
    @summary: Handles key presses according to Vi emulation.

    """
    (NORMAL, INSERT, VISUAL) = range(3)

    def __init__(self, stc, use_normal_default=False):
        super(ViKeyHandler, self).__init__(stc)
        self.mode = 0
        self.last = ''
        self.last_find = ''
        self.commander = ed_vim.EditraCommander(self)
        self.buffer = ''
        if use_normal_default:
            self.NormalMode()
        else:
            self.InsertMode()

    def ClearMode(self):
        """Clear the mode back to default input mode"""
        self.STC.SetLineCaret()
        self.BlockMode = False
        self.last = self.cmdcache = ''
        super(ViKeyHandler, self).ClearMode()

    def GetHandlerName(self):
        """Get the name of this handler"""
        return 'VI'

    def _SetMode(self, newmode, msg):
        """Set the keyhandlers mode
        @param newmode: New mode name to change to

        """
        self.buffer = ''
        self.mode = newmode
        evt = ed_event.StatusEvent(ed_event.edEVT_STATUS, self.stc.GetId(), msg, ed_glob.SB_BUFF)
        wx.PostEvent(self.stc.GetTopLevelParent(), evt)

    def InsertMode(self):
        """Change to insert mode"""
        self.stc.SetLineCaret()
        self.stc.SetOvertype(False)
        self.BlockMode = False
        self._SetMode(ViKeyHandler.INSERT, 'INSERT')

    def ReplaceMode(self):
        """Change to replace mode
        This really just insert mode with overtype set to true

        """
        self.stc.SetLineCaret()
        self.stc.SetOvertype(True)
        self._SetMode(ViKeyHandler.INSERT, 'REPLACE')

    def NormalMode(self):
        """Change to normal (command) mode"""
        if self.IsInsertMode():
            self.commander.SetLastInsertedText(self.buffer)
        self.stc.SetOvertype(False)
        self.stc.SetBlockCaret()
        self.BlockMode = True
        self.commander.Deselect()
        self.commander.InsertRepetition()
        self._SetMode(ViKeyHandler.NORMAL, 'NORMAL')

    def VisualMode(self):
        """Change to visual (selection) mode"""
        self.stc.SetBlockCaret()
        self.BlockMode = True
        self.stc.SetOvertype(False)
        self._SetMode(ViKeyHandler.VISUAL, 'VISUAL')
        self.commander.StartSelection()

    def IsInsertMode(self):
        """Test if we are in insert mode"""
        return self.mode == ViKeyHandler.INSERT

    def IsNormalMode(self):
        """Test if we are in normal mode"""
        return self.mode == ViKeyHandler.NORMAL

    def IsVisualMode(self):
        """Test if we are in visual mode"""
        return self.mode == ViKeyHandler.VISUAL

    def PreProcessKey(self, key_code, ctrldown=False, cmddown=False, shiftdown=False, altdown=False):
        """Pre process any keys before they get to the char handler
        @param key_code: Raw keycode
        @keyword ctrldown: Is the control key down
        @keyword cmddown: Is the Command key down (Mac osx)
        @keyword shiftdown: Is the Shift key down
        @keyword altdown: Is the Alt key down
        @return: bool

        """
        if not shiftdown and key_code == wx.WXK_ESCAPE:
            self.NormalMode()
            return False
        else:
            if (ctrldown or cmddown) and key_code == ord('['):
                self.NormalMode()
                return True
            if key_code in (wx.WXK_RETURN, wx.WXK_BACK,
             wx.WXK_RIGHT, wx.WXK_LEFT) and not self.IsInsertMode():
                self.ProcessKey(key_code)
                return True
            return False

    def ProcessKey(self, key_code, ctrldown=False, cmddown=False, shiftdown=False, altdown=False):
        """Processes keys and decided whether to interpret them as vim commands
        or normal insert text

        @param key_code: Raw key code
        @keyword cmddown: Command/Ctrl key is down
        @keyword shiftdown: Shift Key is down
        @keyword altdown : Alt key is down

        """
        if ctrldown or cmddown or altdown:
            return False
        else:
            f_cmd = self.IsNormalMode() or self.IsVisualMode()
            self._ProcessKey(key_code)
            if self.IsNormalMode():
                if self.stc.GetTopLevelParent():
                    evt = ed_event.StatusEvent(ed_event.edEVT_STATUS, self.stc.GetId(), 'NORMAL %s' % self.buffer, ed_glob.SB_BUFF)
                    wx.PostEvent(self.stc.GetTopLevelParent(), evt)
            if f_cmd:
                return True
            return False

    def _ProcessKey(self, key_code):
        """The real processing of keys"""
        char = unichr(key_code)
        if self.IsNormalMode() or self.IsVisualMode():
            self.buffer += char
            if ed_vim.Parse(self.buffer, self.commander):
                self.buffer = ''
            if self.IsVisualMode():
                self.commander.ExtendSelection()
        elif self.IsInsertMode():
            self.buffer += char

    def InsertText(self, pos, text):
        """Insert text and store it in the buffer if we're in insert mode
        i.e. as if it was typed in

        """
        self.stc.InsertText(pos, text)
        if self.IsInsertMode():
            self.buffer += text