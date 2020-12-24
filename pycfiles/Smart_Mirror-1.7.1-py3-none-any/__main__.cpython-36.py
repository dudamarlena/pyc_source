# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: smart_mirror/__main__.py
# Compiled at: 2018-09-24 17:48:57
# Size of source mod 2**32: 277 bytes
from smart_mirror.app import app, socketio

def main():
    socketio.run(app, host='0.0.0.0', log_output=False)


if __name__ == '__main__':
    main()