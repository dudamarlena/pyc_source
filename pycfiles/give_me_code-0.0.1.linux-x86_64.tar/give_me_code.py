# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/errorcode/lib/python2.7/site-packages/give_me_code.py
# Compiled at: 2016-05-25 23:00:13
import sys
from flask import Flask
app = Flask(__name__)

@app.route('/<int:code>')
def hello_world(code):
    return (str(code), code)


def run():
    if len(sys.argv) < 2:
        print 'Use port to specify server port: %s port' % sys.argv[0]
        port = 8333
    else:
        port = int(sys.argv[1])
    app.run(port=port)


if __name__ == '__main__':
    run()