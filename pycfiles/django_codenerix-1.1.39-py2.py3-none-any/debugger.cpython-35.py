# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/lib/debugger.py
# Compiled at: 2018-04-20 03:39:56
# Size of source mod 2**32: 7767 bytes
"""
Debugger helps to debug the system
"""
__version__ = '2017082500'
__all__ = [
 'Debugger', 'lineno']
import time, datetime, inspect
from codenerix.lib.colors import colors

def lineno():
    """
    Returns the current line number in our program.
    """
    return inspect.currentframe().f_back.f_lineno


class Debugger(object):
    _Debugger__indebug = {}
    _Debugger__inname = None

    def __autoconfig(self):
        import sys
        debugger = {}
        debugger['screen'] = (
         sys.stdout, ['*'])
        self.set_debug(debugger)

    def set_debug(self, debug=None):
        if debug is None:
            self._Debugger__autoconfig()
        else:
            if type(debug) is dict:
                idebug = debug.copy()
                if 'deepness' in debug:
                    if debug['deepness']:
                        idebug['deepness'] -= 1
                    else:
                        idebug = {}
                    self._Debugger__indebug = idebug
            else:
                raise IOError('Argument is not a dictionary')

    def get_debug(self):
        return self._Debugger__indebug

    def set_name(self, name):
        self._Debugger__inname = name

    def get_name(self):
        return self._Debugger__inname

    def color(self, color):
        if color in colors:
            darkbit, subcolor = colors[color]
            return '\x1b[%1d;%02dm' % (darkbit, subcolor)
        else:
            if color:
                self.debug("\x1b[1;31mColor '%s' unknown\x1b[1;00m\n" % color)
            return ''

    def debug(self, msg=None, header=None, color=None, tail=None, head=None, footer=None):
        if header is None:
            if head is None:
                header = True
            else:
                header = head
            if tail is None:
                if footer is None:
                    tail = True
                else:
                    tail = footer
                clname = self.__class__.__name__
                if 'tabular' in self._Debugger__indebug:
                    tabular = self._Debugger__indebug['tabular']
            else:
                tabular = ''
            for name in self._Debugger__indebug:
                if name not in ('deepness', 'tabular'):
                    if name != 'screen':
                        color = None
                    color_ini = self.color(color)
                    color_end = self.color('close')
                    handler, indebug = self._Debugger__indebug[name]
                    if msg and type(handler) == str:
                        handlerbuf = open(handler, 'a')
                else:
                    handlerbuf = handler
                if clname in indebug or '*' in indebug and '-%s' % clname not in indebug:
                    if self._Debugger__inname:
                        headname = self._Debugger__inname
                    else:
                        headname = clname
                    message = color_ini
                    if header:
                        now = datetime.datetime.fromtimestamp(time.time())
                        message += '%02d/%02d/%d %02d:%02d:%02d %-15s - %s' % (now.day, now.month, now.year, now.hour, now.minute, now.second, headname, tabular)
                    if msg:
                        try:
                            message += str(msg)
                        except UnicodeEncodeError:
                            message += str(msg.encode('ascii', 'ignore'))

                        message += color_end
                        if tail:
                            message += '\n'
                        if msg:
                            handlerbuf.write(message)
                            handlerbuf.flush()
                        else:
                            return True
                        if msg and type(handler) == str:
                            handlerbuf.close()

            if not msg:
                return False

    def warning(self, msg, header=True, tail=True):
        self.warningerror(msg, header, 'WARNING', 'yellow', tail)

    def error(self, msg, header=True, tail=True):
        self.warningerror(msg, header, 'ERROR', 'red', tail)

    def warningerror(self, msg, header, prefix, color, tail):
        clname = self.__class__.__name__
        if 'tabular' in self._Debugger__indebug:
            tabular = self._Debugger__indebug['tabular']
        else:
            tabular = ''
        for name in self._Debugger__indebug:
            if name not in ('deepness', 'tabular'):
                handler, indebug = self._Debugger__indebug[name]
                if type(handler) == str:
                    handlerbuf = open(handler, 'a')
                else:
                    handlerbuf = handler
                if name != 'screen':
                    color = None
                color_ini = self.color(color)
                color_end = self.color('close')
                message = color_ini
                if header:
                    if self._Debugger__inname:
                        headname = self._Debugger__inname
                    else:
                        headname = clname
                    now = datetime.datetime.fromtimestamp(time.time())
                    message += '\n%s - %02d/%02d/%d %02d:%02d:%02d %-15s - %s' % (prefix, now.day, now.month, now.year, now.hour, now.minute, now.second, headname, tabular)
                if msg:
                    try:
                        message += str(msg)
                    except UnicodeEncodeError:
                        message += str(msg.encode('ascii', 'ignore'))

                    message += color_end
                    if tail:
                        message += '\n'
                    handlerbuf.write(message)
                    handlerbuf.flush()
                    if type(handler) == str:
                        handlerbuf.close()