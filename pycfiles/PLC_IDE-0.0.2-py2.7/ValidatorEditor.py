# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\lib\ValidatorEditor.py
# Compiled at: 2018-09-18 10:24:52
import string, wx
ALPHA_ONLY = 1
DIGIT_ONLY = 2

class NumValidator(wx.Validator):

    def __init__(self, flag=None, pyVar=None):
        wx.Validator.__init__(self)
        self.flag = DIGIT_ONLY
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return NumValidator(self.flag)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        if self.flag == ALPHA_ONLY:
            for x in val:
                if x not in string.ascii_letters:
                    return False

        elif self.flag == DIGIT_ONLY:
            for x in val:
                if x not in string.digits:
                    if x == '.':
                        continue
                    else:
                        return False

        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if self.flag == ALPHA_ONLY and chr(key) in string.ascii_letters:
            event.Skip()
            return
        if self.flag == DIGIT_ONLY and (chr(key) in string.digits or chr(key) == '.'):
            if chr(key) == '.':
                tc = self.GetWindow()
                ss = tc.GetValue()
                ss += '.'
                if self.is_number(ss):
                    event.Skip()
            else:
                event.Skip()
            return
        if not wx.Validator.IsSilent():
            wx.Bell()

    def TransferToWindow(self):
        """ Transfer data from validator to window.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True

    def TransferFromWindow(self):
        """ Transfer data from window to validator.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False


class AscValidator(wx.Validator):

    def __init__(self, flag=None, pyVar=None):
        wx.Validator.__init__(self)
        self.flag = ALPHA_ONLY
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return AscValidator(self.flag)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        if self.flag == ALPHA_ONLY:
            for x in val:
                if x not in string.ascii_letters:
                    return False

        elif self.flag == DIGIT_ONLY:
            for x in val:
                if x not in string.digits:
                    return False

        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if self.flag == ALPHA_ONLY and chr(key) in string.ascii_letters:
            event.Skip()
            return
        if self.flag == DIGIT_ONLY and chr(key) in string.digits:
            event.Skip()
            return
        if not wx.Validator.IsSilent():
            wx.Bell()

    def TransferToWindow(self):
        """ Transfer data from validator to window.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True

    def TransferFromWindow(self):
        """ Transfer data from window to validator.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True