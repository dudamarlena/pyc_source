# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Newville/Codes/wxmplot/examples/floatcontrol.py
# Compiled at: 2019-09-06 17:04:03
# Size of source mod 2**32: 7415 bytes
"""
This is a collection of general purpose utility functions and classes,
especially useful for wx functionality
"""
import sys, wx
import wx.lib.masked as masked
import numpy

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
            if self.is_valid and hasattr(self._FloatCtrl__action, '__call__') and act:
                self._FloatCtrl__action(value=(self._FloatCtrl__val))
            else:
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

    def OnChar--- This code section failed: ---

 L. 163         0  LOAD_FAST                'event'
                2  LOAD_METHOD              GetKeyCode
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'key'

 L. 164         8  LOAD_GLOBAL              wx
               10  LOAD_ATTR                TextCtrl
               12  LOAD_METHOD              GetValue
               14  LOAD_FAST                'self'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  LOAD_METHOD              strip
               20  CALL_METHOD_0         0  '0 positional arguments'
               22  STORE_FAST               'entry'

 L. 165        24  LOAD_GLOBAL              wx
               26  LOAD_ATTR                TextCtrl
               28  LOAD_METHOD              GetSelection
               30  LOAD_FAST                'self'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  STORE_FAST               'pos'

 L. 168        36  LOAD_FAST                'key'
               38  LOAD_GLOBAL              wx
               40  LOAD_ATTR                WXK_RETURN
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    94  'to 94'

 L. 169        46  LOAD_FAST                'self'
               48  LOAD_ATTR                is_valid
               50  POP_JUMP_IF_TRUE     80  'to 80'

 L. 170        52  LOAD_GLOBAL              wx
               54  LOAD_ATTR                TextCtrl
               56  LOAD_METHOD              SetValue
               58  LOAD_FAST                'self'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                format
               64  LOAD_GLOBAL              set_float
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _FloatCtrl__bound_val
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  BINARY_MODULO    
               74  CALL_METHOD_2         2  '2 positional arguments'
               76  POP_TOP          
               78  JUMP_FORWARD         90  'to 90'
             80_0  COME_FROM            50  '50'

 L. 172        80  LOAD_FAST                'self'
               82  LOAD_METHOD              SetValue
               84  LOAD_FAST                'entry'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  POP_TOP          
             90_0  COME_FROM            78  '78'

 L. 173        90  LOAD_CONST               None
               92  RETURN_VALUE     
             94_0  COME_FROM            44  '44'

 L. 176        94  LOAD_FAST                'key'
               96  LOAD_GLOBAL              wx
               98  LOAD_ATTR                WXK_SPACE
              100  COMPARE_OP               <
              102  POP_JUMP_IF_TRUE    122  'to 122'
              104  LOAD_FAST                'key'
              106  LOAD_GLOBAL              wx
              108  LOAD_ATTR                WXK_DELETE
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_TRUE    122  'to 122'
              114  LOAD_FAST                'key'
              116  LOAD_CONST               255
              118  COMPARE_OP               >
              120  POP_JUMP_IF_FALSE   134  'to 134'
            122_0  COME_FROM           112  '112'
            122_1  COME_FROM           102  '102'

 L. 177       122  LOAD_FAST                'event'
              124  LOAD_METHOD              Skip
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  POP_TOP          

 L. 178       130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           120  '120'

 L. 183       134  LOAD_STR                 '-'
              136  LOAD_FAST                'entry'
              138  COMPARE_OP               in
              140  STORE_FAST               'has_minus'

 L. 184       142  LOAD_GLOBAL              chr
              144  LOAD_FAST                'key'
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  STORE_FAST               'ckey'

 L. 185       150  LOAD_FAST                'ckey'
              152  LOAD_STR                 '.'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   176  'to 176'
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                _FloatCtrl__prec
              162  LOAD_CONST               0
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_TRUE    224  'to 224'
              168  LOAD_STR                 '.'
              170  LOAD_FAST                'entry'
              172  COMPARE_OP               in
              174  POP_JUMP_IF_TRUE    224  'to 224'
            176_0  COME_FROM           156  '156'

 L. 186       176  LOAD_FAST                'ckey'
              178  LOAD_STR                 '-'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   200  'to 200'
              184  LOAD_FAST                'has_minus'
              186  POP_JUMP_IF_TRUE    224  'to 224'
              188  LOAD_FAST                'pos'
              190  LOAD_CONST               0
              192  BINARY_SUBSCR    
              194  LOAD_CONST               0
              196  COMPARE_OP               !=
              198  POP_JUMP_IF_TRUE    224  'to 224'
            200_0  COME_FROM           182  '182'

 L. 187       200  LOAD_FAST                'ckey'
              202  LOAD_STR                 '-'
              204  COMPARE_OP               !=
              206  POP_JUMP_IF_FALSE   228  'to 228'
              208  LOAD_FAST                'has_minus'
              210  POP_JUMP_IF_FALSE   228  'to 228'
              212  LOAD_FAST                'pos'
              214  LOAD_CONST               0
              216  BINARY_SUBSCR    
              218  LOAD_CONST               0
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   228  'to 228'
            224_0  COME_FROM           198  '198'
            224_1  COME_FROM           186  '186'
            224_2  COME_FROM           174  '174'
            224_3  COME_FROM           166  '166'

 L. 188       224  LOAD_CONST               None
              226  RETURN_VALUE     
            228_0  COME_FROM           222  '222'
            228_1  COME_FROM           210  '210'
            228_2  COME_FROM           206  '206'

 L. 190       228  LOAD_GLOBAL              chr
              230  LOAD_FAST                'key'
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                _FloatCtrl__digits
              238  COMPARE_OP               in
              240  POP_JUMP_IF_FALSE   250  'to 250'

 L. 191       242  LOAD_FAST                'event'
              244  LOAD_METHOD              Skip
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  POP_TOP          
            250_0  COME_FROM           240  '240'

Parse error at or near `COME_FROM' instruction at offset 228_1

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