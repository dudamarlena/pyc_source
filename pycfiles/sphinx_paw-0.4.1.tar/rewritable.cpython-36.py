# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amarin/dev/sphinx-mediatel/src/sphinx_paw/rewritable.py
# Compiled at: 2019-11-19 17:00:50
# Size of source mod 2**32: 1413 bytes
"""Allow default templates and configuration files redefinition locally"""
from sphinx.util import logging
from os import path
from sphinx.application import Sphinx
from sphinx.util import console
from sphinx_paw.constants import NOTSET
DEFAULT_PATH = path.join(path.dirname(__file__), 'defaults')
logger = logging.getLogger(__name__)

def rewritable_file_path(app, filename, local_path=NOTSET, default_path=NOTSET):
    """Get filepath in documentation src or default in sphinx_paw"""
    if not isinstance(app, Sphinx):
        raise AssertionError
    else:
        src_dir = app.srcdir
        if local_path:
            found_path = path.join(src_dir, local_path, filename)
        else:
            found_path = path.join(src_dir, filename)
    if path.exists(found_path):
        logger.info(f"Using local {console.bold(filename)}")
        return found_path
    else:
        if default_path is NOTSET:
            default_path = DEFAULT_PATH
        else:
            if default_path is None:
                raise FileNotFoundError(f"Local file {found_path} not found")
        logger.info(f"Using {console.bold('default')} {filename}")
        return path.join(default_path, filename)


def rewritable_file_content(app, filename):
    """Get rewritable file content"""
    assert isinstance(app, Sphinx)
    file_path = rewritable_file_path(app, filename, DEFAULT_PATH)
    with open(file_path, 'rb') as (content_fh):
        content = content_fh.read().decode()
        return content