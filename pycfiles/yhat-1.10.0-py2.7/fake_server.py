# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/fake_server.py
# Compiled at: 2017-04-26 17:15:42
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    username = request.args.get('username', '')
    apikey = request.args.get('apikey', '')
    print 'username: ' + username
    print 'apikey: ' + apikey
    return ('{"success": "true"}', 200)


@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    print request
    return ('You send a request to: %s\n' % path, 200)


if __name__ == '__main__':
    app.run()