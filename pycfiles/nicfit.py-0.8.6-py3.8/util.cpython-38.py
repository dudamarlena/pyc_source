# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/util.py
# Compiled at: 2018-04-10 23:05:37
# Size of source mod 2**32: 3011 bytes
import os, sys, gettext, contextlib
from pathlib import Path
from .logger import getLogger
try:
    import ipdb as _debugger
except ImportError:
    import pdb as _debugger
else:
    log = getLogger(__name__)

    @contextlib.contextmanager
    def cd(path):
        """Context manager that changes to directory `path` and return to CWD
    when exited.
    """
        old_path = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(old_path)


    def copytree(src, dst, symlinks=True):
        """
    Modified from shutil.copytree docs code sample, merges files rather than
    requiring dst to not exist.
    """
        from shutil import copy2, Error, copystat
        names = os.listdir(src)
        if not Path(dst).exists():
            os.makedirs(dst)
        errors = []
        for name in names:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            try:
                if symlinks and os.path.islink(srcname):
                    linkto = os.readlink(srcname)
                    os.symlink(linkto, dstname)
                else:
                    if os.path.isdir(srcname):
                        copytree(srcname, dstname, symlinks)
                    else:
                        copy2(srcname, dstname)
            except OSError as why:
                try:
                    errors.append((srcname, dstname, str(why)))
                finally:
                    why = None
                    del why

            except Error as err:
                try:
                    errors.extend(err.args[0])
                finally:
                    err = None
                    del err

        else:
            try:
                copystat(src, dst)
            except OSError as why:
                try:
                    if why.winerror is None:
                        errors.extend((src, dst, str(why)))
                finally:
                    why = None
                    del why

            else:
                if errors:
                    raise Error(errors)


    def initGetText(domain, install=False, fallback=True):
        locale_paths = [Path(__file__).parent / '..' / 'locale',
         Path(sys.prefix) / 'share' / 'locale']
        locale_dir, translation = (None, None)
        for locale_dir in [d for d in locale_paths if d.exists()]:
            if gettext.find(domain, str(locale_dir)):
                log.debug('Loading message catalogs from {}'.format(locale_dir))
                translation = gettext.translation(domain, str(locale_dir))
                break
            if translation is None:
                translation = gettext.translation(domain, (str(locale_dir)), fallback=fallback)
            assert translation
            if install:
                gettext.install(domain, (str(locale_dir)), names=['ngettext'])
            return translation


    def debugger():
        """If called in the context of an exception, calls post_mortem; otherwise
    set_trace.
    ``ipdb`` is preferred over ``pdb`` if installed.
    """
        e, m, tb = sys.exc_info()
        if tb is not None:
            _debugger.post_mortem(tb)
        else:
            _debugger.set_trace()