# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/util/config.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 14665 bytes
"""Vispy configuration functions
"""
import os
from os import path as op
import json, sys, platform, getopt, traceback, tempfile, atexit
from shutil import rmtree
from .event import EmitterGroup, EventEmitter, Event
from .logs import logger, set_log_level, use_log_level
from ext.six import string_types, file_types
file_types = list(file_types)
try:
    file_types += [tempfile._TemporaryFileWrapper]
except Exception:
    pass

file_types = tuple(file_types)
config = None
_data_path = None
_allowed_config_keys = None

def _init():
    """ Create global Config object, parse command flags
    """
    global _allowed_config_keys
    global _data_path
    global config
    app_dir = _get_vispy_app_dir()
    if app_dir is not None:
        _data_path = op.join(app_dir, 'data')
        _test_data_path = op.join(app_dir, 'test_data')
    else:
        _data_path = _test_data_path = None
    _allowed_config_keys = {'data_path':string_types, 
     'default_backend':string_types, 
     'gl_backend':string_types, 
     'gl_debug':(
      bool,), 
     'glir_file':string_types + file_types, 
     'include_path':list, 
     'logging_level':string_types, 
     'qt_lib':string_types, 
     'dpi':(
      int, type(None)), 
     'profile':string_types + (type(None),), 
     'audit_tests':(
      bool,), 
     'test_data_path':string_types + (type(None),)}
    default_config_options = {'data_path':_data_path, 
     'default_backend':'', 
     'gl_backend':'gl2', 
     'gl_debug':False, 
     'glir_file':'', 
     'include_path':[],  'logging_level':'info', 
     'qt_lib':'any', 
     'dpi':None, 
     'profile':None, 
     'audit_tests':False, 
     'test_data_path':_test_data_path}
    config = Config(**default_config_options)
    try:
        (config.update)(**_load_config())
    except Exception as err:
        try:
            raise Exception('Error while reading vispy config file "%s":\n  %s' % (
             _get_config_fname(), err.message))
        finally:
            err = None
            del err

    set_log_level(config['logging_level'])
    _parse_command_line_arguments()


VISPY_HELP = '\nVisPy command line arguments:\n\n  --vispy-backend=(qt|pyqt4|pyqt5|pyside|glfw|pyglet|sdl2|wx)\n    Selects the backend system for VisPy to use. This will override the default\n    backend selection in your configuration file.\n\n  --vispy-log=(debug|info|warning|error|critical)[,search string]\n    Sets the verbosity of logging output. The default is \'warning\'. If a search\n    string is given, messages will only be displayed if they match the string,\n    or if their call location (module.class:method(line) or\n    module:function(line)) matches the string.\n\n  --vispy-dpi=resolution\n    Force the screen resolution to a certain value (in pixels per inch). By\n    default, the OS is queried to determine the screen DPI.\n\n  --vispy-fps\n    Print the framerate (in Frames Per Second) in the console.\n\n  --vispy-gl-debug\n    Enables error checking for all OpenGL calls.\n\n  --vispy-glir-file\n    Export glir commands to specified file.\n\n  --vispy-profile=locations\n    Measure performance at specific code locations and display results. \n    *locations* may be "all" or a comma-separated list of method names like\n    "SceneCanvas.draw_visual".\n\n  --vispy-cprofile\n    Enable profiling using the built-in cProfile module and display results\n    when the program exits.\n\n  --vispy-audit-tests\n    Enable user auditing of image test results.\n\n  --vispy-help\n    Display this help message.\n\n'

