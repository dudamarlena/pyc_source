# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bhanu/__init__.py
# Compiled at: 2019-02-20 00:24:27
# Size of source mod 2**32: 161 bytes
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, I love Digital Ocean!'


if __name__ == '__main__':
    app.run()