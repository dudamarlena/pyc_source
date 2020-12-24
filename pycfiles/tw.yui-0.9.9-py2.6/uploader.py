# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tw/yui/uploader.py
# Compiled at: 2010-01-27 10:56:55
from base import YUICSSLink, YUIJSLink
from widgets import element_js, datasource_js, datatable_js, yahoo_dom_event_js, skin_css

class uploader_js(YUIJSLink):
    javascript = [
     yahoo_dom_event_js(), element_js(), datasource_js(), datatable_js()]
    css = [skin_css()]
    basename = 'uploader/uploader'