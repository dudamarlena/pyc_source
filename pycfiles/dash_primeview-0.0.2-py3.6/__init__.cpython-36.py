# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dash_primeview\__init__.py
# Compiled at: 2018-03-17 08:49:56
# Size of source mod 2**32: 827 bytes
import os as _os, dash as _dash, sys as _sys
from .version import __version__
_current_path = _os.path.dirname(_os.path.abspath(__file__))
_components = _dash.development.component_loader.load_components(_os.path.join(_current_path, 'metadata.json'), 'dash_primeview')
_this_module = _sys.modules[__name__]
_js_dist = [
 {'relative_package_path':'bundle.js', 
  'external_url':'https://unpkg.com/dash-primeview@{}/dash_primeview/bundle.js'.format(__version__), 
  'namespace':'dash_primeview'}]
_css_dist = []
for _component in _components:
    setattr(_this_module, _component.__name__, _component)
    setattr(_component, '_js_dist', _js_dist)
    setattr(_component, '_css_dist', _css_dist)