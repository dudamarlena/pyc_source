# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brianbruggeman/repos/mine/glfw-cffi/glfw/__init__.py
# Compiled at: 2016-11-24 22:48:46
# Size of source mod 2**32: 23218 bytes
"""
Wrapper file for Python GLFW CFFI library

Created by Brian Bruggeman
Copyright (c) 2016

Usage:

    >>> import glfw
    >>> if not glfw.init():
    ...     raise RuntimeError('Could not initialize glfw')
    >>> win = glfw.create_window(640, 480, 'Sample')
    >>> while (not glfw.window_should_close(win)):  # ctrl+c to break
    ...     # Render scene here
    ...     glfw.swap_buffers(win)  # by default, glfw is double buffered
    ...     glfw.poll_events()
    >>> glfw.terminate()

License:  This file is released as Apache 2.0 license.  However, at
your option, you may apply any free software license you choose
provided that you adhere to the free software license chosen and
additionally follow these three criteria:
 a. list the author's name of this software as a contributor to your
    final product
 b. provide credit to your end user of your product or software without
    your end user asking for where you obtained your software
 c. notify the author of this software that you are using this software
 d. in addition, if you believe there can be some benefit in providing
    your changes upstream, you'll submit a change request.  While this
    criteria is completely optional, please consider not being a dick.
"""
from ctypes.util import find_library as _ctypes_find_library
import fnmatch, functools, imp, os, re, sys
from textwrap import dedent as dd
from cffi import FFI
import OpenGL.GL as _gl
if sys.version.startswith('2'):
    range = xrange
modname = os.path.basename(os.path.dirname(__file__))
__project__ = 'glfw-cffi'
__shortdoc__ = 'Foreign Function Interface wrapper for GLFW v3.x'
__license__ = 'Apache 2.0'
__version_str__ = '0.2.0'
__version__ = tuple(int(v.split('-')[0]) for v in __version_str__.split('.'))
__author__ = 'Brian Bruggeman'
__copyright__ = 'Copyright 2016 Brian Bruggeman'
__email__ = 'brian.m.bruggeman@gmail.com'
__url__ = 'https://github.com/brianbruggeman/glfw-cffi.git'

def _get_function_declaration(line):
    """Reads a line of C code and then extracts function declarations if found"""
    found = None
    pattern = ''.join(('^\\s*(?P<result>(.*))\\s+', '(?P<func_name>(glfw[A-Za-z_0-9*]+))',
                       '\\((?P<args>(.*))\\)\\;\\s*$'))
    eng = re.compile(pattern)
    if all(_ in line for _ in ('(', ')', ';')) and '@' not in line and not line.lstrip(' ').startswith('typedef') and eng.search(line.strip()):
        found = [group.groupdict() for group in eng.finditer(line)][0]
        func_name = found['func_name']
        found['snake_name'] = _camelToSnake(func_name.replace('glfw', ''))
    return found


def _fix_source(data):
    """Remove directives since they are not supported."""
    lines = []
    ignored_directives = ('#include', '#if', '#ifdef', '#endif', '#ifndef', '#else',
                          '#elif', '#error', '#undef', 'extern')
    prev_line = ''
    defines = {}
    for lineno, line in enumerate(data.split('\n')):
        if line.lstrip(' ').startswith(ignored_directives):
            prev_line = line
            continue
            if not line.strip():
                prev_line = line
                continue
                if line.lstrip(' ').startswith('GLFWAPI'):
                    line = line.replace('GLFWAPI ', '')
                vulkan_keys = [
                 'GLFWvkproc', 'VkInstance', 'VkPhysicalDevice']
                if any(key in line for key in vulkan_keys):
                    pass
        else:
            if prev_line == '#ifdef __cplusplus' and line.strip() == '}':
                prev_line = line
                continue
            if line.lstrip(' ').startswith('#define'):
                found = re.search('^(\\s*)\\#define\\s+([0-9A-Za-z_]+)\\s*$', line)
                if found:
                    continue
                else:
                    found = re.search('^(\\s*)\\#define\\s+([0-9A-Za-z_]+)\\s*(.*)$', line)
                if found:
                    space, key, value = found.groups()
                    if not len(space) > 0:
                        if value.startswith('__'):
                            continue
                        else:
                            if value in defines:
                                old_value, value = value, defines[value]
                                line = line.replace(old_value, value)
                            defines[key] = value
                        lines.append(line)
                        prev_line = line

    return '\n'.join(lines)


