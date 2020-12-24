# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/statesofusa/main.py
# Compiled at: 2016-03-09 12:27:58
__author__ = 'Isham'
from app import app, api
from us_states_api import USStates
api.add_resource(USStates, '/states/')
if __name__ == '__main__':
    app.run(debug=True)