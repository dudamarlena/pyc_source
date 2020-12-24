# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/__init__.py
# Compiled at: 2009-02-18 19:37:25
"""pyglet is a cross-platform games and multimedia package.

Detailed documentation is available at http://www.pyglet.org
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: __init__.py 2284 2008-10-04 02:29:50Z Alex.Holkner $'
import os, sys
_is_epydoc = hasattr(sys, 'is_epydoc') and sys.is_epydoc
version = '1.1.2'

def _require_ctypes_version(version):
    import ctypes
    req = [ int(i) for i in version.split('.') ]
    have = [ int(i) for i in ctypes.__version__.split('.') ]
    if not tuple(have) >= tuple(req):
        raise ImportError('pyglet requires ctypes %s or later.' % version)


_require_ctypes_version('1.0.0')
_enable_optimisations = not __debug__
if getattr(sys, 'frozen', None):
    _enable_optimisations = True
options = {'audio': ('directsound', 'openal', 'alsa', 'silent'), 
   'font': ('gdiplus', 'win32'), 
   'debug_font': False, 
   'debug_gl': not _enable_optimisations, 
   'debug_gl_trace': False, 
   'debug_gl_trace_args': False, 
   'debug_graphics_batch': False, 
   'debug_lib': False, 
   'debug_media': False, 
   'debug_texture': False, 
   'debug_trace': False, 
   'debug_trace_args': False, 
   'debug_trace_depth': 1, 
   'debug_trace_flush': True, 
   'debug_win32': False, 
   'debug_x11': False, 
   'graphics_vbo': True, 
   'shadow_window': True, 
   'vsync': None, 
   'xsync': True}
_option_types = {'audio': tuple, 
   'font': tuple, 
   'debug_font': bool, 
   'debug_gl': bool, 
   'debug_gl_trace': bool, 
   'debug_gl_trace_args': bool, 
   'debug_graphics_batch': bool, 
   'debug_lib': bool, 
   'debug_media': bool, 
   'debug_texture': bool, 
   'debug_trace': bool, 
   'debug_trace_args': bool, 
   'debug_trace_depth': int, 
   'debug_trace_flush': bool, 
   'debug_win32': bool, 
   'debug_x11': bool, 
   'graphics_vbo': bool, 
   'shadow_window': bool, 
   'vsync': bool, 
   'xsync': bool}

def _read_environment():
    """Read defaults for options from environment"""
    for key in options:
        env = 'PYGLET_%s' % key.upper()
        try:
            value = os.environ[('PYGLET_%s' % key.upper())]
            if _option_types[key] is tuple:
                options[key] = value.split(',')
            elif _option_types[key] is bool:
                options[key] = value in ('true', 'TRUE', 'True', '1')
            elif _option_types[key] is int:
                options[key] = int(value)
        except KeyError:
            pass


_read_environment()
if sys.platform == 'cygwin':
    import ctypes
    ctypes.windll = ctypes.cdll
    ctypes.oledll = ctypes.cdll
    ctypes.WINFUNCTYPE = ctypes.CFUNCTYPE
    ctypes.HRESULT = ctypes.c_long
_trace_filename_abbreviations = {}

def _trace_repr(value, size=40):
    value = repr(value)
    if len(value) > size:
        value = value[:size // 2 - 2] + '...' + value[-size // 2 - 1:]
    return value


def _trace_frame(frame, indent):
    from pyglet import lib
    import os
    if frame.f_code is lib._TraceFunction.__call__.func_code:
        is_ctypes = True
        func = frame.f_locals['self']._func
        name = func.__name__
        location = '[ctypes]'
    else:
        is_ctypes = False
        code = frame.f_code
        name = code.co_name
        path = code.co_filename
        line = code.co_firstlineno
        try:
            filename = _trace_filename_abbreviations[path]
        except KeyError:
            dir = ''
            (path, filename) = os.path.split(path)
            while len(dir + filename) < 30:
                filename = os.path.join(dir, filename)
                (path, dir) = os.path.split(path)
                if not dir:
                    filename = os.path.join('', filename)
                    break
            else:
                filename = os.path.join('...', filename)

            _trace_filename_abbreviations[path] = filename

        location = '(%s:%d)' % (filename, line)
    if indent:
        name = 'Called from %s' % name
    print '%s%s %s' % (indent, name, location)
    if _trace_args:
        if is_ctypes:
            args = [ _trace_repr(arg) for arg in frame.f_locals['args'] ]
            print '  %sargs=(%s)' % (indent, (', ').join(args))
        else:
            for argname in code.co_varnames[:code.co_argcount]:
                try:
                    argvalue = _trace_repr(frame.f_locals[argname])
                    print '  %s%s=%s' % (indent, argname, argvalue)
                except:
                    pass

    if _trace_flush:
        sys.stdout.flush()


def _trace_func(frame, event, arg):
    if event == 'call':
        indent = ''
        for i in range(_trace_depth):
            _trace_frame(frame, indent)
            indent += '  '
            frame = frame.f_back
            if not frame:
                break

    if event == 'exception':
        (exception, value, traceback) = arg
        print 'First chance exception raised:', repr(exception)


def _install_trace():
    sys.setprofile(_trace_func)


_trace_args = options['debug_trace_args']
_trace_depth = options['debug_trace_depth']
_trace_flush = options['debug_trace_flush']
if options['debug_trace']:
    _install_trace()

class _ModuleProxy(object):
    _module = None

    def __init__(self, name):
        self.__dict__['_module_name'] = name

    def __getattr__(self, name):
        try:
            return getattr(self._module, name)
        except AttributeError:
            if self._module is not None:
                raise
            import_name = 'pyglet.%s' % self._module_name
            __import__(import_name)
            module = sys.modules[import_name]
            object.__setattr__(self, '_module', module)
            globals()[self._module_name] = module
            return getattr(module, name)

        return

    def __setattr__(self, name, value):
        try:
            setattr(self._module, name, value)
        except AttributeError:
            if self._module is not None:
                raise
            import_name = 'pyglet.%s' % self._module_name
            __import__(import_name)
            module = sys.modules[import_name]
            object.__setattr__(self, '_module', module)
            globals()[self._module_name] = module
            setattr(module, name, value)

        return


if not _is_epydoc:
    app = _ModuleProxy('app')
    clock = _ModuleProxy('clock')
    com = _ModuleProxy('com')
    event = _ModuleProxy('event')
    font = _ModuleProxy('font')
    gl = _ModuleProxy('gl')
    graphics = _ModuleProxy('graphics')
    image = _ModuleProxy('image')
    lib = _ModuleProxy('lib')
    media = _ModuleProxy('media')
    resource = _ModuleProxy('resource')
    sprite = _ModuleProxy('sprite')
    text = _ModuleProxy('text')
    window = _ModuleProxy('window')
if False:
    import app, clock, com, event, font, gl, graphics, image, lib, media, resource, sprite, text, window
if _is_epydoc:
    import window