# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jakob/JaloLite/Jalapeno/GUI/views/welcome.py
# Compiled at: 2017-03-30 22:43:35
# Size of source mod 2**32: 167 bytes
from flask import Blueprint, render_template
welcome = Blueprint('welcome', __name__)

@welcome.route('/welcome')
def show():
    return render_template('welcome.html')