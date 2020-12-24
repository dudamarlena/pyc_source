# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/orlo/routes/internal.py
# Compiled at: 2017-04-04 09:14:06
from __future__ import print_function
from flask import jsonify
from orlo.app import app
from orlo import __version__
__author__ = 'alforbes'

@app.route('/internal/version', methods=['GET'])
def internal_version():
    """
    Get the running version of Orlo
    :return:
    """
    return jsonify({'version': __version__})