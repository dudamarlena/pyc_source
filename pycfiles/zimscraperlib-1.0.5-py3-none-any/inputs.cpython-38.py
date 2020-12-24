# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/envs/nautilus/lib/python3.8/site-packages/zimscraperlib/inputs.py
# Compiled at: 2020-04-20 12:55:04
# Size of source mod 2**32: 1454 bytes
import shutil, pathlib, tempfile
from . import logger
from .download import save_file

def handle_user_provided_file(source=None, dest=None, in_dir=None, nocopy=False):
    """ downloads or copies a user provided file (URL or path)

        args:
            source: URL or path to a file (or None)
            dest:   pathlib.Path where to save the resulting file
                    using temp filename if None
            in_dir: pathlib.Path to gen dest within if specified
            nocopy: don't make a copy of source if a path was provided.
                    return source value instead
        return:
            pathlib.Path to handled file (or None)
        """
    if source:
        if not source.strip():
            return
        if not dest:
            dest = pathlib.Path(tempfile.NamedTemporaryFile(suffix=(pathlib.Path(source).suffix),
              dir=in_dir,
              delete=False).name)
        if source.startswith('http'):
            logger.debug(f"download {source} -> {dest}")
            save_file(source, dest)
    else:
        source = pathlib.Path(source).expanduser().resolve()
        if not source.exists():
            raise IOError(f"{source} could not be found.")
        if nocopy:
            return source
        logger.debug(f"copy {source} -> {dest}")
        shutil.copy(source, dest)
    return dest