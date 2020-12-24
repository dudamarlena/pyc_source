# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notebookism/app.py
# Compiled at: 2016-10-01 22:45:51
# Size of source mod 2**32: 407 bytes
from flask import Flask
from IPython import get_ipython
app = Flask(__name__)

@app.route('/')
@app.route('/<path:path>')
def hello(path=''):
    if path:
        repo.value = path
        return __x(**get_ipython().user_ns) | repo_template.render > mistune.markdown
    return 'Hello New World!' + path


if __name__ == '__main__':
    app.run(port=5000)