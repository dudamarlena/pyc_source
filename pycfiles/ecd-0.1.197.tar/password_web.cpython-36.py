# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\pycharm_project\ecd\ecd\password_manage\app\password_web.py
# Compiled at: 2019-05-07 08:38:10
# Size of source mod 2**32: 573 bytes
"""
@author:ZouLingyun
@date:
@summary:
"""
import time
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from ecd.password_manage.app.handle_data import HandleData
hd = HandleData()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/suggest/')
def password():
    keyword = request.args.get('keyword', None)
    hits = hd.search(keyword, 20)
    return jsonify(hits)


if __name__ == '__main__':
    pass