# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/abl/jquery/plugins/form/resources.py
# Compiled at: 2011-02-18 13:05:59
"""
abl.jquery.plugin.form resources

"""
from tw.api import JSLink, CSSLink
from abl.jquery.core import jquery_js
from abl.jquery.plugins.blockUI import jquery_blockUI_js
modname = __name__
form_js = JSLink(filename='static/javascript/jquery.form.js', javascript=[
 jquery_js], modname=modname)
form_widget_css = CSSLink(filename='static/css/form_widget.css', modname=modname)
form_widget_js = JSLink(filename='static/javascript/jquery.form.widget.js', javascript=[
 form_js, jquery_blockUI_js], css=[
 form_widget_css], modname=modname)