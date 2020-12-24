# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/location.py
# Compiled at: 2018-06-25 10:54:26
import inspect, pyficache
from trepan.lib import stack as Mstack
import os.path as osp
from trepan.processor.parse.semantics import Location
INVALID_LOCATION = None

def resolve_location(proc, location, canonic=True):
    """Expand fields in Location namedtuple. If:
       '.':  get fields from stack
       function/module: get fields from evaluation/introspection
       location file and line number: use that
    """
    curframe = proc.curframe
    if location == '.':
        if not curframe:
            proc.errmsg("Don't have a stack to get location from")
            return INVALID_LOCATION
        filename = Mstack.frame2file(proc.core, curframe, canonic=canonic)
        lineno = inspect.getlineno(curframe)
        return Location(filename, lineno, False, None)
    assert isinstance(location, Location)
    is_address = False
    if proc.curframe:
        g = curframe.f_globals
        l = curframe.f_locals
    else:
        g = globals()
        l = locals()
    if location.method:
        filename = lineno = None
        msg = 'Object %s is not known yet as a function, ' % location.method
        try:
            modfunc = eval(location.method, g, l)
        except:
            proc.errmsg(msg)
            return INVALID_LOCATION
        else:
            try:
                if inspect.isfunction(modfunc) or hasattr(modfunc, 'im_func'):
                    pass
                else:
                    proc.errmsg(msg)
                    return INVALID_LOCATION
            except:
                proc.errmsg(msg)
                return INVALID_LOCATION
            else:
                filename = proc.core.canonic(modfunc.func_code.co_filename)
                lineno = modfunc.func_code.co_firstlineno
    elif location.path:
        filename = proc.core.canonic(location.path)
        lineno = location.line_number
        modfunc = None
        msg = '%s is not known as a file' % location.path
        if not osp.isfile(filename):
            try:
                modfunc = eval(location.path, g, l)
            except:
                msg = "Don't see '%s' as a existing file or as an module" % location.path
                proc.errmsg(msg)
                return INVALID_LOCATION
            else:
                is_address = location.is_address
                if inspect.ismodule(modfunc):
                    if hasattr(modfunc, '__file__'):
                        filename = pyficache.pyc2py(modfunc.__file__)
                        filename = proc.core.canonic(filename)
                        if not lineno:
                            lineno = 1
                            is_address = False
                        return Location(filename, lineno, is_address, modfunc)
                    else:
                        msg = "module '%s' doesn't have a file associated with it" % location.path
                proc.errmsg(msg)
                return INVALID_LOCATION
        maxline = pyficache.maxline(filename)
        if maxline and lineno > maxline:
            proc.errmsg('Line number %d out of range; %s has %d lines.' % (lineno, filename, maxline))
            return INVALID_LOCATION
    elif location.line_number:
        filename = Mstack.frame2file(proc.core, curframe, canonic=canonic)
        lineno = location.line_number
        is_address = location.is_address
        modfunc = None
    return Location(filename, lineno, is_address, modfunc)


def resolve_address_location(proc, location, canonic=False):
    """Expand fields in Location namedtuple. If:
       '.':  get fields from stack
       function/module: get fields from evaluation/introspection
       location file and line number: use that
    """
    curframe = proc.curframe
    if location == '.':
        filename = Mstack.frame2file(proc.core, curframe, canonic=canonic)
        offset = curframe.f_lasti
        is_address = True
        return Location(filename, offset, False, None)
    assert isinstance(location, Location)
    is_address = True
    if proc.curframe:
        g = curframe.f_globals
        l = curframe.f_locals
    else:
        g = globals()
        l = locals()
    if location.method:
        filename = offset = None
        msg = 'Object %s is not known yet as a function, ' % location.method
        try:
            modfunc = eval(location.method, g, l)
        except:
            proc.errmsg(msg)
            return INVALID_LOCATION
        else:
            try:
                if inspect.isfunction(modfunc) or hasattr(modfunc, 'im_func'):
                    pass
                else:
                    proc.errmsg(msg)
                    return INVALID_LOCATION
            except:
                proc.errmsg(msg)
                return INVALID_LOCATION
            else:
                filename = proc.core.canonic(modfunc.func_code.co_filename)
                offset = 0
    elif location.path:
        filename = proc.core.canonic(location.path)
        offset = location.line_number
        is_address = location.is_address
        modfunc = None
        msg = '%s is not known as a file' % location.path
        if not osp.isfile(filename):
            try:
                modfunc = eval(location.path, g, l)
            except:
                msg = "Don't see '%s' as a existing file or as an module" % location.path
                proc.errmsg(msg)
                return INVALID_LOCATION
            else:
                is_address = location.is_address
                if inspect.ismodule(modfunc):
                    if hasattr(modfunc, '__file__'):
                        filename = pyficache.pyc2py(modfunc.__file__)
                        filename = proc.core.canonic(filename)
                        if not offset:
                            offset = 0
                            is_address = True
                        return Location(filename, offset, is_address, modfunc)
                    else:
                        msg = "module '%s' doesn't have a file associated with it" % location.path
                proc.errmsg(msg)
                return INVALID_LOCATION
        maxline = pyficache.maxline(filename)
        if maxline and offset > maxline:
            proc.errmsg('Line number %d out of range; %s has %d lines.' % (offset, filename, maxline))
            return INVALID_LOCATION
    elif location.line_number is not None:
        filename = Mstack.frame2file(proc.core, curframe, canonic=False)
        offset = location.line_number
        is_address = location.is_address
        modfunc = proc.list_object
    return Location(filename, offset, is_address, modfunc)