def _parse_command_line_arguments():
    """ Transform vispy specific command line args to vispy config.
    Put into a function so that any variables dont leak in the vispy namespace.
    """
    argnames = [
     'vispy-backend=', 'vispy-gl-debug', 'vispy-glir-file=',
     'vispy-log=', 'vispy-help', 'vispy-profile=', 'vispy-cprofile',
     'vispy-dpi=', 'vispy-audit-tests']
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', argnames)
    except getopt.GetoptError:
        opts = []

    for o, a in opts:
        if o.startswith('--vispy'):
            if o == '--vispy-backend':
                config['default_backend'] = a
                logger.info('vispy backend: %s', a)
            elif o == '--vispy-gl-debug':
                config['gl_debug'] = True
            elif o == '--vispy-glir-file':
                config['glir_file'] = a
            elif o == '--vispy-log':
                if ',' in a:
                    verbose, match = a.split(',')
                else:
                    verbose = a
                    match = None
                config['logging_level'] = a
                set_log_level(verbose, match)
            elif o == '--vispy-profile':
                config['profile'] = a
            elif o == '--vispy-cprofile':
                _enable_profiling()
            elif o == '--vispy-help':
                print(VISPY_HELP)
            elif o == '--vispy-dpi':
                config['dpi'] = int(a)
            elif o == '--vispy-audit-tests':
                config['audit_tests'] = True
            else:
                logger.warning('Unsupported vispy flag: %s' % o)


def _get_vispy_app_dir():
    """Helper to get the default directory for storing vispy data"""
    user_dir = os.path.expanduser('~')
    path = None
    if sys.platform.startswith('win'):
        path1, path2 = os.getenv('LOCALAPPDATA'), os.getenv('APPDATA')
        path = path1 or path2
    else:
        if sys.platform.startswith('darwin'):
            path = os.path.join(user_dir, 'Library', 'Application Support')
        else:
            path = path and os.path.isdir(path) or user_dir
        prefix = sys.prefix
        if getattr(sys, 'frozen', None):
            prefix = os.path.abspath(os.path.dirname(sys.path[0]))
        for reldir in ('settings', '../settings'):
            localpath = os.path.abspath(os.path.join(prefix, reldir))
            if os.path.isdir(localpath):
                try:
                    open(os.path.join(localpath, 'test.write'), 'wb').close()
                    os.remove(os.path.join(localpath, 'test.write'))
                except IOError:
                    pass
                else:
                    path = localpath
                    break

        appname = '.vispy' if path == user_dir else 'vispy'
        path = os.path.join(path, appname)
        return path


class ConfigEvent(Event):
    __doc__ = " Event indicating a configuration change.\n\n    This class has a 'changes' attribute which is a dict of all name:value\n    pairs that have changed in the configuration.\n    "

    def __init__(self, changes):
        Event.__init__(self, type='config_change')
        self.changes = changes


class Config(object):
    __doc__ = ' Container for global settings used application-wide in vispy.\n\n    Events:\n    -------\n    Config.events.changed - Emits ConfigEvent whenever the configuration\n    changes.\n    '

    def __init__(self, **kwargs):
        self.events = EmitterGroup(source=self)
        self.events['changed'] = EventEmitter(event_class=ConfigEvent,
          source=self)
        self._config = {}
        (self.update)(**kwargs)
        self._known_keys = get_config_keys()

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, item, val):
        self._check_key_val(item, val)
        self._config[item] = val
        self.events.changed(changes={item: val})

    def _check_key_val(self, key, val):
        known_keys = _allowed_config_keys
        if key not in known_keys:
            raise KeyError('key "%s" not in known keys: "%s"' % (
             key, known_keys))
        if not isinstance(val, known_keys[key]):
            raise TypeError('Value for key "%s" must be one of %s, not %s.' % (
             key, known_keys[key], type(val)))

    def update(self, **kwargs):
        for key, val in kwargs.items():
            self._check_key_val(key, val)

        self._config.update(kwargs)
        self.events.changed(changes=kwargs)

    def __repr__(self):
        return repr(self._config)


def get_config_keys():
    """The config keys known by vispy and their allowed data types.

    Returns
    -------
    keys : dict
        Dict of {key: (types,)} pairs.
    """
    return _allowed_config_keys.copy()


def _get_config_fname():
    """Helper for the vispy config file"""
    directory = _get_vispy_app_dir()
    if directory is None:
        return
    fname = op.join(directory, 'vispy.json')
    if os.environ.get('_VISPY_CONFIG_TESTING', None) is not None:
        fname = op.join(_TempDir(), 'vispy.json')
    return fname


def _load_config():
    """Helper to load prefs from ~/.vispy/vispy.json"""
    fname = _get_config_fname()
    return fname is None or op.isfile(fname) or dict()
    with open(fname, 'r') as (fid):
        config = json.load(fid)
    return config


