# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tw\paste_template.py
# Compiled at: 2010-01-12 20:05:44
import os, datetime
from pkg_resources import get_distribution, require
require('PasteScript')
from paste.script.templates import Template, var

class ToscaWidgetsTemplate(Template):
    __module__ = __name__
    _template_dir = os.path.join(get_distribution('ToscaWidgets').location, 'tw', 'paste_templates', 'widget_template')
    summary = 'ToscaWidgets widget'
    vars = [
     var('widget_name', 'Name of the widget package (tw.XXX)'), var('version', 'Version', default='0.1a0'), var('description', 'One-line description of the widget'), var('long_description', 'Multi-line description (in reST)'), var('author', 'Author name'), var('author_email', 'Author email'), var('url', 'URL of homepage'), var('license_name', 'License name')]

    def run(self, command, output_dir, vars):
        vars['year'] = str(datetime.datetime.now().year)
        vars['package'] = vars['widget_name'] or vars['package']
        super(ToscaWidgetsTemplate, self).run(command, output_dir, vars)