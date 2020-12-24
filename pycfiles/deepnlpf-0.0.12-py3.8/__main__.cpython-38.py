# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/dashboard/__main__.py
# Compiled at: 2019-07-25 21:28:13
# Size of source mod 2**32: 138 bytes
from .app import app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)