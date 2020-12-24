# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/raj/__init__.py
# Compiled at: 2019-03-07 00:47:11
# Size of source mod 2**32: 186 bytes
from flask import Flask
from flask import viwes
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, I love Digital Ocean!'


if __name__ == '__main__':
    app.run()