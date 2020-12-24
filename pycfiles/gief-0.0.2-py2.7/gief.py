# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gief/gief.py
# Compiled at: 2015-12-22 12:01:12
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
    return '\n    <!doctype html>\n    <title>Gimme</title>\n    <h1>Gimme</h1>\n    <form action="" method=post enctype=multipart/form-data>\n      <p><input type=file name=file>\n         <input type=submit value=Upload>\n    </form>\n    '


@app.route('/', methods=['POST'])
def post():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['path'], filename))
    return filename + ' uploaded'