def _wrap_func(ffi, func_decl, func):
    """Wraps glfw functions with snake skins"""
    func_type = ffi.typeof(func)
    func_args = func_type.args
    func_res = func_type.result
    decl_args = func_decl['args']
    func_fields = []
    for ctype, arg in zip(func_args, decl_args.split(',')):
        arg = arg.replace(ctype.cname, '').replace(ctype.cname.replace(' ', ''), '')
        arg = arg.strip()
        arg = arg.split(' ')[(-1)]
        func_fields.append((arg, ctype))

    @functools.wraps(func)
    def wrapper(*args, **kwds):
        retval = []
        if func_args:
            new_args = []
            func_kwds = {}
            for (fname, ftype), arg in zip(func_fields, args):
                func_kwds[fname] = arg

            for name, ftype in func_fields:
                val = func_kwds.get(name)
                if val is None and ftype.kind == 'pointer':
                    val = ffi.new(ftype.cname, val)
                    func_kwds[name] = val
                    retval.append(val)
                new_args.append(val)

            if func_res.kind != 'void':
                retval = func(*new_args)
            else:
                func(*new_args)
        else:
            if func_res.kind != 'void':
                retval = func()
            else:
                func()
            if retval in [ffi.NULL, []]:
                retval = None
            elif isinstance(retval, list):
                retval = [ffi.string(l[0]) if isinstance(l[0], ffi.CData) and 'char' in ffi.typeof(l).cname else l[0] for l in retval]
        if isinstance(retval, ffi.CData) and 'char' in ffi.typeof(retval).cname:
            retval = ffi.string(retval)
        return retval

    def rename_code_object(func, new_name):
        """Magic bit so a stack trace and profiling doesn't identify wrapper
        as the function"""
        code_object = func.__code__
        function, code = type(func), type(code_object)
        code_objects = [
         code_object.co_argcount,
         code_object.co_nlocals,
         code_object.co_stacksize,
         code_object.co_flags,
         code_object.co_code,
         code_object.co_consts,
         code_object.co_names,
         code_object.co_varnames,
         code_object.co_filename,
         new_name,
         code_object.co_firstlineno,
         code_object.co_lnotab,
         code_object.co_freevars,
         code_object.co_cellvars]
        if sys.version.startswith('3'):
            code_objects.insert(1, code_object.co_kwonlyargcount)
        new_func = function(code(*code_objects), func.__globals__, new_name, func.__defaults__, func.__closure__)
        return new_func

    new_func = rename_code_object(wrapper, func_decl['snake_name'])
    docstring = func.__doc__
    docstring = docstring or '"{snake_name}" wrapps a glfw c-library function:.\n'
    docstring += 'The c-function declaration can be found below:\n\n'
    if func_args:
        if func_res.kind != 'void':
            docstring += '    {result} {func_name}({args})\n'
        else:
            docstring += '    void {func_name}({args})\n'
    else:
        if func_res.kind != 'void':
            docstring += '    {result} {func_name}(void)\n'
        else:
            docstring += '    void {func_name}(void)\n'
    new_func.__doc__ = docstring.format(**func_decl)
    return new_func


