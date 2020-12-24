# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tw/yui/widgets.py
# Compiled at: 2010-01-27 10:56:55
from tw.api import Widget, JSLink, CSSLink
from base import YUICSSLink, YUIJSLink

class element_js(YUIJSLink):
    basename = 'element/element'
    default_suffix = 'beta-min'


class datasource_js(YUIJSLink):
    basename = 'datasource/datasource'


class datatable_js(YUIJSLink):
    basename = 'datatable/datatable'


class json_js(YUIJSLink):
    basename = '/json/json'


class connection_js(YUIJSLink):
    basename = 'connection/connection'


class yahoo_dom_event_js(YUIJSLink):
    basename = 'yahoo-dom-event/yahoo-dom-event'
    default_suffix = ''


class skin_css(YUICSSLink):
    basename = 'assets/skins/sam/skin'
    default_suffix = ''