def save_config(**kwargs):
    """Save configuration keys to vispy config file

    Parameters
    ----------
    **kwargs : keyword arguments
        Key/value pairs to save to the config file.
    """
    if kwargs == {}:
        kwargs = config._config
    else:
        current_config = _load_config()
        (current_config.update)(**kwargs)
        fname = _get_config_fname()
        if fname is None:
            raise RuntimeError('config filename could not be determined')
        op.isdir(op.dirname(fname)) or os.mkdir(op.dirname(fname))
    with open(fname, 'w') as (fid):
        json.dump(current_config, fid, sort_keys=True, indent=0)


def set_data_dir(directory=None, create=False, save=False):
    """Set vispy data download directory

    Parameters
    ----------
    directory : str | None
        The directory to use.
    create : bool
        If True, create directory if it doesn't exist.
    save : bool
        If True, save the configuration to the vispy config.
    """
    if directory is None:
        directory = _data_path
        if _data_path is None:
            raise IOError('default path cannot be determined, please set it manually (directory != None)')
    if not op.isdir(directory):
        if not create:
            raise IOError('directory "%s" does not exist, perhaps try create=True to create it?' % directory)
        os.mkdir(directory)
    config.update(data_path=directory)
    if save:
        save_config(data_path=directory)


def _enable_profiling():
    """ Start profiling and register callback to print stats when the program
    exits.
    """
    global _profiler
    import cProfile, atexit
    _profiler = cProfile.Profile()
    _profiler.enable()
    atexit.register(_profile_atexit)


_profiler = None

def _profile_atexit():
    _profiler.print_stats(sort='cumulative')


def sys_info(fname=None, overwrite=False):
    """Get relevant system and debugging information

    Parameters
    ----------
    fname : str | None
        Filename to dump info to. Use None to simply print.
    overwrite : bool
        If True, overwrite file (if it exists).

    Returns
    -------
    out : str
        The system information as a string.
    """
    if fname is not None:
        if op.isfile(fname):
            if not overwrite:
                raise IOError('file exists, use overwrite=True to overwrite')
    out = ''
    try:
        from ..app import use_app, Canvas
        from app.backends import BACKEND_NAMES
        from ..gloo import gl
        from ..testing import has_backend
        with use_log_level('warning'):
            app = use_app(call_reuse=False)
        out += 'Platform: %s\n' % platform.platform()
        out += 'Python:   %s\n' % str(sys.version).replace('\n', ' ')
        out += 'Backend:  %s\n' % app.backend_name
        for backend in BACKEND_NAMES:
            if backend.startswith('ipynb_'):
                continue
            with use_log_level('warning', print_msg=False):
                which = has_backend(backend, out=['which'])[1]
            out += '{0:<9} {1}\n'.format(backend + ':', which)

        out += '\n'
        canvas = Canvas('Test', (10, 10), show=False, app=app)
        canvas._backend._vispy_set_current()
        out += 'GL version:  %r\n' % (gl.glGetParameter(gl.GL_VERSION),)
        x_ = gl.GL_MAX_TEXTURE_SIZE
        out += 'MAX_TEXTURE_SIZE: %r\n' % (gl.glGetParameter(x_),)
        out += 'Extensions: %r\n' % (gl.glGetParameter(gl.GL_EXTENSIONS),)
        canvas.close()
    except Exception:
        out += '\nInfo-gathering error:\n%s' % traceback.format_exc()

    if fname is not None:
        with open(fname, 'w') as (fid):
            fid.write(out)
    return out


class _TempDir(str):
    __doc__ = 'Class for creating and auto-destroying temp dir\n\n    This is designed to be used with testing modules.\n\n    We cannot simply use __del__() method for cleanup here because the rmtree\n    function may be cleaned up before this object, so we use the atexit module\n    instead.\n    '

    def __new__(self):
        new = str.__new__(self, tempfile.mkdtemp())
        return new

    def __init__(self):
        self._path = self.__str__()
        atexit.register(self.cleanup)

    def cleanup(self):
        rmtree((self._path), ignore_errors=True)


_init()