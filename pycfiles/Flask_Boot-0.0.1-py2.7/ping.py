# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/flask_boot/project/application/api/ping.py
# Compiled at: 2018-09-06 05:23:29
from __future__ import absolute_import, division, print_function
from flask import Blueprint
ping_bp = Blueprint('ping', __name__)

@ping_bp.route('/ping', methods=['GET', 'POST'])
def ping():
    return 'pong'