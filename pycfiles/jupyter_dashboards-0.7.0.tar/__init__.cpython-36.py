# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/dashboards/jupyter_dashboards/__init__.py
# Compiled at: 2017-03-21 21:09:05
# Size of source mod 2**32: 372 bytes


def _jupyter_nbextension_paths():
    """API for JS extension installation on notebook>=4.2"""
    return [
     {'section':'notebook', 
      'src':'nbextension', 
      'dest':'jupyter_dashboards', 
      'require':'jupyter_dashboards/notebook/main'}]