# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wymypy/plugins/library.py
# Compiled at: 2013-12-02 16:55:35
import os
from flask import render_template_string

class Library(object):
    has_panel = True
    button_index = 1
    button_label = 'Library'
    index_template = '\n<h2>\n    {% for path_element in path %}\n        <a href="#" onclick=\'load_plugin_content("library", "index", {path: "{{ "/".join(path[:loop.index]) }}"})\'>{{ path_element }}</a>\n        {% if not loop.last %}/{% else %}\n            <a href="#" onclick=\'execute_plugin("library", "add", {file_name: "{{ path|join("/") }}"}, refresh_player);\'><span>></span></a>\n        {% endif %}\n    {% else %}\n        Library\n    {% endfor %}\n</h2>\n\n{% for dir in dirs %}\n    <li {{ loop.cycle("", "class=\'p\'") }}><a href="#" onclick="load_plugin_content(\'library\', \'index\', {path: \'{{ dir }}\'});">{{ basename(dir) }}</a></li> \n{% endfor %}\n\n{% for file in files %}\n    <li {{ loop.cycle("", "class=\'p\'") }}><a href="#" onclick=\'execute_plugin("library", "add", {file_name: "{{ file }}"}, refresh_player);\'>{{ basename(file) }}</a></li> \n{% endfor %}\n'

    def __init__(self, mpd, config):
        self.config = config
        self.mpd = mpd

    def index(self, path=''):
        return render_template_string(self.index_template, basename=os.path.basename, path=path.split('/') if path else [], dirs=self.mpd.ls([path], onlyDirs=True), files=self.mpd.ls([path], onlyFiles=True))

    def ajax_add(self, file_name):
        self.mpd.add([file_name])