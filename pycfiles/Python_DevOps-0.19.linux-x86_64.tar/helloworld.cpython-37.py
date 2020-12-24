# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/helloworld.py
# Compiled at: 2019-09-27 10:03:27
# Size of source mod 2**32: 181 bytes
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello Python DevOps :)!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')