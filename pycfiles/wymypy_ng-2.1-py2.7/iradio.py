# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wymypy/plugins/iradio.py
# Compiled at: 2013-12-02 18:01:50
from couchdbkit import *
from flask import render_template_string

class Greeting(Document):
    url = StringProperty()


class Iradio(object):
    has_panel = True
    button_index = 50
    button_label = 'iRadio'
    index_template = '\n<h2>Internet Radio</h2>\n{% for radio in docs %}\n    <li {{ loop.cycle("", "class=\'p\'") }}>\n        <a href=\'#\' onclick=\'load_plugin_content("iradio", "delete", {document_id: "{{ radio["_id"] }}" });\'><span>X</span></a>\n        <a href="#" onclick=\'execute_plugin("iradio", "play", {url: "{{ radio[\'url\'] }}"}, refresh_player);\'>{{ radio[\'url\'] }}</a>\n    </li> \n{% endfor %}\n\n<h3>Add Internet Station:\n    <form onsubmit=\'load_plugin_content("iradio", "add", {url: $("#iradio_url").val()});return false\'>\n        <input type=\'text\' id=\'iradio_url\' size="10"/>\n        <button type=\'submit\'>add</button>\n    </form>\n</h3>\n'

    def __init__(self, mpd, config):
        self.config = config
        self.mpd = mpd
        self.server = Server(uri=self.config.get('couchdb_url', ''))
        self.db = self.server.get_or_create_db('mpd_radio')

    def index(self):
        return render_template_string(self.index_template, docs=[ self.db.get(i['id']) for i in self.db.all_docs().all() ])

    def add(self, url=None):
        self.db.save_doc({'url': url})
        return self.index()

    def delete(self, document_id=None):
        self.db.delete_doc(document_id)
        return self.index()

    def ajax_play(self, url):
        self.mpd.add([url])