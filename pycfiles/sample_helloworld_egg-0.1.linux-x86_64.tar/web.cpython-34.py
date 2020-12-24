# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsufitch/helloworld_egg/lib/python3.4/site-packages/helloworld/web.py
# Compiled at: 2014-05-20 17:48:39
# Size of source mod 2**32: 370 bytes
import sys
from helloworld.hello import Hello
from flask import Flask
app = Flask(__name__)
greeter = None

@app.route('/')
def hello():
    global greeter
    return greeter.message


def main():
    global greeter
    message = ' '.join(sys.argv[1:])
    if not message:
        print('Please input some sort of message')
    else:
        greeter = Hello(message)
        app.run()