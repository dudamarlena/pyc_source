# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ebmlib/clipboard.py
# Compiled at: 2011-03-18 14:09:08
"""
Editra Business Model Library: Clipboard

Clipboard helper class

"""
__author__ = 'Hasan Aljudy'
__cvsid__ = '$Id: clipboard.py 67123 2011-03-04 00:02:35Z CJP $'
__revision__ = '$Revision: 67123 $'
__all__ = [
 'Clipboard', 'ClipboardException']
import wx

class ClipboardException(Exception):
    """Thrown for errors in the Clipboard class"""
    pass


class Clipboard(object):
    """Multiple clipboards as named registers (as per vim)

    " is an alias for system clipboard and is also the default clipboard.

    @note: The only way to access multiple clipboards right now is through
           Normal mode when Vi(m) emulation is enabled.

    """
    NAMES = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
    registers = {}
    current = '"'

    @classmethod
    def ClearAll(cls):
        """Clear all registers"""
        for reg in cls.registers:
            cls.registers[reg] = ''

    @classmethod
    def DeleteAll(cls):
        """Delete all registers"""
        cls.registers.clear()

    @classmethod
    def Switch(cls, reg):
        """Switch to register
        @param reg: char

        """
        if reg in cls.NAMES or reg == '"':
            cls.current = reg
        else:
            raise ClipboardException('Switched to invalid register name')

    @classmethod
    def NextFree(cls):
        """Switch to the next free register. If current register is free, no
        switching happens.

        A free register is one that's either unused or has no content

        @note: This is not used yet.

        """
        if cls.Get() == '':
            return
        for name in cls.NAMES:
            if cls.registers.get(name, '') == '':
                cls.Switch(name)
                break

    @classmethod
    def AllUsed(cls):
        """Get a dictionary mapping all used clipboards (plus the system
        clipboard) to their content.
        @note: This is not used yet.
        @return: dict

        """
        cmd_map = {'"': cls.SystemGet()}
        for name in cls.NAMES:
            if cls.registers.get(name, ''):
                cmd_map[name] = cls.registers[name]

        return cmd_map

    @classmethod
    def Get(cls):
        """Get the content of the current register. Used for pasting"""
        if cls.current == '"':
            return cls.SystemGet()
        else:
            return cls.registers.get(cls.current, '')

    @classmethod
    def Set(cls, text):
        """Set the content of the current register
        @param text: string

        """
        if cls.current == '"':
            return cls.SystemSet(text)
        cls.registers[cls.current] = text

    @classmethod
    def SystemGet(cls):
        """Get text from the system clipboard
        @return: string

        """
        text = None
        if wx.TheClipboard.Open():
            if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                text = wx.TextDataObject()
                wx.TheClipboard.GetData(text)
            wx.TheClipboard.Close()
        if text is not None:
            return text.GetText()
        else:
            return ''
            return

    @classmethod
    def SystemSet(cls, text):
        """Set text into the system clipboard
        @param text: string
        @return: bool

        """
        ok = False
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(text))
            wx.TheClipboard.Close()
            ok = True
        return ok