def _camelToSnake(string):
    """Converts camelCase to snake_case

    >>> print(_camelToSnake('ACase'))
    a_case
    >>> print(_camelToSnake('AnotherCaseHere'))
    another_case_here
    >>> print(_camelToSnake('AnotherCaseHereNow'))
    another_case_here_now
    >>> print(_camelToSnake('SimpleCase'))
    simple_case
    >>> print(_camelToSnake('simpleCase2'))
    simple_case_2
    >>> print(_camelToSnake('simpleCase3d'))
    simple_case_3d
    >>> print(_camelToSnake('simpleCase4D'))
    simple_case_4_d
    >>> print(_camelToSnake('simpleCase5thDimension'))
    simple_case_5th_dimension
    >>> print(_camelToSnake('simpleCase66thDimension'))
    simple_case_66th_dimension
    """
    patterns = [
     ('(.)([0-9]+)', '\\1_\\2'),
     ('([a-z]+)([A-Z])', '\\1_\\2')]
    engines = [(pattern, replacement, re.compile(pattern)) for pattern, replacement in patterns]
    for data in engines:
        pattern, replacement, eng = data
        string = eng.sub(replacement, string)

    string = string.lower()
    return string


def _load_header(header_path, ffi):
    """Loads a header file

    Args:
        header_path(str):  String to header file
        ffi(cffi.FFI):  FFI instance

    Returns:
        str: compiled string source
    """
    source = ''
    with open(header_path, 'r') as (fd):
        source = _fix_source(fd.read())
    ffi.cdef(source)
    return source


def _load_library(library_path, ffi):
    """Loads a library file given a path"""
    try:
        lib = ffi.dlopen(library_path)
    except Exception as e:
        import traceback as tb
        print(tb.format_exc(e))
        lib = None

    return lib


def _find_library(library_name, ffi, path=None):
    """Attempts to find and and load library name given path"""
    path = os.getcwd() if path is None else path
    path = path.strip('"')
    path = os.path.abspath(path)
    if os.path.exists(path) and os.path.isfile(path):
        lib = _load_library(path, ffi)
        if lib:
            pass
        return (
         lib, path)
    if not isinstance(library_name, (tuple, list)):
        library_name = [
         library_name]
    for libname in library_name:
        lib_path = _ctypes_find_library(libname)
        if lib_path:
            lib = _load_library(lib_path, ffi)
            if lib:
                lib_path = os.path.abspath(lib_path)
                return (lib, lib_path)

    lib_exts = ('dll', 'so')
    for root, folders, files in os.walk(path):
        for filename in files:
            if filename.startswith(library_name) and filename.endswith(lib_exts):
                filepath = os.path.join(root, filename)
                lib = _load_library(filepath, ffi)
                if lib:
                    return (
                     lib, filepath)

    return (None, '')


def _find_library_header(library_name, library_path, ffi):
    """Attempts to find and load a header file relative to the library path"""
    split_drive = lambda path: os.path.splitdrive(path)[(-1)]
    empty_paths = [os.path.sep, '', None]
    include_path = library_path
    include_path_found = False
    while split_drive(include_path) and split_drive(include_path) not in empty_paths:
        if os.path.isdir(include_path):
            file_list = [folder_object for folder_object in os.listdir(include_path) if fnmatch.fnmatch(folder_object, 'glfw*.h') or 'include' in folder_object]
            if file_list:
                break
        if not include_path_found:
            include_path = os.path.dirname(include_path)

    header_path = ''
    header_path_found = False
    source = ''
    for root, folders, files in os.walk(include_path):
        folders = [folder for folder in folders if folder == 'include']
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            if 'include' not in filepath:
                pass
            else:
                if library_name not in filepath.lower():
                    pass
                elif fnmatch.fnmatch(filename, 'glfw*.h'):
                    header_path = filepath
                    header_path_found = True
                    source = _load_header(header_path, ffi)
                    break

        if header_path_found:
            break

    return (
     header_path, source)


