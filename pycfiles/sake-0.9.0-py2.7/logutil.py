# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sake\logutil.py
# Compiled at: 2011-03-07 00:28:02
"""
Provide supporting functionality to the logging framework.
"""
import __builtin__
from cStringIO import StringIO
import linecache, logging, sys, time, traceback2, types, weakref
from . import network

class LogStream(object):
    """Buffers up console output and redirects it through the logging facilities."""

    def __init__(self, flag):
        self.flag = flag
        self.buff = []
        self.logger = logging.getLogger('CORE')

    def write(self, s):
        self.buff.append(s)
        if '\n' in s:
            for line in ('').join(self.buff).splitlines():
                if line:
                    self.logger.log(self.flag, line)

            del self.buff[:]


class CustomLogFormatter(logging.Formatter):

    def format(self, record):
        message = record.getMessage()
        if record.exc_info:
            if not record.exc_text:
                mode = {logging.FATAL: 'Fatal', logging.ERROR: 'Error', logging.WARNING: 'Warning', logging.INFO: 'Info'}.get(record.levelno, 'Unknown')
                record.exc_text = self.formatException(record.exc_info, message, mode)
        if record.exc_text:
            return record.exc_text
        return message

    def formatException(self, ei, extraText='', mode='Unknown', show_locals=1):
        exctype, exc, tb = ei
        exception_list = traceback2.extract_tb(tb, extract_locals=show_locals)
        if tb:
            caught_list = traceback2.extract_stack(tb.tb_frame)
        else:
            caught_list = traceback2.extract_stack(up=2)
        formatted_exception = traceback2.format_exception_only(exctype, exc)
        stack, stackID = GetStack(exception_list, caught_list, show_locals=show_locals)
        pre = ''
        traceID = GetNextTraceID()
        out = StringIO()
        out.write('%sEXCEPTION #%d logged at %s %s\n' % (pre, traceID, time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime()), extraText))
        for line in stack:
            out.write(line)

        for line in formatted_exception:
            out.write(line)

        try:
            _LogThreadLocals(out)
        except MemoryError:
            pass

        out.write('\n')
        try:
            txt = 'Application versions: '
            from . import app
            txt += app.app.GetVersionString()
            txt += ', RPC #%s' % network.RPC_API_VERSION
            txt += '\n'
            out.write(txt)
        except Exception as e:
            sys.exc_clear()

        out.write('%sEXCEPTION END\n' % pre)
        ret = out.getvalue()
        if stackID is not None:
            CallStackTraceProcessor(stackID, ret, mode)
        return ret


class CustomLogHandler(logging.Handler):
    pass


stackTraceProcessingFunction = None

def SetStackTraceProcessor(fn, ifNone=False):
    global stackTraceProcessingFunction
    if ifNone and stackTraceProcessingFunction is not None:
        return
    else:
        if type(fn) is types.FunctionType:
            stackTraceProcessingFunction = (
             weakref.ref(fn), None)
        elif type(fn) is types.MethodType:
            stackTraceProcessingFunction = (
             weakref.ref(fn.im_self), fn.im_func.func_name)
        return


def CallStackTraceProcessor(stackID, text, mode):
    if stackTraceProcessingFunction is not None:
        wr, functionName = stackTraceProcessingFunction
        r = wr()
        if r is not None:
            if functionName is not None:
                r = getattr(r, functionName)
            try:
                r(stackID, text, mode)
            except Exception:
                sys.stderr.write('Unexpected exception in stack trace processing, please notify Richard Tew')
                traceback2.print_exc()

    return


traceID = 1

def GetNextTraceID():
    global traceID
    _traceID = traceID
    traceID += 1
    return _traceID


getStackFileNames = {}
stackFileNameSubPaths = ()
stackFileNameRequiredPrefixes = ()

def SetStackFileNameSubPaths(subPaths):
    global stackFileNameSubPaths
    stackFileNameSubPaths = tuple(subPaths)


def SetStackFileNameRequiredPrefixes(requiredPrefixes):
    global stackFileNameRequiredPrefixes
    stackFileNameRequiredPrefixes = tuple(requiredPrefixes)


def GetStackFileName(filename):
    """
        returns a acceptable file name for the one passed in.
    """
    if filename not in getStackFileNames:
        filename2 = filename.lower().replace('\\', '/')
        for subpath in stackFileNameSubPaths:
            f = filename2.rfind(subpath)
            if f >= 0:
                filename2 = filename2[f:]
                break

        for prefix in stackFileNameRequiredPrefixes:
            if prefix in filename and prefix not in filename2:
                filename2 = '/..' + prefix[:-1] + filename2

        getStackFileNames[filename] = str(filename2)
    return getStackFileNames[filename]


def GetStack(exception_list, caught_list=None, show_locals=0, show_lines=True):
    s = GetStackOnly(exception_list, caught_list, show_locals, show_lines)
    id = GetStackID(exception_list, caught_list)
    return (s, id)


def GetStackID(exception_list, caught_list=None):
    stack = GetStackOnly(exception_list, caught_list, show_locals=0, show_lines=False)
    stack = ('').join(stack)[-4000:]
    return (adler32(stack), stack)


def GetStackOnly(exception_list, caught_list=None, show_locals=0, show_lines=True):
    if caught_list is not None:
        stack = [
         'Caught at:\n']
        stack += FormatList(caught_list, show_locals=False, show_lines=show_lines)
        stack.append('Thrown at:\n')
    else:
        stack = []
    stack += FormatList(exception_list, show_locals=show_locals, show_lines=show_lines)
    return stack


def FormatList(extracted_list, show_locals=0, show_lines=True):
    l = []
    for line in extracted_list:
        l2 = list(line)
        l2[0] = GetStackFileName(l2[0])
        if not show_lines:
            l2[3] = ''
        l.append(l2)

    lines = traceback2.format_list(l, show_locals, format=traceback2.FORMAT_LOGSRV | traceback2.FORMAT_SINGLE)
    return lines


def _LogThreadLocals(out):
    out.write('Thread Locals:\n')
    if hasattr(__builtin__, 'session'):
        out.write('  session was %s\n' % session)
    else:
        out.write('sorry, no session for you.\n')


import struct

def compute(data_to_checksum, size, modulo, limit=None):
    sum_, sum_of_sum = (1, 0)
    length = len(data_to_checksum)
    if limit is not None and length > limit:
        data_to_checksum = data_to_checksum[:limit]
    for char in data_to_checksum:
        sum_ += ord(char)
        sum_of_sum += sum_
        sum_ %= modulo
        sum_of_sum %= modulo

    return (sum_of_sum << size / 2) + sum_


def adler32(data_to_checksum):
    value = compute(data_to_checksum, 32, 65521, limit=5552)
    s = struct.pack('L', value)
    return struct.unpack('l', s)[0]