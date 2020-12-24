# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tw/yui/autocomplete.py
# Compiled at: 2010-01-27 10:51:41
from tw.api import JSLink
from tw.yui import YUICSSLink, YUIJSLink
autocomplete_css = YUICSSLink(basename='assets/skins/sam/autocomplete', suffix='')
yui_dom_event_js = YUIJSLink(basename='yahoo-dom-event/yahoo-dom-event', suffix='')
datasource_js = YUIJSLink(basename='datasource/datasource')
get_js = YUIJSLink(basename='get/get')
connection_js = YUIJSLink(basename='connection/connection')
animation_js = YUIJSLink(basename='animation/animation')
json_js = YUIJSLink(basename='json/json')
yui_autocomplete_js = YUIJSLink(basename='autocomplete/autocomplete', css=[
 autocomplete_css], javascript=[
 yui_dom_event_js,
 datasource_js,
 get_js,
 connection_js,
 animation_js,
 json_js])
autocomplete_js = JSLink(modname='tw.yui', filename='static/autocomplete/autocomplete.js', javascript=[
 yui_autocomplete_js])
from tw.forms import InputField

class AutoCompleteField(InputField):
    javascript = [
     autocomplete_js]
    engine = 'mako'
    template = 'tw.yui.templates.autocomplete'
    params = ['url']
    url = '.json'