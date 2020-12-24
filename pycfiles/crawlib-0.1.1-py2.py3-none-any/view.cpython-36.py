# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/tests/dummy_site/_index/view.py
# Compiled at: 2019-12-25 17:43:26
# Size of source mod 2**32: 230 bytes
from flask import Blueprint, render_template
bp = Blueprint('index', __name__, template_folder='templates')

@bp.route('/', methods=['GET'])
def index():
    return render_template('index/index.html')