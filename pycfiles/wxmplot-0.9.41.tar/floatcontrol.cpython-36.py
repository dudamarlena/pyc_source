# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Newville/Codes/wxmplot/examples/floatcontrol.py
# Compiled at: 2018-10-13 19:56:45
# Size of source mod 2**32: 7415 bytes
"""
This is a collection of general purpose utility functions and classes,
especially useful for wx functionality
"""
import sys, wx, wx.lib.masked as masked, numpy

def set_float(val):
    """ utility to set a floating value,
    useful for converting from strings """
    out = None
    if val not in (None, ''):
        try:
            out = float(val)
        except ValueError:
            return
        else:
            if numpy.isnan(out):
                out = default
    return out


class Closure:
    __doc__ = "A very simple callback class to emulate a closure (reference to\n    a function with arguments) in python.\n\n    This class holds a user-defined function to be executed when the\n    class is invoked as a function.  This is useful in many situations,\n    especially for 'callbacks' where lambda's are quite enough.\n    Many Tkinter 'actions' can use such callbacks.\n\n    >>>def my_action(x=None):\n    ...    print('my action: x = ', x)\n    >>>c = Closure(my_action,x=1)\n    ..... sometime later ...\n    >>>c()\n     my action: x = 1\n    >>>c(x=2)\n     my action: x = 2\n\n    based on Command class from J. Grayson's Tkinter book.\n    "

    def __init__(self, func=None, *args, **kws):
        self.func = func
        self.kws = kws
        self.args = args

    def __call__(self, *args, **kws):
        self.kws.update(kws)
        if hasattr(self.func, '__call__'):
            self.args = args
            return (self.func)(*self.args, **self.kws)


class FloatCtrl(wx.TextCtrl):
    __doc__ = ' Numerical Float Control::\n    a wx.TextCtrl that allows only numerical input, can take a precision argument\n    and optional upper / lower bounds\n    Options:\n\n    '

    def __init__(self, parent, value='', minval=None, maxval=None, precision=3, bell_on_invalid=True, action=None, action_kw=None, **kws):
        self._FloatCtrl__digits = '0123456789.-'
        self._FloatCtrl__prec = precision
        if precision is None:
            self._FloatCtrl__prec = 0
        self.format = '%%.%if' % self._FloatCtrl__prec
        self.is_valid = True
        self._FloatCtrl__val = set_float(value)
        self._FloatCtrl__max = set_float(maxval)
        self._FloatCtrl__min = set_float(minval)
        self._FloatCtrl__bound_val = None
        self._FloatCtrl__mark = None
        self._FloatCtrl__action = None
        self.fgcol_valid = 'Black'
        self.bgcol_valid = 'White'
        self.fgcol_invalid = 'Red'
        self.bgcol_invalid = (254, 254, 80)
        self.bell_on_invalid = bell_on_invalid
        if action_kw is None:
            action_kw = {}
        (self.SetAction)(action, **action_kw)
        this_sty = wx.TE_PROCESS_ENTER | wx.TE_RIGHT
        if 'style' in kws:
            this_sty = this_sty | kws['style']
        kws['style'] = this_sty
        (wx.TextCtrl.__init__)(self, parent, (wx.ID_ANY), **kws)
        self._FloatCtrl__CheckValid(self._FloatCtrl__val)
        self.SetValue(self._FloatCtrl__val)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_TEXT, self.OnText)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self._FloatCtrl__GetMark()

    def SetAction(self, action, **kws):
        """set callback action"""
        if hasattr(action, '__call__'):
            self._FloatCtrl__action = Closure(action, **kws)

    def SetPrecision(self, prec=0):
        """set precision"""
        self._FloatCtrl__prec = prec
        self.format = '%%.%if' % prec

    def __GetMark(self):
        """ keep track of cursor position within text"""
        try:
            self._FloatCtrl__mark = min(wx.TextCtrl.GetSelection(self)[0], len(wx.TextCtrl.GetValue(self).strip()))
        except:
            self._FloatCtrl__mark = 0

    def __SetMark(self, mark=None):
        """set mark for later"""
        if mark is None:
            mark = self._FloatCtrl__mark
        self.SetSelection(mark, mark)

    def SetValue(self, value=None, act=True):
        """ main method to set value """
        if value is None:
            value = wx.TextCtrl.GetValue(self).strip()
        else:
            self._FloatCtrl__CheckValid(value)
            self._FloatCtrl__GetMark()
            if value is not None:
                wx.TextCtrl.SetValue(self, self.format % set_float(value))
            if self.is_valid:
                if hasattr(self._FloatCtrl__action, '__call__'):
                    if act:
                        self._FloatCtrl__action(value=(self._FloatCtrl__val))
            if not self.is_valid:
                if self.bell_on_invalid:
                    wx.Bell()
        self._FloatCtrl__SetMark()

    def OnKillFocus(self, event):
        """focus lost"""
        self._FloatCtrl__GetMark()
        event.Skip()

    def OnSetFocus(self, event):
        """focus gained - resume editing from last mark point"""
        self._FloatCtrl__SetMark()
        event.Skip()

    def OnChar(self, event):
        """ on Character event"""
        key = event.GetKeyCode()
        entry = wx.TextCtrl.GetValue(self).strip()
        pos = wx.TextCtrl.GetSelection(self)
        if key == wx.WXK_RETURN:
            if not self.is_valid:
                wx.TextCtrl.SetValue(self, self.format % set_float(self._FloatCtrl__bound_val))
            else:
                self.SetValue(entry)
            return
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        has_minus = '-' in entry
        ckey = chr(key)
        if ckey == '.' and (self._FloatCtrl__prec == 0 or '.' in entry) or ckey == '-' and (has_minus or pos[0] != 0) or ckey != '-' and has_minus and pos[0] == 0:
            return
        if chr(key) in self._FloatCtrl__digits:
            event.Skip()

    def OnText(self, event=None):
        """text event"""
        try:
            if event.GetString() != '':
                self._FloatCtrl__CheckValid(event.GetString())
        except:
            pass

        event.Skip()

    def GetValue(self):
        if self._FloatCtrl__prec > 0:
            fmt = '{{:.{:d}f}}'.format(self._FloatCtrl__prec)
            return set_float(fmt.format(self._FloatCtrl__val))
        else:
            return int(self._FloatCtrl__val)

    def GetMin(self):
        """return min value"""
        return self._FloatCtrl__min

    def GetMax(self):
        """return max value"""
        return self._FloatCtrl__max

    def SetMin(self, val):
        """set min value"""
        self._FloatCtrl__min = set_float(val)

    def SetMax(self, val):
        """set max value"""
        self._FloatCtrl__max = set_float(val)

    def __CheckValid(self, value):
        """check for validity of value"""
        val = self._FloatCtrl__val
        self.is_valid = True
        try:
            val = set_float(value)
            if self._FloatCtrl__min is not None:
                if val < self._FloatCtrl__min:
                    self.is_valid = False
                    val = self._FloatCtrl__min
            if self._FloatCtrl__max is not None:
                if val > self._FloatCtrl__max:
                    self.is_valid = False
                    val = self._FloatCtrl__max
        except:
            self.is_valid = False

        self._FloatCtrl__bound_val = self._FloatCtrl__val = val
        fgcol, bgcol = self.fgcol_valid, self.bgcol_valid
        if not self.is_valid:
            fgcol, bgcol = self.fgcol_invalid, self.bgcol_invalid
        self.SetForegroundColour(fgcol)
        self.SetBackgroundColour(bgcol)
        self.Refresh()