def _initialize_module(ffi):
    glfw_library_path = os.environ.get('GLFW_LIBRARY', None)
    library_names = ('glfw3', 'glfw')
    _glfw, glfw_path = _find_library(library_names, ffi, glfw_library_path)
    if not _glfw:
        err = dd('\n        Could not find glfw library.\n        GLFW_LIBRARY = "{}"\n        Update GLFW_LIBRARY environment variable with path to library binary.\n        '.format(glfw_library_path))
        raise RuntimeError(err)
    globals()['library_path'] = glfw_path
    header_path, source = _find_library_header('glfw3', glfw_path, ffi)
    if not header_path:
        err = dd('\n        Could not find glfw library include files.  They must exist within\n        an "include" library near the glfw library binary.\n        GLFW Path = "{}"\n        '.format(glfw_path))
        raise RuntimeError(err)
    globals()['header_path'] = header_path
    camelCase = {_camelToSnake(d.replace('glfw', '')):getattr(_glfw, d) for d in dir(_glfw) if d.startswith('_') or hasattr(getattr(_glfw, d), '__call__')}
    funcs = {_camelToSnake(k.replace('glfw', '')):v for k, v in camelCase.items()}
    for line in source.split('\n'):
        func_decl = _get_function_declaration(line)
        if func_decl:
            snake_name = func_decl['snake_name']
            if snake_name in funcs:
                some_func = funcs[snake_name]
                funcs[snake_name] = _wrap_func(ffi, func_decl, some_func)
            else:
                decl_func_name = func_decl['func_name']
                func = getattr(_glfw, decl_func_name) if hasattr(_glfw, decl_func_name) else None
                if func:
                    funcs[snake_name] = _wrap_func(ffi, func_decl, func)
                    camelCase[decl_func_name] = func

    globals().update(funcs)
    defs = {d.replace('GLFW_', ''):getattr(_glfw, d) for d in dir(_glfw) if d.startswith('GLFW_')}
    globals().update(defs)
    camelCase = {d:getattr(_glfw, d) for d in dir(_glfw) if hasattr(_glfw, d)}
    easy_translate = {_camelToSnake(d.replace('glfw', '')):getattr(_glfw, d) for d in dir(_glfw) if hasattr(_glfw, d)}
    core = imp.new_module('core')
    sys.modules['{}.core'.format(modname)] = core
    core.__dict__.update(camelCase)
    core.__dict__.update(easy_translate)
    globals()['core'] = core
    opengl_camelCase = {d:getattr(_gl, d) for d in dir(_gl) if hasattr(_gl, d) if hasattr(_gl, d)}
    opengl_snake_case = {_camelToSnake(d.replace('gl', '')):getattr(_gl, d) for d in dir(_gl) if hasattr(_gl, d) if not d.upper() == d if not d.startswith('GL_') if not d.startswith('GL_')}
    opengl_enums = {d.replace('GL_', ''):getattr(_gl, d) for d in dir(_gl) if hasattr(_gl, d) and d.upper() == d and d.startswith('GL_') if hasattr(_gl, d) and d.upper() == d and d.startswith('GL_')}
    gl = imp.new_module('gl')
    sys.modules['{}.gl'.format(modname)] = gl
    gl.__dict__.update(opengl_camelCase)
    gl.__dict__.update(opengl_snake_case)
    gl.__dict__.update(opengl_enums)
    globals()['gl'] = gl
    decorators = imp.new_module('decorators')
    sys.modules['{}.decorators'.format(modname)] = decorators
    decorators.__dict__.update(dict(error_callback=ffi.callback('void (int, const char*)'), char_callback=ffi.callback('void (GLFWwindow*, unsigned int)'), char_mods_callback=ffi.callback('void (GLFWwindow*, unsigned int, int)'), cursor_pos_callback=ffi.callback('void (GLFWwindow*, double, double)'), scroll_callback=ffi.callback('void (GLFWwindow*, double, double)'), mouse_button_callback=ffi.callback('void (GLFWwindow*, int, int, int)'), key_callback=ffi.callback('void (GLFWwindow*, int, int, int, int)'), cursor_enter_callback=ffi.callback('void (GLFWwindow*, int)'), framebuffer_size_callback=ffi.callback('void (GLFWwindow*, int, int)'), window_close_callback=ffi.callback('void (GLFWwindow*)'), window_focus_callback=ffi.callback('void (GLFWwindow*, int)'), window_iconify_callback=ffi.callback('void (GLFWwindow*, int)'), window_pos_callback=ffi.callback('void (GLFWwindow*, int, int)'), window_refresh_callback=ffi.callback('void (GLFWwindow*)'), window_size_callback=ffi.callback('void (GLFWwindow*, int, int)'), drop_callback=ffi.callback('void (GLFWwindow* window, int, const char**)'), monitor_callback=ffi.callback('void (GLFWmonitor*, int)')))
    globals()['decorators'] = decorators
    return (ffi, _glfw)


