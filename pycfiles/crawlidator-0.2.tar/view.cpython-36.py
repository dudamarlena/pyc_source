# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/tests/dummy_site/_index/view.py
# Compiled at: 2019-12-25 17:43:26
# Size of source mod 2**32: 230 bytes
from flask import Blueprint, render_template
bp = Blueprint('index', __name__, template_folder='templates')

@bp.route('/', methods=['GET'])
def index():
    return render_template('index/index.html')