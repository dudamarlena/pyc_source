# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyaler/test_app.py
# Compiled at: 2010-07-24 11:44:38
from pyaler import app

@app.route('/')
def index():
    return '<html><title>live</title></html>'