_ffi, _glfw = _initialize_module(FFI())
globs = {k:v for k, v in globals().items()}
for func in globs:
    if func not in ('_ffi', '_glfw') and (func.startswith('_') and not func.startswith('__') or func in ('modname', )):
        globals().pop(func)

globals().pop('globs')
globals().pop('func')

def get_include():
    """Returns header_path found during initialization"""
    include_path = header_path
    if include_path is not None:
        while include_path not in ('/', ''):
            if include_path.split(os.path.sep)[(-1)] == 'include':
                break
            include_path = os.path.dirname(include_path)

    return include_path


def create_window(width=640, height=480, title='Untitled', monitor=None, share=None):
    """Creates a window
    Context is used when state from one window needs to be transferred
    to the new window.  A GlfwWindow * can be used for context.
    This is common when switching between full-screen and windowed
    mode.  During this operation, the window must be destroyed and
    re-created.
    """
    if monitor is None:
        monitor = _ffi.NULL
    if share is None:
        share = _ffi.NULL
    if sys.version.startswith('3'):
        farg = _ffi.new('char []', bytes(title.encode('utf-8')))
        title = farg
    args = (
     width, height, title, monitor, share)
    win = _glfw.glfwCreateWindow(*args)
    if win == _ffi.NULL:
        win = None
    return win


_error_callback_wrapper = None

def set_error_callback(func):
    """Wraps the error callback function for GLFW and sets the callback function
    for the entire program"""
    global _error_callback_wrapper

    @decorators.error_callback
    def wrapper(error, description):
        return func(error, _ffi.string(description))

    _error_callback_wrapper = wrapper
    _glfw.glfwSetErrorCallback(wrapper)


def ffi_string(cdata):
    """Converts char * cdata into a python string"""
    if isinstance(cdata, _ffi.CData) and 'char' in _ffi.typeof(cdata).cname:
        cdata = _ffi.string(cdata)
    return cdata


def get_key_string(key):
    """Returns the name of a key"""
    val = 'KEY_'
    globs = dict(globals().items())
    lookup = {v:k.replace(val, '').lower() for k, v in globs.items() if k.startswith(val)}
    string = lookup.get(key, key)
    return string


def get_mod_string(mods):
    """Returns the name of a modifier"""
    val = 'MOD_'
    lookup = {v:k.replace(val, '').lower() for k, v in globals().items() if k.startswith(val)}
    string = '+'.join(sorted({v for m, v in lookup.items() if m & mods}))
    return string


def get_mouse_button_string(button):
    """Returns the name of a modifier"""
    val = 'MOUSE_BUTTON_'
    lookup = {v:k.replace(val, '').lower() for k, v in sorted(globals().items()) if k.startswith(val)}
    string = lookup.get(button, button)
    return string


def get_action_string(action):
    """Returns the name of a modifier"""
    options = [
     'RELEASE', 'PRESS', 'REPEAT']
    data = {v:k.lower() for k, v in globals().items() if k in options}
    return data.get(action, action)