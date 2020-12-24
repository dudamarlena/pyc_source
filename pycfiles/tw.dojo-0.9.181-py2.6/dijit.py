# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/tw/dojo/dijit.py
# Compiled at: 2013-01-02 11:28:41
"""
dijit widgets
"""
from tw.dojo.core import DojoBase, DojoCSSLink
from tw.forms import InputField
dijit_css = DojoCSSLink(basename='dijit/themes/dijit')

class DojoProgressBar(DojoBase):
    require = [
     'dijit.ProgressBar']
    dojoType = 'dijit.ProgressBar'
    params = ['id', 'jsId']
    store = None
    rootLabel = None
    childrenAttrs = None
    onClick = None
    template = '\n    <span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip="">\n    <div dojoType="dijit.ProgressBar"\n         jsId="$jsId" id="$id"></div>\n    </span>'


class DojoCalendarDatePicker(DojoBase):
    require = [
     'dijit._Calendar']
    dojoType = 'dijit._Calendar'
    params = ['jsId', 'onChange']
    template = '\n    <span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip="">\n    <div dojoType="$dojoType"\n         jsId="$jsId" id="$id" onChange="$onChange"></div>\n    </span>'


class DijitRichTextEditor(DojoBase, InputField):
    require = [
     'dijit.Editor']
    dojoType = 'dijit.Editor'
    params = ['id', 'jsId']
    template = '<div/>'
    template = '<div xmlns="http://www.w3.org/1999/xhtml"\n       dojoType="${dojoType}"\n       jsId="${jsId}"\n       xmlns:py="http://genshi.edgewall.org/"\n       type="${type}" name="${name}" class="${css_class}" id="${id}"\n       py:attrs="attrs" \n       value="${value}" />\n       '