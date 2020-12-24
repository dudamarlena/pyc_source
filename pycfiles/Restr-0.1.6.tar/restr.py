# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nitipit/space/project/restr/restr/restr.py
# Compiled at: 2014-01-27 11:52:45
from appkit.api.v0_2_6 import App
import os, sys
from docutils.core import publish_parts
from jinja2 import Template
app = App(__name__)
try:
    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        open(file_name, 'w').close()
except:
    file_name = None

app.file_name = file_name

@app.route('/')
def index():
    ui_path = os.path.join(os.path.dirname(__file__), 'ui.html')
    template = Template(open(ui_path).read())
    text = None
    if app.file_name is not None:
        text = open(file_name).read()
    return template.render(file_name=app.file_name, text=text)


@app.route('/rst2html/')
def rst2html():
    dom_document = app.webkit_web_view.get_dom_document()
    html = dom_document.get_element_by_id('editor').get_value()
    html = publish_parts(html, writer_name='html')['html_body']
    return html


@app.route('/save/')
def save():
    """save markdown content to the file"""
    document = app.webkit_web_view.get_dom_document()
    file_name = document.get_element_by_id('file').get_value()
    md = document.get_element_by_id('editor').get_value()
    f = open(file_name, 'w')
    f.write(md)
    f.close()
    return 'Saved'


if __name__ == '__main__':
    app.run()