# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/simiki/utils.py
# Compiled at: 2017-06-02 11:17:28
from __future__ import print_function, unicode_literals, absolute_import
import os, sys, os.path, shutil, errno, logging, io, hashlib, simiki
from simiki.compat import unicode
logger = logging.getLogger(__name__)
COLOR_CODES = {b'reset': b'\x1b[0m', 
   b'black': b'\x1b[1;30m', 
   b'red': b'\x1b[1;31m', 
   b'green': b'\x1b[1;32m', 
   b'yellow': b'\x1b[1;33m', 
   b'blue': b'\x1b[1;34m', 
   b'magenta': b'\x1b[1;35m', 
   b'cyan': b'\x1b[1;36m', 
   b'white': b'\x1b[1;37m', 
   b'bgred': b'\x1b[1;41m', 
   b'bggrey': b'\x1b[1;100m'}

def color_msg(color, msg):
    return COLOR_CODES[color] + msg + COLOR_CODES[b'reset']


def check_extension(filename):
    """Check if the file extension is in the allowed extensions

    The `fnmatch` module can also get the suffix:
        patterns = ["*.md", "*.mkd", "*.markdown"]
        fnmatch.filter(files, pattern)
    """
    exts = [ (b'.{0}').format(e) for e in simiki.allowed_extensions ]
    return os.path.splitext(filename)[1] in exts


def copytree(src, dst, symlinks=False, ignore=None):
    """Copy from source directory to destination"""
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def emptytree(directory, exclude_list=None):
    """Delete all the files and dirs under specified directory"""
    if not isinstance(directory, unicode):
        directory = unicode(directory, b'utf-8')
    if not exclude_list:
        exclude_list = []
    for p in os.listdir(directory):
        if p in exclude_list:
            continue
        fp = os.path.join(directory, p)
        if os.path.isdir(fp):
            try:
                shutil.rmtree(fp)
                logger.debug(b'Delete directory %s', fp)
            except OSError as e:
                logger.error(b'Unable to delete directory %s: %s', fp, unicode(e))

        elif os.path.isfile(fp):
            try:
                logging.debug(b'Delete file %s', fp)
                os.remove(fp)
            except OSError as e:
                logger.error(b'Unable to delete file %s: %s', fp, unicode(e))

        else:
            logger.error(b'Unable to delete %s, unknown filetype', fp)


def mkdir_p(path):
    """Make parent directories as needed, like `mkdir -p`"""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def listdir_nohidden(path):
    """List not hidden files or directories under path"""
    for f in os.listdir(path):
        if isinstance(f, str):
            f = unicode(f)
        if not f.startswith(b'.'):
            yield f


def write_file(filename, content):
    """Write content to file."""
    _dir, _ = os.path.split(filename)
    if not os.path.exists(_dir):
        logging.debug(b'The directory %s not exists, create it', _dir)
        mkdir_p(_dir)
    with io.open(filename, b'wt', encoding=b'utf-8') as (fd):
        fd.write(content)


def get_md5(filename):
    with open(filename, b'rb') as (fd):
        md5_hash = hashlib.md5(fd.read()).hexdigest()
    return md5_hash


def get_dir_md5(dirname):
    """Get md5 sum of directory"""
    md5_hash = hashlib.md5()
    for root, dirs, files in os.walk(dirname):
        dirs[:] = sorted(dirs)
        for f in sorted(files):
            with open(os.path.join(root, f), b'rb') as (fd):
                md5_hash.update(fd.read())

    md5_hash = md5_hash.hexdigest()
    return md5_hash


def import_string(import_name, silent=False):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).
    If `silent` is True the return value will be `None` if the import fails.
    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    import_name = str(import_name).replace(b':', b'.')
    try:
        try:
            __import__(import_name)
        except ImportError:
            if b'.' not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit(b'.', 1)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            module = import_string(module_name)

        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)

    except ImportError as e:
        if not silent:
            raise ImportError(e)

    return


if __name__ == b'__main__':
    print(color_msg(b'black', b'Black'))
    print(color_msg(b'red', b'Red'))
    print(color_msg(b'green', b'Green'))
    print(color_msg(b'yellow', b'Yellow'))
    print(color_msg(b'blue', b'Blue'))
    print(color_msg(b'magenta', b'Magenta'))
    print(color_msg(b'cyan', b'Cyan'))
    print(color_msg(b'white', b'White'))
    print(color_msg(b'bgred', b'Background Red'))
    print(color_msg(b'bggrey', b'Background Grey'))