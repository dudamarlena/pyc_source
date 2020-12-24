# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wymypy/plugins/search.py
# Compiled at: 2013-12-02 17:13:33
import os
from flask import render_template_string

class Search(object):
    has_panel = True
    button_index = 100
    button_label = ''
    button_html = '\n        <form onsubmit=\'load_plugin_content("search", "index", {search_type: $("#tq").val(), term:$("#q").val()}); return false\'>\n            <input type=\'text\' id=\'q\' size="10"/>\n            <select id=\'tq\'>\n                <option value=\'filename\'>filename</option>\n                <option value=\'artist\'>artist</option>\n                <option value=\'album\'>album</option>\n                <option value=\'title\'>title</option>\n            </select>\n            <button type=\'submit\'>Search</button>\n        </form>\n    '
    index_template = '\n<h2> Search for \'{{ term }}\' in {{ search_type }}</h2>\n\n{% for result in results %}\n    <li {{ loop.cycle("", "class=\'p\'") }}><a href="#" onclick=\'execute_plugin("search", "add", {file_name: "{{ result }}"}, refresh_player);\'>{{ result }}</a></li> \n{% endfor %}\n'

    def __init__(self, mpd, config):
        self.config = config
        self.mpd = mpd

    def index(self, term, search_type):
        print repr(search_type)
        return render_template_string(self.index_template, term=term, search_type=search_type, results=self.mpd.search(search_type, term))

    def ajax_add(self, file_name):
        self.mpd.add([file_name])