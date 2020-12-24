# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adam/Documents/src/Venvs/lsq/lib/python3.7/site-packages/jupyterlab_lsstquery/__init__.py
# Compiled at: 2018-04-05 13:19:57
# Size of source mod 2**32: 694 bytes
"""
Python module to initialize Server Extension (& Notebook Extension?)
"""
from jupyterlab_lsstquery.handlers import setup_handlers

def _jupyter_server_extension_paths():
    """
    Function to declare Jupyter Server Extension Paths.
    """
    return [
     {'module': 'jupyterlab_lsstquery'}]


def load_jupyter_server_extension(nbapp):
    """
    Function to load Jupyter Server Extension.
    """
    nbapp.log.info('Loading lsstquery server extension.')
    setup_handlers(nbapp.web_app)