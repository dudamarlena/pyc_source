# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nbollweg/Documents/projects/widget-dateslider/dateslider/widgets.py
# Compiled at: 2016-05-08 11:40:24
# Size of source mod 2**32: 604 bytes
from datetime import datetime, timedelta
from traitlets import Unicode
from ipywidgets import DOMWidget
from .traits import Date
jsmodule = 'nbextensions/dateslider/index'
now = datetime.now()

class DateSlider(DOMWidget):
    _view_module = Unicode(jsmodule).tag(sync=True)
    _view_name = Unicode('DateSliderView').tag(sync=True)
    _model_module = Unicode(jsmodule).tag(sync=True)
    _model_name = Unicode('DateSliderModel').tag(sync=True)
    value = Date(now).tag(sync=True)
    start = Date(now - timedelta(days=365)).tag(sync=True)
    end = Date(now + timedelta(days=365)).tag(sync=True)