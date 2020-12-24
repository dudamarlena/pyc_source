# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/utils/filesystem.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals
import json, logging, os, shutil, sys, tempfile
CONFIG_FILE = b'.reviewboardrc'
tempfiles = []
tempdirs = []
builtin = {}

def is_exe_in_path(name):
    """Checks whether an executable is in the user's search path.

    This expects a name without any system-specific executable extension.
    It will append the proper extension as necessary. For example,
    use "myapp" and not "myapp.exe".

    This will return True if the app is in the path, or False otherwise.

    Taken from djblets.util.filesystem to avoid an extra dependency
    """
    if sys.platform == b'win32' and not name.endswith(b'.exe'):
        name += b'.exe'
    for dir in os.environ[b'PATH'].split(os.pathsep):
        if os.path.exists(os.path.join(dir, name)):
            return True

    return False


def cleanup_tempfiles():
    for tmpfile in tempfiles:
        try:
            os.unlink(tmpfile)
        except OSError:
            pass

    for tmpdir in tempdirs:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _load_python_file(filename, config):
    with open(filename) as (f):
        exec compile(f.read(), filename, b'exec') in config
        return config


def make_tempfile(content=None, prefix=b'rbtools.', suffix=None, filename=None):
    """Create a temporary file and return the path.

    If not manually removed, then the resulting temp file will be removed when
    RBTools exits (or if :py:func:`cleanup_tempfiles` is called).

    This can be given an explicit name for a temporary file, in which case
    the file will be created inside of a temporary directory (created with
    :py:func:`make_tempdir`. In this case, the parent directory will only
    be deleted when :py:func:`cleanup_tempfiles` is called.

    Args:
        content (bytes, optional):
            The content for the text file.

        prefix (bool, optional):
            The prefix for the temp filename. This defaults to ``rbtools.``.

        suffix (bool, optional):
            The suffix for the temp filename.

        filename (unicode, optional):
            An explicit name of the file. If provided, this will override
            ``suffix`` and ``prefix``.

    Returns:
        unicode:
        The temp file path.
    """
    if filename is not None:
        tmpdir = make_tempdir()
        tmpfile = os.path.join(tmpdir, filename)
        with open(tmpfile, b'wb') as (fp):
            if content:
                fp.write(content)
    else:
        with tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix or b'', delete=False) as (fp):
            tmpfile = fp.name
            if content:
                fp.write(content)
    tempfiles.append(tmpfile)
    return tmpfile


def make_tempdir(parent=None):
    """Create a temporary directory and return the path.

    The path is stored in an array for later cleanup.

    Args:
        parent (unicode, optional):
            An optional parent directory to create the path in.

    Returns:
        unicode:
        The name of the new temporary directory.
    """
    tmpdir = tempfile.mkdtemp(prefix=b'rbtools.', dir=parent)
    tempdirs.append(tmpdir)
    return tmpdir


def make_empty_files(files):
    """Creates each file in the given list and any intermediate directories."""
    for f in files:
        path = os.path.dirname(f)
        if path and not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                logging.error(b'Unable to create directory %s: %s', path, e)
                continue

        try:
            with open(f, b'w'):
                os.utime(f, None)
        except IOError as e:
            logging.error(b'Unable to create empty file %s: %s', f, e)

    return


def walk_parents(path):
    """Walks up the tree to the root directory."""
    while os.path.splitdrive(path)[1] != os.sep:
        yield path
        path = os.path.dirname(path)


def get_home_path():
    """Retrieve the homepath."""
    if b'HOME' in os.environ:
        return os.environ[b'HOME']
    else:
        if b'APPDATA' in os.environ:
            return os.environ[b'APPDATA']
        return b''


def get_config_paths():
    """Return the paths to each :file:`.reviewboardrc` influencing the cwd.

    A list of paths to :file:`.reviewboardrc` files will be returned, where
    each subsequent list entry should have lower precedence than the previous.
    i.e. configuration found in files further up the list will take precedence.

    Configuration in the paths set in :envvar:`$RBTOOLS_CONFIG_PATH` will take
    precedence over files found in the current working directory or its
    parents.
    """
    config_paths = []
    for path in os.environ.get(b'RBTOOLS_CONFIG_PATH', b'').split(os.pathsep):
        if not path:
            continue
        filename = os.path.realpath(os.path.join(path, CONFIG_FILE))
        if os.path.exists(filename) and filename not in config_paths:
            config_paths.append(filename)

    for path in walk_parents(os.getcwd()):
        filename = os.path.realpath(os.path.join(path, CONFIG_FILE))
        if os.path.exists(filename) and filename not in config_paths:
            config_paths.append(filename)

    home_config_path = os.path.realpath(os.path.join(get_home_path(), CONFIG_FILE))
    if os.path.exists(home_config_path) and home_config_path not in config_paths:
        config_paths.append(home_config_path)
    return config_paths


def parse_config_file(filename):
    """Parse a .reviewboardrc file.

    Returns a dictionary containing the configuration from the file.

    The ``filename`` argument should contain a full path to a
    .reviewboardrc file.
    """
    config = {b'TREES': {}, b'ALIASES': {}}
    try:
        config = _load_python_file(filename, config)
    except SyntaxError as e:
        raise Exception(b'Syntax error in config file: %s\nLine %i offset %i\n' % (
         filename, e.lineno, e.offset))

    return dict((k, config[k]) for k in set(config.keys()) - set(builtin.keys()))


def load_config():
    """Load configuration from .reviewboardrc files.

    This will read all of the .reviewboardrc files influencing the
    cwd and return a dictionary containing the configuration.
    """
    nested_config = {b'ALIASES': {}, b'COLOR': {b'INFO': None, 
                  b'DEBUG': None, 
                  b'WARNING': b'yellow', 
                  b'ERROR': b'red', 
                  b'CRITICAL': b'red'}, 
       b'TREES': {}}
    config = {}
    for filename in reversed(get_config_paths()):
        parsed_config = parse_config_file(filename)
        for key in nested_config:
            nested_config[key].update(parsed_config.pop(key, {}))

        config.update(parsed_config)

    config.update(nested_config)
    return config


exec b'True' in builtin