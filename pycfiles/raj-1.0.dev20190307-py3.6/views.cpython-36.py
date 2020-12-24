# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/raj/views.py
# Compiled at: 2019-03-07 00:36:55
# Size of source mod 2**32: 138 bytes
from flask import Flask
app = Flask(__name__)

@app.route('/add')
def add(a, b):
    z = a + b


add()
if __name__ == '__main__':
    app.run()