# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\utils\filesystem.py
# Compiled at: 2017-04-19 05:14:04
from __future__ import unicode_literals
import logging, os, shutil, tempfile
from rbtools.utils.process import die
CONFIG_FILE = b'.reviewboardrc'
tempfiles = []
tempdirs = []
builtin = {}

def cleanup_tempfiles():
    for tmpfile in tempfiles:
        try:
            os.unlink(tmpfile)
        except:
            pass

    for tmpdir in tempdirs:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _load_python_file(filename, config):
    with open(filename) as (f):
        exec (compile(f.read(), filename, b'exec'), config)
        return config


def make_tempfile(content=None):
    """Creates a temporary file and returns the path.

    The path is stored in an array for later cleanup.
    """
    fd, tmpfile = tempfile.mkstemp()
    if content:
        os.write(fd, content)
    os.close(fd)
    tempfiles.append(tmpfile)
    return tmpfile


def make_tempdir(parent=None):
    """Creates a temporary directory and returns the path.

    The path is stored in an array for later cleanup.
    """
    tmpdir = tempfile.mkdtemp(dir=parent)
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
        die(b'Syntax error in config file: %s\nLine %i offset %i\n' % (
         filename, e.lineno, e.offset))

    return dict((k, config[k]) for k in set(config.keys()) - set(builtin.keys()))


def load_config():
    """Load configuration from .reviewboardrc files.

    This will read all of the .reviewboardrc files influencing the
    cwd and return a dictionary containing the configuration.
    """
    config = {}
    trees = {}
    aliases = {}
    for filename in reversed(get_config_paths()):
        parsed_config = parse_config_file(filename)
        trees.update(parsed_config.pop(b'TREES'))
        aliases.update(parsed_config.pop(b'ALIASES'))
        config.update(parsed_config)

    config[b'TREES'] = trees
    config[b'ALIASES'] = aliases
    return config


exec (
 b'True', builtin)