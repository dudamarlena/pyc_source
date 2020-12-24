# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\utils\filesystem.py
# Compiled at: 2012-09-04 05:45:40
import os, tempfile
from rbtools.utils.process import die
CONFIG_FILE = '.reviewboardrc'
tempfiles = []

def cleanup_tempfiles():
    for tmpfile in tempfiles:
        try:
            os.unlink(tmpfile)
        except:
            pass


def get_config_value(configs, name, default=None):
    for c in configs:
        if name in c:
            return c[name]

    return default


def load_config_files(homepath):
    """Loads data from .reviewboardrc files."""

    def _load_config(path):
        config = {'TREES': {}}
        filename = os.path.join(path, CONFIG_FILE)
        if os.path.exists(filename):
            try:
                execfile(filename, config)
            except SyntaxError, e:
                die('Syntax error in config file: %s\nLine %i offset %i\n' % (
                 filename, e.lineno, e.offset))

            return config
        else:
            return

    configs = []
    for path in walk_parents(os.getcwd()):
        config = _load_config(path)
        if config:
            configs.append(config)

    return (
     _load_config(homepath), configs)


def make_tempfile(content=None):
    """
    Creates a temporary file and returns the path. The path is stored
    in an array for later cleanup.
    """
    (fd, tmpfile) = tempfile.mkstemp()
    if content:
        os.write(fd, content)
    os.close(fd)
    tempfiles.append(tmpfile)
    return tmpfile


def walk_parents(path):
    """
    Walks up the tree to the root directory.
    """
    while os.path.splitdrive(path)[1] != os.sep:
        yield path
        path = os.path.dirname(path)