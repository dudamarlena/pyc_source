# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grmaster/server.py
# Compiled at: 2015-05-28 11:03:40
# Size of source mod 2**32: 1879 bytes
"""Http interface for grmaster."""
from grmaster import data, rules, Manager, setting
from flask import Flask, request, Response, abort
import tempfile
APP = Flask(__name__)
INDEX_HTML = data.readbytes('index.' + setting.LANG + '.html')
TEMPLATE_CSV = data.readbytes('template.csv')

@APP.route('/')
def index():
    """Language-specific function."""
    return INDEX_HTML


@APP.route('/template.csv')
def template():
    """One request, one template."""
    return Response(TEMPLATE_CSV, mimetype='text/csv')


@APP.route('/result.csv', methods=['POST'])
def result():
    """Calc and return result."""
    if 'studentfile' not in request.files:
        abort(400)
    with tempfile.TemporaryFile('w+') as (temp_file):
        temp_file.write(str(request.files['studentfile'].read(), encoding='utf-8'))
        temp_file.seek(0)
        manager = Manager(temp_file)
    rules.apply_all(manager)
    return Response(manager.get_result().to_csv(), mimetype='text/csv')


def run(app=APP):
    """Run app."""
    app.run(port=setting.PORT)